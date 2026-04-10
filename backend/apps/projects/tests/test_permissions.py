"""Permission and access tests for projects and project-user relations."""

from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from apps.companies.models import Company
from apps.projects.models import Project, ProjectUser

User = get_user_model()


class ProjectUserTestCase(TestCase):
    """Tests for ProjectUser model and API endpoints."""

    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name='Test Company',
            rfc='RFC000001',
            email='company@test.com',
            phone='555-1234',
            address='Test Address',
            city='Test City',
            state='Test State',
            country='Colombia',
        )

        cls.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@test.com',
            password='testpass123',
            role='ADMIN',
        )

        cls.consultant_user = User.objects.create_user(
            username='consultant_user',
            email='consultant@test.com',
            password='testpass123',
            role='CONSULTANT',
        )

        cls.client_user = User.objects.create_user(
            username='client_user',
            email='client@test.com',
            password='testpass123',
            role='CLIENT',
        )

        cls.project = Project.objects.create(
            name='Test Project',
            description='Test project',
            company=cls.company,
            status='PLANNING',
            planned_start_date=date.today(),
            planned_end_date=date.today() + timedelta(days=365),
            created_by=cls.admin_user,
        )

    def setUp(self):
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.admin_user)
        self.admin_token = str(refresh.access_token)

        refresh = RefreshToken.for_user(self.consultant_user)
        self.consultant_token = str(refresh.access_token)

        refresh = RefreshToken.for_user(self.client_user)
        self.client_token = str(refresh.access_token)

    def test_create_project_user_as_consultant(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.consultant_token}')

        data = {
            'project': self.project.id,
            'user': self.client_user.id,
            'role': 'VIEWER',
        }

        response = self.client.post('/api/project-users/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['role'], 'VIEWER')

        pu = ProjectUser.objects.get(project=self.project, user=self.client_user)
        self.assertEqual(pu.role, 'VIEWER')

    def test_cannot_create_duplicate_project_user(self):
        ProjectUser.objects.create(
            project=self.project,
            user=self.client_user,
            role='CLIENT',
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.consultant_token}')

        data = {
            'project': self.project.id,
            'user': self.client_user.id,
            'role': 'CONSULTANT',
        }

        response = self.client.post('/api/project-users/', data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_get_project_users_list(self):
        ProjectUser.objects.create(
            project=self.project,
            user=self.admin_user,
            role='ADMIN',
        )
        ProjectUser.objects.create(
            project=self.project,
            user=self.consultant_user,
            role='CONSULTANT',
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/project-users/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_specific_project_user(self):
        pu = ProjectUser.objects.create(
            project=self.project,
            user=self.consultant_user,
            role='CONSULTANT',
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/project-users/{pu.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], 'CONSULTANT')
        self.assertEqual(response.data['username'], 'consultant_user')
        self.assertEqual(response.data['project_name'], 'Test Project')

    def test_update_project_user_role(self):
        pu = ProjectUser.objects.create(
            project=self.project,
            user=self.client_user,
            role='VIEWER',
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.consultant_token}')

        data = {'role': 'CLIENT'}
        response = self.client.patch(f'/api/project-users/{pu.id}/', data, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['role'], 'CLIENT')

        pu.refresh_from_db()
        self.assertEqual(pu.role, 'CLIENT')

    def test_delete_project_user(self):
        pu = ProjectUser.objects.create(
            project=self.project,
            user=self.client_user,
            role='VIEWER',
        )

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.consultant_token}')
        response = self.client.delete(f'/api/project-users/{pu.id}/')

        self.assertEqual(response.status_code, 204)
        self.assertFalse(ProjectUser.objects.filter(id=pu.id).exists())

    def test_client_cannot_create_project_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')

        data = {
            'project': self.project.id,
            'user': self.consultant_user.id,
            'role': 'CONSULTANT',
        }

        response = self.client.post('/api/project-users/', data, format='json')
        self.assertEqual(response.status_code, 403)

    def test_anonymous_cannot_access_project_users(self):
        response = self.client.get('/api/project-users/')
        self.assertEqual(response.status_code, 401)

    def test_project_user_string_representation(self):
        pu = ProjectUser.objects.create(
            project=self.project,
            user=self.consultant_user,
            role='CONSULTANT',
        )

        expected_str = f'{self.consultant_user.username} - {self.project.name} (Consultor)'
        self.assertEqual(str(pu), expected_str)


class ProjectFilteringTestCase(TestCase):
    """Tests for project filtering by role and ProjectUser assignments."""

    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(
            name='Filter Test Company',
            rfc='RFC999999',
            email='filter@test.com',
            phone='555-9999',
            address='Filter Address',
            city='Filter City',
            state='Filter State',
            country='Colombia',
        )

        cls.admin_user = User.objects.create_user(
            username='filter_admin',
            email='admin@filter.com',
            password='testpass123',
            role='ADMIN',
        )

        cls.consultant_user = User.objects.create_user(
            username='filter_consultant',
            email='consultant@filter.com',
            password='testpass123',
            role='CONSULTANT',
        )

        cls.client_user = User.objects.create_user(
            username='filter_client',
            email='client@filter.com',
            password='testpass123',
            role='CLIENT',
        )

        cls.project1 = Project.objects.create(
            name='Project 1',
            description='First project',
            company=cls.company,
            status='PLANNING',
            planned_start_date=date.today(),
            created_by=cls.admin_user,
        )

        cls.project2 = Project.objects.create(
            name='Project 2',
            description='Second project',
            company=cls.company,
            status='IN_PROGRESS',
            planned_start_date=date.today(),
            created_by=cls.admin_user,
        )

        ProjectUser.objects.create(
            project=cls.project1,
            user=cls.client_user,
            role='CLIENT',
        )

        ProjectUser.objects.create(
            project=cls.project1,
            user=cls.consultant_user,
            role='CONSULTANT',
        )
        ProjectUser.objects.create(
            project=cls.project2,
            user=cls.consultant_user,
            role='CONSULTANT',
        )

    def setUp(self):
        self.client = APIClient()

        refresh = RefreshToken.for_user(self.admin_user)
        self.admin_token = str(refresh.access_token)

        refresh = RefreshToken.for_user(self.consultant_user)
        self.consultant_token = str(refresh.access_token)

        refresh = RefreshToken.for_user(self.client_user)
        self.client_token = str(refresh.access_token)

    def test_admin_sees_all_projects(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_client_sees_only_assigned_projects(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.client_token}')
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Project 1')

    def test_consultant_sees_assigned_projects(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.consultant_token}')
        response = self.client.get('/api/projects/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_project_users_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/projects/{self.project1.id}/users/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        usernames = [item['username'] for item in response.data]
        self.assertIn('filter_client', usernames)
        self.assertIn('filter_consultant', usernames)

    def test_user_projects_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/users/{self.client_user.id}/projects/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Project 1')

    def test_consultant_multiple_projects_endpoint(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')
        response = self.client.get(f'/api/users/{self.consultant_user.id}/projects/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
