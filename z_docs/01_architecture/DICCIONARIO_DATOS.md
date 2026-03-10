# DICCIONARIO DE DATOS — VIT

> **Nota de contexto (al 18-02-2026):** el backend cuenta con Users/Companies/Projects/Phases/Tasks. Los módulos SGSI (Scope, Asset, Risk, ISOControl, SoAItem, Evidence, Report, AuditLog) están definidos a nivel documental y se implementarán en las siguientes iteraciones.
## Definiciones, Dominios y Reglas de Negocio
Versión: 1.0 | Fecha: febrero de 2026

---

## Tabla de Contenidos

- [USER (Usuarios)](#user-usuarios)
- [COMPANY (Empresas)](#company-empresas)
- [PROJECT (Proyectos)](#project-proyectos)
- [PHASE (Fases)](#phase-fases)
- [TASK (Tareas)](#task-tareas)
- [RISK (Riesgos)](#risk-riesgos)
- [ASSET (Activos)](#asset-activos)
- [ISOCONTROL (Controles)](#isocontrol-controles)
- [SOAITEM (Aplicabilidad)](#soaitem-aplicabilidad)
- [EVIDENCE (Evidencias)](#evidence-evidencias)
- [DOCUMENT (Documentos)](#document-documentos)
- [AUDITLOG (Auditoría)](#auditlog-auditoría)
- [Resumen de Validaciones](#resumen-de-validaciones)

---

## USER (Usuarios)

### Propósito
Registra todos los usuarios de la plataforma VIT con autenticación, rol y permisos.

### Campos

#### `id` [PK, Integer]
- **Descripción**: Identificador único del usuario
- **Tipo de Dato**: Integer, Auto-increment
- **Constraint**: PRIMARY KEY, NOT NULL
- **Rango**: - ,7,8,7
- **Validación**: No editable, generado automáticamente
- **Ejemplo**:

#### `username` [UNIQUE, Varchar(150)]
- **Descripción**: Nombre único para login (sin espacios, alfanumerico)
- **Tipo de Dato**: Varchar(255)
- **Constraint**: UNIQUE, NOT NULL
- **Validación**:
 - Min: caracteres, Max: 0
 - Permitido: letras, numeros, @, ., +, -, _
 - No permitido: espacios, caracteres especiales (a, e, i, o, u)
 - Insensitive a mayusculas en base de datos
- **Regla de Negocio**: Usuario no puede cambiar su username despues de creado
- **Ejemplo**: `juan.perez`, `jperez@vit`, `juan_perez_0`

#### `email` [UNIQUE, Varchar(254)]
- **Descripción**: Correo electrónico del usuario para comunicaciones
- **Tipo de Dato**: Varchar(255)
- **Constraint**: UNIQUE, NOT NULL
- **Validación**:
 - Formato NIT/RFC (validación email estandar)
 - Max: caracteres
 - Único en base de datos
- **Regla de Negocio**:
 - Email se usa para reset de contraseña
 - Cambio de email requiere verificacion (confirm link)
 - No puede haber dos usuarios con mismo email (incluso si inactivos)
- **Ejemplo**: `juan.perez@consultec.com.co`

#### `password` [Varchar(255)]
- **Descripción**: Contraseña hash (nunca se almacena en texto plano)
- **Tipo de Dato**: Varchar(255) - conteniendo hash bcrypt
- **Constraint**: NOT NULL
- **Validación**:
 - Algoritmo: bcrypt (Django default)
 - Min longitud (antes de hash): 8 caracteres
 - Requiere: mayusculas, minusculas, numeros, simbolo (politica fuerte)
 - Expiracion: segun politica organizacional (90 dias recomendado)
- **Regla de Negocio**:
 - Nunca se retorna en API (ni siqueiera para admin)
 - Reset via email con token temporal (h expiracion)
 - Historial de contrasenas previas (no reutilizar ultimas )
- **Metodo**: Set mediante `user.set_password()`, no asignacion directa
- **Ejemplo**: `$b$$R9h7cIPz0gi.URNNL...` (hash bcrypt)

#### `first_name` [Varchar(150)]
- **Descripción**: Nombre de pila del usuario
- **Tipo de Dato**: Varchar(255)
- **Constraint**: NOT NULL
- **Validación**:
 - Min: caracteres
 - Max: 0 caracteres
 - Permitido: letras, espacios, acentos (a, e, i, o, u)
 - No permitido: numeros, simbolos especiales
- **Regla de Negocio**:
 - Usualmente se combina con last_name para «Nombre Completo»
 - Visible en reports y auditoría
- **Ejemplo**: `Juan`, `Maria Jose`, `Luis Arturo`

#### `last_name` [Varchar(150)]
- **Descripción**: Apellido del usuario
- **Tipo de Dato**: Varchar(255)
- **Constraint**: NOT NULL
- **Validación**:
 - Min: caracteres
 - Max: 0 caracteres
 - Permitido: letras, espacios, acentos
- **Ejemplo**: `Perez Gonzalez`, `Garcia Lopez`

#### `role` [ENUM: ADMIN/CONSULTANT/CLIENT]
- **Descripción**: Rol del usuario que determina permisos y acceso
- **Tipo de Dato**: Varchar(255)
- **Constraint**: NOT NULL
- **Dominios de Valores**:
```
 ADMIN ("Administrador VIT")
 - Acceso: Todas las empresas, todos los proyectos
 - Permisos: CRUD completo, gestion de usuarios, reportes globales
 - Caso de Uso: Personal de VIT (implantadores ISO)
 
 CONSULTANT ("Consultor ISO")
 - Acceso: Proyectos asignados como consultor
 - Permisos: Crear proyectos, evaluar riesgos, seleccionar controles, auditar
 - Caso de Uso: Consultores externos o internos de ISO 27001
 
 CLIENT ("Cliente/Empresa")
 - Acceso: Solo sus propios proyectos dentro su empresa
 - Permisos: Ver dashboard, cargar evidencia, ver SoA, contactar consultor
 - Caso de Uso: Personal de la empresa implementando ISO
 ```
- **Regla de Negocio**:
 - ADMIN >= CONSULTANT >= CLIENT en jerarquía de permisos
 - Un usuario es ADMIN O CONSULTANT O CLIENT (no multiples valores)
 - Cambio de rol requiere auditoría de seguridad
- **Validación**: Solo valores del dominio
- **Ejemplo**: `CONSULTANT`

#### `phone` [Varchar(20), Nullable]
- **Descripción**: Número de telefono del usuario
- **Tipo de Dato**: Varchar(255)
- **Constraint**: NULL allowed
- **Validación**:
 - Formato: +[country_code]-[number] o (XXX)-XXX-XXXX
 - Solo digitos, guiones, parentesis, +
 - Recomendado: +---7
- **Regla de Negocio**: Opcional, usado para contacto directo
- **Ejemplo**: `+7---`, `(0) -0`

#### `is_active` [Boolean, Default=True]
- **Descripción**: Indica si el usuario esta activo (puede hacer login)
- **Tipo de Dato**: Boolean
- **Constraint**: NOT NULL, Default=True
- **Dominios de Valores**: `True` (usuario activo), `False` (usuario desactivado)
- **Regla de Negocio**:
 - Soft-delete: no se elimina usuario, se desactiva
 - Usuario inactivo NO puede hacer login ni API calls
 - Datos historicos (proyectos, evidencias) se mantienen
 - Reactivacion es posible
- **Validación**: None (boolean)
- **Ejemplo**: `true`

#### `created_at` [DateTime, Auto Now Add]
- **Descripción**: Marca de tiempo de creacion del usuario
- **Tipo de Dato**: DateTime with timezone
- **Constraint**: Auto Now Add (se genera automáticamente), NOT NULL, Immutable
- **Precision**: Milisegundos (YYYY-MM-DD HH:MM:SS.mmm)
- **Validación**: No se puede editar manualmente
- **Regla de Negocio**: Usado para auditoría de creacion
- **Ejemplo**: `0-0-0:0:.`

#### `updated_at` [DateTime, Auto Now]
- **Descripción**: Marca de tiempo de ultima actualización
- **Tipo de Dato**: DateTime with timezone
- **Constraint**: Auto Now (actualiza automáticamente en cada save), NOT NULL
- **Precision**: Milisegundos
- **Validación**: No se puede editar manualmente
- **Regla de Negocio**:
 - Actualiza cuando se cambia CUALqueIER campo del usuario
 - Diferencia con created_at identifica modificaciones
- **Ejemplo**: `0-0-::0.`

### Validaciones Complejas

```python
# Validacion de usuario unico
UNIQUE INDEX idx_username ON user(username)
UNIQUE INDEX idx_email ON user(email)

# Validacion de consistencia
CHECK (username != '')
CHECK (email LIKE '%@%.%') -- Email debe tener @ y .
CHECK (char_length(password) >= 0) -- Hash bcrypt >= 0 chars

# Validacion de negocio
if role == "CLIENT":
 assert company_id is not None, "Cliente DEBE estar vinculado a empresa"
```

---

## COMPANY (Empresas)

### Propósito
Representa las organizaciones cliente que implementan ISO 27001.

### Campos

#### `id` [PK, Integer]
- **Descripción**: Identificador único de la empresa
- **Tipo de Dato**: Integer, Auto-increment
- **Constraint**: PRIMARY KEY, NOT NULL
- **Validación**: No editable
- **Ejemplo**: 7

#### `name` [UNIQUE, Varchar(255)]
- **Descripción**: Nombre legal de la empresa (razon social)
- **Tipo de Dato**: Varchar(255)
- **Constraint**: UNIQUE, NOT NULL
- **Validación**:
 - Min: caracteres, Max:
 - Debe coincidir con registro mercantil
 - No permitir duplicados (mismo nombre en BD)
- **Regla de Negocio**:
 - Campo legal, debe ser exacto
 - Usado en reportes y documentos
 - No se puede cambiar facilmente (requiere auditoría)
- **Ejemplo**: `Consultec S.A.S.`, `Banco Regional Colombiano`

#### `tax_id` [UNIQUE, Varchar(30)]
- **Descripción**: Identificador fiscal (Registro de Contribuyente o equivalente)
- **Tipo de Dato**: Varchar(255)
- **Constraint**: UNIQUE, NOT NULL
- **Validación**:
 - Para Colombia: NIT (Número de Identificación Tributaria)
 - Formato: XXXXXXXXXX-Y (0 digitos + verificador)
 - Debe validarse contra DIAN
 - Min: 0 caracteres, Max:
- **Regla de Negocio**:
 - Identificador legal único por empresa
 - No cambiar (inmutable)
 - Usado para identificar empresa en reportes fiscales
- **Ejemplo**: `900-`, `8007`, `9000`

#### `email` [UNIQUE, Varchar(254)]
- **Descripción**: Correo corporativo de la empresa para comunicaciones oficiales
- **Tipo de Dato**: Varchar(255)
- **Constraint**: UNIQUE, NOT NULL
- **Validación**:
 - Formato NIT/RFC
 - Debe ser correo corporativo (NO gmail/yahoo)
 - Validación de dominio (MX record)
- **Regla de Negocio**:
 - Usado para notificaciones de certificacion
 - Debe estar monitoreado por equipo legal/admin
- **Ejemplo**: `legal@consultec.com.co`, `info@bancoregional.com`

#### `phone` [Varchar(20)]
- **Descripción**: Teléfono principal de la empresa
- **Tipo de Dato**: Varchar(255)
- **Constraint**: NOT NULL
- **Validación**: Formato +XX-XXXX-XXXX-XXXX
- **Regla de Negocio**: Contacto administrativo principal
- **Ejemplo**: `+7---`

#### `address` [Text]
- **Descripción**: Domicilio completo de la empresa (calle, numero, complementos)
- **Tipo de Dato**: Text (sin limite de largo)
- **Constraint**: NOT NULL
- **Validación**:
 - Min: 0 caracteres
 - Debe incluir: calle, numero, ciudad, codigo postal
- **Regla de Negocio**:
 - Documentación legal completa
 - Usado en Certificados de ISO 27001
- **Ejemplo**: `Calle N.º -7, Oficina 8B, Bogota D.C., 0`

#### `city` [Varchar(00)]
- **Descripción**: Municipio o ciudad donde se ubica la empresa
- **Tipo de Dato**: Varchar(00)
- **Constraint**: NOT NULL
- **Validación**:
 - Debe ser ciudad valida del pais
 - Predefinido por lista de municipios si es posible
- **Regla de Negocio**: Componente de domicilio legal
- **Ejemplo**: `Bogota`, `Medellin`, `Cali`

#### `state` [Varchar(00)]
- **Descripción**: Departamento o estado donde se ubica la empresa
- **Tipo de Dato**: Varchar(00)
- **Constraint**: NOT NULL
- **Validación**: Debe ser estado/dept valido del pais
- **Regla de Negocio**: Componente de domicilio legal
- **Ejemplo**: `Cundinamarca`, `Antioquia`, `Valle del Cauca`

#### `country` [Varchar(00), Default=«Colombia»]
- **Descripción**: Pais de constitucion de la empresa
- **Tipo de Dato**: Varchar(00)
- **Constraint**: NOT NULL, Default=«Colombia»
- **Validación**:
 - Lista de paises ISO -
 - Predefinido: Colombia (pero expandible)
- **Regla de Negocio**:
 - VIT inicialmente focalizado en Colombia
 - Poder expandir internacionalmente
- **Ejemplo**: `Colombia`, `Ecuador`, `Peru`

#### `contact_person` [Varchar(150)]
- **Descripción**: Nombre completo del contacto principal en la empresa
- **Tipo de Dato**: Varchar(255)
- **Constraint**: NOT NULL
- **Validación**:
 - Min: caracteres
 - Formato: «Nombre(s) Apellido(s)»
- **Regla de Negocio**:
 - Responsable legal de SGSI
 - Receptor de comunicaciones oficiales
 - Firma documentos de certificacion
- **Ejemplo**: `Carlos Andres Martinez Garcia`

#### `contact_position` [Varchar(100)]
- **Descripción**: Cargo del contacto principal
- **Tipo de Dato**: Varchar(255)
- **Constraint**: NOT NULL
- **Validación**:
 - Cargos estandar: CISO, Director, Gerente, Coordinador, etc.
 - Min: caracteres
- **Regla de Negocio**:
 - Identifica autoridad del contacto
 - Cargos previos pueden ser CISO, Director Ejecutivo, Gerente TI
- **Ejemplo**: `Chief Information Security Officer`, `Director de Tecnologia`

#### `sector` [Varchar(00), Nullable]
- **Descripción**: Segmento economico de la empresa para contextualizar SGSI
- **Tipo de Dato**: Varchar(00)
- **Constraint**: NULL allowed
- **Dominios de Valores**:
```
 FINANCIAL - Bancario, aseguradoras, fondos de pension
 HEALTH - Hospitales, clinicas, farmacias
 TECHNOLOGY - Empresas de software, hosting, telecom
 RETAIL - Tiendas, cadenas comerciales, e-commerce
 MANUFACTURING - Industria, manufactura
 GOVERNMENT - Entidades publicas
 ENERGY - Petroleo, gas, energia
 EDUCATION - Universidades, colegios
 LEGAL - Despachos, notarias
 OTHER - Otros sectores
 ```
- **Regla de Negocio**:
 - Usado para tipificacion de riesgos
 - Diferentes sectores tienen diferentes amenazas
 - Reglas especiales por sector (HIPAA para salud, PCI para retail)
- **Ejemplo**: `FINANCIAL`, `TECHNOLOGY`

#### `employee_count` [Integer, Nullable]
- **Descripción**: Cantidad aproximada de empleados de la empresa
- **Tipo de Dato**: Integer
- **Constraint**: NULL allowed, CHECK(employee_count > 0)
- **Validación**:
 - Rango: - ,000,000
 - Información indicativa (no auditada)
- **Regla de Negocio**:
 - Impacta alcance de conciencia (A..)
 - Impacta complejidad de roles
 - Usado en segmentacion de auditar
- **Ejemplo**: 0, 000, 0

#### `created_at` [DateTime, Auto Now Add]
- **Descripción**: Fecha de registro de la empresa en VIT
- **Tipo de Dato**: DateTime with timezone
- **Constraint**: Auto Now Add, NOT NULL
- **Validación**: Inmutable
- **Regla de Negocio**: Auditoría de onboarding
- **Ejemplo**: `0-0-0 09:00:00`

#### `updated_at` [DateTime, Auto Now]
- **Descripción**: Última actualización de datos de la empresa
- **Tipo de Dato**: DateTime with timezone
- **Constraint**: Auto Now, NOT NULL
- **Validación**: Auto-actualizada en cada cambio
- **Ejemplo**: `0-0-::0`

---

## PROJECT (Proyectos)

### Propósito
Representa cada implementación de ISO 27001 para una empresa cliente.

### Campos

#### `id` [PK, Integer]
- **Descripción**: Identificador único del proyecto
- **Tipo de Dato**: Integer, Auto-increment
- **Validación**: No editable
- **Ejemplo**:

#### `company_id` [FK -> Company, NOT NULL]
- **Descripción**: Referencia a la empresa que implementa ISO
- **Tipo de Dato**: Integer (Foreign Key)
- **Constraint**: FK(Company.id), NOT NULL, ON DELETE CASCADE
- **Validación**:
 - Debe existir en tabla Company
 - No puede ser NULL
- **Regla de Negocio**:
 - Cada proyecto pertenece a exactamente UNA empresa
 - Si se elimina company, se eliminan todos sus proyectos (CASCADE)
- **Relacion**: Company () -> Project (N)
- **Ejemplo**: 7 (referencia a Consultec S.A.S.)

#### `name` [Varchar(255)]
- **Descripción**: Nombre descriptivo del proyecto ISO
- **Tipo de Dato**: Varchar(255)
- **Constraint**: NOT NULL
- **Validación**:
 - Min: caracteres, Max:
 - Único por company (no puede haber dos proyectos con mismo nombre en una empresa)
 - UNIQUE (company_id, name) - constraint combinada
- **Regla de Negocio**:
 - Identificable por stakeholders
 - Ejemplos: «ISO 27001:2022Corporate», «SGSI Infraestructura TI»
- **Ejemplo**: `ISO 27001 - Plataforma Web`, `SGSI Bancos`

#### `description` [Text, Nullable]
- **Descripción**: Descripción detallada del alcance y objetivos del proyecto
- **Tipo de Dato**: Text
- **Constraint**: NULL allowed
- **Validación**: Max: 0,000 caracteres
- **Regla de Negocio**:
 - Documentación de justificacion ISO
 - Usado en reportes y comunicaciones internas
- **Ejemplo**: `Implementación de SGSI para infraestructura de datos y sistemas web...`

#### `status` [ENUM: PLANNING/IN_PROGRESS/COMPLETED/ON_HOLD]
- **Descripción**: Estado actual del proyecto ISO
- **Tipo de Dato**: Varchar(255)
- **Constraint**: NOT NULL, ENUM
- **Dominios de Valores**:
```
 PLANNING (Planificacion)
 - Fase: Assessment y Planning
 - Actividades: Evaluacion de riesgos, seleccion de controles
 - Transicion: -> IN_PROGRESS (alcance aprobado)
 - Ejemplos: Riesgos identificados pero no mitigados
 
 IN_PROGRESS (En Ejecucion)
 - Fase: Implementation
 - Actividades: Implementacion de controles, evidencia
 - Transicion: -> COMPLETED (todos controles implementados)
 - Ejemplos: Cargando evidencias, implementando politicas
 
 COMPLETED (Completado)
 - Fase: Certification
 - Actividades: Auditoria externa, certificacion
 - Transicion: -> ON_HOLD (si requiere mantenimiento)
 - Ejemplos: Certificado ISO 27001otorgado
 
 ON_HOLD (Pausado)
 - Razon: Falta de recursos, cambios en negocio, etc.
 - Transicion: -> IN_PROGRESS (reactivacion)
 - Ejemplos: Proyecto pausado temporalmente
 ```
- **Validación**: Solo valores del dominio
- **Regla de Negocio**:
 - Transiciones controladas: PLANNING -> IN_PROGRESS -> COMPLETED
 - ON_HOLD posible desde cualqueier estado
 - Cambio de status genera AuditLog
- **Ejemplo**: `IN_PROGRESS`

#### `start_date` [Date]
- **Descripción**: Fecha planificada de inicio del proyecto
- **Tipo de Dato**: Date (YYYY-MM-DD)
- **Constraint**: NOT NULL
- **Validación**:
 - Debe ser fecha valida
 - Preferentemente no en el pasado (validar en creacion)
- **Regla de Negocio**:
 - Hito de inicio de implementación
 - Contratos con consultores usan esta fecha
- **Ejemplo**: `0-0-0`

#### `end_date` [Date, Nullable]
- **Descripción**: Fecha planificada de finalizacion del proyecto
- **Tipo de Dato**: Date
- **Constraint**: NULL allowed (se define durante ejecucion)
- **Validación**:
 - Si esta definida: end_date >= start_date
 - CHECK (end_date IS NULL OR end_date >= start_date)
- **Regla de Negocio**:
 - Se define en planificacion (fase PLANNING)
 - Puede ajustarse si hay retrasos
 - Tipicamente -meses desde start_date
- **Ejemplo**: `0-08-`, NULL

#### `created_by_id` [FK -> User, NOT NULL]
- **Descripción**: Usuario que creo el proyecto
- **Tipo de Dato**: Integer (Foreign Key)
- **Constraint**: FK(User.id), NOT NULL, ON DELETE SET_NULL
- **Validación**: Debe ser usuario valido
- **Regla de Negocio**:
 - Auditoría de quien inicio proyecto
 - Tipicamente CONSULTANT o ADMIN
 - Si usuario se elimina: created_by queda NULL (SET_NULL)
- **Relacion**: User () -> Project (N)
- **Ejemplo**: (referencia a consultor Carlos)

#### `created_at` [DateTime, Auto Now Add]
- **Descripción**: Fecha de creacion del registro del proyecto
- **Tipo de Dato**: DateTime with timezone
- **Constraint**: Auto Now Add, NOT NULL
- **Validación**: Immutable
- **Ejemplo**: `0-0-0:00:00`

#### `updated_at` [DateTime, Auto Now]
- **Descripción**: Última actualización de datos del proyecto
- **Tipo de Dato**: DateTime with timezone
- **Constraint**: Auto Now, NOT NULL
- **Ejemplo**: `0-0-:0:00`

### Validaciones Complejas

```python
# Validacion de integridad temporal
CHECK (end_date IS NULL OR end_date >= start_date)

# Nombre unico por empresa
UNIQUE (company_id, name)

# Transiciones de estado controladas (en app logic)
def save(self):
 valid_transitions = {
 'PLANNING': ['IN_PROGRESS', 'ON_HOLD'],
 'IN_PROGRESS': ['COMPLETED', 'ON_HOLD'],
 'COMPLETED': ['ON_HOLD'],
 'ON_HOLD': ['PLANNING', 'IN_PROGRESS']
 }
```

---

## PHASE (Fases)

### Propósito
Divide cada proyecto en fases metodológicas de implementación ISO.

### Campos Clave

#### `id` [PK, Integer]
- **Validación**: No editable, auto-increment
- **Ejemplo**:

#### `project_id` [FK -> Project, NOT NULL]
- **Descripción**: Proyecto al que pertenece la fase
- **Constraint**: FK(Project.id), NOT NULL, ON DELETE CASCADE
- **Ejemplo**:

#### `code` [Varchar(20), ENUM]
- **Descripción**: Codigo único de la fase
- **Dominios de Valores**: {INIT, PLAN, IMPLEMENT, MAINTAIN, CERTIFY}
- **Regla de Negocio**:
 - INIT: Iniciacion (kick-off)
 - PLAN: Planificacion (diagnostico + risk assessment)
 - IMPLEMENT: Implementación (ejecutar controles)
 - MAINTAIN: Mantenimiento (post-certificacion)
 - CERTIFY: Certificacion (auditoría externa, auditores)
- **Ejemplo**: `IMPLEMENT`

#### `name` [Varchar(255)]
- **Descripción**: Nombre legible de la fase
- **Validación**: NOT NULL
- **Ejemplo**: `Implementación de Controles`

#### `sequence` [Integer, NOT NULL]
- **Descripción**: Orden de la fase en el proyecto (, , , ...)
- **Validación**:
 - Debe ser único por proyecto: UNIQUE (project_id, sequence)
 - Rango: -00
- **Regla de Negocio**: Define orden cronologico de fases
- **Ejemplo**: (es la tercera fase)

#### `status` [ENUM: NOT_STARTED/IN_PROGRESS/COMPLETED]
- **Descripción**: Estado actual de la fase
- **Dominios de Valores**: {NOT_STARTED, IN_PROGRESS, COMPLETED}
- **Regla de Negocio**:
 - NOT_STARTED: Fase no ha iniciado
 - IN_PROGRESS: Fase en ejecucion
 - COMPLETED: Fase finalizada
- **Ejemplo**: `IN_PROGRESS`

#### `percentage_complete` [Integer, CHECK(0-00)]
- **Descripción**: Porcentaje de completitud de la fase
- **Tipo de Dato**: Integer
- **Constraint**: CHECK (percentage_complete >= 0 AND percentage_complete <= 00)
- **Validación**: 0-00 solamente
- **Regla de Negocio**:
 - Se calcula basado en tasks completadas
 - 0% = no iniciada
 - 00% = fase completada
- **Ejemplo**:

#### `start_date`, `end_date` [Date, Nullable]
- **Descripción**: Fechas reales de ejecucion
- **Validación**:
 - NULL si no ha iniciado
 - end_date >= start_date si ambas definidas
- **Ejemplo**: `0-0-0`, `0-0-`

#### `created_at`, `updated_at` [DateTime]
- **Validación**: Auto-managed
- **Ejemplo**: `0-0-0:00:00`

---

## TASK (Tareas)

### Propósito
Acciónes especificas dentro de cada fase de proyecto.

### Campos Clave

#### `id` [PK, Integer]
- **Validación**: Auto-increment, no editable
- **Ejemplo**:

#### `phase_id` [FK -> Phase, NOT NULL]
- **Descripción**: Fase a la que pertenece la tarea
- **Constraint**: FK(Phase.id), NOT NULL, ON DELETE CASCADE
- **Ejemplo**:

#### `title` [Varchar(255)]
- **Descripción**: Nombre descriptivo de la tarea
- **Constraint**: NOT NULL
- **Validación**:
 - Min: caracteres
 - Max:
- **Ejemplo**: `Implementar MFA en sistema de login`

#### `description` [Text, Nullable]
- **Descripción**: Detalles, requisitos, aceptacion criteria
- **Validación**: Max 0,000 caracteres
- **Ejemplo**: `Implementar autenticación multifactor usando TOTP...`

#### `assigned_to_id` [FK -> User, Nullable]
- **Descripción**: Usuario responsable de ejecutar la tarea
- **Constraint**: FK(User.id), NULL allowed
- **Validación**: Debe ser usuario de tipo CONSULTANT o CLIENT
- **Regla de Negocio**:
 - NULL = tarea no asignada aun
 - No NULL = alguien es responsable
 - Notificacion cuando se asigna
- **Ejemplo**: 8 (consultor Carlos)

#### `priority` [ENUM: LOW/MEDIUM/HIGH/CRITICAL]
- **Descripción**: Prioridad de ejecucion
- **Dominios de Valores**:
```
 LOW - Puede esperar, dependencias minimas (Ej: documentacion secundaria)
 MEDIUM - Normal, plazo flexible (Ej: controles no criticos)
 HIGH - Urgente, impacta otros (Ej: controles mitigadores de riesgos altos)
 CRITICAL - Bloqueante, requiere atencion inmediata (Ej: vulnerabilidades de seguridad)
 ```
- **Validación**: Solo valores del dominio
- **Regla de Negocio**: Ordena backlog de trabajo
- **Ejemplo**: `HIGH`

#### `status` [ENUM: NOT_STARTED/IN_PROGRESS/COMPLETED/BLOCKED]
- **Descripción**: Estado de ejecucion de la tarea
- **Dominios de Valores**:
```
 NOT_STARTED - Tarea planificada, no iniciada
 IN_PROGRESS - Tarea en ejecucion
 COMPLETED - Tarea finalizada y validada
 BLOCKED - Tarea bloqueada por dependencia o recurso
 ```
- **Validación**: Solo valores del dominio
- **Regla de Negocio**: Transiciones: NOT_STARTED -> IN_PROGRESS -> COMPLETED
- **Ejemplo**: `IN_PROGRESS`

#### `due_date` [Date, Nullable]
- **Descripción**: Fecha de entrega esperada
- **Constraint**: NULL allowed
- **Validación**: Si definida, due_date >= today()
- **Regla de Negocio**:
 - Usado para planificacion
 - Alertas si fecha vence
- **Ejemplo**: `0-0-`

#### `created_at`, `updated_at` [DateTime]
- **Validación**: Auto-managed
- **Ejemplo**: `0-0-0:00:00`

---

## RISK (Riesgos)

### Propósito
Evaluación y gestión de riesgos ISO 27001.

### Campos Clave

#### `id` [PK, Integer]
- **Validación**: Auto-increment
- **Ejemplo**:

#### `project_id` [FK -> Project, NOT NULL]
- **Constraint**: FK(Project.id), NOT NULL, ON DELETE CASCADE
- **Ejemplo**:

#### `name` [Varchar(255)]
- **Descripción**: Nombre descriptivo del riesgo
- **Constraint**: NOT NULL
- **Validación**:
 - Min: caracteres
 - Único por proyecto: UNIQUE (project_id, name)
- **Ejemplo**: `Exposicion de datos de clientes`

#### `description` [Text, Nullable]
- **Descripción**: Descripción detallada del riesgo
- **Validación**: Max 0,000 caracteres
- **Ejemplo**: `Acceso no autorizado a base de datos de clientes...`

#### `category` [ENUM, NOT NULL]
- **Descripción**: Tipo de riesgo
- **Dominios de Valores**: {STRATEGIC, OPERATIONAL, COMPLIANCE, TECHNICAL, PERSONNEL}
- **Regla de Negocio**:
 - STRATEGIC: Riesgos de negocio a nivel ejecutivo
 - OPERATIONAL: Riesgos de procesos y operaciones
 - COMPLIANCE: Riesgos regulatorios y legales (GDPR, PCI, etc.)
 - TECHNICAL: Riesgos ciberseguridad y TI
 - PERSONNEL: Riesgos de personal (error humano, interno threat)
- **Ejemplo**: `TECHNICAL`

#### `causes` [Text, Nullable]
- **Descripción**: Causas raiz del riesgo
- **Validación**: Max ,000 caracteres
- **Regla de Negocio**: Análisis de raiz para mitigacion efectiva
- **Ejemplo**: `Falta de encryption, ausencia de access controls...`

#### `consequences` [Text, Nullable]
- **Descripción**: Impacto potencial si ocurre el riesgo
- **Validación**: Max ,000 caracteres
- **Ejemplo**: `Violacion de privacidad de clientes, multa GDPR, perdida reputacion...`

#### `inherent_likelihood` [Integer, CHECK(-), NOT NULL]
- **Descripción**: Probabilidad del riesgo SIN controles (=Muy baja, =Muy alta)
- **Tipo de Dato**: Integer
- **Constraint**: CHECK (inherent_likelihood BETWEEN AND ), NOT NULL
- **Validación**: Solo , , , ,
- **Regla de Negocio**:
 - Evaluación de baseline (que pasaria sin ISO?)
 - Base para comparar efectividad de controles
 - Se evalua con capacidad del atacante, tendencias de threats
- **Ejemplo**: (Alta probabilidad sin controles)

#### `inherent_impact` [Integer, CHECK(-), NOT NULL]
- **Descripción**: Impacto del riesgo (=Muy bajo, =Catastrófico)
- **Tipo de Dato**: Integer
- **Constraint**: CHECK (inherent_impact BETWEEN AND ), NOT NULL
- **Validación**: Solo , , , ,
- **Regla de Negocio**:
 - Daño financiero, reputacional, regulatorio
 - No cambia con controles (impacto es mismo)
- **Ejemplo**: (Catastrófico si datos se filtran)

#### `residual_likelihood` [Integer, CHECK(-), NOT NULL]
- **Descripción**: Probabilidad CON controles implementados
- **Tipo de Dato**: Integer
- **Constraint**: CHECK (residual_likelihood BETWEEN AND ), NOT NULL
- **Validación**:
 - Solo , , , ,
 - residual_likelihood <= inherent_likelihood (controles reducen)
 - CHECK (residual_likelihood <= inherent_likelihood)
- **Regla de Negocio**:
 - Se reduce gracias a controles ISO
 - Mide efectividad de defensa
 - Si no reduce, seleccionar mas controles
- **Ejemplo**: (Baja probabilidad con encryption + MFA)

#### `residual_impact` [Integer, CHECK(-), NOT NULL]
- **Descripción**: Impacto residual CON controles
- **Tipo de Dato**: Integer
- **Constraint**: CHECK (residual_impact BETWEEN AND ), NOT NULL
- **Validación**:
 - Solo -
 - residual_impact <= inherent_impact
 - CHECK (residual_impact <= inherent_impact)
- **Regla de Negocio**:
 - Controles mitigan impacto (ej: backup reduce perdida de datos)
 - Algunos riesgos no se mitigam en impacto (ej: reputacion)
- **Ejemplo**: (Siguen siendo datos criticos, impacto no cambia)

#### `treatment` [ENUM: ACCEPT/MITIGATE/TRANSFER/AVOID, NOT NULL]
- **Descripción**: Estrategia de tratamiento del riesgo
- **Dominios de Valores**:
```
 MITIGATE - Implementar controles para reducir likelihood o impact
 AVOID - Cambiar proceso/ARQUITECTURA para evitar riesgo
 TRANSFER - Pasar riqueza a tercero (seguro, proveedor)
 ACCEPT - Documentar y aceptar conscientemente el riesgo
 ```
- **Validación**:
 - Solo valores del dominio
 - Si treatment=ACCEPT y inherent_risk_score >= -> ERROR
 (no se puede aceptar riesgo intolerable)
- **Regla de Negocio**:
 - Define uso de controles en SoAItems
 - Documenta decision de riesgo
- **Ejemplo**: `MITIGATE`

#### `mitigation_plan` [Text, Nullable]
- **Descripción**: Plan detallado de como se mitiga el riesgo
- **Validación**: Max 0,000 caracteres
- **Regla de Negocio**:
 - Solo si treatment = MITIGATE
 - Debe incluir: controles, responsable, timeline, comprobables
- **Ejemplo**: `Implementar MFA antes -Mar-0(respons: CISO)...`

#### `owner_id` [FK -> User, Nullable]
- **Descripción**: Usuario responsable del riesgo
- **Constraint**: FK(User.id), NULL allowed
- **Validación**: Debe ser CONSULTANT o ADMIN
- **Regla de Negocio**:
 - Accountable del tratamiento del riesgo
 - Notificado cuando riesgo cambia de estado
- **Ejemplo**: 8 (CISO)

#### `status` [ENUM: IDENTIFIED/ASSESSED/MITIGATED/MONITORED, NOT NULL]
- **Descripción**: Estado del riesgo en ciclo de vida
- **Dominios de Valores**: {IDENTIFIED, ASSESSED, MITIGATED, MONITORED}
- **Regla de Negocio**:
 - IDENTIFIED: Riesgo identificado pero no analizado
 - ASSESSED: Evaluado, controles seleccionados
 - MITIGATED: Controles implementados, evidencia aprobada
 - MONITORED: En revisión periodica
- **Ejemplo**: `MITIGATED`

#### `created_at`, `updated_at` [DateTime]
- **Validación**: Auto-managed
- **Ejemplo**: `0-0-0:00:00`

### Propiedades Calculadas (No se guardan)

```python
@property
def inherent_risk_score(self):
 """Score sin controles: likelihood x impact (rango: -)"""
 return self.inherent_likelihood * self.inherent_impact

@property
def residual_risk_score(self):
 """Score con controles: likelihood x impact (rango: -)"""
 return self.residual_likelihood * self.residual_impact

@property
def risk_reduction(self):
 """Puntos reducidos por controles"""
 return self.inherent_risk_score - self.residual_risk_score

@property
def risk_reduction_percentage(self):
 """Porcentaje de reduccion: (inherent - residual) / inherent * 00"""
 if self.inherent_risk_score == 0:
 return 0
 return (self.risk_reduction / self.inherent_risk_score) * 00
```

---

## ASSET (Activos)

### Propósito
Inventario de activos de información en alcance del SGSI.

### Campos Clave

#### `id` [PK, Integer]
- **Ejemplo**: 0

#### `project_id` [FK -> Project, NOT NULL]
- **Constraint**: FK(Project.id), NOT NULL, ON DELETE CASCADE
- **Ejemplo**:

#### `name` [Varchar(255)]
- **Descripción**: Nombre del activo
- **Constraint**: NOT NULL
- **Validación**: Único por proyecto: UNIQUE (project_id, name)
- **Ejemplo**: `Base de Datos Clientes`

#### `type` [ENUM: HARDWARE/SOFTWARE/DATA/PERSONNEL/FACILITY, NOT NULL]
- **Descripción**: Tipo de activo
- **Dominios de Valores**:
```
 HARDWARE - Servidores, PCs, routers, switches, etc.
 SOFTWARE - Aplicaciones, bases de datos, sistemas operativos
 DATA - Datos, informacion, registros, documentos
 PERSONNEL - Personas, conocimiento, competencias
 FACILITY - Inmuebles, data centers, oficinas
 ```
- **Ejemplo**: `DATA`

#### `description` [Text, Nullable]
- **Descripción**: Descripción detallada del activo
- **Ejemplo**: `Base de datos PostgreSQL con información de 0,000+ clientes...`

#### `owner_id` [FK -> User, Nullable]
- **Descripción**: Propietario del activo (quien es responsable)
- **Constraint**: NULL allowed
- **Ejemplo**: (Database Administrator)

#### `location` [Varchar(255), Nullable]
- **Descripción**: Ubicación fisica o lógica
- **Ejemplo**: `AWS Region us-east-`, `Data Center Bogota Piso `

#### `criticality` [ENUM: LOW/MEDIUM/HIGH/CRITICAL]
- **Descripción**: Criticidad del activo
- **Dominios de Valores**:
```
 LOW - Perdida no impacta operaciones significativamente
 MEDIUM - Impacto moderado en operaciones
 HIGH - Impacto severo en operaciones (pocas horas inactividad)
 CRITICAL - Impacto catastrofico (indisponibilidad inmediata)
 ```
- **Ejemplo**: `CRITICAL`

#### `confidentiality_level` [Integer, CHECK(-)]
- **Descripción**: Clasificacion de confidencialidad (=Publico, =Secreto)
- **Constraint**: CHECK (confidentiality_level BETWEEN AND ), NOT NULL
- **Dominios de Valores**:
```
 : Publico (informacion publica, sin restriccion)
 : Interno (uso interno empresa, proteccion basica)
 : Confidencial (informacion sensible, proteccion media)
 : Altamente Confidencial (datos criticos, proteccion fuerte)
 : Secreto (datos maxima proteccion: PII, financiero, medico)
 ```
- **Ejemplo**:

#### `integrity_level` [Integer, CHECK(-)]
- **Descripción**: Requisito de integridad (=No critico, =Maximo)
- **Constraint**: CHECK (integrity_level BETWEEN AND ), NOT NULL
- **Ejemplo**: (Datos de transaciones, no pueden estar corrompidos)

#### `availability_level` [Integer, CHECK(-)]
- **Descripción**: Requisito de disponibilidad (=No critico, =/7)
- **Constraint**: CHECK (availability_level BETWEEN AND ), NOT NULL
- **Dominios de Valores**:
```
 : No critico (indisponibilidad aceptable)
 : Bajo (indisponibilidad > 8 horas aceptable)
 : Medio (indisponibilidad -8 horas aceptable)
 : Alto (indisponibilidad < horas inaceptable)
 : Critico (disponibilidad /7 sin interrupcion)
 ```
- **Ejemplo**:

#### `created_at`, `updated_at` [DateTime]
- **Validación**: Auto-managed
- **Ejemplo**: `0-0-0:00:00`

---

## ISOCONTROL (Controles)

### Propósito
Catálogo maestro inmutable de 93 controles ISO 27001:2022.

### Campos Clave

#### `id` [PK, Integer]
- **Ejemplo**:

#### `code` [Varchar(20), UNIQUE, NOT NULL]
- **Descripción**: Codigo ISO del control (A.., A.., ..., A..)
- **Validación**: Formato A.X.Y (único)
- **Regla de Negocio**:
 - Codigo oficial de ISO 27001:2022
 - Nunca cambia
 - indice de busqueda primaria
- **Ejemplo**: `A.8.`

#### `name` [Varchar(255)]
- **Descripción**: Nombre corto del control
- **Constraint**: NOT NULL
- **Ejemplo**: `Control de acceso`

#### `description` [Text]
- **Descripción**: Descripción completa del control
- **Constraint**: NOT NULL
- **Ejemplo**: `User access to information and IT systems shall be managed...`

#### `category` [Varchar(20), ENUM]
- **Descripción**: Dominio/categoria del Anexo A
- **Dominios de Valores**:
```
 A.: Organizational Controls
 A.: People Controls
 A.7: Physical Controls
 A.8: Technical Controls
 A.9: Management Controls
 ```
- **Ejemplo**: `A.8` (Technical Controls)

#### `iso_27001_text` [Text]
- **Descripción**: Texto oficial de ISO 27001:2022 para este control
- **Constraint**: NOT NULL
- **Regla de Negocio**: Fuente de verdad legal
- **Ejemplo**: `[Texto oficial ISO]`

#### `requirements` [Text]
- **Descripción**: Requisitos especificos de implementación
- **Constraint**: NOT NULL
- **Ejemplo**: `Implement MFA, Log all access attempts, Review access controls quarterly...`

#### `implementation_guidance` [Text, Nullable]
- **Descripción**: Guia de implementación practica
- **Ejemplo**: `Use TOTP or push notifications for MFA authorization...`

#### `created_at` [DateTime, Auto Now Add]
- **Constraint**: NOT NULL
- **Validación**: Immutable (registro maestro)
- **Ejemplo**: `0-0-000:00:00`

### Reglas Especiales

```python
# ISOControl es READ-ONLY
def save(self):
 if self.pk is not None: # Update intento
 raise ValidationError("ISOControl is immutable (reference data)")
 super().save()

def delete(self):
 raise ValidationError("ISOControl cannot be deleted (reference data)")

# Precargado: 93 controles exactos
# Carga via management command: python manage.py load_iso_controls csv
```

---

## SOAITEM (Aplicabilidad)

### Propósito
Statement of Applicability - registro de aplicabilidad de cada control por proyecto.

### Campos Clave

#### `id` [PK, Integer]
- **Ejemplo**: 0

#### `project_id` [FK -> Project, NOT NULL]
- **Constraint**: FK(Project.id), NOT NULL, ON DELETE CASCADE
- **Ejemplo**:

#### `iso_control_id` [FK -> ISOControl, NOT NULL]
- **Constraint**: FK(ISOControl.id), NOT NULL
- **Ejemplo**: 8 (A.8.)

#### `is_applicable` [Boolean, NOT NULL, Default=True]
- **Descripción**: Se aplica este control en el proyecto?
- **Dominios de Valores**: `true` (si aplica), `false` (no aplica)
- **Validación**: Boolean
- **Regla de Negocio**:
 - true: Empresa DEBE implementar este control
 - false: Empresa JUSTIFICA por qué no aplica
- **Ejemplo**: true

#### `justification` [Text, Nullable]
- **Descripción**: Justificacion de por qué no aplica (si is_applicable=false)
- **Validación**:
 - Requerido si is_applicable=false
 - CHECK (is_applicable OR justification IS NOT NULL)
 - Max: ,000 caracteres
- **Regla de Negocio**:
 - Justificacion legal y técnica para auditor externo
 - Auditor revisa y puede rechazar la justificacion
- **Ejemplo**: `Control no aplica: empresa no procesa datos sensibles de salud (HIPAA excepto)`

#### `implementation_status` [ENUM: NOT_IMPLEMENTED/IN_PROGRESS/IMPLEMENTED]
- **Descripción**: Estado de implementación del control
- **Dominios de Valores**:
```
 NOT_IMPLEMENTED - No se ha iniciado implementacion
 IN_PROGRESS - Implementacion en curso
 IMPLEMENTED - Control implementado y evidenciado
 ```
- **Validación**:
 - Solo aplica si is_applicable=true
 - CHECK (NOT is_applicable OR implementation_status IS NOT NULL)
- **Regla de Negocio**:
 - Triable a phase del proyecto:
 - PLANNING -> NOT_IMPLEMENTED
 - IN_PROGRESS -> IN_PROGRESS
 - COMPLETED -> IMPLEMENTED (idealmente)
 - Solo controles IMPLEMENTED cuentan para certificacion
- **Ejemplo**: `IMPLEMENTED`

#### `implementation_date` [Date, Nullable]
- **Descripción**: Fecha de implementación
- **Validación**:
 - Solo si implementation_status = IMPLEMENTED
 - implementation_date <= today()
- **Ejemplo**: `0-0-0`

#### `responsible_id` [FK -> User, Nullable]
- **Descripción**: Usuario responsable de implementar
- **Constraint**: NULL allowed
- **Ejemplo**: (CISO)

#### `created_at`, `updated_at` [DateTime]
- **Validación**: Auto-managed
- **Ejemplo**: `0-0-0:00:00`

### Restricciones Especiales

```python
# Generacion automatica
@receiver(post_save, sender=Project)
def create_soa_items(sender, instance, created, **kwargs):
 if created:
 controls = ISOControl.objects.all()
 for control in controls:
 SoAItem.objects.create(
 project=instance,
 iso_control=control,
 is_applicable=True
 )

# Unicidad: Un control por proyecto
UNIQUE (project_id, iso_control_id)

# Validaciones de cambio
def save(self):
 # Si is_applicable cambia de True a False, requeire justificacion
 if not self.is_applicable and not self.justification:
 raise ValidationError("Justificacion requerida para controles no aplicables")
 super().save()
```

---

## EVIDENCE (Evidencias)

### Propósito
Archivos que demuestran la implementación de controles ISO.

### Campos Clave

#### `id` [PK, Integer]
- **Ejemplo**:

#### `project_id` [FK -> Project, NOT NULL]
- **Constraint**: FK(Project.id), NOT NULL, ON DELETE CASCADE
- **Ejemplo**:

#### `iso_control_id` [FK -> ISOControl, Nullable]
- **Descripción**: Control que esta evidencia respalda
- **Constraint**: NULL allowed (evidencia sin asignacion inicial)
- **Validación**: Debe ser control valido si se especifica
- **Ejemplo**: 8 (A.8.)

#### `name` [Varchar(255)]
- **Descripción**: Nombre descriptivo de la evidencia
- **Constraint**: NOT NULL
- **Ejemplo**: `MFA Configuration Screenshot`

#### `description` [Text, Nullable]
- **Descripción**: Detalles sobre la evidencia
- **Ejemplo**: `Screenshot of MFA configuration in AWS IAM console...`

#### `file` [FileField]
- **Descripción**: Archivo archivado (PDF, DOCX, imagen, etc.)
- **Constraint**: NOT NULL
- **Validación**:
 - Tamano maximo: 0 MB
 - Tipos permitidos: PDF, DOCX, XLSX, PPTX, PNG, JPG, ZIP
 - MIME type validation
- **Almacenamiento**: AWS So local filesystem
- **Regla de Negocio**:
 - Archivos encriptados en almacenamiento
 - Acceso controlado por roles
 - Historico de descargas auditado
- **Ejemplo**: `mfa_configuration.pdf` (0 MB)

#### `file_size` [Integer]
- **Descripción**: Tamano del archivo en bytes
- **Constraint**: NOT NULL, CHECK (file_size > 0 AND file_size <= 0870)
- **Validación**: Automático al subir
- **Ejemplo**: 097(MB)

#### `file_type` [Varchar(100)]
- **Descripción**: MIME type del archivo
- **Constraint**: NOT NULL
- **Validación**: application/pdf, application/vnd.openxmlformats-officedocument.wordprocessingml.document, etc.
- **Ejemplo**: `application/pdf`

#### `uploaded_by_id` [FK -> User, NOT NULL]
- **Descripción**: Usuario que subio el archivo
- **Constraint**: FK(User.id), NOT NULL
- **Validación**: Must be user con acceso al proyecto
- **Ejemplo**: 9 (usuario del cliente)

#### `status` [ENUM: PENDING/APPROVED/REJECTED, NOT NULL, Default=PENDING]
- **Descripción**: Estado de revisión de evidencia
- **Dominios de Valores**:
```
 PENDING - Evidencia recien subida, en espera de revisión
 APPROVED - Admin/Consultor aprobo, cuenta para SoA
 REJECTED - Admin rechazo, no cuenta para SoA
 ```
- **Validación**: Solo valores del dominio
- **Regla de Negocio**:
 - Solo APPROVED cuentan como comprobante de control
 - REJECTED requiere evidencia nueva
- **Ejemplo**: `PENDING`

#### `approved_by_id` [FK -> User, Nullable]
- **Descripción**: Admin/Consultor que aprobo la evidencia
- **Constraint**: FK(User.id), NULL allowed
- **Validación**:
 - Requerido si status = APPROVED
 - Debe ser ADMIN o CONSULTANT
- **Regla de Negocio**:
 - AuditLog registra quien y cuando aprobo
 - Responsabilidad explicita de aprobacion
- **Ejemplo**: (CISO approves)

#### `version` [Integer, NOT NULL, Default=]
- **Descripción**: Número de version del archivo
- **Constraint**: NOT NULL, CHECK (version >= )
- **Validación**: Auto-increment al crear nueva version
- **Regla de Negocio**:
 - Versión es original
 - Versión + son revisiónes
 - Historial completo mantenido
- **Ejemplo**: (v), (v)

#### `previous_version_id` [FK -> Evidence, Self-reference, Nullable]
- **Descripción**: Referencia a version anterior
- **Constraint**: FK(Evidence.id), NULL allowed
- **Validación**:
 - Self-FK (Evidence -> Evidence)
 - Si version= -> NULL
 - Si version> -> debe existir version anterior
 - CHECK (version=OR previous_version_id IS NOT NULL)
- **Regla de Negocio**:
 - Crea cadena: v -> v -> v
 - Historial completo rastreable
 - Auditor puede revisar cambios
- **Ejemplo**: (referencia a version anterior)

#### `is_current` [Boolean, NOT NULL, Default=True]
- **Descripción**: Es la version actual?
- **Constraint**: NOT NULL
- **Validación**:
 - Maximo Evidence por (project, name) con is_current=true
 - UNIQUE (project_id, name, version) WHERE is_current=true
- **Regla de Negocio**:
 - Identifica version «en vigor»
 - API retorna is_current por defecto
 - Historial accesible pero no es version oficial
- **Ejemplo**: true

#### `version_notes` [Text, Nullable]
- **Descripción**: Notas de cambio en esta version
- **Validación**: Max ,000 caracteres
- **Regla de Negocio**:
 - Changelog: «que cambio en vvs v»
 - Usado por auditor para entender evolucion
- **Ejemplo**: `Updated MFA config for Google Workspace integration, fixed screenshot date`

#### `created_at`, `updated_at` [DateTime]
- **Validación**: Auto-managed
- **Ejemplo**: `0-0-0:00:00`

### Versionado de Evidence

```python
# Crear nueva version
def create_new_version(self, file, version_notes):
 # Marcar version actual como historica
 old_version = self
 old_version.is_current = False
 old_version.save()
 
 # Crear nueva version
 new_version = Evidence.objects.create(
 project=self.project,
 iso_control=self.iso_control,
 name=self.name,
 file=file,
 uploaded_by=current_user,
 version=old_version.version + ,
 previous_version=old_version,
 is_current=True,
 version_notes=version_notes,
 status="PENDING" # Nueva version requiere re-aprobacion
 )
 return new_version
```

---

## DOCUMENT (Documentos)

### Propósito
Documentos generados automáticamente (plantillas, reportes).

### Campos Clave

#### `id` [PK, Integer]
- **Ejemplo**:

#### `project_id` [FK -> Project, Nullable]
- **Descripción**: Proyecto asociado (NULL si es plantilla global)
- **Constraint**: FK(Project.id), NULL allowed
- **Validación**: Si no NULL, debe existir
- **Ejemplo**: (proyecto especifico)

#### `type` [ENUM: POLICY/RISK_REGISTER/SOA/ASSET_INVENTORY, NOT NULL]
- **Descripción**: Tipo de documento
- **Dominios de Valores**:
```
 POLICY - Politicas de seguridad
 RISK_REGISTER - Registro de riesgos
 SOA - Statement of Applicability (PDF)
 ASSET_INVENTORY - Inventario de activos
 CONTROL_MATRIX - Matriz de controles
 AUDIT_REPORT - Reporte de auditoria
 TRAINING_MATERIAL - Material de conciencia
 ```
- **Ejemplo**: `SOA`

#### `title` [Varchar(255)]
- **Descripción**: Titulo del documento
- **Constraint**: NOT NULL
- **Ejemplo**: `Statement of Applicability - ISO 27001:2022`

#### `description` [Text, Nullable]
- **Descripción**: Descripción del documento
- **Ejemplo**: `SoA report generated on 0-0-covering 9ISO 27001controls...`

#### `file` [FileField]
- **Descripción**: Archivo generado (PDF, DOCX)
- **Constraint**: NOT NULL
- **Validación**: PDF o DOCX
- **Almacenamiento**: So local filesystem
- **Ejemplo**: `soa_report_00.pdf`

#### `is_template` [Boolean, NOT NULL, Default=False]
- **Descripción**: Es plantilla maestra o documento generado?
- **Dominios de Valores**:
```
 true: Plantilla maestra (texto generico, puede reutilizarse)
 false: Documento generado para proyecto especifico (datos personalizados)
 ```
- **Regla de Negocio**:
 - Templates: project_id = NULL
 - Generated: project_id = NOT NULL
 - Templates modificados por ADMIN, Generated readonly
- **Ejemplo**: false

#### `version` [Integer, NOT NULL, Default=]
- **Descripción**: Versión del documento
- **Validación**: CHECK (version >= )
- **Regla de Negocio**:
 - v: Generación inicial
 - v+: Actualizaciones (project modificado, SoA cambio, etc.)
- **Ejemplo**:

#### `generated_by_id` [FK -> User, Nullable]
- **Descripción**: Usuario que genero
- **Constraint**: FK(User.id), NULL allowed
- **Validación**: Si not NULL, debe ser ADMIN o CONSULTANT
- **Ejemplo**: (CISO genero el SoA)

#### `created_at` [DateTime, Auto Now Add]
- **Validación**: Immutable
- **Ejemplo**: `0-0-:0:00`

---

## AUDITLOG (Auditoría)

### Propósito
Trazabilidad completa de cambios criticos (ISO 27001 exige auditoría).

### Campos Clave

#### `id` [PK, Integer]
- **Ejemplo**: 0

#### `user_id` [FK -> User, NOT NULL]
- **Descripción**: Usuario que realizo la accion
- **Constraint**: FK(User.id), NOT NULL, ON DELETE SET_NULL
- **Validación**: Debe ser usuario valido (si existe)
- **Ejemplo**: 9 (usuario admin)

#### `action` [ENUM: CREATE/UPDATE/DELETE/APPROVE/REJECT, NOT NULL]
- **Descripción**: Tipo de accion realizada
- **Dominios de Valores**:
```
 CREATE - Nuevo registro creado
 UPDATE - Registro modificado
 DELETE - Registro eliminado (soft delete)
 APPROVE - Registro aprobado (Evidence, Risk, etc.)
 REJECT - Registro rechazado
 ```
- **Validación**: Solo valores del dominio
- **Regla de Negocio**:
 - CREATE / UPDATE / DELETE para cambios de datos
 - APPROVE / REJECT para documentos y evidencias
- **Ejemplo**: `UPDATE`

#### `model_name` [Varchar(00)]
- **Descripción**: Nombre del modelo afectado
- **Constraint**: NOT NULL
- **Validación**:
 - Debe ser modelo real de la app
 - Ej: «Risk», «Evidence», «SoAItem», «User», «Project»
- **Regla de Negocio**:
 - Referencia a que tabla se modifico
 - Permite busqueda: «Mostrar todos los audits de Risk»
- **Ejemplo**: `Evidence`

#### `object_id` [Integer]
- **Descripción**: ID del registro modificado
- **Constraint**: NOT NULL
- **Validación**: Entero positivo
- **Regla de Negocio**:
 - Identificador del objeto especifico
 - Permite trazar: «Mostrar historial de Evidence #»
- **Ejemplo**: (ID de la Evidence)

#### `object_description` [Varchar(255), Nullable]
- **Descripción**: Descripción legible del objeto (para referencia rapida)
- **Validación**: Max caracteres
- **Regla de Negocio**:
 - «MFA Configuration Screenshot» (nombre de Evidence)
 - Permite auditor entender sin buscar el objeto
- **Ejemplo**: `MFA Configuration Screenshot`

#### `timestamp` [DateTime, Auto Now Add]
- **Descripción**: Momento exacto de la accion
- **Constraint**: Auto Now Add, NOT NULL
- **Precision**: Milisegundos (YYYY-MM-DD HH:MM:SS.mmm)
- **Validación**: Immutable
- **Regla de Negocio**:
 - Identificador temporal único
 - Orden cronologico de eventos
 - Cumplimiento regulatorio
- **Ejemplo**: `0-0-::.`

#### `changes` [JSON, Nullable]
- **Descripción**: Cambios especificos (antes/despues) para UPDATE
- **Tipo de Dato**: JSON object
- **Constraint**: NULL allowed (no aplica para CREATE/DELETE)
- **Validación**: JSON valido
- **Regla de Negocio**:
 - Captura deltas de cambios
 - Permite auditor saber que cambio
 - Ejemplo para UPDATE:
```json
 {
 "status": {"before": "PENDING", "after": "APPROVED"},
 "implementation_status": {"before": "NOT_IMPLEMENTED", "after": "IMPLEMENTED"},
 "updated_by": {"before": null, "after": }
 }
 ```
- **Ejemplo**: (JSON arriba)

#### `ip_address` [Varchar(45), Nullable]
- **Descripción**: IP del cliente que realizo la accion
- **Constraint**: NULL allowed
- **Validación**:
 - IPv: XXX.XXX.XXX.XXX
 - IPv: Valid IPvformat
- **Regla de Negocio**:
 - Seguridad: detectar patrones anomalos
 - Cumplimiento: donde se realizo cambio
 - Privacidad: almacenar con cuidado (GDPR)
- **Ejemplo**: `9.8..00`, `00:0db8::`

#### `user_agent` [Text, Nullable]
- **Descripción**: Browser/Client usado
- **Validación**: Max 000 caracteres
- **Regla de Negocio**:
 - Identifica tipo de cliente (web, mobile, API)
 - Deteccion de bots
- **Ejemplo**: `Mozilla/.0 (Windows NT 0.0; Win; x) Chrome/9.0..`

### Registros automáticos

```python
# Señales (signals) automáticas para registrar cambios
@receiver(post_save, sender=Risk)
def audit_risk_changes(sender, instance, created, raw, **kwargs):
 if raw:
 return # Skip if loading fixtures
 
 if created:
 AuditLog.objects.create(
 user=current_user,
 action="CREATE",
 model_name="Risk",
 object_id=instance.id,
 object_description=instance.name,
 changes=None
 )
 else:
 # Detectar cambios (before/after comparison)
 changes = detect_changes(instance, old_values)
 AuditLog.objects.create(
 user=current_user,
 action="UPDATE",
 model_name="Risk",
 object_id=instance.id,
 object_description=instance.name,
 changes=changes,
 ip_address=request.META.get('REMOTE_ADDR'),
 user_agent=request.META.get('HTTP_USER_AGENT')
 )

@receiver(post_delete, sender=Evidence)
def audit_evidence_deletion(sender, instance, **kwargs):
 AuditLog.objects.create(
 user=current_user,
 action="DELETE",
 model_name="Evidence",
 object_id=instance.id,
 object_description=instance.name,
 changes=None
 )
```

---

## Resumen de Validaciones

| Validación | Aplicar En | Tipo |
|---|---|---|
| Username Unicidad | User | UNIQUE |
| Email format | User, Company | REGEX |
| Password strength | User | REGEX (creacion) |
| Risk scores -| Risk | CHECK |
| Risk residual <= inherent | Risk | CHECK |
| CIA levels -| Asset | CHECK |
| Percentage 0-00 | Phase | CHECK |
| Date consistency | Project, Phase, Task | CHECK |
| UNIQUE per project | Project.name, Risk.name, Asset.name | UNIQUE |
| SoAItem Unicidad | SoAItem | UNIQUE (project, control) |
| Evidence version | Evidence | Versión cascading |

---

**Diccionario preparado por el equipo VIT**
**Última revisión**: de febrero de 0
**Aplicable a**: Versión Backend .0+
