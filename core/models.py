from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from cloudinary.models import CloudinaryField


class Species(models.TextChoices):
    DOG = "dog", "Dog"
    CAT = "cat", "Cat"
    BIRD = "bird", "Bird"
    DOMESTIC = "domestic", "Domestic animal"


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"


class Location(models.TextChoices):
    lviv = "Lviv", "Lviv, Shevchenka 80"
    kyiv = "Kyiv", "Kyiv, Khmelnytskogo 15"
    odesa = "Odesa", "Varnenska 18"


class Pet(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)
    species = models.CharField(
        blank=False,
        null=False,
        max_length=20,
        choices=Species.choices
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
    image = CloudinaryField(
        "image",
        folder='avatars/',
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.get_species_display()} {self.name}".strip()


class Appointment(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    owner = models.ForeignKey(
        get_user_model(),
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
        related_name="vet_appointments",
        limit_choices_to={"is_vet": True}
    )
    date_time = models.DateTimeField(blank=False, null=False)
    duration = models.PositiveIntegerField(default=30)
    location = models.CharField(
        blank=False,
        null=False,
        choices=Location.choices,
        max_length=20
    )
    brief_complaints = models.TextField(
        blank=False,
        null=False,
        max_length=300
    )

    def __str__(self):
        return (f"{self.date_time.strftime('%d.%m %H:%M')}"
                f" - {self.pet.name} до {self.vet.last_name}")

    def clean(self):
        super().clean()
        if not self.date_time or not self.vet:
            return

        new_start = self.date_time
        new_end = new_start + timedelta(minutes=self.duration)

        overlapping = Appointment.objects.filter(
            vet=self.vet,
            date_time__lt=new_end,
        ).exclude(pk=self.pk)

        for existing in overlapping:
            existing_start = existing.date_time
            existing_end = existing_start + timedelta(
                minutes=existing.duration
            )

            if new_start < existing_end and new_end > existing_start:
                raise ValidationError(
                    f"This time slot ({existing_start.strftime('%H:%M')} - "
                    f"{existing_end.strftime('%H:%M')}) is already "
                    f"booked for this vet."
                )


class MedicalCard(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        related_name="medical_cards"
    )
    diagnosis = models.TextField(blank=False, null=False, max_length=300)
    treatment = models.TextField(blank=False, null=False, max_length=300)
    notes = models.TextField(blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Visit from {self.created_at.date()} "
                f"for {self.pet.name}")
