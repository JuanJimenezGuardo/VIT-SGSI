# 📋 Asignaciones por Sprint (Sprint 1-6)

Desglose día a día y semana a semana de qué construye cada rol. Esto se actualiza cada lunes en la reunión.

**IMPORTANTE:** Todos los sprints están condicionados por la arquitectura de producción definida en `ARQUITECTURA_DESPLIEGUE_PRODUCCION.md`. Cada decisión técnica debe considerar su impacto en el deployment final.

---

## ✅ SPRINT 1 (19 feb → 2 mar) — Seguridad Base + Auth [COMPLETADO]

Objetivo: Pasar de "API abierta" a "plataforma con control de acceso real" ✅ LOGRADO

### Arquitecto (3pleJ)

**Semana 1 (19-23 feb):**
- [x] Diseñar estructura de permisos (Admin, Consultant, Client)
- [x] Diseñar modelo ProjectUser y sus relaciones
- [x] Diseñar estructura mínima de AuditLog
- [x] Documentar en SPRINT_1_GUIA_BACKEND.md (paso a paso)
- [x] Decisión: JWT vs OAuth (documentar por qué JWT)

**Semana 2 (24-28 feb):**
- [x] Implementar modelo User (migrar a AbstractUser)
- [x] Crear clases de permiso (IsAdmin, IsConsultant, IsClient y 3 más)
- [x] Crear modelo ProjectUser con serializer + viewset
- [x] Implementar signals para AuditLog básico
- [x] Code review: Revisar +2 PRs de Osky
- [x] Hacer los ajustes que POS-review requieran

**Semana 3 (1-2 mar):**
- [x] Validar arquitectura final
- [x] Hacer ajustes si es necesario (no quedó falta)
- [x] Preparar demo del sprint

**Output esperado:**
- ✅ User model hereda de AbstractUser
- ✅ JWT funcionando: `/api/token/` devuelve access+refresh (15min + 1day)
- ✅ 6 clases de permiso creadas y aplicadas
- ✅ ProjectUser: CRUD funcionando con filtrado por rol
- ✅ AuditLog: registra CREATE/UPDATE/DELETE automáticamente
- ✅ 0 errores 500 en endpoints
- ✅ Demo data: 3 usuarios, 2 empresas, 2 proyectos
- ✅ Test suite: backend/tests/test_demo_sprint1.py (5 scenarios passing)

---

### Backend Implementador (Osky)

**Semana 1 (19-23 feb):**
- [x] Leer SPRINT_1_GUIA_BACKEND.md completo
- [x] Configurar AbstractUser en models.py
- [x] Instalar SimpleJWT (`pip install djangorestframework-simplejwt`)
- [x] Configurar settings.py (AUTH_USER_MODEL, REST_FRAMEWORK)
- [x] Configurar urls.py (`/api/token/` y `/api/token/refresh/`)
- [x] Hacer 3+ commits de esto

**Semana 2 (24-28 feb):**
- [x] Crear modelo ProjectUser (user, project, role, unique_together)
- [x] Crear serializer y viewset para ProjectUser
- [x] Crear endpoint `/api/project-users/` con filtrado por rol
- [x] Tests básicos: crear, leer, validations
- [x] Implementar signals para AuditLog (10 receivers)
- [x] PR al viernes (Arquitecto revisa)
- [x] Hacer 3+ commits

**Semana 3 (1-2 mar):**
- [x] Ajustes post-review (no había)
- [x] Demo: mostrar en Postman:
  - ✅ Login → recibe tokens (3 roles)
  - ✅ Endpoint sin token → 401
  - ✅ Endpoint con token → funciona
  - ✅ ProjectUser CRUD → funciona
  - ✅ AuditLog automático → validado

**Output esperado:**
- ✅ AbstractUser migrado sin errores
- ✅ JWT tokens generados y funcionales (15min access + 1day refresh)
- ✅ ProjectUser con validaciones y filtrado por rol
- ✅ AuditLog guardando eventos automáticamente
- ✅ 12+ commits con mensajes descriptivos
- ✅ 3 PRs documentadas
- ✅ 0 errores en endpoints

---

### Frontend Developer (Tinky)

**Semana 1 (19-23 feb):**
- [ ] Crear página Login
- [ ] Crear PrivateRoute (proteger rutas)
- [ ] Crear layout base (header, sidebar)
- [ ] Conectar login con `/api/token/` (backend listo ✅)
- [ ] Guardar token en localStorage
- [ ] 3+ commits

**Semana 2 (24-28 feb):**
- [ ] Crear página "Mis Proyectos"
- [ ] Conectar con GET `/api/projects/` (backend listo ✅)
- [ ] Crear página "Detalle Proyecto"
- [ ] Button "Crear Proyecto" (POST listo en backend ✅)
- [ ] PR al viernes
- [ ] 3+ commits

**Semana 3 (1-2 mar):**
- [ ] Ajustes post-review (si hay)
- [ ] Demo: mostrar en navegador:
  - Login → redirecciona a Dashboard
  - Sin token → redirecciona a Login
  - Lista de proyectos visible
  - Detalle abre

**Output esperado (en progreso):**
- ⏳ Login funciona y guarda token
- ⏳ Rutas protegidas redirigen
- ⏳ Dashboard lista proyectos
- ⏳ 3+ commits por semana
- ⏳ 1-2 PRs descriptivos
- ⏳ 0 crashes en React

**Backend Ready for Integration:** ✅ Todos los endpoints listos

---

### 🏭 **Impacto en Producción (Sprint 1)**

Este sprint sienta las bases de seguridad para producción:

- **JWT Cookies:** Configurarlas como `Secure`, `HttpOnly`, `SameSite=Strict` (no solo en prod, hacerlo ahora)
- **CORS:** Definir orígenes específicos desde el inicio (Render backend vs Vercel frontend)
- **Variables de Entorno:** Todas las credenciales NUNCA en código (usar .env desde Sprint 1)
- **Settings por Entorno:** Crear `settings/development.py` y `settings/production.py` ahora (no al final)
- **Database:** PostgreSQL local igual a producción (misma versión, mismas validaciones)
- **Tests en CI:** Configurar GitHub Actions para que corra tests antes de merge
- **SECRET_KEY:** Generar y proteger, nunca hardcodear
- **Debug en Logs:** Usar logging strukturado (no prints), facilita análisis en producción

**Acción:** Leer ARQUITECTURA_DESPLIEGUE_PRODUCCION.md §"Configuración Django para Producción"

---

---

## ✅ SPRINT 2 (3-16 mar) — Scope + Assets (SGSI Base)

### Arquitecto (3pleJ)

**Semana 1 (3-7 mar):**
- [ ] Diseñar modelo Scope (alcance, exclusiones, justificación, estado)
- [ ] Diseñar modelo Asset (inventario, denominación, clasificación, propietario)
- [ ] Definir validaciones (un asset siempre tiene un proyecto)
- [ ] Definir relación Scope ↔ Project (1-N)
- [ ] Documentar en README

**Semana 2 (10-14 mar):**
- [ ] Revisar implementación de Osky
- [ ] Code review de Scope + Asset models
- [ ] Validar que endpoints sean correctos

**Semana 3 (16 mar):**
- [ ] Demo

---

### Backend Implementador (Osky)

**Semana 1 (3-7 mar):**
- [ ] Crear modelo Scope (siguiendo especificación definida)
- [ ] Crear modelo Asset (siguiendo especificación definida)
- [ ] Crear serializers
- [ ] Crear viewsets
- [ ] Endpoints: `/api/scopes/`, `/api/assets/`

**Semana 2 (10-14 mar):**
- [ ] Tests básicos
- [ ] PR al viernes
- [ ] Code review → arreglar si Tú sugiere cambios

**Semana 3 (16 mar):**
- [ ] Demo

---

### Frontend Developer (Tinky)

**Semana 1 (3-7 mar):**
- [ ] Crear página "Alcance del Proyecto"
- [ ] Crear página "Inventario de Activos"
- [ ] Ambas con tabs en el detalle del proyecto

**Semana 2 (10-14 mar):**
- [ ] CRUD: crear, editar, listar, borrar (Scope y Asset)
- [ ] Formularios con validación básica
- [ ] PR al viernes

**Semana 3 (16 mar):**
- [ ] Demo

---

### 🏭 **Impacto en Producción (Sprint 2)**

- **Migraciones Reversibles:** Todos los cambios de modelo deben ser migrables forward y backward
- **Validaciones en BD:** No confiar solo en Django ORM, agregar constraints en PostgreSQL
- **Relaciones Normalizadas:** Diseño de BD limpio = no problemas en prod
- **Indexación:** Pensar en queries lentas ahora, indexar desde el inicio (Scope.project, Asset.scope)
- **Testing de Migraciones:** Cada migration debe testearse localmente antes de production
- **N+1 Queries:** Usar `select_related()` y `prefetch_related()` desde el inicio para DRF

---

---

## ✅ SPRINT 3 (17-30 mar) — Riesgos (CRÍTICO PARA NOTA)

### Arquitecto (3pleJ)

**Semana 1 (17-21 mar):**
- [ ] Diseñar modelo Risk (TODO DETALLADO)
  - [ ] Campos inherentes: prob (1-5), impact (1-5), score
  - [ ] Campos residuales: prob, impact, score
  - [ ] Tratamiento: Aceptar/Mitigar/Transferir/Evitar
  - [ ] Score = probabilidad × impacto
- [ ] Diseñar relación Risk ↔ Asset (N:M)
- [ ] Documentar fórmula en README (1 página mínimo)
- [ ] Validaciones de negocio

**Semana 2 (24-28 mar):**
- [ ] Revisar implementación de modelo Risk
- [ ] Revisar cálculo automático de scores
- [ ] Revisar relación N:M correcta

**Semana 3 (30 mar):**
- [ ] Demo

---

### Backend Implementador (Osky)

**Semana 1 (17-21 mar):**
- [ ] Crear modelo Risk según especificación del Arquitecto
- [ ] Campos: descripción, causa, consecuencia, dueño, fechas, estado
- [ ] Relación N:M Risk ↔ Asset
- [ ] Signal automático: cuando cambias "tratamiento" → recalcula "residual"

**Semana 2 (24-28 mar):**
- [ ] Crear serializer Risk (con scores calculados)
- [ ] Crear viewset Risk
- [ ] Endpoint: `/api/projects/{id}/risks/`
- [ ] Tests (validar que scores se calculan)
- [ ] PR

**Semana 3 (30 mar):**
- [ ] Ajustes, demo

---

### Frontend Developer (Tinky)

**Semana 1 (17-21 mar):**
- [ ] Página "Riesgos" en detalle proyecto
- [ ] Tabla de riesgos con score (mostrando inherit y residual)
- [ ] Columnas: descripción, probabilidad, impacto, score, estado

**Semana 2 (24-28 mar):**
- [ ] Form crear riesgo
- [ ] Asociar activos (multiselect)
- [ ] Form editar tratamiento
- [ ] Mostrar cambio automático de score residual
- [ ] PR

**Semana 3 (30 mar):**
- [ ] Demo

---

### 🏭 **Impacto en Producción (Sprint 3)**

Los riesgos son cálculos críticos en SGSI:

- **Cálculos Determinísticos:** Score = Prob × Impact, NUNCA cambiar fórmula después de producción
- **Signals Thread-Safe:** Si usas signals para recalcular scores, deben ser atomic y no race conditions
- **Audit Trail:** Todos cambios de score deben estar en AuditLog (quién, cuándo, por qué)
- **Reportabilidad:** Datos de riesgos son base de reportes para auditoría, ningún harddelete
- **Performance:** Con 1000+ riesgos, queries deben ser optimizadas (indexes, caching)

**Acción:** Leer ARQUITECTURA_DESPLIEGUE_PRODUCCION.md § "Logging Estructurado"

---

---

## ✅ SPRINT 4 (31 mar - 13 abr) — SoA + ISO Controls

### Arquitecto (3pleJ)

**Semana 1 (31 mar - 4 abr):**
- [ ] Diseñar modelo ISOControl (solo lectura, 93 controles)
- [ ] Diseñar modelo SoAItem (aplicabilidad, estado, justificación)
- [ ] Decidir: SoA generado automático vs botón "generar"
- [ ] Documentar estructura

**Semana 2 (7-11 abr):**
- [ ] Revisar carga de 93 controles
- [ ] Validar generación automática de SoA
- [ ] Code review

---

### Backend Implementador (Osky)

**Semana 1 (31 mar - 4 abr):**
- [ ] Crear modelo ISOControl (campos: código, nombre, descripción)
- [ ] Crear fixture con 93 controles ISO 27001 (CSV o JSON)
- [ ] `python manage.py loaddata iso_controls.json`

**Semana 2 (7-11 abr):**
- [ ] Crear modelo SoAItem
- [ ] Crear signal: cuando creas Project → genera SoAItem para TODOS los ISOControl
- [ ] Crear serializer y viewset SoAItem
- [ ] Endpoint: `/api/projects/{id}/soa/`
- [ ] PR

---

### Frontend Developer (Tinky)

**Semana 1 (31 mar - 4 abr):**
- [ ] Página "SoA" en detalle proyecto
- [ ] Lista de 93 controles

**Semana 2 (7-11 abr):**
- [ ] Checkbox "aplicable"
- [ ] Campo "justificación" (textarea)
- [ ] Dropdown "estado" (No aplicable/Sin implementar/En proceso/Implementado)
- [ ] Guardar cambios
- [ ] Buscar/filtrar controles
- [ ] PR

---

### 🏭 **Impacto en Producción (Sprint 3)**

- **Cálculo de Riesgos en Prod:** La fórmula (prob × impacto) debe ser idéntica en dev y prod
- **Datos Masivos:** 93 controles × múltiples proyectos = cuidado con queries lentas
- **Caching:** Considerar cachear los 93 controles (no cambian frecuentemente)
- **Auditlog de Cambios:** Cada Risk o SoAItem modificado debe auditar (quién, cuándo, qué cambió)
- **Archivos Adjuntos:** Si Risk puede tener evidencias, planificar almacenamiento persistente

---

### 🏭 **Impacto en Producción (Sprint 4)**

- **Datos de Referencia:** Los 93 ISOControls son datos de solo lectura, versionar en BD
- **Generación SoA:** Si es automática, testear que genera correctamente con 1000 controles
- **Truncamiento de Texto:** Justificaciones largas deben validarse (no es charla, es auditoría)
- **Indexación SoA:** Búsquedas por control_code deben ser rápidas (index en lookup)

---

---

## ✅ SPRINT 5 (14-27 abr) — Evidencias + Auditoria Completa

### Arquitecto (3pleJ)

**Semana 1 (14-18 abr):**
- [ ] Diseñar modelo Evidence (archivo, estado, fecha)
- [ ] Diseñar estados: Pendiente/Aprobado/Rechazado
- [ ] Relación Evidence ↔ SoAItem

**Semana 2 (21-25 abr):**
- [ ] Revisar subida de archivos
- [ ] Validar AuditLog completo (Risk, SoAItem, Evidence, Document)
- [ ] Code review

---

### Backend Implementador (Osky)

**Semana 1 (14-18 abr):**
- [ ] Crear modelo Evidence (file, status, uploaded_at, uploaded_by)
- [ ] Implementar subida de archivo
- [ ] Validar que Evidence está vinculada a SoAItem

**Semana 2 (21-25 abr):**
- [ ] Crear serializer y viewset
- [ ] Endpoint: `/api/projects/{id}/evidence/`
- [ ] Endpoint: cambiar estado de evidence
- [ ] Extender AuditLog a Evidence, Risk, SoAItem
- [ ] PR

---

### Frontend Developer (Tinky)

**Semana 1 (14-18 abr):**
- [ ] Página "Evidencias" en detalle proyecto
- [ ] Tabla con evidencias (archivo, estado, fecha)

**Semana 2 (21-25 abr):**
- [ ] Button subir evidencia (input file)
- [ ] Mostrar estado (badge de color)
- [ ] Tabla de logs (quién cambió qué y cuándo)
- [ ] PR

---

### 🏭 **Impacto en Producción (Sprint 5)**

**CRÍTICO:** Este sprint define cómo se manejan archivos en producción.

- **No usar Filesystem Local:** Render tiene filesystem efímero (desaparece en redeploy)
- **Almacenamiento Persistente:** Usar S3 compatible (Supabase Storage o AWS S3)
- **Validación de Archivos:** 
  - Máximo 50MB por archivo
  - Solo tipos permitidos: PDF, DOCX, XLSX, JPG, PNG
  - Validar MIME type en servidor (no confiar en extensión)
- **Virus Scan:** Considerar VirusTotal API para archivos críticos
- **Acceso Controlado:** Las evidencias son confidenciales, acceso solo a usuarios autorizados
- **Download mediante Token:** No exponer URLs de S3 directamente (usar signed URLs con expiracion)
- **AuditLog Completo:** Quién subió, quién descargó, cuándo, desde dónde
- **Encriptación:** S3 con encriptación en reposo
- **Backups:** Asegurar que S3 tiene backups automáticos

**Config Django:** Ver ARQUITECTURA_DESPLIEGUE_PRODUCCION.md §"Almacenamiento (Evidencias)"

---

---

## ✅ SPRINT 6 (28 abr - 11 may) — Reportes + Dashboard

### Arquitecto (3pleJ)

**Semana 1 (28 abr - 2 may):**
- [ ] Definir qué incluye Report
- [ ] Definir métricas clave:
  - % controles con evidencia
  - # riesgos altos
  - % tareas completadas
- [ ] Estructura JSON

**Semana 2 (5-9 may):**
- [ ] Revisar endpoints de métricas
- [ ] Code review

---

### Backend Implementador (Osky)

**Semana 1 (28 abr - 2 may):**
- [ ] Crear modelo Report
- [ ] Crear endpoint `/api/projects/{id}/metrics/` que devuelva:
  ```json
  {
    "control_compliance": "45%",
    "high_risks": 3,
    "tasks_completed": "60%",
    "soa_status": "15/93 implementados"
  }
  ```

**Semana 2 (5-9 may):**
- [ ] Crear endpoint para generar Report
- [ ] Tests básicos
- [ ] PR

---

### Frontend Developer (Tinky)

**Semana 1 (28 abr - 2 may):**
- [ ] Dashboard Consultant (mostrando proyectos, métricas)
- [ ] Dashboard Client (progreso, evidencias pendientes)

**Semana 2 (5-9 may):**
- [ ] Cards con métricas (% compliance, # riesgos, etc.)
- [ ] Gráficas básicas (progress bar, badges)
- [ ] Links rápidos a secciones principales
- [ ] PR

---

### 🏭 **Impacto en Producción (Sprint 6)**

- **Reportes en Prod:** Los reportes acceden a datos en vivo (no caché), queries optimizadas
- **Cálculo de Métricas:** NO hacer cálculos complejos en la request (lazy agregation)
- **Exportación PDF:** Si se exportan reportes a PDF, usar librería que no quebre (reportlab, weasyprint)
- **Carga de Datos:** En prod, 1000 proyectos × 93 controles = 93k registros, performance crítica
- **Paginación:** Todos los endpoints deben paginar (no devolver 10k registros de una)
- **Rate Limiting:** Endpoint de reportes puede ser costoso, limitar a 5 req/hora/usuario
- **Scheduling (Futuro):** Si los reportes son automáticos, usar Celery + Redis (no ahora, pero planificar)

---

---

## 📅 BUFFER (12-15 may) — QA + Demo Final

### Equipo Completo

- [ ] Pruebas completas (flujo end-to-end)
- [ ] Correcciones de bugs
- [ ] Crear datos demo (1 proyecto completamente llenadoconbdatos)
- [ ] Grabar video de 5-8 min (demo final)
- [ ] Documentación final
- [ ] Tag final: `v1.0-production-ready`

---

## 📊 Resumen: Tareas totales por rol

### Arquitecto + Líder Técnico (3pleJ)
- Sprint 1: Diseño Auth + permisos + ProjectUser + AuditLog + implementación User/permisos
- Sprint 2: Diseño Scope + Asset + validaciones
- Sprint 3: Diseño Risk (CRÍTICO) + fórmula + cálculos
- Sprint 4: Diseño SoA + fixture ISO 27001
- Sprint 5: Diseño Evidence + auditoría completa
- Sprint 6: Definir métricas
- **Total:** Diseño arquitectónico + implementación de core + code review todo

### Backend Implementador
- Sprint 1: Implementar JWT + ProjectUser + AuditLog signals
- Sprint 2: Scope + Asset
- Sprint 3: Risk + scoring automático
- Sprint 4: Fixtures + SoAItem automático
- Sprint 5: Evidence + upload
- Sprint 6: Métricas + Report
- **Total:** CRUD endpoints + signals + validaciones

### Frontend Developer
- Sprint 1: Login + layout + rutas protegidas
- Sprint 2: Scope UI + Asset UI
- Sprint 3: Riesgos UI + scoring visual
- Sprint 4: SoA UI + checkboxes
- Sprint 5: Evidencias UI + upload
- Sprint 6: Dashboards
- **Total:** Todas las páginas del sistema

---

## ✅ Verde/Amarillo/Rojo por sprint

### Sprint 1

**🟢 Verde:** User migrado, JWT funciona, ProjectUser creado, AuditLog registra  
**🟡 Amarillo:** JWT parcial o permisos incompletos  
**🔴 Rojo:** User no es AbstractUser, JWT no funciona, 0 PRs  

---

### Sprint 2

**🟢 Verde:** Scope + Asset modelos creados, endpoints funcionan, UI muestra datos  
**🟡 Amarillo:** Modelos creados pero con bugs, endpoints parciales  
**🔴 Rojo:** Scope o Asset no existen, UI no conecta  

---

### Sprint 3

**🟢 Verde:** Risk modelo completo, scoring automático funciona, UI muestra scores inherente y residual  
**🟡 Amarillo:** Modelo Risk existe pero scoring con bugs  
**🔴 Rojo:** Risk no existe, scoring no funciona, 0 commits  

---

### Sprint 4-6

Similar: modelos implementados ✅, endpoints funcionales ✅, UI visible ✅

---

**¿Dudas sobre tareas?** Pregúntale a los que correspondan, no hagas todo tú 😎
