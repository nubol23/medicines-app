import random
from datetime import datetime

from django.urls import reverse
from rest_framework import status

from apps.families.tests.factories import FamilyFactory, MembershipFactory
from apps.remedies.models import Purchase
from apps.remedies.tests.factories import MedicineFactory, PurchaseFactory
from apps.remedies.tests.validators import ValidatePurchase
from apps.users.tests.factories import UserFactory
from utils.tests.testcase import CustomTestCase
from utils.tests.validation import ValidateMultiple


class CreatePurchaseViewSetTests(CustomTestCase):
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

        cls.url = reverse("remedies:purchase-list")

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


class ListPurchaseViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.family = FamilyFactory()
        cls.user.families.add(cls.family)
        cls.medicine = MedicineFactory()

        cls.purchases = PurchaseFactory.create_batch(
            size=2, user=cls.user, family=cls.family
        )
        cls.purchases.extend(PurchaseFactory.create_batch(size=2, family=cls.family))
        PurchaseFactory.create_batch(size=2)

        cls.url = reverse("remedies:purchase-list")

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_list_family_purchases(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        self.purchases.reverse()
        ValidateMultiple.validate(
            self,
            ValidatePurchase.validate,
            self.purchases,
            response.json(),
        )

    def test_list_user_in_family_purchases(self):
        response = self.backend.get(
            self.url, data={"filter_by_user": True}, status=status.HTTP_200_OK
        )

        self.purchases.reverse()
        ValidateMultiple.validate(
            self,
            ValidatePurchase.validate,
            self.purchases[2:],
            response.json(),
        )

    def test_list_filtering_by_family(self):
        family_2 = FamilyFactory()
        self.user.families.add(family_2)
        self.user.save()
        family_3 = FamilyFactory()
        self.user.families.add(family_3)
        self.user.save()

        purchases_2 = PurchaseFactory.create_batch(
            size=2, user=self.user, family=family_2
        )
        purchases_3 = PurchaseFactory.create_batch(
            size=2, user=self.user, family=family_3
        )

        self.purchases.reverse()
        purchases_2.reverse()
        purchases_3.reverse()

        response = self.backend.get(
            self.url,
            data={"family_ids": f"{family_3.id}"},
            status=status.HTTP_200_OK,
        )
        ValidateMultiple.validate(
            self,
            ValidatePurchase.validate,
            purchases_3,
            response.json(),
        )

        response = self.backend.get(
            self.url,
            data={"family_ids": f"{self.family.id},{family_2.id}"},
            status=status.HTTP_200_OK,
        )
        ValidateMultiple.validate(
            self,
            ValidatePurchase.validate,
            purchases_2 + self.purchases,
            response.json(),
        )

    def test_list_filtering_by_medicine_name(self):
        med_1 = MedicineFactory(name="Paracetamol", maker="Laboratorio Chile")
        purchase_1 = PurchaseFactory(user=self.user, medicine=med_1, family=self.family)
        med_2 = MedicineFactory(name="Azitromicina", maker="Delta")
        purchase_2 = PurchaseFactory(user=self.user, medicine=med_2, family=self.family)

        response = self.backend.get(
            self.url, data={"medicine_name": "ol"}, status=status.HTTP_200_OK
        )
        ValidateMultiple.validate(
            self, ValidatePurchase.validate, [purchase_1], response.json()
        )

        response = self.backend.get(
            self.url,
            data={
                "medicine_name": "para",
            },
            status=status.HTTP_200_OK,
        )
        ValidateMultiple.validate(
            self, ValidatePurchase.validate, [purchase_1], response.json()
        )

        response = self.backend.get(
            self.url,
            data={
                "medicine_name": "azitrom",
            },
            status=status.HTTP_200_OK,
        )
        ValidateMultiple.validate(
            self, ValidatePurchase.validate, [purchase_2], response.json()
        )


class UpdatePurchaseViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.family = FamilyFactory()
        cls.user.families.add(cls.family)
        cls.medicine = MedicineFactory()
        cls.purchase = PurchaseFactory(
            medicine=cls.medicine,
            user=cls.user,
            family=cls.family,
        )

        cls.data = {
            "buy_date": datetime.now(),
            "expiration_date": datetime.now(),
            "units": random.randint(1, 20),
        }

        cls.url = reverse(
            "remedies:purchase-details", kwargs={"purchase_id": cls.purchase.id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_access_permission(self):
        self.backend.patch(self.url, data=self.data, status=status.HTTP_200_OK)

        self.backend.logout()
        self.backend.patch(
            self.url, data=self.data, status=status.HTTP_401_UNAUTHORIZED
        )

        # Member of no family
        non_member_user = UserFactory()
        self.backend.login(non_member_user)
        response = self.backend.patch(
            self.url, data=self.data, status=status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            response.json()["detail"], "User doesn't have access to this purchase"
        )
        self.backend.logout()

        # Member of other family
        MembershipFactory(user=non_member_user)
        self.backend.login(non_member_user)
        self.backend.patch(self.url, data=self.data, status=status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "User doesn't have access to this purchase"
        )
        self.backend.logout()

    def test_update_purchase(self):
        response = self.backend.patch(
            self.url, data=self.data, status=status.HTTP_200_OK
        )

        self.purchase.refresh_from_db()
        ValidatePurchase.validate(self, self.purchase, response.json())


class RetrievePurchaseViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.family = FamilyFactory()
        cls.user.families.add(cls.family)
        cls.medicine = MedicineFactory()
        cls.purchases = PurchaseFactory.create_batch(
            size=3,
            medicine=cls.medicine,
            user=cls.user,
            family=cls.family,
        )

        cls.url = reverse(
            "remedies:purchase-details", kwargs={"purchase_id": cls.purchases[1].id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_access_permission(self):
        self.backend.get(self.url, status=status.HTTP_200_OK)

        self.backend.logout()
        self.backend.get(self.url, status=status.HTTP_401_UNAUTHORIZED)

        # Member of no family
        non_member_user = UserFactory()
        self.backend.login(non_member_user)
        response = self.backend.get(self.url, status=status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "User doesn't have access to this purchase"
        )
        self.backend.logout()

        # Member of other family
        MembershipFactory(user=non_member_user)
        self.backend.login(non_member_user)
        self.backend.get(self.url, status=status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "User doesn't have access to this purchase"
        )

    def test_retrieve_purchase_fail(self):
        # Invalid uuid
        self.backend.get(
            reverse("remedies:purchase-details", kwargs={"purchase_id": "random_id"}),
            status=status.HTTP_404_NOT_FOUND,
        )

        # Valid uuid, but non existent purchase
        purchase = PurchaseFactory()
        url = (
            reverse("remedies:purchase-details", kwargs={"purchase_id": purchase.id}),
        )
        purchase.delete()
        self.backend.get(url, status=status.HTTP_404_NOT_FOUND)

    def test_retrieve_purchase_success(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        ValidatePurchase.validate(self, self.purchases[1], response.json())


class DeletePurchaseViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.family = FamilyFactory()
        cls.user.families.add(cls.family)
        cls.medicine = MedicineFactory()
        cls.purchases = PurchaseFactory.create_batch(
            size=3,
            medicine=cls.medicine,
            user=cls.user,
            family=cls.family,
        )

        cls.url = reverse(
            "remedies:purchase-details", kwargs={"purchase_id": cls.purchases[1].id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_access_permission(self):
        self.backend.logout()
        self.backend.delete(self.url, status=status.HTTP_401_UNAUTHORIZED)

        # Member of no family
        non_member_user = UserFactory()
        self.backend.login(non_member_user)
        response = self.backend.delete(self.url, status=status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "User doesn't have access to this purchase"
        )
        self.backend.logout()

        # Member of other family
        MembershipFactory(user=non_member_user)
        self.backend.login(non_member_user)
        self.backend.delete(self.url, status=status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json()["detail"], "User doesn't have access to this purchase"
        )

        self.backend.login(self.user)
        self.backend.delete(self.url, status=status.HTTP_204_NO_CONTENT)

    def test_delete_purchase_success(self):
        count = Purchase.objects.count()
        self.backend.delete(self.url, status=status.HTTP_204_NO_CONTENT)

        self.assertEqual(Purchase.objects.count(), count - 1)
        self.assertFalse(Purchase.objects.filter(id=self.purchases[1].id).exists())
