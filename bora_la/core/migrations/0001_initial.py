# Generated by Django 4.2 on 2023-08-27 20:44

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Categoria",
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
                    models.CharField(help_text="Nome da categoria", max_length=255),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Evento",
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
                ("nome", models.CharField(help_text="Nome do evento.", max_length=255)),
                ("descricao", models.TextField()),
                ("foto", models.CharField(max_length=255)),
                ("preco", models.DecimalField(decimal_places=2, max_digits=10)),
                ("horario", models.DateTimeField()),
                ("localizacao", models.TextField()),
                (
                    "categorias_id",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50),
                        blank=True,
                        help_text="Preferências de categorias em lista",
                        null=True,
                        size=4,
                    ),
                ),
            ],
        ),
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
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=50),
                        blank=True,
                        help_text="Preferências de categorias em lista",
                        null=True,
                        size=4,
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
        migrations.CreateModel(
            name="Notificacao",
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
                ("mensagem", models.TextField()),
                ("alteracao_data", models.BooleanField()),
                ("alteracao_hora", models.BooleanField()),
                ("alteracao_desc", models.BooleanField()),
                (
                    "evento",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.evento"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="evento",
            name="organizador_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.usuario"
            ),
        ),
        migrations.CreateModel(
            name="Avaliacao",
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
                ("nota", models.IntegerField()),
                ("comentario", models.TextField(blank=True, null=True)),
                (
                    "evento_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.evento"
                    ),
                ),
                (
                    "usuario_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.usuario"
                    ),
                ),
            ],
        ),
    ]
