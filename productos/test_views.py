# productos/tests/test_views.py

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

class ViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registro_url = reverse('registro')  # asegúrate de tener esto en tus urls.py
        self.token_url = reverse('token_obtain_pair')  # asegúrate de tener esto en tus urls.py

    # 🧪 Prueba 1: Registro exitoso
    def test_registro_exitoso(self):
        data = {"username": "omar", "password": "123456"}
        response = self.client.post(self.registro_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["mensaje"], "Usuario creado exitosamente.")
        self.assertTrue(User.objects.filter(username="omar").exists())

    # 🧪 Prueba 2: Registro de usuario duplicado
    def test_registro_usuario_duplicado(self):
        User.objects.create_user(username="omar", password="123456")
        data = {"username": "omar", "password": "otro123"}
        response = self.client.post(self.registro_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # 🧪 Prueba 3: Registro con campos vacíos
    def test_registro_campos_vacios(self):
        data = {"username": "", "password": ""}
        response = self.client.post(self.registro_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # 🧪 Prueba 4: Login exitoso con token válido
    def test_login_token_exitoso(self):
        User.objects.create_user(username="omar", password="123456")
        data = {"username": "omar", "password": "123456"}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # 🧪 Prueba 5: Login con credenciales incorrectas
    def test_login_falla_credenciales_incorrectas(self):
        User.objects.create_user(username="omar", password="123456")
        data = {"username": "omar", "password": "incorrecta"}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 🧪 Prueba 6: Login con usuario inexistente
    def test_login_usuario_no_existente(self):
        data = {"username": "desconocido", "password": "123456"}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # 🧪 Prueba 7: Registro sin contraseña
    def test_registro_sin_password(self):
        data = {"username": "omar"}
        response = self.client.post(self.registro_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # 🧪 Prueba 8: Registro sin username
    def test_registro_sin_username(self):
        data = {"password": "123456"}
        response = self.client.post(self.registro_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # 🧪 Prueba 9: Registro con contraseña muy corta
    def test_registro_password_muy_corto(self):
        data = {"username": "omar", "password": "12"}
        response = self.client.post(self.registro_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
