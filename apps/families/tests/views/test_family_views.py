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

        cls.another_user = UserFactory()
        cls.another_family = FamilyFactory()
        MembershipFactory(user=cls.another_user, family=cls.another_family)

        cls.url = reverse(
            "families:user-families-details", kwargs={"family_id": cls.families[0].id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_permissions(self):
        url = reverse(
            "families:user-families-details",
            kwargs={"family_id": self.another_family.id},
        )
        self.backend.delete(url, status=status.HTTP_403_FORBIDDEN)

        self.backend.delete(self.url, status=status.HTTP_204_NO_CONTENT)

    def test_delete_family(self):
        count = Family.objects.count()
        self.backend.delete(self.url, status=status.HTTP_204_NO_CONTENT)

        self.assertEqual(Family.objects.count(), count - 1)
        self.assertFalse(Family.objects.filter(id=self.families[0].id).exists())


class UserFamiliesCreateViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.data = {"family_name": "test family"}

        cls.url = reverse("families:user-families-list")

    def setUp(self):
        self.backend.login(self.user)

    def test_create_family(self):
        count = Family.objects.count()
        response = self.backend.post(
            self.url, self.data, status=status.HTTP_201_CREATED
        )

        self.assertEqual(Family.objects.count(), count + 1)

        family = Family.objects.latest("created_on")
        ValidateShortFamily.validate(self, family, response.json())


class UserFamiliesUpdateViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.families = FamilyFactory.create_batch(size=2)
        for family in cls.families:
            MembershipFactory(user=cls.user, family=family)

        cls.another_user = UserFactory()
        cls.another_family = FamilyFactory()
        MembershipFactory(user=cls.another_user, family=cls.another_family)

        cls.data = {"family_name": "new_family_name"}

        cls.url = reverse(
            "families:user-families-details", kwargs={"family_id": cls.families[0].id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_permissions(self):
        url = reverse(
            "families:user-families-details",
            kwargs={"family_id": self.another_family.id},
        )
        self.backend.patch(url, self.data, status=status.HTTP_403_FORBIDDEN)

        self.backend.patch(self.url, self.data, status=status.HTTP_200_OK)

    def test_update_family(self):
        self.backend.patch(self.url, self.data, status=status.HTTP_200_OK)
        self.families[0].refresh_from_db()

        self.assertEqual(self.families[0].family_name, self.data["family_name"])
