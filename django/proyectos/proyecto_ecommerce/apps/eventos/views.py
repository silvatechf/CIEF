from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from .models import Evento


@login_required
def listar_mis_eventos(request):
    """Vista para que el usuario vea sus propios eventos."""
    eventos = Evento.objects.filter(usuario=request.user).order_by("-fecha_creacion")[:100]
    
    # Estadísticas del usuario
    hoy = timezone.now().date()
    hace_7_dias = timezone.now() - timedelta(days=7)
    
    estadisticas = {
        "total_eventos": Evento.objects.filter(usuario=request.user).count(),
        "eventos_hoy": Evento.objects.filter(
            usuario=request.user,
            fecha_creacion__date=hoy
        ).count(),
        "eventos_7_dias": Evento.objects.filter(
            usuario=request.user,
            fecha_creacion__gte=hace_7_dias
        ).count(),
    }
    
    # Contar eventos por tipo
    tipos_eventos = Evento.objects.filter(usuario=request.user).values('tipo').annotate(count=Count('id')).order_by('-count')
    
    contexto = {
        "eventos": eventos,
        "estadisticas": estadisticas,
        "tipos_eventos": tipos_eventos,
    }
    
    return render(request, "eventos/listar_eventos.html", contexto)


class EventoListView(LoginRequiredMixin, ListView):
    """Vista para mostrar una lista de eventos (solo para administradores)."""
    model = Evento
    template_name = "eventos/eventos_admin.html"
    context_object_name = "eventos"
    paginate_by = 50
    
    def get_queryset(self):
        """Solo superusuarios pueden ver todos los eventos."""
        if not self.request.user.is_superuser:
            return Evento.objects.filter(usuario=self.request.user).order_by("-fecha_creacion")
        return Evento.objects.all().order_by("-fecha_creacion")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Filtros
        tipo_filtro = self.request.GET.get("tipo")
        usuario_filtro = self.request.GET.get("usuario")
        fecha_desde = self.request.GET.get("fecha_desde")
        fecha_hasta = self.request.GET.get("fecha_hasta")
        
        if tipo_filtro:
            context["eventos"] = context["eventos"].filter(tipo=tipo_filtro)
        
        if usuario_filtro and self.request.user.is_superuser:
            context["eventos"] = context["eventos"].filter(usuario__username__icontains=usuario_filtro)
        
        if fecha_desde:
            context["eventos"] = context["eventos"].filter(fecha_creacion__gte=fecha_desde)
        
        if fecha_hasta:
            context["eventos"] = context["eventos"].filter(fecha_creacion__lte=fecha_hasta)
        
        # Estadísticas
        context["total_eventos"] = self.get_queryset().count()
        context["tipos_disponibles"] = Evento.objects.values_list("tipo", flat=True).distinct()
        
        return context
