from django.urls import reverse
from rest_framework import status

from apps.users.models import User
from apps.users.tests.factories import UserFactory
from apps.users.tests.validators import ValidateUser
from utils.tests.faker import faker
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


class ActivateUserViewTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(is_active=False)
        cls.data = {"user_id": cls.user.id}

        cls.url = reverse("users:activate-user")

    def test_activate_user(self):
        with self.assertRaisesMessage(KeyError, "access"):
            self.backend.login(self.user)

        response = self.backend.post(
            self.url, data=self.data, status=status.HTTP_200_OK
        )
        self.assertEqual(response.json()["message"], "user activated correctly")

        self.backend.login(self.user)


class CreateUserViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = {
            "email": faker.email(),
            "first_name": faker.name().split()[0],
            "last_name": faker.name().split()[-1],
            "phone_number": "591" + faker.numerify("#" * 8),
            "password": "test_password",
        }

        cls.url = reverse("users:register-user")

    def test_create_user_with_password(self):
        count = User.objects.count()

        response = self.backend.post(self.url, data=self.data, status=status.HTTP_201_CREATED)

        self.assertEqual(User.objects.count(), count + 1)

        user = User.objects.latest("created_on")
        ValidateUser.validate(self, user, response.json())
