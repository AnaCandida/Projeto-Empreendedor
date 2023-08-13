# Generated by Django 4.2 on 2023-08-13 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0001_initial"),
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
                    models.CharField(help_text="Nome do usuário.", max_length=255),
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
                ("categorias_id", models.JSONField()),
                (
                    "organizador_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.usuario"
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