from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("logar_usuario", logar_usuario, name="logar_usuario"),
    path("deslogar_usuario", deslogar_usuario, name="deslogar_usuario"),
    path("cadastrar_usuario", cadastrar_usuario, name="cadastrar_usuario"),
    path("editar_usuario/<int:id>", editar_usuario, name="editar_usuario"),
    path("cadastrar_evento", cadastrar_evento, name="cadastrar_evento"),
    path("listar_eventos", listar_eventos, name="listar_eventos"),
    path("visualizar_evento/<int:id>", visualizar_evento, name="visualizar_evento"),
    path("editar_evento/<int:id>", editar_evento, name="editar_evento"),
    path("meus_eventos", meus_eventos, name="meus_eventos"),
    path("filtrar_eventos", filtrar_eventos, name="filtrar_eventos"),
    path("", index, name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
