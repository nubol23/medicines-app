from django.urls import path

from remedies.views import ListAllMedicinesViewSet

app_name = "remedies"


urlpatterns = [
    path(
        "medicines-all/",
        ListAllMedicinesViewSet.as_view({"get": "list"}),
        name="medicines-all",
    )
]