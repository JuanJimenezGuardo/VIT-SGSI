from django.test import TestCase

from apps.companies.models import Company


class CompanyModelTest(TestCase):
    """Test cases para el modelo Company."""

    def test_create_company(self):
        company = Company.objects.create(
            name='Test Company',
            rfc='123456789'
        )
        self.assertEqual(company.name, 'Test Company')
        self.assertEqual(company.rfc, '123456789')

    def test_company_defaults(self):
        company = Company.objects.create(
            name='Default Company',
            rfc='987654321'
        )
        self.assertIsNotNone(company.created_at)
        self.assertIsNotNone(company.updated_at)
