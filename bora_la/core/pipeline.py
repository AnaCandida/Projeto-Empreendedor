from social_core.pipeline.user import get_username
from core import models


def create_user(strategy, details, user=None, *args, **kwargs):
    kwargs["is_new"] = False
    if models.Usuario.objects.filter(django_user=user).exists():
        print("not new")

    try:
        print("vou salvar cadastro")

        django_user = user
        cadastro_user = models.Usuario.objects.create(
            django_user=django_user,
            nome=details["fullname"],
            email=details["email"],
            whats="",
            tipo_usuario="1",
            razao_social="",
        )

    except Exception as e:
        print("nao salvou user")
        print(e)

    print("new")
