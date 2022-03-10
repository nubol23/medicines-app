import uuid

from django.db import models

from utils.models import BaseModel


class Medicine(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    maker = models.CharField(max_length=255)
    quantity = models.FloatField()
    unit = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.name} by {self.maker}"
