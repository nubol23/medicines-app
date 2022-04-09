from functools import reduce

from django.db.models import CharField, Q
from django.db.models.functions import Lower
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.remedies.models import Medicine
from apps.remedies.serializers import (
    MedicineCreateUpdateSerializer,
    MedicineListRetrieveSerializer,
)
from utils.views import CustomModelViewSet

CharField.register_lookup(Lower)


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

    def get_queryset(self):
        qs = super().get_queryset()

        q_objects = []
        name = self.request.query_params.get("name")
        if name:
            q_objects.append(Q(name__unaccent__lower__trigram_similar=name))
            q_objects.append(Q(name__icontains=name))

        maker = self.request.query_params.get("maker")
        if maker:
            q_objects.append(Q(maker__unaccent__lower__trigram_similar=maker))
            q_objects.append(Q(maker__icontains=maker))

        if len(q_objects) > 0:
            qs = qs.filter(reduce(lambda q_1, q_2: q_1 | q_2, q_objects))

        return qs
