"""
Script para poblar datos de prueba para demo Sprint 1
Crea:
- 3 usuarios (ADMIN, CONSULTANT, CLIENT)
- 2 empresas
- 2 proyectos
- Asignaciones ProjectUser
"""

import os
import sys
import django
from datetime import date, timedelta
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.users.models import User
from apps.companies.models import Company
from apps.projects.models import Project, ProjectUser


def populate_demo_data():
    print("=" * 60)
    print("POBLANDO DATOS DE PRUEBA PARA DEMO SPRINT 1")
    print("=" * 60)
    
    # Paso 1: Crear usuarios
    print("\n📌 PASO 1: Creando usuarios...")
    
    # Usuario ADMIN
    admin_user, created = User.objects.get_or_create(
        username='admin_vit',
        defaults={
            'email': 'admin@vit.com',
            'first_name': 'Carlos',
            'last_name': 'Rodriguez',
            'role': 'ADMIN',
            'phone': '+57 300 1234567',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"  ✅ Creado: {admin_user.username} (ADMIN)")
    else:
        print(f"  ℹ️  Ya existe: {admin_user.username} (ADMIN)")
    
    # Usuario CONSULTANT
    consultant_user, created = User.objects.get_or_create(
        username='consultant_ana',
        defaults={
            'email': 'ana.martinez@vit.com',
            'first_name': 'Ana',
            'last_name': 'Martinez',
            'role': 'CONSULTANT',
            'phone': '+57 300 2345678',
            'is_staff': False
        }
    )
    if created:
        consultant_user.set_password('consultant123')
        consultant_user.save()
        print(f"  ✅ Creado: {consultant_user.username} (CONSULTANT)")
    else:
        print(f"  ℹ️  Ya existe: {consultant_user.username} (CONSULTANT)")
    
    # Usuario CLIENT
    client_user, created = User.objects.get_or_create(
        username='client_juan',
        defaults={
            'email': 'juan.perez@acme.com',
            'first_name': 'Juan',
            'last_name': 'Perez',
            'role': 'CLIENT',
            'phone': '+57 300 3456789',
            'is_staff': False
        }
    )
    if created:
        client_user.set_password('client123')
        client_user.save()
        print(f"  ✅ Creado: {client_user.username} (CLIENT)")
    else:
        print(f"  ℹ️  Ya existe: {client_user.username} (CLIENT)")
    
    # Paso 2: Crear empresas
    print("\n📌 PASO 2: Creando empresas...")
    
    company1, created = Company.objects.get_or_create(
        rfc='ACM123456AB1',
        defaults={
            'name': 'ACME Corporation',
            'email': 'contacto@acme.com',
            'phone': '+57 601 7654321',
            'address': 'Calle 100 #50-25, Edificio Torre Empresarial',
            'city': 'Bogotá',
            'state': 'Cundinamarca',
            'country': 'Colombia',
            'contact_person': 'Juan Perez',
            'contact_position': 'CTO'
        }
    )
    if created:
        print(f"  ✅ Creada: {company1.name}")
    else:
        print(f"  ℹ️  Ya existe: {company1.name}")
    
    company2, created = Company.objects.get_or_create(
        rfc='BCO789012CD2',
        defaults={
            'name': 'Bancolombia ISO Project',
            'email': 'seguridad@bancolombia.com',
            'phone': '+57 604 5555555',
            'address': 'Carrera 48 #26-85',
            'city': 'Medellín',
            'state': 'Antioquia',
            'country': 'Colombia',
            'contact_person': 'María González',
            'contact_position': 'CISO'
        }
    )
    if created:
        print(f"  ✅ Creada: {company2.name}")
    else:
        print(f"  ℹ️  Ya existe: {company2.name}")
    
    # Paso 3: Crear proyectos
    print("\n📌 PASO 3: Creando proyectos...")
    
    project1, created = Project.objects.get_or_create(
        name='Implementación ISO 27001 - ACME',
        defaults={
            'description': 'Proyecto de implementación completa de SGSI según ISO 27001 para ACME Corporation. Incluye análisis de riesgos, definición de controles, y certificación.',
            'company': company1,
            'status': 'IN_PROGRESS',
            'start_date': date.today() - timedelta(days=30),
            'end_date': date.today() + timedelta(days=150),
            'created_by': consultant_user
        }
    )
    if created:
        print(f"  ✅ Creado: {project1.name} (empresa: {project1.company.name})")
    else:
        print(f"  ℹ️  Ya existe: {project1.name}")
    
    project2, created = Project.objects.get_or_create(
        name='Auditoría ISO 27001 - Bancolombia',
        defaults={
            'description': 'Auditoría de cumplimiento ISO 27001 y mejora continua del SGSI existente. Revisión de controles implementados y GAP analysis.',
            'company': company2,
            'status': 'PLANNING',
            'start_date': date.today() + timedelta(days=15),
            'end_date': date.today() + timedelta(days=180),
            'created_by': admin_user
        }
    )
    if created:
        print(f"  ✅ Creado: {project2.name} (empresa: {project2.company.name})")
    else:
        print(f"  ℹ️  Ya existe: {project2.name}")
    
    # Paso 4: Crear asignaciones ProjectUser
    print("\n📌 PASO 4: Creando asignaciones ProjectUser...")
    
    # CONSULTANT asignado a Proyecto 1 (ACME)
    pu1, created = ProjectUser.objects.get_or_create(
        project=project1,
        user=consultant_user,
        defaults={'role': 'CONSULTANT'}
    )
    if created:
        print(f"  ✅ Asignado: {consultant_user.username} → {project1.name} (CONSULTANT)")
    else:
        print(f"  ℹ️  Ya asignado: {consultant_user.username} → {project1.name}")
    
    # CLIENT asignado a Proyecto 1 (ACME) - es el cliente de ACME
    pu2, created = ProjectUser.objects.get_or_create(
        project=project1,
        user=client_user,
        defaults={'role': 'CLIENT'}
    )
    if created:
        print(f"  ✅ Asignado: {client_user.username} → {project1.name} (CLIENT)")
    else:
        print(f"  ℹ️  Ya asignado: {client_user.username} → {project1.name}")
    
    # ADMIN asignado a Proyecto 2 (Bancolombia) como ADMIN del proyecto
    pu3, created = ProjectUser.objects.get_or_create(
        project=project2,
        user=admin_user,
        defaults={'role': 'ADMIN'}
    )
    if created:
        print(f"  ✅ Asignado: {admin_user.username} → {project2.name} (ADMIN)")
    else:
        print(f"  ℹ️  Ya asignado: {admin_user.username} → {project2.name}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print("✅ DATOS DE PRUEBA POBLADOS EXITOSAMENTE")
    print("=" * 60)
    print("\n📊 RESUMEN:")
    print(f"  • Usuarios creados: {User.objects.count()}")
    print(f"  • Empresas creadas: {Company.objects.count()}")
    print(f"  • Proyectos creados: {Project.objects.count()}")
    print(f"  • Asignaciones ProjectUser: {ProjectUser.objects.count()}")
    
    print("\n🔐 CREDENCIALES PARA DEMO:")
    print("-" * 60)
    print(f"  ADMIN:")
    print(f"    Username: admin_vit")
    print(f"    Password: admin123")
    print(f"    → Debe ver AMBOS proyectos")
    print()
    print(f"  CONSULTANT:")
    print(f"    Username: consultant_ana")
    print(f"    Password: consultant123")
    print(f"    → Solo ve: {project1.name}")
    print()
    print(f"  CLIENT:")
    print(f"    Username: client_juan")
    print(f"    Password: client123")
    print(f"    → Solo ve: {project1.name} (como cliente)")
    print("-" * 60)
    
    print("\n💡 LISTO PARA DEMO:")
    print("  1. Probar login con cada usuario")
    print("  2. Verificar que cada rol ve los proyectos correctos")
    print("  3. Crear nuevo proyecto → verificar AuditLog")
    

if __name__ == '__main__':
    try:
        populate_demo_data()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
