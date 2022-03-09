import factory.django

from apps.families.models import Family, Membership
from apps.users.tests.factories import UserFactory


class FamilyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Family

    family_name = factory.Sequence(lambda n: f"Family {n}")


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    family = factory.SubFactory(FamilyFactory)
    user = factory.SubFactory(UserFactory)
