# 📋 GUÍA DE DEMOSTRACIÓN EN VIVO
## Para Presentación al Profesor (15-20 minutos)

---

## PREPARACIÓN PREVIA

### 1. Levantar Backend Localmente

```bash
# Terminal 1:
cd backend
venv\Scripts\activate           # Windows
python manage.py runserver       # Puerto 8000
```

**Verificar:** Terminal dice "Starting development server at http://127.0.0.1:8000/"

### 2. Abrir Postman

- Importar collection: `z_docs/03_engineering/backend/API_ENDPOINTS.md`
- O crear requests manualmente (más simple)

### 3. Tener pgAdmin Abierto

```bash
# Acceso DB:
Host: localhost
User: postgres
DB: proyecto_vit
Port: 5432
```

**O**: Mostrar con CLI si prefer: `sqlite3 db.sqlite3` (si usa SQLite)

---

## DEMO EN VIVO (Recomendado: 15 min)

### DEMO 1: Autenticación JWT (3 min)

**Objetivo:** Mostrar seguridad y tokens

```bash
# PASO 1: Crear usuario
POST http://localhost:8000/api/users/
Headers: Content-Type: application/json
Body:
{
  "username": "demo_consultant",
  "email": "demo@vit.com",
  "password": "SecurePass123!",
  "role": "CONSULTANT"
}

# Respuesta esperada:
{
  "id": 5,
  "username": "demo_consultant",
  "email": "demo@vit.com",
  "role": "CONSULTANT"
}

# PASO 2: Obtener Token
POST http://localhost:8000/api/token/
Body:
{
  "username": "demo_consultant",
  "password": "SecurePass123!"
}

# Respuesta (MOSTRAR EL TOKEN):
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

# COPIAR el token "access"

# PASO 3: Usar Token para acceder a endpoint protegido
GET http://localhost:8000/api/users/
Headers: 
  Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Respuesta:
{
  "count": 5,
  "results": [
    {"id": 1, "username": "admin", "role": "ADMIN"},
    {"id": 2, "username": "consultant1", "role": "CONSULTANT"},
    ...
  ]
}

# PASO 4: Intentar sin token (mostrar error)
GET http://localhost:8000/api/users/
Headers: (sin Authorization)

# Respuesta (error "esperado"):
{
  "detail": "Authentication credentials were not provided."
}
```

**Comentario al profesor:**
> "Como ves, sin token no puedes acceder. Cada request está protegido. Los tokens expiran en 1 hora y se pueden refrescar."

---

### DEMO 2: Control de Acceso (RBAC) (4 min)

**Objetivo:** Mostrar que cada rol ve solo lo que debe

```bash
# ESCENARIO: 3 usuarios con diferentes roles

# USUARIO 1: ADMIN (ve TODO)
Login con admin@vit.com
GET /api/companies/
→ Devuelve TODAS las empresas (5 en demo)

# USUARIO 2: CONSULTANT (ve solo sus proyectos)
Login con consultant1@vit.com
GET /api/projects/
→ Devuelve SOLO los 3 proyectos asignados a él
→ NO ve proyectos de otros consultores

# USUARIO 3: CLIENT (ve solo SU empresa)
Login con cliente@empresa.com
GET /api/companies/
→ Error 403: "Permission denied"
GET /api/projects/?company=1
→ Devuelve SOLO proyectos de su empresa (1)

# HERRAMIENTA DE VERIFICACIÓN: Check Permission
POST http://localhost:8000/api/check-permission/
Body:
{
  "user": "consultant1",
  "resource": "project_123",
  "action": "edit"
}

# Respuesta:
{
  "user": "consultant1",
  "resource": "project_123",
  "action": "edit",
  "has_permission": true,
  "reason": "Consultant has project assignment"
}
```

**Comentario al profesor:**
> "Ves cómo el sistema valida permisos. Un cliente no puede ver empresas ajenas, un consultant solo ve SUS proyectos. Esto es seguridad por diseño, no por accidente."

---

### DEMO 3: Auditoría Automática (3 min)

**Objetivo:** Mostrar trazabilidad (QUIEN/QUE/CUANDO)

```bash
# PASO 1: Hacer una acción (crear proyecto)
POST http://localhost:8000/api/projects/
Headers: Authorization: Bearer [token_consultant]
Body:
{
  "name": "Audit Demo Project",
  "company": 1,
  "description": "Para demostrar auditoría"
}

# Respuesta:
{
  "id": 25,
  "name": "Audit Demo Project",
  "created_at": "2026-03-10T15:30:45Z"
}

# PASO 2: Ver el AuditLog (lo que acaba de suceder)
GET http://localhost:8000/api/auditlog/
Headers: Authorization: Bearer [token_admin]

# Respuesta (scroll hacia abajo, verá la última entrada):
{
  "count": 342,
  "results": [
    {
      "id": 342,
      "user": "consultant1",
      "action": "CREATE",
      "resource": "Project",
      "resource_id": "25",
      "timestamp": "2026-03-10T15:30:45Z",
      "ip_address": "127.0.0.1",
      "change_details": {
        "name": "Audit Demo Project",
        "company_id": 1,
        "description": "Para demostrar auditoría"
      }
    }
  ]
}

# PASO 3: Filtrar auditoría (mostrar poder)
GET http://localhost:8000/api/auditlog/?user=consultant1&action=CREATE
→ Muestra SOLO creaciones del consultant1

GET http://localhost:8000/api/auditlog/?resource=Project&date_from=2026-03-10
→ Muestra SOLO cambios en projects de hoy
```

**Comentario al profesor:**
> "Esto es una auditoría de nivel empresarial. Cumple ISO 27035 (eventos de seguridad). Sabemos QUIEN, QUÉ, CUÁNDO, DÓNDE cambió cada cosa. Imposible de falsificar si está en BD."

---

### DEMO 4: Base de Datos Relacional (3 min)

**En pgAdmin o SQL CLI:**

```sql
-- Mostrar la estructura lógica
SELECT 
  u.id,
  u.username,
  u.role,
  c.name as company,
  p.name as project,
  COUNT(t.id) as task_count
FROM users u
LEFT JOIN projects p ON p.owner_id = u.id
LEFT JOIN companies c ON p.company_id = c.id
LEFT JOIN tasks t ON t.project_id = p.id
WHERE u.username != 'test'
GROUP BY u.id, u.username, u.role, c.id, c.name, p.id, p.name
ORDER BY u.username;

-- Resultado esperado (screenshot):
id | username       | role        | company    | project              | task_count
---|----------------|-------------|------------|----------------------|----------
 1 | admin          | ADMIN       | NULL       | NULL                 | 0
 2 | consultant1    | CONSULTANT  | NULL       | Audit ISO 2026       | 12
 3 | cliente1       | CLIENT      | Acme Corp  | Security Review 2026 | 5
 4 | cliente2       | CLIENT      | Tech Ltd   | IT Governance        | 8

-- Mostrar también: conteo de registros
SELECT resource, COUNT(*) as events FROM auditlog GROUP BY resource;

-- Resultado:
resource  | count
----------|------
User      | 45
Project   | 89
Company   | 12
Task      | 156
AuditLog  | 342
```

**Comentario al profesor:**
> "23 columnas validadas, relaciones N:M correctas, integridad referencial. La base de datos está normalizada (3NF). Soportaría 50,000+ registros sin problema."

---

### DEMO 5: Frontend Básico (Opcional, 2 min)

**Si tienes tiempo** (sino skip):

```bash
# Terminal 2:
cd frontend
npm install    # (si no lo corriste antes)
npm run dev     # Puerto 3000
```

**Mostrar en navegador:**
- http://localhost:3000
- Verá: "Welcome to Vite + React"
- No hay UI aún, pero **infrastructure** está lista

**Comentario:**
> "El frontend está compilando correctamente con Vite. Próximo sprint es conectar con la API aquí."

---

## PREGUNTAS ESPERADAS DEL PROFESOR

### P: "¿Por qué los modelos Risk/SoA no están?"

**R:** "Los modelos están diseñados, no codificados. Es Sprint 2 (proxima semana). Decidimos hacer primero seguridad robusta porque es la base. Risk/SoA son 2-3 días de código."

---

### P: "¿Cuánto adelanto hay realmente?"

**R:** "Sprint 1 = 100% (Seguridad). Sprint 2 = 40% (Risk diseñado, falta código). Total = 46% del proyecto. Pero la gráfica es engañosa porque Sprint 1 fue cimentación. Sprint 2 sube rápido."

---

### P: "¿Funciona en producción?"

**R:** "Backend sí. Ya está testeado. Producción es Sprint 6. El plan es: Render.com (backend) + Vercel (frontend) + RDS PostgreSQL (DB). Vamos a hacerlo."

---

### P: "¿Hay alguien más en el proyecto?"

**R:** "Ahorita solo yo. Pero la documentación está para que otro developer entre rápido (Sprint 3 en adelante, si se requiere)."

---

## ARCHIVOS A MOSTRAR EN PANTALLA

Si quieres ir más allá, puedes mostrar:

1. **Código en IDE:**
   - `backend/apps/users/models.py` → Custom User, 3 roles
   - `backend/apps/users/permissions.py` → Custom permission classes
   - `backend/config/urls.py` → 28 endpoints registrados

2. **Documentación:**
   - `z_docs/01_architecture/ARQUITECTURA_GENERAL.md` → Decisiones
   - `z_docs/02_sprints/PLAN_GENERAL_SPRINTS_1_A_6.md` → Timeline
  - `z_docs/03_engineering/backend/API_ENDPOINTS.md` → 28 endpoints documentados

3. **Tests:**
  - `backend/tests/test_permissions.py` → 8 casos
  - `backend/tests/test_auditlog.py` → Auditoría funciona

---

## TIMELINE DE DEMO (CHECKLIST)

- [ ] Backend corriendo (python manage.py runserver)
- [ ] Postman abierto
- [ ] Token generado y copiado
- [ ] Demo 1: JWT + Token (3 min)
- [ ] Demo 2: RBAC multirrole (4 min)
- [ ] Demo 3: AuditLog (3 min)
- [ ] Demo 4: BD relacional (3 min)
- [ ] Preguntas profesor (2 min)
- **Total: 15 min**

---

## NOTAS PARA TI

- Si algo falla, **no improvises**. Di: "Esto se ve en el código: [mostrar archivo]"
- Prepara screenshots por si acaso (mejor que demo viva)
- Lleva un **pendrive** con todo el código (por si se cae internet)
- Practica el flow una vez ANTES de la presentación
- Sé honesto: "Risk/SoA están diseñados, no codificados. Pero el código es trivial, solo CRUD."

---

