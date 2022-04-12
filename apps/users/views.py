from uuid import UUID

from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, inline_serializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import CharField, UUIDField
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.families.models import FamilyInvitation, InvitationStatus
from apps.users import serializers
from apps.users.models import User
from apps.users.serializers import UserCreateSerializer, UserSerializer
from apps.users.services.activate_service import send_activate_user_email
from utils.errors import UnprocessableEntityError
from utils.views import CustomModelViewSet


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer


class UserExistsViewSet(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Check if user with email exists",
        description="Return `true` if user with requested email exists, else return `false`.",
        responses=inline_serializer(
            "ExistResponse",
            fields={"exists": CharField(default="true")},
        ),
        tags=["Users"],
    )
    def get(self, request=None, format=None, **kwargs):
        return Response(
            {"exists": User.objects.filter(email=kwargs["user_email"]).exists()}
        )


class ActivateUserView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Activate user",
        description="Activate user and mark any pending invitation with that user's email as accepted.",
        request=inline_serializer(
            "ActivateUserSerializer", fields={"user_id": UUIDField()}
        ),
        responses={
            status.HTTP_200_OK: inline_serializer(
                "ActivateOkResponse",
                fields={
                    "message": CharField(default="user activated correctly"),
                },
            ),
            status.HTTP_422_UNPROCESSABLE_ENTITY: inline_serializer(
                "ActivateUnprocessableResponse",
                fields={
                    "error": CharField(default="invalid user"),
                },
            ),
        },
        tags=["Users"],
    )
    def post(self, request, format=None, **kwargs):
        user_id = self.request.data.get("user_id", None)

        try:
            UUID(user_id)
        except ValueError:
            raise UnprocessableEntityError("invalid user")

        if user_id:
            user = get_object_or_404(User, id=user_id)
            with transaction.atomic():
                user.is_active = True
                user.save()

                # mark the invitation as accepted if logged in as invited
                invitation = FamilyInvitation.objects.filter(email=user.email).first()
                if invitation:
                    invitation.status = InvitationStatus.ACCEPTED
                    invitation.save()

            return Response(
                {"message": "user activated correctly"}, status=status.HTTP_200_OK
            )

        else:
            raise UnprocessableEntityError("invalid user")


@extend_schema_view(
    create=extend_schema(
        summary="Register user",
        description="Create user through registration flow.",
        responses=UserSerializer,
        tags=["Users"],
    )
)
class UserViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    create_serializer_class = UserCreateSerializer
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == "create":
            return self.create_serializer_class

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        email = response.data["email"]
        first_name = response.data["first_name"]
        send_activate_user_email(first_name=first_name, to_email=email)

        return response
