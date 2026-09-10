
# 🛒 Ecommerce Django — Guía de Inicio Rápido y Estado del Proyecto

Sistema de comercio electrónico desarrollado en Django con monitoreo y auditoría automática de eventos de usuarios (accesos, búsquedas, visualización de productos y registro de acciones).

---

## 📌 Estado Actual del Proyecto (Status de Desarrollo)

El proyecto se encuentra en etapa **Funcional / Beta Avanzada**, con las siguientes características e implementaciones estabilizadas:

- **Autenticación y Usuarios (`apps/usuarios`):** Registro, inicio de sesión, cierre de sesión y flujo de formularios aislados del middleware de rastreo para prevenir fallos durante el registro de nuevos clientes.
- **Catálogo de Productos y Categorías (`apps/productos`):**
  - Listado con soporte para paginación (12 elementos por página), filtrado por categoría y búsqueda textual.
  - Ordenamiento dinámico y seguro mediante parámetros sanitizados (`nombre`, `precio`, `created_at`).
  - Mapeo de URLs corregido: soporte para slugs dinámicos de productos evitando conflictos con rutas estáticas (`/categorias/`, `/destacados/`).
  - Compatibilidad con Vistas Basadas en Funciones (FBV) y Vistas Basadas en Clases (CBV).
- **Sistema de Eventos y Auditoría (`apps/eventos`):**
  - Middleware automatizado (`RastreadorEventosMiddleware`) que captura la navegación y las búsquedas en el sitio (`GET`), ignorando rutas estáticas y de autenticación para optimizar el rendimiento.
  - Registro a prueba de fallos (encapsulado en bloques `try-except`) tanto en las vistas principales como en el middleware, garantizando alta disponibilidad de la tienda aunque la tabla de eventos no esté accesible.

---

## 🚀 Cómo Ejecutar el Proyecto

### 1. Clonar el repositorio y preparar el entorno virtual

```bash
# Entrar a la carpeta del proyecto
cd proyecto_ecommerce

# Crear y activar un entorno virtual (recomendado)
python -m venv venv

# En Linux/macOS:
source venv/bin/activate

# En Windows (PowerShell):
.\venv\Scripts\Activate.ps1

```

### 2. Instalar las dependencias

Si el proyecto cuenta con un archivo `requirements.txt`:

```bash
pip install -r requirements.txt

```

Si estás instalando manualmente las dependencias principales:

```bash
pip install Django==5.0 Pillow

```

### 3. Aplicar las migraciones a la base de datos

Para generar y aplicar la estructura de tablas (Productos, Categorías, Usuarios y Eventos):

```bash
python manage.py makemigrations
python manage.py migrate

```

### 4. Crear un superusuario (Administrador)

Crea una cuenta de administrador para gestionar la aplicación desde el panel de control de Django:

```bash
python manage.py createsuperuser

```

*(Ingresa los datos solicitados: usuario, correo electrónico y contraseña)*

### 5. Iniciar el servidor de desarrollo

Para ejecutar la aplicación en entorno local:

```bash
python manage.py runserver

```

### 6. Acceder a la aplicación

* **Tienda (Página Principal):** [http://localhost:8000/](http://localhost:8000/)
* **Panel de Administración:** [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🔧 Comandos Frecuentes

```bash
# Detectar cambios en los modelos y aplicarlos a la base de datos
python manage.py makemigrations
python manage.py migrate

# Consultar el estado de las migraciones
python manage.py showmigrations

# Abrir la consola interactiva de Django
python manage.py shell

# Crear un nuevo módulo o app
python manage.py startapp nombre_de_la_app

# Cargar datos iniciales o de prueba desde un archivo JSON
python manage.py loaddata datos.json

# Exportar el contenido actual de la base de datos a JSON
python manage.py dumpdata > datos.json

```

---

## 📚 Arquitectura y Estructura del Proyecto

```text
proyecto_ecommerce/
├── apps/
│   ├── eventos/     # Middleware y logs de auditoría/rastreo de acciones
│   ├── productos/   # Catálogo, categorías, búsqueda y detalle de productos
│   └── usuarios/    # Gestión de perfiles, registro y autenticación
├── manage.py
└── DOCUMENTACION.md # Guía arquitectónica detallada

```

```

```
