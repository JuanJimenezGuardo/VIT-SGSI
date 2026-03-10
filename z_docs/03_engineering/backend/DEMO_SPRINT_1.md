# 🎬 Demo Sprint 1 - Guía Paso a Paso

**Fecha:** 2 de marzo
**Sprint:** Sprint 1 - Seguridad y Autenticación
**Objetivo:** Demostrar login JWT, permisos por rol, y auditoría automática

---

## 📋 Datos de Prueba

### Usuarios Creados:

| Usuario | Password | Rol | Descripción |
|---------|----------|-----|-------------|
| `admin_vit` | `admin123` | **ADMIN** | Ve TODOS los proyectos |
| `consultant_ana` | `consultant123` | **CONSULTANT** | Solo ve proyectos asignados |
| `client_juan` | `client123` | **CLIENT** | Solo ve proyectos donde es cliente |

### Proyectos Creados:

1. **Implementación ISO 27001 - ACME**
   - Empresa: ACME Corporation
   - Asignados: consultant_ana (CONSULTANT), client_juan (CLIENT)
   - Estado: EN_PROGRESO

2. **Auditoría ISO 27001 - Bancolombia**
   - Empresa: Bancolombia ISO Project
   - Asignados: admin_vit (ADMIN)
   - Estado: PLANEACIÓN

---

## 🎯 Escenarios de Demo

### **Escenario 1: Login y Obtención de Tokens JWT**

#### 1.1 Login como ADMIN
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"admin_vit\", \"password\": \"admin123\"}"
```

**Respuesta esperada:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

💾 **Guardar el `access` token para los siguientes requests**

#### 1.2 Login como CONSULTANT
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"consultant_ana\", \"password\": \"consultant123\"}"
```

#### 1.3 Login como CLIENT
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"client_juan\", \"password\": \"client123\"}"
```

---

### **Escenario 2: Admin ve TODOS los proyectos**

```bash
# Usar el token de admin_vit
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer <ADMIN_ACCESS_TOKEN>"
```

**Resultado esperado:**
- ✅ Ver ambos proyectos (ACME y Bancolombia)
- ✅ Status 200 OK

---

### **Escenario 3: Consultant ve SOLO proyectos asignados**

```bash
# Usar el token de consultant_ana
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer <CONSULTANT_ACCESS_TOKEN>"
```

**Resultado esperado:**
- ✅ Solo ve: "Implementación ISO 27001 - ACME"
- ❌ NO ve: "Auditoría ISO 27001 - Bancolombia"
- ✅ Status 200 OK

---

### **Escenario 4: Client ve SOLO proyectos donde está asignado**

```bash
# Usar el token de client_juan
curl -X GET http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer <CLIENT_ACCESS_TOKEN>"
```

**Resultado esperado:**
- ✅ Solo ve: "Implementación ISO 27001 - ACME" (como CLIENT)
- ❌ NO ve: "Auditoría ISO 27001 - Bancolombia"
- ✅ Status 200 OK

---

### **Escenario 5: Crear Proyecto → AuditLog automático**

#### 5.1 Crear nuevo proyecto como CONSULTANT
```bash
# Usar el token de consultant_ana
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer <CONSULTANT_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ISO 27001 - Empresa XYZ (DEMO)",
    "description": "Proyecto de ejemplo creado durante demo Sprint 1",
    "company": 1,
    "status": "PLANNING",
    "start_date": "2026-03-05"
  }'
```

**Resultado esperado:**
```json
{
  "id": 3,
  "name": "ISO 27001 - Empresa XYZ (DEMO)",
  "description": "Proyecto de ejemplo creado durante demo Sprint 1",
  "company": 1,
  "status": "PLANNING",
  "start_date": "2026-03-05",
  "created_by": 2,
  "created_at": "2026-03-04T..."
}
```

#### 5.2 Verificar que aparece en AuditLog
```bash
# Verificar último registro en AuditLog
curl -X GET "http://localhost:8000/api/audit-logs/?entity_type=Project&action=CREATE" \
  -H "Authorization: Bearer <ANY_ACCESS_TOKEN>"
```

**Resultado esperado:**
```json
[
  {
    "id": 6,
    "user": 2,
    "user_username": "consultant_ana",
    "action": "CREATE",
    "action_display": "Creacion",
    "entity_type": "Project",
    "entity_id": 3,
    "changes": {
      "name": "ISO 27001 - Empresa XYZ (DEMO)",
      "status": "PLANNING",
      "company_id": 1
    },
    "timestamp": "2026-03-04T..."
  }
]
```

---

### **Escenario 6: Permisos - Client NO puede crear proyectos**

```bash
# Intentar crear proyecto como CLIENT (debe fallar)
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer <CLIENT_ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Proyecto NO AUTORIZADO",
    "company": 1,
    "status": "PLANNING",
    "start_date": "2026-03-05"
  }'
```

**Resultado esperado:**
```json
{
  "detail": "No tiene permiso para realizar esta acción."
}
```
- ❌ Status 403 Forbidden (correcto, CLIENT no puede crear proyectos)

---

### **Escenario 7: Endpoint protegido - Sin token = Error**

```bash
# Intentar acceder sin token
curl -X GET http://localhost:8000/api/projects/
```

**Resultado esperado:**
```json
{
  "detail": "Las credenciales de autenticación no se proveyeron."
}
```
- ❌ Status 401 Unauthorized (correcto, todos los endpoints están protegidos)

---

### **Escenario 8: Renovar Token JWT con Refresh Token**

```bash
# Renovar access token usando refresh token
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d "{\"refresh\": \"<REFRESH_TOKEN>\"}"
```

**Respuesta esperada:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...(nuevo token)"
}
```

---

## 📊 Resumen de Verificación

| Característica | Estado | Descripción |
|----------------|--------|-------------|
| ✅ Login JWT | OK | Usuarios obtienen tokens access/refresh |
| ✅ Endpoints protegidos | OK | Sin token → 401 Unauthorized |
| ✅ Permisos ADMIN | OK | Ve todos los proyectos |
| ✅ Permisos CONSULTANT | OK | Solo ve proyectos asignados |
| ✅ Permisos CLIENT | OK | Solo ve proyectos asignados, no puede crear |
| ✅ AuditLog automático | OK | Crear/editar/eliminar → registro en AuditLog |
| ✅ Signals funcionando | OK | Sin código manual, automático via signals |

---

## 🎥 Script para Video (3-5 min)

### **Minuto 0-1: Introducción**
- "Presentación del Sprint 1: Seguridad y Autenticación"
- Mostrar datos de prueba creados (3 usuarios, 2 proyectos)

### **Minuto 1-2: Login y Tokens**
- Login con admin_vit → recibe tokens JWT
- Explicar access token (15 min) vs refresh token (1 día)

### **Minuto 2-3: Permisos por Rol**
- **Admin** → GET /api/projects/ → ve ambos proyectos
- **Consultant** → GET /api/projects/ → solo ve proyecto ACME
- **Client** → GET /api/projects/ → solo ve proyecto ACME

### **Minuto 3-4: Crear Proyecto y AuditLog**
- Consultant crea nuevo proyecto
- Mostrar respuesta exitosa
- GET /api/audit-logs/ → aparece registro automático
- Explicar: "Sin código manual, Django signals lo registran"

### **Minuto 4-5: Seguridad**
- Intentar acceder sin token → 401
- Client intenta crear proyecto → 403
- Conclusión: "Plataforma segura lista para producción"

---

## 🔍 Queries PostgreSQL para Validar

### Ver todos los usuarios:
```sql
SELECT id, username, role, email FROM users_user;
```

### Ver proyectos con asignaciones:
```sql
SELECT 
  p.id, p.name, p.status,
  pu.user_id, u.username, pu.role
FROM projects_project p
LEFT JOIN projects_projectuser pu ON pu.project_id = p.id
LEFT JOIN users_user u ON u.id = pu.user_id;
```

### Ver últimos registros en AuditLog:
```sql
SELECT 
  id, user_id, action, entity_type, entity_id, 
  timestamp
FROM users_auditlog
ORDER BY timestamp DESC
LIMIT 10;
```

---

## ✅ Checklist Final

Antes de grabar el video, verificar:

- [ ] Backend corriendo en `http://localhost:8000`
- [ ] PostgreSQL conectado
- [ ] 3 usuarios creados (admin, consultant, client)
- [ ] 2 proyectos creados (ACME, Bancolombia)
- [ ] Asignaciones ProjectUser correctas
- [ ] Puede hacer login y recibir tokens
- [ ] Admin ve todos los proyectos
- [ ] Consultant/Client solo ven proyectos asignados
- [ ] Crear proyecto genera AuditLog
- [ ] Sin token devuelve 401
- [ ] Client no puede crear proyectos (403)

---

## 🚀 Listo para Video

Una vez verificados todos los checkpoints, grabar video de 3-5 minutos siguiendo el script.

**Herramientas sugeridas:**
- Postman / Thunder Client (más visual que curl)
- OBS Studio / QuickTime (para grabar pantalla)
- PgAdmin (para mostrar tablas PostgreSQL)

**Tips:**
- Usar modo split screen (API requests + DB queries)
- Explicar mientras ejecutas los requests
- Mostrar tanto éxitos (200) como errores esperados (401, 403)

---

**¿Listo?** ¡Hora de grabar! 🎬
