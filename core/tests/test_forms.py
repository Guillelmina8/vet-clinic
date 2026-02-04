import datetime
from django.test import TestCase
from django.utils import timezone
from core.forms import PetForm, AppointmentForm
from django.contrib.auth import get_user_model

User = get_user_model()


class CoreFormsTest(TestCase):
    def test_pet_form_future_date(self):
        future_date = timezone.now().date() + datetime.timedelta(days=1)
        data = {
            "name": "Buddy",
            "species": "dog",
            "birth_date": future_date,
            "gender": "male"
        }
        form = PetForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("birth_date", form.errors)

    def test_appointment_form_past_date(self):
        past_time = timezone.now() - datetime.timedelta(hours=1)
        data = {
            "date_time": past_time,
            "location": "Lviv",
            "brief_complaints": "Urgent"
        }
        form = AppointmentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("date_time", form.errors)
