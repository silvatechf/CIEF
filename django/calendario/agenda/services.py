from __future__ import annotations

from typing import Any

from django.utils import timezone

from agenda.models import Lembrete


def send_whatsapp_message(numero: str, texto: str) -> bool:
    """Integracao placeholder para WhatsApp Business / Twilio.
    Em ambiente real, este metodo deve usar um provedor externo.
    """
    return True


def processar_lembrete(evento: Any, numero_whatsapp: str) -> dict:
    lembrete, _ = Lembrete.objects.get_or_create(
        evento=evento,
        numero_whatsapp=numero_whatsapp,
        defaults={"ultima_interacao": timezone.now()},
    )

    agora = timezone.now()
    intervalo_5_min = agora - lembrete.ultima_interacao

    if intervalo_5_min >= timezone.timedelta(minutes=5):
        if lembrete.quantidade_lembretes < 2:
            lembrete.quantidade_lembretes += 1
        lembrete.ultimo_lembrete = agora
        lembrete.ultima_interacao = agora
        lembrete.save(
            update_fields=[
                "quantidade_lembretes",
                "ultimo_lembrete",
                "ultima_interacao",
                "updated_at",
            ]
        )

    chamada_whatsapp = lembrete.quantidade_lembretes >= 2

    if chamada_whatsapp:
        send_whatsapp_message(
            numero_whatsapp,
            f"Lembrete de urgência para o evento: {evento.titulo}. Responda para confirmar.",
        )

    return {
        "chamada_whatsapp": chamada_whatsapp,
        "quantidade_lembretes": lembrete.quantidade_lembretes,
        "ultimo_lembrete": lembrete.ultimo_lembrete,
    }
