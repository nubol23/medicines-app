from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from apps.users.views import (
    ActivateUserView,
    CustomTokenObtainPairView,
    UserExistsViewSet,
    UserViewSet,
)

app_name = "users"


urlpatterns = [
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("<user_email>/exists/", UserExistsViewSet.as_view(), name="user-exists"),
    path("activate", ActivateUserView.as_view(), name="activate-user"),
    path("register", UserViewSet.as_view({"post": "create"}), name="register-user"),
]
