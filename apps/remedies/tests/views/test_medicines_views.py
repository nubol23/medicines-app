from django.urls import reverse
from rest_framework import status

from apps.remedies.tests.factories import MedicineFactory
from apps.remedies.tests.validators import ValidateMedicine
from apps.users.tests.factories import UserFactory
from utils.tests.testcase import CustomTestCase
from utils.tests.validation import ValidateMultiple


class ListAllMedicinesViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.medicines = MedicineFactory.create_batch(size=3)

        cls.url = reverse("remedies:medicines-all")

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_list_all_medicines(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        self.medicines.reverse()
        ValidateMultiple.validate(
            self, ValidateMedicine.validate, self.medicines, response.json()
        )
