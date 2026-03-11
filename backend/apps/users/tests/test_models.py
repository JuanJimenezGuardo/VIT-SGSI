from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from apps.users.models import User


class UserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            first_name='Test',
            last_name='User',
            role='CONSULTANT',
            phone='1234567890',
            is_active=True,
        )

    def test_create_user_with_all_fields(self):
        # crear user con todos los campos
        user = User.objects.create(
            username='testuser2',
            email='testuser2@example.com',
            password='testpassword2',
            first_name='Test',
            last_name='User2',
            role='ADMIN',
            phone='0987654321',
            is_active=True,
        )
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(user.username, 'testuser2')
        self.assertEqual(user.email, 'testuser2@example.com')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'User2')
        self.assertEqual(user.role, 'ADMIN')
        self.assertEqual(user.phone, '0987654321')
        self.assertTrue(user.is_active)

    def test_str_representation(self):
        user = User.objects.create(
            username='JuanPerez',
            email='juanperez@example.com',
            password='testpassword',
            first_name='Juan',
            last_name='Perez',
            role='ADMIN',
        )
        expected = f'{user.first_name} {user.last_name} ({user.get_role_display()})'
        self.assertEqual(str(user), expected)

    def test_get_full_name_method(self):
        # probar metodo get_full_name
        user = User.objects.create(
            username='mariagonzalez',
            email='mariagonzalez@example.com',
            password='testpassword',
            first_name='Maria',
            last_name='Gonzalez',
            role='CLIENT',
        )
        expected_full_name = f'{user.first_name} {user.last_name}'
        self.assertEqual(user.get_full_name(), expected_full_name)

    def test_role_choices_validation(self):
        # verificar roles validos
        valid_roles = ['ADMIN', 'CONSULTANT', 'CLIENT']

        for role in valid_roles:
            user = User(
                username=f'user_{role.lower()}',
                email=f'user_{role.lower()}@example.com',
                password='testpassword',
                role=role,
            )
            try:
                user.full_clean()
            except ValidationError:
                self.fail(f"Role valido {role} lanzo ValidationError inesperadamente.")

        invalid_user = User(
            username='invalid_user',
            email='invalid_user@example.com',
            password='testpassword',
            role='INVALID',
        )

        with self.assertRaises(ValidationError):
            invalid_user.full_clean()

    def test_default_role_is_client(self):
        # role por defecto debe ser CLIENT
        user = User.objects.create(
            username='defaultrole',
            email='defaultrole@example.com',
            password='testpassword',
        )
        self.assertEqual(user.role, 'CLIENT')

    def test_unique_username_and_email(self):
        # username es unico; email puede repetirse en el modelo actual
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create(
                    username='testuser',
                    email='unique1@example.com',
                    password='testpassword',
                )

        duplicated_email_user = User.objects.create(
            username='uniqueuser',
            email='testuser@example.com',
            password='testpassword',
        )
        self.assertEqual(duplicated_email_user.email, 'testuser@example.com')
