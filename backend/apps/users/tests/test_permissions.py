from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.companies.models import Company

User = get_user_model()


class RoleBasedPermissionsTest(TestCase):
    """Tests para verificar permisos basados en roles."""

    def setUp(self):
        self.client = APIClient()

        self.admin = User.objects.create_user(
            username='admin',
            email='admin@vit.local',
            password='admin123',
            role='ADMIN'
        )

        self.consultant = User.objects.create_user(
            username='consultant',
            email='consultant@vit.local',
            password='consultant123',
            role='CONSULTANT'
        )

        self.client_user = User.objects.create_user(
            username='client',
            email='client@vit.local',
            password='client123',
            role='CLIENT'
        )

        self.company = Company.objects.create(
            name='Test Company',
            rfc='TEST123456789',
            email='test@company.com',
            address='Test Address',
            city='Bogotá',
            state='Cundinamarca',
            country='Colombia',
        )

    def get_token(self, username, password):
        response = self.client.post('/api/token/', {
            'username': username,
            'password': password
        })
        return response.data['access']

    def test_admin_can_access_users_endpoint(self):
        token = self.get_token('admin', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_consultant_cannot_access_users_endpoint(self):
        token = self.get_token('consultant', 'consultant123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_cannot_access_users_endpoint(self):
        token = self.get_token('client', 'client123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_create_company(self):
        token = self.get_token('admin', 'admin123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post('/api/companies/', {
            'name': 'New Company',
            'rfc': 'NEW123456789',
            'email': 'new@company.com',
            'address': 'New Address',
            'city': 'Medellín',
            'state': 'Antioquia',
            'country': 'Colombia',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_consultant_can_create_company(self):
        token = self.get_token('consultant', 'consultant123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post('/api/companies/', {
            'name': 'Consultant Company',
            'rfc': 'CON123456789',
            'email': 'consultant@company.com',
            'address': 'Consultant Address',
            'city': 'Cali',
            'state': 'Valle',
            'country': 'Colombia',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_create_company(self):
        token = self.get_token('client', 'client123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post('/api/companies/', {
            'name': 'Client Company',
            'rfc': 'CLI123456789',
            'email': 'client@company.com',
            'address': 'Client Address',
            'city': 'Barranquilla',
            'state': 'Atlántico',
            'country': 'Colombia',
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_all_roles_can_read_companies(self):
        roles_credentials = [
            ('admin', 'admin123'),
            ('consultant', 'consultant123'),
            ('client', 'client123')
        ]

        for username, password in roles_credentials:
            token = self.get_token(username, password)
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

            response = self.client.get('/api/companies/')
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
                f'Role {username} debería poder leer empresas'
            )

    def test_consultant_can_create_project(self):
        token = self.get_token('consultant', 'consultant123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post('/api/projects/', {
            'name': 'ISO 27001 Implementation',
            'description': 'Test project',
            'company': self.company.id,
            'status': 'PLANNING',
            'planned_start_date': '2026-02-25'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_create_project(self):
        token = self.get_token('client', 'client123')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.post('/api/projects/', {
            'name': 'Client Project',
            'description': 'Should fail',
            'company': self.company.id,
            'status': 'PLANNING',
            'planned_start_date': '2026-02-25'
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
