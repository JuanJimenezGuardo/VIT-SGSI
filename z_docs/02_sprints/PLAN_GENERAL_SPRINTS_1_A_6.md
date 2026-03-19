# 📋 Plan General Sprints 1-6

Desglose día a día y semana a semana de qué construye cada rol. Esto se actualiza cada lunes en la reunión.
Responsable Backend core (Juan Jose Jimenez Guardo): Juan Jose Jimenez Guardo.

**IMPORTANTE:** Todos los sprints están condicionados por la arquitectura de producción definida en `ARQUITECTURA_DESPLIEGUE_PRODUCCION.md`. Cada decisión técnica debe considerar su impacto en el deployment final.

---

## ✅ SPRINT 1 (19 feb → 2 mar) — Seguridad Base + Auth [COMPLETADO]

Objetivo: Pasar de "API abierta" a "plataforma con control de acceso real" ✅ LOGRADO

Nota de cierre: el sprint se considera cerrado por cumplimiento de objetivos de seguridad backend. El frente de UI se continua en los sprints de integracion.

### Arquitecto (Juan Jose Jimenez Guardo)

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

### Frontend Developer (Luis)

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

**Estado frontend tras Sprint 1 (replanificado):**
- ⏳ Login y rutas protegidas en integracion progresiva
- ⏳ Dashboard y vistas de proyecto movidos al sprint de integracion
- ⏳ Estabilizacion de UI continua en roadmap posterior

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

## ✅ SPRINT 2 (11-24 mar) — BD + refactor + migraciones [CIERRE TECNICO COMPLETADO]

Nota: documento actualizado retrospectivamente al cierre tecnico de Sprint 2.

Objetivo: cerrar y validar el modelo de base de datos antes de abrir API y frontend.

Regla operativa del sprint:
- Se prioriza cierre de BD, pero se permiten cambios puntuales en API y frontend para validar el modelo y evitar retrabajo.
- Durante la etapa de cierre BD se evita abrir nuevas pantallas; se permiten solo ajustes puntuales para validar contrato de datos.

Alcance congelado de entidades:
- Company
- Contact
- Project
- ProjectUser
- ProjectContact
- Phase
- Task
- Document
- Asset (sin rediseño)

Cambios obligatorios de esquema:
- Company deja de ser dueno de contact_person y contact_position.
- Project, Phase y Task incorporan planned_start_date, planned_end_date, actual_start_date, actual_end_date.
- Task incorpora work_notes.
- Document entra como entidad formal de trazabilidad.

### Juan Jose Jimenez Guardo (Arquitectura + Backend core + implementacion)

**Semana 1:**
- [x] Implementar Contact
- [x] Implementar ProjectContact
- [x] Implementar validaciones de negocio y constraints criticos
- [x] Implementar serializers/viewsets minimos de Contact y ProjectContact

**Semana 2:**
- [x] Refinar contrato API para apertura minima
- [x] Cerrar checklist tecnico de backend core
- [x] Aprobar cierre tecnico del sprint

### Backend Implementador (Osky)

**Semana 1:**
- [x] Implementar Document
- [x] Agregar campos planned/actual en Project, Phase y Task
- [x] Agregar work_notes en Task
- [x] Crear migraciones estructurales

**Semana 2:**
- [x] Ejecutar data migration legacy Company -> Contact
- [x] Validar constraints y relaciones
- [x] Resolver issues de migracion sin abrir API

### Frontend Developer (Luis)

**Semana 1-2:**
- [x] Congelar nuevas pantallas durante etapa de cierre BD
- [x] Atender solo bugs criticos
- [x] Preparar mapeo de pantallas contra contrato de datos final
- [x] Iniciar integracion cuando la BD este estable; la aprobacion formal se registra al cierre tecnico

### Plan diario por persona (Sprint 2)

| Dia | Juan Jose Jimenez Guardo (Backend core + arquitectura) | Osky (Backend persistencia) | Luis (Frontend) |
| --- | --- | --- | --- |
| Dia 1 | Cerrar modelo final y arrancar Contact | Preparar base de migraciones y campos planned/actual | Congelar nuevas vistas y revisar impacto UI |
| Dia 2 | Terminar Contact y empezar ProjectContact | Implementar work_notes y ajustar relaciones existentes | Mapear payload esperado |
| Dia 3 | Implementar validaciones de ProjectContact | Implementar Document | Documentar ajustes de contrato |
| Dia 4 | Abrir serializers/viewsets minimos de Contact y ProjectContact | Crear migraciones estructurales | Pruebas de compatibilidad |
| Dia 5 | Probar constraints criticos y flujo backend core | Ejecutar data migration legacy Company -> Contact | Soporte a validacion de contrato |
| Dia 6 | Ajustes por hallazgos de migracion | Corregir issues de migracion y consistencia | Corregir bugs criticos |
| Dia 7 | Refinar contrato API para apertura minima | Validar integridad de relaciones en BD | Ajustar mapeo UI/API |
| Dia 8 | Endpoints minimos listos para validacion | Datos de prueba y verificacion post-migracion | Preparar integracion de consumo API |
| Dia 9 | Cierre tecnico de backend core y checklist | Verificacion final de migraciones limpias | Integrar API minima |
| Dia 10 | Aprobacion de cierre BD y handoff a Sprint 3 | Soporte de estabilizacion final | Validacion funcional de integracion |

### 🏭 **Impacto en Producción (Sprint 2)**

- **Migrations first:** todos los cambios de modelo deben ser reversibles y probados.
- **Integridad en BD:** constraints reales en PostgreSQL, no solo validacion de serializer.
- **Consistencia de datos:** migracion legacy validada antes de exponer endpoints.
- **Contrato estable:** API se abre solo cuando el esquema este congelado para evitar retrabajo.

### ✅ Criterio de cierre de BD (obligatorio)

- [x] Diagrama final aprobado
- [x] Models definitivos aprobados
- [x] Migraciones limpias
- [x] Data migration legacy validada
- [x] Constraints probados
- [x] Sin cambios pendientes en nombres, relaciones ni enums

---

---

## SPRINT 3 (25 mar-7 abr) — API + Integración Frontend

Objetivo: consolidar endpoints del core y cerrar integracion frontend sobre contrato de datos estable.

### Juan Jose Jimenez Guardo (Arquitectura + Backend core)

**Semana 1 (25-29 mar):**
- [ ] Definir contrato API final para entidades core
- [ ] Implementar logica critica faltante en backend
- [ ] Revisar consistencia entre serializers y modelo

**Semana 2 (1-7 abr):**
- [ ] Coordinar pruebas de integracion backend-frontend
- [ ] Corregir desviaciones del contrato de datos
- [ ] Cerrar checklist de integracion

---

## SPRINT 4 (8-21 abr) — Riesgos (CRÍTICO PARA NOTA)

### Arquitecto (Juan Jose Jimenez Guardo)

**Semana 1 (8-12 abr):**
- [ ] Diseñar modelo Risk (TODO DETALLADO)
  - [ ] Campos inherentes: prob (1-5), impact (1-5), score
  - [ ] Campos residuales: prob, impact, score
  - [ ] Tratamiento: Aceptar/Mitigar/Transferir/Evitar
  - [ ] Score = probabilidad × impacto
- [ ] Diseñar relación Risk ↔ Asset (N:M)
- [ ] Documentar fórmula en README (1 página mínimo)
- [ ] Validaciones de negocio

**Semana 2 (15-19 abr):**
- [ ] Revisar implementación de modelo Risk
- [ ] Revisar cálculo automático de scores
- [ ] Revisar relación N:M correcta

**Semana 3 (20-21 abr):**
- [ ] Demo

---

### Backend Implementador (Osky)

**Semana 1 (8-12 abr):**
- [ ] Crear modelo Risk según especificación del Arquitecto
- [ ] Campos: descripción, causa, consecuencia, dueño, fechas, estado
- [ ] Relación N:M Risk ↔ Asset
- [ ] Signal automático: cuando cambias "tratamiento" → recalcula "residual"

**Semana 2 (15-19 abr):**
- [ ] Crear serializer Risk (con scores calculados)
- [ ] Crear viewset Risk
- [ ] Endpoint: `/api/projects/{id}/risks/`
- [ ] Tests (validar que scores se calculan)
- [ ] PR

**Semana 3 (20-21 abr):**
- [ ] Ajustes, demo

---

### Frontend Developer (Luis)

**Semana 1 (8-12 abr):**
- [ ] Página "Riesgos" en detalle proyecto
- [ ] Tabla de riesgos con score (mostrando inherit y residual)
- [ ] Columnas: descripción, probabilidad, impacto, score, estado

**Semana 2 (15-19 abr):**
- [ ] Form crear riesgo
- [ ] Asociar activos (multiselect)
- [ ] Form editar tratamiento
- [ ] Mostrar cambio automático de score residual
- [ ] PR

**Semana 3 (20-21 abr):**
- [ ] Demo

---

### 🏭 **Impacto en Producción (Sprint 4)**

Los riesgos son cálculos críticos en SGSI:

- **Cálculos Determinísticos:** Score = Prob × Impact, NUNCA cambiar fórmula después de producción
- **Signals Thread-Safe:** Si usas signals para recalcular scores, deben ser atomic y no race conditions
- **Audit Trail:** Todos cambios de score deben estar en AuditLog (quién, cuándo, por qué)
- **Reportabilidad:** Datos de riesgos son base de reportes para auditoría, ningún harddelete
- **Performance:** Con 1000+ riesgos, queries deben ser optimizadas (indexes, caching)

**Acción:** Leer ARQUITECTURA_DESPLIEGUE_PRODUCCION.md § "Logging Estructurado"

---

---

## SPRINT 5 (22 abr - 5 may) — SoA + ISO Controls

### Arquitecto (Juan Jose Jimenez Guardo)

**Semana 1 (22-26 abr):**
- [ ] Diseñar modelo ISOControl (solo lectura, 93 controles)
- [ ] Diseñar modelo SoAItem (aplicabilidad, estado, justificación)
- [ ] Decidir: SoA generado automático vs botón "generar"
- [ ] Documentar estructura

**Semana 2 (29 abr-3 may):**
- [ ] Revisar carga de 93 controles
- [ ] Validar generación automática de SoA
- [ ] Code review

---

### Backend Implementador (Osky)

**Semana 1 (22-26 abr):**
- [ ] Crear modelo ISOControl (campos: código, nombre, descripción)
- [ ] Crear fixture con 93 controles ISO 27001 (CSV o JSON)
- [ ] `python manage.py loaddata iso_controls.json`

**Semana 2 (29 abr-3 may):**
- [ ] Crear modelo SoAItem
- [ ] Crear signal: cuando creas Project → genera SoAItem para TODOS los ISOControl
- [ ] Crear serializer y viewset SoAItem
- [ ] Endpoint: `/api/projects/{id}/soa/`
- [ ] PR

---

### Frontend Developer (Luis)

**Semana 1 (22-26 abr):**
- [ ] Página "SoA" en detalle proyecto
- [ ] Lista de 93 controles

**Semana 2 (29 abr-3 may):**
- [ ] Checkbox "aplicable"
- [ ] Campo "justificación" (textarea)
- [ ] Dropdown "estado" (No aplicable/Sin implementar/En proceso/Implementado)
- [ ] Guardar cambios
- [ ] Buscar/filtrar controles
- [ ] PR

---

### 🏭 **Impacto en Producción (Sprint 5)**

- **Datos de Referencia:** Los 93 ISOControls son datos de solo lectura, versionar en BD
- **Generación SoA:** Si es automática, testear que genera correctamente con 1000 controles
- **Truncamiento de Texto:** Justificaciones largas deben validarse (no es charla, es auditoría)
- **Indexación SoA:** Búsquedas por control_code deben ser rápidas (index en lookup)

---

---

## SPRINT 6 (6-19 may) — Evidencias + Auditoria Completa + Reportes

### Arquitecto (Juan Jose Jimenez Guardo)

**Semana 1 (6-10 may):**
- [ ] Diseñar modelo Evidence (archivo, estado, fecha)
- [ ] Diseñar estados: Pendiente/Aprobado/Rechazado
- [ ] Relación Evidence ↔ SoAItem

**Semana 2 (13-17 may):**
- [ ] Revisar subida de archivos
- [ ] Validar AuditLog completo (Risk, SoAItem, Evidence, Document)
- [ ] Code review

---

### Backend Implementador (Osky)

**Semana 1 (6-10 may):**
- [ ] Crear modelo Evidence (file, status, uploaded_at, uploaded_by)
- [ ] Implementar subida de archivo
- [ ] Validar que Evidence está vinculada a SoAItem

**Semana 2 (13-17 may):**
- [ ] Crear serializer y viewset
- [ ] Endpoint: `/api/projects/{id}/evidence/`
- [ ] Endpoint: cambiar estado de evidence
- [ ] Extender AuditLog a Evidence, Risk, SoAItem
- [ ] PR

---

### Frontend Developer (Luis)

**Semana 1 (6-10 may):**
- [ ] Página "Evidencias" en detalle proyecto
- [ ] Tabla con evidencias (archivo, estado, fecha)

**Semana 2 (13-17 may):**
- [ ] Button subir evidencia (input file)
- [ ] Mostrar estado (badge de color)
- [ ] Tabla de logs (quién cambió qué y cuándo)
- [ ] PR

---

### 🏭 **Impacto en Producción (Sprint 6)**

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

## 📌 Reportes y Dashboard

El trabajo de reportes y dashboard se ejecuta dentro de Sprint 6 como parte del cierre funcional para demo y entrega.

---

---

## 📅 BUFFER (20-23 may) — QA + Demo Final

### Equipo Completo

- [ ] Pruebas completas (flujo end-to-end)
- [ ] Correcciones de bugs
- [ ] Crear datos demo (1 proyecto completamente llenado con datos)
- [ ] Grabar video de 5-8 min (demo final)
- [ ] Documentación final
- [ ] Tag final: `v1.0-production-ready`

---

## 📊 Resumen: Tareas totales por rol

### Arquitecto + Líder Técnico (Juan Jose Jimenez Guardo)
- Sprint 1: Diseño Auth + permisos + ProjectUser + AuditLog + implementación User/permisos
- Sprint 2: Implementar Contact y ProjectContact, validaciones/constraints críticos y serializers/viewsets mínimos
- Sprint 3: Contrato API final + integración backend/frontend
- Sprint 4: Diseño Risk (CRÍTICO) + fórmula + cálculos
- Sprint 5: Diseño SoA + fixture ISO 27001
- Sprint 6: Diseño Evidence + auditoría + métricas/reportes
- **Total:** Diseño arquitectónico + implementación de core + code review todo

### Backend Implementador
- Sprint 1: Implementar JWT + ProjectUser + AuditLog signals
- Sprint 2: Implementar Document, campos planned/actual y work_notes, migraciones y data migration legacy
- Sprint 3: Consolidación de APIs core + soporte de integración
- Sprint 4: Risk + scoring automático
- Sprint 5: Fixtures + SoAItem automático
- Sprint 6: Evidence + upload + métricas/reportes
- **Total:** CRUD endpoints + signals + validaciones

### Frontend Developer
- Sprint 1: Login + layout + rutas protegidas
- Sprint 2: Frontend congelado durante etapa de cierre BD, solo bugs críticos y preparación de contrato de datos
- Sprint 3: Integración de pantallas core con APIs estabilizadas
- Sprint 4: Riesgos UI + scoring visual
- Sprint 5: SoA UI + checkboxes
- Sprint 6: Evidencias UI + upload + dashboards
- **Total:** Todas las páginas del sistema

---

## ✅ Verde/Amarillo/Rojo por sprint

### Sprint 1

**🟢 Verde:** User migrado, JWT funciona, ProjectUser creado, AuditLog registra  
**🟡 Amarillo:** JWT parcial o permisos incompletos  
**🔴 Rojo:** User no es AbstractUser, JWT no funciona, 0 PRs  

---

### Sprint 2

**🟢 Verde:** Modelo BD-first cerrado y aprobado (Contact/ProjectContact/Document + fechas planned/actual), migraciones limpias y constraints validados  
**🟡 Amarillo:** Modelos y migraciones creados, pero faltan validaciones de integridad o quedan inconsistencias de esquema  
**🔴 Rojo:** Modelo no cerrado, cambios pendientes de nombres/relaciones/enums, o migraciones inestables  

---

### Sprint 3

**🟢 Verde:** APIs core integradas con frontend, sin desviaciones de contrato y con pruebas básicas de flujo  
**🟡 Amarillo:** Integración parcial con endpoints pendientes o fallos aislados en flujos críticos  
**🔴 Rojo:** Integración bloqueada, contrato API inestable, o UI sin consumir backend real  

---

### Sprint 4-6

Similar: modelos implementados ✅, endpoints funcionales ✅, UI visible ✅

---

