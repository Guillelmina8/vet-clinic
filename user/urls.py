from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    ProfileView,
    ProfileUpdateView,
    ProfileDeleteView
)

app_name = "core"

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("update/<int:pk>/", ProfileUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ProfileDeleteView.as_view(), name="delete")
]
