# CARDINALIDADES Y RELACIONES — VIT

> **Nota de contexto (al 18-02-2026):** el backend cuenta con Users/Companies/Projects/Phases/Tasks. Los módulos SGSI (Scope, Asset, Risk, ISOControl, SoAItem, Evidence, Report, AuditLog) están definidos a nivel documental y se implementarán en las siguientes iteraciones.
## Especificación formal de entidades y sus vínculos
Versión: 1.0 | Fecha: febrero de 2026

---

## Tabla de Contenidos

- [Introducción a Cardinalidades](#introducción-a-cardinalidades)
- [Relaciones :N (One-to-Many)](#relaciones-n-one-to-many)
- [Relaciones N:M (Many-to-Many)](#relaciones-nm-many-to-many)
- [Relaciones Self (Autoreferencia)](#relaciones-self-autoreferencia)
- [Diagrama Completo de Relaciones](#diagrama-completo-de-relaciones)
- [Restricciones Referenciales](#restricciones-referenciales)
- [Cascadas de Eliminacion](#cascadas-de-eliminacion)
- [Ejemplo de Flujo de Datos](#ejemplo-de-flujo-de-datos)

---

## Introducción a Cardinalidades

### Notación de Cardinalidad

En base de datos relacional, las cardinalidades especifican **cuántos registros de una tabla pueden conectarse a cuántos de otra**.

```
Notacion: A (cardinalidad_A) <-> (cardinalidad_B) B

Cardinalidades:
- (Uno): Maximo un registro
- N (Muchos): Cero, uno, o multiples registros
- 0..(Cero o Uno): Optativo
- ..N (Uno o Muchos): Obligatorio
```

### Tipos de Relaciones

- **:(One-to-One)** - Un registro de A se conecta a maximo un registro de B
- **:N (One-to-Many)** - Un registro de A puede conectarse a cero, uno, o muchos de B
- **N:M (Many-to-Many)** - Un registro de A puede conectarse a muchos de B y viceversa

### Implementación en Django

```python
# :N: Tabla B tiene FK hacia A
class A(Model):
 pass

class B(Model):
 a_fk = ForeignKey(A, on_delete=...) # N lado

# N:M: Tabla intermedia
class A(Model):
 pass

class B(Model):
 a_set = ManyToManyField(A, through='ABRelation')

class ABRelation(Model):
 a = ForeignKey(A, ...)
 b = ForeignKey(B, ...)
 created_at = DateTimeField(auto_now_add=True)
```

---

## Relaciones :N (One-to-Many)

### . USER (1) <-> (N) PROJECT

**Descripción**: Un usuario puede crear multiples proyectos; cada proyecto tiene un creador.

**Cardinalidad Formal**:
```
User () --created_by--> (N) Project

Restriccion:
- Un user -> N projects (el mismo user puede crear 0, , , ... proyectos)
- Un project <- user (obligatoriamente tiene un creador)
- Cardinalidad: () User : (N) Project
```

**Implementación Django**:
```python
class User(Model):
 username = CharField(UNIQUE=True)
 email = CharField(UNIQUE=True)
 role = CharField(choices=ROLE_CHOICES)
 created_at = DateTimeField(auto_now_add=True)
 # Reverse relation: project_set (automatico)
 # User.objects.get(id=).project_set.all() -> todos sus proyectos

class Project(Model):
 company = ForeignKey(Company, on_delete=CASCADE)
 name = CharField()
 created_by = ForeignKey(User, on_delete=SET_NULL, null=True)
 # created_by es la FK (N lado)
```

**Ejemplo de Datos**:
```
USER TABLE:
| id | username | role |
|----|----------|------------|
| | carlos | CONSULTANT |
| | maria | ADMIN |
| | juan | CLIENT |

PROJECT TABLE:
| id | company_id | name | created_by_id |
|----|------------|-------------------|---------------|
| 1 | | ISO Plan A | (carlos) |
| 2 | | ISO Plan B | (carlos) |
| | | SGSI Implementacion| (maria) |

Relacion:
- User (carlos) -> proyectos (0, )
- User (maria) -> proyecto ()
- User (juan) -> 0 proyectos

Consultas SQL:
SELECT * FROM project WHERE created_by_id = ; -> Retorna proyectos 0, 
```

**Restricciones**:
```sql
FOREIGN KEY (created_by_id) REFERENCES user(id) ON DELETE SET_NULL;
-- Si se elimina user, created_by de sus proyectos queda NULL
```

---

### . COMPANY (1) <-> (N) PROJECT

**Descripción**: Una empresa tiene multiples proyectos ISO; cada proyecto pertenece a una empresa.

**Cardinalidad**:
```
Company () --links--> (N) Project

Restriccion:
- Una company -> 0, , , ... N projects
- Un project <- company (obligatoriamente)
- Cardinalidad: () Company : (N) Project
```

**Implementación**:
```python
class Company(Model):
 name = CharField(UNIQUE=True)
 rfc = CharField(UNIQUE=True)
 email = CharField()
 # Reverse relation: project_set (automatico)
 # Company.objects.get(id=).project_set.all()

class Project(Model):
 company = ForeignKey(Company, on_delete=CASCADE) # N lado
 name = CharField()
 created_by = ForeignKey(User, on_delete=SET_NULL)
```

**Cardinalidad Combinada (con USER)**:
```
Company (1) --(N) Project
Project (1) --created_by--> User (1)
User (1) --(N) projects (reverse)
```

Ejemplo de datos:
Company (Consultec)
- Project 0 (created by User )
- Project (created by User )
- Project (created by User )
- Project (created by User )

Company (Bancarios)
- Project (created by User )
- Project (created by User )
```

**Restricciones**:
```sql
FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE;
-- Si se elimina company, se eliminan TODOS sus proyectos (en cascada)
```

**Impacto de Cascada**:
```
DELETE FROM company WHERE id = ; -> Automáticamente delete FROM project WHERE company_id = ; -> Automáticamente delete FROM phase WHERE project_id IN (0, , , ); -> ... (cascada completa)
```

---

### . PROJECT (1) <-> (N) PHASE

**Descripcion**: Un proyecto tiene multiples fases (Assessment, Planning, Implementation, etc.); cada fase pertenece a un proyecto.

**Cardinalidad**:
```
Project () --contains--> (N) Phase

Restricción:
- Un project -> 0, , , phases (tipicamente -)
- Una phase <- project (obligatoriamente)
- Orden: (sequence) , , , ... (no repeats)
- Cardinalidad: () Project : (N) Phase
```

**Implementacion**:
```python
class Project(Model):
 company = ForeignKey(Company, on_delete=CASCADE)
 name = CharField()
 created_by = ForeignKey(User, on_delete=SET_NULL)
 # Reverse relation: phase_set (automático)

class Phase(Model):
 project = ForeignKey(Project, on_delete=CASCADE) # N lado
 code = CharField(choices=PHASE_CODES) # INIT, PLAN, IMPLEMENT, MAINTAIN, CERTIFY
 name = CharField()
 sequence = IntegerField()

 class Meta:
 unique_together = ('project', 'sequence') # No dos fases con mismo sequence
```

**Ejemplo**:
```
Project 1 (ISO Plan A)
- Phase (sequence=, code=INIT)
- Phase (sequence=, code=PLAN)
- Phase (sequence=, code=IMPLEMENT)
- Phase (sequence=, code=MAINTAIN)
- Phase (sequence=, code=CERTIFY)

Project 2 (ISO Plan B)
- Phase (sequence=, code=INIT)
- Phase (sequence=, code=PLAN)
- Phase (sequence=, code=IMPLEMENT)
```

---

### . PHASE (1) <-> (N) TASK

**Descripcion**: Una fase contiene multiples tareas; cada tarea pertenece a una fase.

**Cardinalidad**:
```
Phase () --contains--> (N) Task

Restricción:
- Una phase -> 0..N tasks
- Un task <- phase (obligatoriamente)
- Cardinalidad: () Phase : (N) Task
```

**Implementacion**:
```python
class Phase(Model):
 project = ForeignKey(Project, on_delete=CASCADE)
 code = CharField()
 name = CharField()
 # Reverse relation: task_set (automático)

class Task(Model):
 phase = ForeignKey(Phase, on_delete=CASCADE) # N lado
 title = CharField()
 assigned_to = ForeignKey(User, on_delete=SET_NULL, null=True)
 priority = CharField(choices=PRIORITY_CHOICES)
 status = CharField(choices=STATUS_CHOICES)
```

---

### . PROJECT (1) <-> (N) RISK

**Descripcion**: Un proyecto tiene multiples riesgos identificados; cada riesgo pertenece a un proyecto.

**Cardinalidad**:
```
Project () --identifies--> (N) Risk

Restricción:
- Un project -> 0..N risks
- Un risk <- project (obligatoriamente)
- Unicidad: (project_id, name) - no dos riesgos con mismo nombre
- Cardinalidad: () Project : (N) Risk
```

**Implementacion**:
```python
class Project(Model):
 company = ForeignKey(Company, on_delete=CASCADE)
 name = CharField()
 # Reverse relation: risk_set (automático)

class Risk(Model):
 project = ForeignKey(Project, on_delete=CASCADE) # N lado
 name = CharField()
 description = TextField()
 inherent_likelihood = IntegerField(choices=LIKELIHOOD_CHOICES)
 inherent_impact = IntegerField(choices=IMPACT_CHOICES)
 # ... riesgos residuales, tratamiento, etc.

 class Meta:
 unique_together = ('project', 'name')
```

---

### . PROJECT (1) <-> (N) ASSET

**Descripcion**: Un proyecto tiene un inventario de activos; cada activo pertenece a un proyecto.

**Cardinalidad**:
```
Project () --has--> (N) Asset

Restricción:
- Un project -> 0..N assets
- Un asset <= project (obligatoriamente)
- Unicidad: (project_id, name)
- Cardinalidad: () Project : (N) Asset
```

**Implementacion**:
```python
class Project(Model):
 company = ForeignKey(Company, on_delete=CASCADE)
 # Reverse relation: asset_set

class Asset(Model):
 project = ForeignKey(Project, on_delete=CASCADE) # N lado
 name = CharField()
 type = CharField(choices=ASSET_TYPES)
 owner = ForeignKey(User, on_delete=SET_NULL, null=True)
 criticality = CharField(choices=CRITICALITY_LEVELS)
 confidentiality_level = IntegerField(choices=CIA_LEVELS)
 integrity_level = IntegerField(choices=CIA_LEVELS)
 availability_level = IntegerField(choices=CIA_LEVELS)

 class Meta:
 unique_together = ('project', 'name')
```

---

### 7. PROJECT (1) <-> (N) SOAITEM

**Descripcion**: **Generacion automatica**: un proyecto genera **exactamente 93 SoAItems** (uno por cada ISOControl).

**Cardinalidad**:
```
Project () --generates--> (N=93) SoAItem

Restricción:
- Un project -> exactamente 93 SoAItems (automático via Signal)
- Un SoAItem <= project (obligatoriamente)
- Unicidad: (project_id, iso_control_id) - un control por proyecto
- Cardinalidad: () Project : (93) SoAItem (constante)
```

**Implementacion con Signal**:
```python
class Project(Model):
 company = ForeignKey(Company, on_delete=CASCADE)
 name = CharField()
 # Reverse relation: soaitem_set (automático)

class SoAItem(Model):
 project = ForeignKey(Project, on_delete=CASCADE) # N lado
 iso_control = ForeignKey(ISOControl, on_delete=PROTECT)
 is_applicable = BooleanField(default=True)
 justification = TextField(null=True)
 implementation_status = CharField(choices=IMPL_STATUS)

 class Meta:
 unique_together = ('project', 'iso_control')

# Signal: Generar automáticamente al crear Project
@receiver(post_save, sender=Project)
def create_soa_items(sender, instance, created, **kwargs):
 if created:
 controls = ISOControl.objects.all() # 93 controles
 soa_items = [
 SoAItem(project=instance, iso_control=control)
 for control in controls
 ]
 SoAItem.objects.bulk_create(soa_items)
```

**Ejemplo**:
```
Project 1 CREATED
Signal triggered: create_soa_items()
for control in ISOControl.objects.all(): # 93 iteraciones
 SoAItem.objects.create(project=1, iso_control=control)

Result:
- SoAItem -> Project 1 + Control A.5.1
- SoAItem -> Project 1 + Control A.5.2
...
Total SoAItems en Project 1: 93 (exactamente)
```

---

### 8. PROJECT (1) <-> (N) DOCUMENT

**Descripcion**: Un proyecto puede generar multiples documentos (reports, templates); cada documento pertenece a un proyecto o es global.

**Cardinalidad**:
```
Project () --generates--> (N) Document

Restricción:
- Un project -> 0..N documents
- Un document <- project (nullable - puede ser global)
- Cardinalidad: () Project : (N) Document (opcional)
```

**Implementacion**:
```python
class Project(Model):
 company = ForeignKey(Company, on_delete=CASCADE)
 # Reverse relation: document_set

class Document(Model):
 project = ForeignKey(Project, on_delete=CASCADE, null=True) # N lado (nullable)
 type = CharField(choices=DOC_TYPES)
 title = CharField()
 file = FileField()
 is_template = BooleanField(default=False)
 version = IntegerField(default=1)
 generated_by = ForeignKey(User, on_delete=SET_NULL, null=True)
```

**Diferencia**:
- `document.project_id = <id>`: Documento especifico del Project 
- `document.project_id = NULL`: Plantilla global (SoA template, Policy template, etc.)

---

### 9. PROJECT (1) <-> (N) EVIDENCE

**Descripcion**: Un proyecto recibe multiples evidencias del cliente; cada evidencia pertenece a un proyecto.

**Cardinalidad**:
```
Project () --receives--> (N) Evidence

Restricción:
- Un project -> 0..N evidences
- Una evidence <= project (obligatoriamente)
- Cardinalidad: () Project : (N) Evidence
```

**Implementacion**:
```python
class Project(Model):
 company = ForeignKey(Company, on_delete=CASCADE)
 # Reverse relation: evidence_set

class Evidence(Model):
 project = ForeignKey(Project, on_delete=CASCADE) # N lado
 iso_control = ForeignKey(ISOControl, on_delete=SET_NULL, null=True)
 name = CharField()
 file = FileField()
 uploaded_by = ForeignKey(User, on_delete=SET_NULL, null=True)
 status = CharField(choices=STATUS_CHOICES)
 version = IntegerField(default=1)
 previous_version = ForeignKey('self', on_delete=SET_NULL, null=True) # Self-FK
```

---

### 0. USER (1) <-> (N) EVIDENCE (uploaded_by)

**Descripcion**: Un usuario carga multiples evidencias; cada evidencia tiene un loader.

**Cardinalidad**:
```
User () --uploads--> (N) Evidence

Restricción:
- Un user -> 0..N evidences (como uploaded_by)
- Una evidence <- user (quien subio, obligatorio)
- Cardinalidad: () User : (N) Evidence
```

**Implementacion**:
```python
class User(Model):
 username = CharField(UNIQUE=True)

class Evidence(Model):
 project = ForeignKey(Project, on_delete=CASCADE)
 uploaded_by = ForeignKey(User, on_delete=SET_NULL, null=True, related_name='uploaded_evidences')
 # related_name permite: user.uploaded_evidences.all()
```

---

### . USER (1) <-> (N) EVIDENCE (approved_by)

**Descripcion**: Un admin/consultor aprueba multiples evidencias; cada evidencia aprobada tiene un aprobador.

**Cardinalidad**:
```
User () --approves--> (N) Evidence

Restricción:
- Un user -> 0..N evidences (como approved_by)
- Una evidence <- user (nullable - solo si aprobada)
- Cardinalidad: () User : (N) Evidence (opcional)
```

**Implementacion**:
```python
class Evidence(Model):
 project = ForeignKey(Project, on_delete=CASCADE)
 uploaded_by = ForeignKey(User, on_delete=SET_NULL, null=True, related_name='uploaded_evidences')
 approved_by = ForeignKey(User, on_delete=SET_NULL, null=True, related_name='approved_evidences')
 status = CharField(choices=['PENDING', 'APPROVED', 'REJECTED'])

 # Validación: si status=APPROVED -> approved_by != NULL
 def clean(self):
 if self.status == 'APPROVED' and not self.approved_by:
 raise ValidationError(«Approved evidence must have approved_by user»)
```

---

### . USER (1) <-> (N) AUDITLOG

**Descripcion**: Un usuario realiza multiples acciones auditadas; cada registro de auditoria identifica al user.

**Cardinalidad**:
```
User () --performs--> (N) AuditLog

Restricción:
- Un user -> 0..N audit entries
- Un auditlog <- user (nullable - user puede ser eliminado)
- Cardinalidad: () User : (N) AuditLog (nullable)
```

**Implementacion**:
```python
class AuditLog(Model):
 user = ForeignKey(User, on_delete=SET_NULL, null=True) # N lado
 action = CharField(choices=ACTIONS)
 model_name = CharField()
 object_id = IntegerField()
 timestamp = DateTimeField(auto_now_add=True)
 changes = JSONField(null=True)
```

---

## Relaciones N:M (Many-to-Many)

### . RISK (N) <-> (M) ASSET

**Descripcion**: Un riesgo puede afectar multiples activos; un activo puede ser afectado por multiples riesgos.

**Cardinalidad**:
```
Risk (N) --affects--> (M) Asset

Restricción:
- Un risk -> 0..N assets
- Un asset <- 0..N risks
- Relacion: muchos a muchos
- Tabla intermedia: risk_asset (Risk.id, Asset.id, created_at)
```

**Implementacion**:
```python
class Risk(Model):
 project = ForeignKey(Project, on_delete=CASCADE)
 name = CharField()
 # Relacion N:M hacia Asset
 affected_assets = ManyToManyField(Asset, related_name='risks_affecting')

class Asset(Model):
 project = ForeignKey(Project, on_delete=CASCADE)
 name = CharField()
 # Reverse relation: risks_affecting (automático)

# Tabla intermedia generada automáticamente: risk_asset
# Acceso:
risk.affected_assets.all() # Todos los assets afectados por este riesgo
asset.risks_affecting.all() # Todos los riesgos que afectan este asset
```

**Ejemplo**:
```
Risk : «Exposicion BD clientes»
- Asset 0: «BD PostgreSQL» -
- Asset : «Servidor APP» -
- Asset : «Router» -

Risk : «Fallo de energia»
- Asset 0: «BD PostgreSQL» -
- Asset : «Servidor APP» -
- Asset 0: «Generador diesel» --

Tabla risk_asset (intermedia):
| risk_id | asset_id |
|---------|----------|
| | 0 |
| | |
| | |
| | 0 |
| | |
```

---

### . RISK (N) <-> (M) ISOCONTROL

**Descripcion**: Un riesgo se mitiga con multiples controles ISO; un control puede mitigar multiples riesgos.

**Cardinalidad**:
```
Risk (N) --mitigated_by--> (M) ISOControl

Restricción:
- Un risk -> 0..N controls (controles que mitigan)
- Un control <- 0..N risks (riesgos que mitiga)
- Relacion: muchos a muchos
- Tabla intermedia: risk_mitigating_controls
```

**Implementacion**:
```python
class Risk(Model):
 project = ForeignKey(Project, on_delete=CASCADE)
 name = CharField()
 inherent_likelihood = IntegerField()
 inherent_impact = IntegerField()
 residual_likelihood = IntegerField()
 residual_impact = IntegerField()
 treatment = CharField(choices=['MITIGATE', 'AVOID', 'TRANSFER', 'ACCEPT'])
 # Relacion N:M hacia ISOControl
 mitigating_controls = ManyToManyField(ISOControl, related_name='mitigated_risks')

class ISOControl(Model):
 code = CharField(UNIQUE=True) # p. ej., A.5.15, A.6.3, A.8.15, A.8.28, etc.
 name = CharField()
 # Reverse relation: mitigated_risks (automático)

# Tabla intermedia: risk_mitigating_controls
# Acceso:
risk.mitigating_controls.add(control, control, control)
risk.mitigating_controls.all() # Todos los controles que mitigan este riesgo
control.mitigated_risks.all() # Todos los riesgos que mitiga este control
```

**Ejemplo**:
```
Risk : «Exposicion BD clientes»
- A.5.15: Control de acceso -
- A.8.24: Uso de criptografía -
- A.6.3: Concientización, educación y capacitación -
- A.8.15 Registro de eventos -

Risk : «Malware infection»
- A.8.: User endpoint protection -
- A.6.3: Concientización, educación y capacitación -
- A.8.15 Registro de eventos -

Tabla risk_mitigating_controls:
| risk_id | isocontrol_id |
|---------|---------------|
| | 8 (A.8.) |
| | 9 (A.8.) |
| | (A.6.3) |
| | (A.8.15) |
| | 7 (A.8.) |
| | (A.6.3) |
| | (A.8.15) |

Intersección (A.6.3, A.8.15): Controles que mitigan multiples riesgos
```

---

### . ISOCONTROL (N) <-> (M) SOAITEM

**Descripcion**: En realidad es **:N** (un control -> N SoAItems). Pero tecnicamente podria considerarse acceso N:M a nivel de datos.

**Cardinalidad Real**:
```
ISOControl () --has--> (N) SoAItem

Restricción:
- Un control -> exactamente N SoAItems (uno por proyecto)
- Un SoAItem <= control (obligatoriamente)
- Cardinalidad: () ISOControl : (N) SoAItem
```

**Implementacion**:
```python
class ISOControl(Model):
 code = CharField(UNIQUE=True)
 name = CharField()
 # Reverse relation: soaitem_set (automático)

class SoAItem(Model):
 project = ForeignKey(Project, on_delete=CASCADE)
 iso_control = ForeignKey(ISOControl, on_delete=PROTECT) # N lado
 is_applicable = BooleanField(default=True)
 implementation_status = CharField()

 class Meta:
 UNIQUE_together = ('project', 'iso_control')
```

**Ejemplo**:
```
ISOControl A.5.15 (Control de acceso)
- SoAItem 00 -> Project 0 + A.8.
- SoAItem 00 -> Project + A.8.
- SoAItem 00 -> Project + A.8.
- ... (un SoAItem por proyecto)

Total SoAItems para A.8.: número_de_proyectos (N)
Total SoAItems en BD: 93 controles x N proyectos
```

---

## Relaciones Self (Autoreferencia)

### . EVIDENCE (1) <-> (N) EVIDENCE (Versionado)

**Descripcion**: Una version de Evidence apunta a su version anterior (self-reference). Crea cadena historica.

**Cardinalidad**:
```
Evidence (self) --previous_version--> Evidence

Restricción:
- Versión : previous_version = NULL
- Versión 1: previous_version = NULL
- Versión n: previous_version = Versión n-1
- Cadena: v1 -> v2 -> v3 -> ... -> vN (current)
```

**Implementacion**:
```python
class Evidence(Model):
 project = ForeignKey(Project, on_delete=CASCADE)
 name = CharField()
 file = FileField()
 version = IntegerField(default=)
 previous_version = ForeignKey(
 'self',
 on_delete=SET_NULL,
 null=True,
 related_name='next_versions'
 )
 is_current = BooleanField(default=True)

# Metodo para crear nueva version
def create_new_version(self, file, user):
 # Marcar version actual como historica
 self.is_current = False
 self.save()

 # Crear nueva version
 new = Evidence.objects.create(
 project=self.project,
 name=self.name,
 file=file,
 version=self.version + ,
 previous_version=self,
 is_current=True,
 uploaded_by=user
 )
 return new
```

**Ejemplo de Cadena**:
```
Evidence «MFA Configuration»
- Versión 1 (created_at: 2024-01-01)
	- file: mfa_v1.pdf
	- previous_version: NULL
	- status: APPROVED
	- is_current: False

- Versión 2 (created_at: 2024-02-01) <= CURRENT
	- file: mfa_v2.pdf
	- previous_version: Versión 1
	- status: PENDING
	- is_current: True

Historial completo:
evidence.previous_version # Versión anterior (v)
evidence.previous_version.previous_version # v
evidence.next_versions.all() # (Versiones posteriores)
```

---

## Diagrama Completo de Relaciones

```
VIT COMPLETE RELATIONSHIP DIAGRAM

COMPANY 1 -- (N) PROJECT (hub)
USER 1 --created_by--> (N) PROJECT

PROJECT 1 -- (N) PHASE -- (N) TASK
PROJECT 1 -- (N) RISK -- (N:M) ASSET
RISK (N:M) ISOCONTROL

PROJECT 1 -- (N) SOAITEM -- (1) ISOCONTROL
PROJECT 0..N -- (N) DOCUMENT (optional project_id)
PROJECT 1 -- (N) EVIDENCE -- (self) previous_version

USER 1 -- (N) EVIDENCE (uploaded_by)
USER 0..N -- (N) EVIDENCE (approved_by)
USER 0..N -- (N) AUDITLOG

LEGEND: -> Foreign Key (one-way), N:M Many-to-Many
```
- RISK se mitiga via N:M ISOCONTROL
- SOAITEM vincula PROJECT x ISOCONTROL (generado automatico)
- EVIDENCE es versionado (self-reference)
- USER no esta en diagrama pero FK subyacentes: created_by, assigned_to, owner, uploaded_by, etc.
- AUDITLOG rastrea cambios en User, Risk, Evidence, Project, etc.

---

## Restricciones Referenciales

### Tipos de ON DELETE

```sql
-- RESTRICT: No permite eliminar si hay referencias
FOREIGN KEY (parent_id) REFERENCES parent(id) ON DELETE RESTRICT;
Ejemplo: No puedes eliminar un User si esta assigned_to tasks

-- CASCADE: Elimina automáticamente registros dependientes
FOREIGN KEY (project_id) REFERENCES project(id) ON DELETE CASCADE;
Ejemplo: Si eliminas Project -> se eliminan Phase, Risk, Asset, etc.

-- SET_NULL: Pone NULL la FK si se elimina padre
FOREIGN KEY (created_by_id) REFERENCES user(id) ON DELETE SET_NULL;
Ejemplo: Si eliminas User -> created_by de sus proyectos queda NULL

-- SET_DEFAULT: Pone valor por defecto
-- (menos comun, no usamos en VIT)
```

### Mapeo VIT

| FK | Tabla Padre | ON DELETE | Razon |
|---|---|---|---|
| `project.company_id` | Company | CASCADE | Empresa eliminada -> todos sus proyectos se van |
| `project.created_by_id` | User | SET_NULL | User eliminado, proyecto se mantiene (historico) |
| `phase.project_id` | Project | CASCADE | Proyecto eliminado -> fases se van |
| `task.phase_id` | Phase | CASCADE | Fase eliminada -> tareas se van |
| `risk.project_id` | Project | CASCADE | Proyecto eliminado -> riesgos se van |
| `asset.project_id` | Project | CASCADE | Proyecto eliminado -> assets se van |
| `soaitem.project_id` | Project | CASCADE | Proyecto eliminado -> SoA Items se van |
| `soaitem.iso_control_id` | ISOControl | PROTECT | Control ISO es inmutable, no se elimina |
| `evidence.project_id` | Project | CASCADE | Proyecto eliminado -> evidencias se van |
| `evidence.uploaded_by_id` | User | SET_NULL | User eliminado, evidencia se mantiene |
| `evidence.approved_by_id` | User | SET_NULL | Approver eliminado, se registra NULL |
| `evidence.previous_version_id` | Evidence | SET_NULL | Version anterior eliminada, referencia se limpia |
| `auditlog.user_id` | User | SET_NULL | User eliminado, auditlog se mantiene (historico) |
| `document.project_id` | Project | CASCADE | Proyecto eliminado -> documentos generados se van |

---

## Cascadas de Eliminacion

### Escenario: Eliminar una Empresa

```
DELETE FROM company WHERE id = <id>;
CASCADE: Elimina todos los proyectos de company
 DELETE FROM project WHERE company_id = <id>;
CASCADE: Para cada proyecto eliminado:
 DELETE FROM phase WHERE project_id IN (...);
 DELETE FROM risk WHERE project_id IN (...);
 DELETE FROM asset WHERE project_id IN (...);
 DELETE FROM soaitem WHERE project_id IN (...);
 DELETE FROM evidence WHERE project_id IN (...);
 DELETE FROM document WHERE project_id IN (...);
CASCADE: Para cada fase/tarea/etc:
 DELETE FROM task WHERE phase_id IN (...);
CASCADE: Para cada riesgo:
 DELETE FROM risk_asset WHERE risk_id IN (...);
 DELETE FROM risk_mitigating_controls WHERE risk_id IN (...);
RESULTADO FINAL:
- Company : DELETED
- Projects (all): DELETED
- Phases, Tasks, Risks, Assets, SoA, Evidence, Documents: DELETED
- Intermediate tables (risk_asset, risk_mitigating_controls): CLEANED
- AuditLog, User: UNCHANGED (pero referencias a company OK)
```

### Escenario: Eliminar un Proyecto

```
DELETE FROM project WHERE id = <id>;
CASCADE:
 DELETE FROM phase WHERE project_id = <id>;
 DELETE FROM risk WHERE project_id = <id>;
 DELETE FROM asset WHERE project_id = <id>;
 DELETE FROM soaitem WHERE project_id = <id>;
 DELETE FROM evidence WHERE project_id = <id>;
 DELETE FROM document WHERE project_id = <id>;
CASCADE: Para cada phase/risk/etc:
 DELETE FROM task WHERE phase_id IN (...);
 DELETE FROM risk_asset WHERE risk_id IN (...);
 DELETE FROM risk_mitigating_controls WHERE risk_id IN (...);
```

---

## Ejemplo de Flujo de Datos

### Caso: Implementacion de ISO 27001 para Empresa Consultec

```
- CREACION DEL PROYECTO
 Admin crea:
 - Company (Consultec S.A.S.)
 - User (Carlos - CONSULTANT, Maria - CLIENT de Consultec)
 - Project (name=«ISO 27001», created_by=Carlos)

- SIGNAL AUTOMATICO
 Al crear Project:
 - Sistema crea Phases (INIT, PLAN, IMPLEMENT, MAINTAIN, CERTIFY)
 - Sistema crea 93 SoAItems (una por control ISO)
 - Cada SoAItem.is_applicable = True (pendiente de valoracion)

- ASSESSMENT PHASE (Carlos - CONSULTANT)
 Carlos identifica:
 - Assets:
	 - BD PostgreSQL (type=DATA, criticality=CRITICAL, CIA=5,5,5)
	 - Web Server (type=HARDWARE, criticality=HIGH, CIA=4,4,4)
 - Risks:
	 - Risk: «Exposicion BD clientes»
		 - inherent: L=5, I=5 (score=25, INTOLERABLE)
		 - affected_assets: BD, API
		 - treatment=MITIGATE
		 - mitigating_controls: A.5.15, A.6.3, A.8.15, A.8.16, A.8.24, A.8.28
	 - Risk: «Malware infection»
		 - inherent: L=4, I=4 (score=16)
		 - mitigating_controls: A.6.3, A.8.15, A.8.16

- PLANNING PHASE (Carlos)
 Carlos evalua por cada Risk:
 - Define mitigacion
 - Ajusta residual likelihood/impact
 - Revisa SoAItems (marca no aplicables)

 Ejemplo para Risk «Exposicion BD clientes»:
 - residual_likelihood = 2 (MFA + encryption)
 - residual_impact = 5
 - residual_score = 10 (TOLERABLE)
 - risk_reduction = 25 - 10 = 15

 SoAItem A.8.1:
 - is_applicable = true
 - implementation_status = NOT_IMPLEMENTED
 - mitigation_plan = «Implement MFA for all user logins»

- IMPLEMENTATION PHASE (Maria - CLIENT)
 Maria carga evidencias:
 - Evidence: «MFA Configuration»
	 - file: mfa_config_v1.pdf
	 - iso_control = A.8.1
	 - uploaded_by = Maria
	 - status = PENDING
 - Evidence: «Encryption Certificate»
	 - file: encryption_cert_v1.pdf
	 - iso_control = A.8.2
	 - uploaded_by = Maria
	 - status = PENDING

- REVIEW & APPROVAL (Carlos - CONSULTANT)
 Carlos revisa evidencias:
 - Evidence (MFA): status PENDING -> APPROVED
 - Evidence (Encryption): status PENDING -> APPROVED
 - Evidence (insufficient):
 - status: PENDING -> REJECTED
 - approved_by = Carlos

7. EVIDENCE VERSIONING
 Maria corrects rejected evidence:
 - Evidence (Upload corrected version):
 ", - name = mismo que Evidence (old)
 ", - version =
 ", - previous_version = Evidence (old)
 ", - is_current = True
 ", - status = PENDING (requiere reaprobacion)
 ", - created_at = 0-0-7 09:00
 ",
 - Evidence (old, v):
 - version =
 - is_current = False
 - (mantiene status = REJECTED para historial)

8. SOAITEM UPDATE
 Cuando Evidence es aprobada:
 - Sistema busca: SoAItem WHERE iso_control=A.8.
 - Actualiza: implementation_status = IN_PROGRESS
 - Si todos controles tienen evidencia: implementation_status = IMPLEMENTED
 ",
 Ejemplo:
 - SoAItem 00 (A.8.): APPROVED evidence -> implementation_status = IMPLEMENTED
 - SoAItem 0(A.8.): APPROVED evidence -> implementation_status = IMPLEMENTED
 - SoAItem 0(A.8.): Sin evidencia -> implementation_status = NOT_IMPLEMENTED
 ",
 Dashboard:
 - Implemented controls: 7/9(8.%)
 - In Progress: /9(8.%)
 - Not Started: /9(.%)

9. AUDIT TRAIL
 Sistema automáticamente registra:
 - AuditLog : action=CREATE, model_name=Project, user=Admin, timestamp=0-0-
 - AuditLog : action=CREATE, model_name=Risk, user=Carlos, timestamp=0-0-0, changes={«name»: «Exposicion BD clientes», «inherent_likelihood»: , ...}
 - AuditLog : action=UPDATE, model_name=Risk, user=Carlos, timestamp=0-0-0, changes={«residual_likelihood»: {«before»: null, «after»: }, ...}
 - AuditLog : action=CREATE, model_name=Evidence, user=Maria, timestamp=0-0-
 - AuditLog : action=APPROVE, model_name=Evidence, user=Carlos, timestamp=0-0-, changes={«status»: {«before»: «PENDING», «after»: «APPROVED»}}
 - ... (mas audits)
 ",
 Auditor Externo puede revisar:
 - quien hizo que
 - Cuando exactamente
 - Antes y despues de cambios
 - Donde (IP address)
 - Desde que cliente (user_agent)

0. FINAL REPORT
 Carlos genera documento final:
 - Document (type=SOA, project=Project 0)
 - file: SoA_Report_Final_0-0-.pdf
 - version =
 - generated_by = Carlos
 ",
 - Contiene: 93 controles, 7 aplicables, 7 implementados, en progreso, no iniciados
```

---

**Documento preparado por el equipo VIT**
**Última revision**: de febrero de 0
**Proximo paso**: Implementación de modelos en Django
