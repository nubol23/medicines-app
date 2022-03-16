from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.families.models import Family, FamilyInvitation, InvitationStatus, Membership
from apps.families.permissions import UserIsFamilyMemberPermission
from apps.families.serializers import (
    FamilyInvitationCreateRequestSerializer,
    FamilyInvitationCreateSerializer,
)
from apps.families.services.invitation_service import send_family_invitation_email
from apps.users.models import User
from utils.errors import BadRequestError, UnprocessableEntityError
from utils.functions import generate_random_password
from utils.views import CustomModelViewSet


@extend_schema_view(
    create=extend_schema(
        summary="Create family invitation",
        description="Create a family invitation if the user doesn't exist, else assign the user to the family",
        request=FamilyInvitationCreateRequestSerializer,
        responses={
            status.HTTP_201_CREATED: inline_serializer(
                "CreatedResponse",
                fields={
                    "message": serializers.CharField(default="Created the invitation"),
                },
            ),
            status.HTTP_200_OK: inline_serializer(
                "OkResponse",
                fields={
                    "message": serializers.CharField(
                        default="added existing user to family"
                    ),
                },
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: inline_serializer(
                "UnprocessableResponse",
                fields={
                    "error": serializers.CharField(
                        default="User already has a pending invitation to this family"
                    ),
                },
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                "BadResponse",
                fields={
                    "error": serializers.CharField(
                        default="User is already a member of this family"
                    ),
                },
            ),
        },
        tags=["Family invitations"],
    )
)
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
            raise BadRequestError("User is already a member of this family")

        invitee = User.objects.filter(
            email__iexact=self.request.data.get("email")
        ).first()
        if invitee:
            # If invitee user already exists, add to the family
            invitee.families.add(self.get_family())
            return Response(
                {"message": "added existing user to family"}, status=status.HTTP_200_OK
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
                family_instance = self.get_family()
                new_user.families.add(family_instance)

            # Send family invitation
            send_family_invitation_email(
                first_name=self.request.data["first_name"],
                inviter=self.request.user.first_name,
                family_name=family_instance.family_name,
                username=self.request.data["email"],
                password=random_password,
                to_email=self.request.data["email"],
            )

            return Response(
                {"message": "Created the invitation"}, status=status.HTTP_201_CREATED
            )
