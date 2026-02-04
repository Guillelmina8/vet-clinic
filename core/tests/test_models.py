import datetime
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from core.models import Pet, Appointment, MedicalCard

User = get_user_model()


class CoreModelsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="owner",
            password="password",
            phone_number="12345"
        )
        self.vet = User.objects.create_user(
            username="vet",
            password="password",
            is_vet=True,
            phone_number="67890"
        )
        self.pet = Pet.objects.create(
            name="Rex",
            species="dog",
            birth_date=datetime.date(2020, 1, 1),
            gender="male",
            owner=self.user
        )

        self.start_time = timezone.now().replace(
            hour=12,
            minute=0,
            second=0,
            microsecond=0
        ) + timedelta(days=1)

        Appointment.objects.create(
            pet=self.pet,
            owner=self.user,
            vet=self.vet,
            date_time=self.start_time,
            location="Lviv",
            brief_complaints="First appointment"
        )

    def test_pet_str(self):
        self.assertEqual(str(self.pet), "Dog Rex")

    def test_appointment_str(self):
        dt = datetime.datetime(2026, 12, 25, 10, 0)
        appointment = Appointment.objects.create(
            pet=self.pet,
            owner=self.user,
            vet=self.vet,
            date_time=dt,
            location="Lviv",
            brief_complaints="Checkup"
        )
        self.assertIn("Rex", str(appointment))

    def test_medical_card_str(self):
        card = MedicalCard.objects.create(
            pet=self.pet,
            diagnosis="Healthy",
            treatment="None"
        )
        self.assertEqual(str(card), f"Visit from "
                                    f"{datetime.date.today()} for Rex")

    def test_appointment_overlap_validation(self):
        duplicate_app = Appointment(
            pet=self.pet,
            owner=self.user,
            vet=self.vet,
            date_time=self.start_time + timedelta(minutes=15),
            location="Lviv",
            brief_complaints="Second appointment"
        )

        with self.assertRaises(ValidationError):
            duplicate_app.full_clean()

    def test_appointment_no_overlap_validation(self):
        safe_app = Appointment(
            pet=self.pet,
            owner=self.user,
            vet=self.vet,
            date_time=self.start_time + timedelta(minutes=30),
            location="Lviv",
            brief_complaints="After first one"
        )

        try:
            safe_app.full_clean()
        except ValidationError:
            self.fail("ValidationError raised on non-overlapping appointment")
