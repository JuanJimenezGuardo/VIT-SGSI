"""
Script para probar signals de AuditLog (Checkpoint Dia 8).
Crea un proyecto y verifica que aparece automaticamente en AuditLog.
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
from apps.companies.models import Company
from apps.projects.models import Project, ProjectUser
from apps.phases.models import Phase
from apps.tasks.models import Task
from datetime import date, datetime

print("=" * 60)
print("CHECKPOINT DIA 8: Probar Signals de AuditLog")
print("=" * 60)

# Obtener usuario admin
admin_user = User.objects.filter(role='ADMIN').first()
if not admin_user:
    print("❌ Error: No hay usuario admin")
    exit(1)

print(f"\n✅ Usuario admin encontrado: {admin_user.username}")

# Obtener o crear empresa
company, created = Company.objects.get_or_create(
    name='Test Company ACME',
    defaults={
        'rfc': 'TCM010101ABC',
        'email': 'contact@acme.com',
        'phone': '555-0100',
        'address': 'Test Address 123',
        'city': 'Bogota',
        'state': 'Cundinamarca',
        'country': 'Colombia',
        'contact_person': 'John Doe',
        'contact_position': 'CEO'
    }
)
print(f"✅ Empresa: {company.name} {'(creada)' if created else '(existente)'}")

# Contar registros actuales en AuditLog
initial_count = AuditLog.objects.count()
print(f"\n📊 Registros en AuditLog antes: {initial_count}")

# TEST 1: Crear un proyecto (debe disparar signal post_save)
print("\n🔔 TEST 1: Crear proyecto...")
project = Project.objects.create(
    name='Proyecto ISO 27001 Test Signals',
    description='Proyecto de prueba para validar signals',
    company=company,
    status='PLANNING',
    start_date=date.today(),
    created_by=admin_user
)
print(f"✅ Proyecto creado: {project.name} (ID: {project.id})")

# Verificar que aparecio en AuditLog
project_logs = AuditLog.objects.filter(entity_type='Project', entity_id=project.id)
if project_logs.exists():
    log = project_logs.first()
    print(f"✅ AuditLog generado automaticamente:")
    print(f"   - Accion: {log.get_action_display()}")
    print(f"   - Usuario: {log.user.username if log.user else 'Sistema'}")
    print(f"   - Timestamp: {log.timestamp}")
    print(f"   - Cambios: {log.changes}")
else:
    print("❌ ERROR: No se genero AuditLog para el proyecto")

# TEST 2: Crear una fase (debe disparar signal post_save)
print("\n🔔 TEST 2: Crear fase...")
phase = Phase.objects.create(
    project=project,
    name='Fase de Evaluacion',
    type='ASSESSMENT',
    description='Fase de prueba',
    start_date=datetime.now(),
    order=1
)
print(f"✅ Fase creada: {phase.name} (ID: {phase.id})")

phase_logs = AuditLog.objects.filter(entity_type='Phase', entity_id=phase.id)
if phase_logs.exists():
    log = phase_logs.first()
    print(f"✅ AuditLog para Phase generado:")
    print(f"   - Accion: {log.get_action_display()}")
    print(f"   - Usuario: {log.user.username if log.user else 'Sistema'}")
else:
    print("❌ ERROR: No se genero AuditLog para la fase")

# TEST 3: Crear una tarea (debe disparar signal post_save)
print("\n🔔 TEST 3: Crear tarea...")
task = Task.objects.create(
    phase=phase,
    name='Tarea de prueba signals',
    description='Validar que se registre en AuditLog',
    assigned_to=admin_user,
    priority='HIGH',
    status='PENDING',
    due_date=date.today()
)
print(f"✅ Tarea creada: {task.name} (ID: {task.id})")

task_logs = AuditLog.objects.filter(entity_type='Task', entity_id=task.id)
if task_logs.exists():
    log = task_logs.first()
    print(f"✅ AuditLog para Task generado:")
    print(f"   - Accion: {log.get_action_display()}")
    print(f"   - Usuario: {log.user.username if log.user else 'Sistema'}")
else:
    print("❌ ERROR: No se genero AuditLog para la tarea")

# TEST 4: Actualizar proyecto (debe disparar signal post_save con UPDATE)
print("\n🔔 TEST 4: Actualizar proyecto...")
project.status = 'IN_PROGRESS'
project.save()
print(f"✅ Proyecto actualizado: status = {project.status}")

update_logs = AuditLog.objects.filter(
    entity_type='Project', 
    entity_id=project.id,
    action='UPDATE'
)
if update_logs.exists():
    log = update_logs.first()
    print(f"✅ AuditLog de UPDATE generado:")
    print(f"   - Accion: {log.get_action_display()}")
    print(f"   - Cambios: {log.changes}")
else:
    print("❌ ERROR: No se genero AuditLog para actualizacion")

# TEST 5: Crear ProjectUser (debe disparar signal)
print("\n🔔 TEST 5: Asignar usuario a proyecto...")
project_user = ProjectUser.objects.create(
    user=admin_user,
    project=project,
    role='CONSULTANT'
)
print(f"✅ ProjectUser creado: {admin_user.username} -> {project.name}")

pu_logs = AuditLog.objects.filter(entity_type='ProjectUser', entity_id=project_user.id)
if pu_logs.exists():
    log = pu_logs.first()
    print(f"✅ AuditLog para ProjectUser generado:")
    print(f"   - Accion: {log.get_action_display()}")
    print(f"   - Cambios: {log.changes}")
else:
    print("❌ ERROR: No se genero AuditLog para ProjectUser")

# Resumen final
final_count = AuditLog.objects.count()
new_logs = final_count - initial_count
print("\n" + "=" * 60)
print(f"📊 Registros en AuditLog despues: {final_count}")
print(f"📈 Nuevos registros generados: {new_logs}")
print("=" * 60)

if new_logs >= 5:  # Deberíamos tener al menos 5: create project, create phase, create task, update project, create projectuser
    print("\n🎉 CHECKPOINT DIA 8 COMPLETADO: Signals funcionan correctamente")
    print("✅ Los cambios en Project, Phase, Task y ProjectUser se registran automaticamente en AuditLog")
else:
    print(f"\n⚠️  ALERTA: Se esperaban al menos 5 registros, solo se generaron {new_logs}")

# Mostrar ultimos 5 registros
print("\n📋 Ultimos 5 registros en AuditLog:")
for log in AuditLog.objects.order_by('-timestamp')[:5]:
    print(f"   - {log}")
