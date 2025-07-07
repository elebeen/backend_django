from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Categoria, Producto, Reseña
from .serializers import CategoriaSerializer, ProductoSerializer, ReseñaSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializers import CustomTokenObtainPairSerializer
from rest_framework.decorators import action # Importar action
from django.db import transaction # Importar transaction para asegurar atomicidad
from django.shortcuts import get_object_or_404 

# 🔹 ViewSet para Categorías
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# 🔹 ViewSet para Productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_fields = ['categoria', 'disponible']

    @action(detail=True, methods=['post'])
    def decrementar_stock(self, request, pk=None):
        """
        Decrementa el stock de un producto específico.
        Requiere un 'cantidad' en el cuerpo de la solicitud.
        """
        producto = get_object_or_404(Producto, pk=pk)
        cantidad_a_decrementar = request.data.get('cantidad')

        if not cantidad_a_decrementar:
            return Response({"error": "La cantidad a decrementar es requerida."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cantidad_a_decrementar = int(cantidad_a_decrementar)
            if cantidad_a_decrementar <= 0:
                return Response({"error": "La cantidad debe ser un número positivo."}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "La cantidad debe ser un número entero."}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Volvemos a cargar el producto dentro de la transacción para asegurar que tenemos el stock más reciente.
            # Esto es importante para evitar condiciones de carrera en entornos concurrentes.
            producto.refresh_from_db()
            
            if producto.stock >= cantidad_a_decrementar:
                producto.stock -= cantidad_a_decrementar
                producto.save()
                return Response({"mensaje": f"Stock de {producto.nombre} decremented en {cantidad_a_decrementar}. Stock actual: {producto.stock}"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": f"Stock insuficiente para {producto.nombre}. Stock actual: {producto.stock}"}, status=status.HTTP_400_BAD_REQUEST)

# 🔹 ViewSet para Reseñas
class ReseñaViewSet(viewsets.ModelViewSet):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer

# ✅ Vista personalizada para registrar usuarios
class RegistroView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Todos los campos son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 6:
            return Response({"error": "La contraseña debe tener al menos 6 caracteres."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Este usuario ya existe."}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        return Response({"mensaje": "Usuario creado exitosamente."}, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
