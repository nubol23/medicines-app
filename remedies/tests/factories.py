import factory.django

from remedies.models import Medicine
from utils.tests.faker import faker


class MedicineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Medicine

    name = factory.Sequence(lambda n: f"Medicine {n}")
    maker = factory.Sequence(lambda n: f"Maker {n}")
    quantity = factory.LazyAttribute(lambda _: faker.pyfloat(positive=True))
    unit = factory.LazyAttribute(lambda _: faker.lexify("??"))
