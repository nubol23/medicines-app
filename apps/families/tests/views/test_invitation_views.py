from unittest.mock import patch

from django.urls import reverse
from rest_framework import status

from apps.families.models import FamilyInvitation, InvitationStatus
from apps.families.serializers import ShortFamilySerializer
from apps.families.tests.factories import (
    FamilyFactory,
    FamilyInvitationFactory,
    MembershipFactory,
)
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

    @patch("utils.functions.send_mail")
    def test_create_user_has_pending_invitation_fail(self, mock_send_email):
        # Create an already invited user with pending invitation
        UserFactory(**self.data)
        FamilyInvitationFactory(**self.data, family=self.family)

        response = self.backend.post(
            self.url, data=self.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertEqual(
            response.json(), ["User already has a pending invitation to this family"]
        )
        mock_send_email.assert_not_called()

    @patch("utils.functions.send_mail")
    def test_create_user_already_family_member_fail(self, mock_send_email):
        # Create an already family member user
        invitee = UserFactory(**self.data)
        MembershipFactory(user=invitee, family=self.family)

        response = self.backend.post(
            self.url, data=self.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

        self.assertEqual(response.json(), ["User is already a member of this family"])
        mock_send_email.assert_not_called()

    @patch("utils.functions.send_mail")
    def test_add_existing_user_as_member_success(self, mock_send_email):
        # Create non member user
        invitee = UserFactory(**self.data)

        # Assert is not family member
        self.assertFalse(invitee.families.filter(id=self.family.id).exists())

        response = self.backend.post(
            self.url, data=self.data, status=status.HTTP_200_OK
        )
        self.assertEqual(response.json(), ["added existing user to family"])

        # Assert is family member
        self.assertTrue(invitee.families.filter(id=self.family.id).exists())
        mock_send_email.assert_not_called()

    @patch("utils.functions.send_mail")
    def test_create_invitation_for_new_user_success(self, mock_send_email):
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

        mock_send_email.assert_called_once()

    # from django.test import override_settings
    #
    # @override_settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend")
    # def test_invitarme(self):
    #     import config.settings.default as settings
    #
    #     data = {
    #         "email": settings.PERSONAL_TEST_EMAIL,
    #         "first_name": settings.PERSONAL_TEST_FIRST_NAME,
    #         "last_name": settings.PERSONAL_TEST_LAST_NAME,
    #         "phone_number": settings.PERSONAL_TEST_PHONE,
    #     }
    #     self.backend.post(self.url, data=data, status=status.HTTP_201_CREATED)
