from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from remedies.models import Medicine
from remedies.serializers import MedicineListSerializer


class ListAllMedicinesViewSet(ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineListSerializer
    permission_classes = [IsAuthenticated]
