from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.assets.models import Asset
from apps.companies.models import Company
from apps.projects.models import Project
from apps.users.models import User


class AssetAPITest(APITestCase):
    """Test cases para los endpoints de Asset."""

    def setUp(self):
        self.company = Company.objects.create(name='Empresa Test', rfc='123456789')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='CONSULTANT'
        )
        self.project = Project.objects.create(
            name='Test Project',
            company=self.company,
            created_by=self.user
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_list_assets(self):
        Asset.objects.create(project=self.project, name='Asset 1', asset_type='SERVER')
        Asset.objects.create(project=self.project, name='Asset 2', asset_type='DATABASE')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/assets/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
