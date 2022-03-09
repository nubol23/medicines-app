from datetime import timezone

import factory.django

from apps.users.models import User
from utils.tests.faker import faker


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    password = factory.PostGenerationMethodCall("set_password", "password")
    first_name = factory.LazyAttribute(lambda _: faker.name().split()[0])
    last_name = factory.LazyAttribute(lambda _: ' '.join(faker.name().split()[1:]))
    phone_number = factory.LazyAttribute(lambda _: "591" + faker.numerify("#" * 8))

    is_active = True
    last_login = factory.LazyAttribute(
        lambda _: faker.date_time_this_month(tzinfo=timezone.utc)
    )

    @factory.lazy_attribute
    def email(self):
        return f"{self.first_name.lower()}.{self.last_name.lower()}@example.com"
