import random
from datetime import datetime

from django.urls import reverse
from rest_framework import status

from apps.families.tests.factories import FamilyFactory, MembershipFactory
from apps.remedies.models import Purchase
from apps.remedies.tests.factories import MedicineFactory
from apps.remedies.tests.validators import ValidatePurchase
from apps.users.tests.factories import UserFactory
from utils.tests.testcase import CustomTestCase


class PurchaseViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.family = FamilyFactory()
        cls.user.families.add(cls.family)
        cls.medicine = MedicineFactory()

        cls.data = {
            "medicine": cls.medicine.id,
            "family": cls.family.id,
            "buy_date": datetime.now(),
            "expiration_date": datetime.now(),
            "units": random.randint(1, 20),
        }

        cls.url = reverse("remedies:purchase-create")

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_access_permission(self):
        self.backend.post(self.url, data=self.data, status=status.HTTP_201_CREATED)

        self.backend.logout()
        self.backend.post(self.url, data=self.data, status=status.HTTP_401_UNAUTHORIZED)

        # Member of no family
        non_member_user = UserFactory()
        self.backend.login(non_member_user)
        self.backend.post(self.url, data=self.data, status=status.HTTP_403_FORBIDDEN)
        self.backend.logout()

        # Member of other family
        MembershipFactory(user=non_member_user)
        self.backend.login(non_member_user)
        self.backend.post(self.url, data=self.data, status=status.HTTP_403_FORBIDDEN)
        self.backend.logout()

    def test_create_purchase_success(self):
        response = self.backend.post(
            self.url, data=self.data, status=status.HTTP_201_CREATED
        )

        instance = Purchase.objects.latest("created_on")
        ValidatePurchase.validate(self, instance, response.json())

    def test_create_purchase_fail(self):
        del self.data["family"]

        self.backend.post(
            self.url, data=self.data, format="json", status=status.HTTP_403_FORBIDDEN
        )
