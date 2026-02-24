# 🎯 Sprint 1 Backend — Guía Tutorial Paso a Paso

**Duración:** 19 feb → 2 mar (12 días)  
**Equipo:** 2 desarrolladores backend  
**Objetivo:** Dejar de ser API abierta → Plataforma con seguridad real

---

## ⚠️ ARQUITECTURA TRANSVERSAL: Consideraciones de Producción

**Importante:** Este sprint construye la base de seguridad. Todas las decisiones aquí impactarán el deployment final en Render.

**Leer primero:** [ARQUITECTURA_DESPLIEGUE_PRODUCCION.md](ARQUITECTURA_DESPLIEGUE_PRODUCCION.md) §"Configuración Django para Producción"

### Decisiones que hacemos HOY que impactan PRODUCCIÓN:

1. **Settings por Entorno:** No solo .env, crear `settings/development.py` y `settings/production.py` ahora
2. **JWT Cookies:**  
   - `Secure=True` (solo HTTPS en prod)
   - `HttpOnly=True` (no accesible desde JavaScript)
   - `SameSite=Strict` (protección CSRF)
3. **CORS:** Definir orígenes específicos (backend en Render, frontend en Vercel)
4. **Variables Sensibles:** NUNCA hardcodear `SECRET_KEY`, `DATABASE_PASSWORD`, etc.
5. **PostgreSQL:** Usar PostgreSQL local (mismo que producción), no SQLite
6. **Debug Mode:** `DEBUG=True` solo en desarrollo, automatizar a `False` en CI/CD
7. **Logging:** Usar estructurado (no prints), facilita análisis en producción

### Antes de empezar:

```bash
# Crear estructura de settings
backend/config/
├── settings/
│   ├── __init__.py
│   ├── base.py          # Configuración común
│   ├── development.py   # Debug=True, DB local
│   └── production.py    # Debug=False, variables de entorno
```

---

## 📋 Resumen del Sprint

Al final del sprint tendrás:
- ✅ Login con JWT (tokens de acceso)
- ✅ Roles funcionando (Admin/Consultor/Cliente)
- ✅ Permisos por endpoint (solo Admin puede X, etc.)
- ✅ ProjectUser (usuarios asignados a proyectos)
- ✅ AuditLog (registro de cambios)

---

## 🧠 Conceptos clave (para que puedas supervisar)

### 1️⃣ AbstractUser vs modelo User custom

**Antes (tu código actual):**
```python
class User(models.Model):  # ❌ Modelo simple, NO usa sistema de Django
    username = ...
    password = ...
```

**Problema:** Django no sabe que éste es TU modelo de usuario. No funciona con admin, permisos, JWT, etc.

**Después:**
```python
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):  # ✅ Hereda funcionalidad completa
    role = models.CharField(...)
    phone = models.CharField(...)
```

**Qué ganas:**
- Django reconoce este modelo como "el usuario oficial"
- Admin panel funciona automáticamente
- JWT funciona sin hacks
- Permisos nativos de Django disponibles

---

### 2️⃣ AUTH_USER_MODEL

En `settings.py` debes activar:
```python
AUTH_USER_MODEL = 'users.User'
```

**Qué hace:** Le dice a Django "usa MI modelo User, no el default".

⚠️ **MUY IMPORTANTE:** Esto debe estar ANTES de la primera migración. Si ya tienes migraciones, hay que borrar la base y empezar de nuevo (por eso te pregunté si tenías datos).

---

### 3️⃣ SimpleJWT

Librería que genera tokens de acceso y refresh.

**Flujo:**
1. Usuario envía username + password a `/api/token/`
2. Backend valida y devuelve 2 tokens:
   - `access`: válido 15 min (para llamadas API)
   - `refresh`: válido 1 día (para renovar access sin pedir password otra vez)
3. Frontend guarda ambos tokens
4. Frontend envía `access` en cada request: `Authorization: Bearer <token>`
5. Cuando `access` expira → envía `refresh` a `/api/token/refresh/` → recibe nuevo `access`

**Por qué es bueno:**
- Stateless (no guarda sesiones en backend)
- Seguro (tokens expiran)
- Escalable (puedes tener múltiples frontends)

---

### 4️⃣ Permisos por rol

Django tiene sistema de permisos, pero tú necesitas permisos por ROL (Admin/Consultor/Cliente).

**Estrategia:**
- Crear clases de permiso personalizadas: `IsAdmin`, `IsConsultant`, `IsClient`
- Aplicarlas a cada ViewSet según regla de negocio

**Ejemplo conceptual:**
- `UserViewSet` → solo Admin puede crear/editar usuarios
- `ProjectViewSet` → Consultor puede crear, Cliente solo puede ver los suyos
- `TaskViewSet` → todos pueden ver, pero solo Consultor y Admin editan

---

### 5️⃣ ProjectUser (el más importante para SGSI)

**Problema:** Un usuario puede ser Consultor en un proyecto y Cliente en otro.

**Solución:** Tabla intermedia que relaciona User ↔ Project con rol específico.

**Modelo conceptual:**
```
ProjectUser
- user (FK a User)
- project (FK a Project)
- role (ADMIN/CONSULTANT/CLIENT)
- created_at
```

**Caso de uso:**
- Juan es CONSULTANT en "Proyecto Bancolombia"
- Juan es CLIENT en "Proyecto Acme"
- Cuando Juan entra a Bancolombia → ve opciones de consultor
- Cuando entra a Acme → solo ve progreso (cliente)

---

### 6️⃣ AuditLog (trazabilidad)

**Para qué:** El profesor quiere ver "quién hizo qué y cuándo".

**Modelo conceptual:**
```
AuditLog
- user (quién hizo el cambio)
- action (CREATE/UPDATE/DELETE)
- entity_type (Project/Task/User/etc)
- entity_id (ID del registro afectado)
- changes (JSON con qué cambió)
- timestamp
```

**Ejemplo:**
- Usuario "Ana" (CONSULTANT) creó Project #5 "ISO ACME" → se guarda en AuditLog
- Usuario "Carlos" (ADMIN) editó Task #12 → se guarda cambio de estado

**Cómo implementar (sin ser programador):**
- Django tiene "signals" que se disparan automáticamente al crear/editar/borrar
- Usas signal `post_save` y `post_delete` para capturar cambios
- En el signal, creas un registro en AuditLog

---

## 📅 Plan día a día (12 días divididos en 3 mini-sprints)

---

## 🔹 Mini-Sprint 1.1 (19-21 feb) — Migrar User + SimpleJWT

### **Día 1 (19 feb) — Preparación y migración User**

**Tareas para Dev 1:**
1. Revisar si hay datos importantes en la base (Users, Projects, etc.)
2. Si NO hay datos importantes → borrar `db.sqlite3` y carpetas `migrations/` de todas las apps
3. Modificar `apps/users/models.py`:
   - Importar `AbstractUser`
   - Cambiar `class User(models.Model):` por `class User(AbstractUser):`
   - Eliminar campos redundantes (username, email, password, first_name, last_name, is_active) porque AbstractUser ya los tiene
   - Mantener campos custom: `role`, `phone`, timestamps
4. Agregar en `config/settings.py`:
   ```python
   AUTH_USER_MODEL = 'users.User'
   ```

**Checkpoint del día:**
- Pregunta al dev: "¿Ya no hay errores al hacer `python manage.py makemigrations`?"
- Si dice "sí" → bien, pasar al día 2
- Si dice "no" → revisar que eliminó campos duplicados y que AUTH_USER_MODEL está bien escrito

---

### **Día 2 (20 feb) — Aplicar migraciones + instalar SimpleJWT**

**Tareas para Dev 1:**
1. Ejecutar:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. Crear superusuario para probar:
   ```bash
   python manage.py createsuperuser
   ```
3. Instalar SimpleJWT:
   ```bash
   pip install djangorestframework-simplejwt
   ```
4. Actualizar `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

**Tareas para Dev 2:**
1. Configurar SimpleJWT en `config/settings.py`:
   - Agregar `'rest_framework_simplejwt'` a `INSTALLED_APPS`
   - Configurar `REST_FRAMEWORK` para usar JWT como auth default
   - Configurar tiempos de expiración de tokens
2. Agregar rutas en `config/urls.py`:
   - `/api/token/` (obtener token)
   - `/api/token/refresh/` (renovar token)

**Checkpoint del día:**
- Pregunta: "¿Puedo hacer login desde Postman/Thunder Client?"
- Test manual:
  1. POST a `http://localhost:8000/api/token/`
  2. Body: `{"username": "admin", "password": "tu_password"}`
  3. ¿Devuelve `access` y `refresh` tokens?
- Si sí → ✅ JWT funciona
- Si no → revisar configuración en settings y urls

---

### **Día 3 (21 feb) — Proteger endpoints con JWT**

**Tareas para Dev 1:**
1. Cambiar `permission_classes` de todos los ViewSets:
   - De `[AllowAny]` a `[IsAuthenticated]`
2. Probar que ahora SÍ pide token:
   - GET `/api/users/` sin token → debe dar 401
   - GET `/api/users/` CON token en header → debe funcionar

**Tareas para Dev 2:**
1. Actualizar serializers si es necesario (ocultar password en respuestas, etc.)
2. Crear endpoint de registro básico (opcional, pero útil para demo)

**Checkpoint del día:**
- Pregunta: "¿Todos los endpoints están protegidos?"
- Test: intentar acceder sin token → debe fallar
- ✅ Demo interna: login → obtener token → usar token en request → ver datos

---

## 🔹 Mini-Sprint 1.2 (24-26 feb) — Permisos por rol + ProjectUser

### **Día 4 (24 feb) — Crear clases de permiso personalizadas**

**Tareas para Dev 1:**
1. Crear archivo `apps/users/permissions.py`
2. Crear 3 clases:
   - `IsAdmin` (solo si `user.role == 'ADMIN'`)
   - `IsConsultant` (si `user.role == 'CONSULTANT'`)
   - `IsClient` (si `user.role == 'CLIENT'`)
3. Documentar cada clase con comentario explicando cuándo se usa

**Tareas para Dev 2:**
1. Aplicar permisos a ViewSets principales:
   - `UserViewSet` → solo Admin
   - `CompanyViewSet` → Admin y Consultant
   - `ProjectViewSet` → Admin y Consultant (por ahora)
2. Probar con usuarios de diferentes roles

**Checkpoint del día:**
- Pregunta: "¿Un usuario CLIENT puede crear proyectos?"
- Respuesta esperada: NO (debe dar 403)
- ✅ Si funciona → permisos básicos listos

---

### **Día 5 (25 feb) — Modelo ProjectUser**

**Tareas para Dev 1:**
1. Crear nueva app o modelo en `apps/projects/models.py`:
   - Modelo `ProjectUser`
   - Campos: `user`, `project`, `role`, `created_at`
   - Relación única: un user no puede estar 2 veces en el mismo proyecto
2. Hacer migraciones

**Tareas para Dev 2:**
1. Crear serializer para ProjectUser
2. Crear ViewSet para CRUD de ProjectUser
3. Agregar rutas en `apps/projects/urls.py`

**Checkpoint del día:**
- Pregunta: "¿Puedo asignar un usuario a un proyecto con rol específico?"
- Test manual:
  1. POST `/api/project-users/`
  2. Body: `{"user": 1, "project": 1, "role": "CONSULTANT"}`
  3. ¿Se crea correctamente?
- ✅ Si sí → ProjectUser funciona

---

### **Día 6 (26 feb) — Filtrar proyectos según ProjectUser**

**Tareas para Dev 1:**
1. Modificar `ProjectViewSet` para que:
   - Admin ve todos los proyectos
   - Consultant y Client solo ven proyectos donde están asignados (vía ProjectUser)
2. Usar `queryset` dinámico según `request.user`

**Tareas para Dev 2:**
1. Agregar endpoint `/api/projects/{id}/users/` para ver usuarios de un proyecto
2. Agregar endpoint `/api/users/{id}/projects/` para ver proyectos de un usuario

**Checkpoint del día:**
- Pregunta: "Si creo un usuario CLIENT y lo asigno solo al Proyecto 1, ¿ve el Proyecto 2?"
- Respuesta esperada: NO
- ✅ Demo: crear 2 proyectos, asignar user solo a 1, hacer GET `/api/projects/` con ese user → debe ver 1 solo

---

## 🔹 Mini-Sprint 1.3 (27 feb - 2 mar) — AuditLog + integración final

### **Día 7 (27 feb) — Modelo AuditLog**

**Tareas para Dev 1:**
1. Crear modelo `AuditLog` en nueva app o en `apps/users/`
2. Campos:
   - `user` (quién)
   - `action` (CREATE/UPDATE/DELETE)
   - `entity_type` (texto: "Project", "Task", etc.)
   - `entity_id` (ID del objeto afectado)
   - `changes` (JSONField opcional)
   - `timestamp`
3. Hacer migraciones

**Tareas para Dev 2:**
1. Crear serializer y ViewSet para AuditLog (solo lectura)
2. Agregar filtros (por user, por entity_type, por fecha)

**Checkpoint del día:**
- Pregunta: "¿Puedo crear un AuditLog manualmente desde Django shell?"
- Test: crear registro → verificar en admin o endpoint
- ✅ Si aparece → modelo funciona

---

### **Día 8 (28 feb) — Signals para auto-registrar cambios**

**Tareas para Dev 1:**
1. Crear archivo `apps/projects/signals.py`
2. Conectar signals `post_save` y `post_delete` para:
   - Project
   - Phase
   - Task
3. Registrar signals en `apps/projects/apps.py`

**Tareas para Dev 2:**
1. Crear signals similares para User y ProjectUser
2. Probar que al crear/editar/borrar, se genera AuditLog automáticamente

**Checkpoint del día:**
- Pregunta: "Si creo un proyecto, ¿aparece en AuditLog automáticamente?"
- Test manual: crear proyecto → GET `/api/audit-logs/` → debe aparecer registro
- ✅ Si aparece → signals funcionan

---

### **Día 9 (1 mar) — Limpieza y pruebas**

**Tareas conjuntas:**
1. Revisar que todos los endpoints tengan permisos correctos
2. Ajustar tests existentes (si los hay) para que funcionen con JWT
3. Documentar endpoints principales en README o archivo separado

**Checkpoint del día:**
- Revisión completa de endpoints con diferentes roles
- ✅ Sin errores 500, todos los permisos funcionando

---

### **Día 10 (2 mar) — Demo final del sprint**

**Tareas:**
1. Preparar datos de prueba (2-3 usuarios, 2 proyectos, asignaciones)
2. Hacer video corto (3-5 min) mostrando:
   - Login con JWT
   - Usuario Admin ve todo
   - Usuario Consultant ve solo sus proyectos
   - Crear proyecto → aparece en AuditLog
3. Commit final y tag `v0.1-sprint1`

---

## ✅ Checklist de verificación final (para ti como líder)

### Funcionalidades:
- [ ] Login funciona y devuelve tokens JWT
- [ ] Endpoints protegidos (sin token → 401)
- [ ] Permisos por rol funcionan (Admin vs Consultant vs Client)
- [ ] ProjectUser permite asignar usuarios a proyectos
- [ ] Usuarios solo ven proyectos donde están asignados
- [ ] AuditLog registra automáticamente cambios en Project/Phase/Task/User/ProjectUser

### Técnico:
- [ ] Modelo User hereda de AbstractUser
- [ ] AUTH_USER_MODEL configurado en settings
- [ ] SimpleJWT instalado y configurado
- [ ] Migraciones aplicadas sin errores
- [ ] No hay permisos AllowAny en producción

### Demo:
- [ ] Video de 3-5 min mostrando flujo completo
- [ ] Capturas de pantalla de Postman/Thunder Client
- [ ] README actualizado con endpoints y roles

---

## 🚨 Errores comunes y cómo evitarlos

### Error 1: "No such table: users_user"
**Causa:** No corriste migraciones  
**Solución:** `python manage.py migrate`

### Error 2: "User model is not set"
**Causa:** Falta `AUTH_USER_MODEL` en settings  
**Solución:** Agregar `AUTH_USER_MODEL = 'users.User'`

### Error 3: "Token inválido"
**Causa:** Token expirado o mal formateado  
**Solución:** Renovar token con `/api/token/refresh/`

### Error 4: "Circular import"
**Causa:** Models importando entre sí incorrectamente  
**Solución:** Usar strings en ForeignKey: `ForeignKey('users.User', ...)`

### Error 5: Signals no se registran
**Causa:** No se importó signals en apps.py  
**Solución:** En `apps/projects/apps.py`, agregar `import apps.projects.signals` en `ready()`

---

## 📊 Métricas de éxito del Sprint 1

Al final del sprint debes poder mostrar:
1. ✅ 3 usuarios creados (Admin, Consultant, Client)
2. ✅ 2 proyectos con usuarios asignados
3. ✅ Login funciona y devuelve tokens
4. ✅ Mínimo 5 registros en AuditLog
5. ✅ Video de demo de 3-5 min

---

## 🎓 Preguntas para hacerle al equipo cada viernes

1. "¿Cuántos commits hiciste esta semana?" (mínimo 3)
2. "¿Puedes mostrarme en pantalla el resultado?" (demo rápida)
3. "¿Qué bloqueadores tuviste?" (para ayudar o escalar)
4. "¿Cuál es el siguiente checkpoint?" (para validar que entienden)

---

## 📖 Recursos para profundizar (para tu equipo)

- Django AbstractUser: https://docs.djangoproject.com/en/4.2/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project
- SimpleJWT: https://django-rest-framework-simplejwt.readthedocs.io/
- DRF Permissions: https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions
- Django Signals: https://docs.djangoproject.com/en/4.2/topics/signals/

---

**¿Dudas o bloqueadores?** Pregúntame cualquier concepto que no entiendas. Estoy aquí como tutor, no como programador 😎
