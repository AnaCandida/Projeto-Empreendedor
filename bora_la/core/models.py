from django.contrib.auth.models import User
from django.db import models
from django import forms


class Categoria(models.Model):
    """
    Modelo para representar uma categoria.
    """

    nome = models.CharField(
        max_length=255, blank=False, null=False, help_text="Nome do usuário."
    )


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
    pref_categorias = models.JSONField(
        default=dict,
        blank=True,
        help_text="Preferências de categorias em formato JSON.",
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
    Modelo para representar uma categoria.
    """

    nome = models.CharField(
        max_length=255, blank=False, null=False, help_text="Nome do evento."
    )
    descricao = models.TextField(null=False)
    foto = models.CharField(max_length=255)  # Deve ser alterado para o tipo adequado
    organizador_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    preco = models.DecimalField(
        max_digits=10, decimal_places=2, null=False
    )  # Alterado para DecimalField
    horario = models.DateTimeField(null=False)
    localizacao = models.TextField(null=False)
    categorias_id = models.JSONField(null=False)


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