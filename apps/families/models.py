from django.db import models

from apps.users.models import User
from utils.models import BaseModel


class Family(BaseModel):
    family_name = models.CharField(max_length=50)
    members = models.ManyToManyField(
        User, through="Membership", related_name="families"
    )


class Membership(BaseModel):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
