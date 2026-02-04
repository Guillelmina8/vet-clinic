from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            phone_number="123456789"
        )

    def test_registration_view_get(self):
        response = self.client.get(reverse('core:register'))
        self.assertEqual(response.status_code, 200)

    def test_login_view_get(self):
        response = self.client.get(reverse('core:login'))
        self.assertEqual(response.status_code, 200)

    def test_profile_view_authenticated(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse('core:profile'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update_view_get(self):
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse(
            'core:update',
            kwargs={'pk': self.user.pk}
        ))
        self.assertEqual(response.status_code, 200)
