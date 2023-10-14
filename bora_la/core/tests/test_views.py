from bora_la.wsgi import *
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from core.models import Usuario, Evento, Categoria
from django.test import RequestFactory
from django.test import Client
from decimal import Decimal


from core.views import (
    cadastrar_usuario,
    logar_usuario,
    deslogar_usuario,
    listar_eventos,
    cadastrar_evento,
)
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile


class TestCadastroUsuario(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.categoria1 = Categoria.objects.create(nome="Categoria1")
        cls.categoria2 = Categoria.objects.create(nome="Categoria2")

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
            "pref_categorias[]": [
                str(self.categoria1.id),
                str(self.categoria2.id),
            ],
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


class TestEdicaoUsuario(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
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

    def test_editar_usuario(self):
        url = reverse("editar_usuario", args=[self.usuario.id])
        data = {
            "username": "newusername",
            "nome": "New Name",
            "email": "newemail@example.com",
            "telefone": "5555555555",
            "whatsapp": "5555555555",
            "user_type": "2",
            "pref_categorias[]": [
                str(self.categoria1.id),
                str(self.categoria2.id),
            ],
            "razao_social": "New Company",
        }

        self.client.login(username="testuser", password="testpass123")

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 302)
        usuario = Usuario.objects.get(id=self.usuario.id)
        usuario.refresh_from_db()

        self.assertEqual(usuario.nome, "New Name")
        self.assertEqual(usuario.email, "newemail@example.com")
        self.assertEqual(usuario.whats, "5555555555")
        self.assertEqual(usuario.tipo_usuario, 2)
        self.assertEqual(usuario.razao_social, "New Company")


class TestCadastroEvento(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = RequestFactory()
        cls.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
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
        image = SimpleUploadedFile(
            "test.png", image_content, content_type="image/png"
        )
        data = {
            "nome_evento": "Meu Evento",
            "descricao_evento": "Descrição do evento",
            "preco_evento": "50.00",
            "image": image,
            "data_evento": "2023-09-01T00:00",
            "endereco_evento": "Localização do evento",
            "pref_categorias[]": [
                str(self.categoria1.id),
                str(self.categoria2.id),
            ],
        }

        self.client.force_login(self.user)
        request = self.client.post(url, data)
        eventos_criados = Evento.objects.filter(nome="Meu Evento")
        self.assertEqual(eventos_criados.count(), 1)
        self.assertEqual(eventos_criados[0].organizador_id, self.usuario)
        self.assertEqual(
            list(eventos_criados[0].categorias_id.all()),
            [self.categoria1, self.categoria2],
        )

    def test__editar_evento(self):
        evento = Evento.objects.create(
            nome="Evento Antigo",
            descricao="Descrição do evento antigo",
            preco="30.00",
            horario="2023-09-02T00:00",
            localizacao="Localização do evento antigo",
            organizador_id=self.usuario,
        )
        evento.categorias_id.add(self.categoria1)

        url = reverse("editar_evento", args=[evento.id])
        image_content = b"new_image_content"
        new_image = SimpleUploadedFile(
            "new_test.png", image_content, content_type="image/png"
        )
        data = {
            "nome_evento": "Evento Atualizado",
            "descricao_evento": "Nova descrição do evento",
            "preco_evento": "40,00",
            "image": new_image,
            "data_evento": "2023-09-03T00:00",
            "endereco_evento": "Nova localização do evento",
            "pref_categorias[]": [str(self.categoria2.id)],
        }
        self.client.force_login(self.user)
        response = self.client.post(url, data)

        # Verifique se a resposta foi redirecionada com sucesso (status code 302)
        self.assertEqual(response.status_code, 302)

        # Atualize o objeto evento da base de dados
        evento.refresh_from_db()

        # Verifique se os campos foram atualizados corretamente
        self.assertEqual(evento.nome, "Evento Atualizado")
        self.assertEqual(evento.descricao, "Nova descrição do evento")
        self.assertEqual(evento.preco, Decimal("40.00"))
        self.assertEqual(
            evento.horario.strftime("%Y-%m-%dT%H:%M"), "2023-09-03T00:00"
        )
        self.assertEqual(evento.localizacao, "Nova localização do evento")

        # Verifique se as categorias foram atualizadas corretamente
        self.assertEqual(list(evento.categorias_id.all()), [self.categoria2])

    def test_ver_tela_cadastrar_evento_metodo(self):
        url = reverse("cadastrar_evento")
        response_get = self.client.get(url)
        self.assertEqual(response_get.status_code, 200)
