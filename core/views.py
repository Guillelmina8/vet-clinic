from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    ListView,
    DetailView
)
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import (
    UsersCreationForm,
    UserProfileUpdateForm,
    PetForm,
    AppointmentForm,
    MedicalCardForm
)
from .models import (Pet, Appointment, MedicalCard)

User = get_user_model()


def index(request):
    vets = User.objects.filter(is_vet=True)

    context = {
        "vets": vets,
    }
    return render(request, "core/index.html", context)


class ServicesView(TemplateView):
    template_name = "core/services.html"


class VetsView(ListView):
    model = User
    template_name = "core/vets_list.html"
    paginate_by = 3
    queryset = User.objects.filter(is_vet=True)


class UserRegistrationView(CreateView):
    form_class = UsersCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register.html"


class UserLoginView(LoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("core:index")


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "core/profile.html"

    def get_object(self):
        return self.request.user


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileUpdateForm
    template_name = "core/form.html"
    success_url = reverse_lazy("core:profile")


class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("core:index")

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.delete()
        logout(self.request)
        return redirect(success_url)

    def get_object(self, queryset=None):
        return self.request.user


class PetCreateView(LoginRequiredMixin, CreateView):
    model = Pet
    form_class = PetForm
    success_url = reverse_lazy("core:pet-list")
    template_name = "core/form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Pet"
        return context


class PetsListView(LoginRequiredMixin, ListView):
    model = Pet
    paginate_by = 3
    context_object_name = "pets"

    def get_queryset(self):
        if self.request.user.is_vet:
            queryset = Pet.objects.all().prefetch_related("medical_cards")
        else:
            queryset = Pet.objects.filter(
                owner=self.request.user
            ).prefetch_related("medical_cards")

        query = self.request.GET.get("name")
        if query:
            queryset = queryset.filter(name__icontains=query)

        return queryset


class PetUpdateView(LoginRequiredMixin, UpdateView):
    model = Pet
    form_class = PetForm
    template_name = "core/form.html"
    success_url = reverse_lazy("core:pet-list")


class PetDeleteView(LoginRequiredMixin, DeleteView):
    model = Pet
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("core:pet-list")


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = "core/form.html"
    success_url = reverse_lazy("core:appointment-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Appointment"
        return context


class AppointmentsListView(LoginRequiredMixin, ListView):
    model = Appointment
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        if user.is_vet:
            return Appointment.objects.filter(vet=user).order_by("date_time")
        return Appointment.objects.filter(
            pet__owner=user
        ).select_related(
            "pet",
            "vet"
        ).order_by("date_time")


class AppointmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Appointment
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("core:appointment-list")


class MedicalCardCreateView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    CreateView
):
    model = MedicalCard
    form_class = MedicalCardForm
    template_name = "core/form.html"
    success_url = reverse_lazy("core:pet-list")

    def test_func(self):
        return self.request.user.is_vet

    def form_valid(self, form):
        form.instance.pet_id = self.kwargs["pet_id"]
        return super().form_valid(form)


class MedicalCardsListView(LoginRequiredMixin, ListView):
    model = MedicalCard
    paginate_by = 5

    def get_queryset(self):
        return MedicalCard.objects.filter(
            pet_id=self.kwargs["pet_id"]
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["pet"] = Pet.objects.get(id=self.kwargs["pet_id"])
        return context


class MedicalCardDeleteView(
    UserPassesTestMixin,
    LoginRequiredMixin,
    DeleteView
):
    model = MedicalCard
    template_name = "core/confirm_delete.html"
    success_url = reverse_lazy("core:pet-list")
