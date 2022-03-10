from datetime import datetime

import factory.django
from django.utils import timezone

from apps.families.tests.factories import FamilyFactory
from apps.remedies.models import Medicine, Purchase
from apps.users.tests.factories import UserFactory
from utils.tests.faker import faker


class MedicineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Medicine

    name = factory.Sequence(lambda n: f"Medicine {n}")
    maker = factory.Sequence(lambda n: f"Maker {n}")
    quantity = factory.LazyAttribute(lambda _: faker.pyfloat(positive=True))
    unit = factory.LazyAttribute(lambda _: faker.lexify("??"))


class PurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Purchase

    medicine = factory.SubFactory(MedicineFactory)
    user = factory.SubFactory(UserFactory)
    family = factory.SubFactory(FamilyFactory)
    buy_date = factory.LazyAttribute(lambda _: datetime.now(tz=timezone.utc))
    expiration_date = factory.LazyAttribute(
        lambda _: faker.future_datetime(tzinfo=timezone.utc)
    )
