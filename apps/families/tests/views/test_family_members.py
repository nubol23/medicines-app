from django.urls import reverse
from rest_framework import status

from apps.families.models import FamilyInvitation, Membership, InvitationStatus
from apps.families.tests.factories import (
    FamilyFactory,
    FamilyInvitationFactory,
    MembershipFactory,
)
from apps.families.tests.validators import ValidateMember
from apps.users.tests.factories import UserFactory
from utils.tests.testcase import CustomTestCase
from utils.tests.validation import ValidateMultiple


class ListFamilyMembersViewSetTests(CustomTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.family = FamilyFactory()
        # cls.family.members.add(cls.user)
        cls.user_membership = MembershipFactory(user=cls.user, family=cls.family)
        # User has pending invitation
        FamilyInvitationFactory(email=cls.user.email)

        cls.members = MembershipFactory.create_batch(size=2, family=cls.family)
        # Non member users
        MembershipFactory.create_batch(size=3)

        cls.url = reverse(
            "families:family-members", kwargs={"family_id": cls.family.id}
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
        self.backend.get(self.url, status=status.HTTP_403_FORBIDDEN)
        self.backend.logout()

        # Member of other family
        MembershipFactory(user=non_member_user)
        self.backend.login(non_member_user)
        self.backend.get(self.url, status=status.HTTP_403_FORBIDDEN)
        self.backend.logout()

    def test_list_family_members(self):
        response = self.backend.get(self.url, status=status.HTTP_200_OK)

        self.members.reverse()
        ValidateMultiple.validate(
            self,
            ValidateMember.validate,
            self.members + [self.user_membership],
            response.json(),
        )


class RemoveFamilyMembersViewSetTests(CustomTestCase):
    def _build_url(self, family_id, user_id):
        return reverse(
            "families:family-members-delete",
            kwargs={"family_id": family_id, "user_id": user_id},
        )

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory()
        cls.family = FamilyFactory()
        cls.user_membership = MembershipFactory(user=cls.user, family=cls.family)
        # User has pending invitation
        FamilyInvitationFactory(email=cls.user.email)

        cls.members = MembershipFactory.create_batch(size=2, family=cls.family)

    def setUp(self):
        super().setUp()
        self.backend.login(self.user)

    def test_access_permission(self):
        url = self._build_url(self.family.id, self.user.id)

        self.backend.logout()
        self.backend.delete(url, status=status.HTTP_401_UNAUTHORIZED)

        # Member of no family
        non_member_user = UserFactory()
        self.backend.login(non_member_user)
        self.backend.delete(url, status=status.HTTP_403_FORBIDDEN)
        self.backend.logout()

        # Member of other family
        MembershipFactory(user=non_member_user)
        self.backend.login(non_member_user)
        self.backend.delete(url, status=status.HTTP_403_FORBIDDEN)
        self.backend.logout()

        self.backend.login(self.user)
        self.backend.delete(url, status=status.HTTP_204_NO_CONTENT)

    def test_remove_already_member_user(self):
        user = self.members[0].user
        url = self._build_url(self.family.id, user.id)
        self.backend.delete(url, status=status.HTTP_204_NO_CONTENT)

        self.assertFalse(
            Membership.objects.filter(family=self.family, user=user).exists()
        )

    def test_remove_pending_member_user(self):
        url = self._build_url(self.family.id, self.user.id)
        self.backend.delete(url, status=status.HTTP_204_NO_CONTENT)

        self.assertFalse(
            Membership.objects.filter(family=self.family, user=self.user).exists()
        )
        invitation = FamilyInvitation.objects.get(email=self.user.email)
        self.assertEqual(invitation.status, InvitationStatus.REVOKED)
