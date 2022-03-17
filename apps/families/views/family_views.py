from rest_framework.permissions import IsAuthenticated

from apps.families.models import Family
from apps.families.serializers import ShortFamilySerializer
from utils.views import CustomModelViewSet


class UserFamiliesListViewSet(CustomModelViewSet):
    queryset = Family.objects.all()
    serializer_class = ShortFamilySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(members=self.request.user)

        return qs
