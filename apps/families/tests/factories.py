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

    email = factory.LazyAttribute(lambda _: faker.email())
    family = factory.SubFactory(FamilyFactory)
    invited_by = factory.SubFactory(UserFactory)
