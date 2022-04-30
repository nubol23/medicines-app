from rest_framework import serializers

from apps.families.models import Family
from apps.families.serializers import ShortFamilySerializer
from apps.remedies.models import Medicine, Purchase
from apps.remedies.serializers import MedicineListRetrieveSerializer
from apps.users.serializers import UserSerializer


class PurchaseCreateSerializer(serializers.ModelSerializer):
    medicine = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())
    family = serializers.PrimaryKeyRelatedField(queryset=Family.objects.all())

    class Meta:
        model = Purchase
        fields = ("medicine", "family", "buy_date", "expiration_date", "units")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class PurchaseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = (
            "buy_date",
            "expiration_date",
            "units",
            "consumed",
        )


class PurchaseRetrieveSerializer(serializers.ModelSerializer):
    medicine = MedicineListRetrieveSerializer()
    user = UserSerializer()
    family = ShortFamilySerializer()

    class Meta:
        model = Purchase
        fields = (
            "id",
            "medicine",
            "user",
            "family",
            "buy_date",
            "expiration_date",
            "units",
            "consumed",
            "is_expired",
        )
