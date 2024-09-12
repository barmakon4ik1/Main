# tests.py
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from apps.apartment.models import Housing, Address
from apps.users.models import User


class HousingTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='password123',
            first_name='New',
            last_name='User',
        )
        self.address = Address.objects.create(
            country='Country',
            city='City',
            street='Street',
            house_number='1',
            postal_code='12345'
        )
        self.housing = Housing.objects.create(
            objects_name='Test Apartment',
            type='APARTMENT',
            rooms=2,
            description='Description',
            price=100.00,
            address=self.address,
            owner=self.user
        )
        self.url = reverse('apartment-list', args=[self.housing.pk])

    def test_patch_housing(self):
        self.client.login(username='owner@example.com', password='password123')  # Аутентификация пользователя

        # Обновление данных с помощью PATCH
        data = {'price': 150.00}
        response = self.client.patch(self.url, data, format='json')

        # Проверка успешности запроса
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка обновления данных
        self.housing.refresh_from_db()
        self.assertEqual(self.housing.price, 150.00)
