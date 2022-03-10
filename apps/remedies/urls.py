from django.urls import path

from apps.remedies.views import ListAllMedicinesViewSet, PurchasesViewSet

app_name = "remedies"


urlpatterns = [
    path(
        "medicines-all/",
        ListAllMedicinesViewSet.as_view({"get": "list"}),
        name="medicines-all",
    ),
    path(
        "purchase-medicine",
        PurchasesViewSet.as_view({"post": "create"}),
        name="purchase-create",
    ),
]
