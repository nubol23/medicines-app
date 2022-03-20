from django.urls import path

from apps.remedies.views import PurchasesViewSet, MedicinesViewSet

app_name = "remedies"


urlpatterns = [
    path(
        "medicines-all/",
        MedicinesViewSet.as_view({"get": "list"}),
        name="medicines-all",
    ),
    path(
        "purchase-medicine",
        PurchasesViewSet.as_view({"post": "create"}),
        name="purchase-create",
    ),
]
