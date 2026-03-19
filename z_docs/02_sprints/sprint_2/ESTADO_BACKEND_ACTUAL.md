# Estado Actual del Backend - Sprint 2

**Fecha**: March 16, 2026  
**Objetivo**: Baseline para implementación Día 1-10  

---

## ✅ Qué YA Existe

### Modelos Base Implementados

| Modelo | Ubicación | Estado | Campos Base |
|--------|-----------|--------|------------|
| **Contact** | `backend/apps/contacts/models.py` | ✅ Completo | company, user, full_name, email, phone, position, is_active, timestamps |
| **ProjectContact** | `backend/apps/projects/models.py` | ✅ Completo | project, contact, contact_role, is_primary, timestamps |
| **Document** | `backend/apps/documents/models.py` | ✅ Completo | project, phase, task, title, doc_type, status, file, version, approved_by, approved_at, timestamps |
| **Asset** | `backend/apps/assets/models.py` | ✅ Completo | (con migraciones 0001, 0002) |
| **Project** | `backend/apps/projects/models.py` | ✅ Completo | (con relaciones a Contact, ProjectUser) |
| **Phase** | `backend/apps/phases/models.py` | ✅ Completo | |
| **Task** | `backend/apps/tasks/models.py` | ✅ Completo | |
| **User** | `backend/apps/users/models.py` | ✅ Completo | (con AuditLog) |
| **Company** | `backend/apps/companies/models.py` | ✅ Completo | |

### API Endpoints Existentes

```
✅ /api/users/
✅ /api/audit-logs/
✅ /api/companies/
✅ /api/projects/
✅ /api/project-users/
✅ /api/project-contacts/
✅ /api/phases/
✅ /api/tasks/
✅ /api/contacts/
✅ /api/documents/
✅ /api/assets/
✅ /api/token/ (JWT)
✅ /api/token/refresh/
```

### Migraciones Aplicadas

```
users/           → 0001, 0002, 0003 ✅
companies/       → 0001, 0002 ✅
projects/        → 0001, 0002, 0003 ✅
phases/          → 0001, 0002 ✅
tasks/           → 0001, 0002 ✅
contacts/        → 0001 ✅
documents/       → 0001 ✅
assets/          → 0001, 0002 ✅
```

### Validaciones Implementadas

**Contact:**
- ✅ Constraint único: (company, email)
- ✅ ValidationError si se vincula user incorrectamente
- ✅ Related_name bien configurados

**ProjectContact:**
- ✅ Unique_together: ['project', 'contact']
- ✅ Validación en clean(): contact.company == project.company
- ✅ Validación en save(): llama full_clean()

**Document:**
- ✅ Validación en clean(): phase.project == document.project
- ✅ Validación: documento aprobado requiere approved_by + approved_at

---

## ⚠️ Qué FALTA para Sprint 2

### Día 1-2: Campos Faltantes en Modelos Existentes

**Contact** - Necesita:
```python
work_notes = models.TextField(blank=True, null=True)  # Para Día 2 (Osky)
```

**ProjectContact** - Necesita:
```python
work_notes = models.TextField(blank=True, null=True)  # Para Día 2 (Osky)
```

**Document** - Necesita:
```python
planned_date = models.DateField(null=True, blank=True)   # Para Día 1 (Osky)
actual_date = models.DateField(null=True, blank=True)    # Para Día 1 (Osky)
```

### Día 3-4: Migraciones

**Debe crearse migración** en cada app:
- `contacts/migrations/0002_contact_work_notes.py`
- `projects/migrations/0004_projectcontact_work_notes.py`
- `documents/migrations/0002_add_planned_actual_dates.py`

### Día 4: Serializers/Viewsets

**Contact/ProjectContact serializers:**
```python
# Actualmente existen pero necesitan:
- Actualizar para incluir work_notes
- Validación de unicidad (company, email) en serializer
```

**Document serializer:**
```python
# Necesita:
- Incluir planned_date, actual_date
- Validación de relaciones (phase.project == project, etc.)
```

### Día 6-7: Documentación + Deploy

**Documentos nuevos a crear:**
- `SISTEMA_FLUJO_COMPLETO.md` (modelo + procesos)
- `MODELO_DATOS_REFERENCIA.md` (persistencia)
- `FLUJO_UI_CASOS_USO.md` (frontend)
- `POSTGRESQL_SETUP_SCRIPT.sql` (deploy)
- `POSTGRESQL_DEPLOYMENT_GUIDE.md` (paso a paso)

**Config actualizar:**
- `.env.example` finalizar
- `requirements.txt` auditar
- Instrucciones PostgreSQL

---

## 🎬 Acción para Hoy (Día 1 - March 16)

### Juan Jose Jimenez Guardo (Backend core - Contact)

**Revisar:**
1. ✅ Contact model actual en `backend/apps/contacts/models.py`
2. ✅ Validaciones existentes
3. ⚠️ Identificar si ContactFormulario o casos especiales necesitan ajustes

**Preparar para mañana:**
- Documentar qué constraints hacen falta (si alguno)
- Validar que Contact esté "listo" para Día 2

---

### Osky (Backend persistencia - Migraciones)

**Revisar:**
1. ✅ Estado actual de migraciones (`python manage.py showmigrations`)
2. ⚠️ Campos faltantes:
   - Add `work_notes` a Contact
   - Add `work_notes` a ProjectContact
   - Add `planned_date`, `actual_date` a Document
3. Preparar estructura de migraciones

**Tareas Día 1:**
- Actualizar modelos Contact, ProjectContact, Document con campos faltantes
- Crear migraciones (pero NO ejecutar aún - Día 3-4)

---

### Luis (Frontend - Congelar vistas)

**Revisar:**
1. ¿Qué pantallas nuevas existen para Contact, ProjectContact, Document?
2. ¿Cuáles cumplen contrato con backend?
3. ¿Cuáles necesitan actualizarse por cambios BD?

**Día 1:**
- Documentar el impacto que el cambio Contact/ProjectContact/Document tendrá en UI
- Preparar lista de componentes que necesitan update

---

## 📊 Resumen Visual

```
Modelo              Existe?   API?   Serializer?  Campos OK?  Migración?
────────────────────────────────────────────────────────────────────
Contact             ✅        ✅     ✅           ⚠️ +work_notes   ✅
ProjectContact      ✅        ✅     ✅           ⚠️ +work_notes   ✅
Document            ✅        ✅     ✅           ⚠️ +dates        ✅
Asset               ✅        ✅     ✅           ✅              ✅
Project             ✅        ✅     ✅           ✅              ✅
Phase               ✅        ✅     ✅           ✅              ✅
Task                ✅        ✅     ✅           ✅              ✅
User                ✅        ✅     ✅           ✅              ✅
Company             ✅        ✅     ✅           ✅              ✅
```

---

## 📍 Próximos Pasos

**Inmediato (HOY):**
```bash
cd backend
python manage.py showmigrations  # Ver estado
python manage.py test            # Verificar que todo funciona
```

**Mañana (Día 2):**
- Ejecutar modelo Contact y ProjectContact updates
- Crear migraciones
- Validar constraints

**Días 3-10:**
- Seguir plan SPRINT2_PLAN_AJUSTADO_v2.md

---

## 📎 Referencias

- Modelos: `backend/apps/*/models.py`
- Migraciones: `backend/apps/*/migrations/`
- Config: `backend/config/settings/`
- ERD Vigente: `z_docs/01_architecture/Plataforma ISO 27001 SGSI - ERD PostgreSQL_2.jpg`
- Plan Ajustado: `z_docs/02_sprints/sprint_2/SPRINT2_PLAN_AJUSTADO_v2.md`
