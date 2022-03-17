from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import CharField
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users import serializers
from apps.users.models import User


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
