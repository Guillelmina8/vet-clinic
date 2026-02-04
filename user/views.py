from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import (
    UsersCreationForm,
    UserProfileUpdateForm,
)


User = get_user_model()


class UserRegistrationView(CreateView):
    form_class = UsersCreationForm
    success_url = reverse_lazy("core:login")
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
