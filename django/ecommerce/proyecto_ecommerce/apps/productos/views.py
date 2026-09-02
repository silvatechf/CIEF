"""
Vistas de la aplicación de Productos.

Define las vistas para listar, ver detalles y buscar productos.

Documentación: https://docs.djangoproject.com/es/5.0/topics/http/views/
"""

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db import models
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Producto, Categoria
from apps.eventos.utils import registrar_evento, obtener_ip_cliente, obtener_user_agent


def listar_productos(request):
    """
    Vista para listar todos los productos activos.

    Soporta filtrado por categoría, búsqueda y paginación.

    Args:
        request: Objeto HttpRequest

    Returns:
        HttpResponse con la página de listado de productos
    """
    productos = Producto.objects.filter(activo=True).select_related("categoria")

    # Filtrado por categoría
    categoria_id = request.GET.get("categoria")
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    # Búsqueda
    busqueda = request.GET.get("buscar", "").strip()
    if busqueda:
        productos = productos.filter(
            Q(nombre__icontains=busqueda) | Q(descripcion__icontains=busqueda)
        )
        
        # Registrar evento de búsqueda (protegido contra fallos)
        try:
            usuario = request.user if request.user.is_authenticated else None
            registrar_evento(
                usuario=usuario,
                tipo="BUSCAR",
                descripcion=f"Búsqueda de productos: '{busqueda}'",
                url=request.build_absolute_uri(),
                ip_address=obtener_ip_cliente(request),
                user_agent=obtener_user_agent(request),
                datos_adicionales={"termino_busqueda": busqueda}
            )
        except Exception:
            pass

    # Ordenamiento seguro
    orden_permitidos = ["nombre", "-nombre", "precio", "-precio", "created_at", "-created_at"]
    orden = request.GET.get("orden", "-created_at")
    if orden not in orden_permitidos:
        orden = "-created_at"
    productos = productos.order_by(orden)

    # Paginación
    paginator = Paginator(productos, 12)  # 12 productos por página
    numero_pagina = request.GET.get("pagina")
    pagina = paginator.get_page(numero_pagina)

    # Contexto
    categorias = Categoria.objects.filter(activa=True)

    contexto = {
        "pagina": pagina,
        "productos": pagina.object_list,
        "categorias": categorias,
        "busqueda": busqueda,
        "total_productos": paginator.count,
    }

    return render(request, "productos/listar_productos.html", contexto)


def detalle_producto(request, slug):
    """
    Vista para mostrar detalles de un producto.

    Args:
        request: Objeto HttpRequest
        slug: Identificador único del producto

    Returns:
        HttpResponse con la página de detalles del producto
    """
    producto = get_object_or_404(Producto, slug=slug, activo=True)
    
    # Registrar evento de visualización de producto (protegido contra fallos)
    try:
        usuario = request.user if request.user.is_authenticated else None
        registrar_evento(
            usuario=usuario,
            tipo="VER_PRODUCTO",
            descripcion=f"Visualización de producto: {producto.nombre}",
            url=request.build_absolute_uri(),
            ip_address=obtener_ip_cliente(request),
            user_agent=obtener_user_agent(request),
            datos_adicionales={"producto_id": producto.id, "producto_slug": producto.slug}
        )
    except Exception:
        pass

    # Productos relacionados (misma categoría)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria, activo=True
    ).exclude(id=producto.id)[:4]

    contexto = {
        "producto": producto,
        "productos_relacionados": productos_relacionados,
        "galeria": producto.galeria.all(),
    }

    return render(request, "productos/detalle_producto.html", contexto)


def listar_categorias(request):
    """
    Vista para listar todas las categorías activas.

    Args:
        request: Objeto HttpRequest

    Returns:
        HttpResponse con la página de categorías
    """
    categorias = Categoria.objects.filter(activa=True).annotate(
        cantidad_productos=models.Count("productos", filter=Q(productos__activo=True))
    )

    contexto = {
        "categorias": categorias,
    }

    return render(request, "productos/categorias.html", contexto)


def productos_destacados(request):
    """
    Vista para mostrar productos destacados.

    Args:
        request: Objeto HttpRequest

    Returns:
        HttpResponse con productos destacados
    """
    productos = Producto.objects.filter(activo=True, destacado=True).order_by(
        "-created_at"
    )[:8]

    contexto = {
        "productos": productos,
        "titulo": "Productos Destacados",
    }

    return render(request, "productos/productos_destacados.html", contexto)


# Vista basada en clases (CBV) - Alternativa
class ListaProductosView(ListView):
    """
    Vista basada en clases para listar productos.

    Alternativa moderna a la vista listar_productos.
    """

    model = Producto
    template_name = "productos/listar_productos_cbv.html"
    context_object_name = "productos"
    paginate_by = 12

    def get_queryset(self):
        """Retorna solo productos activos."""
        return Producto.objects.filter(activo=True).select_related("categoria")

    def get_context_data(self, **kwargs):
        """Agrega datos adicionales al contexto."""
        contexto = super().get_context_data(**kwargs)
        contexto["categorias"] = Categoria.objects.filter(activa=True)
        contexto["busqueda"] = self.request.GET.get("buscar", "")
        return contexto


class DetalleProductoView(DetailView):
    """
    Vista basada en clases para mostrar detalles de un producto.

    Alternativa moderna a la vista detalle_producto.
    """

    model = Producto
    template_name = "productos/detalle_producto_cbv.html"
    context_object_name = "producto"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        """Retorna solo productos activos."""
        return Producto.objects.filter(activo=True)

    def get_object(self, queryset=None):
        producto = super().get_object(queryset)
        try:
            usuario = self.request.user if self.request.user.is_authenticated else None
            registrar_evento(
                usuario=usuario,
                tipo="VER_PRODUCTO",
                descripcion=f"Visualización de producto: {producto.nombre}",
                url=self.request.build_absolute_uri(),
                ip_address=obtener_ip_cliente(self.request),
                user_agent=obtener_user_agent(self.request),
                datos_adicionales={"producto_id": producto.id, "producto_slug": producto.slug}
            )
        except Exception:
            pass
        return producto

    def get_context_data(self, **kwargs):
        """Agrega productos relacionados al contexto."""
        contexto = super().get_context_data(**kwargs)
        producto = self.object
        contexto["productos_relacionados"] = Producto.objects.filter(
            categoria=producto.categoria, activo=True
        ).exclude(id=producto.id)[:4]
        contexto["galeria"] = producto.galeria.all()
        return contexto