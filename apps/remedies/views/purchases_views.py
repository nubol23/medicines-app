from functools import reduce

from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import CharField, Q
from django.db.models.functions import Lower
from django.http import Http404
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.remedies.models import Purchase
from apps.remedies.permissions import (
    UserHasFamilyAccessObjectPermission,
    UserHasFamilyAccessPermission,
)
from apps.remedies.serializers import (
    PurchaseCreateSerializer,
    PurchaseRetrieveSerializer,
    PurchaseUpdateSerializer,
)
from utils.views import CustomModelViewSet

CharField.register_lookup(Lower)


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
                "filter_by_not_consumed",
                type=bool,
                description="Filter only purchases that are not finished yet",
                default=False,
            ),
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
            OpenApiParameter(
                "medicine_name",
                type=str,
                description="Medicine name to search by<br/><br/>"
                "Filter all purchases by searched medicine name",
            ),
        ],
        tags=["Purchases"],
    ),
    partial_update=extend_schema(
        summary="Update Purchase",
        request=PurchaseUpdateSerializer,
        responses=PurchaseRetrieveSerializer,
        tags=["Purchases"],
    ),
    retrieve=extend_schema(
        summary="Retrieve purchase",
        responses=PurchaseRetrieveSerializer,
        tags=["Purchases"],
    ),
    destroy=extend_schema(
        summary="Delete purchase",
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

    def get_purchase_bypass_qs(self):
        try:
            return get_object_or_404(Purchase, id=self.kwargs.get("purchase_id"))
        except DjangoValidationError:
            raise Http404

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
        if self.action == "partial_update":
            return self.update_serializer_class
        return self.serializer_class

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(family__in=self.request.user.families.all())

        filter_by_not_consumed = self.request.query_params.get(
            "filter_by_not_consumed", False
        )
        if str(filter_by_not_consumed).lower() == "true":
            qs = qs.filter(consumed=False)

        filter_by_user = self.request.query_params.get("filter_by_user", False)
        if str(filter_by_user).lower() == "true":
            qs = qs.filter(user=self.request.user)

        family_ids = self.request.query_params.get("family_ids", None)
        if family_ids and isinstance(family_ids, str):
            family_ids = family_ids.split(",")
            qs = qs.filter(family__in=family_ids)

        # Search by medicines name
        q_objects = []
        name = self.request.query_params.get("medicine_name")
        if name:
            q_objects.append(Q(medicine__name__unaccent__lower__trigram_similar=name))
            q_objects.append(Q(medicine__name__icontains=name))
        if len(q_objects) > 0:
            qs = qs.filter(reduce(lambda q_1, q_2: q_1 | q_2, q_objects))

        return qs
