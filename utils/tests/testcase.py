from django.test import TestCase
from django.urls import reverse
from django.utils.functional import cached_property
from rest_framework.test import APIClient


class CustomAPIClient(APIClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def login(self, user, password="password"):
        """Login a user so that calls will be authenticated with the specified user."""
        response = self.post(
            reverse("users:token_obtain_pair"),
            data={"email": user.email, "password": password},
        )
        user.refresh_from_db()
        auth_token = response.json()
        self.credentials(HTTP_AUTHORIZATION="Bearer " + auth_token["access"])
        return auth_token


class CustomTestCase(TestCase):
    @cached_property
    def backend(self):
        return CustomAPIClient()
