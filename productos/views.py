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
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Todos los campos son obligatorios."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Este usuario ya existe."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({"mensaje": "Usuario creado exitosamente."}, status=status.HTTP_201_CREATED)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
