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


class UpdateMedicineViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.medicine = MedicineFactory()

        cls.url = reverse(
            "remedies:medicines-details", kwargs={"medicine_id": cls.medicine.id}
        )

        cls.data = {
            "name": "new_name",
            "maker": "new_maker",
        }

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_update_medicine(self):
        response = self.backend.patch(self.url, data=self.data, status=status.HTTP_200_OK)

        self.medicine.refresh_from_db()
        ValidateMedicine.validate(self, self.medicine, response.json())


class RetrieveMedicineViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.medicines = MedicineFactory.create_batch(size=3)

        cls.url = reverse(
            "remedies:medicines-details", kwargs={"medicine_id": cls.medicines[1].id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_retrieve_medicine(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        ValidateMedicine.validate(self, self.medicines[1], response.json())


class DestroyMedicineViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()

        cls.medicines = MedicineFactory.create_batch(size=3)

        cls.url = reverse(
            "remedies:medicines-details", kwargs={"medicine_id": cls.medicines[1].id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_delete_medicine(self):
        count = Medicine.objects.count()
        self.backend.delete(self.url, status=status.HTTP_204_NO_CONTENT)

        self.assertEqual(Medicine.objects.count(), count - 1)
        self.assertFalse(Medicine.objects.filter(id=self.medicines[1].id).exists())
