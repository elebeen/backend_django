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

    # Descripción: Verifica que un usuario nuevo se registre exitosamente
    def test_registro_exitoso(self):
        data = {"username": "omar", "password": "123456"}
        response = self.client.post(self.registro_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["mensaje"], "Usuario creado exitosamente.")
        self.assertTrue(User.objects.filter(username="omar").exists())

    # Descripción: Verifica que no se permita registrar un usuario ya existente
    def test_registro_usuario_duplicado(self):
        User.objects.create_user(username="omar", password="123456")
        data = {"username": "omar", "password": "otro123"}
        response = self.client.post(self.registro_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # Descripción: Verifica que no se permita registrar con campos vacíos
    def test_registro_campos_vacios(self):
        data = {"username": "", "password": ""}
        response = self.client.post(self.registro_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    # Descripción: Verifica que se obtenga un token JWT válido con credenciales correctas
    def test_login_token_exitoso(self):
        User.objects.create_user(username="omar", password="123456")
        data = {"username": "omar", "password": "123456"}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    # Descripción: Verifica que login falle con credenciales incorrectas
    def test_login_falla_credenciales_incorrectas(self):
        User.objects.create_user(username="omar", password="123456")
        data = {"username": "omar", "password": "incorrecta"}
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
