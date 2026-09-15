from rest_framework import viewsets

from .models import Producto
from .serializers import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    filterset_fields = [
        "categoria",
        "activo",
    ]

    search_fields = [
        "nombre",
        "descripcion",
    ]

    ordering_fields = [
        "nombre",
        "precio",
        "stock",
        "creado_en",
    ]

    ordering = [
        "-creado_en",
    ]