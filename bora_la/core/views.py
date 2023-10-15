from django.shortcuts import render
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import Usuario, Evento, Categoria
from django.contrib import messages
from django.shortcuts import get_object_or_404
import pprint
from decimal import Decimal
from datetime import datetime
import pytz
from django.core.paginator import Paginator
import environ
from urllib.parse import quote
from django.http import JsonResponse
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone


env = environ.Env()
env.read_env()
EVENTOS_POR_PAGINA = 3
MSG_PARA_COMPARTILHAR = "Confira esse evento incrível que está chegando! Clique no link abaixo para conferir mais detalhes:"
MSG_ERRO_COMPARTILHAR = "Ocorreu um erro ao tentar compartilhar o evento"
MSG_SUCESS_AGRADECIMENTO = "Obrigada por compartilhar conosco sua experiência!"
MSG_ERROR_AUTHENTICATION = (
    "Credenciais inválidas. Verifique seu nome de usuário e senha."
)


def get_tipo_usuario(usuario):
    user = Usuario.objects.filter(django_user=usuario)
    return user[0].tipo_usuario if user else None


def get_usuario(usuario):
    user = Usuario.objects.filter(django_user=usuario)
    return user[0] if user else None


def index(request):
    return render(request, "index.html")


def cadastrar_usuario(request):
    categorias_disponiveis = Categoria.objects.all()

    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            nome = request.POST.get("nome")
            email = request.POST.get("email")
            telefone = request.POST.get("telefone")
            whatsapp = request.POST.get("telefone")
            tipo_usuario = request.POST.get("user_type")
            razao_social = request.POST.get("razao_social")
            selected_categories = request.POST.getlist("pref_categorias[]")
            categorias_instancias = []
            for categoria_id in selected_categories:
                categoria = Categoria.objects.get(pk=categoria_id)
                categorias_instancias.append(categoria)
            try:
                print("vou salvar cadastro")

                user = form_usuario.save()
                django_user = user
                cadastro_user = Usuario.objects.create(
                    django_user=django_user,
                    nome=nome,
                    email=email,
                    whats=telefone,
                    tipo_usuario=tipo_usuario,
                    razao_social=razao_social,
                )
                cadastro_user.pref_categorias.set(categorias_instancias)

            except Exception as e:
                print("nao salvou user")
                print(e)

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return redirect("listar_eventos")
        else:
            erros_formulario = form_usuario.errors
            return render(
                request,
                "cadastro.html",
                {
                    "form_usuario": form_usuario,
                    "erros_formulario": erros_formulario,
                    "categorias": categorias_disponiveis,
                },
            )
    else:
        form_usuario = UserCreationForm()
        return render(
            request,
            "cadastro.html",
            {"form_usuario": form_usuario, "categorias": categorias_disponiveis},
        )


def editar_usuario(request, id):
    categorias_default = Categoria.objects.all()
    usuario = get_usuario(request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        nome = request.POST.get("nome")
        email = request.POST.get("email")
        telefone = request.POST.get("telefone")
        whatsapp = request.POST.get("telefone")
        tipo_usuario = request.POST.get("user_type")
        razao_social = request.POST.get("razao_social")
        selected_categories = request.POST.getlist("pref_categorias[]")
        selected_categories = request.POST.getlist("pref_categorias[]")
        categorias_instancias = []
        for categoria_id in selected_categories:
            categoria = Categoria.objects.get(pk=categoria_id)
            categorias_instancias.append(categoria)
        try:
            print("vou editar cadastro")
            usuario = get_object_or_404(Usuario, pk=id)
            django_user = request.user

            pprint.pprint(usuario.__dict__)
            pprint.pprint(django_user.username)

            django_user.username = username if username else django_user.username
            usuario.nome = nome if nome else usuario.nome
            usuario.tipo_usuario = (
                tipo_usuario if tipo_usuario else usuario.tipo_usuario
            )
            usuario.email = email if email else usuario.email
            usuario.whats = telefone if telefone else usuario.whats
            usuario.razao_social = (
                razao_social if razao_social else usuario.razao_social
            )

            usuario.save()
            usuario.pref_categorias.set(categorias_instancias)

            django_user.save()
            print("editei user")
            pprint.pprint(usuario.__dict__)
            pprint.pprint(django_user.username)
            pprint.pprint(usuario.pref_categorias.values_list("id", flat=True))
            return redirect(
                "listar_eventos"
            )  # Redirecione para meus eventos após editar cadastro
        except Exception as e:
            print("nao editou user")
            print(e)

    context = {
        "tipo_usuario": usuario.tipo_usuario,
        "usuario": usuario,
        "categorias": categorias_default,
        "categorias_usuario": usuario.pref_categorias.values_list("id", flat=True),
    }
    pprint.pprint(usuario.pref_categorias.values_list("id", flat=True))

    return render(request, "editar_usuario.html", context)


def editar_senha(request, id):
    categorias_default = Categoria.objects.all()
    usuario = get_usuario(request.user)

    context = {
        "tipo_usuario": usuario.tipo_usuario,
        "usuario": usuario,
        "categorias": categorias_default,
        "categorias_usuario": usuario.pref_categorias.values_list("id", flat=True),
    }

    if request.method == "POST":
        nova_senha = request.POST.get("nova_senha")
        confirmar_senha = request.POST.get("confirmar_senha")

        # Validação da senha
        try:
            validate_password(nova_senha, usuario.django_user)
            if nova_senha and nova_senha == confirmar_senha:
                usuario.django_user.set_password(nova_senha)
                usuario.django_user.save()
                login(request, usuario.django_user)

                return JsonResponse(
                    {"success": True, "message": "Senha atualizada com sucesso!"}
                )
            else:
                return JsonResponse(
                    {
                        "success": False,
                        "error_message": "As senhas não coincidem. Por favor, tente novamente.",
                    }
                )
        except Exception as e:
            error_message = ", ".join(e)
            return JsonResponse({"success": False, "error_message": error_message})

    return redirect("editar_usuario", context)


def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect("listar_eventos")
        else:
            form_login = AuthenticationForm(request, data=request.POST)
            messages.error(request, MSG_ERROR_AUTHENTICATION)
    else:
        form_login = AuthenticationForm()

    return render(request, "login.html", {"form_login": form_login})


@login_required(login_url="/logar_usuario")
def deslogar_usuario(request):
    logout(request)
    return redirect("index")


@login_required
def meus_eventos(request):
    usuario = Usuario.objects.filter(django_user=request.user).first()
    tipo_usuario = usuario.tipo_usuario

    eventos = Evento.objects.filter(organizador_id=usuario)

    if eventos.exists():
        context = {
            "eventos": eventos,
            "tipo_usuario": tipo_usuario,
        }
        return render(request, "meus_eventos.html", context)
    else:
        error_message = "Você ainda não cadastrou nenhum evento."
        context = {
            "error_message": error_message,
            "tipo_usuario": tipo_usuario,
        }
        return render(request, "meus_eventos.html", context)


def cadastrar_evento(request):
    tipo_usuario = None

    if request.method == "POST":
        nome_evento = request.POST.get("nome_evento")
        descricao = request.POST.get("descricao_evento")
        horario_str = request.POST.get("data_evento")
        horario = datetime.strptime(horario_str, "%Y-%m-%dT%H:%M").replace(
            tzinfo=pytz.UTC
        )
        localizacao = request.POST.get("endereco_evento")
        preco_ingressos = request.POST.get("preco_evento")
        if preco_ingressos:
            preco_ingressos = preco_ingressos.replace(".", "")
            preco_ingressos = preco_ingressos.replace(",", ".")
            print(preco_ingressos)
            preco_ingressos = Decimal(preco_ingressos)
        foto = request.FILES.get("image")
        categorias = request.POST.getlist("pref_categorias[]")
        categorias_instancias = []
        for categoria_id in categorias:
            categoria = Categoria.objects.get(pk=categoria_id)
            categorias_instancias.append(categoria)
        organizador = Usuario.objects.get(django_user=request.user)
        try:
            criar_evento = Evento.objects.create(
                nome=nome_evento,
                descricao=descricao,
                organizador_id=organizador,
                horario=horario,
                localizacao=localizacao,
                preco=preco_ingressos if preco_ingressos else 0,
                foto=foto,
            )
            criar_evento.categorias_id.set(categorias_instancias)

            print("Evento cadastrado com sucesso")
            pprint.pprint(criar_evento.__dict__)
            return redirect("meus_eventos")
        except Exception as e:
            print("ERROR")
            print(e)

    else:
        if request.user.is_authenticated:
            tipo_usuario = get_tipo_usuario(request.user)

    categorias_default = Categoria.objects.all()

    context = {
        "tipo_usuario": tipo_usuario if tipo_usuario else 0,
        "categorias": categorias_default,
    }

    return render(request, "cadastro_evento.html", context)


def editar_evento(request, id):
    tipo_usuario = None
    categorias_default = Categoria.objects.all()

    evento = get_object_or_404(Evento, pk=id)
    if request.method == "POST":
        nome_evento = request.POST.get("nome_evento")
        descricao = request.POST.get("descricao_evento")
        user = request.user
        horario_str = request.POST.get("data_evento")
        # horario = datetime.strptime(horario_str, "%Y-%m-%dT%H:%M").replace(
        #     tzinfo=pytz.UTC
        # )
        horario = timezone.make_aware(datetime.strptime(horario_str, "%Y-%m-%dT%H:%M"))

        localizacao = request.POST.get("endereco_evento")
        preco_ingressos = request.POST.get("preco_evento")
        foto = request.FILES.get("image")
        preco_ingressos = request.POST.get("preco_evento")
        if preco_ingressos:
            preco_ingressos = preco_ingressos.replace(".", "")
            preco_ingressos = preco_ingressos.replace(",", ".")
            preco_ingressos = Decimal(preco_ingressos)
        categorias = request.POST.getlist("pref_categorias[]")
        categorias_instancias = []
        for categoria_id in categorias:
            categoria = Categoria.objects.get(pk=categoria_id)
            categorias_instancias.append(categoria)
        organizador = Usuario.objects.get(django_user=user)
        try:
            evento.nome = nome_evento
            evento.descricao = descricao
            evento.horario = horario
            evento.localizacao = localizacao
            evento.preco = preco_ingressos if preco_ingressos else 0
            if foto:
                evento.foto = foto
            evento.organizador_id = organizador
            evento.save()
            evento.categorias_id.set(categorias_instancias)

            print("Evento alterado com sucesso")
            pprint.pprint(evento.__dict__)
            return redirect(
                "meus_eventos"
            )  # Redirecione para a lista de eventos após o cadastro
        except Exception as e:
            print("ERROR")
            print(e)
    else:
        if request.user.is_authenticated:
            tipo_usuario = get_tipo_usuario(request.user)

    context = {
        "tipo_usuario": tipo_usuario if tipo_usuario else 0,
        "evento": evento,
        "categorias_evento": evento.categorias_id.values_list("id", flat=True),
        "categorias": categorias_default,
    }
    pprint.pprint(evento.__dict__)
    pprint.pprint(evento.categorias_id.all())
    pprint.pprint(evento.categorias_id.values_list("id", flat=True))

    return render(request, "editar_evento.html", context)


def visualizar_evento(request, id):
    api_key = env("API_KEY")
    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = get_tipo_usuario(request.user)
    evento = get_object_or_404(Evento, pk=id)
    # Codifica a localizacao para usar na URL do Google Maps
    localizacao = quote(evento.localizacao)
    context = {
        "evento": evento,
        "tipo_usuario": tipo_usuario if tipo_usuario else 0,
        "API_KEY": api_key,
        "localizacao": localizacao,  # Adiciona a localizacao codificada ao contexto
    }
    print(api_key)
    print(evento.localizacao)
    return render(request, "visualizar_evento.html", context)


def listar_eventos(request):
    tipo_usuario = None
    if request.user.is_authenticated:
        tipo_usuario = get_tipo_usuario(request.user)

    eventos = Evento.objects.all()
    eventos_por_pagina = EVENTOS_POR_PAGINA
    paginator = Paginator(eventos, eventos_por_pagina)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "eventos": eventos,
        "tipo_usuario": tipo_usuario if tipo_usuario else 0,
    }

    return render(request, "listar_eventos.html", context)


def filtrar_eventos(request):
    nome = request.GET.get("nome_parcial")

    eventos = Evento.objects.all()

    if nome:
        eventos = eventos.filter(nome__icontains=nome)

    eventos_por_pagina = EVENTOS_POR_PAGINA
    paginator = Paginator(eventos, eventos_por_pagina)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    context = {
        "page": page,
        "eventos": eventos,
    }

    return render(request, "listar_eventos.html", context)
