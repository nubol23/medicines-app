from django.urls import path

from apps.families.views import FamilyMembersViewSet
from apps.families.views.family_views import UserFamiliesViewSet
from apps.families.views.invitation_views import FamilyInvitationViewSet

app_name = "families"


urlpatterns = [
    path(
        "<family_id>/members",
        FamilyMembersViewSet.as_view({"get": "list"}),
        name="family-members",
    ),
    path(
        "<family_id>/delete-member/<user_id>",
        FamilyMembersViewSet.as_view({"delete": "destroy"}),
        name="family-members-delete",
    ),
    path(
        "<family_id>/create-invitation",
        FamilyInvitationViewSet.as_view({"post": "create"}),
        name="family-create-invitation",
    ),
    path(
        "",
        UserFamiliesViewSet.as_view({"get": "list", "post": "create"}),
        name="user-families-list",
    ),
    path(
        "<family_id>",
        UserFamiliesViewSet.as_view(
            {"get": "retrieve", "delete": "destroy", "patch": "partial_update"}
        ),
        name="user-families-details",
    ),
]
