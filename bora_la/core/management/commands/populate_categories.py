from django.bora_la.core.management.base import BaseCommand
from bora_la.core.models import Categoria


class Command(BaseCommand):
    help = 'Popula as categorias no banco de dados'

    def handle(self, *args, **kwargs):
        categorias = [
            "Comida",
            "Ar Livre",
            "Negocio Local",
            "Cultura",
            "Esporte",
            "Musica",
        ]

        for categoria_nome in categorias:
            categoria, created = Categoria.objects.get_or_create(
                nome=categoria_nome
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Criada categoria: {categoria.nome}")
                )
            else:
                self.stdout.write(f"Categoria já existe: {categoria.nome}")
