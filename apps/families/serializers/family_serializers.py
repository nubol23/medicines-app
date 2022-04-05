from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.families.models import Family, FamilyInvitation, InvitationStatus, Membership
from apps.users.serializers import UserSerializer


class FamilyMemberSerializer(ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone_number = serializers.CharField(source="user.phone_number")
    email = serializers.CharField(source="user.email")
    status = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = ("first_name", "last_name", "phone_number", "email", "status")

    def get_status(self, instance):
        email = instance.user.email
        invitation = FamilyInvitation.objects.filter(email=email).first()
        if invitation and invitation.status == InvitationStatus.PENDING:
            return "pending"
        else:
            return ""


class FamilySerializer(ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Family
        fields = ("id", "family_name", "members")


class ShortFamilySerializer(ModelSerializer):
    class Meta:
        model = Family
        fields = (
            "id",
            "family_name",
        )
