from datetime import date

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from apps.companies.models import Company
from apps.phases.models import Phase
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.users.models import User


class TaskAPITest(APITestCase):
    """Tests para el API REST de Task."""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            role='CONSULTANT'
        )

        cls.company = Company.objects.create(
            name='Test Corp',
            rfc='RFC123456789',
            email='contact@test.com',
            phone='1234567890',
            address='Calle Test 123',
            city='Bogotá',
            state='Cundinamarca',
            country='Colombia',
        )

        cls.project = Project.objects.create(
            name='Test Project',
            company=cls.company,
            created_by=cls.user,
            planned_start_date=date(2026, 2, 5)
        )

        cls.phase = Phase.objects.create(
            name='Assessment',
            project=cls.project,
            type='ASSESSMENT',
            planned_start_date=timezone.now()
        )

        cls.task = Task.objects.create(
            phase=cls.phase,
            name='Existing Task',
            priority='HIGH'
        )

        cls.url_list = reverse('task-list')

    def setUp(self):
        self.client.force_authenticate(user=self.user)

    def test_list_tasks_returns_200(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_tasks_returns_multiple_items(self):
        Task.objects.create(
            phase=self.phase,
            name='Task 2',
            priority='LOW'
        )

        response = self.client.get(self.url_list)

        data = response.data
        if isinstance(data, dict) and 'results' in data:
            self.assertEqual(len(data['results']), 2)
        else:
            self.assertEqual(len(data), 2)

    def test_create_task_returns_201(self):
        payload = {
            'name': 'New Task via API',
            'description': 'Task creada por API',
            'phase': self.phase.id,
            'priority': 'MEDIUM',
            'status': 'PENDING',
            'assigned_to': self.user.id
        }

        response = self.client.post(self.url_list, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Task via API')
        self.assertTrue(Task.objects.filter(name='New Task via API').exists())

    def test_retrieve_task_returns_200(self):
        url = reverse('task-detail', args=[self.task.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Existing Task')

    def test_update_task_returns_200(self):
        url = reverse('task-detail', args=[self.task.id])
        payload = {
            'name': 'Updated Task',
            'priority': 'LOW'
        }

        response = self.client.patch(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Task')

    def test_delete_task_returns_204(self):
        task = Task.objects.create(
            phase=self.phase,
            name='Task to Delete'
        )
        task_id = task.id

        url = reverse('task-detail', args=[task_id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=task_id).exists())

    def test_create_task_missing_phase_returns_400(self):
        payload = {
            'name': 'Task without phase',
            'priority': 'HIGH'
        }

        response = self.client.post(self.url_list, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_invalid_priority_returns_400(self):
        payload = {
            'name': 'Invalid Priority Task',
            'phase': self.phase.id,
            'priority': 'SUPER_HIGH',
            'status': 'PENDING'
        }

        response = self.client.post(self.url_list, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
