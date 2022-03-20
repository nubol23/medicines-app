from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.remedies.models import Purchase
from apps.remedies.permissions import UserHasFamilyAccessPermission
from apps.remedies.serializers import (
    PurchaseCreateSerializer,
    PurchaseRetrieveSerializer,
)
from utils.views import CustomModelViewSet


@extend_schema_view(
    create=extend_schema(
        summary="Create purchase",
        description="Create a purchase relation with the purchased medicine instance's expiration date",
        request=PurchaseCreateSerializer,
        responses=PurchaseRetrieveSerializer,
        tags=["Purchases"],
    )
)
class PurchasesViewSet(CustomModelViewSet):
    queryset = Purchase.objects.all()
    create_serializer_class = PurchaseCreateSerializer
    serializer_class = PurchaseRetrieveSerializer
    permission_classes = [IsAuthenticated, UserHasFamilyAccessPermission]

    def get_serializer_class(self):
        if self.action == "create":
            return self.create_serializer_class
        return self.serializer_class
