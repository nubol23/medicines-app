from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.remedies.models import Medicine
from apps.remedies.serializers import (
    MedicineCreateUpdateSerializer,
    MedicineListRetrieveSerializer,
)
from utils.views import CustomModelViewSet


@extend_schema_view(
    list=extend_schema(
        summary="List all medicines",
        description="List all medicines in the database",
        tags=["Medicines"],
    ),
    create=extend_schema(
        summary="Create medicine",
        request=MedicineCreateUpdateSerializer,
        responses=MedicineListRetrieveSerializer,
        tags=["Medicines"],
    ),
    partial_update=extend_schema(
        summary="Update medicine",
        request=MedicineCreateUpdateSerializer,
        responses=MedicineListRetrieveSerializer,
        tags=["Medicines"],
    ),
    retrieve=extend_schema(
        summary="Retrieve medicine",
        responses=MedicineListRetrieveSerializer,
        tags=["Medicines"],
    ),
    destroy=extend_schema(
        summary="Delete medicine",
        tags=["Medicines"],
    ),
)
class MedicinesViewSet(CustomModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineListRetrieveSerializer
    create_update_serializer_class = MedicineCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "medicine_id"
    lookup_field = "id"

    def get_serializer_class(self):
        if self.action in ["create", "partial_update"]:
            return self.create_update_serializer_class
        return self.serializer_class
