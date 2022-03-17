from rest_framework.permissions import IsAuthenticated

from apps.families.models import Family
from apps.families.permissions import UserIsFamilyMemberPermission
from apps.families.serializers import ShortFamilySerializer
from utils.views import CustomModelViewSet


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
