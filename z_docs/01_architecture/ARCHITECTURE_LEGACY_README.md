# VIT — Plataforma Web para Implementación de SGSI ISO/IEC 27001

Documentación técnica del proyecto **VIT (Virtual ISMS Tool)**, una plataforma web para **implementar y operar un SGSI** alineado con **ISO/IEC 27001:2022**.

---

## Objetivo del proyecto

Construir una plataforma completa donde:

- Los usuarios se autentiquen con **3 roles**: **Administrador (Admin)**, **Consultor** y **Cliente**
- Los consultores creen **proyectos ISO 27001** con **fases** y **tareas**
- Se evalúen **riesgos** y se gestionen **controles del Anexo A**
- Se gestione **documentación y evidencias**
- Se generen **reportes de progreso** y trazabilidad de implementación

---

## Estado actual del proyecto (al 4 marzo 2026)

**✅ SPRINT 1 COMPLETADO (v0.1-sprint1):**
- ✅ User model con AbstractUser (3 roles: ADMIN, CONSULTANT, CLIENT)
- ✅ JWT authentication (SimpleJWT implementado, tokens generados)
- ✅ Permisos por rol/proyecto (RBAC + ProjectUser con 6 permission classes)
- ✅ AuditLog con Django signals (registro automático de QUIEN/QUE/CUANDO)
- ✅ Companies, Projects, Phases, Tasks (CRUD completo)
- ✅ Demo data population (backend/scripts/populate_demo_data.py)
- ✅ Test suite automatizado (backend/tests/test_demo_sprint1.py: 5 escenarios validados)
- ✅ Git: Commit tagged v0.1-sprint1, historial limpio

**Próximos pasos inmediatos (Sprint 2-6):**
1. **Sprint 2:** Implementar **Scope + Asset** (alcance del SGSI e inventarios)
2. **Sprint 3:** Implementar **Risk** (riesgos inherente/residual con cálculo automático)
3. **Sprint 4:** Cargar **ISOControl** (93 controles) y generar **SoA** automático
4. **Sprint 5:** Implementar **Evidence** (carga/versioning/aprobación)
5. **Sprint 6:** Reports + Dashboards
6. **Frontend:** React + Vite (Login, PrivateRoute, dashboards por rol)



## Alcance funcional (alto nivel)

- **Autenticación y autorización por roles** (RBAC)
- **Gestión de compañías y proyectos** (cliente / consultor responsable)
- **Fases y tareas** por proyecto, con estados, prioridad y trazabilidad
- **Gestión de riesgos** (riesgo inherente y residual) + **activos**
- **Catálogo de controles ISO** (93 controles del Anexo A 27001:2022) y **SoA**
- **Evidencias** (archivos) y **documentos generados** (p. ej., reportes/SoA en PDF)
- **Auditoría y trazabilidad** (bitácora de eventos, historial de cambios, integridad)

---

## Stack propuesto

- **Backend**: Django + Django REST Framework
- **BD**: PostgreSQL
- **Frontend**: React + Vite (planeado)
- **Almacenamiento de archivos**: local/S3 (según despliegue)

---

## Documentos incluidos

- `RESUMEN_EJECUTIVO.md` — visión ejecutiva y backlog inicial
- `MODELO_DATOS_FORMAL.md` — modelo entidad–relación y tablas (formal)
- `DICCIONARIO_DATOS.md` — definiciones de campos, reglas y validaciones
- `CARDINALIDADES_RELACIONES.md` — relaciones y cardinalidades entre entidades
- `ARQUITECTURA_RIESGOS.md` — arquitectura de gestión de riesgos (ISO 27001)
- `ESTRATEGIA_AUDITORIA.md` — estrategia de trazabilidad/auditoría (alineación Anexo A)

---

## Nota de implementación

En los documentos se usa una **convención mixta**:
- Los **nombres de modelos/campos** se presentan en estilo técnico (compatibles con Django/BD).
- Las **descripciones y reglas** están en español para facilitar revisión académica y de negocio.
