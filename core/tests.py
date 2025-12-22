import datetime

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Pet

User = get_user_model()


class CoreViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='client',
            password="password123",
            is_vet=False,
            phone_number="1234567890"
        )
        self.vet = User.objects.create_user(
            username='doctor',
            password="password123",
            is_vet=True,
            phone_number="0987654321"
        )
        self.pet = Pet.objects.create(
            name='Rex',
            owner=self.user,
            birth_date=datetime.date(2000, 1, 1)
        )
        self.pet.save()

    def test_index_page_available_for_everyone(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)

    def test_pet_list_requires_login(self):
        response = self.client.get(reverse('core:pet-list'))
        self.assertEqual(response.status_code, 302)

    def test_client_sees_only_their_pets(self):
        other_user = User.objects.create_user(
            username='other',
            password='password',
            phone_number='1112223334')
        Pet.objects.create(
            name='StrangerDog',
            owner=other_user,
            birth_date=datetime.date(2000, 1, 1))

        self.client.login(username='client', password='password123')
        response = self.client.get(reverse('core:pet-list'))

        self.assertContains(response, 'Rex')
        self.assertNotContains(response, 'StrangerDog')

    def test_vet_sees_all_pets(self):
        self.client.login(username='doctor', password='password123')
        response = self.client.get(reverse('core:pet-list'))
        self.assertContains(response, 'Rex')

    def test_search_pets_by_name(self):
        self.client.login(username='client', password='password123')
        response = self.client.get(reverse('core:pet-list'), {'name': 'Rex'})
        self.assertContains(response, 'Rex')
        response = self.client.get(
            reverse('core:pet-list'),
            {'name': 'Bublik'})
        self.assertNotContains(response, 'Rex')

    def test_only_vet_can_access_medical_card_create(self):
        self.client.login(username='client', password='password123')
        url = reverse(
            'core:medical-card-create',
            kwargs={'pet_id': self.pet.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.login(username='doctor', password='password123')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_appointment_create_post(self):
        self.client.login(username='client', password='password123')
        data = {
            'pet': self.pet.id,
            'vet': self.vet.id,
            'date_time': '2025-12-25 10:00',
            'location': 'Lviv',
            'brief_complaints': 'Checkup'
        }
        response = self.client.post(reverse('core:appointment-create'), data)
        if response.status_code == 200:
            print(response.context['form'].errors)
        self.assertEqual(response.status_code, 302)
