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

    def __str__(self):
        return f"Family: {self.family_name}"


class Membership(BaseModel):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} member of {self.family.family_name}"
