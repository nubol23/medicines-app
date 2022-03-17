from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.families.models import FamilyInvitation, InvitationStatus, Membership
from apps.families.permissions import UserIsFamilyMemberPermission
from apps.families.serializers import FamilyMemberSerializer
from apps.users.models import User


@extend_schema_view(
    list=extend_schema(
        summary="List Family Members",
        description="List all family members given a family id",
        tags=["Family members"],
    ),
    destroy=extend_schema(
        summary="Remove member from family",
        description="Remove a member from a family given the user and family ids. <br>"
        "If the member has a pending invitation to the family, mark it as revoked.",
        tags=["Family members"],
    ),
)
class FamilyMembersViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAuthenticated, UserIsFamilyMemberPermission]

    def get_user(self):
        return get_object_or_404(User, id=self.kwargs.get("user_id"))

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(family__id=self.kwargs["family_id"])

        return qs

    def destroy(self, request, *args, **kwargs):
        user = self.get_user()
        qs = self.get_queryset()

        with transaction.atomic():
            instance = qs.filter(user=user)
            self.perform_destroy(instance)

            # Revoking invitation if pending
            invitation = FamilyInvitation.objects.filter(email=user.email).first()
            if invitation and invitation.status == InvitationStatus.PENDING:
                invitation.status = InvitationStatus.REVOKED
                invitation.save()

        return Response(status=status.HTTP_204_NO_CONTENT)
