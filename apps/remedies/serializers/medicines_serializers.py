from rest_framework.serializers import ModelSerializer

from apps.remedies.models import Medicine


class MedicineListSerializer(ModelSerializer):
    class Meta:
        model = Medicine
        fields = (
            "id",
            "name",
            "maker",
            "quantity",
            "unit",
        )
