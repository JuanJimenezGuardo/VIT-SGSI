from django.test import TestCase

from apps.companies.models import Company
from apps.phases.models import Phase
from apps.projects.models import Project
from apps.users.models import User


class PhaseModelTest(TestCase):
    """Test cases para el modelo Phase."""

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

    def test_create_phase(self):
        phase = Phase.objects.create(
            project=self.project,
            name='Assessment',
            type='ASSESSMENT',
            description='Initial assessment'
        )
        self.assertEqual(phase.name, 'Assessment')
        self.assertEqual(phase.project, self.project)

    def test_phase_defaults(self):
        phase = Phase.objects.create(
            project=self.project,
            name='Test Phase',
            type='PLANNING'
        )
        self.assertIsNotNone(phase.created_at)
        self.assertIsNotNone(phase.updated_at)
