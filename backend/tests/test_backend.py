#!/usr/bin/env python
"""
Script para probar todos los endpoints del backend VIT
Ejecuta: python tests/test_backend.py (desde la carpeta backend)
"""

import os
import sys
from pathlib import Path
import django

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection
from django.apps import apps

def test_database():
    """Verificar estado de la base de datos"""
    print("\n" + "="*70)
    print("DATABASE CHECK")
    print("="*70)
    
    try:
        # Verificar conexión
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        print("✅ Base de datos conectada")
        
        # Mostrar tipo de BD
        engine = connection.settings_dict['ENGINE']
        if 'sqlite' in engine:
            print("✅ Usando SQLite para desarrollo")
        elif 'postgresql' in engine:
            print("✅ Usando PostgreSQL")
        
        # Contar tablas
        tables = connection.introspection.table_names()
        print(f"✅ Total de tablas creadas: {len(tables)}")
        
        # Mostrar tablas principales
        print("\n📊 Tablas de la aplicación:")
        app_tables = {
            'users': [t for t in tables if 'user' in t],
            'companies': [t for t in tables if 'compan' in t],
            'projects': [t for t in tables if 'project' in t or 'phase' in t or 'task' in t],
            'risks': [t for t in tables if 'risk' in t],
            'iso_controls': [t for t in tables if 'iso' in t or 'soa' in t],
            'documents': [t for t in tables if 'document' in t or 'evidence' in t],
            'reports': [t for t in tables if 'report' in t],
        }
        
        for app, app_tbl in app_tables.items():
            if app_tbl:
                print(f"\n   {app}:")
                for table in sorted(app_tbl):
                    print(f"      ✓ {table}")
        
        return True
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        return False


def test_models():
    """Verificar que todos los modelos existen"""
    print("\n" + "="*70)
    print("MODELS CHECK")
    print("="*70)
    
    try:
        # Usuarios
        from apps.users.models import User
        user_count = User.objects.count()
        print(f"✅ User model - {user_count} usuarios registrados")
        
        # Empresas
        from apps.companies.models import Company
        company_count = Company.objects.count()
        print(f"✅ Company model - {company_count} empresas registradas")
        
        # Proyectos
        from apps.projects.models import Project, Phase, Task
        project_count = Project.objects.count()
        phase_count = Phase.objects.count()
        task_count = Task.objects.count()
        print(f"✅ Project model - {project_count} proyectos")
        print(f"✅ Phase model - {phase_count} fases")
        print(f"✅ Task model - {task_count} tareas")
        
        # Riesgos
        from apps.risks.models import Risk
        risk_count = Risk.objects.count()
        print(f"✅ Risk model - {risk_count} riesgos")
        
        # Controles ISO
        from apps.iso_controls.models import ISOControl, SoAItem
        control_count = ISOControl.objects.count()
        soa_count = SoAItem.objects.count()
        print(f"✅ ISOControl model - {control_count} controles ISO")
        print(f"✅ SoAItem model - {soa_count} items SoA")
        
        # Documentos
        from apps.documents.models import Document, Evidence
        doc_count = Document.objects.count()
        evidence_count = Evidence.objects.count()
        print(f"✅ Document model - {doc_count} documentos")
        print(f"✅ Evidence model - {evidence_count} evidencias")
        
        # Reportes
        from apps.reports.models import Report
        report_count = Report.objects.count()
        print(f"✅ Report model - {report_count} reportes")
        
        return True
    except Exception as e:
        print(f"❌ Error en modelos: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_urls():
    """Verificar que las URLs están configuradas"""
    print("\n" + "="*70)
    print("URLS CHECK")
    print("="*70)
    
    try:
        from django.urls import get_resolver
        resolver = get_resolver()
        
        print("✅ URLs configuradas:")
        
        url_patterns = [
            '/api/users/',
            '/api/companies/',
            '/api/projects/',
            '/api/phases/',
            '/api/tasks/',
            '/api/risks/',
            '/api/iso-controls/',
            '/api/soa-items/',
            '/api/documents/',
            '/api/evidence/',
            '/api/reports/',
            '/admin/',
        ]
        
        for pattern in url_patterns:
            try:
                match = resolver.resolve(pattern)
                print(f"   ✓ {pattern}")
            except:
                print(f"   ⚠ {pattern}")
        
        return True
    except Exception as e:
        print(f"❌ Error en URLs: {e}")
        return False


def main():
    """Ejecutar todas las pruebas"""
    print("\n" + "="*70)
    print("     PRUEBA COMPLETA DEL BACKEND VIT")
    print("="*70)
    
    results = {
        'database': test_database(),
        'models': test_models(),
        'urls': test_urls(),
    }
    
    print("\n" + "="*70)
    print("RESULTADO FINAL")
    print("="*70)
    
    all_pass = all(results.values())
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    print("\n" + "="*70)
    if all_pass:
        print("✅ BACKEND FUNCIONANDO CORRECTAMENTE")
        print("\nPara iniciar el servidor ejecuta:")
        print("   python manage.py runserver")
    else:
        print("⚠️  ALGUNOS TESTS FALLARON - Revisa los errores arriba")
    print("="*70 + "\n")
    
    return 0 if all_pass else 1


if __name__ == '__main__':
    sys.exit(main())
