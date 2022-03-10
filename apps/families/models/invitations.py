import uuid

from django.contrib.postgres.fields import CIEmailField
from django.db import models

from apps.families.models import Family
from apps.users.models import User
from utils.models import BaseModel


class InvitationStatus(models.TextChoices):
    PENDING = "PE", "Pending"
    ACCEPTED = "AC", "Accepted"
    REVOKED = "RE", "Revoked"


class FamilyInvitation(BaseModel):
    Status = InvitationStatus

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Invited user data
    email = CIEmailField(max_length=255)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)

    family = models.ForeignKey(
        Family, related_name="invitations", on_delete=models.PROTECT
    )
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.PENDING
    )
    invited_by = models.ForeignKey(
        User, related_name="created_invitations", on_delete=models.PROTECT
    )
