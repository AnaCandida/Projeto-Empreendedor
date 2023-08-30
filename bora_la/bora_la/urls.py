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
    path("cadastrar_evento", cadastrar_evento, name="cadastrar_evento"),
    path("listar_eventos", listar_eventos, name="listar_eventos"),
    path("meus_eventos", meus_eventos, name="meus_eventos"),
    path('editar_evento/<int:id>', evento_view, name="editar_evento"),

    path("", index, name="index"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
