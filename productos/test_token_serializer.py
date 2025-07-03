# productos/tests/test_token_serializer.py

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from productos.token_serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class CustomTokenObtainPairSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="omar", password="123456")

    # Descripción: Verifica que el token generado incluya el campo personalizado 'username'
    def test_token_incluye_username(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertIn("username", token)
        self.assertEqual(token["username"], "omar")

    # Descripción: Verifica que el token generado sea una instancia válida de RefreshToken
    def test_token_es_instancia_refresh_token(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertIsInstance(token, RefreshToken)

    # Descripción: Verifica que el token contenga los campos estándar de JWT (como 'user_id' y 'exp')
    def test_token_contiene_campos_basicos(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertIn("user_id", token)
        self.assertIn("exp", token)
        self.assertIn("username", token)

    # Descripción: Verifica que el campo personalizado 'username' refleje correctamente el username actual
    def test_username_personalizado_refleja_usuario_actual(self):
        self.user.username = "nuevo_nombre"
        self.user.save()
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertEqual(token["username"], "nuevo_nombre")
