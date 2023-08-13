from django.contrib import admin
from .models import Usuario, Categoria, Evento, Notificacao, Avaliacao

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "email", "whats", "tipo_usuario", "razao_social")
    list_filter = ("tipo_usuario",)
    search_fields = ("nome", "email", "razao_social")

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ("nome", "organizador_id", "horario")
    list_filter = ("organizador_id",)
    search_fields = ("nome",)

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ("evento", "mensagem", "alteracao_data", "alteracao_hora", "alteracao_desc")

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ("usuario_id", "evento_id", "nota")
    list_filter = ("usuario_id", "evento_id")
