from rest_framework import serializers

from apps.families.models import Family
from apps.families.serializers import FamilySerializer
from apps.remedies.models import Medicine, Purchase
from apps.remedies.serializers import MedicineListSerializer
from apps.users.serializers import UserSerializer


class PurchaseCreateSerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())
    family = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all())

    class Meta:
        model = Purchase
        fields = ("medicine", "family", "buy_date", "expiration_date")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class PurchaseRetrieveSerializer(serializers.ModelSerializer):
    medicine = MedicineListSerializer()
    user = UserSerializer()
    family = FamilySerializer()

    class Meta:
        model = Purchase
        fields = ("id", "medicine", "user", "family", "buy_date", "expiration_date")
