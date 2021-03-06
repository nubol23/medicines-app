import config.settings.default as settings
from utils.functions import send_email


def send_family_invitation_email(
    first_name,
    inviter,
    family_name,
    username,
    password,
    to_email,
    user_id,
    redirect_to=settings.EMAIL_REDIRECT_TO_URL,
):
    context = {
        "first_name": first_name,
        "inviter": inviter,
        "family_name": family_name,
        "username": username,
        "password": password,
        "redirect_to": f"{redirect_to}/{user_id}",
    }
    send_email(
        subject=f"{inviter} te invitó a unirse a su familia en MedicinesApp",
        template="family_invitation.html",
        context=context,
        to=[to_email],
        sender=settings.EMAIL_HOST_USER,
    )
