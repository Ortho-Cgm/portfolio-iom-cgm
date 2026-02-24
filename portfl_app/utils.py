# utils.py
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import EmailLog
from datetime import date
import logging

logger = logging.getLogger(__name__)


def send_quote_email(service_request, quote, manual=False):
    subject = "Votre devis est prêt"
    recipient = service_request.email

    context = {
        "name": service_request.name,
        "email": service_request.email,
        "service": service_request.get_service_type_display(),
        "amount": quote.amount,
        "quote_id": quote.id,
        "created_at": quote.created_at.strftime("%d/%m/%Y"),
        "year": date.today().year,
    }

    text_content = f"""
    Bonjour {service_request.name},

    Votre devis est prêt.

    Service : {service_request.get_service_type_display()}
    Montant : {quote.amount} $

    IOM-CGM
    """

    html_content = render_to_string("emails/quote_email.html", context)

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,  # no-reply@sendgrid.net
            to=[recipient],
        )
        email.attach_alternative(html_content, "text/html")

        # IMPORTANT
        email.send(fail_silently=True)

        EmailLog.objects.create(
            quote=quote,
            recipient=recipient,
            subject=subject,
            is_manual=manual,
        )

    except Exception:
        logger.exception("❌ Erreur envoi devis (SMTP)")