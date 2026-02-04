from django.test import TestCase
from user.forms import UsersCreationForm


class UserFormsTest(TestCase):
    def test_phone_number_validation(self):
        data = {
            "username": "testuser",
            "phone_number": "notdigits",
        }
        form = UsersCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("phone_number", form.errors)

    def test_name_validation(self):
        data = {
            "username": "testuser",
            "first_name": "Ivan123",
        }
        form = UsersCreationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("first_name", form.errors)
