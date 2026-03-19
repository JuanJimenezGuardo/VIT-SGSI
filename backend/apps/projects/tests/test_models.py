"""Tests for Project and ProjectUser models."""

from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.companies.models import Company
from apps.projects.models import Project, ProjectUser

User = get_user_model()


class ProjectModelTest(TestCase):
    """Test cases para el modelo Project."""

    def setUp(self):
        self.company = Company.objects.create(
            name='Empresa Test',
            rfc='123456789'
        )
        self.user = User.objects.create_user(
            username='projectuser',
            email='project@test.com',
            password='testpass123',
            role='CONSULTANT'
        )

    def test_create_project_basic(self):
        project = Project.objects.create(
            name='Test Project',
            company=self.company,
            created_by=self.user
        )
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(project.status, 'PLANNING')

    def test_project_date_validation(self):
        project = Project(
            name='Invalid Date Project',
            company=self.company,
            created_by=self.user,
            planned_start_date=date(2026, 3, 20),
            planned_end_date=date(2026, 3, 10)
        )

        with self.assertRaises(Exception):
            project.full_clean()


class ProjectUserModelTest(TestCase):
    """Test cases para el modelo ProjectUser."""

    def setUp(self):
        self.company = Company.objects.create(
            name='Empresa Test',
            rfc='123456789'
        )
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@test.com',
            password='testpass123',
            role='CONSULTANT'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@test.com',
            password='testpass123',
            role='CLIENT'
        )
        self.project = Project.objects.create(
            name='Test Project',
            company=self.company,
            created_by=self.user1
        )

    def test_create_project_user(self):
        pu = ProjectUser.objects.create(
            project=self.project,
            user=self.user2,
            role='CONSULTANT'
        )
        self.assertEqual(pu.role, 'CONSULTANT')

    def test_unique_together_constraint(self):
        ProjectUser.objects.create(
            project=self.project,
            user=self.user2,
            role='CONSULTANT'
        )

        duplicate = ProjectUser(
            project=self.project,
            user=self.user2,
            role='CLIENT'
        )

        with self.assertRaises(Exception):
            duplicate.save()
