from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from apps.users.views import (
    CustomTokenObtainPairView,
    PasswordRestoreRequestViewSet, UserExistsViewSet, ActivateUserView, UserViewSet,
)

app_name = "users"


urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("<user_email>/exists/", UserExistsViewSet.as_view(), name="user-exists"),
    path("activate", ActivateUserView.as_view(), name="activate-user"),
    path("register", UserViewSet.as_view({"post": "create"}), name="register-user"),
    path(
        "restoration",
        PasswordRestoreRequestViewSet.as_view({"post": "create"}),
        name="restore-password",
    ),
    path(
        "restoration/<request_id>",
        PasswordRestoreRequestViewSet.as_view({"post": "update_password_with_invite"}),
        name="restore-password-detail",
    ),
    path(
        "update/<user_id>",
        UserViewSet.as_view({"patch": "partial_update"}),
        name="update-user",
    ),
    path("<user_id>", UserViewSet.as_view({"get": "retrieve"}), name="retrieve-user"),
]
