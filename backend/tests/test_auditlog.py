"""
Script para probar el modelo AuditLog manualmente (Checkpoint Dia 7).
Crea un registro de auditoria y verifica que se puede leer.
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

from apps.users.models import User, AuditLog
from apps.projects.models import Project

# Obtener o crear un usuario para la prueba
user = User.objects.filter(role='ADMIN').first()
if not user:
    user = User.objects.create_user(
        username='testadmin',
        email='admin@test.com',
        password='testpass123',
        role='ADMIN'
    )
    print(f"✅ Usuario creado: {user.username}")
else:
    print(f"✅ Usuario encontrado: {user.username}")

# Crear un registro de auditoria manual
audit = AuditLog.objects.create(
    user=user,
    action='CREATE',
    entity_type='Project',
    entity_id=1,
    changes={'name': 'Proyecto ISO 27001 ACME', 'status': 'active'}
)

print(f"\n✅ AuditLog creado exitosamente:")
print(f"   - ID: {audit.id}")
print(f"   - Usuario: {audit.user.username}")
print(f"   - Acción: {audit.get_action_display()}")
print(f"   - Entidad: {audit.entity_type} #{audit.entity_id}")
print(f"   - Timestamp: {audit.timestamp}")
print(f"   - Cambios: {audit.changes}")

# Verificar que se puede consultar
all_logs = AuditLog.objects.all()
print(f"\n✅ Total de registros de auditoría en BD: {all_logs.count()}")

# Filtrar por usuario
user_logs = AuditLog.objects.filter(user=user)
print(f"✅ Registros del usuario {user.username}: {user_logs.count()}")

# Filtrar por tipo de entidad
project_logs = AuditLog.objects.filter(entity_type='Project')
print(f"✅ Registros de tipo Project: {project_logs.count()}")

print("\n🎉 CHECKPOINT DÍA 7 COMPLETADO: Modelo AuditLog funciona correctamente")
