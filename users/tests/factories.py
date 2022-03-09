from datetime import timezone

import factory.django
from faker import Faker

from users.models import User

faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f"someone_{n}@mail.com")
    password = factory.PostGenerationMethodCall("set_password", "password")
    first_name = factory.Sequence(lambda n: f"Firstname {n}")
    last_name = factory.Sequence(lambda n: f"Lastname {n}")
    phone_number = factory.Faker("bothify", text="#"*11)

    is_active = True
    last_login = factory.Faker("date_time_this_month", tzinfo=timezone.utc)
