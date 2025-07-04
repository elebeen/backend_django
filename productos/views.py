from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Categoria, Producto, Reseña
from .serializers import CategoriaSerializer, ProductoSerializer, ReseñaSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .token_serializers import CustomTokenObtainPairSerializer



# 🔹 ViewSet para Categorías
class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

# 🔹 ViewSet para Productos
class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filterset_fields = ['categoria', 'disponible']

# 🔹 ViewSet para Reseñas
class ReseñaViewSet(viewsets.ModelViewSet):
    queryset = Reseña.objects.all()
    serializer_class = ReseñaSerializer

# ✅ Vista personalizada para registrar usuarios
class RegistroView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Se requieren 'username' y 'password'."}, status=400)

        if len(password) < 6:
            return Response({"error": "La contraseña debe tener al menos 6 caracteres."}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "El usuario ya existe."}, status=400)

        user = User.objects.create_user(username=username, password=password)
        return Response({"mensaje": "Usuario creado exitosamente."}, status=201)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
