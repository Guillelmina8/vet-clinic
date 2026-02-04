from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class UsersCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "phone_number",
        )

    def clean_first_name(self):
        return validate_first_name(self.cleaned_data["first_name"])

    def clean_last_name(self):
        return validate_last_name(self.cleaned_data["last_name"])

    def clean_phone_number(self):
        return validate_phone_number(self.cleaned_data["phone_number"])


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "image"]

    def clean_phone_number(self):
        return validate_phone_number(self.cleaned_data["phone_number"])

    def clean_first_name(self):
        return validate_first_name(self.cleaned_data["first_name"])

    def clean_last_name(self):
        return validate_last_name(self.cleaned_data["last_name"])


def validate_first_name(first_name):
    if not first_name.isalpha():
        raise forms.ValidationError("First name must contain only letters.")
    return first_name


def validate_last_name(last_name):
    if not last_name.isalpha():
        raise forms.ValidationError("Last name must contain only letters.")
    return last_name


def validate_phone_number(phone_number):
    if not phone_number.isdigit():
        raise forms.ValidationError("Phone number must contain only digits.")
    return phone_number
