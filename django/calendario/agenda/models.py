from django.db import models
from django.urls import reverse
from django.utils import timezone


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default="")
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    ubicacion = models.CharField(max_length=255, blank=True, default="")
    categoria = models.ManyToManyField(Categoria, related_name="eventos", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("evento_detalle", kwargs={"pk": self.pk})

    @property
    def duracion_horas(self):
        delta = self.fecha_fin - self.fecha_inicio
        return max(delta.total_seconds() / 3600, 0)


class Lembrete(models.Model):
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name="lembretes",
    )
    numero_whatsapp = models.CharField(max_length=20)
    quantidade_lembretes = models.PositiveIntegerField(default=0)
    ultimo_lembrete = models.DateTimeField(null=True, blank=True)
    ultima_interacao = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("evento", "numero_whatsapp")

    def __str__(self):
        return f"{self.evento.titulo} - {self.numero_whatsapp}"
