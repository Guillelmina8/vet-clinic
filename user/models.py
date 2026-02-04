from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    is_vet = models.BooleanField(default=False)
    phone_number = PhoneNumberField(
        blank=False, null=False, max_length=20, unique=True)
    image = CloudinaryField(
        "image",
        folder="avatars/",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = "core_user"

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
