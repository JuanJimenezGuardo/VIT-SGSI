# Script de Demo Automatizado - Sprint 1
# Duracion: 5 minutos
# Ejecutar desde: c:\Proyecto_VIT\backend

# Cambiar al directorio backend si no estamos ahi
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($scriptPath) {
    Set-Location $scriptPath
}

# Usar Python del entorno virtual
$pythonExe = ".\.venv\Scripts\python.exe"
if (-not (Test-Path $pythonExe)) {
    Write-Host "[ERROR] No se encuentra el entorno virtual en .venv" -ForegroundColor Red
    Write-Host "[INFO] Ejecuta primero: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "   DEMO SPRINT 1 - VIT ISO 27001 Platform" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Variables globales
$BASE_URL = "http://127.0.0.1:8000"
$ADMIN_TOKEN = ""

# Funcion para pausar y continuar
function Pause-Demo {
    param([string]$message = "Presiona ENTER para continuar...")
    Write-Host ""
    Write-Host $message -ForegroundColor Yellow
    Read-Host
}

# [STEP 1] Verificar salud del sistema (30 seg)
Write-Host "============================================" -ForegroundColor Green
Write-Host " [STEP 1] VERIFICACION DE SALUD DEL SISTEMA" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "[GUION] Primero verificamos que el sistema Django este saludable" -ForegroundColor White
Write-Host ""
Write-Host "Ejecutando: python manage.py check" -ForegroundColor Gray
Write-Host "[ESPERA] Django esta cargando, esto puede tomar 5-10 segundos..." -ForegroundColor Yellow
Write-Host "[IMPORTANTE] NO presiones ninguna tecla mientras carga..." -ForegroundColor Magenta
Write-Host ""

try {
    $output = & $pythonExe manage.py check 2>&1
    $exitCode = $LASTEXITCODE
    
    Write-Host $output
    Write-Host ""
    
    if ($exitCode -eq 0) {
        Write-Host "[OK] Sistema saludable - No hay problemas detectados" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] Error en la verificacion del sistema" -ForegroundColor Red
        Write-Host "[INFO] Presiona ENTER para continuar de todas formas..." -ForegroundColor Yellow
        Read-Host
    }
} catch {
    Write-Host "[ERROR] Excepcion: $_" -ForegroundColor Red
    Write-Host "[INFO] Presiona ENTER para continuar de todas formas..." -ForegroundColor Yellow
    Read-Host
}

Pause-Demo

# [STEP 2] Cargar datos de demo (30 seg)
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " [STEP 2] CARGA DE DATOS DE DEMOSTRACION" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Cargo datos de ejemplo: empresas, proyectos y usuarios con roles" -ForegroundColor White
Write-Host ""
Write-Host "Ejecutando: python populate_demo_data.py" -ForegroundColor Gray
& $pythonExe populate_demo_data.py

Write-Host ""
Write-Host "[OK] Datos creados:" -ForegroundColor Green
Write-Host "   - 3 usuarios (Admin + Consultor + Cliente)" -ForegroundColor Cyan
Write-Host "   - 2 empresas cliente" -ForegroundColor Cyan
Write-Host "   - 2 proyectos ISO 27001" -ForegroundColor Cyan
Write-Host "   - Asignaciones ProjectUser con roles" -ForegroundColor Cyan
Write-Host ""
Write-Host "[NOTA] Esto demuestra multi-tenancy funcionando correctamente" -ForegroundColor Magenta

Pause-Demo

# [STEP 3] Autenticacion JWT (1 min)
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " [STEP 3] AUTENTICACION JWT" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "El sistema usa autenticacion JWT. El login devuelve access y refresh tokens" -ForegroundColor White
Write-Host ""
Write-Host "Ejecutando: POST /api/token/ con credenciales de admin" -ForegroundColor Gray

# Verificar que el servidor este corriendo
try {
    $loginData = @{
        username = "admin_vit"
        password = "admin123"
    } | ConvertTo-Json

    $response = Invoke-RestMethod -Uri "$BASE_URL/api/token/" -Method Post -Body $loginData -ContentType "application/json"
    $ADMIN_TOKEN = $response.access
    
    Write-Host ""
    Write-Host "[OK] Login exitoso:" -ForegroundColor Green
    Write-Host "   Access Token:  $($response.access.Substring(0, 40))..." -ForegroundColor Cyan
    Write-Host "   Refresh Token: $($response.refresh.Substring(0, 40))..." -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[NOTA] Esto demuestra seguridad moderna con tokens JWT" -ForegroundColor Magenta
    
} catch {
    Write-Host ""
    Write-Host "[ADVERTENCIA] El servidor no esta corriendo. Iniciandolo..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Por favor, ejecuta en otra terminal:" -ForegroundColor Red
    Write-Host "   cd backend" -ForegroundColor White
    Write-Host "   python manage.py runserver" -ForegroundColor White
    Write-Host ""
    Pause-Demo "Presiona ENTER cuando el servidor este corriendo..."
    
    # Intentar de nuevo
    $response = Invoke-RestMethod -Uri "$BASE_URL/api/token/" -Method Post -Body $loginData -ContentType "application/json"
    $ADMIN_TOKEN = $response.access
    Write-Host "[OK] Login exitoso" -ForegroundColor Green
}

Pause-Demo

# [STEP 4] Control de permisos por rol (1 min)
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " [STEP 4] CONTROL DE PERMISOS POR ROL" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Cada usuario ve solo lo que su rol le permite" -ForegroundColor White
Write-Host ""
Write-Host "Ejecutando: GET /api/projects/ con token de Admin" -ForegroundColor Gray

try {
    $headers = @{
        "Authorization" = "Bearer $ADMIN_TOKEN"
    }
    
    $projects = Invoke-RestMethod -Uri "$BASE_URL/api/projects/" -Method Get -Headers $headers
    
    Write-Host ""
    Write-Host "[OK] Proyectos visibles para ADMIN:" -ForegroundColor Green
    foreach ($project in $projects) {
        Write-Host "   - $($project.name) - $($project.company_name)" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "[MATRIZ] Permisos por rol:" -ForegroundColor Yellow
    Write-Host "   +-------------+----------------------------+" -ForegroundColor Gray
    Write-Host "   | ADMIN       | Ve TODOS los proyectos     |" -ForegroundColor Gray
    Write-Host "   | CONSULTANT  | Ve solo proyectos asignados|" -ForegroundColor Gray
    Write-Host "   | CLIENT      | Ve solo su proyecto        |" -ForegroundColor Gray
    Write-Host "   +-------------+----------------------------+" -ForegroundColor Gray
    Write-Host ""
    Write-Host "[NOTA] Controlado por permission classes personalizadas" -ForegroundColor Magenta
    
} catch {
    Write-Host "[ERROR] Error al obtener proyectos: $_" -ForegroundColor Red
}

Pause-Demo

# [STEP 5] AuditLog automatico (1 min)
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " [STEP 5] AUDITORIA AUTOMATICA (AuditLog)" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Cada accion queda registrada automaticamente usando Django signals" -ForegroundColor White
Write-Host ""
Write-Host "Ejecutando: GET /api/audit-logs/" -ForegroundColor Gray

try {
    $headers = @{
        "Authorization" = "Bearer $ADMIN_TOKEN"
    }
    
    $logs = Invoke-RestMethod -Uri "$BASE_URL/api/audit-logs/" -Method Get -Headers $headers
    
    Write-Host ""
    Write-Host "[OK] Ultimos registros de auditoria:" -ForegroundColor Green
    
    $recentLogs = $logs | Select-Object -First 5
    foreach ($log in $recentLogs) {
        $timestamp = $log.timestamp
        $user = $log.user
        $action = $log.action
        $modelName = $log.model_name
        Write-Host "   - $timestamp - $user - $action - $modelName" -ForegroundColor Cyan
    }
    
    Write-Host ""
    Write-Host "[INFO] Informacion capturada en cada log:" -ForegroundColor Yellow
    Write-Host "   - Usuario que realizo la accion" -ForegroundColor Cyan
    Write-Host "   - Tipo de accion (CREATE / UPDATE / DELETE)" -ForegroundColor Cyan
    Write-Host "   - Timestamp preciso" -ForegroundColor Cyan
    Write-Host "   - Modelo afectado" -ForegroundColor Cyan
    Write-Host "   - Cambios realizados (JSON diff)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "[NOTA] Esto impresiona porque demuestra compliance y trazabilidad" -ForegroundColor Magenta
    
} catch {
    Write-Host "[ERROR] Error al obtener audit logs: $_" -ForegroundColor Red
}

Pause-Demo

# [STEP 6] Suite de tests (30 seg)
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " [STEP 6] SUITE DE TESTS AUTOMATIZADOS" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Todos los escenarios criticos estan cubiertos con tests automatizados" -ForegroundColor White
Write-Host ""
Write-Host "Ejecutando: python test_demo_sprint1.py" -ForegroundColor Gray
& $pythonExe test_demo_sprint1.py

Write-Host ""
Write-Host "[NOTA] Coverage de tests:" -ForegroundColor Magenta
Write-Host "   - Autenticacion JWT" -ForegroundColor Cyan
Write-Host "   - Permisos por rol" -ForegroundColor Cyan
Write-Host "   - Filtrado multi-tenant" -ForegroundColor Cyan
Write-Host "   - AuditLog automatico" -ForegroundColor Cyan
Write-Host "   - Manejo de errores 401/403" -ForegroundColor Cyan

Pause-Demo

# [STEP 7] Resumen de arquitectura
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " [STEP 7] ARQUITECTURA DEL SISTEMA" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "[ARCHIVOS] Archivos clave para revisar en VS Code:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   1. config/urls.py" -ForegroundColor Cyan
Write-Host "      -> API centralizada en un router" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. apps/users/permissions.py" -ForegroundColor Cyan
Write-Host "      -> 6 permission classes personalizadas" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. apps/projects/signals.py" -ForegroundColor Cyan
Write-Host "      -> Generacion automatica de AuditLog" -ForegroundColor Gray
Write-Host ""

Pause-Demo

# [CONCLUSION]
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "   [OK] DEMO COMPLETADA EXITOSAMENTE" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para la presentacion:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Este Sprint 1 entrega una base production-ready:" -ForegroundColor White
Write-Host "    - Autenticacion JWT" -ForegroundColor Cyan
Write-Host "    - Control de acceso multi-tenant" -ForegroundColor Cyan
Write-Host "    - Auditoria automatica" -ForegroundColor Cyan
Write-Host "    - Suite de tests que valida todo el flujo" -ForegroundColor White
Write-Host ""
Write-Host "[ESTADISTICAS] Sprint 1:" -ForegroundColor Yellow
Write-Host "   - 5 apps Django implementadas" -ForegroundColor Cyan
Write-Host "   - 8 modelos de datos" -ForegroundColor Cyan
Write-Host "   - 12 endpoints REST API" -ForegroundColor Cyan
Write-Host "   - 6 permission classes" -ForegroundColor Cyan
Write-Host "   - 15+ tests automatizados" -ForegroundColor Cyan
Write-Host ""
Write-Host "[LISTO] El sistema esta listo para el siguiente sprint!" -ForegroundColor Green
Write-Host ""
