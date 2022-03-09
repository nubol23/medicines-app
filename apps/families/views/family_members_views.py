from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.families.models import Membership
from apps.families.permissions import UserIsFamilyMemberPermission
from apps.families.serializers import FamilyMemberSerializer


class FamilyMembersViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = FamilyMemberSerializer
    permission_classes = [IsAuthenticated, UserIsFamilyMemberPermission]

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(family__id=self.kwargs["family_id"])

        return qs
