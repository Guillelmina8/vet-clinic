from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class UserModelsTest(TestCase):
    def test_user_str(self):
        user = User.objects.create_user(
            username="testuser",
            first_name="Ivan",
            last_name="Ivanov",
            phone_number="12345"
        )
        self.assertEqual(str(user), "Ivan Ivanov")

    def test_user_str_fallback_to_username(self):
        user = User.objects.create_user(
            username="only_username",
            phone_number="54321"
        )
        self.assertEqual(str(user), "only_username")
