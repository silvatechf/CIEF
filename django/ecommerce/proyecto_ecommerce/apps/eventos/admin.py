from django.contrib import admin
from .models import Evento, TipoEvento


@admin.register(TipoEvento)
class TipoEventoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "descripcion"]
    search_fields = ["nombre", "descripcion"]
    readonly_fields = ["nombre"]


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ["usuario", "tipo", "fecha_creacion", "ip_address"]
    list_filter = ["tipo", "fecha_creacion", "usuario"]
    search_fields = ["usuario__username", "descripcion", "ip_address"]
    readonly_fields = ["usuario", "tipo", "descripcion", "url", "ip_address", "user_agent", "datos_adicionales", "fecha_creacion"]
    
    fieldsets = (
        ("Información del evento", {
            "fields": ("usuario", "tipo", "descripcion")
        }),
        ("Detalles técnicos", {
            "fields": ("url", "ip_address", "user_agent"),
            "classes": ("collapse",)
        }),
        ("Datos adicionales", {
            "fields": ("datos_adicionales",),
            "classes": ("collapse",)
        }),
        ("Fecha de creación", {
            "fields": ("fecha_creacion",)
        }),
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
