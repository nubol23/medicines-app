from django.db import models

from apps.families.models import Family
from apps.remedies.models import Medicine
from apps.users.models import User
from utils.models import BaseModel


class Purchase(BaseModel):
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
