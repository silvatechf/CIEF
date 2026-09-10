# Sistema de Eventos - Documentación

## Descripción General

Se ha implementado un sistema completo de rastreo de eventos en el proyecto de e-commerce. Este sistema registra automáticamente todas las acciones de los usuarios en la plataforma, permitiendo:

- Auditoría de acciones del usuario
- Análisis de comportamiento del cliente
- Historial de actividades
- Estadísticas de uso

## Características Implementadas

### 1. **Modelos de Datos**

#### `TipoEvento`

Define los tipos de eventos que se pueden registrar:

- **LOGIN**: Login de usuario
- **LOGOUT**: Logout de usuario
- **REGISTRO**: Nuevo registro de usuario
- **VER_PRODUCTO**: Visualización de producto
- **AGREGAR_CARRITO**: Agregar producto al carrito
- **ELIMINAR_CARRITO**: Eliminar producto del carrito
- **CREAR_PEDIDO**: Crear pedido
- **COMPLETAR_PEDIDO**: Completar pedido
- **CANCELAR_PEDIDO**: Cancelar pedido
- **ACTUALIZAR_PERFIL**: Actualizar perfil de usuario
- **CAMBIAR_CONTRASEÑA**: Cambiar contraseña
- **RESEÑA_PRODUCTO**: Crear reseña de producto
- **BUSCAR**: Búsqueda en la tienda
- **FILTRAR**: Aplicar filtros de búsqueda
- **OTRO**: Otro evento

#### `Evento`

Registra cada evento con los siguientes campos:

- `usuario`: Usuario que realiza la acción (puede ser nulo para anónimos)
- `tipo`: Tipo de evento (de las opciones anteriores)
- `descripcion`: Descripción detallada del evento
- `url`: URL de la página donde ocurrió el evento
- `ip_address`: Dirección IP del cliente
- `user_agent`: User Agent del navegador
- `datos_adicionales`: Datos JSON adicionales personalizables
- `fecha_creacion`: Fecha y hora del evento

### 2. **Middleware de Rastreo**

Se implementó el middleware `RastreadorEventosMiddleware` que:

- Registra automáticamente todas las visitas a páginas
- Detecta búsquedas en la tienda
- Ignora rutas estáticas, media y admin
- Captura información técnica del cliente

**Ubicación**: `apps/eventos/middleware.py`

### 3. **Utilidades**

Funciones auxiliares en `apps/eventos/utils.py`:

- `registrar_evento()`: Función principal para registrar eventos
- `obtener_ip_cliente()`: Extrae la IP del cliente
- `obtener_user_agent()`: Extrae el User Agent

### 4. **Vistas Implementadas**

#### `listar_mis_eventos()` - Vista de Usuario

- URL: `/eventos/mis-eventos/`
- Muestra los últimos 100 eventos del usuario autenticado
- Incluye estadísticas:
  - Total de eventos
  - Eventos de hoy
  - Eventos de los últimos 7 días
  - Distribución por tipo de evento
- Requiere login

#### `EventoListView` - Vista de Administrador

- URL: `/eventos/`
- Muestra todos los eventos del sistema (solo para superusuarios)
- Incluye filtros:
  - Por tipo de evento
  - Por usuario
  - Por rango de fechas
- Paginación de 50 eventos por página
- Requiere login de superusuario

### 5. **Interfaz de Admin**

Paneles configurados en Django Admin (`/admin/`):

- **Eventos**: Visualización de solo lectura con filtros y búsqueda
- **Tipos de Eventos**: Gestión de tipos de eventos

### 6. **Eventos Registrados por Módulo**

#### Módulo de Usuarios (`apps/usuarios/`)

- **REGISTRO**: Al crear una nueva cuenta
- **LOGIN**: Al iniciar sesión
- **LOGOUT**: Al cerrar sesión
- **ACTUALIZAR_PERFIL**: Al actualizar datos de perfil

#### Módulo de Productos (`apps/productos/`)

- **BUSCAR**: Al realizar una búsqueda
- **VER_PRODUCTO**: Al ver detalles de un producto

#### Módulo de Carrito (`apps/carrito/`)

- **AGREGAR_CARRITO**: Al agregar un producto
- **ELIMINAR_CARRITO**: Al eliminar un producto

#### Módulo de Pedidos (`apps/pedidos/`)

- **CREAR_PEDIDO**: Al crear un nuevo pedido
- **CANCELAR_PEDIDO**: Al cancelar un pedido

### 7. **Información Capturada**

Cada evento captura:

- **Usuario**: Quién realizó la acción
- **Tipo**: Qué tipo de acción fue
- **Descripción**: Texto descriptivo
- **URL**: Dónde ocurrió
- **IP**: Desde dónde se conectó
- **User Agent**: Qué navegador/dispositivo usó
- **Datos Adicionales**: Información específica del evento (en JSON)
- **Timestamp**: Cuándo ocurrió

Ejemplo de datos adicionales para un evento de búsqueda:

```json
{
  "termino_busqueda": "laptop"
}
```

Ejemplo para agregar al carrito:

```json
{
  "producto_id": 5,
  "producto_nombre": "Laptop Dell",
  "cantidad": 2,
  "precio": 1200.0
}
```

## Configuración

### Settings.py

La aplicación ya está configurada en `config/settings.py`:

```python
INSTALLED_APPS = [
    ...
    "apps.eventos",
]

MIDDLEWARE = [
    ...
    "apps.eventos.middleware.RastreadorEventosMiddleware",
]
```

### URLs

Las rutas ya están incluidas en `config/urls.py`:

```python
path("eventos/", include("apps.eventos.urls")),
```

## Base de Datos

Las migraciones ya han sido ejecutadas:

```bash
python manage.py makemigrations eventos
python manage.py migrate eventos
```

## Uso

### Para ver tus eventos como usuario:

1. Inicia sesión en la plataforma
2. Accede a `/eventos/mis-eventos/`
3. Verás un dashboard con tus actividades y estadísticas

### Para administradores (ver todos los eventos):

1. Accede al panel admin (`/admin/`)
2. Navega a "Eventos"
3. Usa los filtros para buscar eventos específicos
4. O visita `/eventos/` para una vista más completa con búsqueda y filtros avanzados

### Para registrar eventos personalizados:

```python
from apps.eventos.utils import registrar_evento, obtener_ip_cliente, obtener_user_agent

registrar_evento(
    usuario=request.user,
    tipo="CREAR_PEDIDO",
    descripcion="Pedido creado exitosamente",
    url=request.build_absolute_uri(),
    ip_address=obtener_ip_cliente(request),
    user_agent=obtener_user_agent(request),
    datos_adicionales={"monto": 150.00}
)
```

## Consideraciones de Rendimiento

### Índices

El modelo Evento tiene índices en:

- `-fecha_creacion`: Para acceso rápido a eventos recientes
- `usuario, -fecha_creacion`: Para filtrar eventos por usuario
- `tipo, -fecha_creacion`: Para filtrar eventos por tipo

### Paginación

- Vista de usuario: Últimos 100 eventos
- Vista de admin: 50 eventos por página

### Rotación de Datos

Para proyectos en producción, se recomienda implementar una política de eliminación de eventos antiguos:

```python
from django.utils import timezone
from datetime import timedelta
from apps.eventos.models import Evento

# Eliminar eventos más antiguos de 90 días
hace_90_dias = timezone.now() - timedelta(days=90)
Evento.objects.filter(fecha_creacion__lt=hace_90_dias).delete()
```

## Rutas Ignoradas por el Middleware

El middleware NO registra accesos a:

- `/static/` - Archivos estáticos
- `/media/` - Archivos multimedia
- `/admin/` - Panel administrativo

## Seguridad

- Los eventos solo pueden ser agregados por el middleware o funciones del sistema
- Las direcciones IP se registran con seguridad
- El User Agent se almacena para auditoría
- Solo se registra información no sensible

## Extensibilidad

### Para agregar nuevos tipos de eventos:

1. Edita `apps/eventos/models.py`
2. Agrega la opción a `TipoEvento.TIPOS_EVENTO`
3. Ejecuta migraciones si es necesario

### Para capturar nuevos eventos:

1. Importa `registrar_evento` en tu vista
2. Llama la función con los parámetros apropiados
3. Los eventos aparecerán automáticamente en el dashboard

## Archivo de Migraciones

Se generó automáticamente:

- `apps/eventos/migrations/0001_initial.py`

Esta migración crea las tablas `eventos_tipoevent` y `eventos_evento`.

## Próximas Mejoras Sugeridas

- [ ] Exportar eventos a CSV/Excel
- [ ] Gráficos de actividad en dashboard
- [ ] Alertas para eventos específicos
- [ ] Análisis avanzado de comportamiento
- [ ] API REST para acceso a eventos
- [ ] Webhook para integración con terceros
- [ ] Compresión de datos antiguos
