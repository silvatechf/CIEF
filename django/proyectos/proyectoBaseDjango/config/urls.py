from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.core.views import home


urlpatterns = [
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "",
        home,
        name="home",
    ),
    path(
        "api/",
        include("apps.tareas.urls"),
    ),
    path(
        "api/",
        include("apps.productos.urls"),
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )