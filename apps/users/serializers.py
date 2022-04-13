from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.users.models import PasswordRestoreRequest, User


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["first"] = user.first_name
        token["email"] = user.email
        token["is_superuser"] = user.is_superuser
        token["is_staff"] = user.is_staff

        return token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone_number",
        )


class UserCreateSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "password",
        )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PasswordRestoreRequestSerializer(ModelSerializer):
    class Meta:
        model = PasswordRestoreRequest
        read_only_fields = (
            "id",
            "expiration_date",
        )
        fields = (
            "id",
            "email",
            "expiration_date",
        )
