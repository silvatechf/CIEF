from .models import Evento


def registrar_evento(
    usuario=None,
    tipo="OTRO",
    descripcion="",
    url=None,
    ip_address=None,
    user_agent=None,
    datos_adicionales=None
):
    """
    Función auxiliar para registrar eventos en el sistema.
    
    Args:
        usuario: Usuario que realiza la acción (puede ser None para usuarios anónimos)
        tipo: Tipo de evento (debe estar en TipoEvento.TIPOS_EVENTO)
        descripcion: Descripción detallada del evento
        url: URL de la página donde ocurrió el evento
        ip_address: Dirección IP del cliente
        user_agent: User Agent del navegador
        datos_adicionales: Diccionario con datos adicionales del evento
    """
    if datos_adicionales is None:
        datos_adicionales = {}
    
    evento = Evento(
        usuario=usuario,
        tipo=tipo,
        descripcion=descripcion,
        url=url,
        ip_address=ip_address,
        user_agent=user_agent,
        datos_adicionales=datos_adicionales
    )
    evento.save()
    return evento


def obtener_ip_cliente(request):
    """Obtiene la dirección IP del cliente desde la request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def obtener_user_agent(request):
    """Obtiene el User Agent del cliente desde la request."""
    return request.META.get('HTTP_USER_AGENT', '')
