from django.utils.deprecation import MiddlewareMixin
from .utils import registrar_evento, obtener_ip_cliente, obtener_user_agent


class RastreadorEventosMiddleware(MiddlewareMixin):
    """
    Middleware para rastrear eventos de usuario automáticamente.
    Registra accesos a páginas sin interferir con el registro de formularios.
    """

    # Rutas que no se deben rastrear
    RUTAS_IGNORADAS = [
        "/static/",
        "/media/",
        "/admin/",
        "/usuarios/login/",
        "/usuarios/registro/",
        "/usuarios/logout/",
        "/favicon.ico",
        "/api/schema/",
        "/swagger/",
    ]

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Se ejecuta cuando una vista va a ser procesada."""

        # Ignorar rutas específicas
        if any(request.path.startswith(ruta) for ruta in self.RUTAS_IGNORADAS):
            return None

        # Ignorar métodos HTTP que no sean GET para no interferir en la creación de usuarios o formularios
        if request.method != "GET":
            return None

        # Obtener información del cliente
        ip_address = obtener_ip_cliente(request)
        user_agent = obtener_user_agent(request)
        url = request.build_absolute_uri()

        # Detectar eventos específicos basados en la ruta y el usuario
        usuario = request.user if request.user.is_authenticated else None

        # Rastrear cambios de página (todos los accesos GET excepto los ignorados)
        try:
            registrar_evento(
                usuario=usuario,
                tipo="BUSCAR" if "search" in request.path or "q=" in request.GET else "OTRO",
                descripcion=f"Acceso a {request.path}",
                url=url,
                ip_address=ip_address,
                user_agent=user_agent,
                datos_adicionales={
                    "metodo": request.method,
                    "ruta": request.path,
                    "parametros": dict(request.GET) if request.GET else {},
                },
            )
        except Exception as e:
            # No interrumpir el flujo si hay error en el registro de eventos
            print(f"Error al registrar evento en middleware: {e}")

        return None

    def process_response(self, request, response):
        """Se ejecuta después de que la vista ha sido procesada."""
        return response