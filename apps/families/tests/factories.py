import factory.django

from apps.families.models import Family, FamilyInvitation, Membership
from apps.users.tests.factories import UserFactory
from utils.tests.faker import faker


class FamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Family

    family_name = factory.Sequence(lambda n: f"Family {n}")


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    family = factory.SubFactory(FamilyFactory)
    user = factory.SubFactory(UserFactory)


class FamilyInvitationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FamilyInvitation

    first_name = factory.LazyAttribute(lambda _: faker.name().split()[0])
    last_name = factory.LazyAttribute(lambda _: " ".join(faker.name().split()[1:]))
    phone_number = factory.LazyAttribute(lambda _: "591" + faker.numerify("#" * 8))

    family = factory.SubFactory(FamilyFactory)
    invited_by = factory.SubFactory(UserFactory)

    @factory.lazy_attribute
    def email(self):
        return f"{self.first_name.lower()}.{self.last_name.lower()}@example.com"
