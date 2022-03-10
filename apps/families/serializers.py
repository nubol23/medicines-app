from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.families.models import Family, Membership
from apps.users.serializers import UserSerializer


class FamilyMemberSerializer(ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone_number = serializers.CharField(source="user.phone_number")
    email = serializers.CharField(source="user.email")

    class Meta:
        model = Membership
        fields = ("first_name", "last_name", "phone_number", "email")


class FamilySerializer(ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Family
        fields = ("family_name", "members")
