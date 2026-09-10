"""
Configuración de Django para el proyecto Ecommerce.
"""

import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# SEGURIDAD
SECRET_KEY = "django-insecure-cambiar-esta-clave-en-produccion"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# APLICACIONES INSTALADAS
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Apps locales
    "apps.productos",
    "apps.usuarios",
    "apps.carrito",
    "apps.pedidos",
    "apps.eventos",
]

# MIDDLEWARE
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.eventos.middleware.RastreadorEventosMiddleware",
]

ROOT_URLCONF = "config.urls"

# PLANTILLAS (TEMPLATES)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # Context Processor para disponibilizar o carrinho em todo o projeto
                #"apps.carrito.context_processors.carrito",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# BASE DE DATOS
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# VALIDACIÓN DE CONTRASEÑAS
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# INTERNACIONALIZACIÓN
LANGUAGE_CODE = "es-es"
TIME_ZONE = "America/Mexico_City"
USE_I18N = True
USE_TZ = True

# ARCHIVOS ESTÁTICOS Y MEDIA
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"  # Usando pathlib (estándar en Django moderno)

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# CONFIGURACIÓN DE SESIONES
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True

# CONFIGURACIÓN DE CACHÉ
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "ecommerce-cache",
    }
}

# LOGGING
LOGS_DIR = BASE_DIR / "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": LOGS_DIR / "django.log",
            "encoding": "utf-8",
            "formatter": "verbose",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": "INFO",
    },
}