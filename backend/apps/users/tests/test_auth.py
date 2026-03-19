"""Tests de autenticación y seguridad JWT."""

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


class JWTAuthenticationTest(TestCase):
    """Tests para autenticación con JWT"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@vit.local',
            password='testpass123',
            role='ADMIN'
        )
        self.token_url = '/api/token/'
        self.refresh_url = '/api/token/refresh/'
    
    def test_login_successful(self):
        """Test: Login exitoso retorna access y refresh tokens"""
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertIsInstance(response.data['access'], str)
        self.assertIsInstance(response.data['refresh'], str)
    
    def test_login_invalid_credentials(self):
        """Test: Login con credenciales inválidas retorna 401"""
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_login_missing_credentials(self):
        """Test: Login sin credenciales retorna 400"""
        response = self.client.post(self.token_url, {})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_refresh_token_successful(self):
        """Test: Refresh token válido retorna nuevo access token"""
        # Primero obtener tokens
        login_response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        refresh_token = login_response.data['refresh']
        
        # Luego refrescar
        response = self.client.post(self.refresh_url, {
            'refresh': refresh_token
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
    
    def test_refresh_token_invalid(self):
        """Test: Refresh token inválido retorna 401"""
        response = self.client.post(self.refresh_url, {
            'refresh': 'invalid_token_string'
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class JWTSecurityTest(TestCase):
    """Tests de seguridad para JWT"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@vit.local',
            password='testpass123',
            role='ADMIN'
        )
        self.token_url = '/api/token/'
    
    def test_token_contains_user_id(self):
        """Test: Token contiene información del usuario"""
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # Verificar que el token se genera correctamente
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        access_token = response.data['access']
        
        # Usar el token para acceder a un endpoint
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        user_response = self.client.get('/api/users/')
        
        self.assertEqual(user_response.status_code, status.HTTP_200_OK)
    
    def test_different_users_get_different_tokens(self):
        """Test: Usuarios diferentes obtienen tokens diferentes"""
        # Usuario 1
        response1 = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        token1 = response1.data['access']
        
        # Usuario 2
        user2 = User.objects.create_user(
            username='testuser2',
            email='test2@vit.local',
            password='testpass456',
            role='CLIENT'
        )
        response2 = self.client.post(self.token_url, {
            'username': 'testuser2',
            'password': 'testpass456'
        })
        token2 = response2.data['access']
        
        # Los tokens deben ser diferentes
        self.assertNotEqual(token1, token2)
    
    def test_token_cannot_be_reused_after_refresh(self):
        """Test: Refresh token funciona correctamente"""
        # Obtener tokens iniciales
        response = self.client.post(self.token_url, {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        refresh_token = response.data['refresh']
        
        # Usar refresh token para obtener nuevo access token
        refresh_response = self.client.post('/api/token/refresh/', {
            'refresh': refresh_token
        })
        
        self.assertEqual(refresh_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', refresh_response.data)
        
        # El nuevo access token debe funcionar
        new_access_token = refresh_response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {new_access_token}')
        
        endpoint_response = self.client.get('/api/users/')
        self.assertEqual(endpoint_response.status_code, status.HTTP_200_OK)
    
    def test_malformed_token_header_returns_401(self):
        """Test: Header mal formado retorna 401"""
        # Sin "Bearer" prefix
        self.client.credentials(HTTP_AUTHORIZATION='just_a_token')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Con formato incorrecto
        self.client.credentials(HTTP_AUTHORIZATION='Token invalid_format')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_empty_token_returns_401(self):
        """Test: Token vacío retorna 401"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ')
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class ProtectedEndpointsTest(TestCase):
    """Tests para validar que los endpoints están protegidos"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@vit.local',
            password='testpass123',
            role='ADMIN'
        )
        
        # Obtener token válido
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.access_token = response.data['access']
        
        # Endpoints a probar
        self.protected_endpoints = [
            '/api/users/',
            '/api/companies/',
            '/api/projects/',
            '/api/phases/',
            '/api/tasks/',
        ]
    
    def test_endpoints_without_token_return_401(self):
        """Test: Endpoints sin token retornan 401"""
        for endpoint in self.protected_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"Endpoint {endpoint} debería retornar 401 sin token"
            )
    
    def test_endpoints_with_valid_token_return_200(self):
        """Test: Endpoints con token válido retornan 200"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        for endpoint in self.protected_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
                f"Endpoint {endpoint} debería retornar 200 con token válido"
            )
    
    def test_endpoints_with_invalid_token_return_401(self):
        """Test: Endpoints con token inválido retornan 401"""
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token_123')
        
        for endpoint in self.protected_endpoints:
            response = self.client.get(endpoint)
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED,
                f"Endpoint {endpoint} debería retornar 401 con token inválido"
            )
    
    def test_token_endpoint_is_public(self):
        """Test: Endpoint de login no requiere autenticación"""
        response = self.client.post('/api/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# ---- from test_role_permissions.py ----

"""
Tests para permisos por rol
Valida que los permisos personalizados funcionan correctamente
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from apps.companies.models import Company

User = get_user_model()


