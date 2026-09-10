# Ecommerce Django - Documentación Completa

## 📋 Tabla de Contenidos

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación y Configuración](#instalación-y-configuración)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Aplicaciones](#aplicaciones)
6. [Configuración de Base de Datos](#configuración-de-base-de-datos)
7. [Uso de la Interfaz de Administración](#uso-de-la-interfaz-de-administración)
8. [Funcionalidades Principales](#funcionalidades-principales)
9. [Mejores Prácticas](#mejores-prácticas)
10. [Problemas Comunes](#problemas-comunes)
11. [Seguridad](#seguridad)
12. [Despliegue](#despliegue)

---

## Introducción

Este es un proyecto de **Ecommerce completo** desarrollado con **Django 5.0+** siguiendo las mejores prácticas de desarrollo web. El proyecto está completamente documentado en español y utiliza una arquitectura moderna basada en aplicaciones reutilizables.

### Características principales:

- ✅ Gestión de productos con categorías
- ✅ Autenticación y perfiles de usuario
- ✅ Carrito de compras persistente
- ✅ Sistema de pedidos completo
- ✅ Interfaz de administración personalizada
- ✅ Manejo de inventario
- ✅ Múltiples métodos de pago
- ✅ Historial de cambios de pedidos
- ✅ Facturación
- ✅ Totalmente documentado en español

---

## Requisitos del Sistema

### Software Requerido:

- **Python 3.9+** (recomendado 3.11+)
- **pip** (gestor de paquetes Python)
- **Git** (opcional, para control de versiones)
- **SQLite3** (incluido con Python, para desarrollo)

### Dependencias del Proyecto:

```
Django==5.2.17
Pillow==10.0.0  # Para manejo de imágenes
python-decouple==3.8  # Para variables de entorno
```

---

## Instalación y Configuración

### 1. Crear y activar el entorno virtual

```bash
# En Windows
python -m venv env
env\\Scripts\\activate

# En Linux/macOS
python3 -m venv env
source env/bin/activate
```

### 2. Instalar dependencias

```bash
pip install Django==5.2.17 Pillow==10.0.0
```

Opcionalmente, crear un archivo `requirements.txt`:

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

### 3. Aplicar migraciones

Las migraciones crean las tablas en la base de datos:

```bash
cd proyecto_ecommerce
python manage.py migrate
```

### 4. Crear superusuario (Admin)

```bash
python manage.py createsuperuser
```

Responde las preguntas:

- **Username**: tu_usuario
- **Email**: tu_email@ejemplo.com
- **Password**: tu_contraseña (mínimo 8 caracteres)

### 5. Ejecutar el servidor

```bash
python manage.py runserver
```

Accede a:

- **Sitio web**: http://localhost:8000/
- **Administrador**: http://localhost:8000/admin/

---

## Estructura del Proyecto

```
proyecto_ecommerce/
├── manage.py                          # Script de gestión de Django
├── config/                            # Configuración del proyecto
│   ├── __init__.py
│   ├── settings.py                   # Configuración principal
│   ├── urls.py                       # URLs principales
│   └── wsgi.py                       # Configuración WSGI
├── apps/                             # Aplicaciones del proyecto
│   ├── productos/                    # Gestión de productos
│   │   ├── models.py                # Modelos
│   │   ├── views.py                 # Vistas
│   │   ├── forms.py                 # Formularios
│   │   ├── urls.py                  # URLs
│   │   ├── admin.py                 # Admin personalizado
│   │   └── apps.py
│   │
│   ├── usuarios/                     # Gestión de usuarios
│   │   ├── models.py                # Perfil y Direcciones
│   │   ├── views.py                 # Vistas de auth
│   │   ├── forms.py                 # Formularios
│   │   ├── urls.py                  # URLs
│   │   └── admin.py
│   │
│   ├── carrito/                      # Carrito de compras
│   │   ├── models.py                # Carrito e Items
│   │   ├── views.py                 # Vistas del carrito
│   │   ├── forms.py                 # Formularios
│   │   ├── urls.py                  # URLs
│   │   └── admin.py
│   │
│   └── pedidos/                      # Gestión de pedidos
│       ├── models.py                # Pedidos e Items
│       ├── views.py                 # Vistas de pedidos
│       ├── forms.py                 # Formularios
│       ├── urls.py                  # URLs
│       └── admin.py
│
├── templates/                        # Plantillas HTML
├── static/                           # Archivos estáticos
│   ├── css/
│   └── js/
├── media/                            # Archivos subidos por usuarios
├── db.sqlite3                        # Base de datos (desarrollo)
└── logs/                             # Archivos de log

```

---

## Aplicaciones

### 1. **Productos** (`apps/productos`)

Gestiona el catálogo de productos del ecommerce.

#### Modelos:

- **Categoria**: Categorías de productos
  - `nombre`: Nombre único
  - `descripcion`: Descripción de la categoría
  - `imagen`: Imagen representativa
  - `slug`: URL amigable
  - `activa`: Activa/Inactiva

- **Producto**: Productos del ecommerce
  - `nombre`, `descripcion`, `categoria`
  - `precio`, `precio_descuento`
  - `stock`: Inventario disponible
  - `imagen`: Imagen principal
  - `slug`: URL amigable
  - `activo`, `destacado`: Estado del producto

- **Imagen**: Galería de imágenes por producto
  - `producto`: Relación con el producto
  - `imagen`: Archivo de imagen
  - `orden`: Orden de visualización

#### Métodos útiles en el modelo Producto:

```python
producto = Producto.objects.first()

# Propiedades
producto.precio_final           # Precio con descuento
producto.tiene_descuento        # ¿Tiene descuento?
producto.porcentaje_descuento   # % de descuento
producto.en_stock()             # ¿Está en stock?

# Métodos
producto.reducir_stock(5)       # Reduce stock
producto.aumentar_stock(3)      # Aumenta stock
```

#### URLs principales:

```
/productos/                     # Listar productos
/productos/<slug>/              # Detalles del producto
/productos/categorias/          # Listar categorías
/productos/destacados/          # Productos destacados
```

---

### 2. **Usuarios** (`apps/usuarios`)

Gestiona la autenticación y perfiles de usuarios.

#### Modelos:

- **Perfil**: Información adicional del usuario
  - `usuario`: Relación con Usuario de Django
  - `telefono`, `direccion`, `ciudad`, `estado`, `codigo_postal`, `pais`
  - `imagen_perfil`: Foto de perfil
  - `bio`: Biografía
  - `newsletter`: Suscripción a newsletter

- **Direccion**: Múltiples direcciones por usuario
  - `usuario`, `tipo` (hogar, trabajo, otra)
  - `nombre`: Nombre descriptivo
  - `direccion`, `ciudad`, `estado`, `codigo_postal`, `pais`
  - `predeterminada`: Dirección por defecto
  - `activa`: Activa/Inactiva

#### Métodos útiles:

```python
perfil = usuario.perfil

# Métodos
perfil.nombre_completo()              # Retorna nombre completo
perfil.obtener_direccion_completa()   # Dirección formateada

# Direcciones
direcciones = usuario.direcciones.filter(activa=True)
```

#### URLs principales:

```
/usuarios/registrarse/          # Registro de nuevos usuarios
/usuarios/login/                # Login
/usuarios/logout/               # Logout
/usuarios/perfil/               # Ver/editar perfil
/usuarios/direcciones/          # Listar direcciones
/usuarios/direcciones/crear/    # Crear nueva dirección
/usuarios/direcciones/<id>/editar/      # Editar dirección
/usuarios/direcciones/<id>/eliminar/    # Eliminar dirección
```

---

### 3. **Carrito** (`apps/carrito`)

Gestiona el carrito de compras persistente.

#### Modelos:

- **Carrito**: Carrito de un usuario
  - `usuario`: Relación uno a uno con Usuario
  - Propiedades: `cantidad_items`, `total`, `total_con_impuesto`
  - Método: `limpiar()` para vaciar el carrito

- **ItemCarrito**: Items en el carrito
  - `carrito`, `producto`
  - `cantidad`: Cantidad del producto
  - `precio_unitario`: Precio al momento de agregar
  - Propiedad: `subtotal`
  - Métodos: `aumentar_cantidad()`, `reducir_cantidad()`

#### Métodos útiles:

```python
carrito = usuario.carrito

# Propiedades
carrito.cantidad_items         # Total de items
carrito.total                  # Total sin impuesto
carrito.total_con_impuesto     # Total + IVA (16%)

# Operaciones
carrito.limpiar()              # Vaciar carrito
```

#### URLs principales:

```
/carrito/                       # Ver carrito
/carrito/agregar/<id>/          # Agregar al carrito
/carrito/actualizar/            # Actualizar cantidades
/carrito/eliminar/<item_id>/    # Eliminar item
/carrito/limpiar/               # Vaciar carrito
/carrito/contador/              # AJAX para contador
```

---

### 4. **Pedidos** (`apps/pedidos`)

Gestiona los pedidos de los clientes.

#### Modelos:

- **Pedido**: Pedido del cliente
  - `numero_pedido`: Único, autogenerado
  - `usuario`, `estado`, `direccion_envio`
  - `metodo_pago`: Tarjeta, PayPal, Transferencia, Efectivo
  - `subtotal`, `impuesto`, `costo_envio`, `total`
  - `pagado`, `fecha_pago`
  - Estados: pendiente, confirmado, procesando, enviado, entregado, cancelado, retornado
  - Métodos: `puede_cancelarse()`, `puede_retornarse()`, `marcar_como_pagado()`

- **ItemPedido**: Items en el pedido
  - `pedido`, `producto`
  - `cantidad`, `precio_unitario`
  - Propiedad: `subtotal`

- **HistorialPedido**: Registro de cambios del pedido
  - `pedido`, `estado_anterior`, `estado_nuevo`
  - `notas`, `fecha`

- **Factura**: Información de facturación
  - `pedido`, `numero_factura`
  - `rfc`, `razon_social`

#### Métodos útiles:

```python
pedido = Pedido.objects.first()

# Estados
pedido.puede_cancelarse()      # ¿Se puede cancelar?
pedido.puede_retornarse()      # ¿Se puede retornar?

# Operaciones
pedido.marcar_como_pagado()    # Marcar como pagado
pedido.save()                  # Recalcula totales
```

#### URLs principales:

```
/pedidos/crear/                # Crear pedido desde carrito
/pedidos/                       # Listar pedidos del usuario
/pedidos/<numero_pedido>/       # Detalles del pedido
/pedidos/<numero_pedido>/cancelar/  # Cancelar pedido
```

---

## Configuración de Base de Datos

### Desarrollo (SQLite)

Por defecto, el proyecto usa SQLite (no requiere instalación adicional):

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Producción (PostgreSQL)

Para producción, se recomienda PostgreSQL:

```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nombre_bd',
        'USER': 'usuario',
        'PASSWORD': 'contraseña',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Operaciones comunes:

```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Ver estado de migraciones
python manage.py showmigrations

# Crear copia de seguridad
python manage.py dumpdata > backup.json

# Restaurar copia de seguridad
python manage.py loaddata backup.json
```

---

## Uso de la Interfaz de Administración

La interfaz de administración de Django está disponible en `/admin/`.

### Acceso:

1. Inicia el servidor: `python manage.py runserver`
2. Abre http://localhost:8000/admin/
3. Inicia sesión con el superusuario creado

### Operaciones comunes:

#### Categorías:

- Crear categorías para agrupar productos
- El slug se genera automáticamente
- Activar/desactivar categorías

#### Productos:

- Crear productos con toda la información
- Agregar imágenes a la galería
- Establecer precios y descuentos
- Marcar como destacados
- Controlar el stock

#### Usuarios:

- Ver perfiles de usuarios
- Gestionar direcciones de envío
- Ver historial de compras

#### Pedidos:

- Ver todos los pedidos
- Cambiar estado del pedido
- Acceder a historial de cambios
- Marcar como pagados
- Agregar notas

---

## Funcionalidades Principales

### 1. Gestión de Productos

Los administradores pueden:

- Crear/editar/eliminar productos
- Organizar en categorías
- Establecer precios y descuentos
- Controlar inventario
- Agregar múltiples imágenes

### 2. Autenticación y Perfiles

Los usuarios pueden:

- Registrarse con email y contraseña
- Editar su perfil
- Guardar múltiples direcciones
- Actualizar información personal

### 3. Carrito de Compras

Los usuarios pueden:

- Agregar/remover productos
- Actualizar cantidades
- Ver total con impuesto
- Ver el carrito en cualquier momento (persistente)

### 4. Creación de Pedidos

Los usuarios pueden:

- Crear pedidos desde el carrito
- Seleccionar dirección de envío
- Elegir método de pago
- Agregar notas especiales
- Ver historial de pedidos
- Cancelar pedidos si no han sido confirmados

### 5. Panel de Administración

Los administradores pueden:

- Gestionar todo desde una interfaz amigable
- Realizar acciones en lote (cambiar estado, marcar como pagado)
- Ver reportes de ventas
- Gestionar inventario

---

## Mejores Prácticas

### 1. Modelos

```python
# ✅ Correcto: Usar related_name
usuario = models.ForeignKey(User, related_name='pedidos')

# ✅ Usar verbose_name para mejor legibilidad
nombre = models.CharField(max_length=100, verbose_name='Nombre del Producto')

# ✅ Usar Meta.ordering para orden por defecto
class Meta:
    ordering = ['-created_at']
```

### 2. Vistas

```python
# ✅ Usar login_required para vistas que requieren autenticación
@login_required(login_url='usuarios:login')
def mi_vista(request):
    pass

# ✅ Usar get_object_or_404 para seguridad
producto = get_object_or_404(Producto, slug=slug)

# ✅ Usar select_related/prefetch_related para optimizar
productos = Producto.objects.select_related('categoria').all()
```

### 3. Formularios

```python
# ✅ Usar widgets personalizado para HTML mejor
email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

# ✅ Implementar validación personalizada
def clean(self):
    cleaned_data = super().clean()
    if condicion_invalida:
        raise forms.ValidationError('Mensaje de error')
```

### 4. Admin

```python
# ✅ Personalizar la visualización
list_display = ['nombre', 'precio', 'stock', 'activo']
list_filter = ['activo', 'categoria', 'created_at']
search_fields = ['nombre', 'descripcion']
readonly_fields = ['created_at', 'updated_at']
```

### 5. URLs

```python
# ✅ Usar namespaces para evitar conflictos
app_name = 'productos'

urlpatterns = [
    path('', views.listar_productos, name='listar'),
]

# Uso: {% url 'productos:listar' %}
```

---

## Problemas Comunes

### Problema: "ModuleNotFoundError: No module named 'django'"

**Solución:**

```bash
# Asegurate de que el entorno virtual esté activado
pip install Django==5.2.17
```

### Problema: "No such table" en la base de datos

**Solución:**

```bash
python manage.py migrate
```

### Problema: Imágenes no se muestran

**Verificar:**

1. `DEBUG = True` en settings.py (para desarrollo)
2. Archivos estáticos configurados correctamente
3. Las imágenes están en la carpeta `media/`

**Comando útil:**

```bash
python manage.py collectstatic
```

### Problema: "PermissionError" al guardar archivos

**Solución:**

- Asegurar permisos en carpeta `media/`
- En Windows: Ejecutar como administrador
- En Linux: `chmod 755 media/`

---

## Seguridad

### Para Desarrollo (settings.py actual):

```python
DEBUG = True  # Activo para desarrollo
SECRET_KEY = 'django-insecure-cambiar-esta-clave'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

### Para Producción:

```python
# Generar nueva SECRET_KEY segura
import secrets
SECRET_KEY = secrets.token_urlsafe(50)

# Configurar seguridad
DEBUG = False
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Buenas prácticas:

1. **Nunca compartir SECRET_KEY**
2. **Usar variables de entorno para datos sensibles**
3. **Actualizar Django regularmente**
4. **Usar HTTPS en producción**
5. **Validar siempre entrada del usuario**
6. **Usar CSRF tokens en formularios**

---

## Despliegue

### Opciones de hosting:

- **Heroku**: Fácil de usar, incluye base de datos
- **PythonAnywhere**: Python hosting simplificado
- **DigitalOcean**: Máquinas virtuales (VPS)
- **AWS Elastic Beanstalk**: Escalable, profesional
- **Render**: Alternativa moderna a Heroku

### Pasos generales de despliegue:

1. **Preparar el proyecto**

   ```bash
   python manage.py collectstatic
   pip freeze > requirements.txt
   ```

2. **Configurar production settings**
   - DEBUG = False
   - SECRET_KEY segura
   - ALLOWED_HOSTS correctos
   - Base de datos productiva

3. **Subir a servidor**
   - Usando Git
   - SFTP
   - SSH

4. **Configurar WSGI**
   - Con Gunicorn
   - Con uWSGI

5. **Reverse proxy (Nginx)**
   - Servir archivos estáticos
   - SSL/TLS

---

## Conclusión

Este ecommerce Django está completamente funcional y listo para expandirse con nuevas características. La arquitectura modular permite agregar fácilmente:

- Integración de pasarelas de pago (Stripe, PayPal)
- Búsqueda avanzada con Elasticsearch
- API REST con Django REST Framework
- Caché con Redis
- Colas de tareas con Celery
- Emails automáticos
- Análisis y reportes

**¡Feliz desarrollo!** 🚀

---

Para más información sobre Django:

- Documentación oficial: https://docs.djangoproject.com/es/
- Django REST Framework: https://www.django-rest-framework.org/
- Comunidad: https://www.djangoproject.com/weblog/
