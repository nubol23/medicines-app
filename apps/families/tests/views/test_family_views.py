from django.urls import reverse
from rest_framework import status

from apps.families.models import Family
from apps.families.tests.factories import FamilyFactory, MembershipFactory
from apps.families.tests.validators import ValidateShortFamily
from apps.users.tests.factories import UserFactory
from utils.tests.testcase import CustomTestCase
from utils.tests.validation import ValidateMultiple


class UserFamiliesListViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.families = FamilyFactory.create_batch(size=2)
        for family in cls.families:
            MembershipFactory(user=cls.user, family=family)

        another_user = UserFactory()
        another_family = FamilyFactory()
        MembershipFactory(user=another_user, family=another_family)

        cls.url = reverse("families:user-families-list")

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_list_families(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        self.families.reverse()
        ValidateMultiple.validate(
            self, ValidateShortFamily.validate, self.families, response.json()
        )


class UserFamiliesDestroyViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.families = FamilyFactory.create_batch(size=2)
        for family in cls.families:
            MembershipFactory(user=cls.user, family=family)

        another_user = UserFactory()
        another_family = FamilyFactory()
        MembershipFactory(user=another_user, family=another_family)

        cls.url = reverse(
            "families:user-families-details",
            kwargs={"family_id": cls.families[0].id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_delete_family(self):
        count = Family.objects.count()
        self.backend.delete(self.url, status=status.HTTP_204_NO_CONTENT)

        self.assertEqual(Family.objects.count(), count - 1)
        self.assertFalse(Family.objects.filter(id=self.families[0].id).exists())
