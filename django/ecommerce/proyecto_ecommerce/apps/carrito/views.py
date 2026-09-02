"""
Vistas de la aplicación de Carrito.

Define las vistas para gestionar el carrito de compras.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from apps.productos.models import Producto
from .models import Carrito, ItemCarrito
from apps.eventos.utils import registrar_evento, obtener_ip_cliente, obtener_user_agent


@login_required(login_url="usuarios:login")
def ver_carrito(request):
    """
    Vista para ver el contenido del carrito.

    Args:
        request: Objeto HttpRequest

    Returns:
        HttpResponse con la página del carrito
    """
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    contexto = {
        "carrito": carrito,
        "items": carrito.items.select_related("producto").all(),
        "titulo": "Mi Carrito",
    }

    return render(request, "carrito/ver_carrito.html", contexto)


@login_required(login_url="usuarios:login")
@require_POST
def agregar_al_carrito(request, producto_id):
    """
    Vista para agregar un producto al carrito.

    Args:
        request: Objeto HttpRequest
        producto_id: ID del producto a agregar

    Returns:
        Redirección o JSON response
    """
    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    # Obtener cantidad del formulario
    cantidad = int(request.POST.get("cantidad", 1))

    # Validar stock disponible
    if cantidad > producto.stock:
        messages.warning(
            request, f"No hay suficiente stock. Disponible: {producto.stock}"
        )
        return redirect("productos:detalle", slug=producto.slug)

    # Obtener o crear item
    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto,
        defaults={"cantidad": cantidad, "precio_unitario": producto.precio_final},
    )

    if not creado:
        # Si el item ya existe, aumentar cantidad
        if item.cantidad + cantidad > producto.stock:
            messages.warning(
                request, f"Stock insuficiente. Máximo disponible: {producto.stock}"
            )
        else:
            item.cantidad += cantidad
            item.save()
            messages.success(request, f"{producto.nombre} agregado al carrito.")
    else:
        messages.success(request, f"{producto.nombre} agregado al carrito.")
    
    # Registrar evento de agregar al carrito
    registrar_evento(
        usuario=request.user,
        tipo="AGREGAR_CARRITO",
        descripcion=f"Agregado al carrito: {producto.nombre} (cantidad: {cantidad})",
        url=request.build_absolute_uri(),
        ip_address=obtener_ip_cliente(request),
        user_agent=obtener_user_agent(request),
        datos_adicionales={
            "producto_id": producto.id,
            "producto_nombre": producto.nombre,
            "cantidad": cantidad,
            "precio": float(producto.precio_final)
        }
    )

    # Redirigir al carrito si se solicita, si no a la página de producto
    siguiente = request.POST.get(
        "siguiente", request.META.get("HTTP_REFERER", "carrito:ver")
    )
    return redirect(siguiente)


@login_required(login_url="usuarios:login")
def actualizar_carrito(request):
    """
    Vista para actualizar cantidades en el carrito.

    Args:
        request: Objeto HttpRequest

    Returns:
        HttpResponse con la página del carrito actualizada
    """
    if request.method == "POST":
        carrito = get_object_or_404(Carrito, usuario=request.user)

        # Obtener actualizaciones de cantidad
        for item_id, cantidad in request.POST.items():
            if item_id.startswith("cantidad_"):
                item_id = item_id.replace("cantidad_", "")
                item = ItemCarrito.objects.filter(id=item_id, carrito=carrito).first()

                if item:
                    try:
                        cantidad = int(cantidad)
                        if cantidad > 0:
                            item.cantidad = cantidad
                            item.save()
                        elif cantidad == 0:
                            item.delete()
                    except (ValueError, TypeError):
                        pass

        messages.success(request, "Carrito actualizado.")

    return redirect("carrito:ver")


@login_required(login_url="usuarios:login")
@require_POST
def eliminar_del_carrito(request, item_id):
    """
    Vista para eliminar un item del carrito.

    Args:
        request: Objeto HttpRequest
        item_id: ID del item a eliminar

    Returns:
        Redirección al carrito
    """
    item = get_object_or_404(ItemCarrito, id=item_id, carrito__usuario=request.user)
    producto_nombre = item.producto.nombre
    producto_id = item.producto.id
    
    item.delete()
    
    # Registrar evento de eliminar del carrito
    registrar_evento(
        usuario=request.user,
        tipo="ELIMINAR_CARRITO",
        descripcion=f"Eliminado del carrito: {producto_nombre}",
        url=request.build_absolute_uri(),
        ip_address=obtener_ip_cliente(request),
        user_agent=obtener_user_agent(request),
        datos_adicionales={
            "producto_id": producto_id,
            "producto_nombre": producto_nombre
        }
    )
    
    messages.success(request, f"{producto_nombre} eliminado del carrito.")
    return redirect("carrito:ver")


@login_required(login_url="usuarios:login")
@require_POST
def limpiar_carrito(request):
    """
    Vista para vaciar completamente el carrito.

    Args:
        request: Objeto HttpRequest

    Returns:
        Redirección al carrito
    """
    carrito = get_object_or_404(Carrito, usuario=request.user)
    carrito.limpiar()
    messages.success(request, "Carrito vaciado.")
    return redirect("carrito:ver")


@login_required(login_url="usuarios:login")
def contador_carrito(request):
    """
    Vista AJAX para obtener el contador de items en el carrito.

    Args:
        request: Objeto HttpRequest

    Returns:
        JSON response con la cantidad de items
    """
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    return JsonResponse(
        {
            "cantidad": carrito.cantidad_items,
            "total": str(carrito.total),
        }
    )
