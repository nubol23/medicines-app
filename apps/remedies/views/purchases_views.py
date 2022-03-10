from rest_framework.permissions import IsAuthenticated

from apps.remedies.models import Purchase
from apps.remedies.permissions import UserHasFamilyAccessPermission
from apps.remedies.serializers import (
    PurchaseCreateSerializer,
    PurchaseRetrieveSerializer,
)
from utils.views import CustomModelViewSet


class PurchasesViewSet(CustomModelViewSet):
    queryset = Purchase.objects.all()
    create_serializer_class = PurchaseCreateSerializer
    serializer_class = PurchaseRetrieveSerializer
    permission_classes = [IsAuthenticated, UserHasFamilyAccessPermission]

    def get_serializer_class(self):
        if self.action == "create":
            return self.create_serializer_class
        return self.serializer_class
