from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.remedies.models import Purchase
from apps.remedies.permissions import UserHasFamilyAccessPermission, UserHasFamilyAccessObjectPermission
from apps.remedies.serializers import (
    PurchaseCreateSerializer,
    PurchaseRetrieveSerializer, PurchaseUpdateSerializer,
)
from utils.views import CustomModelViewSet


@extend_schema_view(
    create=extend_schema(
        summary="Create purchase",
        description="Create a purchase relation with the purchased medicine instance's expiration date",
        request=PurchaseCreateSerializer,
        responses=PurchaseRetrieveSerializer,
        tags=["Purchases"],
    ),
    list=extend_schema(
        summary="List purchases",
        description="List purchases for the families the user has access, if provided, "
        "filter by comma separated list of family_ids or list only by current user's purchases.",
        parameters=[
            OpenApiParameter(
                "filter_by_user",
                type=bool,
                description="Filter only purchases made by the logged in user",
                default=False,
            ),
            OpenApiParameter(
                "family_ids",
                type=str,
                description="List of comma separated family ids.<br><br>"
                "Filter only purchases for the given families, if not provided, filter by all families",
            ),
        ],
        tags=["Purchases"],
    ),
)
class PurchasesViewSet(CustomModelViewSet):
    queryset = Purchase.objects.all()
    create_serializer_class = PurchaseCreateSerializer
    update_serializer_class = PurchaseUpdateSerializer
    serializer_class = PurchaseRetrieveSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "purchase_id"
    lookup_field = "id"

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = self.permission_classes + [
                UserHasFamilyAccessPermission
            ]
        elif self.action in ["destroy", "retrieve", "partial_update"]:
            self.permission_classes = self.permission_classes + [
                UserHasFamilyAccessObjectPermission
            ]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return self.create_serializer_class
        return self.serializer_class

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(family__in=self.request.user.families.all())

        filter_by_user = self.request.query_params.get("filter_by_user", False)
        if str(filter_by_user).lower() == "true":
            qs = qs.filter(user=self.request.user)

        family_ids = self.request.query_params.get("family_ids", None)
        if family_ids and isinstance(family_ids, str):
            family_ids = family_ids.split(",")
            qs = qs.filter(family__in=family_ids)

        return qs
