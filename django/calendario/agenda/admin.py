from django.contrib import admin

from agenda.models import Categoria, Evento, Lembrete

admin.site.register(Evento)
admin.site.register(Categoria)
admin.site.register(Lembrete)
