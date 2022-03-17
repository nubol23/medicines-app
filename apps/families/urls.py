from django.urls import path

from apps.families.views import FamilyMembersViewSet
from apps.families.views.family_views import UserFamiliesListViewSet
from apps.families.views.invitation_views import FamilyInvitationViewSet

app_name = "families"


urlpatterns = [
    path(
        "<family_id>/members",
        FamilyMembersViewSet.as_view({"get": "list"}),
        name="family-members",
    ),
    path(
        "<family_id>/create-invitation",
        FamilyInvitationViewSet.as_view({"post": "create"}),
        name="family-create-invitation",
    ),
    path(
        "",
        UserFamiliesListViewSet.as_view({"get": "list"}),
        name="list-user-families",
    ),
]
