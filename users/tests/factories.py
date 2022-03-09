from datetime import timezone

import factory.django

from users.models import User
from utils.tests.faker import faker


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.LazyAttribute(lambda _: faker.unique.email())
    password = factory.PostGenerationMethodCall("set_password", "password")
    first_name = factory.LazyAttribute(lambda _: faker.name().split()[0])
    last_name = factory.LazyAttribute(lambda _: faker.name().split()[1:])
    phone_number = factory.LazyAttribute(lambda _: "591" + faker.numerify("#" * 8))

    is_active = True
    last_login = factory.LazyAttribute(
        lambda _: faker.date_time_this_month(tzinfo=timezone.utc)
    )
