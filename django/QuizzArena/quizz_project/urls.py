from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas para la API REST (Fase 2)
    path('api/v1/', include('quizz_app.api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    
    # Rutas para la aplicación Web HTML (Fase 1)
    path('', include('quizz_app.urls')),
]