from bora_la.wsgi import *
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models import Usuario, Evento, Categoria
from django.test import RequestFactory
from core.views import (
    cadastrar_usuario,
    logar_usuario,
    deslogar_usuario,
    listar_eventos,
    cadastrar_evento,
)
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


# Teste unitário funcionalidade cadastrar_evento #
class TestCadastrarEvento(TestCase):
    def rf():
        return RequestFactory()

    def user():
        user = Usuario.objects.create_user(
            username="testuser",
            password="testpass123",
        )
        return user

    def categorias():
        return [
            Categoria.objects.create(nome="Categoria1"),
            Categoria.objects.create(nome="Categoria2"),
        ]

    @pytest.fixture
    def post_data(categorias):
        return {
            "nome_evento": "Meu Evento",
            "descricao_evento": "Descrição do evento",
            "preco_evento": "50.00",
            "data_evento": "2023-09-01",
            "endereco_evento": "Localização do evento",
            "pref_categorias[]": [str(cat.id) for cat in categorias],
        }

    @pytest.mark.django_db
    def test_cadastrar_evento(rf, user, categorias, post_data):
        request = rf.post("/cadastrar_evento/", data=post_data)
        request.user = user

        response = cadastrar_evento(request)

        assert response.status_code == 302  # Verifique se o redirecionamento ocorreu
        eventos_criados = Evento.objects.filter(nome="Meu Evento")
        assert eventos_criados.count() == 1
        evento_criado = eventos_criados.first()
        assert evento_criado.organizador_id == Usuario  # Substitua pelo campo correto
        assert list(evento_criado.categorias_id.all()) == categorias

        # Teste para o caso em que a criação do evento falha
        with pytest.raises(Exception):
            request_with_error = rf.post("/cadastrar_evento/", data={})
            request_with_error.user = user
            cadastrar_evento(request_with_error)

        # Teste para o caso em que o método não é POST
        request_get = rf.get("/cadastrar_evento/")
        request_get.user = user
        response_get = cadastrar_evento(request_get)
        assert response_get.status_code == 200
