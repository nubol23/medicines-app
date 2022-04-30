from rest_framework.serializers import ModelSerializer

from apps.remedies.models import Medicine


class MedicineListRetrieveSerializer(ModelSerializer):
    class Meta:
        model = Medicine
        fields = (
            "id",
            "name",
            "maker",
            "quantity",
            "unit",
        )


class MedicineCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Medicine
        fields = ("name", "maker", "quantity", "unit", "created_by")

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
