from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.remedies.models import Medicine
from apps.remedies.serializers import MedicineListSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all medicines",
        description="List all medicines in the database",
        tags=["Medicines"],
    )
)
class MedicinesViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineListSerializer
    permission_classes = [IsAuthenticated]
