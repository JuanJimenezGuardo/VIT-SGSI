"""Tests for Project and ProjectUser API endpoints."""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.companies.models import Company
from apps.contacts.models import Contact
from apps.projects.models import Project, ProjectUser, ProjectContact

User = get_user_model()


class ProjectUserAPITest(APITestCase):
    """Tests for ProjectUser API endpoints."""

    def setUp(self):
        self.company = Company.objects.create(
            name='Test Company',
            rfc='123456789'
        )

        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@test.com',
            password='testpass123',
            role='ADMIN'
        )

        self.consultant_user = User.objects.create_user(
            username='consultant_user',
            email='consultant@test.com',
            password='testpass123',
            role='CONSULTANT'
        )

        self.client_user = User.objects.create_user(
            username='client_user',
            email='client@test.com',
            password='testpass123',
            role='CLIENT'
        )

        self.project = Project.objects.create(
            name='Test Project',
            company=self.company,
            created_by=self.admin_user
        )

        refresh = RefreshToken.for_user(self.admin_user)
        self.admin_token = str(refresh.access_token)

        refresh = RefreshToken.for_user(self.consultant_user)
        self.consultant_token = str(refresh.access_token)

        refresh = RefreshToken.for_user(self.client_user)
        self.client_token = str(refresh.access_token)

    def test_create_project_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.consultant_token}')

        data = {
            'project': self.project.id,
            'user': self.client_user.id,
            'role': 'VIEWER'
        }

        response = self.client.post('/api/project-users/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['role'], 'VIEWER')

    def test_list_project_users(self):
        ProjectUser.objects.create(
            project=self.project,
            user=self.admin_user,
            role='ADMIN'
        )
        ProjectUser.objects.create(
            project=self.project,
            user=self.consultant_user,
            role='CONSULTANT'
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/project-users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_project_user(self):
        pu = ProjectUser.objects.create(
            project=self.project,
            user=self.consultant_user,
            role='CONSULTANT'
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/project-users/{pu.id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'CONSULTANT')

    def test_update_project_user(self):
        pu = ProjectUser.objects.create(
            project=self.project,
            user=self.client_user,
            role='VIEWER'
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.consultant_token}')

        data = {'role': 'CLIENT'}
        response = self.client.patch(f'/api/project-users/{pu.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['role'], 'CLIENT')


class ProjectContactAPITest(APITestCase):
    """Tests for ProjectContact API endpoints."""

    def setUp(self):
        self.company = Company.objects.create(
            name='Test Company',
            rfc='123456789'
        )
        self.other_company = Company.objects.create(
            name='Other Company',
            rfc='987654321'
        )
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
        self.contact = Contact.objects.create(
            company=self.company,
            full_name='Contacto QA',
            email='contactoqa@test.com'
        )
        self.other_contact = Contact.objects.create(
            company=self.other_company,
            full_name='Contacto externo',
            email='externo@test.com'
        )

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_list_project_contacts(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get('/api/project-contacts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_project_contact(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        payload = {
            'project': self.project.id,
            'contact': self.contact.id,
            'contact_role': 'PROJECT_MANAGER',
            'is_primary': True,
            'work_notes': 'Contacto principal del proyecto'
        }
        response = self.client.post('/api/project-contacts/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contact_role'], 'PROJECT_MANAGER')

    def test_patch_project_contact(self):
        project_contact = ProjectContact.objects.create(
            project=self.project,
            contact=self.contact,
            contact_role='CISO',
            is_primary=False,
            work_notes='Inicial'
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        payload = {
            'is_primary': True,
            'work_notes': 'Actualizado por QA'
        }
        response = self.client.patch(f'/api/project-contacts/{project_contact.id}/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_primary'])
        self.assertEqual(response.data['work_notes'], 'Actualizado por QA')

    def test_create_project_contact_cross_company_returns_400(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        payload = {
            'project': self.project.id,
            'contact': self.other_contact.id,
            'contact_role': 'CONSULTANT',
            'is_primary': False
        }
        response = self.client.post('/api/project-contacts/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
