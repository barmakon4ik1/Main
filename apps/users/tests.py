from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User


class UserTests(APITestCase):
    def setUp(self):
        # Создание суперпользователя, иначе тест на просмотр пользователей не пройдет
        self.admin_user = User.objects.create_superuser(
            username='admin_user',
            first_name='Admin',
            last_name='User',
            email='adminuser@example.com',
            password='admin_password123'
        )

        # Аутентификация под администратором
        self.client.force_authenticate(user=self.admin_user)

        # Создание нескольких тестовых пользователей
        User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123',
            first_name='User11',
            last_name='User12'
        )
        User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123',
            first_name='User21',
            last_name='User22'
        )

    def test_user_list(self):
        """
        Тестирование получения списка пользователей через API для администратора.
        """
        url = reverse('users-list')
        response = self.client.get(url, format='json')

        # Проверка количества пользователей (с учетом администратора и созданных в setUp)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4) # Должны быть 4 пользователя (3 из setUp и 1 новый)

    def test_user_registration(self):
        """
        Тестирование регистрации пользователя через API.
        """
        url = reverse('register')
        data = {
            'username': 'new_user',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'position': 'USER',
            'password': 'newpassword123',
            're_password': 'newpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)  # Должны быть 4 пользователя (3 из setUp и 1 новый)
        self.assertEqual(User.objects.get(username='new_user').email, 'newuser@example.com')

    def test_user_registration_password_mismatch(self):
        """
        Тестирование ошибки регистрации при несовпадении паролей.
        """
        url = reverse('register')
        data = {
            'username': 'new_user',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'position': 'USER',
            'password': 'newpassword123',
            're_password': 'different_password123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)


# Вызов теста из терминала:
# python.exe .\manage.py test apps.users.tests

