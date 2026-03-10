# 🎯 Sprint 2 - Backlog Detallado: Gestión de Riesgos e ISO Controles

**Duración:** 2 semanas (11-24 marzo)  
**Objetivo:** Implementar gestión completa de riesgos y mapeo de controles ISO 27001  
**Entregable:** API fully functional con 20+ nuevos endpoints  

---

## 📋 Resumen de Tareas

| # | Tarea | Días | Prioridad | Status |
|----|-------|------|-----------|--------|
| 1 | Modelo Risk | 1 | 🔴 Critical | ⏳ TODO |
| 2 | Modelo ISOControl | 1 | 🔴 Critical | ⏳ TODO |
| 3 | Modelo SoAItem | 1 | 🔴 Critical | ⏳ TODO |
| 4 | Endpoints CRUD Risk | 0.5 | 🟡 High | ⏳ TODO |
| 5 | Endpoints CRUD ISOControl | 0.5 | 🟡 High | ⏳ TODO |
| 6 | Endpoints CRUD SoAItem | 0.5 | 🟡 High | ⏳ TODO |
| 7 | Tests para Riesgos | 1 | 🟡 High | ⏳ TODO |
| 8 | Tests para Controles | 1 | 🟡 High | ⏳ TODO |
| 9 | SoA Generator | 1 | 🟡 High | ⏳ TODO |
| 10 | Risk filtering/búsqueda | 0.5 | 🟢 Medium | ⏳ TODO |
| 11 | Dashboard API endpoints | 1 | 🟢 Medium | ⏳ TODO |
| 12 | Documentation | 1 | 🟢 Medium | ⏳ TODO |

**Total tiempo estimado:** 10 días = 2 semanas ✅

---

## 📅 Plan Día a Día

### **SEMANA 1 (11-15 marzo)**

#### ✅ Día 1 (11 marzo) - Modelado de Datos
**Tarea:** Crear 3 modelos Django principales

**Horas:** 4-5 horas

**Checklist:**
- [ ] Crear app `risks/` con `python manage.py startapp risks`
- [ ] Implementar modelo `Risk`
- [ ] Implementar modelo `ISOControl`
- [ ] Crear migraciones
- [ ] Registrar en admin

**Código a escribir:**

```python
# apps/risks/models.py

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Risk(models.Model):
    """Modelo de gestión de riesgos de proyecto"""
    
    LIKELIHOOD_CHOICES = [
        ('LOW', 'Baja'),
        ('MEDIUM', 'Media'),
        ('HIGH', 'Alta'),
        ('CRITICAL', 'Crítica'),
    ]
    
    IMPACT_CHOICES = [
        ('LOW', 'Bajo'),
        ('MEDIUM', 'Medio'),
        ('HIGH', 'Alto'),
        ('CRITICAL', 'Crítico'),
    ]
    
    STATUS_CHOICES = [
        ('IDENTIFIED', 'Identificado'),
        ('ANALYZING', 'Analizando'),
        ('MITIGATING', 'Mitigando'),
        ('MITIGATED', 'Mitigado'),
        ('CLOSED', 'Cerrado'),
    ]
    
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='risks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Análisis de riesgo
    likelihood = models.CharField(max_length=20, choices=LIKELIHOOD_CHOICES)
    impact = models.CharField(max_length=20, choices=IMPACT_CHOICES)
    
    # Valores númericos (1-5)
    likelihood_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    impact_score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    
    # Cálculo automático: risk_score = likelihood_score * impact_score
    risk_score = models.IntegerField(read_only=True)
    
    # Mitigación
    mitigation_plan = models.TextField(blank=True, null=True)
    mitigating_controls = models.TextField(
        help_text="Controles ISO que mitigan este riesgo"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='IDENTIFIED'
    )
    
    owner = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_risks'
    )
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='created_risks'
    )
    
    class Meta:
        ordering = ['-risk_score', '-created_at']
        verbose_name_plural = "Risks"
    
    def save(self, *args, **kwargs):
        # Calcular risk_score automáticamente
        self.risk_score = self.likelihood_score * self.impact_score
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.title} (Score: {self.risk_score})"


class ISOControl(models.Model):
    """Controles ISO 27001 - Referencia de Annex A"""
    
    # Ejemplo: A.5.1.1, A.5.2.1, etc.
    control_code = models.CharField(max_length=20, unique=True)
    control_name = models.CharField(max_length=255)
    description = models.TextField()
    
    # Dominio (A.5, A.6, A.7, etc.)
    domain = models.CharField(max_length=5)  # "A.5", "A.6", etc.
    
    # Información adicional
    references = models.TextField(
        blank=True,
        help_text="Referencias normativas o documentos relacionados"
    )
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['control_code']
        verbose_name_plural = "ISO Controls"
    
    def __str__(self):
        return f"{self.control_code} - {self.control_name}"


class SoAItem(models.Model):
    """Statement of Applicability - Aplicabilidad de controles por proyecto"""
    
    APPLICABILITY_CHOICES = [
        ('APPLICABLE', 'Aplicable'),
        ('NOT_APPLICABLE', 'No Aplicable'),
        ('PARTIALLY_APPLICABLE', 'Parcialmente Aplicable'),
    ]
    
    STATUS_CHOICES = [
        ('PLANNED', 'Planificado'),
        ('IMPLEMENTED', 'Implementado'),
        ('REVIEWED', 'Revisado'),
        ('APPROVED', 'Aprobado'),
    ]
    
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='soa_items'
    )
    
    control = models.ForeignKey(
        ISOControl,
        on_delete=models.CASCADE,
        related_name='soa_items'
    )
    
    # Aplicabilidad
    is_applicable = models.CharField(
        max_length=20,
        choices=APPLICABILITY_CHOICES,
        default='APPLICABLE'
    )
    
    applicability_justification = models.TextField(
        blank=True,
        help_text="Por qué es/no es aplicable"
    )
    
    # Implementación
    implementation_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PLANNED'
    )
    
    current_state = models.TextField(
        help_text="Estado actual de implementación"
    )
    
    planned_action = models.TextField(
        blank=True,
        help_text="Acciones planeadas"
    )
    
    responsible = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='soa_items'
    )
    
    target_completion = models.DateField(null=True, blank=True)
    
    # Evidence
    evidence_file = models.FileField(
        upload_to='soa_evidence/',
        blank=True,
        null=True
    )
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('project', 'control')
        ordering = ['control__control_code']
    
    def __str__(self):
        return f"{self.project.name} - {self.control.control_code}"
```

**Después crear migrations:**
```bash
python manage.py makemigrations risks
python manage.py migrate
```

**Verificar:**
- [ ] `python manage.py check` pasa (0 issues)
- [ ] Models aparecen en admin
- [ ] Migraciones creadas sin errores

---

#### ✅ Día 2 (12 marzo) - Serializers y ViewSets

**Tarea:** Crear DRF serializers y viewsets para los 3 modelos

**Horas:** 3-4 horas

**Checklist:**
- [ ] Crear `RiskSerializer`
- [ ] Crear `ISOControlSerializer`
- [ ] Crear `SoAItemSerializer`
- [ ] Crear `RiskViewSet`
- [ ] Crear `ISOControlViewSet`
- [ ] Crear `SoAItemViewSet`
- [ ] Registrar en router

**Código:**

```python
# apps/risks/serializers.py

from rest_framework import serializers
from apps.risks.models import Risk, ISOControl, SoAItem

class RiskSerializer(serializers.ModelSerializer):
    project_name = serializers.CharField(source='project.name', read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    
    class Meta:
        model = Risk
        fields = [
            'id', 'project', 'project_name', 'title', 'description',
            'likelihood', 'impact', 'likelihood_score', 'impact_score',
            'risk_score', 'mitigation_plan', 'mitigating_controls',
            'status', 'owner', 'owner_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['risk_score', 'created_at', 'updated_at']
    
    def validate(self, data):
        if data.get('likelihood_score') and data.get('impact_score'):
            if data['likelihood_score'] * data['impact_score'] > 20:
                raise serializers.ValidationError(
                    "Risk score excede límite permitido (5x5)"
                )
        return data


class ISOControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = ISOControl
        fields = [
            'id', 'control_code', 'control_name', 'description',
            'domain', 'references', 'is_active'
        ]


class SoAItemSerializer(serializers.ModelSerializer):
    control_code = serializers.CharField(source='control.control_code', read_only=True)
    control_name = serializers.CharField(source='control.control_name', read_only=True)
    project_name = serializers.CharField(source='project.name', read_only=True)
    responsible_name = serializers.CharField(
        source='responsible.get_full_name', read_only=True
    )
    
    class Meta:
        model = SoAItem
        fields = [
            'id', 'project', 'project_name', 'control', 'control_code',
            'control_name', 'is_applicable', 'applicability_justification',
            'implementation_status', 'current_state', 'planned_action',
            'responsible', 'responsible_name', 'target_completion',
            'evidence_file', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
```

```python
# apps/risks/views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.risks.models import Risk, ISOControl, SoAItem
from apps.risks.serializers import (
    RiskSerializer, ISOControlSerializer, SoAItemSerializer
)
from apps.users.permissions import IsAdminOrConsultant, IsProjectMember

class RiskViewSet(viewsets.ModelViewSet):
    serializer_class = RiskSerializer
    permission_classes = [IsAdminOrConsultant]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return Risk.objects.all()
        elif user.role == 'CONSULTANT':
            # Consultor ve riesgos de proyectos asignados
            return Risk.objects.filter(
                project__projectuser__user=user
            ).distinct()
        return Risk.objects.none()
    
    @action(detail=False, methods=['get'])
    def high_risk(self, request):
        """Filtra riesgos críticos (score >= 15)"""
        queryset = self.get_queryset().filter(risk_score__gte=15)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def mark_mitigated(self, request, pk=None):
        """Marca riesgo como mitigado"""
        risk = self.get_object()
        risk.status = 'MITIGATED'
        risk.save()
        return Response({'status': 'Risk marked as mitigated'})


class ISOControlViewSet(viewsets.ReadOnlyModelViewSet):
    """Vista de solo lectura para controles ISO (datos de referencia)"""
    queryset = ISOControl.objects.filter(is_active=True)
    serializer_class = ISOControlSerializer
    
    @action(detail=False, methods=['get'])
    def by_domain(self, request):
        """Agrupa controles por dominio (A.5, A.6, etc.)"""
        domain = request.query_params.get('domain')
        if domain:
            controls = ISOControl.objects.filter(domain=domain, is_active=True)
        else:
            controls = ISOControl.objects.filter(is_active=True)
        serializer = self.get_serializer(controls, many=True)
        return Response(serializer.data)


class SoAItemViewSet(viewsets.ModelViewSet):
    serializer_class = SoAItemSerializer
    permission_classes = [IsAdminOrConsultant]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'ADMIN':
            return SoAItem.objects.all()
        elif user.role == 'CONSULTANT':
            return SoAItem.objects.filter(
                project__projectuser__user=user
            ).distinct()
        return SoAItem.objects.none()
    
    @action(detail=False, methods=['post'])
    def generate_soa(self, request):
        """Genera automáticamente items de SoA para un proyecto"""
        project_id = request.data.get('project_id')
        if not project_id:
            return Response(
                {'error': 'project_id required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Obtener todos los controles ISO activos
        controls = ISOControl.objects.filter(is_active=True)
        
        # Crear SoA items para cada control
        soa_items = []
        for control in controls:
            item, created = SoAItem.objects.get_or_create(
                project_id=project_id,
                control=control,
                defaults={
                    'is_applicable': 'APPLICABLE',
                    'implementation_status': 'PLANNED'
                }
            )
            if created:
                soa_items.append(item)
        
        return Response({
            'created': len(soa_items),
            'message': f'{len(soa_items)} SoA items created successfully'
        })
```

```python
# config/urls.py (agregar a los routers existentes)

from apps.risks.views import RiskViewSet, ISOControlViewSet, SoAItemViewSet

router.register(r'risks', RiskViewSet, basename='risk')
router.register(r'iso-controls', ISOControlViewSet, basename='iso-control')
router.register(r'soa-items', SoAItemViewSet, basename='soa-item')
```

**Verificar:**
- [ ] `python manage.py check` pasa
- [ ] Endpoints en `/admin/` listados correctamente
- [ ] Curl a `GET /api/iso-controls/` devuelve 200

---

#### ✅ Día 3 (13 marzo) - Populate ISO Controls

**Tarea:** Cargar base de datos con 50+ controles ISO 27001

**Horas:** 2-3 horas

**Checklist:**
- [ ] Crear script `populate_iso_controls.py`
- [ ] Cargar todos los control codes del Annex A
- [ ] Verificar carga en admin

**Script:**

```python
# populate_iso_controls.py

from apps.risks.models import ISOControl

ISO_CONTROLS = [
    # A.5 - Organizational Controls
    ('A.5.1.1', 'Policies for information security', 'Establecimiento de políticas de seguridad', 'A.5'),
    ('A.5.1.2', 'Information security policy review and approval', 'Revisión y aprobación de políticas', 'A.5'),
    # ... Agregar todos los controles (ver documento oficial ISO 27001)
    
    # A.6 - People Controls
    ('A.6.1.1', 'Screening', 'Evaluación de antecedentes', 'A.6'),
    ('A.6.1.2', 'Terms and conditions of employment', 'Términos y condiciones laborales', 'A.6'),
    # ... etc
    
    # Copiar todo el Annex A aquí
]

def populate():
    for code, name, desc, domain in ISO_CONTROLS:
        ISOControl.objects.get_or_create(
            control_code=code,
            defaults={
                'control_name': name,
                'description': desc,
                'domain': domain,
                'is_active': True
            }
        )
    print(f"✅ {len(ISO_CONTROLS)} ISO controls loaded")

if __name__ == '__main__':
    populate()
```

**Ejecutar:**
```bash
python populate_iso_controls.py
```

---

#### ✅ Día 4 (14 marzo) - Tests para Riesgos

**Tarea:** Escribir comprehensive tests para Risk model y endpoints

**Horas:** 3-4 horas

**Checklist:**
- [ ] Test: Risk score calcula correctamente
- [ ] Test: Consultor solo ve sus riesgos
- [ ] Test: Admin ve todos los riesgos
- [ ] Test: high_risk endpoint filtra correctamente
- [ ] Test: mark_mitigated actualiza status

**Código:**

```python
# apps/risks/tests/test_risks.py

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.risks.models import Risk, ISOControl
from apps.users.models import User
from apps.companies.models import Company
from apps.projects.models import Project

class RiskModelTest(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Test Corp", rut="12345678-9")
        self.user = User.objects.create_user(
            username="admin", password="pass123", role="ADMIN", company=self.company
        )
        self.project = Project.objects.create(
            name="Test Project", company=self.company, created_by=self.user
        )
    
    def test_risk_score_calculation(self):
        """Risk score debe calcularse como likelihood_score * impact_score"""
        risk = Risk.objects.create(
            project=self.project,
            title="High Risk",
            description="Test",
            likelihood="HIGH",
            likelihood_score=5,
            impact="CRITICAL",
            impact_score=5,
            created_by=self.user
        )
        self.assertEqual(risk.risk_score, 25)
    
    def test_risk_score_medium(self):
        """Test con score medio"""
        risk = Risk.objects.create(
            project=self.project,
            title="Medium Risk",
            description="Test",
            likelihood="MEDIUM",
            likelihood_score=3,
            impact="MEDIUM",
            impact_score=3,
            created_by=self.user
        )
        self.assertEqual(risk.risk_score, 9)


class RiskViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.company = Company.objects.create(name="Test Corp", rut="12345678-9")
        self.admin = User.objects.create_user(
            username="admin", password="pass123", role="ADMIN", company=self.company
        )
        self.consultant = User.objects.create_user(
            username="consultant", password="pass123", role="CONSULTANT", company=self.company
        )
        self.project = Project.objects.create(
            name="Test Project", company=self.company, created_by=self.admin
        )
        self.risk = Risk.objects.create(
            project=self.project,
            title="Test Risk",
            description="Test",
            likelihood="HIGH",
            likelihood_score=4,
            impact="HIGH",
            impact_score=4,
            created_by=self.admin
        )
    
    def test_high_risk_filter(self):
        """Endpoint /risks/high_risk/ filtra riesgos críticos"""
        # Token para admin
        from rest_framework.authtoken.models import Token
        Token.objects.create(user=self.admin)
        token = Token.objects.get(user=self.admin).key
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
        
        response = self.client.get('/api/risks/high_risk/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
```

---

#### ✅ Día 5 (15 marzo) - Tests para SoA y Polish

**Tarea:** Tests para SoAItem y limpieza de código

**Horas:** 3 horas

**Checklist:**
- [ ] Test: SoA items creados correctamente
- [ ] Test: generate_soa crea items para todos los controles
- [ ] Test: SoA items únicos por proyecto-control
- [ ] Ejecutar `python manage.py test` - todos deben pasar
- [ ] Code cleanup y docstrings

**Verificar:**
```bash
python manage.py test apps.risks
# Output: OK (sin errores)
```

---

### **SEMANA 2 (18-24 marzo)**

#### ✅ Día 6 (18 marzo) - Risk Matrix & Filtering

**Tarea:** Endpoints avanzados para matriz de riesgos

**Horas:** 3 horas

**Checklist:**
- [ ] Crear endpoint `/risks/matrix/` que devuelva matriz (likelihood x impact)
- [ ] Crear endpoint `/risks/by_status/` para filtrar por estado
- [ ] Crear endpoint `/risks/statistics/` con KPIs
- [ ] Tests para nuevos endpoints

**Código:**

```python
# apps/risks/views.py (agregar a RiskViewSet)

@action(detail=False, methods=['get'])
def matrix(self, request):
    """Devuelve matriz de riesgos (likelihood x impact)"""
    queryset = self.get_queryset()
    
    matrix = {}
    for likelihood in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
        matrix[likelihood] = {}
        for impact in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
            count = queryset.filter(
                likelihood=likelihood, impact=impact
            ).count()
            matrix[likelihood][impact] = count
    
    return Response(matrix)

@action(detail=False, methods=['get'])
def statistics(self, request):
    """Devuelve estadísticas de riesgos"""
    queryset = self.get_queryset()
    
    return Response({
        'total_risks': queryset.count(),
        'by_status': {
            status: queryset.filter(status=status).count()
            for status, _ in Risk.STATUS_CHOICES
        },
        'average_risk_score': queryset.aggregate(
            models.Avg('risk_score')
        )['risk_score__avg'],
        'critical_risks': queryset.filter(risk_score__gte=20).count(),
    })
```

---

#### ✅ Día 7 (19 marzo) - SoA Dashboard Endpoints

**Tarea:** Endpoints para dashboards de SoA

**Horas:** 3 horas

**Checklist:**
- [ ] Endpoint `/soa-items/by_status/` - filtrar por estado implementación
- [ ] Endpoint `/soa-items/compliance_summary/` - resumen compliance
- [ ] Endpoint `/soa-items/not_applicable/` - controles N/A
- [ ] Tests para endpoints

**Código:**

```python
# apps/risks/views.py (agregar a SoAItemViewSet)

@action(detail=False, methods=['get'])
def compliance_summary(self, request):
    """Resumen de compliance por proyecto"""
    project_id = request.query_params.get('project_id')
    queryset = self.get_queryset()
    
    if project_id:
        queryset = queryset.filter(project_id=project_id)
    
    total = queryset.count()
    implemented = queryset.filter(implementation_status='IMPLEMENTED').count()
    
    return Response({
        'total_controls': total,
        'implemented': implemented,
        'compliance_percentage': (implemented / total * 100) if total > 0 else 0,
        'by_status': {
            status: queryset.filter(implementation_status=status).count()
            for status, _ in SoAItem.STATUS_CHOICES
        }
    })
```

---

#### ✅ Día 8 (20 marzo) - Documentation

**Tarea:** Documentar todos los endpoints

**Horas:** 2 horas

**Checklist:**
- [ ] Actualizar `API_ENDPOINTS.md` con nuevos endpoints
- [ ] Crear ejemplos de curl para cada endpoint
- [ ] Documentar modelos y campos

**Ejemplo:**

```markdown
# Risk Endpoints

## GET /api/risks/
Lista todos los riesgos (filtrados por permisos)

**Parámetros:**
- `project_id` (query): Filtrar por proyecto
- `status` (query): Filtrar por estado

**Ejemplo:**
```bash
curl http://localhost:8000/api/risks/ \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json"
```

**Response (200):**
```json
[
  {
    "id": 1,
    "project": 1,
    "title": "Acceso no autorizado a datos",
    "risk_score": 20,
    "status": "IDENTIFIED",
    "created_at": "2026-03-04T10:00:00Z"
  }
]
```
```

---

#### ✅ Día 9 (21 marzo) - Integration Testing

**Tarea:** Tests de integración entre modelos

**Horas:** 3 horas

**Checklist:**
- [ ] Test: Risk y SoA items relacionados
- [ ] Test: Eliminar control ISO elimina SoA items
- [ ] Test: Eliminar proyecto elimina riesgos y SoA
- [ ] Ejecutar suite completa de tests

```bash
python manage.py test apps.risks
# Output: 25 tests, OK
```

---

#### ✅ Día 10 (22-24 marzo) - Buffer & Polish

**Tarea:** Revisión, bug fixes, optimización

**Horas:** 1.5 días

**Checklist:**
- [ ] Ejecutar `python manage.py check` - 0 issues
- [ ] Todos los tests en verde
- [ ] Performance review - queries optimizadas
- [ ] Code review - no TODO comments
- [ ] Documentación actualizada

**Verificar:**
```bash
# Final check
python manage.py check
python manage.py test apps.risks
python manage.py test apps.projects  # Verificar que nada se rompió
```

---

## 📊 Checklist de Features

### ✅ Modelos (100%)
- [ ] Risk model con scoring automático
- [ ] ISOControl model con 50+ controles
- [ ] SoAItem model con justificación y estado

### ✅ APIs (100%)
- [ ] CRUD completo para Risks
- [ ] CRUD completo para ISOControl (read-only)
- [ ] CRUD completo para SoAItems
- [ ] High-risk filtering
- [ ] Risk matrix por likelihood/impact
- [ ] Risk statistics endpoint
- [ ] SoA generate endpoint
- [ ] SoA compliance summary
- [ ] Mark risk as mitigated

### ✅ Testing (100%)
- [ ] Risk score calculation tests
- [ ] Permission tests (ADMIN vs CONSULTANT)
- [ ] Endpoint functional tests
- [ ] Integration tests

### ✅ Documentation (100%)
- [ ] API endpoints documentados
- [ ] Curl examples para cada endpoint
- [ ] Model diagrams
- [ ] Field descriptions

---

## 🎯 API Endpoints Summary

### Risks
```
GET    /api/risks/                    - List all risks
POST   /api/risks/                    - Create risk
GET    /api/risks/{id}/               - Get risk detail
PUT    /api/risks/{id}/               - Update risk
DELETE /api/risks/{id}/               - Delete risk
GET    /api/risks/high_risk/          - High risk filter
GET    /api/risks/matrix/             - Risk matrix
GET    /api/risks/statistics/         - Risk stats
POST   /api/risks/{id}/mark_mitigated - Mark as mitigated
```

### ISO Controls
```
GET    /api/iso-controls/             - List all controls
GET    /api/iso-controls/{id}/        - Get control detail
GET    /api/iso-controls/by_domain/   - Controls by domain
```

### Statement of Applicability
```
GET    /api/soa-items/                - List SoA items
POST   /api/soa-items/                - Create SoA item
GET    /api/soa-items/{id}/           - Get SoA item
PUT    /api/soa-items/{id}/           - Update SoA item
POST   /api/soa-items/generate_soa/   - Auto-generate SoA
GET    /api/soa-items/compliance_summary/ - Compliance report
```

---

## 🧪 Test Commands

```bash
# Todos los tests
python manage.py test apps.risks

# Tests específicos
python manage.py test apps.risks.tests.RiskModelTest
python manage.py test apps.risks.tests.RiskViewSetTest

# Con cobertura
coverage run --source='apps.risks' manage.py test apps.risks
coverage report

# Tests + check
python manage.py check && python manage.py test apps.risks
```

---

## 📋 Definición de "Done"

Sprint 2 estará completado cuando:

- ✅ Todos los modelos creados y migrados
- ✅ Todos los endpoints implementados
- ✅ 25+ tests implementados y pasando
- ✅ Cobertura >= 80%
- ✅ Documentación actualizada
- ✅ `python manage.py check` = 0 issues
- ✅ No hay "TODO" comments en código
- ✅ Code reviewed y funcionando en dev

---

## 📦 Deliverables al Final de Sprint 2

1. **Backend API completa** - 20+ endpoints funcionales
2. **Base de datos** - Modelos Risk, ISOControl, SoAItem
3. **Tests** - 25+ tests con 80%+ cobertura
4. **Documentación** - API_ENDPOINTS.md actualizado
5. **Demo script** actualizado para incluir risk demo

---

## 📈 Success Metrics

| Métrica | Target | Status |
|---------|--------|--------|
| Endpoints implementados | 15+ | ⏳ TODO |
| Tests passing | 100% | ⏳ TODO |
| Code coverage | >= 80% | ⏳ TODO |
| Time spent | <= 10 días | ⏳ IN PROGRESS |
| No critical bugs | 100% | ⏳ TODO |

---

## 💡 Pro Tips para Sprint 2

1. **Empezar por los tests**
   - Define qué debe hacerse antes de implementar
   - Tests guían el diseño

2. **Migrations temprano**
   - Crear migraciones después de cada modelo
   - Verificar con `python manage.py check`

3. **Populate data**
   - ISO controls deben estar en BD antes de tests
   - Script para cargar datos de referencia

4. **Documentar mientras codeas**
   - Mantener `API_ENDPOINTS.md` actualizado
   - Ejemplos de curl funcionales

5. **Tests de integración**
   - No solo unit tests
   - Probar flujos reales end-to-end

---

## 🚀 Orden Recomendado de Trabajo

```
Día 1: Models + Migrations
  ├─ Risk model
  ├─ ISOControl model
  ├─ SoAItem model
  └─ Migraciones

Día 2: Serializers + ViewSets
  ├─ RiskSerializer + RiskViewSet
  ├─ ISOControlSerializer + ViewSet
  ├─ SoAItemSerializer + ViewSet
  └─ Router setup

Día 3: Populate Data
  └─ ISO controls (50+ items)

Día 4-5: Tests básicos
  ├─ Model tests
  ├─ ViewSet tests
  └─ Endpoint tests

Día 6-7: Features avanzadas
  ├─ Risk matrix
  ├─ Statistics
  ├─ SoA generate
  └─ Compliance summary

Día 8: Documentation
  └─ API docs + curl examples

Día 9-10: Polish
  ├─ Bug fixes
  ├─ Performance
  └─ Final testing
```

---

## ⚡ Quick Commands para Sprint 2

```bash
# Setup
cd backend
source .venv/Scripts/activate

# Crear app risks
python manage.py startapp risks

# Después de models
python manage.py makemigrations risks
python manage.py migrate

# After serializers
python manage.py check

# Populate ISO controls
python populate_iso_controls.py

# Run all tests
python manage.py test apps.risks

# Check coverage
coverage run --source='apps.risks' manage.py test apps.risks
coverage report --include=apps/risks/*

# Verify everything
python manage.py check && python manage.py test
```

---

**Listo para empezar Sprint 2 el 11 de marzo!** 🚀

¿Necesitas que ajuste algo del plan o que te genere el código completo de un día específico?
