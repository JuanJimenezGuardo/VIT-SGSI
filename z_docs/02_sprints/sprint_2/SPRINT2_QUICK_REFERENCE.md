# 🚀 Sprint 2 - Quick Reference Card

**Imprime esto y tenlo cerca durante Sprint 2** 📄

---

## 📅 Cronograma Sprint 2 (11-24 Marzo)

```
Semana 1 (11-15 mar):
  Lunes 11:    Modelos (Risk, ISOControl, SoAItem)
  Martes 12:   Serializers + ViewSets
  Miércoles 13:Populate ISO Controls
  Jueves 14:   Tests Riesgos
  Viernes 15:  Tests SoA + Polish

Semana 2 (18-24 mar):
  Lunes 18:    Risk Matrix + Filtering
  Martes 19:   SoA Dashboard Endpoints
  Miércoles 20:Documentation
  Jueves 21:   Integration Tests
  Viernes 22-24:Buffer + Bug Fixes
```

---

## 📁 Archivos a Crear

```
backend/
├── apps/risks/                 # Nueva app
│   ├── __init__.py
│   ├── admin.py               ← Copiar de SPRINT2_CODIGO_READY_TO_COPY.md
│   ├── apps.py
│   ├── models.py              ← Copiar de SPRINT2_CODIGO_READY_TO_COPY.md
│   ├── serializers.py         ← Copiar de SPRINT2_CODIGO_READY_TO_COPY.md
│   ├── views.py               ← Copiar de SPRINT2_CODIGO_READY_TO_COPY.md
│   ├── tests.py               ← Copiar de SPRINT2_CODIGO_READY_TO_COPY.md
│   ├── urls.py                (opcional, routing en config/urls.py)
│   └── migrations/
│       └── __init__.py
│
└── populate_iso_controls.py   ← Copiar script
```

---

## ⚡ 10 Comandos Clave

```bash
# 1. Crear app
python manage.py startapp risks

# 2. Después de models.py
python manage.py makemigrations risks
python manage.py migrate

# 3. Verificar
python manage.py check

# 4. Populate ISO (después de migración)
python populate_iso_controls.py

# 5. Tests
python manage.py test apps.risks

# 6. Tests verbose
python manage.py test apps.risks -v 2

# 7. Cobertura
coverage run --source='apps.risks' manage.py test
coverage report

# 8. Admin
python manage.py createsuperuser  # Si no existe

# 9. Run server
python manage.py runserver

# 10. Shell (debug)
python manage.py shell
```

---

## 📊 3 Modelos Principales

### 1. Risk
```
proyecto → título → descripción →
likelihood (LOW/MEDIUM/HIGH/CRITICAL)
impact (LOW/MEDIUM/HIGH/CRITICAL)
scores (1-5) → risk_score automático
status → IDENTIFIED/ANALYZING/MITIGATING/MITIGATED/CLOSED
mitigacion_plan
```

### 2. ISOControl
```
A.5.1.1 → "Policies for information security"
A.5.1.2 → "Information security policy review"
...
A.18.2.3
(50+ controles del Annex A)
```

### 3. SoAItem
```
proyecto + control (único) →
¿Aplicable? → APPLICABLE/NOT_APPLICABLE/PARTIALLY
status → PLANNED/IMPLEMENTED/REVIEWED/APPROVED
evidence_file
responsible
target_completion
```

---

## ✅ Endpoints Resultantes

### Risks
```
GET    /api/risks/
POST   /api/risks/
GET    /api/risks/{id}/
PUT    /api/risks/{id}/
DELETE /api/risks/{id}/
GET    /api/risks/high_risk/
GET    /api/risks/matrix/
GET    /api/risks/statistics/
POST   /api/risks/{id}/mark_mitigated/
```

### ISO Controls
```
GET    /api/iso-controls/
GET    /api/iso-controls/{id}/
GET    /api/iso-controls/by_domain/
GET    /api/iso-controls/all_domains/
```

### SoA Items
```
GET    /api/soa-items/
POST   /api/soa-items/
GET    /api/soa-items/{id}/
PUT    /api/soa-items/{id}/
POST   /api/soa-items/generate_soa/
GET    /api/soa-items/compliance_summary/
```

---

## 🧪 Testing Checklist

- [ ] Risk score = likelihood_score * impact_score
- [ ] No risk_score > 25
- [ ] Admin ve todos los riesgos
- [ ] Consultant ve solo asignados
- [ ] high_risk filtra >= 15
- [ ] matrix devuelve {likelihood x impact}
- [ ] statistics calcula average, critical
- [ ] generate_soa crea items para todos controles
- [ ] SoA items son únicos (project, control)
- [ ] compliance_summary calcula %

---

## 🔗 Relaciones de Modelos

```
Project 1:N Risk
Project 1:N SoAItem
ISOControl 1:N SoAItem
User 1:N Risk (created_by)
User N:1 Risk (owner)
User N:1 SoAItem (responsible)
```

---

## 📋 Migración Paso a Paso

### 1. Setup (30 min)
```bash
python manage.py startapp risks
# Copiar models.py, serializers.py, views.py, admin.py
python manage.py makemigrations risks
python manage.py migrate
python manage.py check  # 0 issues
```

### 2. Populate (10 min)
```bash
python populate_iso_controls.py
# Verifica: python manage.py dbshell
# SELECT COUNT(*) FROM risks_isocontrol;
# Should be: 50+
```

### 3. Wire up Router (5 min)
```python
# config/urls.py
router.register(r'risks', RiskViewSet)
router.register(r'iso-controls', ISOControlViewSet)
router.register(r'soa-items', SoAItemViewSet)
```

### 4. Test (30 min)
```bash
python manage.py test apps.risks
# All tests passing
```

---

## 📚 Archivos de Referencia

| Archivo | Contenido |
|---------|-----------|
| `SPRINT2_BACKLOG_DETALLADO.md` | Plan día a día, arquitectura |
| `SPRINT2_CODIGO_READY_TO_COPY.md` | Código completo para copiar/pegar |
| `SPRINT2_QUICK_REFERENCE.md` | Este archivo (resumen) |

---

## 🎯 Success Criteria

Sprint 2 está completo cuando:

- ✅ 3 modelos creados + migrados
- ✅ 15+ endpoints implementados
- ✅ 25+ tests pasando
- ✅ 80%+ cobertura
- ✅ 50+ ISO controles en BD
- ✅ `python manage.py check` = 0 issues
- ✅ Documentación actualizada

---

## 🐛 Debugging Rápido

```python
# python manage.py shell
from apps.risks.models import Risk, ISOControl, SoAItem

# Ver totales
Risk.objects.count()
ISOControl.objects.count()
SoAItem.objects.count()

# Ver por proyecto
Risk.objects.filter(project_id=1)

# Ver risk_score
Risk.objects.filter(risk_score__gte=15)

# Debuggear queries
from django.db import connection
connection.queries
```

---

## 💡 Tips Profesionales

1. **Copiar código de SPRINT2_CODIGO_READY_TO_COPY.md exactamente**
   - No improvisees, usa blueprint probado

2. **Migrate después de cada modelo**
   - No esperes final, test inmediatamente

3. **Populate ISO antes de tests**
   - Los tests necesitan controles en BD

4. **Usar fixtures si necesario**
   - Para tests reproducibles

5. **Documentar mientras codeas**
   - Mantener API_ENDPOINTS.md actualizado

---

## 🚨 Errores Comunes

### Error: "No app named 'risks'"
```bash
# Olvidaron registrar en settings
# INSTALLED_APPS = ['apps.risks', ...]
```

### Error: "SyntaxError en models.py"
```bash
# Copiar exactamente del archivo CODIGO_READY_TO_COPY.md
# No modificar indentación
```

### Error: "Integrity Error" en populate
```bash
# ISO controls ya existen
# python manage.py shell
# ISOControl.objects.all().delete()
# python populate_iso_controls.py
```

### Error: Tests no encuentran models
```bash
# Olvidaron migraciones
python manage.py makemigrations risks
python manage.py migrate
```

---

## 📞 Recursos Rápidos

- `SPRINT2_BACKLOG_DETALLADO.md` - Plan completo
- `SPRINT2_CODIGO_READY_TO_COPY.md` - Código para copiar
- `API_ENDPOINTS.md` - Documentación API
- `PREGUNTAS_FRECUENTES_SPRINT1.md` - Debugging patterns

---

## ⏱️ Estimación Realista

| Tarea | Tiempo |
|-------|--------|
| Setup + Models | 2 horas |
| Serializers + Views | 2 horas |
| Populate + Router | 1 hora |
| Tests básicos | 3 horas |
| Endpoints avanzados | 2 horas |
| Documentation | 1.5 horas |
| Debugging + Buffer | 2 horas |
| **TOTAL** | **13.5 horas** |

---

## 🏁 Antes de Terminar Sprint 2

```bash
# Final verification
python manage.py check           # ✅ 0 issues
python manage.py test apps.risks # ✅ All passing
python manage.py test            # ✅ No regressions
curl -X GET http://localhost:8000/api/iso-controls/ # ✅ 200 OK
```

---

## 🎬 Ready?

1. ✅ Leíste `SPRINT2_BACKLOG_DETALLADO.md` (20 min)
2. ✅ Copiaste código de `SPRINT2_CODIGO_READY_TO_COPY.md`
3. ✅ Ejecutaste migrate + populate
4. ✅ Todos los tests en verde

→ **Vas a tener Sprint 2 listo en 2 semanas** 🚀

---

*Sprint 2: 11-24 Marzo*  
*Objetivo: +20 endpoints + 50 ISO controles + 25 tests*
