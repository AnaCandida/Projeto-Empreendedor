from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import Usuario
from django.contrib import messages


MSG_PARA_COMPARTILHAR = "Confira esse evento incrível que está chegando! Clique no link abaixo para conferir mais detalhes:"
MSG_ERRO_COMPARTILHAR = "Ocorreu um erro ao tentar compartilhar o evento"
MSG_SUCESS_AGRADECIMENTO = "Obrigada por compartilhar conosco sua experiência!"
MSG_ERROR_AUTHENTICATION = (
    "Credenciais inválidas. Verifique seu nome de usuário e senha."
)


def index(request):
    return render(request, "index.html")


def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            user = form_usuario.save()
            django_user = user
            nome = request.POST.get("nome")
            email = request.POST.get("email")
            telefone = request.POST.get("telefone")
            whatsapp = request.POST.get("telefone")
            tipo_usuario = request.POST.get("user_type")
            razao_social = request.POST.get("razao_social")

            selected_categories = request.POST.getlist("pref_categorias[]")
            pref_categorias = {}
            for category in selected_categories:
                pref_categorias[category] = True

            try:
                print("vou salvar cadastro")
                cadastro_user = Usuario.objects.create(
                    django_user=user,
                    nome=nome,
                    email=email,
                    whats=telefone,
                    tipo_usuario=tipo_usuario,
                    razao_social=razao_social,
                    pref_categorias=pref_categorias,
                )
            except Exception as e:
                print(e)

            login(request, user)

            return redirect("listar_eventos")
        else:
            erros_formulario = form_usuario.errors
            return render(
                request,
                "cadastro.html",
                {"form_usuario": form_usuario, "erros_formulario": erros_formulario},
            )
    else:
        form_usuario = UserCreationForm()
        return render(request, "cadastro.html", {"form_usuario": form_usuario})


def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect("listar_eventos")
        else:
            form_login = AuthenticationForm()
            messages.error(request, MSG_ERROR_AUTHENTICATION)
    else:
        form_login = AuthenticationForm()

    return render(request, "login.html", {"form_login": form_login})


@login_required(login_url="/logar_usuario")
def deslogar_usuario(request):
    logout(request)
    return redirect("index")


def criar_evento(request):
    return render(request, "criar_evento.html")


def listar_eventos(request):
    tipo_usuario = None
    if request.user.is_authenticated:
        print("autenticado")
        usuario = Usuario.objects.filter(django_user=request.user).first()
        if usuario:
            tipo_usuario = usuario.tipo_usuario

    return render(request, "listar_eventos.html", {"tipo_usuario": tipo_usuario})


def cadastrar_evento(request):
    if request.method == "POST":
        form_evento = EventoCreationForm(request.POST)
        if form_evento.is_valid():
            #evento = form_evento.save()

            django_user = user
                        
            nome_evento = request.POST.get("nome_evento")
            descricao = request.POST.get("descricao")
            horario =  request.POST.get("horario")
            localizacao = request.POST.get("localizacao")
            preco_ingressos = request.POST.get("preco_ingressos")
            imagem = request.POST.get("imagem")
            categoria = request.POST.get("categoria")
            organizador = request.user

            try:
                print("Evento cadastrado com sucesso")
                criar_evento = Evento.objects.create(
                    django_user=user,
                    nome=nome_evento,
                    descricao=descricao,
                    foto=imagem,
                    organizador_id=organizador,
                    preco=preco_ingressos,
                    horario=pref_categorias,
                    localizacao = localizacao,
                    categorias_id = categoria,
                )
            except Exception as e:
                print(e)       

            form_evento.save()

            return redirect("listar_eventos")  # Redirecione para a lista de eventos após o cadastro

        else:
            erros_formulario = form_evento.errors
            return render(
                request,
                "criar_evento.html",
                {"form_evento": form_evento, "erros_formulario": erros_formulario},
            )    
    else:
        form_evento = EventoCreationForm()

    return render(request, "criar_evento.html", {"form_evento": form_evento})

