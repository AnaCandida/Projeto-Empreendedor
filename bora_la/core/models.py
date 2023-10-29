from django.contrib.auth.models import User
from django.db import models
from django import forms
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse


class Categoria(models.Model):
    """
    Modelo para representar uma categoria.
    """

    nome = models.CharField(
        max_length=255, blank=False, null=False, help_text="Nome da categoria"
    )

    def __str__(self):
        return self.nome


class Usuario(models.Model):
    """
    Classe que representa um usuário personalizado com campos adicionais.
    A senha é tratada pelo sistema de autenticação.
    Documentação: https://docs.djangoproject.com/en/dev/topics/auth/#storing-additional-information-about-users
    """

    TIPOS_USUARIO = (
        (1, "Usuário Geral"),
        (2, "Usuário Organizador"),
    )

    django_user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="Referência ao modelo de usuário do Django.",
    )
    nome = models.CharField(
        max_length=255, blank=False, null=False, help_text="Nome do usuário."
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        blank=False,
        null=False,
        help_text="Endereço de e-mail do usuário (único).",
    )
    whats = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Número de telefone do usuário (opcional).",
    )
    notificacoes = models.BooleanField(
        default=True, help_text="Preferência de notificações para o usuário."
    )
    pref_categorias = models.ManyToManyField(
        Categoria, help_text="Preferências de categorias em lista"
    )

    tipo_usuario = models.IntegerField(
        choices=TIPOS_USUARIO,
        default=1,
        help_text="Tipo de usuário conforme definido em TIPOS_USUARIO.",
    )
    razao_social = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Razão social do usuário organizador (opcional).",
    )

    def __str__(self):
        return self.nome


class Evento(models.Model):
    """
    Modelo para representar uma evento.
    """

    nome = models.CharField(
        max_length=255, blank=False, null=False, help_text="Nome do evento."
    )
    descricao = models.TextField(null=False)
    foto = models.ImageField(
        upload_to="event_photos/",  # Define o caminho onde as imagens serão armazenadas
        blank=True,
        null=True,
        help_text="Foto representativa do evento (JPEG, até 5MB, 1200x1200px)",
    )
    organizador_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    preco = models.DecimalField(
        max_digits=10, decimal_places=2, null=False
    )  # Alterado para DecimalField
    horario = models.DateTimeField(null=False)
    localizacao = models.TextField(null=False)
    categorias_id = models.ManyToManyField(Categoria)

    def get_absolute_url(self):
        return reverse('visualizar_evento', args=[str(self.id)])


class Notificacao(models.Model):
    """
    Modelo para representar uma notificação de evento.
    """

    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    mensagem = models.TextField()
    alteracao_data = models.BooleanField()
    alteracao_hora = models.BooleanField()
    alteracao_desc = models.BooleanField()


class Avaliacao(models.Model):
    """
    Modelo para representar uma avaliação de evento.
    """

    usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False)
    evento_id = models.ForeignKey(Evento, on_delete=models.CASCADE, null=False)
    nota = models.IntegerField(null=False)
    comentario = models.TextField(blank=True, null=True)
