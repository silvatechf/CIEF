"""
Guía de desarrollo - Ecommerce Django

Este archivo contiene información útil para desarrolladores que quieran
contribuir o expandir el proyecto.
"""

# ESTRUCTURA DEL PROYECTO
# ========================

# El proyecto está organizado en aplicaciones Django reutilizables:
#
# apps/
#   ├── productos/      - Gestión del catálogo
#   ├── usuarios/       - Autenticación y perfiles
#   ├── carrito/        - Carrito de compras
#   └── pedidos/        - Gestión de pedidos
#
# Cada aplicación sigue la estructura:
#   - __init__.py
#   - apps.py           - Configuración de la app
#   - models.py         - Modelos de datos
#   - views.py          - Vistas (función-based y class-based)
#   - forms.py          - Formularios
#   - urls.py           - Rutas
#   - admin.py          - Personalización del admin
#   - tests.py          - Tests unitarios
#   - serializers.py    - (opcional) Para API REST

# AGREGAR NUEVAS FUNCIONALIDADES
# ================================

# Ejemplo 1: Crear una nueva aplicación
# 1. python manage.py startapp resenas
# 2. Crear modelos en resenas/models.py
# 3. Registrar en apps de INSTALLED_APPS
# 4. Crear migraciones: python manage.py makemigrations
# 5. Aplicar: python manage.py migrate

# Ejemplo 2: Agregar un modelo a una aplicación existente
# 1. Editar apps/productos/models.py
# 2. Crear migraciones: python manage.py makemigrations
# 3. Aplicar: python manage.py migrate
# 4. (Opcional) Registrar en admin.py

# EJECUTAR TESTS
# ===============

"""
Ejecutar todos los tests:
    python manage.py test

Ejecutar tests de una aplicación:
    python manage.py test apps.productos

Ejecutar una clase de tests:
    python manage.py test apps.productos.tests.ProductoTestCase

Ejecutar un test específico:
    python manage.py test apps.productos.tests.ProductoTestCase.test_crear_producto

Con verbosidad:
    python manage.py test --verbosity=2

Ver cobertura de tests (requiere coverage):
    pip install coverage
    coverage run --source='.' manage.py test
    coverage report
"""

# SHELL DE DJANGO
# ================

"""
Acceder al shell interactivo:
    python manage.py shell

Ejemplos de uso:

    # Importar modelos
    from apps.productos.models import Producto, Categoria
    from apps.usuarios.models import Perfil
    from apps.carrito.models import Carrito
    from apps.pedidos.models import Pedido

    # Crear categoría
    cat = Categoria.objects.create(nombre='Nuevos')
    
    # Crear producto
    prod = Producto.objects.create(
        nombre='Producto',
        descripcion='Desc',
        categoria=cat,
        precio=100,
        stock=10
    )
    
    # Consultar
    Producto.objects.all()
    Producto.objects.filter(precio__gte=100)
    Producto.objects.get(id=1)
    
    # Actualizar
    prod.precio = 150
    prod.save()
    
    # Eliminar
    prod.delete()
    
    # Relaciones
    cat.productos.all()
    
    # Contar
    Producto.objects.count()
"""

# REALIZAR QUERIES
# =================

"""
Operadores de filtrado:

    __exact      - Coincidencia exacta (default)
    __iexact     - Coincidencia insensible a mayúsculas
    __contains   - Contiene
    __icontains  - Contiene (insensible a mayúsculas)
    __gt         - Mayor que
    __gte        - Mayor o igual
    __lt         - Menor que
    __lte        - Menor o igual
    __startswith - Comienza con
    __istartswith - Comienza con (insensible a mayúsculas)
    __endswith   - Termina con
    __iendswith  - Termina con (insensible a mayúsculas)
    __range      - Rango
    __in         - En lista
    __isnull     - Es nulo
    __year       - Año
    __month      - Mes
    __day        - Día

Ejemplos:

    Producto.objects.filter(precio__gte=100)           # precio >= 100
    Producto.objects.filter(nombre__icontains='lap')   # nombre contiene 'lap'
    Producto.objects.filter(stock__gt=0)               # stock > 0
    Producto.objects.filter(created_at__year=2024)     # creado en 2024
"""

# MIGRACIONES
# ============

"""
Crear migraciones después de cambiar modelos:
    python manage.py makemigrations
    
Aplicar migraciones:
    python manage.py migrate

Ver migraciones pendientes:
    python manage.py showmigrations
    
Ver SQL que ejecutarán las migraciones:
    python manage.py sqlmigrate apps.productos 0001

Revertir migraciones:
    python manage.py migrate apps.productos 0001  # Ir a una migración específica
    python manage.py migrate apps.productos zero   # Revertir todas
"""

# VARIABLES DE ENTORNO
# ====================

"""
Para usar variables de entorno (recomendado para producción):

1. Instalar: pip install python-decouple

2. Crear archivo .env en la raíz del proyecto:
    SECRET_KEY=tu-clave-secreta-aqui
    DEBUG=False
    ALLOWED_HOSTS=localhost,127.0.0.1,tudominio.com
    DATABASE_URL=postgresql://user:password@localhost/dbname

3. En settings.py:
    from decouple import config
    
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEBUG', default=False, cast=bool)
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=lambda v: [s.strip() for s in v.split(',')])

4. IMPORTANTE: Agregar .env a .gitignore
"""

# LOGGING
# ========

"""
El proyecto incluye configuración de logging en settings.py.

Los logs se guardan en:
    logs/django.log

En tus vistas/modelos puedes usarlos:

    import logging
    logger = logging.getLogger(__name__)
    
    logger.debug('Mensaje de debug')
    logger.info('Información')
    logger.warning('Advertencia')
    logger.error('Error')
    logger.critical('Error crítico')
"""

# OPTIMIZACIÓN DE QUERIES
# ========================

"""
Usar select_related() para Foreign Keys (relaciones uno-a-muchos):
    Producto.objects.select_related('categoria').all()

Usar prefetch_related() para Many-to-Many y reverse relations:
    Carrito.objects.prefetch_related('items__producto').all()

Evitar N+1 queries:
    ✗ for carrito in carritos:
        print(carrito.usuario.username)
    
    ✓ carritos = Carrito.objects.select_related('usuario')
      for carrito in carritos:
          print(carrito.usuario.username)

Usar values()/values_list() para proyecciones:
    Producto.objects.values('nombre', 'precio')  # Dict
    Producto.objects.values_list('nombre', flat=True)  # Lista
"""

# SIGNAL (Señales)
# =================

"""
Las señales permiten ejecutar código cuando ocurre algo:

Ejemplo en apps/usuarios/signals.py:

    from django.db.models.signals import post_save
    from django.dispatch import receiver
    from django.contrib.auth.models import User
    from .models import Perfil
    
    @receiver(post_save, sender=User)
    def crear_perfil(sender, instance, created, **kwargs):
        if created:
            Perfil.objects.create(usuario=instance)
    
    @receiver(post_save, sender=User)
    def guardar_perfil(sender, instance, **kwargs):
        instance.perfil.save()

Y en apps/usuarios/apps.py:

    class UsuariosConfig(AppConfig):
        default_auto_field = 'django.db.models.BigAutoField'
        name = 'apps.usuarios'
        verbose_name = 'Gestión de Usuarios'
        
        def ready(self):
            import apps.usuarios.signals
"""

# CUSTOM MANAGERS
# ================

"""
Crear managers personalizados para queries comunes:

En models.py:

    from django.db import models
    
    class ProductoManager(models.Manager):
        def activos(self):
            return self.filter(activo=True)
        
        def con_descuento(self):
            return self.filter(precio_descuento__isnull=False)
    
    class Producto(models.Model):
        # ... campos ...
        objects = ProductoManager()
    
    # Uso:
    Producto.objects.activos()
    Producto.objects.con_descuento()
"""

# DECORADORES ÚTILES
# ====================

"""
@login_required          - Requiere que el usuario esté autenticado
@permission_required()   - Requiere permisos específicos
@require_http_methods()  - Restringe métodos HTTP (GET, POST, etc)
@require_GET / @require_POST
@cache_page()            - Cachea la respuesta
@vary_on_cookie          - Varía según cookies
@transaction.atomic      - Transacción ACID
"""

# FORMS Y VALIDACIÓN
# ====================

"""
Validación a nivel de campo:
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email ya registrado')
        return email

Validación a nivel de formulario:
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise ValidationError('Las contraseñas no coinciden')
        return cleaned_data

Validadores personalizados:
    from django.core.validators import RegexValidator
    
    telefono = models.CharField(
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message='Teléfono inválido'
            )
        ]
    )
"""

print(__doc__)
