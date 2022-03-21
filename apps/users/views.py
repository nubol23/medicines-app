from django.db import transaction
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import CharField
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.families.models import FamilyInvitation, InvitationStatus
from apps.users import serializers
from apps.users.models import User
from utils.errors import UnprocessableEntityError


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
    )
    def get(self, request=None, format=None, **kwargs):
        return Response(
            {"exists": User.objects.filter(email=kwargs["user_email"]).exists()}
        )


class ActivateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None, **kwargs):
        user_id = self.request.data.get("user_id", None)
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
                {"message": "user validated correctly"}, status=status.HTTP_200_OK
            )

        else:
            raise UnprocessableEntityError("invalid user")
