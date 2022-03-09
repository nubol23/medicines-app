from django.urls import reverse
from rest_framework import status

from apps.families.tests.factories import FamilyFactory, MembershipFactory
from apps.families.tests.validators import ValidateMember
from apps.users.tests.factories import UserFactory
from utils.tests.testcase import CustomTestCase
from utils.tests.validation import ValidateMultiple


class ListAllMedicinesViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.family = FamilyFactory()
        # cls.family.members.add(cls.user)
        cls.user_membership = MembershipFactory(user=cls.user, family=cls.family)

        cls.members = MembershipFactory.create_batch(size=2, family=cls.family)
        # Non member users
        MembershipFactory.create_batch(size=3)

        cls.url = reverse(
            "families:family-members", kwargs={"family_id": cls.family.id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_list_family_members(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        self.members.reverse()
        ValidateMultiple.validate(
            self,
            ValidateMember.validate,
            self.members + [self.user_membership],
            response.json(),
        )
