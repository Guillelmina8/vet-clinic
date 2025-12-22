from django.urls import path
from .views import (
    index,
    ServicesView,
    VetsView,
    UserRegistrationView,
    UserLoginView,
    ProfileView,
    ProfileUpdateView,
    ProfileDeleteView,
    PetCreateView,
    PetsListView,
    PetUpdateView,
    PetDeleteView,
    AppointmentCreateView,
    AppointmentDeleteView,
    AppointmentsListView,
    MedicalCardsListView,
    MedicalCardCreateView,
    MedicalCardDeleteView,
)

app_name = "core"

urlpatterns = [
    path("", index, name="index"),
    path("services/", ServicesView.as_view(), name="services"),
    path("vets/", VetsView.as_view(), name="vets-list"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("update/<int:pk>/", ProfileUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", ProfileDeleteView.as_view(), name="delete"),
    path("pets/", PetsListView.as_view(), name="pet-list"),
    path("pets/create/", PetCreateView.as_view(), name="pet-create"),
    path("pets/<int:pk>/update/", PetUpdateView.as_view(), name="pet-update"),
    path("pets/<int:pk>/delete/", PetDeleteView.as_view(), name="pet-delete"),
    path(
        "appointments/",
        AppointmentsListView.as_view(),
        name="appointment-list"),
    path(
        "appointments/create/",
        AppointmentCreateView.as_view(),
        name="appointment-create"),
    path(
        "appointments/<int:pk>/delete/",
        AppointmentDeleteView.as_view(),
        name="appointment-delete"),
    path(
        "pets/<int:pet_id>/medical-card/",
        MedicalCardsListView.as_view(),
        name="medical-card-list"),
    path(
        "pets/<int:pet_id>/add-medical-card/",
        MedicalCardCreateView.as_view(),
        name="medical-card-create"),
    path(
        "medical-card/<int:pk>/delete/",
        MedicalCardDeleteView.as_view(),
        name="medical-card-delete"),
]
