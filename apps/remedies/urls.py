from django.urls import path

from apps.remedies.views import PurchasesViewSet, MedicinesViewSet

app_name = "remedies"


urlpatterns = [
    path(
        "medicines/",
        MedicinesViewSet.as_view({"get": "list", "post": "create"}),
        name="medicines-list",
    ),
    path(
        "purchase-medicine",
        PurchasesViewSet.as_view({"post": "create"}),
        name="purchase-create",
    ),
]
