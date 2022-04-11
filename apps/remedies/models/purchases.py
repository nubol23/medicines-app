import uuid

from django.db import models

from apps.families.models import Family
from apps.remedies.models import Medicine
from apps.users.models import User
from utils.models import BaseModel


class Purchase(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medicine = models.ForeignKey(
        Medicine,
        related_name="purchases",
        on_delete=models.PROTECT,
    )
    user = models.ForeignKey(
        User,
        related_name="purchases",
        on_delete=models.PROTECT,
    )
    family = models.ForeignKey(
        Family, related_name="purchases", on_delete=models.PROTECT
    )
    buy_date = models.DateTimeField()
    expiration_date = models.DateTimeField()
    units = models.PositiveIntegerField()

    def __str__(self):
        return f"Purchase: {self.medicine.name} for {self.family.family_name}"
