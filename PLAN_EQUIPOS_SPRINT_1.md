# 🎯 Definición de Roles y Responsabilidades — VIT Project

**Proyecto:** VIT — Plataforma SGSI ISO 27001  
**Equipo:** 3 desarrolladores  
**Duración:** 18 feb → 15 may  
**Objetivo:** Implementar plataforma completa de gestión SGSI con Auth, riesgos, SoA, evidencias y reportes

---

## ⚠️ PRINCIPIO FUNDAMENTAL: LAS DECISIONES DE HOY CONDICIONAN RENDER

**ESTO ES CRÍTICO DESDE EL LUNES 24 FEB:**

Cada decisión técnica que toman Osky y Tinky DEBE tener en mente que en Mayo esto corre en **Render (backend) + Vercel (frontend) + PostgreSQL 15 (managed)**. 

**NO es "hacemos en desarrollo y después adaptamos para producción".**

Es "**hacemos EN DESARROLLO de forma que ya funcione en Render sin cambios posteriores**".

Esto significa:
- PostgreSQL local versión 15, NUNCA SQLite
- JWT configurado con Secure + HttpOnly + SameSite desde Sprint 1, no Sprint 6
- Settings con `development.py` y `production.py` desde DÍA 1
- Variables en .env siempre, NUNCA hardcodeadas
- Validaciones y migraciones reversibles (porque la BD en Render es real)

**Arquitecto valida esto:** Cada PR debe mostrar consideración para Render. Si hay "TODO: hacer seguro en producción", mereca es rechazada.

---

## 📋 Estructura del equipo

Tenemos 3 roles claramente definidos para evitar overlaps y asegurar que cada parte crítica del proyecto tenga propiedad y calidad.

---

## 👤 ROL 1: Arquitecto + Líder Técnico + Backend Core (3pleJ)

### Responsabilidades principales

**Diseño y especificaciones:**
- Definir estructura de datos (modelos, relaciones, validaciones)
- Diseñar permisos y control de acceso por rol
- Definir flujos de negocio SGSI ISO 27001
- Tomar decisiones técnicas críticas (JWT vs OAuth, JSONField vs texto, etc.)
- Documentar especificaciones para que Backend Implementador las siga al pie

**Implementación de componentes core:**
- Implementar modelos complejos (User AbstractUser, permisos, ProjectUser, AuditLog)
- Implementar lógica de negocio crítica (cálculo de riesgos, generación SoA, scoring)
- Diseñar estructura de signals y validaciones automáticas

**Code review y governance:**
- Revisor obligatorio de TODOS los PRs (validar que el código siga especificaciones)
- Validar que se respete la arquitectura definida
- Aprobar/rechazar cambios arquitectónicos
- Dar feedback técnico constructivo

**Dirección:**
- Resolver bloqueadores técnicos de Osky y Tinky
- Ajustar plan si hay cambios de requerimientos
- Coordinar entregas entre backend y frontend

### Qué NO hace este rol (para eficiencia)

❌ NO escribe todos los serializers (Osky los implementa)  
❌ NO escribe todos los endpoints (Osky los implementa)  
❌ NO hace toda la UI (Tinky lo hace)  
❌ NO corrige bugs menores (Osky arregla tras review)  

### Tiempo estimado por semana

- Lunes: 30 min (diseño de especificaciones de la semana)
- Miércoles: 30-45 min (code review de PRs)
- Viernes: 30 min (demo y validación de criterios)
- Esporádico: resolución de bloqueadores

**Total esperado:** 2-3 horas por semana (gestión + revisión)

---

## 👨‍💻 ROL 2: Backend Implementador (Osky)

### Responsabilidades principales

**Implementación de especificaciones:**
- Crear modelos exactamente como están documentados (sin improvisos)
- Crear serializers y views para endpoints
- Implementar lógica definida en especificaciones
- Conectar signals y validaciones según diseño

**Testing y calidad:**
- Tests unitarios para modelos
- Tests para endpoints (validar auth, permisos, comportamiento)
- Validar endpoints localmente (Postman) antes de PR
- Reportar bugs encontrados

**Comunicación:**
- Si algo NO está claro en la especificación → preguntar (no adivinar)
- Reportar si una especificación no es técnicamente viable
- Hacer PRs descriptivos que enlacen a la especificación

### Qué NO es responsabilidad de Backend Implementador

❌ NO diseña arquitectura (eso está predefinido)  
❌ NO cambia modelos sin pasar por especificación  
❌ NO deixa endpoints sin validación/permisos "por ahora"  
❌ NO improvisa soluciones creativas a problemas definidos  

### Entregables esperados

| Periodicidad | Métrica | Estándar |
|---|---|---|
| Diario | Código que compila | 0 errores de sintaxis |
| Por semana | Commits | 3+ commits significativos |
| Por semana | PRs | 1-2 PRs descriptivos |
| Viernes | Demo | Feature funcionando en Postman/Thunder |

---

## 🎨 ROL 3: Frontend Developer (Tinky)

### Responsabilidades principales

**Interfaz de usuario:**
- Crear componentes React reutilizables
- Crear páginas/vistas (Login, Dashboard, Proyectos, etc.)
- Conectar con endpoints que Backend define

**Integración con backend:**
- Consumir APIs usando axios
- Manejar estados de loading y error
- Respetar estructura de respuestas que Backend entrega
- Reportar si un endpoint no cumple especificación

**Testing básico:**
- Componentes renderizan sin crashes
- Requests a APIs funcionan
- Validar en navegador

### Qué NO es responsabilidad de Frontend Developer

❌ NO diseña la API (Backend/Arquitecto lo hacen)  
❌ NO cambia endpoints ("úsalos tal como están")  
❌ NO decide modelos de datos  
❌ NO implementa permisos backend  

### Entregables esperados

| Periodicidad | Métrica | Estándar |
|---|---|---|
| Diario | React sin errores | 0 crashes en console |
| Por semana | Commits | 3+ commits significativos |
| Por semana | PRs | 1-2 PRs descriptivos |
| Viernes | Demo | Páginas funcionando en navegador |

---

### Revisión Miércoles (Asincrónica)

**Propiedad:** Arquitecto

**Proceso:**
- Osky abre PR con cambios
- Arquitecto revisa y comenta (max 4 horas después)
- Osky arregla si hay cambios solicitados
- Nada se mergea sin aprobación de Arquitecto
- Tinky también entrega PRs en paralelo

---

### Demo y Validación Viernes (Obligatoria, 45 min)

**Asisten:** Arquitecto, Osky, Tinky  
**Duración:** 45 minutos

**Parte 1: Demo en vivo (20 min)**
- Backend Implementador: muestra en Postman qué features funcionan
- Frontend Developer: muestra en navegador qué pantallas funcionan
- Regla: no vale "casi listo", debe verse ejecutando

**Parte 2: Validación Técnica (15 min)**
- Arquitecto hace preguntas de control
- Valida que entiendan lo que hicieron
- Identifica bloqueadores para la semana siguiente

**Parte 3: Ajustes (10 min)**
- Define tareas claras para semana próxima
- Clarifica dudas antes de que terminen

---

## 🚨 Reglas no negociables

### 1. Código en Git

**Todos los cambios van a Git.**

- NO código en email
- NO código en Drive
- NO "te lo paso después"

Esto facilita la revisión de código y el control de versiones.

### 2. Pull Requests obligatorios

**Cada cambio es un PR** (mínimo 1-2 por semana por persona)

**Regla:** Nada se mergea sin revisión del Arquitecto  

**Proceso:**
- Quien hace cambios abre PR con descripción
- Enlaza a la especificación que está implementando
- Arquitecto revisa y aprueba o pide cambios
- Cambios se aplican, luego se mergea

---

### 3. Commits regularmente

**Mínimo 3 commits por semana por persona**

Commits pequeños y descriptivos (no gigantes):

```
git commit -m "feat: Crear modelo ProjectUser"
git commit -m "feat: Agregar endpoint /project-users/"
git commit -m "fix: Validar unique_together en ProjectUser"
```

---

### 4. PR con descripción clara

**Template mínimo:**

```
## Qué implementa este PR
- Modelo Risk con campos inherente/residual
- Endpoint POST /risks/
- Signal para cálculo automático de score

## Estado
- [x] Sigue especificación
- [x] Tests pasan
- [x] Sin errores obvios

## Enlace a tarea/especificación
Ver SPRINT_1_GUIA_BACKEND.md Día 3
```

---

### 5. Demo es obligatoria

**Todos los viernes, en pantalla funcionando**

Si no se puede demostrar ejecutando, no está listo.

---

### 6. Feedback objetivo (no personal)

Al hacer code review:
- ✅ "Este endpoint falta validar"
- ✅ "No veo dónde se captura el error"
- ❌ "Código malo"

---

## 💡 Cultura de trabajo

### Confianza basada en estructura

El sistema de demostración, commits y PRs NO es desconfianza.

Es gobierno real de proyecto:
- Commits regulares = evidencia de trabajo
- PRs = revisión de calidad
- Demos = validación de que funciona
- Preguntas técnicas = asegurar que entiendan

Eso es profesionalismo.

---

### Protocolo cuando alguien se bloquea

1. Escriben en el chat: "Estoy bloqueado en X"
2. Arquitecto responde en máximo 4 horas
3. Si Arquitecto no puede resolver, escala al profesor

**Nunca:** "esperar a que se le ocurra qué hacer"

---

### Si alguien no cumple

**Semana 1:** Feedback directo, sin drama  
**Semana 2:** Reunión 1-1 para entender qué falta  
**Semana 3:** Reestructuración de tareas si es necesario

---

## 📊 Responsabilidades por rol (resumen)

| Entregable | Arquitecto | Backend Dev | Frontend Dev |
|---|---|---|---|
| **Por semana** | Especificación clara | 3+ commits, 1-2 PRs | 3+ commits, 1-2 PRs |
| **Viernes demo** | Preguntas técnicas | Feature en Postman | Página en navegador |
| **Miércoles** | Code review (4h max) | PRs en Git | PRs en Git |
| **Respuesta a bloqueos** | Max 4 horas | Report en chat | Report en chat |

---

## 🎯 Éxito significa

- ✅ Cada quien sabe exactamente qué hace
- ✅ No hay sorpresas el viernes
- ✅ Todo está en Git (evidencia de trabajo)
- ✅ Demos muestran funcionalidad real
- ✅ Código sigue estándar de calidad

---

**Próximo paso:** Cada miembro del equipo lee su rol completo. Luego: preguntas en el chat.

Discord/email es para bloqueadores urgentes. Las dudas de clarificación se resuelven en reuniones programadas.
