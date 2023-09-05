import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bora_la.settings")
django.setup()

from core.models import Categoria


def populate_categories():
    categorias = ["Comida", "Ar Livre", "Negocio Local", "Cultura", "Esporte", "Musica"]

    for categoria_nome in categorias:
        categoria, created = Categoria.objects.get_or_create(nome=categoria_nome)
        if created:
            print(f"Criada categoria: {categoria.nome}")
        else:
            print(f"Categoria já existe: {categoria.nome}")


if __name__ == "__main__":
    populate_categories()
