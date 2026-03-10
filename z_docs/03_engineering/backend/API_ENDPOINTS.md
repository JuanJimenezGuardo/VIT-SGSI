# 📚 API Endpoints - Sprint 1

**Base URL:** `http://localhost:8000/api/`

## 🔐 Autenticación

### Obtener Token JWT
```http
POST /api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbG...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbG..."
}
```

### Renovar Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbG..."
}
```

---

## 👥 Usuarios (`/api/users/`)

**Permisos:** Solo ADMIN puede crear/editar/eliminar usuarios

### Listar Usuarios
```http
GET /api/users/
Authorization: Bearer <access_token>
```

### Crear Usuario
```http
POST /api/users/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "username": "nuevo_usuario",
  "email": "usuario@example.com",
  "password": "password123",
  "role": "CLIENT",
  "first_name": "Juan",
  "last_name": "Pérez",
  "phone": "555-1234"
}
```

**Roles disponibles:**
- `ADMIN`: Administrador VIT (acceso total)
- `CONSULTANT`: Consultor (crear proyectos, gestionar ISO)
- `CLIENT`: Cliente (ver solo proyectos asignados)

### Obtener Proyectos de un Usuario
```http
GET /api/users/{id}/projects/
Authorization: Bearer <access_token>
```

---

## 🏢 Empresas (`/api/companies/`)

**Permisos:** ADMIN y CONSULTANT pueden crear/editar, todos pueden ver

### Listar Empresas
```http
GET /api/companies/
Authorization: Bearer <access_token>
```

### Crear Empresa
```http
POST /api/companies/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "ACME Corp",
  "rfc": "ACM010101ABC",
  "email": "contacto@acme.com",
  "phone": "555-0100",
  "address": "Av. Principal 123",
  "city": "Bogotá",
  "state": "Cundinamarca",
  "country": "Colombia",
  "contact_person": "Juan Pérez",
  "contact_position": "CEO"
}
```

---

## 📁 Proyectos (`/api/projects/`)

**Permisos:** ADMIN ve todos, CONSULTANT/CLIENT solo proyectos asignados

### Listar Proyectos
```http
GET /api/projects/
Authorization: Bearer <access_token>
```

**Filtrado dinámico:**
- Admin: ve TODOS los proyectos
- Consultant/Client: solo proyectos donde está asignado (via ProjectUser)

### Crear Proyecto
```http
POST /api/projects/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Proyecto ISO 27001 ACME",
  "description": "Implementación de SGSI",
  "company": 1,
  "status": "PLANNING",
  "start_date": "2026-03-01",
  "end_date": "2026-12-31"
}
```

**Estados disponibles:**
- `PLANNING`: Planeación
- `IN_PROGRESS`: En progreso
- `COMPLETED`: Completado
- `ON_HOLD`: En pausa

### Obtener Usuarios de un Proyecto
```http
GET /api/projects/{id}/users/
Authorization: Bearer <access_token>
```

---

## 👤 Asignaciones de Usuarios a Proyectos (`/api/project-users/`)

**Permisos:** ADMIN y CONSULTANT pueden crear/editar

### Listar Asignaciones
```http
GET /api/project-users/
Authorization: Bearer <access_token>
```

### Asignar Usuario a Proyecto
```http
POST /api/project-users/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "user": 2,
  "project": 1,
  "role": "CONSULTANT"
}
```

**Roles en proyecto:**
- `ADMIN`: Administrador del proyecto
- `CONSULTANT`: Consultor asignado
- `CLIENT`: Cliente (solo lectura)
- `VIEWER`: Observador

---

## 📋 Fases (`/api/phases/`)

**Permisos:** Usuarios autenticados

### Listar Fases
```http
GET /api/phases/
Authorization: Bearer <access_token>
```

### Crear Fase
```http
POST /api/phases/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "project": 1,
  "name": "Evaluación Inicial",
  "type": "ASSESSMENT",
  "description": "Fase de evaluación del estado actual",
  "start_date": "2026-03-01T09:00:00Z",
  "end_date": "2026-03-15T18:00:00Z",
  "order": 1
}
```

**Tipos de fase:**
- `ASSESSMENT`: Evaluación
- `PLANNING`: Planificación
- `IMPLEMENTATION`: Implementación
- `AUDIT`: Auditoría
- `CERTIFICATION`: Certificación

---

## ✅ Tareas (`/api/tasks/`)

**Permisos:** Usuarios autenticados

### Listar Tareas
```http
GET /api/tasks/
Authorization: Bearer <access_token>
```

### Crear Tarea
```http
POST /api/tasks/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "phase": 1,
  "name": "Documentar políticas de seguridad",
  "description": "Elaborar documento de políticas",
  "assigned_to": 2,
  "priority": "HIGH",
  "status": "PENDING",
  "due_date": "2026-03-10"
}
```

**Prioridades:**
- `LOW`: Baja
- `MEDIUM`: Media
- `HIGH`: Alta
- `CRITICAL`: Crítica

**Estados:**
- `PENDING`: Pendiente
- `IN_PROGRESS`: En progreso
- `COMPLETED`: Completada

---

## 📝 Registros de Auditoría (`/api/audit-logs/`)

**Permisos:** Solo lectura para usuarios autenticados

### Listar Logs
```http
GET /api/audit-logs/
Authorization: Bearer <access_token>
```

**Filtros disponibles:**
```http
GET /api/audit-logs/?user=1
GET /api/audit-logs/?entity_type=Project
GET /api/audit-logs/?action=CREATE
GET /api/audit-logs/?ordering=-timestamp
```

### Campos de respuesta
```json
{
  "id": 1,
  "user": 1,
  "user_username": "admin",
  "action": "CREATE",
  "action_display": "Creacion",
  "entity_type": "Project",
  "entity_id": 5,
  "changes": {
    "name": "Proyecto ISO 27001 ACME",
    "status": "PLANNING"
  },
  "timestamp": "2026-03-04T03:43:20.946696Z"
}
```

**Acciones registradas automáticamente:**
- CREATE: Creación de entidades
- UPDATE: Actualización de entidades
- DELETE: Eliminación de entidades

**Entidades monitoreadas:**
- Project
- Phase
- Task
- User
- ProjectUser

---

## 🔒 Matriz de Permisos

| Endpoint | ADMIN | CONSULTANT | CLIENT |
|----------|-------|------------|--------|
| `/api/users/` | ✅ CRUD | ❌ | ❌ |
| `/api/companies/` | ✅ CRUD | ✅ CRUD | 👁️ Read |
| `/api/projects/` | ✅ All | ✅ Assigned | 👁️ Assigned |
| `/api/project-users/` | ✅ CRUD | ✅ CRUD | 👁️ Read |
| `/api/phases/` | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| `/api/tasks/` | ✅ CRUD | ✅ CRUD | ✅ CRUD |
| `/api/audit-logs/` | 👁️ Read | 👁️ Read | 👁️ Read |

**Leyenda:**
- ✅ CRUD: Crear, Leer, Actualizar, Eliminar
- 👁️ Read: Solo lectura
- ❌ Sin acceso
- Assigned: Solo entidades donde el usuario está asignado

---

## 🧪 Ejemplos de Uso

### Flujo Completo: Crear Proyecto con Usuarios

**1. Login como Admin:**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**2. Crear Proyecto:**
```bash
curl -X POST http://localhost:8000/api/projects/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "ISO 27001 Banco XYZ",
    "company": 1,
    "status": "PLANNING",
    "start_date": "2026-03-01"
  }'
```

**3. Asignar Consultor:**
```bash
curl -X POST http://localhost:8000/api/project-users/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "user": 2,
    "project": 1,
    "role": "CONSULTANT"
  }'
```

**4. Verificar AuditLog:**
```bash
curl -X GET http://localhost:8000/api/audit-logs/ \
  -H "Authorization: Bearer <access_token>"
```

---

## ⚠️ Códigos de Error

- **401 Unauthorized**: Token inválido o expirado
- **403 Forbidden**: Permisos insuficientes para la operación
- **404 Not Found**: Recurso no encontrado
- **400 Bad Request**: Datos de entrada inválidos
- **500 Internal Server Error**: Error del servidor

### Renovar Token Expirado
Si recibes 401, renueva el token:
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

---

## 📊 Estado del Sistema

- **JWT Lifetime**: Access 15 min, Refresh 1 día
- **Auditoría**: Automática via Django signals
- **Base de Datos**: PostgreSQL 15
- **Autenticación**: JWT Bearer tokens
- **CORS**: Configurado para desarrollo local

---

**Última actualización:** Sprint 1 - Día 9 (Marzo 3, 2026)
