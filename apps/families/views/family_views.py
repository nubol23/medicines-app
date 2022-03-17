from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated

from apps.families.models import Family
from apps.families.permissions import UserIsFamilyMemberPermission
from apps.families.serializers import ShortFamilySerializer
from utils.views import CustomModelViewSet


@extend_schema_view(
    list=extend_schema(
        summary="List Families",
        description="List all families for which the current user is a member",
        tags=["Family"],
    ),
    create=extend_schema(
        summary="Create Family",
        description="Create family given a name",
        tags=["Family"],
    ),
    partial_update=extend_schema(
        summary="Update Family",
        description="Update family name given a family id",
        tags=["Family"],
    ),
    destroy=extend_schema(
        summary="Delete Family",
        description="Delete a family given a family id",
        tags=["Family"],
    ),
)
class UserFamiliesViewSet(CustomModelViewSet):
    queryset = Family.objects.all()
    serializer_class = ShortFamilySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "id"
    lookup_url_kwarg = "family_id"

    def get_permissions(self):
        if self.action in ["destroy", "partial_update"]:
            self.permission_classes = self.permission_classes + [
                UserIsFamilyMemberPermission
            ]

        return super().get_permissions()

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(members=self.request.user)

        return qs
