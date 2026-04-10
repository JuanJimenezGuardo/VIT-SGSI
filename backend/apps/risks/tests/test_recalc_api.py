from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.companies.models import Company
from apps.projects.models import Project, ProjectUser
from apps.risks.models import Job, Risk

User = get_user_model()


class RiskRecalcAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = Company.objects.create(name='Empresa Recalc')

        cls.admin = User.objects.create_user(
            username='admin_recalc',
            email='admin_recalc@test.com',
            password='test1234',
            role='ADMIN',
        )
        cls.consultant = User.objects.create_user(
            username='consultant_recalc',
            email='consultant_recalc@test.com',
            password='test1234',
            role='CONSULTANT',
        )
        cls.client_user = User.objects.create_user(
            username='client_recalc',
            email='client_recalc@test.com',
            password='test1234',
            role='CLIENT',
        )
        cls.consultant_unassigned = User.objects.create_user(
            username='consultant_unassigned',
            email='consultant_unassigned@test.com',
            password='test1234',
            role='CONSULTANT',
        )

        cls.project = Project.objects.create(
            name='Proyecto Recalc',
            company=cls.company,
            created_by=cls.admin,
        )

        ProjectUser.objects.create(project=cls.project, user=cls.consultant, role='CONSULTANT')
        ProjectUser.objects.create(project=cls.project, user=cls.client_user, role='CLIENT')

        for idx in range(1, 41):
            Risk.objects.create(
                project=cls.project,
                name=f'Riesgo {idx}',
                probability=(idx % 5) + 1,
                impact=((idx + 2) % 5) + 1,
                treatment_strategy='Mitigate',
                owner=cls.admin,
            )

    def test_admin_trigger_sync_job_completes_with_metrics(self):
        self.client.force_authenticate(user=self.admin)

        response = self.client.post(
            f'/api/risks/{self.project.id}/trigger-recalc/?sync=true&workers=4',
            {},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job = Job.objects.get(pk=response.data['job_id'])

        self.assertEqual(job.status, 'SUCCESS')
        self.assertIsNotNone(job.tseq_ms)
        self.assertIsNotNone(job.tpar_ms)
        self.assertIn('summary', job.result)
        self.assertEqual(job.result['summary']['total_risks'], 40)

    def test_consultant_assigned_can_trigger(self):
        self.client.force_authenticate(user=self.consultant)

        response = self.client.post(
            f'/api/risks/{self.project.id}/trigger-recalc/',
            {'sync': True, 'workers': 2},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        job = Job.objects.get(pk=response.data['job_id'])
        self.assertEqual(job.status, 'SUCCESS')

    def test_consultant_unassigned_cannot_trigger(self):
        self.client.force_authenticate(user=self.consultant_unassigned)

        response = self.client.post(
            f'/api/risks/{self.project.id}/trigger-recalc/',
            {'sync': True},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_cannot_trigger(self):
        self.client.force_authenticate(user=self.client_user)

        response = self.client.post(
            f'/api/risks/{self.project.id}/trigger-recalc/',
            {'sync': True},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assigned_client_can_read_job_status(self):
        job = Job.objects.create(project=self.project, status='PENDING')
        self.client.force_authenticate(user=self.client_user)

        response = self.client.get(f'/api/risks/job-status/{job.job_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(response.data['job_id']), str(job.job_id))

    def test_unassigned_consultant_cannot_read_job_status(self):
        job = Job.objects.create(project=self.project, status='PENDING')
        self.client.force_authenticate(user=self.consultant_unassigned)

        response = self.client.get(f'/api/risks/job-status/{job.job_id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assigned_consultant_can_create_risk(self):
        self.client.force_authenticate(user=self.consultant)

        payload = {
            'project': self.project.id,
            'name': 'Riesgo Nuevo Consultant',
            'probability': 3,
            'impact': 4,
            'treatment_strategy': 'Mitigate',
            'owner': self.consultant.id,
        }
        response = self.client.post('/api/risks/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_client_cannot_create_risk(self):
        self.client.force_authenticate(user=self.client_user)

        payload = {
            'project': self.project.id,
            'name': 'Riesgo Prohibido Cliente',
            'probability': 3,
            'impact': 4,
            'treatment_strategy': 'Mitigate',
            'owner': self.client_user.id,
        }
        response = self.client.post('/api/risks/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_cannot_update_risk(self):
        risk = Risk.objects.filter(project=self.project).first()
        self.client.force_authenticate(user=self.client_user)

        response = self.client.patch(
            f'/api/risks/{risk.id}/',
            {'probability': 5},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_cannot_delete_risk(self):
        risk = Risk.objects.filter(project=self.project).first()
        self.client.force_authenticate(user=self.client_user)

        response = self.client.delete(f'/api/risks/{risk.id}/')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assigned_consultant_can_soft_delete_risk(self):
        risk = Risk.objects.filter(project=self.project).first()
        self.client.force_authenticate(user=self.consultant)

        response = self.client.delete(f'/api/risks/{risk.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        risk.refresh_from_db()
        self.assertTrue(risk.is_archived)

        listed = self.client.get(f'/api/risks/?project_id={self.project.id}')
        ids = [item['id'] for item in listed.data]
        self.assertNotIn(risk.id, ids)
