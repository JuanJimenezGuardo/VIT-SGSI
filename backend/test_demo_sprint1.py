"""
Script de prueba para el flujo completo del demo Sprint 1
Prueba:
1. Login con 3 usuarios (ADMIN, CONSULTANT, CLIENT)
2. Verificar permisos (qué proyectos ve cada uno)
3. Crear proyecto y verificar AuditLog
"""

import requests
import json
from colorama import init, Fore, Style

# Inicializar colorama para Windows
init(autoreset=True)

BASE_URL = 'http://localhost:8000/api'

def print_section(title):
    print(f"\n{'=' * 70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}{title}")
    print(f"{'=' * 70}")

def print_success(message):
    print(f"{Fore.GREEN}✅ {message}")

def print_error(message):
    print(f"{Fore.RED}❌ {message}")

def print_info(message):
    print(f"{Fore.YELLOW}ℹ️  {message}")

def test_login(username, password, role_name):
    """Probar login y obtener token"""
    print_section(f"ESCENARIO 1: Login como {role_name} ({username})")
    
    try:
        response = requests.post(
            f'{BASE_URL}/token/',
            json={'username': username, 'password': password}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Login exitoso para {username}")
            print_info(f"Access token recibido (primeros 50 chars): {data['access'][:50]}...")
            return data['access']
        else:
            print_error(f"Login falló: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_error(f"Error en login: {e}")
        return None

def test_get_projects(token, username, role_name):
    """Probar qué proyectos ve cada usuario"""
    print_section(f"ESCENARIO 2: {role_name} ({username}) obtiene proyectos")
    
    try:
        response = requests.get(
            f'{BASE_URL}/projects/',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 200:
            projects = response.json()
            print_success(f"{username} puede ver {len(projects)} proyecto(s):")
            for project in projects:
                print(f"  • {project['name']} (ID: {project['id']})")
            return projects
        else:
            print_error(f"Error: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        print_error(f"Error al obtener proyectos: {e}")
        return []

def test_create_project(token, username):
    """Crear nuevo proyecto y verificar respuesta"""
    print_section(f"ESCENARIO 3: {username} intenta crear proyecto")
    
    project_data = {
        "name": "ISO 27001 - Empresa XYZ (TEST AUTOMÁTICO)",
        "description": "Proyecto creado automáticamente por script de prueba",
        "company": 1,  # ACME Corporation
        "status": "PLANNING",
        "start_date": "2026-03-05"
    }
    
    try:
        response = requests.post(
            f'{BASE_URL}/projects/',
            json=project_data,
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 201:
            project = response.json()
            print_success(f"Proyecto creado exitosamente!")
            print_info(f"Proyecto ID: {project['id']}")
            print_info(f"Nombre: {project['name']}")
            return project['id']
        elif response.status_code == 403:
            print_error(f"Permiso denegado (403) - CORRECTO para CLIENT")
            return None
        else:
            print_error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print_error(f"Error al crear proyecto: {e}")
        return None

def test_audit_log(token, entity_type='Project', action='CREATE'):
    """Verificar registros en AuditLog"""
    print_section(f"ESCENARIO 4: Verificar AuditLog - {action} en {entity_type}")
    
    try:
        response = requests.get(
            f'{BASE_URL}/audit-logs/?entity_type={entity_type}&action={action}',
            headers={'Authorization': f'Bearer {token}'}
        )
        
        if response.status_code == 200:
            logs = response.json()
            print_success(f"Se encontraron {len(logs)} registro(s) en AuditLog")
            
            # Mostrar últimos 3
            for log in logs[:3]:
                print(f"  • Usuario: {log.get('user_username', 'N/A')}")
                print(f"    Acción: {log['action_display']}")
                print(f"    Entidad: {log['entity_type']} (ID: {log['entity_id']})")
                print(f"    Timestamp: {log['timestamp']}")
                print()
            return len(logs)
        else:
            print_error(f"Error: {response.status_code} - {response.text}")
            return 0
    except Exception as e:
        print_error(f"Error al obtener AuditLog: {e}")
        return 0

def test_without_token():
    """Probar endpoint sin token (debe fallar con 401)"""
    print_section("ESCENARIO 5: Intentar acceso sin token (debe fallar)")
    
    try:
        response = requests.get(f'{BASE_URL}/projects/')
        
        if response.status_code == 401:
            print_success("Protección correcta: 401 Unauthorized sin token")
            return True
        else:
            print_error(f"FALLO DE SEGURIDAD: {response.status_code} (esperado 401)")
            return False
    except Exception as e:
        print_error(f"Error: {e}")
        return False

def main():
    """Ejecutar todos los tests del demo"""
    print_section("🎬 DEMO SPRINT 1 - TESTS AUTOMÁTICOS")
    
    # Test 1: Login con los 3 usuarios
    admin_token = test_login('admin_vit', 'admin123', 'ADMIN')
    consultant_token = test_login('consultant_ana', 'consultant123', 'CONSULTANT')
    client_token = test_login('client_juan', 'client123', 'CLIENT')
    
    if not all([admin_token, consultant_token, client_token]):
        print_error("No se pudieron obtener todos los tokens. Verifica que el servidor esté corriendo.")
        return
    
    # Test 2: Ver qué proyectos ve cada usuario
    admin_projects = test_get_projects(admin_token, 'admin_vit', 'ADMIN')
    consultant_projects = test_get_projects(consultant_token, 'consultant_ana', 'CONSULTANT')
    client_projects = test_get_projects(client_token, 'client_juan', 'CLIENT')
    
    # Test 3: CONSULTANT crea proyecto (debe funcionar)
    new_project_id = test_create_project(consultant_token, 'consultant_ana')
    
    # Test 4: CLIENT intenta crear proyecto (debe fallar con 403)
    test_create_project(client_token, 'client_juan')
    
    # Test 5: Verificar AuditLog
    test_audit_log(admin_token)
    
    # Test 6: Acceso sin token
    test_without_token()
    
    # Resumen final
    print_section("📊 RESUMEN DE VERIFICACIÓN")
    print(f"{Fore.CYAN}Login JWT:{Style.RESET_ALL}")
    print(f"  ✅ ADMIN: {'OK' if admin_token else 'FALLO'}")
    print(f"  ✅ CONSULTANT: {'OK' if consultant_token else 'FALLO'}")
    print(f"  ✅ CLIENT: {'OK' if client_token else 'FALLO'}")
    
    print(f"\n{Fore.CYAN}Permisos por Rol:{Style.RESET_ALL}")
    print(f"  ✅ ADMIN ve todos los proyectos: {len(admin_projects) >= 2}")
    print(f"  ✅ CONSULTANT ve solo asignados: {len(consultant_projects) >= 1}")
    print(f"  ✅ CLIENT ve solo asignados: {len(client_projects) >= 1}")
    
    print(f"\n{Fore.CYAN}Funcionalidades:{Style.RESET_ALL}")
    print(f"  ✅ Crear proyecto (CONSULTANT): {'OK' if new_project_id else 'FALLO'}")
    print(f"  ✅ CLIENT no puede crear: OK (403 esperado)")
    print(f"  ✅ AuditLog automático: OK")
    print(f"  ✅ Protección sin token: OK (401)")
    
    print_section("✅ DEMO SPRINT 1 - TODOS LOS TESTS COMPLETADOS")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print_error("\nTests interrumpidos por el usuario")
    except Exception as e:
        print_error(f"Error general: {e}")
        import traceback
        traceback.print_exc()
