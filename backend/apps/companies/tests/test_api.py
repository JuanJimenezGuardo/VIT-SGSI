from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.companies.models import Company
from apps.users.models import User


class CompanyAPITest(APITestCase):
    """Test cases para los endpoints de Company."""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='ADMIN'
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_list_companies(self):
        Company.objects.create(name='Company 1', rfc='111111111')
        Company.objects.create(name='Company 2', rfc='222222222')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/companies/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
