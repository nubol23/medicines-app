from django.urls import path

from apps.families.views import FamilyMembersViewSet

app_name = "families"


urlpatterns = [
    path(
        "<family_id>/members",
        FamilyMembersViewSet.as_view({"get": "list"}),
        name="family-members",
    )
]
