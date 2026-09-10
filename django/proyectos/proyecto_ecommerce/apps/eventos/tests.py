from django.test import TestCase
from django.contrib.auth.models import User
from apps.eventos.models import Evento, TipoEvento
from apps.eventos.utils import registrar_evento


class EventoModelTestCase(TestCase):
    """Tests para el modelo Evento."""
    
    def setUp(self):
        """Crear datos de prueba."""
        self.usuario = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_crear_evento(self):
        """Prueba la creación de un evento."""
        evento = Evento.objects.create(
            usuario=self.usuario,
            tipo="LOGIN",
            descripcion="Usuario inició sesión",
            ip_address="192.168.1.1"
        )
        self.assertEqual(evento.usuario, self.usuario)
        self.assertEqual(evento.tipo, "LOGIN")
        self.assertEqual(evento.ip_address, "192.168.1.1")
    
    def test_evento_sin_usuario(self):
        """Prueba la creación de un evento sin usuario (anónimo)."""
        evento = Evento.objects.create(
            usuario=None,
            tipo="OTRO",
            descripcion="Evento anónimo"
        )
        self.assertIsNone(evento.usuario)
        self.assertEqual(evento.tipo, "OTRO")
    
    def test_evento_datos_adicionales(self):
        """Prueba el almacenamiento de datos adicionales en JSON."""
        datos = {"producto_id": 5, "cantidad": 2}
        evento = Evento.objects.create(
            usuario=self.usuario,
            tipo="AGREGAR_CARRITO",
            descripcion="Producto agregado",
            datos_adicionales=datos
        )
        self.assertEqual(evento.datos_adicionales, datos)


class UtilsTestCase(TestCase):
    """Tests para las funciones utilitarias."""
    
    def setUp(self):
        """Crear datos de prueba."""
        self.usuario = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
    
    def test_registrar_evento(self):
        """Prueba la función registrar_evento."""
        evento = registrar_evento(
            usuario=self.usuario,
            tipo="LOGIN",
            descripcion="Test de login"
        )
        self.assertIsNotNone(evento.id)
        self.assertEqual(evento.usuario, self.usuario)
        self.assertEqual(evento.tipo, "LOGIN")
    
    def test_registrar_evento_con_datos_adicionales(self):
        """Prueba registrar un evento con datos adicionales."""
        datos = {"test_key": "test_value"}
        evento = registrar_evento(
            usuario=self.usuario,
            tipo="BUSCAR",
            descripcion="Búsqueda de prueba",
            datos_adicionales=datos
        )
        self.assertEqual(evento.datos_adicionales, datos)


class EventoViewsTestCase(TestCase):
    """Tests para las vistas de eventos."""
    
    def setUp(self):
        """Crear datos de prueba."""
        self.usuario = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        # Crear algunos eventos de prueba
        for i in range(5):
            Evento.objects.create(
                usuario=self.usuario,
                tipo="LOGIN",
                descripcion=f"Evento de prueba {i}"
            )
    
    def test_vista_mis_eventos_sin_login(self):
        """Prueba que listar_mis_eventos requiere login."""
        response = self.client.get("/eventos/mis-eventos/")
        self.assertEqual(response.status_code, 302)  # Redirección a login
        self.assertIn("/login/", response.url)
    
    def test_vista_mis_eventos_con_login(self):
        """Prueba la vista de eventos del usuario autenticado."""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get("/eventos/mis-eventos/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Mis Eventos")
        self.assertEqual(len(response.context["eventos"]), 5)