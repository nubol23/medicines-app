from django.contrib.postgres.fields import CIEmailField
from django.db import models

from apps.families.models import Family
from utils.models import BaseModel


class InvitationStatus(models.TextChoices):
    PENDING = "PE", "Pending"
    ACCEPTED = "AC", "Accepted"
    REVOKED = "RE", "Revoked"


class FamilyInvitation(BaseModel):
    Status = InvitationStatus

    user_email = CIEmailField(max_length=255)
    family = models.ForeignKey(
        Family, related_name="invitations", on_delete=models.PROTECT
    )
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PENDING
    )
