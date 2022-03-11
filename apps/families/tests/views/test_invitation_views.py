from django.urls import reverse
from rest_framework import status

from apps.families.models import FamilyInvitation, InvitationStatus
from apps.families.serializers import ShortFamilySerializer
from apps.families.tests.factories import FamilyFactory, MembershipFactory
from apps.families.tests.validators.invitation_validators import (
    ValidateFamilyInvitationCreation,
)
from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.users.tests.factories import UserFactory
from utils.tests.faker import faker
from utils.tests.testcase import CustomTestCase


class FamilyInvitationViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.family = FamilyFactory()
        MembershipFactory(user=cls.user, family=cls.family)

        cls.data = {
            "email": faker.email(),
            "first_name": faker.name().split()[0],
            "last_name": " ".join(faker.name().split()[1:]),
            "phone_number": "591" + faker.numerify("#" * 8),
        }

        cls.url = reverse(
            "families:family-create-invitation", kwargs={"family_id": cls.family.id}
        )

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_create_invitation_for_new_user_success(self):
        # Assert user doesn't exist
        self.assertFalse(User.objects.filter(email=self.data["email"]).exists())

        self.backend.post(self.url, data=self.data, status=status.HTTP_201_CREATED)

        invitation = FamilyInvitation.objects.latest("created_on")

        expected_data = {
            "family": ShortFamilySerializer(instance=self.family).data,
            "status": InvitationStatus.PENDING,
            "invited_by": UserSerializer(instance=self.user).data,
        }
        expected_data.update(self.data)

        ValidateFamilyInvitationCreation.validate(self, invitation, expected_data)

        # Assert is a member of the family
        self.assertTrue(self.family.members.filter(email=self.data["email"]).exists())
