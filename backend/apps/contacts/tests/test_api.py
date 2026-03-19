from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.companies.models import Company
from apps.contacts.models import Contact
from apps.users.models import User


class ContactAPITest(APITestCase):
    """Test cases para los endpoints de Contact."""

    def setUp(self):
        self.company = Company.objects.create(name='Empresa Test', rfc='123456789')
        self.user = User.objects.create_user(
            username='contact_api_user',
            email='contactapi@test.com',
            password='testpass123',
            role='CONSULTANT'
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.contact_data = {
            'company': self.company.id,
            'full_name': 'Carlos Mendez',
            'email': 'carlos@test.com',
            'phone': '3009876543',
            'position': 'Gerente TI',
            'is_active': True,
            'work_notes': 'Contacto para proyectos de seguridad'
        }

    def test_create_contact_via_api(self):
        response = self.client.post('/api/contacts/', self.contact_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['full_name'], 'Carlos Mendez')
        self.assertEqual(response.data['work_notes'], 'Contacto para proyectos de seguridad')

    def test_list_contacts_api(self):
        Contact.objects.create(company=self.company, full_name='Test 1', email='test1@test.com')
        Contact.objects.create(company=self.company, full_name='Test 2', email='test2@test.com')

        response = self.client.get('/api/contacts/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_contact_api(self):
        contact = Contact.objects.create(
            company=self.company,
            full_name='Retrieve Test',
            email='retrieve@test.com',
            work_notes='Nota de prueba'
        )

        response = self.client.get(f'/api/contacts/{contact.id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Retrieve Test')
        self.assertEqual(response.data['work_notes'], 'Nota de prueba')

    def test_update_contact_work_notes_api(self):
        contact = Contact.objects.create(
            company=self.company,
            full_name='Update Test',
            email='update@test.com',
            work_notes='Nota inicial'
        )

        update_data = {'work_notes': 'Nota actualizada'}
        response = self.client.patch(f'/api/contacts/{contact.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['work_notes'], 'Nota actualizada')

    def test_contact_field_visible_in_response(self):
        contact = Contact.objects.create(
            company=self.company,
            full_name='Visibility Test',
            email='visibility@test.com',
            work_notes='Campo visible'
        )

        response = self.client.get(f'/api/contacts/{contact.id}/', format='json')
        self.assertIn('work_notes', response.data)
        self.assertEqual(response.data['work_notes'], 'Campo visible')

    def test_create_contact_duplicate_email_returns_400(self):
        Contact.objects.create(
            company=self.company,
            full_name='Existente',
            email='duplicado@test.com'
        )

        payload = {
            'company': self.company.id,
            'full_name': 'Duplicado',
            'email': 'duplicado@test.com',
            'position': 'Analista'
        }
        response = self.client.post('/api/contacts/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
