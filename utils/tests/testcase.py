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

    # Modify the base request to check for status
    def assert_status(self, response, extra):
        status = extra.pop("status", None)
        if status:
            assert (
                response.status_code == status
            ), f"returned {response.status_code} instead with response {response.data}"

    def get(self, path, data=None, follow=False, **extra):
        response = super().get(path, data, follow, **extra)
        self.assert_status(response, extra)
        return response

    def post(self, path, data=None, format="json", content_type=None, **extra):
        response = super().post(path, data, format, content_type, **extra)
        self.assert_status(response, extra)
        return response

    def put(
        self, path, data=None, format="json", content_type=None, follow=False, **extra
    ):
        response = super().put(path, data, format, content_type, follow, **extra)
        self.assert_status(response, extra)
        return response

    def patch(
        self, path, data=None, format="json", content_type=None, follow=False, **extra
    ):
        response = super().patch(path, data, format, content_type, follow, **extra)
        self.assert_status(response, extra)
        return response

    def delete(
        self, path, data=None, format="json", content_type=None, follow=False, **extra
    ):
        response = super().delete(path, data, format, content_type, follow, **extra)
        self.assert_status(response, extra)
        return response


class CustomTestCase(TestCase):
    @cached_property
    def backend(self):
        return CustomAPIClient()
