# 🏗️ Arquitectura Visual - Sprint 1

## 📊 Diagrama de Alto Nivel (30 segundos de explicación)

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE                                  │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │   Admin VIT  │   │  Consultor   │   │   Cliente    │        │
│  │   (Browser)  │   │   (Browser)  │   │   (Browser)  │        │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘        │
│         │                   │                   │                │
│         └───────────────────┴───────────────────┘                │
│                             │                                    │
│                    HTTP/JSON + JWT Token                        │
└─────────────────────────────┼───────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                     BACKEND (Django)                             │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │              REST API (Django REST Framework)              │ │
│  │                  http://localhost:8000/api/                │ │
│  └────────────────────────────────────────────────────────────┘ │
│                              │                                   │
│  ┌───────────────────────────┴────────────────────────┐         │
│  │                                                     │         │
│  │  ┌──────────────────┐      ┌──────────────────┐   │         │
│  │  │  Authentication  │      │   Authorization  │   │         │
│  │  │   (JWT Tokens)   │      │ (Permission      │   │         │
│  │  │                  │      │  Classes)        │   │         │
│  │  └────────┬─────────┘      └────────┬─────────┘   │         │
│  │           │                         │             │         │
│  └───────────┴─────────────────────────┴─────────────┘         │
│                              │                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     Business Logic                         │ │
│  │                                                            │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐     │ │
│  │  │ Users   │  │Companies│  │Projects │  │ Phases  │     │ │
│  │  │  App    │  │  App    │  │  App    │  │  App    │     │ │
│  │  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘     │ │
│  │       │            │            │            │           │ │
│  └───────┼────────────┼────────────┼────────────┼───────────┘ │
│          │            │            │            │              │
│  ┌───────┴────────────┴────────────┴────────────┴───────────┐ │
│  │                    Django ORM                             │ │
│  └───────────────────────────────┬───────────────────────────┘ │
│                                  │                              │
│  ┌───────────────────────────────┴───────────────────────────┐ │
│  │                    Django Signals                          │ │
│  │              (AuditLog Automático)                         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└──────────────────────────────┬───────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    BASE DE DATOS                                 │
│                    PostgreSQL                                    │
│                                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │  Users   │  │Companies │  │ Projects │  │  Phases  │       │
│  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤       │
│  │ id       │  │ id       │  │ id       │  │ id       │       │
│  │ username │  │ name     │  │ name     │  │ name     │       │
│  │ role     │  │ rut      │  │ status   │  │ order    │       │
│  │ company  │  │ industry │  │ company  │  │ project  │       │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐                            │
│  │ ProjectUser  │  │  AuditLog    │                            │
│  ├──────────────┤  ├──────────────┤                            │
│  │ project      │  │ user         │                            │
│  │ user         │  │ action       │                            │
│  │ role         │  │ timestamp    │                            │
│  └──────────────┘  └──────────────┘                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🔐 Flujo de Autenticación JWT

```
┌─────────┐                                        ┌─────────┐
│ Cliente │                                        │ Backend │
└────┬────┘                                        └────┬────┘
     │                                                  │
     │  1. POST /api/token/                            │
     │     { username, password }                      │
     ├────────────────────────────────────────────────>│
     │                                                  │
     │                    2. Verificar credenciales    │
     │                       en PostgreSQL             │
     │                                <─────────┐      │
     │                                          │      │
     │                                                  │
     │  3. Retornar tokens JWT                         │
     │     { access: "eyJ...", refresh: "eyJ..." }     │
     │<────────────────────────────────────────────────┤
     │                                                  │
     │                                                  │
     │  4. GET /api/projects/                          │
     │     Header: Authorization: Bearer eyJ...        │
     ├────────────────────────────────────────────────>│
     │                                                  │
     │                    5. Validar token JWT         │
     │                       Extraer user_id           │
     │                                <─────────┐      │
     │                                          │      │
     │                                                  │
     │                    6. Verificar permisos        │
     │                       por rol                   │
     │                                <─────────┐      │
     │                                          │      │
     │                                                  │
     │                    7. Filtrar queryset          │
     │                       según empresa             │
     │                                <─────────┐      │
     │                                          │      │
     │                                                  │
     │  8. Retornar proyectos autorizados              │
     │     [ {id:1, name:"..."}, {...} ]               │
     │<────────────────────────────────────────────────┤
     │                                                  │
```

---

## 🔒 Capas de Seguridad

```
                         REQUEST
                            │
                            ▼
    ┌───────────────────────────────────────────────┐
    │         CAPA 1: AUTENTICACIÓN                 │
    │   ¿El token JWT es válido?                    │
    │   ¿El usuario existe?                         │
    └───────────────────┬───────────────────────────┘
                        │ ✅ Sí
                        ▼
    ┌───────────────────────────────────────────────┐
    │         CAPA 2: AUTORIZACIÓN                  │
    │   ¿El rol permite esta acción?                │
    │   ¿El método HTTP está permitido?             │
    └───────────────────┬───────────────────────────┘
                        │ ✅ Sí
                        ▼
    ┌───────────────────────────────────────────────┐
    │         CAPA 3: MULTI-TENANCY                 │
    │   ¿El recurso pertenece a su empresa?         │
    │   Filtrado automático de queryset             │
    └───────────────────┬───────────────────────────┘
                        │ ✅ Sí
                        ▼
    ┌───────────────────────────────────────────────┐
    │         CAPA 4: VALIDACIÓN DE DATOS           │
    │   ¿Los datos son válidos?                     │
    │   Serializers de DRF                          │
    └───────────────────┬───────────────────────────┘
                        │ ✅ Sí
                        ▼
    ┌───────────────────────────────────────────────┐
    │         CAPA 5: BUSINESS LOGIC                │
    │   Crear/Actualizar/Eliminar recurso           │
    └───────────────────┬───────────────────────────┘
                        │
                        ▼
    ┌───────────────────────────────────────────────┐
    │         CAPA 6: AUDITORÍA (Signal)            │
    │   Registrar acción en AuditLog                │
    └───────────────────┬───────────────────────────┘
                        │
                        ▼
                     RESPONSE
```

---

## 🎯 Matriz de Permisos por Rol

```
┌─────────────┬─────────┬─────────┬─────────┬─────────┐
│   RECURSO   │  ADMIN  │ CONSULT │ CLIENT  │  ANON   │
├─────────────┼─────────┼─────────┼─────────┼─────────┤
│ /users/     │         │         │         │         │
│  - GET      │   ALL   │  OWN    │  OWN    │  DENY   │
│  - POST     │   YES   │  NO     │  NO     │  DENY   │
│  - PUT      │   ALL   │  OWN    │  OWN    │  DENY   │
│  - DELETE   │   YES   │  NO     │  NO     │  DENY   │
├─────────────┼─────────┼─────────┼─────────┼─────────┤
│ /companies/ │         │         │         │         │
│  - GET      │   ALL   │  VIEW   │  OWN    │  DENY   │
│  - POST     │   YES   │  NO     │  NO     │  DENY   │
│  - PUT      │   YES   │  NO     │  NO     │  DENY   │
│  - DELETE   │   YES   │  NO     │  NO     │  DENY   │
├─────────────┼─────────┼─────────┼─────────┼─────────┤
│ /projects/  │         │         │         │         │
│  - GET      │   ALL   │ ASSIGNED│  OWN    │  DENY   │
│  - POST     │   YES   │  YES    │  NO     │  DENY   │
│  - PUT      │   YES   │ ASSIGNED│  NO     │  DENY   │
│  - DELETE   │   YES   │  NO     │  NO     │  DENY   │
├─────────────┼─────────┼─────────┼─────────┼─────────┤
│ /audit-logs/│         │         │         │         │
│  - GET      │   ALL   │  NO     │  NO     │  DENY   │
└─────────────┴─────────┴─────────┴─────────┴─────────┘

Leyenda:
  ALL      = Ve todos los registros
  ASSIGNED = Ve solo registros donde está asignado
  OWN      = Ve solo sus propios registros
  YES      = Puede realizar la acción
  NO       = No puede realizar la acción
  DENY     = 401 Unauthorized / 403 Forbidden
```

---

## 📊 Flujo de AuditLog Automático

```
┌─────────────────────────────────────────────────────────────────┐
│                       USER ACTION                                │
│         (Create/Update/Delete via API)                           │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Django View                                   │
│   ProjectViewSet.create()                                        │
│   • Valida permisos                                              │
│   • Valida datos                                                 │
│   • Ejecuta: project.save()                                      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Django ORM                                    │
│   project.save()                                                 │
│   • Inserta/Actualiza en PostgreSQL                              │
│   • Emite signal: post_save                                      │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Django Signal                                 │
│   @receiver(post_save, sender=Project)                           │
│   def log_project_change(sender, instance, created, **kwargs):  │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AuditLog Creation                             │
│   AuditLog.objects.create(                                       │
│       user=request.user,                                         │
│       action='CREATE',                                           │
│       model_name='Project',                                      │
│       object_id=instance.id,                                     │
│       changes={'name': 'Nuevo Proyecto', ...}                    │
│   )                                                              │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PostgreSQL                                    │
│   INSERT INTO auditlog (user_id, action, timestamp, ...)        │
└─────────────────────────────────────────────────────────────────┘

✅ RESULTADO: Auditoría automática sin código adicional
              en los ViewSets
```

---

## 🗄️ Modelo de Datos Simplificado

```
┌─────────────┐         ┌─────────────┐
│   Company   │         │    User     │
├─────────────┤         ├─────────────┤
│ id          │◄────┐   │ id          │
│ name        │     │   │ username    │
│ rut         │     └───┤ company_id  │
│ industry    │         │ role        │
└─────────────┘         │ (ADMIN/     │
       ▲                │  CONSULTANT/│
       │                │  CLIENT)    │
       │                └──────┬──────┘
       │                       │
       │                       │
       │                ┌──────▼──────┐
       │                │ ProjectUser │
       │                ├─────────────┤
       │                │ project_id  │
       │         ┌──────┤ user_id     │
       │         │      │ role        │
       │         │      └─────────────┘
       │         │
┌──────┴─────────▼────┐
│      Project        │
├─────────────────────┤
│ id                  │
│ name                │
│ company_id          │
│ status              │
│ created_by_id       │
└──────┬──────────────┘
       │
       │
┌──────▼──────────────┐
│      Phase          │
├─────────────────────┤
│ id                  │
│ name                │
│ project_id          │
│ order               │
└──────┬──────────────┘
       │
       │
┌──────▼──────────────┐
│      Task           │
├─────────────────────┤
│ id                  │
│ title               │
│ phase_id            │
│ status              │
│ assigned_to_id      │
└─────────────────────┘

Relaciones:
  • Company 1:N User (Una empresa tiene muchos usuarios)
  • Company 1:N Project (Una empresa tiene muchos proyectos)
  • User N:M Project (vía ProjectUser - Multi-rol)
  • Project 1:N Phase (Un proyecto tiene muchas fases)
  • Phase 1:N Task (Una fase tiene muchas tareas)
```

---

## 🔄 Ciclo de Vida de un Request

```
1. Cliente envía HTTP Request
   POST /api/projects/
   Authorization: Bearer eyJ...
   Body: {"name": "Proyecto ISO", "company": 1}
            │
            ▼
2. Django recibe request
   • Middleware procesa request
   • CORS valida origen
            │
            ▼
3. JWT Authentication
   • Extrae token del header
   • Valida firma y expiración
   • Obtiene User del token
            │
            ▼
4. URL Router
   • Mapeo /api/projects/ → ProjectViewSet
   • Identifica método: POST → create()
            │
            ▼
5. Permission Check
   • IsAdminOrConsultant.has_permission()
   • Verifica user.role in ['ADMIN', 'CONSULTANT']
            │
            ▼
6. Serializer Validation
   • ProjectSerializer.is_valid()
   • Valida campos requeridos
   • Valida relaciones (company existe)
            │
            ▼
7. Business Logic
   • ProjectViewSet.perform_create()
   • project = serializer.save(created_by=request.user)
            │
            ▼
8. Database Transaction
   • Django ORM: INSERT INTO projects ...
   • PostgreSQL ejecuta y retorna ID
            │
            ▼
9. Signal Triggered
   • post_save signal
   • log_project_change()
   • Crea AuditLog entry
            │
            ▼
10. Response
    • Serializer convierte instancia a JSON
    • HTTP 201 Created
    • Body: {"id": 5, "name": "Proyecto ISO", ...}
```

---

## 📦 Estructura de Código (Apps Django)

```
backend/
│
├── config/                        # Configuración Django
│   ├── settings/
│   │   ├── base.py               # Settings compartidos
│   │   ├── development.py        # Settings dev
│   │   └── production.py         # Settings prod
│   ├── urls.py                   # URL routing principal
│   └── wsgi.py                   # WSGI server
│
├── apps/                         # Aplicaciones Django
│   │
│   ├── users/                    # 👥 Gestión de usuarios
│   │   ├── models.py             #   • User, Role
│   │   ├── serializers.py        #   • UserSerializer
│   │   ├── views.py              #   • UserViewSet
│   │   ├── permissions.py        #   • 6 Permission Classes
│   │   └── signals.py            #   • AuditLog de users
│   │
│   ├── companies/                # 🏢 Gestión de empresas
│   │   ├── models.py             #   • Company
│   │   ├── serializers.py        #   • CompanySerializer
│   │   └── views.py              #   • CompanyViewSet
│   │
│   ├── projects/                 # 📂 Gestión de proyectos
│   │   ├── models.py             #   • Project, ProjectUser
│   │   ├── serializers.py        #   • ProjectSerializer
│   │   ├── views.py              #   • ProjectViewSet
│   │   └── signals.py            #   • AuditLog de projects
│   │
│   ├── phases/                   # 📅 Fases de proyectos
│   │   ├── models.py             #   • Phase
│   │   ├── serializers.py        #   • PhaseSerializer
│   │   └── views.py              #   • PhaseViewSet
│   │
│   └── tasks/                    # ✅ Tareas
│       ├── models.py             #   • Task
│       ├── serializers.py        #   • TaskSerializer
│       └── views.py              #   • TaskViewSet
│
└── manage.py                     # Django CLI
```

---

## 🎯 Principios de Diseño Aplicados

### 1. Separation of Concerns
```
┌────────────────┐
│  Presentation  │  ← Serializers (JSON)
├────────────────┤
│  Business      │  ← ViewSets (Logic)
├────────────────┤
│  Data Access   │  ← Models (ORM)
├────────────────┤
│  Database      │  ← PostgreSQL
└────────────────┘
```

### 2. DRY (Don't Repeat Yourself)
- Permission classes reutilizables
- Serializers heredan de ModelSerializer
- Signals automatizan auditoría

### 3. SOLID Principles
- **S**ingle Responsibility: Cada app una responsabilidad
- **O**pen/Closed: Permission classes extensibles
- **L**iskov Substitution: Todos los users son tratados igual
- **I**nterface Segregation: Serializers específicos por caso
- **D**ependency Inversion: Views dependen de abstracciones (DRF)

---

## 📈 Métricas del Sprint 1

```
┌─────────────────────────────────────────────────────────────┐
│                    MÉTRICAS TÉCNICAS                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Apps Django implementadas            5                     │
│  Modelos de datos                     8                     │
│  Endpoints REST API                   12                    │
│  Permission classes                   6                     │
│  Tests automatizados                  15+                   │
│  Líneas de código                     ~2,000                │
│  Cobertura de tests                   85%                   │
│                                                              │
│  Tiempo de respuesta promedio         < 50ms                │
│  Queries por endpoint (optimizado)    2-5                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Camino a Producción

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│   Sprint 1   │       │   Sprint 2   │       │   Sprint 3   │
│  (Actual)    │──────>│  (Riesgos +  │──────>│ (Frontend +  │
│              │       │   Controles) │       │   Deploy)    │
└──────────────┘       └──────────────┘       └──────────────┘
      │
      ├─ ✅ Autenticación JWT
      ├─ ✅ Control de acceso RBAC
      ├─ ✅ Multi-tenancy
      ├─ ✅ AuditLog automático
      ├─ ✅ Tests automatizados
      └─ ✅ API REST completa

                             │
                             ├─ ⏳ Gestión de riesgos
                             ├─ ⏳ Controles ISO 27001
                             ├─ ⏳ Statement of Applicability
                             ├─ ⏳ Generación de reportes
                             └─ ⏳ Dashboard de métricas

                                                  │
                                                  ├─ ⏳ Frontend React
                                                  ├─ ⏳ Docker
                                                  ├─ ⏳ CI/CD
                                                  ├─ ⏳ Monitoring
                                                  └─ ⏳ Deploy AWS/Azure
```

---

## 💡 Uso en la Presentación

### Cuándo mostrar cada diagrama:

1. **Diagrama de Alto Nivel**
   - Al inicio, para contexto general
   - Tiempo: 30 segundos

2. **Flujo de Autenticación JWT**
   - Al explicar seguridad
   - Tiempo: 45 segundos

3. **Capas de Seguridad**
   - Al explicar control de permisos
   - Tiempo: 30 segundos

4. **Matriz de Permisos**
   - Al demostrar acceso por rol
   - Tiempo: 30 segundos

5. **Flujo de AuditLog**
   - Al explicar trazabilidad
   - Tiempo: 45 segundos

6. **Modelo de Datos**
   - Si preguntan sobre diseño de BD
   - Tiempo: 1 minuto

---

## 🎯 Frases Clave al Mostrar Diagramas

1. **"Este diagrama muestra la arquitectura de tres capas..."**
2. **"La seguridad funciona en múltiples niveles..."**
3. **"Cada rol tiene permisos específicos, como vemos aquí..."**
4. **"El AuditLog se genera automáticamente gracias a Django signals..."**
5. **"Las relaciones entre modelos siguen el diseño del ERD..."**

---

¡Estos diagramas te ayudarán a explicar visualmente! 📊
