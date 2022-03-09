from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.remedies.models import Medicine
from apps.remedies.serializers import MedicineListSerializer


class ListAllMedicinesViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineListSerializer
    permission_classes = [IsAuthenticated]
