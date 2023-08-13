# Generated by Django 4.2 on 2023-08-13 01:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(help_text="Nome do usuário.", max_length=255),
                ),
                (
                    "email",
                    models.EmailField(
                        help_text="Endereço de e-mail do usuário (único).",
                        max_length=254,
                        unique=True,
                    ),
                ),
                (
                    "whats",
                    models.CharField(
                        blank=True,
                        help_text="Número de telefone do usuário (opcional).",
                        max_length=20,
                        null=True,
                    ),
                ),
                (
                    "notificacoes",
                    models.BooleanField(
                        default=True,
                        help_text="Preferência de notificações para o usuário.",
                    ),
                ),
                (
                    "pref_categorias",
                    models.JSONField(
                        blank=True,
                        default=dict,
                        help_text="Preferências de categorias em formato JSON.",
                    ),
                ),
                (
                    "tipo_usuario",
                    models.IntegerField(
                        choices=[(1, "Usuário Geral"), (2, "Usuário Organizador")],
                        default=1,
                        help_text="Tipo de usuário conforme definido em TIPOS_USUARIO.",
                    ),
                ),
                (
                    "razao_social",
                    models.CharField(
                        blank=True,
                        help_text="Razão social do usuário organizador (opcional).",
                        max_length=255,
                        null=True,
                    ),
                ),
                (
                    "django_user",
                    models.OneToOneField(
                        help_text="Referência ao modelo de usuário do Django.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
