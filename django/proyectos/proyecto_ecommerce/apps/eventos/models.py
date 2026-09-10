from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class TipoEvento(models.Model):
    """Modelo para definir tipos de eventos."""
    
    TIPOS_EVENTO = [
        ("LOGIN", "Login de usuário"),
        ("LOGOUT", "Logout de usuário"),
        ("REGISTRO", "Novo registro de usuário"),
        ("VER_PRODUCTO", "Visualización de producto"),
        ("AGREGAR_CARRITO", "Agregar producto al carrito"),
        ("ELIMINAR_CARRITO", "Eliminar producto del carrito"),
        ("CREAR_PEDIDO", "Crear pedido"),
        ("COMPLETAR_PEDIDO", "Completar pedido"),
        ("CANCELAR_PEDIDO", "Cancelar pedido"),
        ("ACTUALIZAR_PERFIL", "Actualizar perfil de usuario"),
        ("CAMBIAR_CONTRASEÑA", "Cambiar contraseña"),
        ("RESEÑA_PRODUCTO", "Crear reseña de producto"),
        ("BUSCAR", "Búsqueda en la tienda"),
        ("FILTRAR", "Aplicar filtros de búsqueda"),
        ("OTRO", "Otro evento"),
    ]
    
    nombre = models.CharField(max_length=50, unique=True, choices=TIPOS_EVENTO)
    descripcion = models.CharField(max_length=255, blank=True)
    
    class Meta:
        verbose_name = "Tipo de evento"
        verbose_name_plural = "Tipos de eventos"
    
    def __str__(self):
        return self.get_nombre_display()


class Evento(models.Model):
    """Modelo para registrar eventos de usuarios."""
    
    usuario = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="eventos"
    )
    tipo = models.CharField(
        max_length=50,
        choices=TipoEvento.TIPOS_EVENTO,
        default="OTRO"
    )
    descripcion = models.TextField(blank=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    datos_adicionales = models.JSONField(default=dict, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["-fecha_creacion"]
        indexes = [
            models.Index(fields=["-fecha_creacion"]),
            models.Index(fields=["usuario", "-fecha_creacion"]),
            models.Index(fields=["tipo", "-fecha_creacion"]),
        ]
    
    def __str__(self):
        usuario_str = self.usuario.username if self.usuario else "Anónimo"
        return f"{usuario_str} - {self.get_tipo_display()} - {self.fecha_creacion.strftime('%d/%m/%Y %H:%M')}"
