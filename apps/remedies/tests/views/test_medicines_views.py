from django.urls import reverse
from rest_framework import status

from apps.remedies.models import Medicine
from apps.remedies.tests.factories import MedicineFactory
from apps.remedies.tests.validators import ValidateMedicine
from apps.users.tests.factories import UserFactory
from utils.tests.faker import faker
from utils.tests.testcase import CustomTestCase
from utils.tests.validation import ValidateMultiple


class ListAllMedicinesViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.medicines = MedicineFactory.create_batch(size=3)

        cls.url = reverse("remedies:medicines-list")

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_list_all_medicines(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        self.medicines.reverse()
        ValidateMultiple.validate(
            self, ValidateMedicine.validate, self.medicines, response.json()
        )


class CreateMedicineViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.url = reverse("remedies:medicines-list")

        cls.data = {
            "name": faker.lexify(),
            "maker": faker.lexify(),
            "quantity": faker.numerify("##"),
            "unit": faker.lexify("??"),
        }

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_create_medicine(self):
        response = self.backend.post(
            self.url, data=self.data, status=status.HTTP_201_CREATED
        )

        medicine = Medicine.objects.latest("created_on")
        ValidateMedicine.validate(self, medicine, response.json())
