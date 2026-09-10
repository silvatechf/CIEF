"""
Vistas principales del sitio.

Incluye la página de inicio y vistas generales.
"""

from django.shortcuts import render
from apps.productos.models import Producto, Categoria


def inicio(request):
    """
    Vista de inicio del sitio.

    Muestra:
    - Productos destacados
    - Categorías principales
    - Información general

    Args:
        request: Objeto HttpRequest

    Returns:
        HttpResponse con la página de inicio
    """
    productos_destacados = Producto.objects.filter(
        activo=True, destacado=True
    ).order_by("-created_at")[:8]

    categorias = Categoria.objects.filter(activa=True).order_by("nombre")

    contexto = {
        "productos_destacados": productos_destacados,
        "categorias": categorias,
        "titulo": "Inicio - Ecommerce",
    }

    return render(request, "inicio.html", contexto)


def acerca_de(request):
    """
    Vista de la página 'Acerca de'.

    Args:
        request: Objeto HttpRequest

    Returns:
        HttpResponse con información de la empresa
    """
    contexto = {
        "titulo": "Acerca de Nosotros",
    }

    return render(request, "acerca_de.html", contexto)


def contacto(request):
    """
    Vista de contacto.

    Args:
        request: Objeto HttpRequest

    Returns:
        HttpResponse con el formulario de contacto
    """
    if request.method == "POST":
        # Aquí iría el procesamiento del formulario
        # Por ejemplo, enviar email, guardar en BD, etc.
        pass

    contexto = {
        "titulo": "Contacto",
    }

    return render(request, "contacto.html", contexto)


def terminos_servicio(request):
    """Vista de términos de servicio."""
    contexto = {
        "titulo": "Términos de Servicio",
    }

    return render(request, "terminos_servicio.html", contexto)


def politica_privacidad(request):
    """Vista de política de privacidad."""
    contexto = {
        "titulo": "Política de Privacidad",
    }

    return render(request, "politica_privacidad.html", contexto)
