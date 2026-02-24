# 🎯 Sistema de Monitoreo Sin Drama

El sistema de control del Arquitecto para seguimiento de avance **sin ser agresivo**, pero siendo claro y estructurado.

---

## ⚠️ VALIDACIÓN DE PRODUCTION-READINESS (CADA VIERNES)

El Arquitecto debe hacer estas preguntas adicionales cada viernes para asegurar que el código YA no solo funciona localmente, sino que está LISTO para Render:

**Preguntas críticas:**

1. ❓ "¿El código que escribiste dependería de SQLite o de PostgreSQL específicamente?"
   - Si responden "SQLite estaría bien": **BLOQUEADOR**
   - Si responden "PostgreSQL": ✅ Correctos

2. ❓ "¿Hay credentials, SECRET_KEY, o DB passwords hardcodeados en el código?"
   - Si responden "sí, están en settings.py": **BLOQUEADOR**
   - Si responden "todo en .env": ✅ Correctos

3. ❓ "¿En los endpoints con permiso [AllowAny], cuál es la justificación?"
   - Si responden "solo /api/token/ tiene AllowAny": ✅ Correctos
   - Si hay otros con AllowAny: **BLOQUEADOR**

4. ❓ "¿Probaste el código con PostgreSQL local o solamente con SQLite?"
   - Si responden "solo SQLite": **BLOQUEADOR**
   - Si responden "PostgreSQL 15": ✅ Correctos

5. ❓ "¿Los settings tienen development.py y production.py separados?"
   - Si responden "no, todo en un settings.py": **AVISAR** (refactorizar en siguiente sprint)
   - Si responden "sí, tenemos ambos": ✅ Correctos

**Si alguna respuesta es BLOQUEADOR:** Solicitar refactor antes de merge.

---

## 📅 Monitoreo Diario (sin necesidad de reunión)

### Lunes (planificación)

**El Arquitecto pregunta en chat:**
> "¿Qué tareas van a atacar esta semana?"

**Espera respuesta clara tipo:**
- Osky: "Voy con AbstractUser migration y JWT setup"
- Tinky: "Hago Login page y PrivateRoute"

**Si responden bien:** ✅ Se continúa con el plan  
**Si dicen "no sé":** El Arquitecto repasa los archivos ASIGNACIONES_SPRINT_1_A_6.md y PLAN_EQUIPOS_SPRINT_1.md

---

### Miércoles (mid-week checkpoint)

**El Arquitecto pregunta en chat:**
> "¿Qué completaron? ¿Links a commits?"

**Espera:**
- Osky: "Hice AbstractUser (commit 123), JWT setup (commit 456), falta settings configurar"
- Tinky: "Hice Login page (commit 789), PrivateRoute (commit 012)"

**Estándar:** mínimo 2 commits por persona a mitad de semana

**Si están en 0 commits:**
- 🟡 Amarillo: Reunión extra de 30 min para identificar bloqueador
- El Arquitecto pregunta: "¿Qué necesitas de mí?"

---

### Viernes (demo obligatoria)

**Reunión 45 min (todos):**

**Parte 1: Demo (20 min)**

Osky muestra:
- En Postman/Thunder: usuario login → devuelve tokens
- GET `/api/users/` SIN token → 401
- GET `/api/users/` CON token → funciona
- ¿ProjectUser creado y asignando usuarios?
- ¿AuditLog guardando eventos?

Tinky muestra:
- Login page en navegador
- Ingresa credenciales → redirecciona a Dashboard
- Sin token → redirecciona a Login
- Lista de proyectos visible

**Si no se puede mostrar en pantalla → NO está hecho.**

---

**Parte 2: Verificación (15 min)**

El Arquitecto les hace estas preguntas:

**A Osky:**
- [ ] "¿Cuántos commits hiciste?" (esperado: 3+)
- [ ] "Muestra el modelo User. ¿Hereda de AbstractUser?" (debe responder "sí")
- [ ] "¿Dónde está el archivo permissions.py?" (debe mostrar en repo)
- [ ] "¿ProjectUser tiene unique_together?" (debe responder "sí")
- [ ] "¿Los signals en AuditLog están registrados en apps.py?" (debe responder "sí")

**A Tinky:**
- [ ] "¿Cuántos commits hiciste?" (esperado: 3+)
- [ ] "¿El token se guarda en localStorage?" (debe responder "sí")
- [ ] "¿Qué pasa si intento acceder a /dashboard sin token?" (debe redireccionar a login)
- [ ] "¿Dónde está la llamada axios a /api/token/?" (debe mostrar archivo)

**A ambos:**
- [ ] "¿Hay algún bloqueador para la siguiente semana?" (El Arquitecto identifica si alguien necesita help)

---

**Parte 3: Ajustes (10 min)**

El Arquitecto decide basado en demo:

**Scenario 1: Todo funciona ✅**
> "Bien, la próxima semana focalizamos en [siguiente tarea]"

**Scenario 2: Hay bugs pequeños 🟡**
> "OK, estos cambios quedan para la próxima semana. Mientras, focalizamos en [otra tarea]"

**Scenario 3: No funciona nada o 0 commits 🔴**
> "Necesitamos reunión. ¿Qué necesitas de mí para desbloquear?"

---

## 📊 Dashboard de estado (para el Arquitecto)

Completa esto cada viernes post-demo para tener **vista general clara**.

### Sprint 1 — Estado General

| Criterio | Osky | Tinky | Notas |
|----------|------|-------|-------|
| Commits esta semana | 5 | 4 | ✅ Mín 3 |
| PRs abiertos/pendientes | 1 | 1 | Revisar hoy |
| User → AbstractUser | ✅ | - | Osky hizo migracion |
| JWT tokens | ✅ | - | Postman valida |
| Permisos por rol | ✅ | - | 3 clases creadas |
| ProjectUser | ✅ | - | Unique constraint agregado |
| AuditLog | ⏳ | - | Signals registrados, testing viernes |
| Login page | - | ✅ | Funciona, token guardado |
| Rutas protegidas | - | ✅ | PrivateRoute implementado |
| Demo resultado | ✅ | ✅ | Todo en pantalla |

**Interpretación:**
- ✅ = Listo, verificado
- ⏳ = En progreso, casi listo
- 🔴 = Bloqueado o no empezó

---

## 🚨 Semáforo de Riesgo

Cada viernes, después de la demo, marcar un color:

### 🟢 Verde (seguir igual)

**Condiciones:**
- [ ] Ambos tienen 3+ commits
- [ ] Demo funciona sin errores
- [ ] Responden correctamente tus preguntas técnicas
- [ ] No hay bloqueadores

**Acción:** "Continúen con siguiente tarea. Excelente ritmo."

---

### 🟡 Amarillo (revisar, posible retraso)

**Condiciones:**
- [ ] Uno tiene <3 commits (pero >0)
- [ ] Demo tiene bugs pequeños (UI no alineada, endpoint tarda, etc.)
- [ ] Alguna pregunta técnica no responden bien
- [ ] Hay 1 bloqueador identificado

**Acción:** "Reunión extra miércoles 30 min. ¿Qué necesitan?"

---

### 🔴 Rojo (intervenir, retraso crítico)

**Condiciones:**
- [ ] Alguien tiene 0-1 commits en la semana
- [ ] Demo no funciona o está vacía
- [ ] Ambos están bloqueados
- [ ] Respuestas vagas a preguntas técnicas (ej: "no sé dónde pongo eso")

**Acción:**
1. Reunión urgente (mismo viernes si es posible)
2. Preguntar: "¿Qué necesitan? ¿Horas? ¿Claridad en tareas? ¿Help conmigo?"
3. Reestructurar si es necesario (ej: dividir tarea diferente)

---

## 📋 Template: Reporte Semanal (para el Arquitecto)

Después de cada demo, llena esto:

```
## Semana X (fechas)

### Demo
- [ ] Osky mostró: (qué features funcionan)
- [ ] Tinky mostró: (qué UI funciona)
- [ ] Duración: XX min
- [ ] Problemas técnicos: ninguno / (describir)

### Commits
- Osky: X commits (links / primeras líneas)
- Tinky: X commits (links / primeras líneas)

### PRs
- Osky: X abierto/merged
- Tinky: X abierto/merged

### Respuestas técnicas
- Osky respondió bien: (preguntas) → ✅ / ⏳ / 🔴
- Tinky respondió bien: (preguntas) → ✅ / ⏳ / 🔴

### Bloqueadores
- [ ] Ninguno
- [ ] (describir si existen)

### Semáforo: 🟢 / 🟡 / 🔴

### Observaciones
(notas para próxima semana)
```

---

## 💬 Conversaciones de ejemplo (sin drama)

### Escenario 1: Todo bien

**Viernes 3:15 PM**

3pleJ: "¿Listos para demo?"

Osky: "Sí, tengo JWT y ProjectUser funcionando"

Tinky: "Sí, login y dashboard listos"

(Demuestran 10 min)

3pleJ: "Perfecto. Preguntas rápidas:
- Osky: ¿User hereda de AbstractUser? ✅
- Tinky: ¿Token se guarda? ✅
- Bloqueadores? No.
Excelente, la próxima semana Scope + Asset. Buen trabajo 🎉"

---

### Escenario 2: Hay un bug

**Viernes 3:15 PM**

3pleJ: "¿Listos?"

Osky: "Sí pero JWT tiene un bug pequeño, los tokens expiran muy rápido"

Tinky: "Sí, login funciona pero form de crear proyecto igual falta"

(Demuestran)

3pleJ: "Ok:
- Osky: ese bug (tokens expiran) lo dejas para lunes y el próximo viernes traes. Mientras continúa con ProjectUser.
- Tinky: Ignora crear proyecto por ahora, focalizate en rutas protegidas.
- Bloqueadores? No.
Bien, la próxima semana refinamos. Continuemos 💪"

---

### Escenario 3: Hay un bloqueador

**Miércoles 2:00 PM (via chat)**

Osky: "Estoy bloqueado. No entiendo cómo hacer AbstractUser sin romper las migraciones existentes."

3pleJ: "Ok, reunión a las 4 PM. Sácate 30 min."

(Reunión rápida)

3pleJ: "Borra db.sqlite3 y la carpeta migrations de users. Empieza limpio. ¿Entendés?"

Osky: "Ah ok, perfecto."

3pleJ: "Bien. Mándame commit cuando lo termines."

---

### Escenario 4: Alguien desapareció

**Viernes 3:15 PM**

3pleJ: "¿Listos para demo?"

Osky: "Yo traigo algo"

Tinky: "...." (no responde)

3pleJ: "Osky muestra tu trabajado. Tinky ¿dónde estás?"

Tinky: "Perdón, paracaídas. Apenas empezaba."

3pleJ: "Ok, pero de las 5 tareas que tenías, ¿hiciste alguna? Así validamos avance."

Tinky: "No, nada."

3pleJ: "Ok. Reunión el lunes. Te paso un plan más simple. ¿Necesitas ayuda mía o algo más?"

Tinky: "Sí, no entendía qué hacer con las rutas."

3pleJ: "Perfecto, el lunes te lo explico. Preparate leyendo PLAN_EQUIPOS_SPRINT_1.md."

(Lunes 3pleJ explica de nuevo, más simple)

---

## ✅ Checklist 3PLEJ como Líder

Cada viernes después de demo:

- [ ] Ambos demostraron en pantalla
- [ ] Preguntas técnicas → entienden lo que hicieron
- [ ] Commits visibles en Git
- [ ] PRs abiertos o merged
- [ ] Bloqueadores identificados
- [ ] Próximas tareas claras
- [ ] Color 🟢/🟡/🔴 asignado

**Tiempo total:** 45 min

---

## 📞 Cuándo el Arquitecto llama ayuda extra (profesora/tutor)

El Arquitecto contacta si:
- [ ] Ambos están 🔴 por más de 2 sprints
- [ ] Hay decisión arquitectónica que no sabe cómo resolver
- [ ] Un dev literalmente desapareció (no contactable)

**El Arquitecto NO contacta para:**
- [ ] "¿Este código está bien?" (eso es para code review tranquilo)
- [ ] Errores de sintaxis (Google)
- [ ] Un dev tiene un pequeño bug (eso ordenas en siguiente demo)

---

## 🎓 La lección de gestión real

Lo que estás haciendo (demo + commits + preguntas técnicas) es:

- ✅ Governance real
- ✅ No es micromanagement
- ✅ Es medir avance de verdad
- ✅ Es permitir que otros trabajen con libertad pero con estructura

Eso es lo que valora tu profesor.

No es "hice todo yo" (eso no impresiona).  
Es **"lideré un equipo para que hiciera un sistema SGSI profesional"** (eso SÍ impresiona).

---

**Siguiente paso:** El Arquitecto comparte estos 3 documentos con el Backend Implementador y Frontend Developer el lunes, y empiezan 😎

**¿Alguna duda sobre cómo monitorear sin drama?**
