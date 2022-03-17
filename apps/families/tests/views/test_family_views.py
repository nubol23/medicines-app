from django.urls import reverse
from rest_framework import status

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

        cls.url = reverse("families:list-user-families")

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_list_families(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        self.families.reverse()
        ValidateMultiple.validate(
            self, ValidateShortFamily.validate, self.families, response.json()
        )
