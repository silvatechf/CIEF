"""
Context processors para la aplicación Carrito.
Permite acceder a los datos del carrito desde cualquier plantilla HTML.
"""

from .models import Carrito


def carrito(request):
    """
    Agrega el objeto carrito al contexto global de las plantillas.
    """
    if request.user.is_authenticated:
        carrito_obj, _ = Carrito.objects.get_or_create(usuario=request.user)
    else:
        carrito_obj = None

    return {
        "carrito_global": carrito_obj,
    }