from django.shortcuts import render
from django.http import HttpResponse
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from core.models import Usuario, Evento, Categoria
from django.contrib import messages
from django.shortcuts import get_object_or_404


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
            nome = request.POST.get("nome")
            email = request.POST.get("email")
            telefone = request.POST.get("telefone")
            whatsapp = request.POST.get("telefone")
            tipo_usuario = request.POST.get("user_type")
            razao_social = request.POST.get("razao_social")
            selected_categories = request.POST.getlist("pref_categorias[]")

            try:
                print("vou salvar cadastro")

                user = form_usuario.save()
                django_user = user
                cadastro_user = Usuario.objects.create(
                    django_user=user,
                    nome=nome,
                    email=email,
                    whats=telefone,
                    tipo_usuario=tipo_usuario,
                    razao_social=razao_social,
                    pref_categorias=selected_categories,
                )
            except Exception as e:
                print("nao salvou user")
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
        categorias_disponiveis = Categoria.objects.all()

        form_usuario = UserCreationForm()
        return render(
            request,
            "cadastro_usuario.html",
            {"form_usuario": form_usuario, "categorias": categorias_disponiveis},
        )


def logar_usuario(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect("listar_eventos")
        else:
            form_login = AuthenticationForm(
                request, data=request.POST
            )  # Passar o data=request.POST aqui
            messages.error(request, MSG_ERROR_AUTHENTICATION)
    else:
        form_login = AuthenticationForm()

    return render(request, "login.html", {"form_login": form_login})


@login_required(login_url="/logar_usuario")
def deslogar_usuario(request):
    logout(request)
    return redirect("index")


def listar_eventos(request):
    tipo_usuario = None
    if request.user.is_authenticated:
        print("autenticado", request.user)
        usuario = Usuario.objects.filter(django_user=request.user).first()
        if usuario:
            tipo_usuario = usuario.tipo_usuario

    return render(request, "listar_eventos.html", {"tipo_usuario": tipo_usuario})


@login_required
def meus_eventos(request):
    usuario = Usuario.objects.filter(django_user=request.user).first()
    tipo_usuario = usuario.tipo_usuario

    eventos = Evento.objects.filter(organizador_id=usuario)

    if eventos.exists():
        context = {
            "eventos": eventos,
            "tipo_usuario": tipo_usuario,
        }  # Passar 'tipo_usuario' no contexto
        return render(request, "meus_eventos.html", context)
    else:
        error_message = "Você ainda não cadastrou nenhum evento."
        context = {
            "error_message": error_message,
            "tipo_usuario": tipo_usuario,
        }  # Passar 'tipo_usuario' no contexto
        return render(request, "meus_eventos.html", context)


def cadastrar_evento(request):
    categorias_default = Categoria.objects.all()
    tipo_usuario = None
    if request.method == "POST":        
        nome_evento = request.POST.get("nome_evento")
        descricao = request.POST.get("descricao_evento")
        user = request.user
        horario = request.POST.get("data_evento")
        localizacao = request.POST.get("endereco_evento")
        preco_ingressos = request.POST.get("preco_evento")
        foto = request.FILES.get("image")
        categorias = request.POST.getlist("pref_categorias[]")

        organizador = Usuario.objects.get(django_user=user)
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

            criar_evento.categorias_id.set(categorias)
            print("Evento cadastrado com sucesso")
            return redirect(
                "listar_eventos"
            )  # Redirecione para a lista de eventos após o cadastro
        except Exception as e:
            print("ERROR")
            print(e)

    else:
        tipo_usuario = None
        if request.user.is_authenticated:
            print("autenticado", request.user)
            usuario = Usuario.objects.filter(django_user=request.user).first()
            if usuario:
                tipo_usuario = usuario.tipo_usuario

    return render(
        request,
        "cadastro_evento.html",
        {"tipo_usuario": tipo_usuario, "categorias": categorias_default},
    )


def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.method == "POST":
        #form_evento = EventoCreationForm(request.POST, request.FILES, instance=evento)
        nome_evento = request.POST.get("nome_evento")
        descricao = request.POST.get("descricao_evento")
        horario = request.POST.get("data_evento")
        localizacao = request.POST.get("endereco_evento")
        preco_ingressos = request.POST.get("preco_evento")
        foto = request.FILES.get("image")
        categorias = request.POST.getlist("pref_categorias[]")
        try:
            editar_evento = Evento.objects.update(
                nome=nome_evento,
                descricao=descricao,
                horario=horario,
                localizacao=localizacao,
                preco=preco_ingressos if preco_ingressos else 0,
                foto=foto,                
            )
            editar_evento.categorias_id.set(categorias)

            return redirect("listar_eventos")  # Redirecione para a lista de eventos após a edição
        except Exception as e:
            print("ERROR")
            print(e)

    return render(request, "cadastro_evento.html", {"tipo_usuario": tipo_usuario,"categorias": categorias_default})
