# utils.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import EmailLog
from datetime import date
import logging
logger = logging.getLogger(__name__)


def send_quote_email(service_request, quote, manual=False):
    try:
        logger.info(f"📨 Envoi email à {service_request.email}")

        subject = "Votre devis est prêt"
        recipient = service_request.email

        context = {
            "name": service_request.name,
            "email": service_request.email,
            "service": service_request.get_service_type_display(),
            "amount": quote.amount,
            "details": quote.details,
            "quote_id": quote.id,
            "created_at": quote.created_at.strftime("%d/%m/%Y"),
            "year": date.today().year
        }

        html_content = render_to_string("emails/quote_email.html", context)

        email = EmailMultiAlternatives(
            subject,
            "Votre devis est prêt",
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
        )
        email.attach_alternative(html_content, "text/html")
        email.send()

        EmailLog.objects.create(
            quote=quote,
            recipient=recipient,
            subject=subject,
            is_manual=manual,
        )

        logger.info("✅ Email envoyé avec succès")

    except Exception as e:
        logger.error(f"❌ ERREUR EMAIL : {e}")
        raise