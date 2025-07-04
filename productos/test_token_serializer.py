# productos/tests/test_token_serializer.py

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from productos.token_serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.exceptions import TokenError
import time

class CustomTokenObtainPairSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="omar", password="123456")

    # 🧪 Prueba 1: El token incluye el campo personalizado 'username'
    def test_token_incluye_username(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertIn("username", token)
        self.assertEqual(token["username"], "omar")

    # 🧪 Prueba 2: El token es una instancia de RefreshToken
    def test_token_es_instancia_refresh_token(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertIsInstance(token, RefreshToken)

    # 🧪 Prueba 3: El token contiene campos estándar
    def test_token_contiene_campos_basicos(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertIn("user_id", token)
        self.assertIn("exp", token)
        self.assertIn("username", token)

    # 🧪 Prueba 4: El token refleja cambios en el username del usuario
    def test_username_personalizado_refleja_usuario_actual(self):
        self.user.username = "nuevo_nombre"
        self.user.save()
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertEqual(token["username"], "nuevo_nombre")

    # 🧪 Prueba 5: El token contiene el ID correcto del usuario
    def test_token_contiene_user_id_correcto(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertEqual(token["user_id"], self.user.id)

    # 🧪 Prueba 6: El token generado puede serializarse a string sin errores
    def test_token_es_valido_y_convertible_a_string(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        try:
            token_str = str(token)
            self.assertIsInstance(token_str, str)
            self.assertGreater(len(token_str), 0)
        except TokenError:
            self.fail("El token generado no es válido o no se puede convertir a string.")

    # 🧪 Prueba 7: El token no contiene campos innecesarios
    def test_token_no_contiene_campos_innecesarios(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        campos_esperados = {"user_id", "exp", "username", "jti", "iat", "token_type"}
        self.assertTrue(set(token.payload.keys()).issubset(campos_esperados))


    # 🧪 Prueba 8: El campo 'exp' tiene una expiración válida
    def test_token_exp_tiene_valor_esperado(self):
        token = CustomTokenObtainPairSerializer.get_token(self.user)
        self.assertGreater(token["exp"], int(time.time()))

    # 🧪 Prueba 9: El token cambia en cada generación (no es reutilizable)
    def test_token_distinto_en_generaciones_diferentes(self):
        token1 = str(CustomTokenObtainPairSerializer.get_token(self.user))
        token2 = str(CustomTokenObtainPairSerializer.get_token(self.user))
        self.assertNotEqual(token1, token2)
