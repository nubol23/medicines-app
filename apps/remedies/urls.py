from django.urls import path

from apps.remedies.views import MedicinesViewSet, PurchasesViewSet

app_name = "remedies"


urlpatterns = [
    path(
        "medicines/",
        MedicinesViewSet.as_view({"get": "list", "post": "create"}),
        name="medicines-list",
    ),
    path(
        "medicines/<medicine_id>",
        MedicinesViewSet.as_view(
            {"patch": "partial_update", "get": "retrieve", "delete": "destroy"}
        ),
        name="medicines-details",
    ),
    path(
        "purchase",
        PurchasesViewSet.as_view({"post": "create", "get": "list"}),
        name="purchase-list",
    ),
    path(
        "purchase/<purchase_id>",
        PurchasesViewSet.as_view({"patch": "partial_update"}),
        name="purchase-details",
    ),
]
