"""
Modelos de la aplicación de Usuarios.

Define los modelos para la gestión de usuarios y perfiles.

Documentación: https://docs.djangoproject.com/es/5.0/topics/auth/
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Perfil(models.Model):
    """
    Modelo que extiende el usuario de Django con información adicional.

    Permite almacenar información personalizada de cada usuario.

    Atributos:
        usuario: Relación con el usuario de Django
        telefono: Número de teléfono del usuario
        direccion: Dirección de envío
        ciudad: Ciudad
        estado: Estado/Provincia
        codigo_postal: Código postal
        pais: País
        imagen_perfil: Foto de perfil
        bio: Biografía corta del usuario
        newsletter: Suscripción a newsletter
        created_at: Fecha de creación
        updated_at: Fecha de última actualización
    """

    usuario = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="perfil", verbose_name="Usuario"
    )

    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")

    direccion = models.CharField(max_length=255, blank=True, verbose_name="Dirección")

    ciudad = models.CharField(max_length=100, blank=True, verbose_name="Ciudad")

    estado = models.CharField(
        max_length=100, blank=True, verbose_name="Estado/Provincia"
    )

    codigo_postal = models.CharField(
        max_length=20, blank=True, verbose_name="Código Postal"
    )

    pais = models.CharField(max_length=100, blank=True, verbose_name="País")

    imagen_perfil = models.ImageField(
        upload_to="perfiles/", blank=True, null=True, verbose_name="Imagen de Perfil"
    )

    bio = models.TextField(max_length=500, blank=True, verbose_name="Biografía")

    newsletter = models.BooleanField(
        default=False, verbose_name="¿Desea recibir newsletter?"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Perfil"
        verbose_name_plural = "Perfiles"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

    def nombre_completo(self):
        """Retorna el nombre completo del usuario."""
        if self.usuario.first_name and self.usuario.last_name:
            return f"{self.usuario.first_name} {self.usuario.last_name}"
        return self.usuario.username

    def obtener_direccion_completa(self):
        """Retorna la dirección completa formateada."""
        partes = [
            self.direccion,
            self.ciudad,
            self.estado,
            self.codigo_postal,
            self.pais,
        ]
        return ", ".join([p for p in partes if p])


class Direccion(models.Model):
    """
    Modelo para guardar múltiples direcciones de un usuario.

    Permite que los usuarios tengan varias direcciones
    (hogar, trabajo, etc.).

    Atributos:
        usuario: Relación con el usuario
        tipo: Tipo de dirección (hogar, trabajo, otro)
        nombre: Nombre descriptivo de la dirección
        direccion: Dirección completa
        ciudad: Ciudad
        estado: Estado/Provincia
        codigo_postal: Código postal
        pais: País
        predeterminada: Marca si es la dirección por defecto
        activa: Marca si está activa
        created_at: Fecha de creación
    """

    TIPO_CHOICES = [
        ("hogar", "Hogar"),
        ("trabajo", "Trabajo"),
        ("otra", "Otra"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="direcciones",
        verbose_name="Usuario",
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default="hogar",
        verbose_name="Tipo de dirección",
    )

    nombre = models.CharField(max_length=100, verbose_name="Nombre descriptivo")

    direccion = models.CharField(max_length=255, verbose_name="Dirección")

    ciudad = models.CharField(max_length=100, verbose_name="Ciudad")

    estado = models.CharField(max_length=100, verbose_name="Estado/Provincia")

    codigo_postal = models.CharField(max_length=20, verbose_name="Código Postal")

    pais = models.CharField(max_length=100, verbose_name="País")

    predeterminada = models.BooleanField(
        default=False, verbose_name="¿Dirección por defecto?"
    )

    activa = models.BooleanField(default=True, verbose_name="¿Activa?")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de creación"
    )

    class Meta:
        verbose_name = "Dirección"
        verbose_name_plural = "Direcciones"
        ordering = ["-predeterminada", "-created_at"]

    def __str__(self):
        return f"{self.nombre} - {self.usuario.username}"

    def obtener_direccion_completa(self):
        """Retorna la dirección completa formateada."""
        partes = [
            self.direccion,
            self.ciudad,
            self.estado,
            self.codigo_postal,
            self.pais,
        ]
        return ", ".join([p for p in partes if p])

    def save(self, *args, **kwargs):
        """Si esta es la dirección predeterminada, desactiva las otras."""
        if self.predeterminada:
            Direccion.objects.filter(usuario=self.usuario, predeterminada=True).exclude(
                id=self.id
            ).update(predeterminada=False)
        super().save(*args, **kwargs)
