# Proyecto Base Django — API de Productos

## Estado del proyecto

**Estado actual:** EN DESARROLLO — PAUSADO EN UN PUNTO ESTABLE

Este documento registra el estado técnico alcanzado hasta el momento, las decisiones tomadas y la hoja de ruta prevista para continuar el proyecto.

La prioridad del proyecto es construir una base Django + Django REST Framework con criterios profesionales: estructura clara, validación, seguridad, pruebas y evolución incremental.

---

## 1. Objetivo del proyecto

El proyecto parte de una base Django existente y se está ampliando de forma incremental con una API REST para gestionar productos.

La intención no es construir únicamente un CRUD de demostración, sino utilizar el proyecto como base de aprendizaje y práctica para desarrollar una API con criterios de calidad aplicables a un proyecto real.

### Principios de trabajo

- Cambios pequeños y controlados.
- Una etapa debe quedar verificada antes de avanzar.
- La máquina local es la fuente de verdad para las pruebas.
- No realizar refactorizaciones innecesarias.
- Proteger el comportamiento existente.
- Cada cambio debe tener un motivo claro.
- Cada etapa debe poder verificarse mediante comandos concretos.
- No avanzar por suposiciones: primero evidencia, después decisión.

---

# 2. Base existente protegida

El proyecto ya disponía de una aplicación `apps/tareas`.

Esta aplicación forma parte de la base existente y **no debe modificarse innecesariamente** durante la construcción de `apps/productos`.

La API existente de tareas utiliza Django REST Framework y sirve como referencia arquitectónica para la nueva API.

---

# 3. Arquitectura actual

La estructura relevante actualmente incluye:

```text
proyectoBaseDjango/
│
├── apps/
│   ├── core/
│   ├── tareas/
│   └── productos/
│
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   └── urls.py
│
├── templates/
├── frontend/
├── static/
├── manage.py
├── .env
├── .gitignore
└── .venv/
```

La configuración utiliza separación entre settings base, desarrollo y producción.

---

# 4. Entorno de desarrollo

Se creó y configuró un entorno virtual:

```text
.venv/
```

Las dependencias necesarias fueron instaladas dentro del entorno virtual.

También se configuró un archivo `.env` para las variables básicas de desarrollo:

```env
DJANGO_SECRET_KEY=django-dev-secret-change-me
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

Se creó además el directorio:

```text
static/
```

para resolver la configuración de archivos estáticos durante el desarrollo.

### Verificación

El proyecto fue comprobado mediante:

```powershell
python manage.py check
```

Resultado:

```text
System check identified no issues (0 silenced).
```

---

# 5. Nueva aplicación `productos`

Se creó:

```text
apps/productos/
```

y se registró correctamente como:

```python
"apps.productos"
```

en las aplicaciones locales de Django.

La configuración de la aplicación utiliza:

```python
class ProductosConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.productos"
```

La aplicación quedó integrada sin errores en Django.

---

# 6. Modelo `Producto`

Se creó el modelo:

```python
class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )
    stock = models.PositiveIntegerField(default=0)
    categoria = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
```

## Decisiones principales

### `nombre`

Nombre del producto.

### `descripcion`

Descripción opcional del producto.

### `precio`

Se utiliza `DecimalField` porque representa valores monetarios y evita utilizar `float` para dinero.

### `stock`

Se utiliza:

```python
PositiveIntegerField
```

para impedir cantidades negativas.

### `categoria`

Actualmente se mantiene como texto simple.

La normalización de categorías podrá evaluarse más adelante si el dominio del proyecto realmente lo necesita.

### `activo`

Permite desactivar un producto sin eliminarlo físicamente.

### Fechas

Se registran automáticamente:

```text
creado_en
actualizado_en
```

---

# 7. Migraciones

La migración inicial de productos fue creada y aplicada correctamente.

Verificación realizada:

```powershell
python manage.py showmigrations productos
```

La migración:

```text
0001_initial
```

aparece aplicada:

```text
[X] 0001_initial
```

---

# 8. Serializer

Se creó:

```text
apps/productos/serializers.py
```

con `ProductoSerializer`.

Los campos expuestos actualmente son:

```text
id
nombre
descripcion
precio
stock
categoria
activo
creado_en
actualizado_en
```

Los siguientes campos son de solo lectura:

```text
id
creado_en
actualizado_en
```

Esto evita que el cliente de la API pueda modificar directamente esos valores.

---

# 9. ViewSet

Se creó:

```text
ProductoViewSet
```

basado en:

```python
viewsets.ModelViewSet
```

Esto proporciona las operaciones REST principales:

```text
GET
POST
PUT
PATCH
DELETE
```

La consulta base utiliza:

```python
Producto.objects.all()
```

---

# 10. Filtros, búsqueda y ordenación

El `ProductoViewSet` incorpora:

## Filtros

```python
filterset_fields = [
    "categoria",
    "activo",
]
```

Ejemplo:

```text
GET /api/productos/?categoria=Tecnologia
```

La prueba real confirmó que el filtro por categoría funciona.

---

## Búsqueda

```python
search_fields = [
    "nombre",
    "descripcion",
]
```

Ejemplo:

```text
GET /api/productos/?search=Laptop
```

La prueba real encontró los productos correspondientes.

---

## Ordenación

```python
ordering_fields = [
    "nombre",
    "precio",
    "stock",
    "creado_en",
]
```

Ordenación predeterminada:

```python
ordering = [
    "-creado_en",
]
```

Ejemplos:

```text
GET /api/productos/?ordering=precio
```

```text
GET /api/productos/?ordering=-stock
```

Las solicitudes fueron aceptadas correctamente.

---

# 11. Paginación

Se configuró Django REST Framework globalmente:

```python
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}
```

La API ahora devuelve respuestas paginadas.

Ejemplo de estructura:

```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": []
}
```

Esto es importante porque el frontend deberá consumir posteriormente `results` en lugar de asumir que la respuesta raíz es directamente una lista.

**El frontend todavía no se ha modificado para este cambio.**

---

# 12. CRUD verificado

Se verificó mediante HTTP real que la API permite crear y consultar productos.

Se comprobó:

```text
GET /api/productos/
```

con respuesta HTTP:

```text
200
```

También se realizó un `POST` real y posteriormente:

```text
GET /api/productos/1/
```

con respuesta HTTP:

```text
200
```

La respuesta contiene correctamente:

```text
id
nombre
descripcion
precio
stock
categoria
activo
creado_en
actualizado_en
```

Durante las pruebas se creó accidentalmente dos veces el mismo producto. Esto fue consecuencia de ejecutar el `POST` dos veces durante la validación y **no representa un problema de implementación del CRUD**.

---

# 13. Validación de datos — ÚLTIMA ETAPA COMPLETADA

Se realizó una prueba específica para comprobar que el stock negativo no puede entrar en el sistema.

Se intentó crear:

```json
{
    "nombre": "Producto Invalido",
    "descripcion": "Prueba de validacion",
    "precio": "100.00",
    "stock": -5,
    "categoria": "Prueba",
    "activo": true
}
```

La API respondió:

```text
400
```

con:

```json
{
    "stock": [
        "Asegúrese de que este valor es mayor o igual a 0."
    ]
}
```

## Conclusión

La validación de dominio funciona correctamente:

```text
POST
  ↓
Serializer / Model validation
  ↓
PositiveIntegerField
  ↓
stock = -5 rechazado
  ↓
HTTP 400
```

No fue necesario añadir código adicional para impedir el valor negativo.

**Este es el punto exacto donde el proyecto queda pausado.**

---

# 14. Situación conocida: Browsable API

Durante las pruebas se detectó un problema en la representación HTML del Browsable API relacionado con:

```text
django_filters/rest_framework/form.html
```

El error observado fue:

```text
TemplateDoesNotExist:
django_filters/rest_framework/form.html
```

La API JSON continúa funcionando correctamente.

Por este motivo, este asunto queda registrado como **pendiente técnico de desarrollo**, pero no se mezcló con la validación del modelo ni se realizaron cambios especulativos.

Debe resolverse posteriormente de forma aislada y verificable.

---

# 15. Estado actual

## Completado

- [x] Entorno virtual `.venv`
- [x] Dependencias instaladas
- [x] Variables `.env`
- [x] Configuración básica de desarrollo
- [x] Directorio `static/`
- [x] `python manage.py check`
- [x] Aplicación `apps/productos`
- [x] Modelo `Producto`
- [x] Migración `0001_initial`
- [x] Serializer
- [x] ViewSet
- [x] Router
- [x] Endpoint `/api/productos/`
- [x] CRUD básico
- [x] Paginación
- [x] Filtros
- [x] Búsqueda
- [x] Ordenación
- [x] Validación de stock negativo
- [x] Verificación mediante HTTP real

## Pendiente

- [ ] Revisar Browsable API / django-filter
- [ ] Validaciones de negocio adicionales
- [ ] Seguridad de la API
- [ ] Autenticación/autorización
- [ ] Pruebas automatizadas
- [ ] PostgreSQL
- [ ] Docker
- [ ] CI/CD
- [ ] Preparación para producción
- [ ] Adaptación del frontend a la respuesta paginada
- [ ] Documentación de API

---

# 16. Hoja de ruta futura

La continuación prevista será incremental.

## Etapa 1 — API sólida

Profundizar en:

- validaciones de negocio;
- respuestas de error;
- filtros;
- búsqueda;
- ordenación;
- paginación;
- documentación de endpoints.

---

## Etapa 2 — Seguridad

Incorporar progresivamente:

- autenticación;
- autorización;
- permisos;
- protección de endpoints;
- configuración segura;
- CORS;
- throttling/rate limiting;
- gestión correcta de secretos;
- endurecimiento de producción.

---

## Etapa 3 — Testing

Construir pruebas automatizadas para:

- modelos;
- serializers;
- endpoints;
- validaciones;
- permisos;
- filtros;
- búsqueda;
- ordenación;
- casos de error.

La prioridad será comprobar comportamiento real y evitar regresiones.

---

## Etapa 4 — Base de datos PostgreSQL

Migrar progresivamente desde SQLite hacia PostgreSQL.

Se revisarán:

- configuración;
- variables de entorno;
- migraciones;
- índices;
- restricciones;
- rendimiento;
- comportamiento de consultas.

---

## Etapa 5 — Docker

Containerizar el proyecto.

Objetivo aproximado:

```text
Django
   +
PostgreSQL
   +
Frontend
```

con una configuración reproducible para desarrollo y posteriormente producción.

---

## Etapa 6 — CI/CD

Incorporar automatización para:

```text
Commit
  ↓
Lint / checks
  ↓
Tests
  ↓
Security checks
  ↓
Build
  ↓
Deployment
```

La implementación concreta se decidirá cuando las etapas anteriores estén estabilizadas.

---

## Etapa 7 — Producción

Finalmente se trabajará en:

- settings de producción;
- variables de entorno;
- HTTPS;
- seguridad de cookies;
- headers;
- logging;
- observabilidad;
- backups;
- despliegue;
- mantenimiento.

---

# 17. Regla de continuidad del proyecto

Antes de realizar cualquier cambio futuro se debe declarar:

### 1. Qué cambia

Archivo, componente o comportamiento concreto.

### 2. Por qué cambia

Problema o necesidad que justifica el cambio.

### 3. Qué comportamiento existente queda protegido

Especialmente:

- `apps/tareas`;
- API existente;
- `apps/productos`;
- migraciones;
- comportamiento ya verificado.

### 4. Cómo se verifica

Comandos concretos que puedan ejecutarse localmente.

### 5. Criterio de aceptación

Debe existir una condición clara para determinar:

```text
PASS
```

o

```text
FAIL
```

No se considera completada una etapa por asumir que el código "debería funcionar".

---

# 18. Punto de reanudación

Cuando se retome el proyecto, **no se debe comenzar desde cero ni rehacer las etapas ya verificadas**.

El punto de reanudación es:

```text
API Productos
    ↓
CRUD básico              ✅
Paginación               ✅
Filtros                  ✅
Búsqueda                 ✅
Ordenación               ✅
Validación stock         ✅
    ↓
[PAUSA ACTUAL]
    ↓
Siguiente decisión:
revisar Browsable API
y continuar con validaciones
```

La próxima sesión deberá partir de este estado.

---

# 19. Filosofía del proyecto

El objetivo no es acumular funcionalidades rápidamente.

El objetivo es aprender a construir software Django de forma profesional:

```text
Objetivo
   ↓
Diseño
   ↓
Implementación mínima
   ↓
Prueba local real
   ↓
Evidencia
   ↓
Aceptación
   ↓
Siguiente etapa
```

**No avanzar por cantidad de código. Avanzar por evidencia.**
