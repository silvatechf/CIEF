from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from agenda.forms import EventoForm
from agenda.models import Categoria, Evento
from agenda.services import processar_lembrete


def home(request):
    proximos = Evento.objects.filter(fecha_inicio__gte=timezone.now()).order_by(
        "fecha_inicio"
    )[:5]
    total_eventos = Evento.objects.count()
    hoy = timezone.now()
    return render(
        request,
        "agenda/home.html",
        {
            "proximos": proximos,
            "total_eventos": total_eventos,
            "hoy": hoy,
        },
    )


def eventos(request):
    queryset = Evento.objects.all().order_by("fecha_inicio")
    query = request.GET.get("q", "").strip()
    categoria_id = request.GET.get("categoria")

    if query:
        queryset = queryset.filter(
            Q(titulo__icontains=query)
            | Q(descripcion__icontains=query)
            | Q(ubicacion__icontains=query)
        )

    if categoria_id:
        queryset = queryset.filter(categoria=categoria_id)

    categorias = Categoria.objects.all().order_by("nombre")
    categoria_actual = (
        categorias.filter(id=categoria_id).first() if categoria_id else None
    )

    return render(
        request,
        "agenda/eventos.html",
        {
            "data": queryset,
            "categorias": categorias,
            "query": query,
            "categoria_actual": categoria_actual,
        },
    )


def evento_detalle(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    return render(request, "agenda/evento_detalle.html", {"evento": evento})


def evento_crear(request):
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save()
            return redirect("evento_detalle", pk=evento.pk)
    else:
        form = EventoForm()

    return render(
        request, "agenda/evento_form.html", {"form": form, "titulo": "Crear evento"}
    )


def evento_editar(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            evento = form.save()
            return redirect("evento_detalle", pk=evento.pk)
    else:
        form = EventoForm(instance=evento)

    return render(
        request, "agenda/evento_form.html", {"form": form, "titulo": "Editar evento"}
    )


def evento_eliminar(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == "POST":
        evento.delete()
        return redirect("eventos")
    return redirect("evento_detalle", pk=evento.pk)


def lembrete_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    numero_whatsapp = request.GET.get("numero_whatsapp", "5511999999999")
    resultado = processar_lembrete(evento, numero_whatsapp=numero_whatsapp)
    return JsonResponse(
        {
            "ok": True,
            "evento": evento.titulo,
            "chamada_whatsapp": resultado["chamada_whatsapp"],
            "quantidade_lembretes": resultado["quantidade_lembretes"],
        }
    )
