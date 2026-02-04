from django import forms
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Pet, Appointment, MedicalCard, Species, Gender, Location

User = get_user_model()


class PetForm(forms.ModelForm):
    species = forms.ChoiceField(choices=Species, widget=forms.Select)
    birth_date = forms.DateField(
        widget=forms.DateInput(
            attrs={"type": "date"}
        )
    )
    gender = forms.ChoiceField(choices=Gender, widget=forms.Select)

    class Meta:
        model = Pet
        fields = ["name", "species", "birth_date", "gender", "image"]

    def clean_birth_date(self):
        birth_date = self.cleaned_data["birth_date"]
        if birth_date > timezone.now().date():
            raise forms.ValidationError(
                "Birth date must be up to or "
                "including today's date."
            )
        return birth_date


class PetSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={"placeholder": "Search by name"}),
    )


class AppointmentForm(forms.ModelForm):
    pet = forms.ModelChoiceField(
        queryset=Pet.objects.all(),
        widget=forms.Select()
    )
    vet = forms.ModelChoiceField(
        queryset=User.objects.filter(is_vet=True).all(),
        widget=forms.Select
    )
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"}
        )
    )
    location = forms.ChoiceField(
        choices=Location.choices,
        widget=forms.Select()
    )

    class Meta:
        model = Appointment
        fields = ["pet", "vet", "date_time", "location", "brief_complaints", ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AppointmentForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=user)

    def clean_date_time(self):
        date_time = self.cleaned_data["date_time"]
        if date_time < timezone.now():
            raise forms.ValidationError("Date time cannot be in the past.")
        return date_time


class MedicalCardForm(forms.ModelForm):

    class Meta:
        model = MedicalCard
        fields = ["diagnosis", "treatment", "notes", ]
        widgets = {
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 2}),
        }
