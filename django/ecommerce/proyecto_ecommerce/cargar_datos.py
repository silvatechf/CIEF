"""
Script para cargar datos de prueba en la base de datos.

Uso:
    python manage.py shell
    exec(open('cargar_datos.py').read())

O:
    python manage.py shell < cargar_datos.py
"""

from django.contrib.auth.models import User
from apps.productos.models import Categoria, Producto
from apps.usuarios.models import Perfil, Direccion

print("Cargando datos de prueba...")

# Crear categorías
print("\n📦 Creando categorías...")

categoria_electronica, _ = Categoria.objects.get_or_create(
    nombre="Electrónica", 
    defaults={"descripcion": "Productos electrónicos y accesorios", "activa": True}
)
print(f"  ✓ Categoría: {categoria_electronica.nombre}")

categoria_ropa, _ = Categoria.objects.get_or_create(
    nombre="Ropa", 
    defaults={"descripcion": "Ropa para hombre, mujer y niños", "activa": True}
)
print(f"  ✓ Categoría: {categoria_ropa.nombre}")

categoria_libros, _ = Categoria.objects.get_or_create(
    nombre="Libros", 
    defaults={"descripcion": "Libros de todos los géneros", "activa": True}
)
print(f"  ✓ Categoría: {categoria_libros.nombre}")

# Crear productos
print("\n🎁 Creando productos...")

productos_data = [
    {
        "nombre": "Laptop Dell XPS 13",
        "descripcion": "Laptop ultradelgada de alta gama con procesador Intel i7, 16GB RAM, 512GB SSD",
        "categoria": categoria_electronica,
        "precio": 1500.00,
        "precio_descuento": 1350.00,
        "stock": 10,
        "destacado": True,
    },
    {
        "nombre": "iPhone 15 Pro",
        "descripcion": "Último modelo de Apple con chip A17 Pro, cámara de 48MP, 5G",
        "categoria": categoria_electronica,
        "precio": 1200.00,
        "precio_descuento": None,
        "stock": 15,
        "destacado": True,
    },
    {
        "nombre": "Samsung Galaxy S24",
        "descripcion": "Smartphone con pantalla AMOLED, procesador Snapdragon 8 Gen 3",
        "categoria": categoria_electronica,
        "precio": 1100.00,
        "precio_descuento": 950.00,
        "stock": 20,
        "destacado": False,
    },
    {
        "nombre": "Camiseta Básica Negra",
        "descripcion": "Camiseta 100% algodón, disponible en varias tallas",
        "categoria": categoria_ropa,
        "precio": 29.99,
        "precio_descuento": 24.99,
        "stock": 50,
        "destacado": False,
    },
    {
        "nombre": "Jeans Clásicos Azul",
        "descripcion": "Jeans denim de calidad, corte clásico, disponible en todas las tallas",
        "categoria": categoria_ropa,
        "precio": 79.99,
        "precio_descuento": None,
        "stock": 30,
        "destacado": False,
    },
    {
        "nombre": "Don Quijote de la Mancha",
        "descripcion": "Novela clásica de Miguel de Cervantes, edición de bolsillo",
        "categoria": categoria_libros,
        "precio": 15.99,
        "precio_descuento": None,
        "stock": 25,
        "destacado": False,
    },
]

for prod_data in productos_data:
    producto, created = Producto.objects.get_or_create(
        nombre=prod_data["nombre"],
        defaults=prod_data
    )
    print(f"  ✓ Producto: {producto.nombre}")

# Crear usuarios de prueba
print("\n👥 Creando usuarios de prueba...")

def crear_o_actualizar_usuario(username, email, password, first_name, last_name, perfil_data):
    usuario, created = User.objects.get_or_create(
        username=username,
        defaults={
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }
    )
    if created:
        usuario.set_password(password)
        usuario.save()
    
    Perfil.objects.update_or_create(
        usuario=usuario,
        defaults=perfil_data
    )
    return usuario

usuario1 = crear_o_actualizar_usuario(
    username="juan",
    email="juan@ejemplo.com",
    password="password123",
    first_name="Juan",
    last_name="García",
    perfil_data={"telefono": "555-1234", "ciudad": "Madrid", "pais": "España"}
)
print(f"  ✓ Usuario: {usuario1.username}")

usuario2 = crear_o_actualizar_usuario(
    username="maria",
    email="maria@ejemplo.com",
    password="password123",
    first_name="María",
    last_name="López",
    perfil_data={"telefono": "555-5678", "ciudad": "Barcelona", "pais": "España"}
)
print(f"  ✓ Usuario: {usuario2.username}")

# Crear direcciones
print("\n📍 Creando direcciones...")

Direccion.objects.get_or_create(
    usuario=usuario1,
    nombre="Casa de Juan",
    defaults={
        "tipo": "hogar",
        "direccion": "Calle Principal 123",
        "ciudad": "Madrid",
        "estado": "Madrid",
        "codigo_postal": "28001",
        "pais": "España",
        "predeterminada": True,
    }
)
print(f"  ✓ Dirección cargada para {usuario1.username}")

Direccion.objects.get_or_create(
    usuario=usuario2,
    nombre="Casa de María",
    defaults={
        "tipo": "hogar",
        "direccion": "Avenida Catalunya 456",
        "ciudad": "Barcelona",
        "estado": "Barcelona",
        "codigo_postal": "08002",
        "pais": "España",
        "predeterminada": True,
    }
)
print(f"  ✓ Dirección cargada para {usuario2.username}")

print("\n✅ ¡Datos de prueba cargados exitosamente!")
print("\nCredenciales de prueba:")
print("  Usuario: juan / Contraseña: password123")
print("  Usuario: maria / Contraseña: password123")
print("\nPuedes acceder a:")
print("  http://localhost:8000/productos/")
print("  http://localhost:8000/admin/")