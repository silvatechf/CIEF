from django import forms

from agenda.models import Categoria, Evento


class EventoForm(forms.ModelForm):
    categoria = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all().order_by("nombre"),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Evento
        fields = [
            "titulo",
            "descripcion",
            "fecha_inicio",
            "fecha_fin",
            "ubicacion",
            "categoria",
        ]
        widgets = {
            "titulo": forms.TextInput(attrs={"placeholder": "Ej: Reunión de equipo"}),
            "descripcion": forms.Textarea(
                attrs={
                    "placeholder": "Describe el evento, los objetivos o detalles importantes"
                }
            ),
            "fecha_inicio": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "fecha_fin": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "ubicacion": forms.TextInput(attrs={"placeholder": "Ej: São Paulo, SP"}),
        }
        labels = {
            "titulo": "Título",
            "descripcion": "Descripción",
            "fecha_inicio": "Fecha de inicio",
            "fecha_fin": "Fecha de fin",
            "ubicacion": "Ubicación",
            "categoria": "Categorías",
        }
