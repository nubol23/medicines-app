from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.families.models import Family, FamilyInvitation, InvitationStatus, Membership
from apps.families.permissions import UserIsFamilyMemberPermission
from apps.families.serializers import FamilyInvitationCreateSerializer
from apps.users.models import User
from utils.errors import UnprocessableEntityError
from utils.functions import generate_random_password
from utils.views import CustomModelViewSet


class FamilyInvitationViewSet(CustomModelViewSet):
    queryset = FamilyInvitation.objects.all()
    serializer_class = FamilyInvitationCreateSerializer
    permission_classes = [IsAuthenticated, UserIsFamilyMemberPermission]

    def get_family(self):
        return get_object_or_404(Family, id=self.kwargs.get("family_id"))

    def create(self, request, *args, **kwargs):
        qs = self.get_queryset()

        if qs.filter(
            email__iexact=self.request.data.get("email"),
            family__id=self.kwargs["family_id"],
            status=InvitationStatus.PENDING,
        ).exists():
            raise UnprocessableEntityError(
                "User already has a pending invitation to this family"
            )

        if Membership.objects.filter(
            user__email__iexact=self.request.data.get("email"),
            family_id=self.kwargs["family_id"],
        ).exists():
            raise UnprocessableEntityError("User is already a member of this family")

        invitee = User.objects.filter(
            email__iexact=self.request.data.get("email")
        ).first()
        if invitee:
            # If invitee user already exists, add to the family
            invitee.families.add(self.get_family())
            return Response(
                ["added existing user to family"], status=status.HTTP_200_OK
            )
        else:
            # If user doesn't exists, create it, create the invitation and send it
            with transaction.atomic():
                random_password = generate_random_password()
                new_user = User.objects.create_user(
                    email=self.request.data["email"],
                    first_name=self.request.data["first_name"],
                    last_name=self.request.data["last_name"],
                    phone_number=self.request.data["phone_number"],
                    password=random_password,
                )
                self.request.data["family"] = self.kwargs["family_id"]
                super().create(request, *args, **kwargs)
                # Add user as member of the family
                new_user.families.add(self.get_family())

            # TODO: Send email invitation with a signal
            print("SEND EMAIL")

            return Response(["Created the invitation"], status=status.HTTP_201_CREATED)
