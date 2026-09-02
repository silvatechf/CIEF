from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from agenda.models import Categoria, Evento, Lembrete
from agenda.services import processar_lembrete


class EventoModelTest(TestCase):
    def test_evento_pode_ser_criado_com_categoria(self):
        categoria = Categoria.objects.create(nombre="Reunión")
        inicio = timezone.now() + timezone.timedelta(days=1)
        fin = inicio + timezone.timedelta(hours=2)

        evento = Evento.objects.create(
            titulo="Sprint planning",
            descripcion="Planejamento do próximo sprint",
            fecha_inicio=inicio,
            fecha_fin=fin,
            ubicacion="São Paulo, SP",
        )
        evento.categoria.add(categoria)

        self.assertEqual(str(evento), "Sprint planning")
        self.assertEqual(evento.categoria.count(), 1)


class AgendaViewsTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Trabalho")
        inicio = timezone.now() + timezone.timedelta(days=2)
        fin = inicio + timezone.timedelta(hours=1)
        self.evento = Evento.objects.create(
            titulo="Reunião importante",
            descripcion="Planejamento estratégico",
            fecha_inicio=inicio,
            fecha_fin=fin,
            ubicacion="Rio de Janeiro, RJ",
        )
        self.evento.categoria.add(self.categoria)

    def test_lista_de_eventos_exibe_dados(self):
        response = self.client.get(reverse("eventos"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Reunião importante")

    def test_criar_evento_por_post(self):
        payload = {
            "titulo": "Evento novo",
            "descripcion": "Nova reunião de alinhamento",
            "fecha_inicio": (timezone.now() + timezone.timedelta(days=5)).strftime(
                "%Y-%m-%dT%H:%M"
            ),
            "fecha_fin": (
                timezone.now() + timezone.timedelta(days=5, hours=1)
            ).strftime("%Y-%m-%dT%H:%M"),
            "ubicacion": "Belo Horizonte, MG",
            "categoria": [self.categoria.id],
        }

        response = self.client.post(reverse("evento_crear"), payload)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Evento.objects.filter(titulo="Evento novo").exists())


class LembreteWhatsAppTest(TestCase):
    @patch("agenda.services.send_whatsapp_message")
    def test_processar_lembrete_dispara_chamada_apos_dois_lembretes(self, mock_send):
        evento = Evento.objects.create(
            titulo="Consulta crítica",
            descripcion="Acompanhamento do cliente",
            fecha_inicio=timezone.now() + timezone.timedelta(hours=2),
            fecha_fin=timezone.now() + timezone.timedelta(hours=3),
            ubicacion="São Paulo, SP",
        )

        lembrete = Lembrete.objects.create(
            evento=evento,
            quantidade_lembretes=2,
            ultimo_lembrete=timezone.now() - timezone.timedelta(minutes=6),
            ultima_interacao=timezone.now() - timezone.timedelta(minutes=7),
            numero_whatsapp="5511999999999",
        )

        resultado = processar_lembrete(evento, numero_whatsapp="5511999999999")

        self.assertTrue(resultado["chamada_whatsapp"])
        self.assertEqual(Lembrete.objects.get(pk=lembrete.pk).quantidade_lembretes, 2)
        self.assertGreaterEqual(mock_send.call_count, 1)
