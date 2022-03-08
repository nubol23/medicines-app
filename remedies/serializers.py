from rest_framework.serializers import ModelSerializer

from remedies.models import Medicine


class MedicineListSerializer(ModelSerializer):
    class Meta:
        model = Medicine
        fields = (
            "name",
            "maker",
            "quantity",
            "unit",
        )
