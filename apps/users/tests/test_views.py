import datetime
from unittest.mock import patch

from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from apps.users.models import PasswordRestoreRequest, User
from apps.users.tests.factories import PasswordRestoreRequestFactory, UserFactory
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

    @patch("utils.functions.send_mail")
    def test_create_user_with_password(self, mock_send_email):
        count = User.objects.count()
        response = self.backend.post(
            self.url, data=self.data, status=status.HTTP_201_CREATED
        )
        self.assertEqual(User.objects.count(), count + 1)

        mock_send_email.assert_called_once()

        user = User.objects.latest("created_on")
        ValidateUser.validate(self, user, response.json())

        # Fail login in as inactive user
        with self.assertRaisesMessage(KeyError, "access"):
            self.backend.login(user)

        # Activate user
        activate_url = reverse("users:activate-user")
        self.backend.post(
            activate_url, data={"user_id": user.id}, status=status.HTTP_200_OK
        )

        # Login with incorrect password
        with self.assertRaisesMessage(KeyError, "access"):
            self.backend.login(user)

        # Login with correct password
        self.backend.login(user, password="test_password")

    # from django.test import override_settings
    #
    # @override_settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend")
    # def test_send_activate_email_to_me(self):
    #     import config.settings.default as settings
    #
    #     data = {
    #         "email": settings.PERSONAL_TEST_EMAIL,
    #         "first_name": settings.PERSONAL_TEST_FIRST_NAME,
    #         "last_name": settings.PERSONAL_TEST_LAST_NAME,
    #         "phone_number": settings.PERSONAL_TEST_PHONE,
    #         "password": "test_password",
    #     }
    #
    #     self.backend.post(
    #         self.url, data=data, status=status.HTTP_201_CREATED
    #     )


class UserViewSetUpdateTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.url = reverse("users:update-user", kwargs={"user_id": cls.user.id})

        cls.data = {
            "first_name": "New name",
            "last_name": "New last name",
            "email": "new.email@test.com",
            "phone_number": "1234567",
        }

    def setUp(self):
        self.backend.login(self.user)

    def test_update_user_data(self):
        response = self.backend.patch(
            self.url, data=self.data, status=status.HTTP_200_OK
        )

        self.user.refresh_from_db()
        ValidateUser.validate(self, self.user, response.json())

    def test_update_user_data_with_password(self):
        self.data["password"] = "new_password"

        response = self.backend.patch(
            self.url, data=self.data, status=status.HTTP_200_OK
        )

        self.user.refresh_from_db()
        ValidateUser.validate(self, self.user, response.json())

        # Fail login with old password
        with self.assertRaisesMessage(KeyError, "access"):
            self.backend.login(self.user)
        # Login with new password
        self.backend.login(self.user, password="new_password")


class CreatePasswordRestoreRequestViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.url = reverse("users:restore-password")

        cls.data = {"email": cls.user.email}

    @patch("utils.functions.send_mail")
    def test_create_password_restore_request(self, mock_send_email):
        mock_send_email.assert_not_called()
        count = PasswordRestoreRequest.objects.count()

        response = self.backend.post(
            self.url, data=self.data, status=status.HTTP_201_CREATED
        )

        self.assertEqual(PasswordRestoreRequest.objects.count(), count + 1)
        self.assertEqual(response.json()["email"], self.user.email)
        mock_send_email.assert_called_once()

    @patch("utils.functions.send_mail")
    def test_create_password_restore_request_invalid_user_fail(self, mock_send_email):
        mock_send_email.assert_not_called()

        self.backend.post(
            self.url,
            data={"email": "patito@email.com"},
            status=status.HTTP_404_NOT_FOUND,
        )

        mock_send_email.assert_not_called()

    # from django.test import override_settings
    #
    # @override_settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend")
    # def test_send_restore_password_to_me(self):
    #     import config.settings.default as settings
    #
    #     User.objects.create_user(
    #         email=settings.PERSONAL_TEST_EMAIL,
    #         first_name=settings.PERSONAL_TEST_FIRST_NAME,
    #         last_name=settings.PERSONAL_TEST_LAST_NAME,
    #         phone_number=settings.PERSONAL_TEST_PHONE
    #     )
    #
    #     data = {"email": settings.PERSONAL_TEST_EMAIL}
    #
    #     self.backend.post(
    #         self.url, data=data, status=status.HTTP_201_CREATED
    #     )


class PasswordRestoreRequestViewSetUpdatePasswordTests(CustomTestCase):
    FREEZE_TIME = "2022-01-02T00:00:00Z"

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.password_request = PasswordRestoreRequestFactory(email=cls.user.email)

        cls.url = reverse(
            "users:restore-password-detail",
            kwargs={"request_id": cls.password_request.id},
        )

        cls.data = {"password": "new_password"}

    def test_update_password_by_request_success(self):
        old_password_hash = self.user.password

        self.backend.post(self.url, data=self.data, status=status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.password_request.refresh_from_db()
        self.assertNotEqual(old_password_hash, self.user.password)
        self.assertTrue(self.password_request.is_expired)

        # Fail login with old password
        with self.assertRaisesMessage(KeyError, "access"):
            self.backend.login(self.user)

        # Login with new password
        self.backend.login(self.user, password="new_password")

    @freeze_time(FREEZE_TIME)
    def test_update_password_by_request_expired_fail(self):
        self.password_request.expiration_date = datetime.datetime(
            2022, 1, 1, tzinfo=datetime.timezone.utc
        )
        self.password_request.save()

        old_password_hash = self.user.password

        response = self.backend.post(
            self.url, data=self.data, status=status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(response.json()["error"], "Expired request")

        self.user.refresh_from_db()
        self.assertEqual(old_password_hash, self.user.password)
