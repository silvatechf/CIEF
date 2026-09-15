from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.core import views


urlpatterns = [
    path(
        "",views.home,name="home"
    ),
  
]


