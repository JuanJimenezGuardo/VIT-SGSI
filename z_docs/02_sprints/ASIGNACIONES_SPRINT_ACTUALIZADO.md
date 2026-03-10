# Asignaciones por Sprint (Sprint 1-6)

**ESTRUCTURA DEL PROYECTO:**
- **Sprint 1 (COMPLETADO)**: 3pleJ ha ejecutado TODO (100%)
- **Sprints 2-6 (EN VEREMOS)**: Pendiente confirmación si Osky (Backend) y Tinky (Frontend) participarán

Desglose de lo que 3pleJ ha completado en Sprint 1 y lo que potencialmente se ejecutará en Sprints 2-6 (sujeto a confirmación de participantes).

**IMPORTANTE:** Todos los sprints están condicionados por la arquitectura de producción definida en `ARQUITECTURA_DESPLIEGUE_PRODUCCION.md`. Cada decisión técnica debe considerar su impacto en el deployment final.

---

## SPRINT 1 (19 feb → 2 mar) — Seguridad Base + Auth [COMPLETADO]

Objetivo: Pasar de "API abierta" a "plataforma con control de acceso real" ✅ LOGRADO

### 3pleJ (Ejecutar todo: Arquitectura, Backend)

**Semana 1 (19-23 feb):**
- [x] Diseñar estructura de permisos (Admin, Consultant, Client)
- [x] Diseñar modelo ProjectUser y sus relaciones
- [x] Diseñar estructura AuditLog
- [x] Documentar especificación (SPRINT_1_GUIA_BACKEND.md)
- [x] Configurar AbstractUser en models.py
- [x] Instalar SimpleJWT y configurar JWT
- [x] Configurar `/api/token/` y `/api/token/refresh/`
- [x] 3+ commits

**Semana 2 (24-28 feb):**
- [x] Crear 6 permission classes (IsAdmin, IsConsultant, IsClient, IsAdminOrReadOnly, IsConsultantOrReadOnly, IsOwnerOrReadOnly)
- [x] Crear modelo ProjectUser con serializer + viewset
- [x] Crear endpoint `/api/project-users/` con filtrado por rol
- [x] Tests basicos: crear, leer, validations
- [x] Implementar signals para AuditLog (10 receivers automaticos)
- [x] Code review y ajustes
- [x] 3+ commits

**Semana 3 (1-2 mar):**
- [x] Validar arquitectura final
- [x] Demo Postman: Login, Tokens, ProjectUser CRUD, AuditLog automatico
- [x] Preparar demo data (backend/scripts/populate_demo_data.py: 3 usuarios, 2 empresas, 2 proyectos)
- [x] Crear test suite automatizado (backend/tests/test_demo_sprint1.py: 5 escenarios)
- [x] Git: v0.1-sprint1 tagged

**Output completado:**
- ✅ User model hereda de AbstractUser
- ✅ JWT funcionando: `/api/token/` devuelve access+refresh (15min + 1day)
- ✅ 6 clases de permiso creadas y aplicadas
- ✅ ProjectUser: CRUD funcionando con filtrado por rol
- ✅ AuditLog: registra CREATE/UPDATE/DELETE automaticamente
- ✅ 0 errores 500 en endpoints
- ✅ Demo data: 3 usuarios, 2 empresas, 2 proyectos
- ✅ Test suite: backend/tests/test_demo_sprint1.py (5 scenarios passing)
- ✅ 12+ commits con mensajes descriptivos
- ✅ v0.1-sprint1 tagged en GitHub

**Impacto en Produccion (Sprint 1):**
- JWT Cookies: Configuradas como Secure, HttpOnly, SameSite=Strict
- CORS: Habilitado para localhost:3000 (Vercel cuando pase a prod)
- Variables de Entorno: .env.example creado, credenciales nunca en codigo
- Settings por Entorno: development.py y production.py
- Database: PostgreSQL 15 local igual a produccion
- Tests en CI: GitHub Actions configurado
- SECRET_KEY: Generado y protegido
- Logging: Estructurado para produccion

---

## SPRINT 2 (3-16 mar) — Scope + Assets (SGSI Base) [EN VEREMOS]

### Asignaciones (Confirmar si Osky + Tinky participarán)

**Option A - Si participan todos:**
- 3pleJ (Arquitecto): Diseño y especificación
- Osky (Backend): Implementación de modelos Scope + Asset
- Tinky (Frontend): Páginas de Alcance e Inventario

**Option B - Si solo 3pleJ continúa:**
- 3pleJ ejecuta TODO (Arquitectura, Backend, Frontend)

**Semana 1 (3-7 mar):**
- [ ] Diseñar modelo Scope (alcance, exclusiones, justificacion, estado)
- [ ] Diseñar modelo Asset (inventario, denominación, clasificación, propietario)
- [ ] Definir validaciones (un asset siempre tiene un proyecto)
- [ ] Definir relación Scope ↔ Project (1-N)
- [ ] Implementar Scope + Asset models, serializers, viewsets
- [ ] Endpoints: `/api/scopes/`, `/api/assets/`
- [ ] 3+ commits

**Semana 2 (10-14 mar):**
- [ ] Tests: validación de relaciones, N+1 query prevention
- [ ] Frontend: página "Alcance del Proyecto"
- [ ] Frontend: página "Inventario de Activos"
- [ ] CRUD: crear, editar, listar, borrar (Scope y Asset)
- [ ] 3+ commits

**Semana 3 (16 mar):**
- [ ] Demo

---

## SPRINT 3 (17-30 mar) — Riesgos (CRITICO) [EN VEREMOS]

**Semana 1 (17-21 mar):**
- [ ] Diseñar modelo Risk (inherent prob/impact/score, residual, tratamientos)
- [ ] Diseñar relación Risk ↔ Asset (N:M)
- [ ] Documentar fórmula: Score = Probabilidad x Impacto
- [ ] Implementar modelo Risk con signals para calculo automatico
- [ ] 3+ commits

**Semana 2 (24-28 mar):**
- [ ] Crear serializer Risk (con scores calculados)
- [ ] Crear viewset Risk
- [ ] Endpoint: `/api/projects/{id}/risks/`
- [ ] Tests (validar que scores se calculan)
- [ ] Frontend: página "Riesgos" con tabla de scores (inherent vs residual)
- [ ] 3+ commits

**Semana 3 (30 mar):**
- [ ] Demo

---

## SPRINT 4 (31 mar - 13 abr) — SoA + ISO Controls [EN VEREMOS]

**Semana 1 (31 mar - 4 abr):**
- [ ] Cargar 93 controles ISO 27001 (Anexo A)
- [ ] Diseñar modelo SoAItem (control, proyecto, aplicable, justificacion, estado)
- [ ] Auto-generar 93 SoAItems al crear proyecto
- [ ] 3+ commits

**Semana 2 (7-11 abr):**
- [ ] Crear serializers + viewsets para SoA
- [ ] Endpoint: `/api/projects/{id}/soa/`
- [ ] Frontend: tabla 93 controles con estado (NOT_IMPL, IN_PROGRESS, IMPLEMENTED)
- [ ] 3+ commits

**Semana 3 (13 abr):**
- [ ] Demo

---

## SPRINT 5 (14 - 27 abr) — Evidence + Audit [EN VEREMOS]

**Semana 1 (14-18 abr):**
- [ ] Modelo Evidence (versioning, estados, comentarios)
- [ ] Upload de archivos (S3 o local)
- [ ] Serializers + viewsets
- [ ] 3+ commits

**Semana 2 (21-25 abr):**
- [ ] Frontend: formulario carga evidencias
- [ ] Evidence approval workflow
- [ ] Integración con SoAItem (cuando aprobada, marca IMPLEMENTED)
- [ ] 3+ commits

**Semana 3 (27 abr):**
- [ ] Demo

---

## SPRINT 6 (28 abr - 11 may) — Reports + Dashboard [EN VEREMOS]

**Semana 1 (28 apr - 2 may):**
- [ ] Generar SoA en PDF
- [ ] Dashboard por rol (Admin/Consultant/Client con métricas diferentes)
- [ ] 3+ commits

**Semana 2 (5-9 may):**
- [ ] Reportes: Progress, Risks, Compliance
- [ ] Frontend: visualización reportes
- [ ] 3+ commits

**Semana 3 (11 may):**
- [ ] Demo final

---

## BUFFER Y FINAL (12 - 15 may)

- [ ] QA: End-to-end testing
- [ ] Demo final ejecutivo
- [ ] Production readiness validation
- [ ] Posibles ajustes finales
