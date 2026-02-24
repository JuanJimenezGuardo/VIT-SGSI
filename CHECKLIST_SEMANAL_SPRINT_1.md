# ✅ Checklist Semanal Sprint 1 (para control sin programar)

## ⚠️ VALIDACIÓN DE ARQUITECTURA PARA RENDER

Cada checkpoint debe validar que el código NO solo "funciona en desarrollo" sino que "ya está listo para Render".

**Preguntas de validación OBLIGATORIAS cada viernes:**

1. ❓ "¿El código dependería de SQLite?" → Si dice sí, bloqueador (debe ser PostgreSQL)
2. ❓ "¿Hay passwords o SECRET_KEY hardcodeados?" → Si dice sí, bloqueador (debe estar en .env)
3. ❓ "¿Hay AllowAny en endpoints que no son /api/token/?" → Si dice sí, bloqueador
4. ❓ "¿Los settings discriminan entre development y production?" → Si dice no, avistar

---

## 📅 Semana 1 (19-23 feb) — Auth + JWT + Permisos básicos

### Viernes 21 feb — Mini Demo

**Pide al equipo que muestre en pantalla:**

1. ✅ Login con Postman/Thunder Client
   - POST a `/api/token/` con username + password
   - Debe devolver `access` y `refresh` tokens
   
2. ✅ Request protegido
   - GET `/api/users/` SIN token → debe dar **401 Unauthorized**
   - GET `/api/users/` CON token en header → debe devolver lista de usuarios

3. ✅ Modelo User migrado
   - Ejecutar `python manage.py shell` y correr:
     ```python
     from apps.users.models import User
     print(User.__bases__)  # Debe incluir AbstractUser
     ```

**Preguntas de control:**

- [ ] "¿Cuántos commits hiciste?" (mínimo 3-5)
- [ ] "¿Puedo ver el código del modelo User?" → debe heredar de AbstractUser
- [ ] "¿Está AUTH_USER_MODEL en settings?" → debe estar
- [ ] "¿requirements.txt tiene djangorestframework-simplejwt?" → debe estar

**Entregable mínimo:**
- [ ] Screenshot de Postman con login exitoso
- [ ] Screenshot de error 401 sin token
- [ ] Link a commits de la semana

---

## 📅 Semana 2 (24-28 feb) — Permisos por rol + ProjectUser + AuditLog base

### Viernes 28 feb — Mini Demo

**Pide al equipo que muestre en pantalla:**

1. ✅ Permisos por rol funcionando
   - Login con usuario ADMIN → GET `/api/companies/` → funciona
   - Login con usuario CLIENT → POST `/api/companies/` → debe dar **403 Forbidden**

2. ✅ ProjectUser creado
   - POST `/api/project-users/` con:
     ```json
     {
       "user": 1,
       "project": 1,
       "role": "CONSULTANT"
     }
     ```
   - Debe crear la asignación

3. ✅ Filtrado por ProjectUser
   - Login como usuario asignado solo a Proyecto 1
   - GET `/api/projects/` → debe devolver SOLO Proyecto 1
   - No debe ver Proyecto 2

4. ✅ AuditLog registra cambios
   - Crear un proyecto
   - GET `/api/audit-logs/` → debe aparecer registro con:
     - action: "CREATE"
     - entity_type: "Project"
     - user: quien creó
     - timestamp

**Preguntas de control:**

- [ ] "¿Cuántos roles de permiso creaste?" → mínimo 3 (IsAdmin, IsConsultant, IsClient)
- [ ] "¿En qué archivo están?" → debe estar en `apps/users/permissions.py`
- [ ] "¿ProjectUser tiene unique_together?" → debe tener (user, project)
- [ ] "¿Los signals están registrados?" → debe estar en apps.py

**Entregable mínimo:**
- [ ] Screenshot de 403 cuando CLIENT intenta crear empresa
- [ ] Screenshot de ProjectUser creado (desde admin o Postman)
- [ ] Screenshot de AuditLog con al menos 3 registros
- [ ] Link a commits de la semana (mínimo 5-8)

---

## 📅 Semana 3 (1-2 mar) — Limpieza + Demo final

### Lunes 2 mar — Demo Final Sprint 1

**Flujo completo (grabado en video 3-5 min):**

1. ✅ **Setup inicial**
   - Mostrar que hay 3 usuarios:
     - user_admin (role=ADMIN)
     - user_consultant (role=CONSULTANT)
     - user_client (role=CLIENT)
   - Mostrar que hay 2 proyectos creados

2. ✅ **Login y JWT**
   - POST `/api/token/` con user_consultant
   - Copiar access token

3. ✅ **Permisos por rol**
   - Con token de CONSULTANT:
     - GET `/api/projects/` → funciona
     - POST `/api/projects/` → funciona (puede crear)
   - Con token de CLIENT:
     - GET `/api/projects/` → funciona (solo ve los suyos)
     - POST `/api/projects/` → 403 (no puede crear)

4. ✅ **ProjectUser**
   - Asignar user_client al Proyecto 1
   - Login como user_client
   - GET `/api/projects/` → debe ver SOLO Proyecto 1

5. ✅ **AuditLog**
   - Crear un nuevo proyecto
   - GET `/api/audit-logs/?entity_type=Project`
   - Mostrar que aparece el registro con timestamp y user

**Checklist técnico final:**

- [ ] AUTH_USER_MODEL está en settings
- [ ] SimpleJWT instalado y configurado
- [ ] Tiempo de expiración de tokens configurado (access: 15min, refresh: 1 día)
- [ ] Todos los ViewSets usan IsAuthenticated como mínimo
- [ ] Permisos personalizados aplicados a Users, Companies, Projects
- [ ] Modelo ProjectUser creado y funcionando
- [ ] AuditLog registra automáticamente via signals
- [ ] Signals registrados en apps.py
- [ ] No hay errores en consola al correr servidor
- [ ] requirements.txt actualizado

**Documentación:**

- [ ] README tiene sección "Autenticación" explicando login
- [ ] README lista los 3 roles y sus permisos
- [ ] Endpoints documentados con permisos requeridos
- [ ] Ejemplo de request con token en header

**Assets entregables:**

- [ ] Video de 3-5 min mostrando flujo completo
- [ ] 3-5 screenshots clave (login, 403, AuditLog, ProjectUser)
- [ ] Tag en Git: `v0.1-sprint1-complete`
- [ ] Pull Request o branch: `sprint-1-auth-jwt`

---

## 🎯 Criterios de éxito generales

Para considerar Sprint 1 **COMPLETO**, debes poder responder SÍ a estas preguntas:

### Seguridad:
- [ ] ¿Puedo hacer login y obtener token?
- [ ] ¿Los endpoints rechazan requests sin token?
- [ ] ¿Un usuario CLIENT no puede crear empresas ni proyectos?
- [ ] ¿Un usuario CONSULTANT puede crear proyectos?
- [ ] ¿Un usuario ADMIN puede hacer todo?

### ProjectUser:
- [ ] ¿Puedo asignar un usuario a un proyecto?
- [ ] ¿Un usuario solo ve los proyectos donde está asignado?
- [ ] ¿Un ADMIN ve todos los proyectos sin importar ProjectUser?

### AuditLog:
- [ ] ¿Se registra automáticamente cuando creo un proyecto?
- [ ] ¿Se registra cuando edito una tarea?
- [ ] ¿Se registra cuando borro una fase?
- [ ] ¿El log incluye quién hizo el cambio?
- [ ] ¿El log incluye timestamp?

### Técnico:
- [ ] ¿El servidor arranca sin errores?
- [ ] ¿Las migraciones están aplicadas?
- [ ] ¿No hay warnings de seguridad obvios?
- [ ] ¿El código está en Git con commits descriptivos?

---

## 🚦 Semáforo de control (para ti)

### 🟢 Verde (todo bien, seguir)
- Todos los checkpoints cumplidos
- Demos funcionan sin errores
- Commits regulares (3+ por semana por dev)
- Equipo responde preguntas correctamente

### 🟡 Amarillo (revisar, posible retraso)
- 1-2 checkpoints fallidos
- Demo funciona pero con bugs menores
- Commits irregulares (menos de 3 por semana)
- Equipo tiene dudas conceptuales

**Acción:** Reunión extra de 30 min para resolver dudas

### 🔴 Rojo (intervenir, retraso crítico)
- 3+ checkpoints fallidos
- Demo no funciona
- Menos de 2 commits por dev en la semana
- Equipo bloqueado sin avanzar

**Acción:** Parar, revisar plan, posible reasignación de tareas

---

## 💬 Preguntas frecuentes del equipo (y tus respuestas)

### "¿Tengo que borrar la base de datos?"
**Tu respuesta:** Si ya hiciste migraciones ANTES de configurar AUTH_USER_MODEL, sí. Si apenas estás empezando, perfecto momento para hacerlo limpio.

### "¿Por qué AbstractUser y no AbstractBaseUser?"
**Tu respuesta:** AbstractUser incluye username, email, etc. ya implementados. AbstractBaseUser es para casos muy custom. Para VIT, AbstractUser es suficiente.

### "¿Dónde guardo el token en el frontend?"
**Tu respuesta:** Eso es para el dev de frontend (Sprint 1 frontend). Por ahora, solo prueben con Postman guardando el token manualmente.

### "¿SimpleJWT es la única opción?"
**Tu respuesta:** No, pero es la más usada y mejor documentada en Django. Knox es alternativa, pero SimpleJWT es estándar.

### "¿Tengo que hacer tests?"
**Tu respuesta:** Por ahora, tests manuales están bien. En Sprint 2-3 agregamos tests automatizados.

### "¿ProjectUser es obligatorio?"
**Tu respuesta:** SÍ. Es lo que diferencia tu sistema de un simple gestor de proyectos. Es clave para ISO 27001 (roles por proyecto).

### "¿AuditLog debe guardar JSON o solo texto?"
**Tu respuesta:** Ideal es JSONField para guardar qué campos cambiaron. Si es complejo, al menos timestamp + action + user es suficiente para Sprint 1.

---

## 📞 Cuándo contactarme (como tutor)

Contacta si:
- ❌ Llevan 2+ horas bloqueados en el mismo error
- ❌ Van 3 días y no tienen ningún checkpoint cumplido
- ❌ Necesitan decidir entre 2 enfoques técnicos
- ✅ Quieren validar que van por buen camino

**NO** me contactes para:
- ❌ Errores de sintaxis (eso se busca en Google)
- ❌ "¿Está bien este código?" sin contexto (muéstrame el error o la duda específica)
- ❌ Pedir código completo (soy tutor, no ghost-coder)

---

**Próximo paso:** Una vez completo Sprint 1, pasamos a **Sprint 2 — Scope + Assets** 🚀
