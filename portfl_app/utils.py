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

        text_content = f"""
        Bonjour {service_request.name},

        Votre devis est prêt.

        Service : {service_request.get_service_type_display()}
        Montant : {quote.amount} $

        Merci de nous contacter pour validation.

        Portfolio CGM
        Email : orthocgm@gmail.com
        """

        html_content = render_to_string("emails/quote_email.html", context)

        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            [recipient],
            reply_to=[settings.EMAIL_HOST_USER],
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