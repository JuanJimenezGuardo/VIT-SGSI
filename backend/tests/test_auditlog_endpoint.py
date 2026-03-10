"""
Script para probar el endpoint GET /api/audit-logs/ (Checkpoint Dia 7).
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

# Crear cliente de prueba
client = Client()

# Obtener usuario admin
user = User.objects.filter(role='ADMIN').first()
if not user:
    print("❌ Error: No hay usuario admin")
    exit(1)

# Generar token JWT
refresh = RefreshToken.for_user(user)
access_token = str(refresh.access_token)

# Hacer request al endpoint de audit logs
response = client.get(
    '/api/audit-logs/',
    HTTP_AUTHORIZATION=f'Bearer {access_token}'
)

print(f"✅ GET /api/audit-logs/")
print(f"   Status Code: {response.status_code}")
print(f"   Response: {response.json()}")

if response.status_code == 200:
    data = response.json()
    if 'results' in data:
        logs = data['results']
    else:
        logs = data
    
    print(f"\n✅ Total de registros retornados: {len(logs)}")
    if logs:
        print(f"✅ Primer registro:")
        print(f"   - ID: {logs[0]['id']}")
        print(f"   - Usuario: {logs[0]['user_username']}")
        print(f"   - Acción: {logs[0]['action_display']}")
        print(f"   - Entidad: {logs[0]['entity_type']} #{logs[0]['entity_id']}")

    print("\n🎉 ENDPOINT /api/audit-logs/ funciona correctamente")
else:
    print(f"❌ Error: Código de estado {response.status_code}")
