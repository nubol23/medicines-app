from django.urls import reverse
from rest_framework import status

from apps.users.tests.factories import UserFactory
from utils.tests.testcase import CustomTestCase


class UserExistsViewTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

    def setUp(self):
        self.backend.login(self.user)

    def test_check_existing_user(self):
        url = reverse("users:user-exists", kwargs={"user_email": self.user.email})
        response = self.backend.get(url, status=status.HTTP_200_OK)

        self.assertTrue(response.json()["exists"])

    def test_check_non_existing_user(self):
        url = reverse(
            "users:user-exists", kwargs={"user_email": "patito.test@example.com"}
        )
        response = self.backend.get(url, status=status.HTTP_200_OK)

        self.assertFalse(response.json()["exists"])
