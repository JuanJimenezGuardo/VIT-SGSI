from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class UserAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            role='ADMIN',
            phone='1234567890',
            is_active=True,
        )

        cls.url_list = reverse('user-list')

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_list_users_returns_200(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_users_returns_multiple_items(self):
        User.objects.create(
            username='testuser2',
            email='testuser2@example.com',
            password='testpassword',
        )

        response = self.client.get(self.url_list)
        data = response.data

        if isinstance(data, dict) and 'results' in data:
            self.assertEqual(len(data['results']), 2)
        else:
            self.assertEqual(len(data), 2)

    def test_create_user_returns_201(self):
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'role': 'ADMIN',
            'phone': '111222333',
            'is_active': True,
        }

        response = self.client.post(self.url_list, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_retrieve_user_returns_200(self):
        url = reverse('user-detail', args=[self.user.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_user_returns_200(self):
        url = reverse('user-detail', args=[self.user.id])
        payload = {
            'first_name': 'Updated',
            'last_name': 'Name',
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'Updated')
        self.assertEqual(response.data['last_name'], 'Name')

    def test_delete_user_returns_204(self):
        user = User.objects.create(
            username='todelete',
            email='todelete@example.com',
            password='testpassword',
        )
        url = reverse('user-detail', args=[user.id])

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=user.id).exists())

    def test_create_user_missing_username_returns_400(self):
        payload = {
            'email': 'nouser@example.com',
            'role': 'CLIENT',
        }

        response = self.client.post(self.url_list, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid_role_returns_400(self):
        payload = {
            'username': 'badrole',
            'email': 'badrole@example.com',
            'role': 'INVALID',
        }

        response = self.client.post(self.url_list, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

