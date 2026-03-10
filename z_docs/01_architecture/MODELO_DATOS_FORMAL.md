# MODELO DE DATOS FORMAL — VIT

> **Nota de contexto (al 18-02-2026):** el backend cuenta con Users/Companies/Projects/Phases/Tasks. Los módulos SGSI (Scope, Asset, Risk, ISOControl, SoAItem, Evidence, Report, AuditLog) están definidos a nivel documental y se implementarán en las siguientes iteraciones.
## Plataforma Web para Implementación de SGSI ISO 27001
Versión: 1.0 | Fecha: febrero de 2026

---

## Tabla de Contenidos

- [Introducción](#introducción)
- [Entidades Principales](#entidades-principales)
- [Relaciones entre Entidades](#relaciones-entre-entidades)
- [Restricciones e Integridad](#restricciones-e-integridad)
- [Diagrama Entidad-Relacion](#diagrama-entidad-relacion)
- [Notas Importantes](#notas-importantes)

---

## Introducción

Este documento describe formalmente el modelo de datos de la plataforma VIT, basado en los requisitos de ISO/IEC 27001:2022 para la implementación de Sistemas de Gestión de Seguridad de la Información (SGSI).

El modelo soporta:
- Gestión completa del ciclo de vida de proyectos ISO 27001
- Evaluación de riesgos con cálculo de riesgo inherente y residual
- Mapeo de 93 controles ISO 27001 Anexo A
- Generación automatica de Statement of Applicability (SoA)
- Trazabilidad completa de cambios (auditoría)
- Versionado de documentos y evidencias

---

## Entidades Principales

### . USER (Usuarios del Sistema)

**Propósito**: Registra todos los usuarios de la plataforma VIT con sus roles y permisos.

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `username` | Varchar(150) | UNIQUE, NOT NULL | Nombre de usuario |
| `email` | Varchar(254) | UNIQUE, NOT NULL | Correo electrónico |
| `password` | Varchar(255) | NOT NULL | Contraseña (hash bcrypt) |
| `first_name` | Varchar(150) | NOT NULL | Nombre |
| `last_name` | Varchar(150) | NOT NULL | Apellido |
| `role` | Varchar(20) | ENUM, NOT NULL | Rol del usuario (ADMIN/CONSULTANT/CLIENT) |
| `phone` | Varchar(20) | NULL | Número de teléfono |
| `is_active` | Boolean | NOT NULL, Default=True | Usuario activo o inactivo |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |
| `updated_at` | DateTime | Auto Now | Fecha de ultima actualización |

**Dominios de Valores**:
- `role`: {ADMIN = Administrador VIT, CONSULTANT = Consultor ISO, CLIENT = Cliente/Empresa}

**Integridad**:
- Usuario único por username
- Usuario único por email
- Al menos un ADMIN debe existir siempre

---

### . COMPANY (Empresas Cliente)

**Propósito**: Representa las organizaciones que implementan ISO 27001.

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `name` | Varchar(255) | NOT NULL, UNIQUE | Nombre legal de la empresa |
| `tax_id` | Varchar(30) | NOT NULL, UNIQUE | NIT/RFC (identificación fiscal) |
| `email` | Varchar(254) | NOT NULL | Correo corporativo |
| `phone` | Varchar(20) | NULL | Teléfono principal |
| `address` | Text | NOT NULL | Domicilio completo |
| `city` | Varchar(00) | NOT NULL | Ciudad |
| `state` | Varchar(00) | NOT NULL | Estado/Provincia |
| `country` | Varchar(00) | NOT NULL, Default=Colombia | Pais |
| `contact_person` | Varchar(150) | NOT NULL | Nombre del contacto principal |
| `contact_position` | Varchar(100) | NOT NULL | Cargo del contacto |
| `sector` | Varchar(00) | NULL | Sector economico (Bancario, Salud, TI, etc.) |
| `employee_count` | Integer | NULL | Cantidad de empleados |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |
| `updated_at` | DateTime | Auto Now | Fecha de ultima actualización |

**Integridad**:
- Empresa unica por RFC
- Empresa unica por nombre
- Al menos un contacto debe estar definido

---

### . PROJECT (Proyectos ISO 27001)

**Propósito**: Representa cada implementación de ISO 27001 para una company.

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `company_id` | Integer | FK(Company), NOT NULL | Empresa a la que pertenece |
| `name` | Varchar(255) | NOT NULL | Nombre del proyecto |
| `description` | Text | NULL | Descripción detallada |
| `status` | Varchar(20) | ENUM, NOT NULL | Estado (PLANNING/IN_PROGRESS/COMPLETED/ON_HOLD) |
| `start_date` | Date | NOT NULL | Fecha de inicio |
| `end_date` | Date | NULL | Fecha de finalizacion planificada |
| `created_by_id` | Integer | FK(User), NOT NULL | Usuario que creo el proyecto |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |
| `updated_at` | DateTime | Auto Now | Fecha de ultima actualización |

**Dominios de Valores**:
- `status`: {PLANNING, IN_PROGRESS, COMPLETED, ON_HOLD}

**Integridad**:
- `end_date` >= `start_date` (si ambas estan presentes)
- Nombre único por company (no puede haber dos proyectos con el mismo nombre en una empresa)

---

### . PHASE (Fases del Proyecto)

**Propósito**: Divide cada proyecto en fases metodológicas ISO 27001.

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `project_id` | Integer | FK(Project), NOT NULL | Proyecto al que pertenece |
| `code` | Varchar(20) | NOT NULL | Código de fase (INIT, PLAN, IMPLEMENT, MAINTAIN, CERTIFY) |
| `name` | Varchar(100) | NOT NULL | Nombre de la fase |
| `description` | Text | NULL | Descripción |
| `sequence` | Integer | NOT NULL | Orden en el cronograma (, , , etc.) |
| `status` | Varchar(20) | ENUM, NOT NULL | Estado (NOT_STARTED/IN_PROGRESS/COMPLETED) |
| `percentage_complete` | Integer | CHECK(0-00) | Porcentaje completado |
| `start_date` | Date | NULL | Fecha de inicio real |
| `end_date` | Date | NULL | Fecha de finalizacion real |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |
| `updated_at` | DateTime | Auto Now | Fecha de ultima actualización |

**Dominios de Valores**:
- `code`: {INIT, PLAN, IMPLEMENT, MAINTAIN, CERTIFY}
- `status`: {NOT_STARTED, IN_PROGRESS, COMPLETED}

---

### . TASK (Tareas de Implementación)

**Propósito**: Acciónes especificas dentro de cada fase.

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `phase_id` | Integer | FK(Phase), NOT NULL | Fase a la que pertenece |
| `title` | Varchar(255) | NOT NULL | Título de la tarea |
| `description` | Text | NULL | Descripción detallada |
| `assigned_to_id` | Integer | FK(User), NULL | Usuario responsable |
| `priority` | Varchar(20) | ENUM, NOT NULL | Prioridad (LOW/MEDIUM/HIGH/CRITICAL) |
| `status` | Varchar(20) | ENUM, NOT NULL | Estado (NOT_STARTED/IN_PROGRESS/COMPLETED/BLOCKED) |
| `due_date` | Date | NULL | Fecha de entrega |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |
| `updated_at` | DateTime | Auto Now | Fecha de ultima actualización |

**Dominios de Valores**:
- `priority`: {LOW, MEDIUM, HIGH, CRITICAL}
- `status`: {NOT_STARTED, IN_PROGRESS, COMPLETED, BLOCKED}

---

### . RISK (Gestión de Riesgos ISO 27001)

**Propósito**: Evaluación y seguimiento de riesgos identificados en el SGSI siguiendo ISO 27001.

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `project_id` | Integer | FK(Project), NOT NULL | Proyecto al que pertenece |
| `name` | Varchar(255) | NOT NULL | Nombre del riesgo |
| `description` | Text | NULL | Descripción del riesgo |
| `category` | Varchar(20) | ENUM, NOT NULL | Categoria (STRATEGIC/OPERATIONAL/COMPLIANCE/TECHNICAL/PERSONNEL) |
| `causes` | Text | NULL | Causas raiz del riesgo |
| `consequences` | Text | NULL | Consecuencias potenciales |
| **Riesgo Inherente** (sin controles) | | | |
| `inherent_likelihood` | Integer | CHECK(-), NOT NULL | Probabilidad sin controles (=Muy baja, =Muy alta) |
| `inherent_impact` | Integer | CHECK(-), NOT NULL | Impacto sin controles (=Muy bajo, =Muy alto) |
| **Riesgo Residual** (con controles) | | | |
| `residual_likelihood` | Integer | CHECK(-), NOT NULL | Probabilidad con controles aplicados |
| `residual_impact` | Integer | CHECK(-), NOT NULL | Impacto con controles aplicados |
| **Tratamiento ISO 27001** | | | |
| `treatment` | Varchar(20) | ENUM, NOT NULL | Estrategia (ACCEPT/MITIGATE/TRANSFER/AVOID) |
| `mitigation_plan` | Text | NULL | Plan de mitigacion |
| `owner_id` | Integer | FK(User), NULL | Responsable del riesgo |
| `status` | Varchar(20) | ENUM, NOT NULL | Estado (IDENTIFIED/ASSESSED/MITIGATED/MONITORED) |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |
| `updated_at` | DateTime | Auto Now | Fecha de ultima actualización |

**Propiedades Calculadas** (no se guardan, se calculan):
- `inherent_risk_score = inherent_likelihood x inherent_impact` (rango: -)
- `residual_risk_score = residual_likelihood x residual_impact` (rango: -)
- `risk_reduction = inherent_risk_score - residual_risk_score` (KPI de efectividad)

**Dominios de Valores**:
- `category`: {STRATEGIC, OPERATIONAL, COMPLIANCE, TECHNICAL, PERSONNEL}
- `treatment`: {ACCEPT, MITIGATE, TRANSFER, AVOID}
- `status`: {IDENTIFIED, ASSESSED, MITIGATED, MONITORED}

**Integridad**:
- `residual_likelihood` <= `inherent_likelihood` (controles reducen probabilidad)
- `residual_impact` <= `inherent_impact` (controles reducen impacto)

---

### 7. ASSET (Inventario de Activos)

**Propósito**: Registra activos de información en el alcance del SGSI.

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `project_id` | Integer | FK(Project), NOT NULL | Proyecto asociado |
| `name` | Varchar(255) | NOT NULL | Nombre del activo |
| `type` | Varchar(20) | ENUM, NOT NULL | Tipo (HARDWARE/SOFTWARE/DATA/PERSONNEL/FACILITY) |
| `description` | Text | NULL | Descripción |
| `owner_id` | Integer | FK(User), NULL | Propietario del activo |
| `location` | Varchar(255) | NULL | Ubicación fisica o lógica |
| `criticality` | Varchar(20) | ENUM, NOT NULL | Criticidad (LOW/MEDIUM/HIGH/CRITICAL) |
| `confidentiality_level` | Integer | CHECK(-), NOT NULL | Nivel confidencialidad (=Publico, =Secreto) |
| `integrity_level` | Integer | CHECK(-), NOT NULL | Nivel integridad (=Sin requisito, =Maximo) |
| `availability_level` | Integer | CHECK(-), NOT NULL | Nivel disponibilidad (=No critico, =/7) |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |
| `updated_at` | DateTime | Auto Now | Fecha de ultima actualización |

**Dominios de Valores**:
- `type`: {HARDWARE, SOFTWARE, DATA, PERSONNEL, FACILITY}
- `criticality`: {LOW, MEDIUM, HIGH, CRITICAL}

---

### 8. ISOCONTROL (Controles ISO 27001)

**Propósito**: Catálogo maestro de 93 controles del Anexo A de ISO 27001:2022 (registro inmutable, solo lectura).

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `code` | Varchar(20) | UNIQUE, NOT NULL | Código ISO (A.., A.., ... A..) |
| `name` | Varchar(255) | NOT NULL | Nombre del control |
| `description` | Text | NOT NULL | Descripción oficial ISO 27001:2022|
| `category` | Varchar(00) | ENUM, NOT NULL | Dominio ISO (Organizacion, Personas, Fisicos, Técnicos, Criptografia, etc.) |
| `iso_27001_text` | Text | NOT NULL | Texto completo de ISO 27001:2022 para este control |
| `requirements` | Text | NOT NULL | Requisitos especificos |
| `implementation_guidance` | Text | NULL | Guia de implementación |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |

**Caracteristicas Especiales**:
- **Inmutable**: Estos datos vienen precargados (93 registros) y no se modifican
- **Lectura**: Solo GET, nunca POST/PUT/DELETE en este modelo
- **Origen**: Datos oficiales de ISO 27001:2022

**Categorias** (dominios del Anexo A):
- A.- Organizational Controls (controles)
- A.- People Controls (controles)
- A.7 - Physical Controls (controles)
- A.8 - Technical Controls (controles)
- A.9 - Management Controls (7 controles)

---

### 9. SOAITEM (Statement of Applicability)

**Propósito**: Registro de aplicabilidad de cada control ISO al proyecto especifico.

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `project_id` | Integer | FK(Project), NOT NULL | Proyecto al que pertenece |
| `iso_control_id` | Integer | FK(ISOControl), NOT NULL | Control ISO referenciado |
| `is_applicable` | Boolean | NOT NULL, Default=True | Se aplica este control en el proyecto? |
| `justification` | Text | NULL | Justificacion si NO es aplicable |
| `implementation_status` | Varchar(20) | ENUM, NOT NULL | Estado (NOT_IMPLEMENTED/IN_PROGRESS/IMPLEMENTED) |
| `implementation_date` | Date | NULL | Fecha de implementación |
| `responsible_id` | Integer | FK(User), NULL | Responsable de implementar |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |
| `updated_at` | DateTime | Auto Now | Fecha de ultima actualización |

**Caracteristicas Especiales**:
- **Generación automatica**: Al crear un Project, se crean automáticamente 93 SoAItems (uno por control)
- **UNIQUE constraint**: UNIQUE_together(project, iso_control) - un control aparece una sola vez por proyecto
- **Predeterminado**: `is_applicable=True` - el usuario decide cuales no aplican

**Dominios de Valores**:
- `implementation_status`: {NOT_IMPLEMENTED, IN_PROGRESS, IMPLEMENTED}

---

### 0. EVIDENCE (Evidencias de Cumplimiento)

**Propósito**: Archivos que demuestran la implementación de controles ISO.

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `project_id` | Integer | FK(Project), NOT NULL | Proyecto asociado |
| `iso_control_id` | Integer | FK(ISOControl), NULL | Control al que evidencia (puede estar sin asignar) |
| `name` | Varchar(255) | NOT NULL | Nombre descriptivo de la evidencia |
| `description` | Text | NULL | Descripción |
| `file` | FileField | NOT NULL | Archivo (PDF, DOCX, XLSX, PNG, etc.) |
| `file_size` | Integer | NOT NULL | Tamano en bytes |
| `file_type` | Varchar(100) | NOT NULL | MIME type (application/pdf, etc.) |
| `uploaded_by_id` | Integer | FK(User), NOT NULL | Usuario que subio |
| `status` | Varchar(20) | ENUM, NOT NULL, Default=PENDING | Estado (PENDING/APPROVED/REJECTED) |
| `approved_by_id` | Integer | FK(User), NULL | Admin que aprobo |
| **Versionado** | | | |
| `version` | Integer | NOT NULL, Default=1 | Número de versión |
| `previous_version_id` | Integer | FK(Evidence), NULL | Versión anterior (self-reference) |
| `is_current` | Boolean | NOT NULL, Default=True | Es la version actual? |
| `version_notes` | Text | NULL | Notas de cambio en esta version |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |
| `updated_at` | DateTime | Auto Now | Fecha de ultima actualización |

**Validaciones de Archivo**:
- Tamano maximo: 0 MB
- Tipos permitidos: PDF, DOCX, XLSX, PPTX, PNG, JPG, ZIP
- Mime type: application/pdf, application/msword, application/vnd.ms-excel, etc.

**Dominios de Valores**:
- `status`: {PENDING, APPROVED, REJECTED}

**Integridad**:
- Al crear nueva version: `is_current=False` en version anterior
- `previous_version` crea historial: v -> v -> v

---

### . DOCUMENT (Documentos Generados)

**Propósito**: Documentos generados automáticamente (plantillas, reportes, SoA PDF).

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `project_id` | Integer | FK(Project), NULL | Proyecto (NULL si es plantilla global) |
| `type` | Varchar(50) | ENUM, NOT NULL | Tipo de documento |
| `title` | Varchar(255) | NOT NULL | Título |
| `description` | Text | NULL | Descripción |
| `file` | FileField | NOT NULL | Archivo PDF/DOCX |
| `is_template` | Boolean | NOT NULL, Default=False | Es plantilla maestra? |
| `version` | Integer | NOT NULL, Default=1 | Número de versión |
| `generated_by_id` | Integer | FK(User), NULL | Usuario que genero |
| `created_at` | DateTime | Auto Now Add | Fecha de creación |

**Tipos de Documentos**:
- POLICY: Politicas de seguridad
- RISK_REGISTER: Registro de riesgos
- SOA: Statement of Applicability (PDF)
- ASSET_INVENTORY: Inventario de activos
- CONTROL_MATRIX: Matriz de controles
- Etc.

---

### . AUDITLOG (Trazabilidad de Cambios)

**Propósito**: Registro de auditoría que rastrea QUIEN, QUE, CUANDO en cambios criticos (ISO 27001 exige trazabilidad).

**Estructura**:

| Campo | Tipo | Restricción | Descripción |
|-------|------|-------------|-------------|
| `id` | Integer | PK, Auto Increment | Identificador único |
| `user_id` | Integer | FK(User), NOT NULL | Usuario que realizo la accion |
| `action` | Varchar(20) | ENUM, NOT NULL | Acción (CREATE/UPDATE/DELETE/APPROVE/REJECT) |
| `model_name` | Varchar(00) | NOT NULL | Nombre del modelo (Evidence, Risk, SoAItem, etc.) |
| `object_id` | Integer | NOT NULL | ID del objeto modificado |
| `object_description` | Varchar(255) | NULL | Descripción del objeto (para referencia) |
| `timestamp` | DateTime | Auto Now Add | Momento exacto de la accion |
| `changes` | JSON | NULL | Cambios (antes/despues) para UPDATE |
| `ip_address` | Varchar(45) | NULL | IP del usuario |
| `user_agent` | Text | NULL | Browser/Client usado |

**Ejemplo de `changes` (JSON)**:
```json
{
 "field": {"before": "Valor anterior", "after": "Valor nuevo"},
 "status": {"before": "PENDING", "after": "APPROVED"}
}
```

**Dominios de Valores**:
- `action`: {CREATE, UPDATE, DELETE, APPROVE, REJECT}

---

## Relaciones entre Entidades

### Diagrama de Relaciones (Formato Textual)

```
USER ()
 - :N -> PROJECT (created_by)
 - :N -> TASK (assigned_to)
 - :N -> AUDITLOG (user)
 - :N -> EVIDENCE (uploaded_by)
 - :N -> EVIDENCE (approved_by)

COMPANY ()
 - :N -> PROJECT

PROJECT ()
 - :N -> PHASE
 - :N -> TASK
 - :N -> RISK
 - :N -> ASSET
 - :N -> SOAITEM (93 items) <= Signal automatico
 - :N -> EVIDENCE
 - :N -> DOCUMENT

PHASE ()
 - :N -> TASK

RISK ()
 - N:M -> ASSET (tabla: risk_asset)
 - N:M -> ISOCONTROL (tabla: risk_mitigating_controls)
 - :N -> AUDITLOG

ISOCONTROL ()
 - :N -> SOAITEM (cada control tiene item por proyecto)
 - N:M -> RISK

SOAITEM (N)
 - N: -> PROJECT
 - N: -> ISOCONTROL
 - :N -> AUDITLOG

EVIDENCE ()
 - N: -> PROJECT
 - N: -> ISOCONTROL
 - N: -> USER (uploaded_by)
 - N: -> USER (approved_by)
 - :N -> EVIDENCE (self, para versionado)
 - :N -> AUDITLOG
```

### Cardinalidades Formales

| Relacion | Tipo | Cardinalidad | Restricción |
|----------|------|--------------|-------------|
| User -> Project | :N | user crea N projects | FK NOT NULL, CASCADE |
| Company -> Project | :N | company tiene N projects | FK NOT NULL, CASCADE |
| Project -> Phase | :N | project tiene N phases | FK NOT NULL, CASCADE |
| Project -> Risk | :N | project tiene N risks | FK NOT NULL, CASCADE |
| Project -> SoAItem | :N | project -> 93 SoAItems | FK NOT NULL, CASCADE, Signal |
| Project -> Asset | :N | project tiene N assets | FK NOT NULL, CASCADE |
| Risk <-> Asset | N:M | Un riesgo afecta N assets | Tabla intermedia risk_asset |
| Risk <-> ISOControl | N:M | Un riesgo se mitiga con N controles | Tabla intermedia risk_mitigating_controls |
| ISOControl -> SoAItem | :N | control -> N SoAItems (uno por proyecto) | FK NOT NULL |
| Evidence -> Evidence | Self | Versionado (v -> v -> v) | previous_version_id self-FK |

---

## Restricciones e Integridad

### Restricciones de Dominio

**Validación de Valores**:
```python
# Risk
CHECK (inherent_likelihood BETWEEN AND )
CHECK (inherent_impact BETWEEN AND )
CHECK (residual_likelihood BETWEEN AND )
CHECK (residual_impact BETWEEN AND )
CHECK (residual_likelihood <= inherent_likelihood)
CHECK (residual_impact <= inherent_impact)

# Asset
CHECK (confidentiality_level BETWEEN AND )
CHECK (integrity_level BETWEEN AND )
CHECK (availability_level BETWEEN AND )

# Phase
CHECK (percentage_complete BETWEEN 0 AND 00)
CHECK (end_date >= start_date OR end_date IS NULL)

# Project
CHECK (end_date >= start_date OR end_date IS NULL)
```

### Restricciones de Clave unica

```sql
UNIQUE (User.username)
UNIQUE (User.email)
UNIQUE (Company.rfc)
UNIQUE (Company.name)
UNIQUE (ISOControl.code)
UNIQUE (Project.name, Project.company_id) -- Nombre unico por empresa
UNIQUE (Phase.code, Phase.project_id) -- Código unico por proyecto
UNIQUE (SoAItem.project_id, SoAItem.iso_control_id) -- Un control por proyecto
UNIQUE (Evidence.project_id, Evidence.version) -- Una version actual por evidence
```

### Restricciones Referenciales

```sql
-- CASCADE: Si se elimina un Project, se eliminan sus Phases, Tasks, Risks, etc.
FK Project -> Company ON DELETE CASCADE
FK Phase -> Project ON DELETE CASCADE
FK Task -> Phase ON DELETE CASCADE
FK Risk -> Project ON DELETE CASCADE
FK Asset -> Project ON DELETE CASCADE
FK SoAItem -> Project ON DELETE CASCADE
FK Evidence -> Project ON DELETE CASCADE

-- SET_NULL: Si se elimina un User, se pone NULL en algunos campos
FK Risk.owner_id -> User ON DELETE SET_NULL
FK Task.assigned_to_id -> User ON DELETE SET_NULL
FK Evidence.approved_by_id -> User ON DELETE SET_NULL
```

---

## Diagrama Entidad-Relacion




## Notas Importantes

### Generación Automática (Signals)

Cuando se crea un nuevo `Project`:
- Sistema crea automáticamente **9SoAItem** (uno por cada ISOControl)
- Todos inician con `is_applicable=True`
- Usuario modifica segun necesidad del proyecto

### Versionado de Evidence

Cuando se carga una nueva version de Evidence:
- La version anterior recibe `is_current=False`
- Se crea nuevo registro con `version+=`
- Campo `previous_version_id` crea cadena historica

### Cálculo de Risk Score

No se guardan en BD, se calculan en aplicacion:
```
inherent_risk_score = inherent_likelihood x inherent_impact
residual_risk_score = residual_likelihood x residual_impact
risk_reduction = inherent_risk_score - residual_risk_score
```

---

**Documento preparado por el equipo de desarrollo VIT**
**Última revision**: febrero de 2026
