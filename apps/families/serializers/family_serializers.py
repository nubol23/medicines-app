from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.families.models import Family, FamilyInvitation, InvitationStatus, Membership
from apps.users.serializers import UserSerializer


class FamilyMemberSerializer(ModelSerializer):
    user_id = serializers.UUIDField(source="user.id")
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    phone_number = serializers.CharField(source="user.phone_number")
    email = serializers.CharField(source="user.email")
    status = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = (
            "user_id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "status",
        )

    def get_status(self, instance):
        email = instance.user.email
        invitation = FamilyInvitation.objects.filter(email=email).first()
        if invitation and invitation.status == InvitationStatus.PENDING:
            return "pending"
        else:
            return "active"


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

    def create(self, validated_data):
        instance = super().create(validated_data)
        instance.members.add(self.context["request"].user)
        instance.save()

        return instance
