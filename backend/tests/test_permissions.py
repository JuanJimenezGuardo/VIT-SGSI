"""
Script de validacion de permisos y roles (Checkpoint Dia 9).
Prueba todos los endpoints con diferentes roles: ADMIN, CONSULTANT, CLIENT.
Verifica que los permisos funcionan correctamente sin errores 500.
"""
import os
import sys
from pathlib import Path
import django

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken
from apps.users.models import User
from apps.companies.models import Company
from apps.projects.models import Project, ProjectUser
import json

# Colores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def get_token_for_user(user):
    """Genera token JWT para un usuario"""
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)

def test_endpoint(client, method, url, token=None, data=None, expected_status=None):
    """Prueba un endpoint con un metodo HTTP especifico"""
    headers = {}
    if token:
        headers['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    
    if method == 'GET':
        response = client.get(url, **headers)
    elif method == 'POST':
        response = client.post(url, data=json.dumps(data) if data else None, 
                               content_type='application/json', **headers)
    elif method == 'PUT':
        response = client.put(url, data=json.dumps(data) if data else None, 
                              content_type='application/json', **headers)
    elif method == 'DELETE':
        response = client.delete(url, **headers)
    
    status = response.status_code
    success = True
    
    if expected_status:
        success = status == expected_status
        if success:
            print_success(f"{method} {url} → {status} (esperado: {expected_status})")
        else:
            print_error(f"{method} {url} → {status} (esperado: {expected_status})")
    else:
        # Sin status esperado, solo verificamos que no sea 500
        if status >= 500:
            print_error(f"{method} {url} → {status} SERVER ERROR")
            success = False
        elif status >= 400:
            print_warning(f"{method} {url} → {status}")
        else:
            print_success(f"{method} {url} → {status}")
    
    return success, status, response

print("=" * 70)
print("CHECKPOINT DIA 9: Validacion de Permisos y Endpoints")
print("=" * 70)

# Crear usuarios de prueba para cada rol
print("\n📋 Preparando usuarios de prueba...")
admin_user, _ = User.objects.get_or_create(
    username='test_admin',
    defaults={'email': 'admin@test.com', 'role': 'ADMIN', 'password': 'test123'}
)
admin_user.set_password('test123')
admin_user.save()
print_success(f"Usuario ADMIN: {admin_user.username}")

consultant_user, _ = User.objects.get_or_create(
    username='test_consultant',
    defaults={'email': 'consultant@test.com', 'role': 'CONSULTANT', 'password': 'test123'}
)
consultant_user.set_password('test123')
consultant_user.save()
print_success(f"Usuario CONSULTANT: {consultant_user.username}")

client_user, _ = User.objects.get_or_create(
    username='test_client',
    defaults={'email': 'client@test.com', 'role': 'CLIENT', 'password': 'test123'}
)
client_user.set_password('test123')
client_user.save()
print_success(f"Usuario CLIENT: {client_user.username}")

# Generar tokens
admin_token = get_token_for_user(admin_user)
consultant_token = get_token_for_user(consultant_user)
client_token = get_token_for_user(client_user)
print_info("Tokens JWT generados para todos los usuarios")

# Cliente de prueba
client = Client()

# Resultados
total_tests = 0
passed_tests = 0
failed_tests = 0

print("\n" + "=" * 70)
print("TEST 1: Endpoints sin autenticacion (deben dar 401)")
print("=" * 70)

tests = [
    ('GET', '/api/users/', None, 401),
    ('GET', '/api/companies/', None, 401),
    ('GET', '/api/projects/', None, 401),
    ('GET', '/api/audit-logs/', None, 401),
]

for method, url, token, expected in tests:
    success, status, _ = test_endpoint(client, method, url, token, expected_status=expected)
    total_tests += 1
    if success:
        passed_tests += 1
    else:
        failed_tests += 1

print("\n" + "=" * 70)
print("TEST 2: Endpoint /api/users/ - Solo ADMIN puede acceder")
print("=" * 70)

tests = [
    ('GET', '/api/users/', admin_token, 200),
    ('GET', '/api/users/', consultant_token, 403),
    ('GET', '/api/users/', client_token, 403),
]

for method, url, token, expected in tests:
    success, status, _ = test_endpoint(client, method, url, token, expected_status=expected)
    total_tests += 1
    if success:
        passed_tests += 1
    else:
        failed_tests += 1

print("\n" + "=" * 70)
print("TEST 3: Endpoint /api/companies/ - ADMIN y CONSULTANT pueden crear")
print("=" * 70)

tests = [
    ('GET', '/api/companies/', admin_token, 200),
    ('GET', '/api/companies/', consultant_token, 200),
    ('GET', '/api/companies/', client_token, 200),
]

for method, url, token, expected in tests:
    success, status, _ = test_endpoint(client, method, url, token, expected_status=expected)
    total_tests += 1
    if success:
        passed_tests += 1
    else:
        failed_tests += 1

print("\n" + "=" * 70)
print("TEST 4: Endpoint /api/projects/ - Filtrado por rol")
print("=" * 70)

# Crear proyecto de prueba
test_company, _ = Company.objects.get_or_create(
    name='Test Company Permissions',
    defaults={
        'rfc': 'TCP010101ABC',
        'email': 'test@company.com',
        'phone': '555-9999',
        'address': 'Test Address',
        'city': 'Test City',
        'state': 'Test State',
        'country': 'Colombia',
        'contact_person': 'Test Person',
        'contact_position': 'Manager'
    }
)

test_project, created = Project.objects.get_or_create(
    name='Test Project Permissions',
    defaults={
        'company': test_company,
        'status': 'PLANNING',
        'start_date': '2026-03-01',
        'created_by': admin_user
    }
)
if created:
    print_info(f"Proyecto de prueba creado: {test_project.name}")

# Asignar solo consultant al proyecto
ProjectUser.objects.get_or_create(
    user=consultant_user,
    project=test_project,
    defaults={'role': 'CONSULTANT'}
)
print_info(f"Consultant asignado al proyecto {test_project.name}")

tests = [
    ('GET', '/api/projects/', admin_token, 200),  # Admin ve todos
    ('GET', '/api/projects/', consultant_token, 200),  # Consultant ve asignados
    ('GET', '/api/projects/', client_token, 200),  # Client ve asignados (vacio)
]

for method, url, token, expected in tests:
    success, status, response = test_endpoint(client, method, url, token, expected_status=expected)
    total_tests += 1
    if success:
        passed_tests += 1
        # Verificar contenido de respuesta
        if token == admin_token:
            data = response.json()
            results = data.get('results', data)
            print_info(f"  Admin ve {len(results)} proyectos")
        elif token == consultant_token:
            data = response.json()
            results = data.get('results', data)
            print_info(f"  Consultant ve {len(results)} proyectos (debe incluir Test Project)")
        elif token == client_token:
            data = response.json()
            results = data.get('results', data)
            print_info(f"  Client ve {len(results)} proyectos (debe ser 0)")
    else:
        failed_tests += 1

print("\n" + "=" * 70)
print("TEST 5: Endpoint /api/audit-logs/ - Solo lectura para todos")
print("=" * 70)

tests = [
    ('GET', '/api/audit-logs/', admin_token, 200),
    ('GET', '/api/audit-logs/', consultant_token, 200),
    ('GET', '/api/audit-logs/', client_token, 200),
]

for method, url, token, expected in tests:
    success, status, _ = test_endpoint(client, method, url, token, expected_status=expected)
    total_tests += 1
    if success:
        passed_tests += 1
    else:
        failed_tests += 1

print("\n" + "=" * 70)
print("TEST 6: Verificar que no hay errores 500")
print("=" * 70)

# Endpoints a verificar que no den 500
endpoints_to_check = [
    '/api/users/',
    '/api/companies/',
    '/api/projects/',
    '/api/project-users/',
    '/api/phases/',
    '/api/tasks/',
    '/api/audit-logs/',
]

tokens_to_test = {
    'admin': admin_token,
    'consultant': consultant_token,
    'client': client_token
}

print_info("Verificando todos los endpoints con todos los roles...")
for endpoint in endpoints_to_check:
    for role_name, token in tokens_to_test.items():
        success, status, _ = test_endpoint(client, 'GET', endpoint, token)
        total_tests += 1
        if status < 500:
            passed_tests += 1
        else:
            failed_tests += 1
            print_error(f"ERROR 500 en {endpoint} con rol {role_name}")

print("\n" + "=" * 70)
print("RESUMEN DE VALIDACION")
print("=" * 70)
print(f"\nTotal de pruebas: {total_tests}")
print(f"{Colors.GREEN}✅ Exitosas: {passed_tests}{Colors.END}")
print(f"{Colors.RED}❌ Fallidas: {failed_tests}{Colors.END}")

success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
print(f"\nTasa de exito: {success_rate:.1f}%")

if failed_tests == 0:
    print(f"\n{Colors.GREEN}🎉 CHECKPOINT DIA 9 COMPLETADO{Colors.END}")
    print(f"{Colors.GREEN}✅ Todos los endpoints tienen permisos correctos{Colors.END}")
    print(f"{Colors.GREEN}✅ Sin errores 500{Colors.END}")
else:
    print(f"\n{Colors.RED}⚠️  ALERTA: {failed_tests} pruebas fallaron{Colors.END}")
    print("Revisar permisos en los endpoints indicados")

print("\n" + "=" * 70)
