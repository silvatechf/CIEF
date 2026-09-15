from django.shortcuts import render
from rest_framework import viewsets
from .models import Tarea
from .serializers import TareaSerializer

# Create your views here.
class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.all()
    serializer_class = TareaSerializer
