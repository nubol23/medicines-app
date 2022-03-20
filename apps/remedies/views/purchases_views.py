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
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "retrieve", "partial_update"]:
            self.permission_classes = self.permission_classes + [
                UserHasFamilyAccessPermission
            ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return self.create_serializer_class
        return self.serializer_class

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(family__in=self.request.user.families.all())

        filter_by_user = self.request.query_params.get("filter-by-user", False)
        if str(filter_by_user).lower() == "true":
            qs = qs.filter(user=self.request.user)

        return qs
