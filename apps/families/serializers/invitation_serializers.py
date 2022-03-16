from rest_framework import serializers

from apps.families.models import Family, FamilyInvitation
from apps.users.models import User


class FamilyInvitationCreateRequestSerializer(serializers.ModelSerializer):
    """Dummy serializer for documentation purposes"""

    invited_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = FamilyInvitation
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "status",
            "invited_by",
        )


class FamilyInvitationCreateSerializer(serializers.ModelSerializer):
    family = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all())
    invited_by = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False
    )

    class Meta:
        model = FamilyInvitation
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "family",
            "status",
            "invited_by",
        )

    def create(self, validated_data):
        validated_data["invited_by"] = self.context["request"].user
        return super().create(validated_data)
