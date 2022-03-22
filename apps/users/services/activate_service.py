import config.settings.default as settings
from utils.functions import send_email


def send_activate_user_email(
    first_name,
    to_email,
    redirect_to=settings.EMAIL_REDIRECT_TO_URL,
):
    context = {
        "first_name": first_name,
        "redirect_to": redirect_to,
    }
    send_email(
        subject="Activar su cuenta en MedicinesApp",
        template="user_activation.html",
        context=context,
        to=[to_email],
        sender=settings.EMAIL_HOST_USER,
    )
