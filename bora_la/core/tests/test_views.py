from bora_la.wsgi import *
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models import Usuario
from django.test import RequestFactory
from core.views import cadastrar_usuario, logar_usuario, deslogar_usuario, listar_eventos
import pytest

class TestUsuario(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

    def test_cadastrar_usuario(self):
        url = reverse("cadastrar_usuario")
        data = {
            "username": "testuser",
            "password1": "testpass123",
            "password2": "testpass123",
            "nome": "Test User",
            "email": "test@example.com",
            "telefone": "1234567890",
            "whatsapp": "1234567890",
            "user_type": "1",
            "pref_categorias[]": ["comida", "ar_livre"],
            "razao_social": "Test Company",
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)  

        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user)

        usuario = Usuario.objects.filter(django_user=user).first()
        self.assertIsNotNone(usuario)
        self.assertEqual(usuario.nome, "Test User")
        self.assertEqual(usuario.email, "test@example.com")
        self.assertEqual(usuario.whats, "1234567890")
        self.assertEqual(usuario.tipo_usuario, 1)
        self.assertEqual(usuario.razao_social, "Test Company")
        self.assertIn("comida", usuario.pref_categorias)
        self.assertIn("ar_livre", usuario.pref_categorias)

    def test_logar_usuario(self):
        User.objects.create_user(username="testuser", password="testpass123")
        url = reverse("logar_usuario")
        data = {"username": "testuser", "password": "testpass123"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302) 

    def test_deslogar_usuario(self):
        url = reverse("deslogar_usuario")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_listar_eventos_unauthenticated(self):
        url = reverse("listar_eventos")

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context.get("tipo_usuario"))