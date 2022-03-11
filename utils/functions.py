import random
import string

from django.core.mail import send_mail
from django.template.loader import get_template


def generate_random_password(length=16):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return "".join(random.choices(chars, k=length))


def send_email(subject, template, context, to, sender=""):
    template = get_template(template)
    message = template.render(context)
    send_mail(subject, message, sender, to, html_message=message)
