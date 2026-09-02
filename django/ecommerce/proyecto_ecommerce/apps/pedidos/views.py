"""
Vistas de la aplicación de Pedidos.

Define las vistas para crear, listar, ver detalles de pedidos y procesar webhooks de pago.
"""

import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.db import transaction
from decouple import config

from apps.carrito.models import Carrito
from apps.productos.models import Producto
from apps.usuarios.models import Direccion
from .models import Pedido, ItemPedido, HistorialPedido
from .forms import CrearPedidoForm
from apps.eventos.utils import registrar_evento, obtener_ip_cliente, obtener_user_agent


@login_required(login_url="usuarios:login")
def crear_pedido(request):
    """
    Vista para crear un nuevo pedido desde el carrito con protección de concurrencia.
    """
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    if not carrito.items.exists():
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("carrito:ver")

    direcciones = request.user.direcciones.filter(activa=True)

    if request.method == "POST":
        form = CrearPedidoForm(request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    # Bloqueo pesimista para evitar race conditions en el stock
                    for item_carrito in carrito.items.all():
                        producto = Producto.objects.select_for_update().get(id=item_carrito.producto.id)
                        producto.reducir_stock(item_carrito.cantidad)

                    # Crear pedido
                    pedido = Pedido.objects.create(
                        usuario=request.user,
                        estado="pendiente",
                        direccion_envio=form.cleaned_data.get("direccion_envio"),
                        metodo_pago=form.cleaned_data["metodo_pago"],
                        notas=form.cleaned_data.get("notas", ""),
                    )

                    # Crear items del pedido desde el carrito
                    for item_carrito in carrito.items.all():
                        ItemPedido.objects.create(
                            pedido=pedido,
                            producto=item_carrito.producto,
                            cantidad=item_carrito.cantidad,
                            precio_unitario=item_carrito.precio_unitario,
                        )

                    # Calcular y guardar totales
                    pedido.save()

                    # Registrar en historial
                    HistorialPedido.objects.create(
                        pedido=pedido,
                        estado_nuevo="pendiente",
                        notas="Pedido creado exitosamente."
                    )

                    # Registrar evento de crear pedido
                    registrar_evento(
                        usuario=request.user,
                        tipo="CREAR_PEDIDO",
                        descripcion=f"Pedido creado: {pedido.numero_pedido} - Total: ${pedido.total}",
                        url=request.build_absolute_uri(),
                        ip_address=obtener_ip_cliente(request),
                        user_agent=obtener_user_agent(request),
                        datos_adicionales={
                            "numero_pedido": pedido.numero_pedido,
                            "total": float(pedido.total),
                            "metodo_pago": pedido.metodo_pago,
                            "cantidad_items": pedido.items.count()
                        }
                    )

                    # Limpiar carrito
                    carrito.limpiar()

            except ValueError as e:
                # Stock insuficiente capturado por el modelo Producto
                messages.error(request, str(e))
                return redirect("carrito:ver")

            if pedido.metodo_pago == "tarjeta":
                # TODO: Implementar redirección real a la sesión de Stripe
                messages.info(request, "Redirigiendo a la pasarela de pago segura...")
                return redirect("pedidos:detalle", numero_pedido=pedido.numero_pedido)
            
            messages.success(request, f"Pedido {pedido.numero_pedido} creado exitosamente.")
            return redirect("pedidos:detalle", numero_pedido=pedido.numero_pedido)
    else:
        form = CrearPedidoForm()

    contexto = {
        "form": form,
        "carrito": carrito,
        "direcciones": direcciones,
        "titulo": "Crear Pedido",
    }

    return render(request, "pedidos/crear_pedido.html", contexto)


@login_required(login_url="usuarios:login")
def listar_pedidos(request):
    """
    Vista para listar los pedidos del usuario.
    """
    pedidos = request.user.pedidos.all()
    estado = request.GET.get("estado")
    if estado:
        pedidos = pedidos.filter(estado=estado)

    contexto = {
        "pedidos": pedidos,
        "titulo": "Mis Pedidos",
        "estado_filtro": estado,
    }
    return render(request, "pedidos/listar_pedidos.html", contexto)


@login_required(login_url="usuarios:login")
def detalle_pedido(request, numero_pedido):
    """
    Vista para ver los detalles de un pedido.
    """
    pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido, usuario=request.user)
    contexto = {
        "pedido": pedido,
        "items": pedido.items.select_related("producto"),
        "historial": pedido.historial.all(),
        "titulo": f"Pedido {pedido.numero_pedido}",
    }
    return render(request, "pedidos/detalle_pedido.html", contexto)


@login_required(login_url="usuarios:login")
def cancelar_pedido(request, numero_pedido):
    """
    Vista para cancelar un pedido, restaurando el stock.
    """
    pedido = get_object_or_404(Pedido, numero_pedido=numero_pedido, usuario=request.user)

    if not pedido.puede_cancelarse():
        messages.error(request, "Este pedido no puede ser cancelado.")
        return redirect("pedidos:detalle", numero_pedido=numero_pedido)

    with transaction.atomic():
        estado_anterior = pedido.estado
        pedido.estado = "cancelado"
        pedido.save()

        HistorialPedido.objects.create(
            pedido=pedido,
            estado_anterior=estado_anterior,
            estado_nuevo="cancelado",
            notas="Pedido cancelado por el cliente",
        )

        # Restaurar stock usando select_for_update para evitar concurrencia
        for item in pedido.items.all():
            if item.producto:
                producto = Producto.objects.select_for_update().get(id=item.producto.id)
                producto.aumentar_stock(item.cantidad)
        
        # Registrar evento de cancelar pedido
        registrar_evento(
            usuario=request.user,
            tipo="CANCELAR_PEDIDO",
            descripcion=f"Pedido cancelado: {pedido.numero_pedido}",
            url=request.build_absolute_uri(),
            ip_address=obtener_ip_cliente(request),
            user_agent=obtener_user_agent(request),
            datos_adicionales={
                "numero_pedido": pedido.numero_pedido,
                "estado_anterior": estado_anterior,
                "estado_nuevo": "cancelado"
            }
        )

    messages.success(request, f"Pedido {pedido.numero_pedido} cancelado.")
    return redirect("pedidos:detalle", numero_pedido=numero_pedido)


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """
    Endpoint para procesar eventos asíncronos de Stripe (Pago completado).
    """
    stripe.api_key = config('STRIPE_SECRET_KEY', default='')
    endpoint_secret = config('STRIPE_WEBHOOK_SECRET', default='')
    
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        numero_pedido = session.get('client_reference_id')
        
        if numero_pedido:
            try:
                with transaction.atomic():
                    pedido = Pedido.objects.select_for_update().get(numero_pedido=numero_pedido)
                    if pedido.estado == 'pendiente':
                        pedido.marcar_como_pagado()
                        estado_anterior = pedido.estado
                        pedido.estado = 'confirmado'
                        pedido.save()
                        
                        HistorialPedido.objects.create(
                            pedido=pedido,
                            estado_anterior=estado_anterior,
                            estado_nuevo='confirmado',
                            notas='Pago confirmado automaticamente via Stripe.'
                        )
            except Pedido.DoesNotExist:
                pass

    return HttpResponse(status=200)


# Vistas basadas en clases (alternativas)
class ListaPedidosView(ListView):
    model = Pedido
    template_name = "pedidos/lista_pedidos_cbv.html"
    context_object_name = "pedidos"
    paginate_by = 10

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user).order_by("-fecha_creacion")


class DetallePedidoView(DetailView):
    model = Pedido
    template_name = "pedidos/detalle_pedido_cbv.html"
    context_object_name = "pedido"
    slug_field = "numero_pedido"
    slug_url_kwarg = "numero_pedido"

    def get_queryset(self):
        return Pedido.objects.filter(usuario=self.request.user)