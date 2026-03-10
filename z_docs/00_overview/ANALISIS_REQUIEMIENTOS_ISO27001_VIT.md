Ahora tengo toda la informaciÃ³n necesaria. Voy a compilar un anÃ¡lisis exhaustivo basado en todos los documentos que he revisado:

---

# ðŸ“Š ANÃLISIS COMPLETO DE VIT - PLATAFORMA SGSI ISO 27001

## A) RESUMEN EJECUTIVO

### Â¿QuÃ© es VIT? Â¿CuÃ¡l es su propÃ³sito principal?

**VIT** es una plataforma web B2B diseÃ±ada para asistir a empresas en la **implementaciÃ³n completa de un Sistema de GestiÃ³n de Seguridad de la InformaciÃ³n (SGSI)** conforme a la norma **ISO/IEC 27001:2022**. 

**PropÃ³sito principal:**
- Simplificar el proceso de certificaciÃ³n ISO 27001 mediante una plataforma digital estructurada
- Automatizar gestiÃ³n de riesgos (cÃ¡lculo inherente/residual), controles, y evidencias
- Generar documentaciÃ³n y reportes de cumplimiento (SoA, auditorÃ­as, mÃ©tricas)
- Proporcionar trazabilidad completa (auditorÃ­a QUIEN/QUE/CUANDO) para cumplimiento normativo

### Â¿A quiÃ©n va dirigida la plataforma?

VIT utiliza **3 roles principales** con acceso y funcionalidades diferenciados:

1. **Administrador VIT (ADMIN)**
   - Personal de VIT (empresa proveedora de servicios)
   - Acceso: todas las empresas, todos los proyectos
   - Permisos: CRUD completo, gestiÃ³n de usuarios, reportes globales, definir templates
   - Caso de uso: gestiÃ³n central de la plataforma

2. **Consultor ISO (CONSULTANT)**
   - Consultores internos o externos especializados en ISO 27001
   - Acceso: proyectos asignados como consultor responsable
   - Permisos: crear proyectos, realizar diagnÃ³sticos, evaluar riesgos, seleccionar controles, auditar
   - Caso de uso: liderazgo tÃ©cnico de implementaciÃ³n ISO

3. **Cliente/Empresa (CLIENT)**
   - Personal de empresas implementando ISO 27001
   - Acceso: solo sus propios proyectos dentro su empresa
   - Permisos: ver progreso, cargar evidencias, revisar SoA, ver resultados
   - Caso de uso: ejecuciÃ³n local de control de cambios, operaciones

### Â¿CuÃ¡l es el alcance principal de ISO 27001 que cubre?

VIT cubre **el ciclo de vida ISO 27001 COMPLETO** (fases 0-5):

- **F0 Inicio**: Charter, RACI, planificaciÃ³n
- **F1 Contexto y Alcance**: anÃ¡lisis de contexto, definiciÃ³n de alcance, polÃ­tica de SI
- **F2 Riesgos y Controles**: inventario de activos, evaluaciÃ³n de riesgos, selecciÃ³n de 93 controles (Anexo A), SoA justificado
- **F3 ImplementaciÃ³n y OperaciÃ³n**: procedimientos, capacitaciÃ³n, control operativo, evidencias
- **F4 EvaluaciÃ³n y Mejora**: KPIs, auditorÃ­a interna, revisiÃ³n direcciÃ³n
- **F5 Readiness**: simulacro, cierre de GAPs

---

## B) REQUERIMIENTOS FUNCIONALES (RF) Y CASOS DE USO

### Requerimientos Funcionales Identificados

#### **RF1: AutenticaciÃ³n y GestiÃ³n de Usuarios**
- **DescripciÃ³n**: Sistema de login con JWT, roles y permisos por rol
- **Usuarios/roles involucrados**: Admin, Consultant, Client
- **Subrequisitos**:
  - RF1.1: Login con username/password (retorna access + refresh tokens)
  - RF1.2: Refresh token (renovar access sin re-login)
  - RF1.3: Logout
  - RF1.4: Crear/editar/desactivar usuarios (solo Admin)
  - RF1.5: Cambio de contraseÃ±a
  - RF1.6: Reset de contraseÃ±a via email (future)

#### **RF2: GestiÃ³n de Empresas**
- **DescripciÃ³n**: Registro y administraciÃ³n de empresas cliente
- **Usuarios/roles involucrados**: Admin
- **Subrequisitos**:
  - RF2.1: Crear empresa (nombre, RFC, contacto, direcciÃ³n)
  - RF2.2: Editar empresa
  - RF2.3: Listar empresas (Admin ve todas; Client solo su empresa)
  - RF2.4: Asignar usuarios a empresas
  - RF2.5: Ver proyectos por empresa

#### **RF3: GestiÃ³n de Proyectos ISO 27001**
- **DescripciÃ³n**: Crear y gestionar proyectos de implementaciÃ³n SGSI
- **Usuarios/roles involucrados**: Admin, Consultant (creador), Client (consultado)
- **Subrequisitos**:
  - RF3.1: Crear proyecto (nombre, empresa, fecha inicio, consultor responsable)
  - RF3.2: Editar proyecto
  - RF3.3: Listar proyectos (con filtros: empresa, estado, consultor)
  - RF3.4: Cambiar estado proyecto (PLANNING â†’ IN_PROGRESS â†’ COMPLETED)
  - RF3.5: Asignar usuarios a proyecto (ProjectUser con rol especÃ­fico)
  - RF3.6: Ver progreso del proyecto (% de fases completadas)

#### **RF4: GestiÃ³n de Fases y Tareas**
- **DescripciÃ³n**: Dividir proyectos en fases metodolÃ³gicas con tareas
- **Usuarios/roles involucrados**: Consultant (crea/edita), Client (ve estado)
- **Subrequisitos**:
  - RF4.1: Crear fases (INIT, PLAN, IMPLEMENT, MAINTAIN, CERTIFY) en proyecto
  - RF4.2: Crear tareas dentro de fase (con descripciÃ³n, responsable, fecha vencimiento)
  - RF4.3: Cambiar estado tarea (NOT_STARTED â†’ IN_PROGRESS â†’ COMPLETED)
  - RF4.4: Listar tareas por fase (con % completado)
  - RF4.5: Asignar tarea a usuario

#### **RF5: DefiniciÃ³n de Alcance y Activos**
- **DescripciÃ³n**: Definir quÃ© sistemas/datos estÃ¡n en alcance SGSI
- **Usuarios/roles involucrados**: Consultant (define), Admin/Client (revisa)
- **Subrequisitos**:
  - RF5.1: Crear Scope (alcance inicial, sistemas incluidos, exclusiones, justificaciÃ³n)
  - RF5.2: Crear Activos (hardware, software, datos, personal, instalaciones)
  - RF5.3: Clasificar activos por criticidad (LOW/MEDIUM/HIGH/CRITICAL)
  - RF5.4: Asignar niveles CIA (Confidentiality, Integrity, Availability)
  - RF5.5: Asociar activo a dueÃ±o (usuario responsable)
  - RF5.6: Listar activos con filtros (tipo, criticidad, propietario)

#### **RF6: GestiÃ³n de Riesgos (Dual: Inherente/Residual)**
- **DescripciÃ³n**: EvaluaciÃ³n completa de riesgos antes y despuÃ©s de controles
- **Usuarios/roles involucrados**: Consultant (evalÃºa), Admin (revisa)
- **Subrequisitos**:
  - RF6.1: Crear riesgo (descripciÃ³n, causa, consecuencia, categorÃ­a)
  - RF6.2: Evaluar riesgo inherente (probabilidad 1-5 + impacto 1-5 = score)
  - RF6.3: Seleccionar controles mitigantes (N:M Risk â†” ISOControl)
  - RF6.4: Evaluar riesgo residual (prob + impacto POST-controles)
  - RF6.5: Calcular efectividad (inherente - residual = KPI)
  - RF6.6: Definir tratamiento (ACCEPT/MITIGATE/TRANSFER/AVOID)
  - RF6.7: Cambiar estado riesgo (IDENTIFIED â†’ ASSESSED â†’ MITIGATED â†’ MONITORED)
  - RF6.8: Listar riesgos con matriz (2D: Prob vs Impact, color-coded)
  - RF6.9: Filtrar riesgos (por estado, categorÃ­a, dueÃ±o, efectividad mÃ­nima)

#### **RF7: Mapeo de Controles ISO 27001 (SoA)**
- **DescripciÃ³n**: Mapeo de 93 controles del Anexo A con aplicabilidad por proyecto
- **Usuarios/roles involucrados**: Consultant (justifica), Admin (revisa), Client (operacionaliza)
- **Subrequisitos**:
  - RF7.1: Cargar catÃ¡logo 93 ISOControls (precargado, solo lectura)
  - RF7.2: Crear SoAItem automÃ¡tico (1 por control cuando creas proyecto)
  - RF7.3: Marcar control como aplicable/no aplicable
  - RF7.4: Justificar por quÃ© NO aplica (si aplica)
  - RF7.5: Cambiar estado implementaciÃ³n (NOT_IMPLEMENTED â†’ IN_PROGRESS â†’ IMPLEMENTED)
  - RF7.6: Asignar responsable implementaciÃ³n por control
  - RF7.7: Listar SoA (tabla completa 93 controles)
  - RF7.8: Filtrar SoA (por dominio, estado, responsable)
  - RF7.9: Exportar SoA (PDF/Excel)

#### **RF8: GestiÃ³n de Evidencias**
- **DescripciÃ³n**: Carga y versionado de documentos que prueban control implementado
- **Usuarios/roles involucrados**: Client (carga), Consultant/Admin (revisa y aprueba)
- **Subrequisitos**:
  - RF8.1: Subir archivo de evidencia (PDF, DOCX, XLSX, JPG, PNG)
  - RF8.2: Validar tipo y tamaÃ±o de archivo (mÃ¡x 50MB)
  - RF8.3: Asociar evidencia a SoAItem especÃ­fico
  - RF8.4: Versionar evidencias (v1 â†’ v2 â†’ v3, con historial)
  - RF8.5: Cambiar estado evidencia (PENDING â†’ APPROVED / REJECTED)
  - RF8.6: Dejar comentarios en revisiÃ³n
  - RF8.7: Descargar evidencia
  - RF8.8: Listar evidencias por proyecto/SoAItem
  - RF8.9: Auditar cambios (quiÃ©n, cuÃ¡ndo, quÃ© cambiÃ³)

#### **RF9: GeneraciÃ³n de Documentos y Reportes**
- **DescripciÃ³n**: Crear reportes e informes de cumplimiento SGSI
- **Usuarios/roles involucrados**: Consultant (genera), Admin (distribuye), Client (revisa)
- **Subrequisitos**:
  - RF9.1: Generar Documento SoA (con 93 controles, estado, evidencias)
  - RF9.2: Generar Reporte de Riesgos (matriz, grÃ¡ficas, KPIs)
  - RF9.3: Generar Reporte de Cumplimiento (% por fase, por control)
  - RF9.4: Generar Acta de RevisiÃ³n DirecciÃ³n
  - RF9.5: Generar Reporte Ejecutivo (resumen para stakeholders)
  - RF9.6: Exportar reportes a PDF/Excel
  - RF9.7: Programar envÃ­o de reportes por email
  - RF9.8: Ver historial de versiones de reportes

#### **RF10: AuditorÃ­a y Trazabilidad**
- **DescripciÃ³n**: Registro inmutable de todos los cambios (QUIEN/QUE/CUANDO/DONDE)
- **Usuarios/roles involucrados**: Admin (revisa logs), todos (generan eventos)
- **Subrequisitos**:
  - RF10.1: Auto-registrar CREATE/UPDATE/DELETE de entidades crÃ­ticas
  - RF10.2: Capturar IP, User-Agent, timestamp de cada evento
  - RF10.3: Guardar cambios antes/despuÃ©s (JSON diff)
  - RF10.4: Listar AuditLog con filtros (usuario, acciÃ³n, entidad, fecha)
  - RF10.5: Exportar AuditLog (para auditor externo)
  - RF10.6: Generar reportes de actividad por usuario

#### **RF11: Dashboard y KPIs**
- **DescripciÃ³n**: Visualizar mÃ©tricas de avance y cumplimiento SGSI
- **Usuarios/roles involucrados**: Consultant (estratÃ©gico), Client (operativo)
- **Subrequisitos**:
  - RF11.1: Dashboard por rol (Admin/Consultant/Client con vistas diferentes)
  - RF11.2: KPIs: % proyecto completado, % riesgos mitigados, % controles implementados
  - RF11.3: KRIs: riesgos residuales, control gaps, evidencias pendientes
  - RF11.4: GrÃ¡ficas: matriz de riesgos, cronograma fases, SoA estado
  - RF11.5: Tablas resumen: prÃ³ximas tareas, riesgos crÃ­ticos, cambios recientes

#### **RF12: Notificaciones y Alertas**
- **DescripciÃ³n**: Alertar usuarios sobre eventos crÃ­ticos, vencimientos
- **Usuarios/roles involucrados**: Todos
- **Subrequisitos** (future):
  - RF12.1: Tarea vencida â†’ notificaciÃ³n
  - RF12.2: Evidencia rechazada â†’ notificaciÃ³n
  - RF12.3: Cambio sensible en riesgo â†’ notificaciÃ³n
  - RF12.4: ReuniÃ³n de auditorÃ­a prÃ³xima â†’ recordatorio

### Casos de Uso Principales

#### **CU1: Empresa implementa ISO 27001 (flujo completo)**
1. Admin crea empresa "Bancolombia S.A."
2. Consultor "Carlos" se asigna como Consultant en proyecto
3. Carlos crea Proyecto "ISO 27001 Bancolombia"
4. Sistema auto-genera 5 fases + SoA (93 items)
5. Carlos define Scope y 50 Activos crÃ­ticos
6. Carlos evalÃºa 150 riesgos (inherente/residual con 93 controles)
7. Equipos de Bancolombia cargan evidencias para 93 controles
8. Carlos audita evidencias â†’ aprueba/rechaza
9. Sistema genera SoA final + Reporte Ejecutivo
10. Auditor externo descarga SoA + AuditLog â†’ certifica

#### **CU2: EvaluaciÃ³n de riesgo individual**
1. Consultant crea Riesgo: "Acceso no autorizado a BD"
2. Calcula Inherente: Prob=5, Impact=5 â†’ Score=25
3. Selecciona 3 controles: A.5.15, A.8.24, A.6.3
4. Calcula Residual: Prob=2, Impact=5 â†’ Score=10
5. Tratamiento: MITIGATE
6. Sistema registra: Risk â†’ SoAItem (3 items) â†’ Evidence (pendiente)
7. Client carga 3 archivos de evidencia
8. AuditLog registra cada movimiento

#### **CU3: AuditorÃ­a de cambios**
1. Admin abre panel AuditLog
2. Filtra: User="Carlos", Action="UPDATE", Entity="SoAItem", desde=hace 7 dÃ­as
3. Ve: Carlos cambiÃ³ 23 items "estado" a IMPLEMENTED
4. Abre cada uno: ve before/after (PENDING â†’ IMPLEMENTED)
5. Consulta IP: desde red corporativa Bancolombia
6. Genera reporte: "Carlos implementÃ³ 23 controles en 7 dÃ­as" + evidencias
7. Exporta para auditor externo

---

## C) FASES DE IMPLEMENTACIÃ“N ISO 27001

Basado en el Planner CSV y doctos arquitectÃ³nicos, VIT soporta 6 fases:

### **FASE 0: INICIO (F0)**
**DuraciÃ³n tÃ­pica**: 1-2 semanas  
**PropÃ³sito**: PlanificaciÃ³n y aprobaciÃ³n ejecutiva

**Actividades**:
- F0.1 Charter y RACI: Definir comitÃ©, roles, responsabilidades
- F0.2 Plan 150 dÃ­as: Definir hitos, entregables, recursos

**Entregables**:
- Charter aprobado
- RACI publicado
- Calendario de comitÃ©

**VIT genera/usa**:
- Proyecto creado
- Usuarios asignados (ProjectUser con roles)
- Fases auto-generadas

---

### **FASE 1: CONTEXTO Y ALCANCE (F1)**
**DuraciÃ³n tÃ­pica**: 3-4 semanas  
**PropÃ³sito**: Entender contexto interno/externo y definir lÃ­mite SGSI

**Actividades**:
- F1.1 Contexto/Partes: Matriz anÃ¡lisis contexto interno, partes interesadas, requisitos
- F1.2 Alcance/PolÃ­tica: Definir quÃ© sistemas/datos estÃ¡n in-scope, publicar polÃ­tica

**Entregables**:
- Matriz contexto documentada
- Matriz partes interesadas
- Matriz requisitos legales
- Documento Alcance SGSI
- PolÃ­tica Seguridad InformaciÃ³n publicada

**VIT genera/usa**:
- Scope creado (included systems, excluded systems, justification)
- Modelo: Scope (1:N con Project)

---

### **FASE 2: RIESGOS Y CONTROLES (F2)**
**DuraciÃ³n tÃ­pica**: 6-8 semanas  
**PropÃ³sito**: EvaluaciÃ³n completa de riesgos y selecciÃ³n de controles mitigantes

**Actividades**:
- F2.1 Inventario Activos: Catalogar TODOS los activos (hardware, software, datos, personal, instalaciones)
- F2.2 MetodologÃ­a/EvaluaciÃ³n: Definir escala de riesgos (Prob 1-5, Impact 1-5), evaluar 150-300 riesgos inherentes
- F2.3 PTR y SoA: 
  - PTR (Plan de Tratamiento de Riesgos): para cada riesgo â†’ seleccionar controles
  - SoA (Statement of Applicability): para cada of 93 ISO controls â†’ Aplicable SI/NO + justificaciÃ³n

**Entregables**:
- Hoja 04-Activos: Inventario completo (~50-200 activos)
- Matriz 05-Riesgos: 150-300 riesgos con scores inherente/residual
- Documento 06-PTR: Plan detallado de mitigaciÃ³n
- Documento 07-SoA: 93 items con estado (Aplicable/No Aplicable, NOT_IMPL/IN_PROGRESS/IMPLEMENTED)

**VIT genera/usa**:
- Asset creados (N assets)
- Risk creados y evaluados (inherent + residual scores calculados automÃ¡ticamente)
- Risk linked a ISOControl (N:M)
- SoAItem generados automÃ¡ticamente (93 items, 1 por ISOControl)
- Modelos: Asset, Risk, ISOControl (read-only), SoAItem

---

### **FASE 3: IMPLEMENTACIÃ“N Y OPERACIÃ“N (F3)**
**DuraciÃ³n tÃ­pica**: 8-12 semanas  
**PropÃ³sito**: Ejecutar plan de implementaciÃ³n de controles y operacionalizar SGSI

**Actividades**:
- F3.1 PolÃ­ticas/Procedimientos: Crear documentos (polÃ­ticas, procedimientos), capacitar equipos
- F3.2 Control Operativo: Implementar operaciones (control de cambios, gestiÃ³n terceros, logging)

**Entregables**:
- Procedimientos publicados y comunicados
- Registros operacionales (logs, auditorÃ­as internas)
- Capacitaciones completadas
- ITSM activo (tickets, CAB, CMDB)
- Matriz terceros (SaaS, proveedores, etc.)

**VIT genera/usa**:
- SoAItem estado â†’ IN_PROGRESS (equipos implementando)
- Evidence empiezan a cargarse (archivos que prueban implementaciÃ³n)
- Task estado â†’ COMPLETED
- AuditLog registra cada cambio de estado

---

### **FASE 4: EVALUACIÃ“N Y MEJORA (F4)**
**DuraciÃ³n tÃ­pica**: 4-6 semanas  
**PropÃ³sito**: Evaluar efectividad de controles, detectar gaps, mejorar

**Actividades**:
- F4.1 KPI/KRI: Definir mÃ©tricas de Ã©xito (% controls implemented, % risk reduction, incidentes, etc.)
- F4.2 AuditorÃ­a Interna: Ejecutar auditorÃ­a interna de SGSI, generar hallazgos (ACCs = Actions Correctivas)
- F4.3 RevisiÃ³n DirecciÃ³n: Acta ejecutiva con decisiones, recursos, mejoras

**Entregables**:
- KPIs definidos e iniciando mediciÃ³n
- Plan auditorÃ­a interno
- Informes de auditorÃ­a + Acciones Correctivas
- Acta RevisiÃ³n DirecciÃ³n
- Plan de mejora continua

**VIT genera/usa**:
- Tablero KPIs (% proyecto, % riesgos residuales, % controls implemented)
- Report AuditorÃ­a Interna (basado en AuditLog)
- SoAItem evidence validadas
- Risk residual calculados post-implementaciÃ³n

---

### **FASE 5: READINESS (F5)**
**DuraciÃ³n tÃ­pica**: 1-2 semanas  
**PropÃ³sito**: ValidaciÃ³n final antes de auditorÃ­a de certificaciÃ³n externa

**Actividades**:
- F5.1 Simulacro y Cierres: GAP final, readiness review, cierre de acciones pendientes

**Entregables**:
- Informe Readiness (go-live para auditor externo SI/NO)
- SoA final (93 items IMPLEMENTED)
- PTR final (riesgos residuales documentados)
- Cierre de todas acciones correctivas
- Evidencias completas

**VIT genera/usa**:
- Report Readiness (todas evidencias cargadas?, todos controles IMPLEMENTED?, riesgos residuales aceptados?)
- Export SoA + PTR + AuditLog (para auditor externo)
- Risk analysis final (residuales vs aceptaciÃ³n)

---

## D) MÃ“DULOS/FUNCIONALIDADES PRINCIPALES

### **MÃ³dulo 1: USERS & AUTENTICACIÃ“N**
**DescripciÃ³n**: GestiÃ³n de usuarios y control de acceso (JWT + RBAC)

**QuÃ© datos maneja**:
- User (username, email, password hash, role: ADMIN/CONSULTANT/CLIENT)
- ProjectUser (user â†” project mapping con rol especÃ­fico)
- AuditLog (eventos de login, cambios)

**QuiÃ©n accede**:
- Admin: CRUD de usuarios, ver todos
- Consultant: ver usuarios de sus proyectos
- Client: ver su perfil

**QuÃ© hace**:
- AutenticaciÃ³n JWT (access + refresh tokens)
- AutorizaciÃ³n basada en rol + ProjectUser
- Cambio de contraseÃ±a, reset vÃ­a email (future)
- GestiÃ³n de sesiones (timeout, logout)

**Endpoints principales**:
- POST /api/token/ (login â†’ tokens)
- POST /api/token/refresh/ (renovar)
- GET/POST /api/users/ (CRUD)
- GET/POST /api/project-users/ (asignar usuario-proyecto)

---

### **MÃ³dulo 2: COMPANIES & PROJECTS**
**DescripciÃ³n**: GestiÃ³n de empresas cliente y sus proyectos ISO

**QuÃ© datos maneja**:
- Company (name, tax_id/RFC, email, phone, address, contact_person)
- Project (company, name, status, dates, created_by)
- Phase (project, code: INIT/PLAN/IMPLEMENT/MAINTAIN/CERTIFY, status, %)
- Task (phase, title, status, priority, assigned_to, due_date)

**QuiÃ©n accede**:
- Admin: ver todos
- Consultant: crear/editar proyectos asignados
- Client: ver proyecto su empresa

**QuÃ© hace**:
- Crear/editar/eliminar empresas
- Crear/editar proyectos
- Auto-generar 5 fases por proyecto
- CRUD tareas
- Cambiar estados
- Ver progreso (%)

**Endpoints principales**:
- GET/POST /api/companies/
- GET/POST /api/projects/
- GET/POST /api/phases/
- GET/POST /api/tasks/

---

### **MÃ³dulo 3: SCOPE & ASSETS**
**DescripciÃ³n**: DefiniciÃ³n de alcance SGSI e inventario de activos

**QuÃ© datos maneja**:
- Scope (project, included_systems[], excluded_systems[], justification, approved_by, status)
- Asset (project, name, type: HARDWARE/SOFTWARE/DATA/PERSONNEL/FACILITY, owner, location, criticality, CIA_levels)

**QuiÃ©n accede**:
- Consultant: define scope + crea activos
- Admin: revisa
- Client: ve activos de su proyecto

**QuÃ© hace**:
- Definir quÃ© entra/sale del alcance SGSI
- Crear inventario de activos
- Clasificar por criticidad (LOW/MEDIUM/HIGH/CRITICAL)
- Asignar niveles CIA (1-5 cada uno)
- Reportar activos crÃ­ticos

**Endpoints principales**:
- POST /api/scopes/
- GET/POST /api/projects/{id}/assets/

---

### **MÃ³dulo 4: RISK (Riesgos)**
**DescripciÃ³n**: EvaluaciÃ³n completa de riesgos (inherente/residual)

**QuÃ© datos maneja**:
- Risk (project, name, description, causa, consequence, category, owner)
  - Inherent: likelihood 1-5, impact 1-5, score (auto)
  - Residual: likelihood 1-5, impact 1-5, score (auto)
  - Treatment: ACCEPT/MITIGATE/TRANSFER/AVOID
  - Status: IDENTIFIED/ASSESSED/MITIGATED/MONITORED
- Risk â†” Asset (N:M)
- Risk â†” ISOControl (N:M, vÃ­a SoAItem)

**QuiÃ©n accede**:
- Consultant: crea/evalÃºa riesgos
- Admin: revisa, aprueba
- Client: ve dashboard

**QuÃ© hace**:
- Crear riesgos con descripciÃ³n completa
- Evaluar inherente (Prob Ã— Impact = Score)
- Seleccionar controles mitigantes
- Auto-calcular residual post-controles
- Calcular efectividad (inherente - residual)
- Cambiar estado riesgo
- Matriz 5Ã—5 (color-coded)
- KPI: promedio scores, % reducciÃ³n, riesgos aceptados

**Endpoints principales**:
- GET/POST /api/projects/{id}/risks/
- GET/PUT /api/risks/{id}/ (incluyendo cambio de status/tratamiento)

---

### **MÃ³dulo 5: ISO CONTROLS & SOA**
**DescripciÃ³n**: Mapeo de 93 controles ISO 27001 y Statement of Applicability

**QuÃ© datos maneja**:
- ISOControl (code: A.5.1 â†’ A.9.7, name, description, category, iso_27001_text, requirements) Ã— 93
- SoAItem (project, iso_control, is_applicable, justification, impl_status, impl_date, responsible)

**QuiÃ©n acceso**:
- Consultant: completa SoA (justificaciones, estado)
- Admin: revisa
- Client: ve SoA, puede marcar como implementado + cargar evidencias

**QuÃ© hace**:
- CatÃ¡logo 93 controles (precargado, read-only)
- Auto-generar SoAItem (93 items por proyecto)
- Marcar control aplicable/no aplicable
- Justificar por quÃ© no aplica
- Cambiar estado implementaciÃ³n (NOT_IMPL â†’ IN_PROGRESS â†’ IMPLEMENTED)
- Asignar responsable
- Exportar SoA (PDF con 93 items)
- BÃºsqueda/filtro por cÃ³digo, dominio, estado

**Endpoints principales**:
- GET /api/iso-controls/ (93 controles, sin POST)
- GET/PUT /api/projects/{id}/soa/
- GET/PUT /api/soa-items/{id}/

---

### **MÃ³dulo 6: EVIDENCE (Evidencias)**
**DescripciÃ³n**: Carga, versioning y validaciÃ³n de documentos de evidencia

**QuÃ© datos maneja**:
- Evidence (soaitem, file_path, version, status: PENDING/APPROVED/REJECTED, uploaded_by, uploaded_at, comments)
- Evidence self-referencia (v1 â†’ v2 â†’ v3)

**QuiÃ©n accede**:
- Client: carga evidencias
- Consultant/Admin: revisa, aprueba/rechaza, comenta

**QuÃ© hace**:
- Validar tipo archivo (PDF, DOCX, XLSX, JPG, PNG)
- Validar tamaÃ±o (mÃ¡x 50MB)
- Almacenar en S3 (persistente en producciÃ³n)
- Versioning: nueva versiÃ³n reemplaza anterior
- Cambiar estado: PENDING â†’ APPROVED o REJECTED
- Comentarios de revisiÃ³n
- Descargar
- Auditar cambios (quiÃ©n, cuÃ¡ndo)

**Endpoints principales**:
- GET/POST /api/projects/{id}/evidence/
- PUT /api/evidence/{id}/ (cambiar estado)
- GET /api/evidence/{id}/download/

---

### **MÃ³dulo 7: REPORTS & DOCUMENTS**
**DescripciÃ³n**: GeneraciÃ³n de reportes e informes de cumplimiento

**QuÃ© datos maneja**:
- Report (project, type, generated_at, generated_by, content, status)
- Document (project, name, type: TEMPLATE/GENERATED/UPLOADED, file)

**QuiÃ©n accede**:
- Consultant: genera reportes
- Admin: distribuye
- Client: descarga

**QuÃ© hace**:
- Generar SoA en PDF (93 items, estado, evidencias)
- Generar Matriz Riesgos (grÃ¡fica 5Ã—5 + tabla)
- Generar Reporte Cumplimiento (% by control, by phase)
- Generar Reporte Ejecutivo (KPIs, riesgos crÃ­ticos)
- Generar Acta RevisiÃ³n DirecciÃ³n
- Exportar a PDF/Excel
- Programar envÃ­o por email (future)
- Historial de versiones

**Endpoints principales**:
- POST /api/projects/{id}/reports/generate/
- GET /api/projects/{id}/reports/
- GET /api/reports/{id}/download/

---

### **MÃ³dulo 8: AUDIT LOG & TRAZABILIDAD**
**DescripciÃ³n**: Registro inmutable de eventos (QUIEN/QUE/CUANDO/DONDE)

**QuÃ© datos maneja**:
- AuditLog (timestamp_utc, actor, actor_snapshot, action: CREATE/UPDATE/DELETE/APPROVE/REJECT/VIEW, entity_type, object_id, changes: JSON, outcome: SUCCESS/FAIL, ip_address, user_agent, request_id)

**QuiÃ©n accede**:
- Admin: lista todos
- Consultant: ve logs de su proyecto

**QuÃ© hace**:
- Auto-registra cambios vÃ­a signals (post_save, post_delete)
- Inmutable (append-only, sin UPDATE/DELETE)
- Filtra por usuario, acciÃ³n, entidad, fecha
- Exportar para auditor externo
- Genera reportes de actividad
- DetecciÃ³n de anomalÃ­as (future)

**Endpoints principales**:
- GET /api/audit-logs/?user=1&action=CREATE&entity=Risk&date_from=...
- GET /api/audit-logs/export/ (CSV/JSON)

---

### **MÃ³dulo 9: DASHBOARD & METRICS**
**DescripciÃ³n**: VisualizaciÃ³n de avance y KPIs SGSI

**QuÃ© datos maneja**:
- Datos agregados de Project, Phase, Task, Risk, SoAItem, Evidence
- KPIs: % project, % risks mitigated, % controls implemented
- KRIs: residual risks, control gaps, pendientes evidencias

**QuiÃ©n accede**:
- Admin: ve empresa/proyecto
- Consultant: ve proyecto
- Client: ve su proyecto

**QuÃ© hace**:
- Dashboard por rol (diferentes mÃ©tricas)
- GrÃ¡ficas: matriz riesgos, cronograma, SoA progreso
- Tablas: prÃ³ximas tareas, riesgos crÃ­ticos, cambios recientes
- KPIs: avance por semana, velocidad implementaciÃ³n

**Endpoints principales**:
- GET /api/projects/{id}/dashboard/ (retorna mÃ©tricas)

---

## E) ENTIDADES/DATOS CLAVE

### **Entidades Principales y Relaciones**

| Entidad | Campos clave | RelaciÃ³n | Cardinalidad | PropÃ³sito |
|---------|------------|----------|--------------|-----------|
| User | id, username, email, role, phone | - | - | AutenticaciÃ³n |
| Company | id, name, tax_id, email, contact | User | 1:N | Empresa cliente |
| Project | id, company, name, status, dates | Company | 1:N | Proyecto ISO |
| Phase | id, project, code, name, sequence | Project | 1:N | Fase metodolÃ³gica |
| Task | id, phase, title, status, priority | Phase | 1:N | Tarea por fase |
| Scope | id, project, included, excluded | Project | 1:1 | Alcance SGSI |
| Asset | id, project, name, type, criticality, CIA | Project | 1:N | Inventario |
| Risk | id, project, risk data, inherent/residual scores | Project | 1:N | Riesgo evaluado |
| Asset_Risk | asset_id, risk_id | N:M | N:M | RelaciÃ³n |
| ISOControl | id, code, name, description (Ã—93) | - | - | CatÃ¡logo read-only |
| SoAItem | id, project, control, status, justification | Project + ISOControl | N:M | Aplicabilidad control |
| Evidence | id, soaitem, file, status, version | SoAItem | 1:N | Documento evidencia |
| Document | id, project, type, file | Project | 1:N | Reporte generado |
| AuditLog | id, user, action, entity, changes, timestamp | User | 1:N | Evento registrado |
| ProjectUser | id, user, project, role | User + Project | M:M | Usuario-proyecto |

### **Controles ISO (Anexo A: 93 Controles)**

**Estructura de ISOControl**:
- **CÃ³digo**: A.5.1 a A.9.7 (nuevo esquema ISO 27001:2022)
- **CategorÃ­as** (4 temas principales):
  - **A.5-A.7**: Organizational, People, Physical Controls (~35 controles)
  - **A.8**: Technological Controls (~46 controles)
    - A.8.1-A.8.10: Cryptography y Endpoint Security
    - A.8.11-A.8.13: Logging y Monitoring
    - A.8.14-A.8.26: Acceso, Comunicaciones, Desarrollo
  - **A.9**: System Integration (~12 controles)

**Uso en VIT**:
- **Precargados**: 93 registros en BD inicial (fixture JSON o CSV)
- **Solo lectura**: Admin NO puede crear/editar/eliminar controles
- **Mapeo con Risk**: Cada Risk puede vincular N controles mitigantes
- **SoA**: 93 items automÃ¡ticos por proyecto (uno por control)

---

### **Roles y Niveles de Acceso**

#### **Administrador VIT (ADMIN)** - Rol 1
**Permisos**:
- âœ… Ver todas empresas, todos proyectos
- âœ… CRUD usuarios (crear, editar, desactivar)
- âœ… CRUD empresas y proyectos
- âœ… Ver AuditLog de toda plataforma
- âœ… Generar reportes globales
- âœ… Cambiar estado proyecto/fase/riesgo/SoA
- âœ… Aprobar/Rechazar evidencias
- âœ… Cambiar roles de usuarios

**Ejemplos acciones**:
- Crear usuario "Carlos" con role CONSULTANT
- Ver auditorÃ­a de cambios en proyecto de Bancolombia
- Generar reporte global de auditorÃ­a para cumplimiento legal

---

#### **Consultor ISO (CONSULTANT)** - Rol 2
**Permisos**:
- âœ… Crear proyectos (queda como creator)
- âœ… Editar proyectos asignados (vÃ­a ProjectUser)
- âœ… Ver empresas asignadas
- âœ… CRUD Scope, Asset, Risk (propios proyectos)
- âœ… Llenar SoA (marcar aplicables/no aplicables)
- âœ… Evaluar riesgos inherente/residual
- âœ… Aprobar/Rechazar evidencias
- âœ… Generar reportes por proyecto
- âœ… Ver AuditLog de proyecto
- âŒ Ver otros proyectos
- âŒ Cambiar usuarios (es Admin)

**Ejemplos acciones**:
- Crear proyecto "ISO Bancolombia"
- Evaluar 150 riesgos y seleccionar controles
- Revisar evidencias que carga Cliente
- Generar SoA final

---

#### **Cliente/Empresa (CLIENT)** - Rol 3
**Permisos**:
- âœ… Ver proyectos de su empresa (vÃ­a ProjectUser)
- âœ… Ver Scope, Activos, Riesgos (lectura)
- âœ… Cargar evidencias
- âœ… Ver estado SoA
- âœ… Ver reportes
- âœ… Cambiar estado tarea (en su proyecto)
- âŒ Crear proyecto
- âŒ Evaluar riesgos
- âŒ Cambiar decisiones de control
- âŒ Ver otras empresas

**Ejemplos acciones**:
- Ver progreso del proyecto (fases, tareas)
- Subir evidencia "Backup-2026-02-20.zip" para control A.5.18
- Revisar SoA y confirmar quÃ© controles ya estÃ¡ implementando

---

### **Estados y Ciclos de Vida**

#### **Project Status**
```
PLANNING -> IN_PROGRESS -> COMPLETED -> (ON_HOLD)
   â†“             â†“           â†“
 Fase 0     Fases 1-4      Fase 5
```

#### **Phase Status**
```
NOT_STARTED -> IN_PROGRESS -> COMPLETED
   â†“             â†“             â†“
  0%           10-99%        100%
```

#### **Task Status**
```
NOT_STARTED -> IN_PROGRESS -> COMPLETED -> (BLOCKED)
```

#### **Risk Status**
```
IDENTIFIED -> ASSESSED -> MITIGATED -> MONITORED
   â†“         â†“          â†“           â†“
sin eval   eval Ok    controles   follow-up
           completos  in place
```

#### **SoAItem Status (implementation_status)**
```
NOT_IMPLEMENTED -> IN_PROGRESS -> IMPLEMENTED
     â†“              â†“              â†“
   Nueva         parte          completo
              implementando     + evidencias
```

#### **Evidence Status**
```
PENDING -> APPROVED  âœ“
        \
         -> REJECTED  âœ—
           (cargar nueva versiÃ³n)
```

---

## F) PROCESOS Y WORKFLOWS

### **Workflow 1: Ciclo Completo Proyecto ISO 27001**

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  INICIO (F0)                                                    â”‚
â”‚  - Admin crea Empresa                                           â”‚
â”‚  - Consultant (Carlos) asignado como responsable               â”‚
â”‚  - Proyecto creado â†’ Auto-genera 5 fases + 93 SoA items       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                            â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  CONTEXTO Y ALCANCE (F1) - semanas 1-4                         â”‚
â”‚  - Carlos define Scope (sistemas in/out of scope)              â”‚
â”‚  - Sistema guarda Scope                                         â”‚
â”‚  - AuditLog registra: "Carlos CREATED Scope#5"                â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                            â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  RIESGOS Y CONTROLES (F2) - semanas 5-12                       â”‚
â”‚  1. Carlos crea Asset "BD Clientes" (type=DATA)               â”‚
â”‚  2. Carlos crea Risk "Acceso no auth" (Prob=5, Imp=5)         â”‚
â”‚  3. Risk inherent_score = 5Ã—5 = 25 (auto-calc)               â”‚
â”‚  4. Carlos selecciona 3 controles (A.5.15, A.8.24, A.6.3)    â”‚
â”‚  5. Carlos cambia Prob residual a 2 (con controles)          â”‚
â”‚  6. Risk residual_score = 2Ã—5 = 10 (auto-calc)               â”‚
â”‚  7. Efectividad = 25 - 10 = 15 (auto-calc)                   â”‚
â”‚  8. SoA items para esos 3 controles cambian a IN_PROGRESS     â”‚
â”‚  - AuditLog registra cada cambio                              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                            â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  IMPLEMENTACIÃ“N Y OPERACIÃ“N (F3) - semanas 13-24               â”‚
â”‚  1. Client (MarÃ­a) ve SoA: 93 controles, 3 en IN_PROGRESS     â”‚
â”‚  2. MarÃ­a carga Evidence "auth_config.pdf" â†’ SoA A.5.15       â”‚
â”‚  3. Estado Evidence: PENDING (waiting Consultant review)       â”‚
â”‚  4. Carlos revisa Evidence: aprueba âœ“                          â”‚
â”‚  5. SoA item A.5.15 â†’ estado IMPLEMENTED                       â”‚
â”‚  6. Repite para 92 controles mÃ¡s...                           â”‚
â”‚  7. Dashboard muestra: 45% controles implementados             â”‚
â”‚  - AuditLog registra cada upload, aprobaciÃ³n, cambio          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                            â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  EVALUACIÃ“N Y MEJORA (F4) - semanas 25-28                      â”‚
â”‚  1. Carlos genera Report AuditorÃ­a Interna                     â”‚
â”‚  2. Report muestra: 90 de 93 controles IMPLEMENTED             â”‚
â”‚  3. 3 gaps restantes: habilitar MFA, formalizar roles, etc    â”‚
â”‚  4. MarÃ­a y equipo cierran los 3 gaps                          â”‚
â”‚  5. RevisiÃ³n DirecciÃ³n aprueba cumplimiento                    â”‚
â”‚  - Dashboard final: 100% controles, riesgos residuales doc    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                            â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  READINESS (F5) - semana 29                                    â”‚
â”‚  1. Carlos genera Report Readiness                             â”‚
â”‚  2. Report: "LISTO para auditor externo"                       â”‚
â”‚  3. Exporta: SoA final + PTR + AuditLog (para auditor)        â”‚
â”‚  4. Auditor externo certifica â†’ ISO 27001 awarded              â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

---

### **Workflow 2: CreaciÃ³n y ValidaciÃ³n de Riesgo (Detallado)**

```
Paso 1: IDENTIFICACIÃ“N
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Consultant Carlos crea Risk           â”‚
â”‚ - name: "SQL Injection en app"        â”‚
â”‚ - description: "AplicaciÃ³n vulnerable"â”‚
â”‚ - cause: "ValidaciÃ³n insuficiente"    â”‚
â”‚ - consequence: "Acceso no autorizado" â”‚
â”‚ - category: TECHNICAL                 â”‚
â”‚ - owner: Usuario#5 (DBA)              â”‚
â”‚ - status: IDENTIFIED                  â”‚
â”‚ Risk#123 creado                       â”‚
â”‚ AuditLog: "Carlos CREATE Risk#123"    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â†“
Paso 2: EVALUACIÃ“N INHERENTE
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Carlos evalÃºa sin controles           â”‚
â”‚ - inherent_likelihood: 5 (muy probable)
â”‚ - inherent_impact: 5 (catastrÃ³fico)   â”‚
â”‚ - inherent_score: 5Ã—5 = 25 â† AUTOMÃTICO
â”‚ Risk#123 update (IDENTIFIEDâ†’ASSESSED) â”‚
â”‚ AuditLog: "Carlos UPDATE Risk#123"    â”‚
â”‚         changes: {likelihood:5, ...}  â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â†“
Paso 3: SELECCIONAR CONTROLES
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Carlos vincula N controles            â”‚
â”‚ - A.5.15 (Control de acceso)         â”‚
â”‚ - A.8.24 (CriptografÃ­a)              â”‚
â”‚ - A.6.3 (CapacitaciÃ³n)               â”‚
â”‚ Risk#123.controls = [A.5.15, A.8.24] â”‚
â”‚ SoAItem para esos 3 â†’ status = ..ING  â”‚
â”‚ AuditLog: "Carlos LINK Riskâ†’SoA"      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â†“
Paso 4: EVALUACIÃ“N RESIDUAL
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Carlos evalÃºa con controles           â”‚
â”‚ - residual_likelihood: 2 (baja)       â”‚
â”‚ - residual_impact: 5 (aÃºn alto)       â”‚
â”‚ - residual_score: 2Ã—5 = 10 â† AUTOMÃTICO
â”‚ - risk_reduction: 25 - 10 = 15        â”‚
â”‚ - treatment: MITIGATE                 â”‚
â”‚ Risk#123 update                       â”‚
â”‚ AuditLog: "Carlos UPDATE Risk#123"    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â†“
Paso 5: EVIDENCIA CARGA
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Client MarÃ­a ve SoA item A.5.15       â”‚
â”‚ - status: IN_PROGRESS                 â”‚
â”‚ MarÃ­a carga Evidence:                 â”‚
â”‚ - file: "waf_config.pdf"              â”‚
â”‚ - status: PENDING                     â”‚
â”‚ Evidence#456 creado                   â”‚
â”‚ AuditLog: "MarÃ­a CREATE Evidence#456" â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â†“
Paso 6: REVISIÃ“N Y APROBACIÃ“N
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Consultant Carlos revisa Evidence     â”‚
â”‚ - Lee file: OK âœ“                      â”‚
â”‚ - Marca: APPROVED                     â”‚
â”‚ Evidence#456 update                   â”‚
â”‚ SoAItem.status â†’ IMPLEMENTED          â”‚
â”‚ Risk#123.status â†’ MITIGATED           â”‚
â”‚ AuditLog: "Carlos APPROVE Evidence"   â”‚
â”‚         "Carlos UPDATE SoAItem"       â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
               â†“
RESULTADO
- Risk#123: inherent=25, residual=10, reduction=15 (KPI)
- 3 SoAItems: IMPLEMENTED con evidencias aprobadas
- AuditLog: 6 eventos registrados (trazabilidad completa)
```

---

### **Workflow 3: Matriz de Riesgos (5Ã—5)**

```
                    IMPACTO
                1    2    3    4    5
                â”œâ”€â”€â”€â”€â”¼â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”¤
             1  â”‚ 1âœ“ â”‚ 2âœ“ â”‚ 3âœ“ â”‚ 4âœ“ â”‚ 5âœ“â•‘
             2  â”‚ 2âœ“ â”‚ 4âœ“ â”‚ 6âœ“ â”‚ 8âš  â”‚10âš â•‘
             3  â”‚ 3âœ“ â”‚ 6âœ“ â”‚ 9âš  â”‚12âš  â”‚15âŒâ•‘
             4  â”‚ 4âœ“ â”‚ 8âš  â”‚12âš  â”‚16âŒ â”‚20âŒâ•‘
             5  â”‚ 5âœ“ â”‚10âš  â”‚15âŒ â”‚20âŒ â”‚25âŒâ•‘
             
Leyenda:
âœ“ = Aceptable (ACCEPT)
âš  = Mitigar recomendado (MITIGATE)
âŒ = CrÃ­tico (MUST MITIGATE)

Ejemplo: Risk "SQL Injection"
- ANTES (inherent): Prob=5, Impact=5 â†’ Score=25 (âŒ crÃ­tico)
- DESPUÃ‰S (residual): Prob=2, Impact=5 â†’ Score=10 (âš  mitigable)
- Efectividad: 25-10 = 15 (50% reducciÃ³n)
```

---

### **Workflow 4: Statement of Applicability (SoA)**

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Crear Proyecto "ISO Bancolombia"             â”‚
â”‚ â†’ Auto-genera 93 SoAItems (1 Ã— control)      â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                    â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Consultant Carlos revisa cada control        â”‚
â”‚ A.5.1 "PolÃ­ticas de seguridad"              â”‚
â”‚  â”œâ”€ is_applicable: YES (mandatorio)         â”‚
â”‚  â”œâ”€ justification: "" (no aplica porque...)  â”‚
â”‚  â”œâ”€ impl_status: NOT_IMPLEMENTED             â”‚
â”‚  â””â”€ responsible: Usuario#10 (CISO)          â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                    â†“
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚ Para control A.5.15 se repite 3 veces...    â”‚
â”‚ A.5.15 "Control de acceso"                  â”‚
â”‚  â”œâ”€ is_applicable: NO                        â”‚
â”‚  â”œâ”€ justification: "Acceso biomÃ©trico, no   â”‚
â”‚  â”‚  por usuario/contraseÃ±a"                 â”‚
â”‚  â”œâ”€ impl_status: N/A                        â”‚
â”‚  â””â”€ responsible: null                       â”‚
â”‚                                             â”‚
â”‚ A.5.15 (Risk "SQL Injection") = LINKED      â”‚
â”‚  â”œâ”€ is_applicable: YES                      â”‚
â”‚  â”œâ”€ justification: "Mitigar inyecciÃ³n SQL"  â”‚
â”‚  â”œâ”€ impl_status: IN_PROGRESS (MarÃ­a cargÃ³) â”‚
â”‚  â”œâ”€ evidence: "waf_config.pdf"              â”‚
â”‚  â””â”€ responsible: Usuario#5 (DBA)            â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                    â†“
RESULTADO: 93 SoA items
- 85 controles: Aplicable + en proceso/implementado
- 8 controles: No aplicable (con justificaciÃ³n)
- 100% de aplicables con evidencias pronto
```

---

### **Workflow 5: AuditorÃ­a y Cambios (AuditLog)**

```
AcciÃ³n 1: Consultant "Carlos" crea Risk
â†’ AuditLog entry:
  {
    timestamp: 2026-02-20 14:30:45 UTC
    actor: User#12 (Carlos)
    actor_snapshot: "carlos@consultec.com"
    action: "CREATE"
    entity: "Risk"
    object_id: "123"
    changes: {
      name: "SQL Injection",
      inherent_likelihood: 5,
      inherent_impact: 5,
      category: "TECHNICAL"
    }
    outcome: "SUCCESS"
    ip_address: "181.55.20.45"
    user_agent: "Mozilla/... Chrome/90"
  }

AcciÃ³n 2: Consultant "Carlos" evalÃºa residual
â†’ AuditLog entry:
  {
    timestamp: 2026-02-20 15:05:30 UTC
    actor: User#12 (Carlos)
    action: "UPDATE"
    entity: "Risk"
    object_id: "123"
    changes: {
      residual_likelihood: { before: null, after: 2 },
      residual_impact: { before: null, after: 5 },
      treatment: { before: null, after: "MITIGATE" }
    }
    outcome: "SUCCESS"
  }

AcciÃ³n 3: Client "MarÃ­a" sube evidencia
â†’ AuditLog entry:
  {
    timestamp: 2026-02-20 16:10:00 UTC
    actor: User#8 (MarÃ­a)
    action: "CREATE"
    entity: "Evidence"
    object_id: "456"
    changes: {
      file: "waf_config.pdf",
      soaitem_id: 15,
      status: "PENDING"
    }
    outcome: "SUCCESS"
  }

AcciÃ³n 4: Consultant "Carlos" aprueba
â†’ AuditLog entry:
  {
    timestamp: 2026-02-20 16:15:00 UTC
    actor: User#12 (Carlos)
    action: "APPROVE"
    entity: "Evidence"
    object_id: "456"
    changes: {
      status: { before: "PENDING", after: "APPROVED" }
    }
    outcome: "SUCCESS"
  }

REPORTE AUDITORÃA (7 dÃ­as):
- Total eventos: 1247
- Por acciÃ³n: CREATE=520, UPDATE=587, APPROVE=140
- Por usuario: Carlos=450, MarÃ­a=320, Admin=477
- Por entidad: Risk=340, Evidence=450, SoAItem=280, ...
- AnomalÃ­as: 2 UPDATE out-of-hours (02:30), 1 FAIL (403)
```

---

## G) REQUERIMIENTOS DE SEGURIDAD Y AUDITORÃA

### **Datos Sensibles (que VIT gestiona)**

1. **PII (Personally Identifiable Information)**
   - Email, telÃ©fono, nombres usuarios
   - Datos contacto empresas
   - Responsables de controles

2. **Credenciales**
   - Hashes contraseÃ±a (bcrypt)
   - JWT tokens (acceso/refresh)

3. **InformaciÃ³n de Riesgos**
   - Causas/consecuencias de riesgos (confidencial)
   - Evaluaciones de vulnerabilidades

4. **Evidencias Clasificadas**
   - Logs de sistemas (pueden contener PII)
   - Configuraciones sensibles
   - Certificados, keys (si se anexan)

5. **Datos Operacionales**
   - CMDB sistema (inventario)
   - Relaciones activos-riesgos-controles
   - MÃ©tricas de cumplimiento

### **AuditorÃ­a Requerida**

**Nivel 1: Eventos crÃ­ticos (siempre registrar)**
- Login/Logout (SUCCESS/FAIL)
- Cambios en User (crear, editar, cambio de rol)
- Cambios en Risk (crear, editar scores, estado)
- Cambios en SoAItem (aplicabilidad, estado, justificaciÃ³n)
- Cambios en Evidence (subir, aprobar, rechazar)
- Cambios en Project (estado, cierre)

**Nivel 2: Cambios sensibles (trace completa)**
- UPDATE de riesgo inherente/residual (quiÃ©n, cuÃ¡ndo, deâ†’a)
- UPDATE de tratamiento riesgo
- APPROVE/REJECT evidence (quiÃ©n, fecha, comentarios)
- DELETE (FORBIDDEN en AuditLog, solo INSERT)

**Nivel 3: Accesos (si disponible)**
- VIEW evidence (opcional, segÃºn data classification)
- EXPORT SoA (quiÃ©n, cuÃ¡ndo)
- DOWNLOAD reports

### **Permisos y Niveles de Acceso**

#### **Por Rol (Role-Based Access Control)**

```
                ADMIN  CONSULTANT  CLIENT
â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
User CRUD        âœ“         âœ—         âœ—
Company CRUD     âœ“         âœ—         âœ—
Project CREATE   âœ“         âœ“         âœ—
Project EDIT     âœ“      âœ“(own)       âœ—
Project READ     âœ“      âœ“(own)    âœ“(own)
Scope CRUD       âœ“         âœ“         âœ—
Asset CRUD       âœ“         âœ“         âœ“(view)
Risk CRUD        âœ“         âœ“      âœ“(view)
SoA EDIT         âœ“         âœ“      âœ“(impl)
Evidence UPLOAD  âœ“         âœ“         âœ“
Evidence APPROVE âœ“         âœ“         âœ—
Report GENERATE  âœ“         âœ“      âœ“(view)
AuditLog VIEW    âœ“      âœ“(own)       âœ—
```

#### **Por ProjectUser (user-project specific)**

```
User "Carlos" en Proyecto "A" = CONSULTANT
  â†’ Puede editar proyecto A, NO verlo en proyecto B

User "MarÃ­a" en Proyecto "A" = CLIENT
  â†’ Puede subir evidencias A, NO borrar

GarantÃ­a: SELECT projects WHERE user IN (ProjectUser)
```

### **Cumplimientos Legales y Normativos**

1. **ISO 27001:2022**
   - **A.8.15** (Logging): VIT registra eventos crÃ­ticos en AuditLog
   - **A.8.16** (Monitoring): Reportes de auditorÃ­a detectan anomalÃ­as
   - **A.8.17** (Clock sync): Usar UTC para timestamps
   - **A.8.24** (CriptografÃ­a): JWT en HTTPS, passwords en bcrypt

2. **GDPR (si datos EU)**
   - **Art. 5** (Principios): Lawfulness, fairness, transparency
   - **Art. 32** (Security): Encryption, access control âœ“
   - **Art. 33/34** (Notification): Breach notification (manual en VIT)
   - **Art. 35/36** (DPIA): Data Protection Impact Assessment

3. **Ley 1581/2012 (Colombia)**
   - **Responsabilidad**: VIT es "Responsable" de datos personales
   - **Consentimiento**: Usuarios consienten al login
   - **Seguridad**: ContraseÃ±as + HTTPS + logs
   - **Derechos**: Acceso, correcciÃ³n, eliminaciÃ³n (future)

4. **Ley 1266/2008 (Habeas Data - Colombia)**
   - Para datos crediticios: registro de accesos (AuditLog)
   - AuditorÃ­a de usuario acceso a datos sensibles

### **ImplementaciÃ³n de Seguridad en VIT**

**Backend (Django)**:
- âœ… AUTH_USER_MODEL = 'users.User'
- âœ… ContraseÃ±as: bcrypt (set_password())
- âœ… JWT SimpleJWT con Refresh tokens
- âœ… Permisos por rol (@permission_required o custom permission classes)
- âœ… CORS bloqueado (solo frontend autorizado)
- âœ… HTTPS en producciÃ³n (Render incluida SSL)
- âœ… AuditLog signals (auto-registra cambios)
- âœ… Validaciones de entrada (Django ORM)
- âœ… Sanitization de output (JSON)
- âœ… Rate limiting (future: throttling en DRF)

**Frontend (React)**:
- âœ… Token en localStorage (o sessionStorage)
- âœ… Interceptor axios: agrega Authorization header
- âœ… RedirecciÃ³n 401 â†’ Login
- âœ… Session timeout (renovar refresh token)
- âœ… HTTPS en producciÃ³n (Vercel incluida)

**Base de Datos**:
- âœ… PostgreSQL con backup automÃ¡tico
- âœ… Constrains PK/FK/UNIQUE/CHECK
- âœ… Ãndices para queries eficientes
- âœ… Sem acceso directo: solo via Django ORM

**Almacenamiento Archivos**:
- âœ… S3 compatible (Supabase Storage o AWS)
- âœ… ValidaciÃ³n tipo/tamaÃ±o antes de subir
- âœ… Antivirus scan (future: VirusTotal API)
- âœ… Acceso controlado (solo usuarios autorizados)

---

## H) CHECKLIST Y VALIDACIONES

### **Validaciones AutomÃ¡ticas (Backend en VIT)**

1. **Usuario**
   - âœ“ Username Ãºnico + no espacios
   - âœ“ Email vÃ¡lido + Ãºnico
   - âœ“ ContraseÃ±a mÃ­n 8 caracteres + fuerte (mayÃºs, minÃºs, nÃºmero, sÃ­mbolo)
   - âœ“ Role en {ADMIN, CONSULTANT, CLIENT}
   - âœ“ Email no permite cambio fÃ¡cil (require confirmation)

2. **Company**
   - âœ“ Nombre Ãºnico + RFC Ãºnico
   - âœ“ Email corporativo (validar dominio MX)
   - âœ“ TelÃ©fono formato vÃ¡lido
   - âœ“ DirecciÃ³n completa (calle, ciudad, cÃ³digo postal)

3. **Project**
   - âœ“ end_date >= start_date
   - âœ“ Nombre Ãºnico por empresa
   - âœ“ Status en {PLANNING, IN_PROGRESS, COMPLETED, ON_HOLD}
   - âœ“ Created_by debe estar asignado (ProjectUser)

4. **Phase**
   - âœ“ Sequence Ãºnico en proyecto (1,2,3,... no repeats)
   - âœ“ Code en {INIT, PLAN, IMPLEMENT, MAINTAIN, CERTIFY}
   - âœ“ percentage_complete entre 0-100
   - âœ“ end_date >= start_date (si ambas presentes)

5. **Task**
   - âœ“ Priority en {LOW, MEDIUM, HIGH, CRITICAL}
   - âœ“ Status en {NOT_STARTED, IN_PROGRESS, COMPLETED, BLOCKED}
   - âœ“ Due_date no puede ser menor a fase start_date (validaciÃ³n de negocio)

6. **Asset**
   - âœ“ Type en {HARDWARE, SOFTWARE, DATA, PERSONNEL, FACILITY}
   - âœ“ Criticality en {LOW, MEDIUM, HIGH, CRITICAL}
   - âœ“ CIA levels entre 1-5 cada uno
   - âœ“ Name Ãºnico por proyecto

7. **Risk** â† CRÃTICO
   - âœ“ inherent_likelihood entre 1-5
   - âœ“ inherent_impact entre 1-5
   - âœ“ inherent_score = likelihood Ã— impact (auto)
   - âœ“ residual_likelihood <= inherent_likelihood
   - âœ“ residual_impact <= inherent_impact
   - âœ“ residual_score = likelihood Ã— impact (auto)
   - âœ“ Todas likelihood/impact no null
   - âœ“ Treatment en {ACCEPT, MITIGATE, TRANSFER, AVOID}
   - âœ“ Status en {IDENTIFIED, ASSESSED, MITIGATED, MONITORED}
   - âœ“ Si Treatment=ACCEPT â†’ residual score <= THRESHOLD

8. **SoAItem** â† CRÃTICO
   - âœ“ Exactamente 1 SoAItem por project Ã— isocontrol (UNIQUE TOGETHER)
   - âœ“ is_applicable es boolean
   - âœ“ Si is_applicable=FALSE â†’ justification NOT NULL
   - âœ“ impl_status en {NOT_IMPLEMENTED, IN_PROGRESS, IMPLEMENTED}
   - âœ“ impl_date solo permitida si impl_status=IMPLEMENTED
   - âœ“ Si impl_status=IMPLEMENTED â†’ must have approved Evidence

9. **Evidence**
   - âœ“ Archivo max 50MB
   - âœ“ Tipo en {PDF, DOCX, XLSX, JPG, PNG}
   - âœ“ MIME type validado (servidor, NO confiar en extensiÃ³n)
   - âœ“ Virus scan (future)
   - âœ“ Status en {PENDING, APPROVED, REJECTED}
   - âœ“ Version auto-increment (v1 â†’ v2)
   - âœ“ Nuevo upload = nueva versiÃ³n, reemplaza anterior

10. **AuditLog**
    - âœ“ Append-only (insert allowed, update/delete forbidden)
    - âœ“ Action en {CREATE, UPDATE, DELETE, APPROVE, REJECT, VIEW, EXPORT, LOGIN, LOGOUT}
    - âœ“ Timestamp UTC obligatorio
    - âœ“ Outcome en {SUCCESS, FAIL}
    - âœ“ Si outcome=FAIL â†’ reason NOT NULL
    - âœ“ IP address parseable + user_agent present

### **Checklists de Empresa (Completitud por Fase)**

#### **ANTES DE F2 (Riesgos):**
```
[ ] Scope definido (sistemas in/out of scope)
[ ] PolÃ­tica de Seguridad InformaciÃ³n publicada
[ ] ComitÃ© SGSI constituido (RACI)
[ ] Criterios de aceptaciÃ³n riesgos definidos
[ ] Usuarios con roles asignados
```

#### **ANTES DE F3 (ImplementaciÃ³n):**
```
[ ] Risk Register completado (150+ riesgos evaluados)
[ ] SoA justificado (93 controles, aplicables/no aplicables)
[ ] Controles seleccionados para 93 items
[ ] Plan de Tratamiento de Riesgos (PTR) aprobado
[ ] Responsables por control asignados
[ ] Procedimientos documentados (borrador)
```

#### **ANTES DE F4 (AuditorÃ­a):**
```
[ ] Evidencias cargadas para 85+ controles
[ ] Evidencias aprobadas: 80%+
[ ] Procedimientos operando (logs activos)
[ ] Incidentes registrados (mÃ­n 1 para validar logs)
[ ] KPIs medidos (primera semana)
[ ] Usuarios capacitados (mÃ­n 80%)
```

#### **ANTES DE F5 (Readiness):**
```
[ ] 93 controles: estado NOT_IMPLEMENTED â‰¤ 5%
[ ] 93 controles: evidencias aprobadas â‰¥ 90%
[ ] Riesgos residuales: todos â‰¤ THRESHOLD
[ ] AuditLog: â‰¥ 100 eventos registrados (prueba)
[ ] Gaps identificados (â‰¤ 3 permitidos)
[ ] Acta RevisiÃ³n DirecciÃ³n firmada
[ ] Auditor externo confirmado para semana siguiente
```

### **Criterios de Cumplimiento**

**Por Control (SoAItem):**
- âœ“ Aplicable: justificaciÃ³n documentada
- âœ“ No aplicable: razÃ³n documentada
- âœ“ Implementado: evidencia aprobada
- âœ“ No implementado: plan de cierre documentado

**Por Riesgo:**
- âœ“ Score inherente â‰¤ THRESHOLD: ACEPTABLE
- âœ“ Score residual â‰¤ THRESHOLD: MITIGADO
- âœ“ Score residual > THRESHOLD: ACCEPT documentado + aprobado ejecutivo

**Por Proyecto:**
- âœ“ Progreso: â‰¥ 80% controles implementados
- âœ“ Calidad: â‰¥ 90% evidencias aprobadas sin rechazos
- âœ“ Trazabilidad: â‰¥ 100 eventos en AuditLog
- âœ“ DocumentaciÃ³n: SoA + PTR + Acta RD presentes

---

## I) INFORMACIÃ“N RELEVANTE PARA FRONTEND + BACKEND

### **Componentes UI Necesarios (Frontend React)**

#### **1. AutenticaciÃ³n**
- **LoginPage**
  - Form: username, password (validar en cliente + server)
  - Button: "Iniciar SesiÃ³n"
  - Error: "Usuario/contraseÃ±a invÃ¡lido"
  - Link: "Â¿OlvidÃ³ contraseÃ±a?" (future)
  - Redirige Dashboard si login OK

- **PrivateRoute**
  - Verifica token en localStorage
  - Si no hay token â†’ redirect Login
  - Si token expirado â†’ intenta refresh
  - Si refresh falla â†’ logout + redirect Login

#### **2. Navigation & Layout**
- **Header**
  - Logo VIT
  - Usuario actual (nombre + rol)
  - Button "Mis Proyectos"
  - Dropdown usuario: Perfil, Cambiar contraseÃ±a, Logout
  - Breadcrumb de navegaciÃ³n

- **Sidebar**
  - NavegaciÃ³n por rol:
    - **Admin**: Usuarios, Empresas, Proyectos, AuditorÃ­a
    - **Consultant**: Mis Proyectos, Reportes
    - **Client**: Mi Empresa, Mis Proyectos

#### **3. Dashboard (por rol)**
- **Admin Dashboard**
  - Tabla empresas (nombre, proyectos, estado)
  - KPI: total proyectos, total usuarios, Ãºltimos cambios
  - GrÃ¡fica: proyectos por estado (pie)
  - Link: crear empresa, crear proyecto

- **Consultant Dashboard**
  - Tabla "Mis Proyectos" (nombre, empresa, estado, progreso%)
  - KPI: proyectos in progress, riesgos crÃ­ticos, evidencias pendientes
  - GrÃ¡fica: matriz riesgos (inherent vs residual)
  - Button: crear proyecto, ver auditorÃ­a

- **Client Dashboard**
  - Tabla proyecto (estado, progreso%, prÃ³ximas tareas)
  - KPI: tareas vencidas, evidencias pendientes, controles
  - GrÃ¡fica: SoA progreso (barra 0-100%)
  - Button: subir evidencia, ver SoA

#### **4. Project Management**
- **ProjectList**
  - Tabla: nombre, empresa, estado, created_by, dates
  - Filtros: empresa, estado, consultor
  - Sort: por fecha, por estado
  - Button: crear proyecto, editar, borrar (admin)

- **ProjectDetail**
  - Tabs: InformaciÃ³n, Fases, Tareas, Riesgos, SoA, Evidencias, Reportes
  - InformaciÃ³n: empresa, estado, dates, description, usuarios asignados
  - Button: cambiar estado, editar, asignar usuario

- **PhaseView** (en tab)
  - Lista 5 fases (INIT, PLAN, IMPLEMENT, MAINTAIN, CERTIFY)
  - Cada fase: nombre, estado, progreso%, fecha
  - Expandible: show tareas de fase

- **TaskList** (en tab)
  - Tabla: titulo, responsable, prioridad, estado, vencimiento
  - Filtros: prioridad, estado
  - Button: crear tarea, editar, cambiar estado

#### **5. Scope & Assets**
- **ScopeView**
  - Texto: sistemas incluidos (textarea)
  - Texto: sistemas excluidos (textarea)
  - Textarea: justificaciÃ³n
  - Button: guardar, editar, descargar

- **AssetsList**
  - Tabla: nombre, type (badge color), criticality, dueÃ±o, ubicaciÃ³n
  - Filtros: type, criticality
  - Button: crear asset, editar, borrar
  - Form crear: name, type (dropdown), criticality, CIA levels (sliders 1-5)

#### **6. Risk Management** â† CRÃTICO
- **RiskList**
  - Tabla: descripciÃ³n, categorÃ­a, inherent_score, residual_score, tratamiento, estado
  - Matriz visual (5Ã—5 grid, color-coded):
    - Inherent score: X en zona roja
    - Residual score: Î” en zona verde
    - Eficiencia: tooltip muestra reducciÃ³n
  - Filtros: categorÃ­a, estado, effectividad mÃ­nima
  - Sort: por score, por estado
  - Button: crear riesgo, ver detalle, editar

- **RiskDetail** (modal/pÃ¡gina)
  - DescripciÃ³n, causa, consecuencias
  - Valores inherent (Prob, Impact, Score)
  - Valores residual (Prob, Impact, Score) con recalculaciÃ³n en tiempo real
  - Multiselect: controles mitigantes (A.5.1, A.5.15, etc.)
  - Dropdown: tratamiento (ACCEPT/MITIGATE/TRANSFER/AVOID)
  - Dropdown: estado (IDENTIFIED/ASSESSED/MITIGATED/MONITORED)
  - TextField: plan mitigaciÃ³n
  - Tabla: controles vinculados (edit vÃ­a SoA)
  - Button: guardar, generar evidencias (future)

- **RiskMatrix** (componente)
  - Grid 5Ã—5
  - Eje X: Impact 1-5
  - Eje Y: Likelihood 1-5
  - Cada cell: riesgos en esa combinaciÃ³n (clickeable)
  - Colores: verde (â‰¤aceptable), amarillo (mitigable), rojo (crÃ­tico)
  - Toggle: mostrar inherent O residual

#### **7. ISO Controls & SoA**
- **SoAList** â† CRÃTICO
  - Tabla: cÃ³digo (A.5.1), nombre, categorÃ­a, aplicable?, estado?, evidencias? responsable
  - Filtros: categorÃ­a, aplicable, estado, responsable
  - Sort: cÃ³digo
  - Expandible: detalle + campo editar
  - Form inline: checkbox aplicable, textarea justificaciÃ³n,  dropdown estado, select responsable
  - Button: guardar cambio, exportar SoA (PDF/Excel)

- **SoADetail** (modal)
  - Nombre control (read-only)
  - DescripciÃ³n ISO (read-only)
  - Checkbox: "Â¿Aplica en este proyecto?"
  - Si NO aplica: textarea para justificaciÃ³n
  - Si SÃ aplica:
    - Dropdown: estado (NOT_IMPL/IN_PROGRESS/IMPLEMENTED)
    - Select: responsable implementaciÃ³n
    - Tabla: evidencias asociadas (version, status, fecha, button)
    - Button: subir nueva evidencia
  - Timeline: historial de cambios (AuditLog)

#### **8. Evidence Management**
- **EvidenceList**
  - Tabla: control, versiÃ³n, estado (badge), fecha upload, uploader, button ver/descargar
  - Filtros: control, estado (PENDING/APPROVED/REJECTED)
  - Sort: fecha DESC
  - Button: subir evidencia

- **EvidenceUpload** (form/modal)
  - Selector: control/SoA item (dropdown)
  - File input: solo PDF/DOCX/XLSX/JPG/PNG, mÃ¡x 50MB
  - Ãrea: "drag-drop aquÃ­"
  - Button: upload
  - Feedback: porcentaje upload, success/error

- **EvidenceReview** (modal)
  - Mostrar: archivo (PDF preview si disponible)
  - Info: versiÃ³n, uploader, fecha, actual status
  - Si status=PENDING (y usuario es Consultant):
    - Botones: APPROVE, REJECT
    - Textarea: comentarios
  - Si rejected: histÃ³rico de rechazos + nuevo upload option
  - Timeline: versiones anteriores (v1, v2, v3)

#### **9. Reports & Exports**
- **ReportGenerator**
  - Dropdown: tipo reporte (SoA, Riesgos, Cumplimiento, Ejecutivo)
  - Button: generar (puede tardarse)
  - Tabla: histÃ³rico reportes (fecha, tipo, button descargar)
  - Formato export: PDF o Excel

- **ReportViewer**
  - Embed PDF viewer o tabla
  - GrÃ¡ficas: matriz riesgos, barra SoA progreso, pie fases
  - Tablas: tabulaciÃ³n data
  - Button: descargar, imprimir

#### **10. AuditorÃ­a & Logs**
- **AuditLogBrowser** (admin only)
  - Tabla: fecha, usuario, acciÃ³n, entidad, objeto_id, resultado
  - Filtros: usuario, acciÃ³n, entidad, fecha_from/to
  - Expandible: ver cambios (JSON diff)
  - Button: exportar (CSV/JSON)

---

### **APIs/Endpoints NecesÃ¡rios (Backend Django)**

#### **1. AUTENTICACIÃ“N (users app)**
```
POST   /api/token/
       Body: {username, password}
       Response: {access, refresh}

POST   /api/token/refresh/
       Body: {refresh}
       Response: {access}

POST   /api/logout/ (optional)
       Response: {success}

POST   /api/users/ (Admin)
       Body: {username, email, password, first_name, last_name, role, phone}
       Response: User object

GET    /api/users/
       Query: ?role=CONSULTANT&is_active=true
       Response: [User...]

GET    /api/users/{id}/
       Response: User object

PUT    /api/users/{id}/
       Body: {first_name, last_name, phone}
       Response: User object

PUT    /api/users/{id}/change-password/
       Body: {password, new_password}
       Response: {success}

GET    /api/profile/
       Response: User object (current user)
```

#### **2. COMPANIES (companies app)**
```
POST   /api/companies/ (Admin)
       Body: {name, tax_id, email, phone, address, city, state, contact_person, sector}
       Response: Company object

GET    /api/companies/
       Query: ?name=Bancolombia&sector=BANKING
       Response: [Company...]

GET    /api/companies/{id}/
       Response: Company object

PUT    /api/companies/{id}/
       Body: {email, phone, contact_person}
       Response: Company object

DELETE /api/companies/{id}/ (Admin)
       Response: {success}
```

#### **3. PROJECTS (projects app)**
```
POST   /api/projects/ (Consultant)
       Body: {company_id, name, description, start_date, end_date}
       Response: Project object + auto-generates 5 Phases + 93 SoAItems

GET    /api/projects/
       Query: ?company_id=1&status=IN_PROGRESS&created_by=12
       Response: [Project...]

GET    /api/projects/{id}/
       Response: Project object including Phases, Tasks, counts

PUT    /api/projects/{id}/
       Body: {name, description, end_date, status}
       Response: Project object

DELETE /api/projects/{id}/
       Response: {success}

POST   /api/project-users/ (Admin/Consultant)
       Body: {project_id, user_id, role}
       Response: ProjectUser object

GET    /api/projects/{id}/users/
       Response: [ProjectUser...]

GET    /api/users/{id}/projects/
       Response: [Project...]
```

#### **4. PHASES & TASKS**
```
GET    /api/projects/{id}/phases/
       Response: [Phase...]

PUT    /api/phases/{id}/
       Body: {status, percentage_complete}
       Response: Phase object

POST   /api/projects/{id}/tasks/ (Consultant)
       Body: {phase_id, title, description, assigned_to_id, priority, due_date}
       Response: Task object

GET    /api/projects/{id}/tasks/
       Query: ?status=IN_PROGRESS&priority=HIGH
       Response: [Task...]

PUT    /api/tasks/{id}/
       Body: {status, assigned_to_id}
       Response: Task object
```

#### **5. SCOPE & ASSETS**
```
POST   /api/projects/{id}/scope/ (Consultant)
       Body: {included_systems, excluded_systems, justification}
       Response: Scope object

PUT    /api/scope/{id}/
       Body: {included_systems, excluded_systems, justification}
       Response: Scope object

POST   /api/projects/{id}/assets/ (Consultant/Client)
       Body: {name, type, owner_id, location, criticality, confidentiality_level, integrity_level, availability_level}
       Response: Asset object

GET    /api/projects/{id}/assets/
       Query: ?type=DATA&criticality=CRITICAL
       Response: [Asset...]

PUT    /api/assets/{id}/
       Body: {name, type, criticality, CIA levels}
       Response: Asset object

DELETE /api/assets/{id}/
       Response: {success}
```

#### **6. RISK (risks app)** â† CRÃTICO
```
POST   /api/projects/{id}/risks/ (Consultant)
       Body: {name, description, cause, consequence, category, owner_id,
               inherent_likelihood, inherent_impact,
               (residual_likelihood, residual_impact),
               treatment, mitigation_plan}
       Response: Risk object 
       Auto-calc: inherent_score, residual_score, risk_reduction

GET    /api/projects/{id}/risks/
       Query: ?status=MITIGATED&min_residual_score=10
       Response: [Risk...]

GET    /api/risks/{id}/
       Response: Risk object

PUT    /api/risks/{id}/
       Body: {residual_likelihood, residual_impact, treatment, status, mitigation_plan}
       Response: Risk object (scores recalculated)
       Auto-update: SoAItems linked

DELETE /api/risks/{id}/ (Consultant)
       Response: {success}

POST   /api/risks/{id}/controls/ (Consultant)
       Body: {iso_control_id}
       Response: M2M relation created

DELETE /api/risks/{id}/controls/{iso_control_id}/
       Response: {success}

GET    /api/projects/{id}/risks/matrix/
       Response: {
         data: [[score_1_1, score_1_2, ...], ...],
         risks: [
           {prob: 5, impact: 5, inherent_score: 25, residual_score: 10, ...}
         ]
       }
```

#### **7. ISO CONTROLS & SOA** â† CRÃTICO
```
GET    /api/iso-controls/
       Query: ?category=ORGANIZATIONAL&code=A.5
       Response: [ISOControl...] â† 93 precargados

GET    /api/iso-controls/{id}/
       Response: ISOControl object

GET    /api/projects/{id}/soa/
       Query: ?is_applicable=true&impl_status=IMPLEMENTED
       Response: [SoAItem...]

GET    /api/soa-items/{id}/
       Response: SoAItem object

PUT    /api/soa-items/{id}/ (Consultant/Client)
       Body: {is_applicable, justification, implementation_status, responsible_id}
       Response: SoAItem object
       Auto-update: Risk linked if impl_status=IMPLEMENTED

POST   /api/projects/{id}/soa/export/
       Query: ?format=pdf (o excel)
       Response: file download (PDF/Excel con 93 items)
```

#### **8. EVIDENCE (documents app)**
```
POST   /api/projects/{id}/evidence/ (Client/Consultant)
       Headers: Content-Type: multipart/form-data
       Body: {soaitem_id, file}
       Validation: tipo+tamaÃ±o
       Response: Evidence object {id, version, status: PENDING, ...}

GET    /api/projects/{id}/evidence/
       Query: ?status=PENDING&soaitem_id=15
       Response: [Evidence...]

GET    /api/evidence/{id}/download/
       Response: file (application/octet-stream)

PUT    /api/evidence/{id}/ (Consultant)
       Body: {status, comments}
       Response: Evidence object
       Auto-update: SoAItem.status â†’ IMPLEMENTED si APPROVED

DELETE /api/evidence/{id}/ (Consultant)
       Response: {success}
```

#### **9. REPORTS**
```
POST   /api/projects/{id}/reports/generate/
       Body: {type: "SOA" | "RISKS" | "COMPLIANCE" | "EXECUTIVE"}
       Response: {report_id, status: "PROCESSING"}
       (puede retornar async + webhook o polling)

GET    /api/projects/{id}/reports/
       Response: [Report...]

GET    /api/reports/{id}/
       Response: Report object {id, type, generated_at, file_path}

GET    /api/reports/{id}/download/
       Query: ?format=pdf (default) | excel
       Response: file download

POST   /api/reports/{id}/email/
       Body: {recipients: [email@...]}
       Response: {sent: true}
```

#### **10. AUDIT LOG**
```
GET    /api/audit-logs/
       Query: ?user_id=12&action=UPDATE&entity=Risk&date_from=2026-02-01&date_to=2026-02-28
       Response: [AuditLog...]

GET    /api/audit-logs/{id}/
       Response: AuditLog object

GET    /api/audit-logs/export/
       Query: ?format=csv&filters=...
       Response: file download (CSV/JSON)
```

#### **11. DASHBOARD (projects app)**
```
GET    /api/projects/{id}/dashboard/
       Response: {
         project_info: {...},
         phases_progress: [{code, status, percentage}, ...],
         tasks_summary: {total, completed, blocked},
         risks_summary: {total, by_status, avg_inherent, avg_residual, reduction},
         soa_summary: {total, implemented, pending, not_applicable},
         evidence_summary: {total, approved, rejected, pending},
         kpi: {
           project_progress: 45,
           risk_mitigation: 60,
           control_implementation: 30
         }
       }
```

---

### **BÃºsquedas y Filtros CrÃ­ticos**

| Funcionalidad | Query Parameters |
|---|---|
| Listar Proyectos | `?company_id=1&status=IN_PROGRESS&created_by=12` |
| Filtrar Riesgos | `?status=MITIGATED&min_score=10&category=TECHNICAL` |
| BÃºscar SoA | `?category=ORGANIZATIONAL&impl_status=NOT_IMPLEMENTED` |
| Evidencias pendientes | `?status=PENDING&date_from=2026-02-01` |
| AuditorÃ­a | `?user_id=12&action=UPDATE&entity=Risk&date_from=2026-02-01` |
| Activos crÃ­ticos | `?criticality=CRITICAL&type=DATA` |
| Tareas vencidas | `?status=NOT_STARTED&due_date_lte=today` |

---

### **Reportes y Exportaciones**

1. **SoA Report (PDF/Excel)**
   - 93 lÃ­neas: cÃ³digo, nombre, categorÃ­a, aplicable, justificaciÃ³n, estado, responsable, evidencias
   - Resumen: % implementado, % no aplicable, gaps

2. **Risk Report**
   - Tabla: descripciÃ³n, categorÃ­a, inherent_score, residual_score, reducciÃ³n, tratamiento, estado
   - Matriz 5Ã—5 visual
   - GrÃ¡fica: distribuciÃ³n por categorÃ­a
   - KPI: promedio scores, proyecciÃ³n cierre

3. **Cumplimiento Report**
   - % por fase (INIT, PLAN, IMPLEMENT, MAINTAIN, CERTIFY)
   - % por control (implementado vs pendiente)
   - Timeline cronograma vs real
   - List: tareas no completadas, evidencias rechazadas

4. **Ejecutivo**
   - KPIs clave: progreso proyecto, riesgos residuales, controles implementados
   - GrÃ¡ficas: dashboard visual
   - Resumen decisiones: aprobaciones, cambios tratamiento
   - PrÃ³ximos pasos y riesgos crÃ­ticos

5. **Audit Log Export**
   - CSV: timestamp, usuario, acciÃ³n, entidad, objeto_id, resultado
   - JSON: para anÃ¡lisis programÃ¡tico
   - Filtrable por rango fechas, usuario, acciÃ³n

---

### **Rendimiento Esperado (bÃºsquedas/filtros)**

- **GET /api/projects/**: â‰¤500ms (con Ã­ndices en company, status)
- **GET /api/projects/{id}/soa/**: â‰¤1000ms (93 items + joins)
- **GET /api/projects/{id}/dashboard/**: â‰¤2000ms (agregaciones)
- **POST /api/reports/generate/**: async (puede tardar 5-10s), retornar job_id

---

## CONCLUSIÃ“N

VIT es una plataforma **SGSI ISO 27001 end-to-end** que:
- âœ… Estructura implementaciÃ³n en 6 fases (INIT â†’ READINESS)
- âœ… Automatiza evaluciÃ³n de riesgos (dual inherent/residual)
- âœ… Mapea 93 controles con aplicabilidad por proyecto (SoA)
- âœ… Gestiona evidencias con versionado y aprobaciÃ³n
- âœ… Audita TODOS cambios (QUIEN/QUE/CUANDO/DONDE)
- âœ… Genera reportes de cumplimiento para auditorÃ­a externa
- âœ… Implementa RBAC (3 roles) + PBAC (ProjectUser)
- âœ… Prioriza seguridad desde inicio (JWT, bcrypt, HTTPS, logs)

**Tipo de arquitectura**: Full-stack B2B multi-tenant, dirigido a empresas medianas/grandes ($$$) implementando certificaciÃ³n ISO 27001.

**Diferenciador clave**: Modelo de riesgo dual (inherent vs residual) + auditorÃ­a automÃ¡tica = cumplimiento verificable post-certificaciÃ³n.

---

AnÃ¡lisis completado basado en documentaciÃ³n oficial del proyecto (RESUMEN_EJECUTIVO, DICCIONARIO_DATOS, MODELO_DATOS_FORMAL, ARQUITECTURA_RIESGOS, CARDINALIDADES, ESTRATEGIA_AUDITORIA, SPRINT_1_GUIA, ASIGNACIONES, Planner 150 dÃ­as).
