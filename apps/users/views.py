from uuid import UUID

from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import (
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
    inline_serializer,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import CharField, EmailField, UUIDField
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.families.models import FamilyInvitation, InvitationStatus
from apps.users import serializers
from apps.users.models import PasswordRestoreRequest, User
from apps.users.serializers import (
    PasswordRestoreRequestSerializer,
    PasswordRestoreSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from apps.users.services.activate_service import send_activate_user_email
from apps.users.services.restore_password_service import send_restore_password_email
from utils.errors import BadRequestError, UnprocessableEntityError
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
    ),
    partial_update=extend_schema(
        summary="Update user",
        description="Update user data and password if sent.",
        responses=UserSerializer,
        tags=["Users"],
    ),
    retrieve=extend_schema(
        summary="Retrieve user",
        description="Retrieve user data without password.",
        responses=UserSerializer,
        tags=["Users"],
    ),
)
class UserViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    create_serializer_class = UserCreateSerializer
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
    lookup_url_kwarg = "user_id"

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return self.create_serializer_class

        return self.serializer_class

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        email = response.data["email"]
        first_name = response.data["first_name"]
        send_activate_user_email(
            first_name=first_name, to_email=email, user_id=response.data["id"]
        )

        return response


@extend_schema_view(
    create=extend_schema(
        summary="Create Password Restore Request",
        description="Create a passoword restore request and send a password recovery email.",
        request=inline_serializer(
            "PasswordRestoreRequestCreateSerializer", fields={"email": EmailField()}
        ),
        tags=["Users"],
    ),
    update_password_with_invite=extend_schema(
        summary="Restore password given a valid restore request id",
        description="Restore password if a not expired password restore request exists",
        request=PasswordRestoreSerializer,
        responses={
            status.HTTP_200_OK: inline_serializer(
                "PasswordRestoredResponseSerializer",
                fields={"message": CharField(default="Restored password successfully")},
            ),
            status.HTTP_400_BAD_REQUEST: inline_serializer(
                "PasswordRestoredErrorResponseSerializer",
                fields={"error": CharField(default="Expired request")},
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                description="Invalid request or user"
            ),
        },
        tags=["Users"],
    ),
)
class PasswordRestoreRequestViewSet(CustomModelViewSet):
    queryset = PasswordRestoreRequest.objects.all()
    serializer_class = PasswordRestoreRequestSerializer
    permission_classes = [AllowAny]
    lookup_field = "id"
    lookup_url_kwarg = "request_id"

    def create(self, request, *args, **kwargs):
        email = self.request.data.get("email")
        user = get_object_or_404(User, email=email)

        response = super().create(request, *args, **kwargs)

        send_restore_password_email(
            first_name=user.first_name,
            to_email=user.email,
            restore_request_id=response.data["id"],
        )

        return response

    @action(detail=True, methods=["post"])
    def update_password_with_invite(self, request, *args, **kwargs):
        serializer = PasswordRestoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        req = self.get_object()

        if req.is_expired:
            raise BadRequestError("Expired request")

        with transaction.atomic():
            user = get_object_or_404(User, email=req.email)
            user.set_password(validated_data["password"])
            user.save()

            req.mark_expired()

        return Response(
            {"message": "Restored password successfully"}, status=status.HTTP_200_OK
        )
