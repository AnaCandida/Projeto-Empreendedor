from bora_la.wsgi import *
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models import Usuario, Evento, Categoria
from django.test import RequestFactory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import authenticate
from django.test import Client

from core.views import (
    cadastrar_usuario,
    logar_usuario,
    deslogar_usuario,
    listar_eventos,
    cadastrar_evento,
)
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile


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


class TestCadastrarEvento(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(username="testuser", password="testpass123")
        cls.usuario = Usuario.objects.create(
            django_user=cls.user,
            nome="Test User",
            email="test@example.com",
            whats="1234567890",
            tipo_usuario=2,
            razao_social="Test Company",
        )
        cls.categoria1 = Categoria.objects.create(nome="Categoria1")
        cls.categoria2 = Categoria.objects.create(nome="Categoria2")
        cls.client = Client()

    def test_cadastrar_evento(self):
        url = reverse("cadastrar_evento")
        image_content = b"image_content"
        image = SimpleUploadedFile("test.png", image_content, content_type="image/png")
        data = {
            "nome_evento": "Meu Evento",
            "descricao_evento": "Descrição do evento",
            "preco_evento": "50.00",
            "image": image,
            "data_evento": "2023-09-01T00:00",
            "endereco_evento": "Localização do evento",
            "pref_categorias[]": [str(self.categoria1.id), str(self.categoria2.id)],
        }

        self.client.force_login(self.user)
        request = self.client.post(url, data)
        eventos_criados = Evento.objects.filter(nome="Meu Evento")
        self.assertEqual(eventos_criados.count(), 1)
        self.assertEqual(eventos_criados[0].organizador_id, self.usuario)
        # self.assertEqual(list(evento_criado.categorias_id.all()), [self.categoria1, self.categoria2])

    def test_ver_tela_cadastrar_evento_metodo(self):
        url = reverse("cadastrar_evento")
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
