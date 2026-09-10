"""
Vistas de la aplicación de Usuarios.

Define las vistas para registro, login, perfil y direcciones.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Perfil, Direccion
from .forms import RegistroForm, PerfilForm, DireccionForm
from apps.eventos.utils import registrar_evento, obtener_ip_cliente, obtener_user_agent


def registrarse(request):
    """Vista para el registro de nuevos usuarios."""
    if request.user.is_authenticated:
        return redirect("productos:listar")

    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data["password"])
            usuario.save()

            # Garantiza la creación del perfil
            Perfil.objects.get_or_create(usuario=usuario)
            
            # Registrar evento de registro
            try:
                registrar_evento(
                    usuario=usuario,
                    tipo="REGISTRO",
                    descripcion=f"Nuevo usuario registrado: {usuario.username}",
                    url=request.build_absolute_uri(),
                    ip_address=obtener_ip_cliente(request),
                    user_agent=obtener_user_agent(request)
                )
            except Exception:
                pass

            messages.success(
                request, "Usuario registrado exitosamente. Por favor inicia sesión."
            )
            return redirect("usuarios:login")
    else:
        form = RegistroForm()

    contexto = {
        "form": form,
        "titulo": "Registro",
    }

    return render(request, "usuarios/registrarse.html", contexto)


def login_view(request):
    """Vista para el login de usuarios."""
    if request.user.is_authenticated:
        return redirect("productos:listar")

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        usuario = authenticate(request, username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            
            # Registrar evento de login
            try:
                registrar_evento(
                    usuario=usuario,
                    tipo="LOGIN",
                    descripcion=f"Usuario {usuario.username} ha iniciado sesión",
                    url=request.build_absolute_uri(),
                    ip_address=obtener_ip_cliente(request),
                    user_agent=obtener_user_agent(request)
                )
            except Exception:
                pass
            
            messages.success(request, f"Bienvenido {usuario.username}")
            
            next_url = request.POST.get("next") or request.GET.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("productos:listar")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")

    return render(request, "usuarios/login.html")


@login_required(login_url="usuarios:login")
def logout_view(request):
    """Vista para el logout de usuarios."""
    usuario = request.user
    
    try:
        registrar_evento(
            usuario=usuario,
            tipo="LOGOUT",
            descripcion=f"Usuario {usuario.username} ha cerrado sesión",
            url=request.build_absolute_uri(),
            ip_address=obtener_ip_cliente(request),
            user_agent=obtener_user_agent(request)
        )
    except Exception:
        pass
    
    logout(request)
    messages.success(request, "Ha cerrado sesión exitosamente.")
    return redirect("productos:listar")


@login_required(login_url="usuarios:login")
def perfil(request):
    """Vista para ver y editar el perfil del usuario."""
    perfil_obj, _ = Perfil.objects.get_or_create(usuario=request.user)

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil_obj)
        if form.is_valid():
            form.save()
            
            try:
                registrar_evento(
                    usuario=request.user,
                    tipo="ACTUALIZAR_PERFIL",
                    descripcion=f"Usuario {request.user.username} actualizó su perfil",
                    url=request.build_absolute_uri(),
                    ip_address=obtener_ip_cliente(request),
                    user_agent=obtener_user_agent(request)
                )
            except Exception:
                pass
            
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect("usuarios:perfil")
    else:
        form = PerfilForm(instance=perfil_obj)

    direcciones = Direccion.objects.filter(usuario=request.user, activa=True) if hasattr(Direccion, 'activa') else Direccion.objects.filter(usuario=request.user)

    contexto = {
        "form": form,
        "perfil": perfil_obj,
        "direcciones": direcciones,
        "titulo": "Mi Perfil",
    }

    return render(request, "usuarios/perfil.html", contexto)


@login_required(login_url="usuarios:login")
def listar_direcciones(request):
    """Vista para listar las direcciones del usuario."""
    direcciones = Direccion.objects.filter(usuario=request.user, activa=True) if hasattr(Direccion, 'activa') else Direccion.objects.filter(usuario=request.user)

    contexto = {
        "direcciones": direcciones,
        "titulo": "Mis Direcciones",
    }

    return render(request, "usuarios/listar_direcciones.html", contexto)


@login_required(login_url="usuarios:login")
def crear_direccion(request):
    """Vista para crear una nueva dirección."""
    if request.method == "POST":
        form = DireccionForm(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.usuario = request.user
            direccion.save()
            messages.success(request, "Dirección creada exitosamente.")
            return redirect("usuarios:direcciones")
    else:
        form = DireccionForm()

    contexto = {
        "form": form,
        "titulo": "Nueva Dirección",
    }

    return render(request, "usuarios/crear_direccion.html", contexto)


@login_required(login_url="usuarios:login")
def editar_direccion(request, id):
    """Vista para editar una dirección existente."""
    direccion = get_object_or_404(Direccion, id=id, usuario=request.user)

    if request.method == "POST":
        form = DireccionForm(request.POST, instance=direccion)
        if form.is_valid():
            form.save()
            messages.success(request, "Dirección actualizada exitosamente.")
            return redirect("usuarios:direcciones")
    else:
        form = DireccionForm(instance=direccion)

    contexto = {
        "form": form,
        "direccion": direccion,
        "titulo": "Editar Dirección",
    }

    return render(request, "usuarios/editar_direccion.html", contexto)


@login_required(login_url="usuarios:login")
@require_http_methods(["POST"])
def eliminar_direccion(request, id):
    """Vista para eliminar una dirección (soft delete si aplica)."""
    direccion = get_object_or_404(Direccion, id=id, usuario=request.user)
    if hasattr(direccion, 'activa'):
        direccion.activa = False
        direccion.save()
    else:
        direccion.delete()
    messages.success(request, "Dirección eliminada exitosamente.")
    return redirect("usuarios:direcciones")