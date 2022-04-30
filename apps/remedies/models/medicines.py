import uuid

from django.db import models

from apps.users.models import User
from utils.models import BaseModel


class Medicine(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    maker = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="medicines",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name} by {self.maker}"
