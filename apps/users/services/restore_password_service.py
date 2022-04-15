import config.settings.default as settings
from utils.functions import send_email


def send_restore_password_email(
    first_name,
    to_email,
    restore_request_id,
    redirect_to=settings.EMAIL_RESTORE_PASSWORD_URL,
):
    context = {
        "first_name": first_name,
        "redirect_to": f"{redirect_to}/{restore_request_id}",
    }
    send_email(
        subject="Recuperar su contraseña en MedicinesApp",
        template="password_restoration.html",
        context=context,
        to=[to_email],
        sender=settings.EMAIL_HOST_USER,
    )
