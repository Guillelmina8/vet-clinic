from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Species(models.TextChoices):
    DOG = "dog", "Dog"
    CAT = "cat", "Cat"
    BIRD = "bird", "Bird"
    DOMESTIC = "domestic", "Domestic animal"


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"


class Location(models.TextChoices):
    lviv = "lviv", "Lviv, Shevchenka 80"
    kyiv = "kyiv", "Kyiv, Khmelnytskogo 15"
    odesa = "odesa", "Varnenska 18"


class User(AbstractUser):
    is_vet = models.BooleanField(default=False)
    phone_number = models.CharField(blank=False, null=False, max_length=20)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def str(self):
        return self.first_name + " " + self.last_name

    def get_absolute_url(self):
        ...


class Pet(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)
    species = models.CharField(
        blank=False,
        null=False,
        max_length=20,
        choices=Species
    )
    birth_date = models.DateField(blank=False, null=False)
    gender = models.CharField(
        blank=False,
        null=False,
        max_length=20,
        choices=Gender.choices
    )
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="pets"
    )

    class Meta:
        ordering = ["name"]


class Appointment(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="user_appointments"
    )
    vet = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="vet_appointments"
    )
    date_time = models.DateTimeField(blank=False, null=False)
    location = models.CharField(
        blank=False,
        null=False,
        choices=Location.choices
    )
    brief_complaints = models.TextField(blank=False, null=False, max_length=300)


class MedicalCard(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )
    diagnosis = models.TextField(blank=False, null=False, max_length=300)
    treatment = models.TextField(blank=False, null=False, max_length=300)
    notes = models.TextField(blank=True, null=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
