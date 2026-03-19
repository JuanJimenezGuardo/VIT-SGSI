from datetime import date

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.companies.models import Company
from apps.documents.models import Document
from apps.projects.models import Project
from apps.users.models import User


class DocumentModelTest(TestCase):
    """Test cases para el modelo Document."""

    def setUp(self):
        self.company = Company.objects.create(name='Empresa Test', rfc='123456789')
        self.user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='testpass123',
            role='CONSULTANT'
        )
        self.project = Project.objects.create(
            name='Proyecto Test',
            company=self.company,
            created_by=self.user
        )

    def _build_file(self, name='model_doc.txt'):
        return SimpleUploadedFile(name, b'contenido de prueba', content_type='text/plain')

    def test_create_document_basic(self):
        doc = Document.objects.create(
            project=self.project,
            title='Política de Seguridad',
            doc_type='POLICY',
            status='DRAFT',
            file=self._build_file('basic.txt')
        )
        self.assertEqual(doc.title, 'Política de Seguridad')
        self.assertEqual(doc.doc_type, 'POLICY')
        self.assertEqual(doc.status, 'DRAFT')

    def test_create_document_with_dates(self):
        doc = Document.objects.create(
            project=self.project,
            title='Documento con Fechas',
            doc_type='REPORT',
            status='DRAFT',
            file=self._build_file('dates.txt'),
            planned_date=date(2026, 3, 20),
            actual_date=date(2026, 3, 22)
        )
        self.assertEqual(doc.planned_date, date(2026, 3, 20))
        self.assertEqual(doc.actual_date, date(2026, 3, 22))

    def test_document_approved_validation(self):
        doc = Document(
            project=self.project,
            title='Documento sin Aprobador',
            doc_type='PROCEDURE',
            status='APPROVED'
        )

        with self.assertRaises(ValidationError):
            doc.full_clean()

    def test_document_str_representation(self):
        doc = Document.objects.create(
            project=self.project,
            title='Documento Test',
            doc_type='POLICY',
            status='DRAFT',
            file=self._build_file('str.txt')
        )
        expected = f'Documento Test ({self.project.name})'
        self.assertEqual(str(doc), expected)

    def test_document_defaults(self):
        doc = Document.objects.create(
            project=self.project,
            title='Test Doc',
            doc_type='OTHER',
            status='DRAFT',
            file=self._build_file('defaults.txt')
        )
        self.assertEqual(doc.version, '1.0')
        self.assertIsNone(doc.planned_date)
        self.assertIsNone(doc.actual_date)
        self.assertIsNotNone(doc.created_at)
