import uuid

from django.db import models

from apps.users.models import User
from utils.models import BaseModel


class Family(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    family_name = models.CharField(max_length=50)
    members = models.ManyToManyField(
        User, through="Membership", related_name="families"
    )


class Membership(BaseModel):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
