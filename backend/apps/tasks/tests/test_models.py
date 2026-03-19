from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.companies.models import Company
from apps.phases.models import Phase
from apps.projects.models import Project
from apps.tasks.models import Task
from apps.users.models import User


class TaskModelTest(TestCase):
    """Tests para el modelo Task."""

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

    def test_create_task_returns_correct_object(self):
        task = Task.objects.create(
            phase=self.phase,
            name='Definir alcance',
            description='Documentar el alcance del SGSI',
            priority='HIGH',
            status='IN_PROGRESS'
        )

        self.assertEqual(task.name, 'Definir alcance')
        self.assertEqual(task.description, 'Documentar el alcance del SGSI')
        self.assertEqual(task.priority, 'HIGH')
        self.assertEqual(task.status, 'IN_PROGRESS')

    def test_str_representation_returns_correct_format(self):
        task = Task.objects.create(
            phase=self.phase,
            name='Test Task',
            priority='MEDIUM'
        )

        expected = f'Test Task - {self.phase.name}'
        self.assertEqual(str(task), expected)

    def test_required_fields_raises_validation_error(self):
        task = Task()

        with self.assertRaises(ValidationError):
            task.full_clean()

    def test_optional_fields_accepts_none(self):
        task = Task.objects.create(
            phase=self.phase,
            name='Minimal Task'
        )

        self.assertIsNone(task.assigned_to)
        self.assertIsNone(task.planned_end_date)
        self.assertIsNone(task.actual_end_date)

    def test_timestamps_are_auto_generated(self):
        task = Task.objects.create(
            phase=self.phase,
            name='Timestamped Task'
        )

        self.assertIsNotNone(task.created_at)
        self.assertIsNotNone(task.updated_at)
        self.assertLessEqual(task.created_at, task.updated_at)
