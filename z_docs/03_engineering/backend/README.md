# Proyecto VIT Backend - Django REST Framework

## Estructura del Proyecto

### Configuracion
- manage.py - Punto de entrada de Django
- config/settings.py - Configuracion principal con apps instaladas, middleware, CORS, DB
- config/urls.py - URLs principales y rutas de API
- config/wsgi.py - WSGI application para produccion
- config/asgi.py - ASGI application para WebSockets
- .env.example - Template de variables de entorno
- .env - Variables de entorno actuales
- requirements.txt - Dependencias Python

### Aplicaciones Django

1. users/ - Gestion de usuarios y autenticacion
   - Modelo: User (custom, con roles: ADMIN, CONSULTANT, CLIENT)
   - Endpoints: /api/users/ (CRUD), /api/users/login/ (autenticacion)
   - Serializers, ViewSets, Admin panel

2. companies/ - Gestion de empresas (clientes)
   - Modelo: Company (nombre, RFC, contacto, ubicacion)
   - Endpoints: /api/companies/
   - CRUD completo

3. projects/ - Gestion de proyectos ISO 27001
   - Modelos: Project, Phase, Task, ProjectUser
   - Endpoints: /api/projects/, /api/phases/, /api/tasks/, /api/project-users/
   - Relaciones anidadas, seguimiento de tareas
   - ProjectUser: asignación de usuarios a proyectos con roles específicos
   - Filtrado automático: cada usuario ve solo sus proyectos

4. users/ - Autenticación, seguridad y auditoría (SPRINT 1 ✅)
   - Modelo: User (AbstractUser con roles ADMIN/CONSULTANT/CLIENT)
   - Modelo: AuditLog (QUIEN/QUE/CUANDO/DONDE con JSONField para cambios)
   - Endpoints: /api/token/ (login JWT), /api/users/ (CRUD), /api/audit-logs/ (consulta)
   - Signals: 10 receivers automáticos registran cambios en todas las acciones
   - 6 permission classes para control fino de acceso

5. risks/ - Evaluacion de riesgos (Sprint 3)
   - Modelo: Risk (con matriz likelihood x impact)
   - Endpoints: /api/risks/
   - Cálculo automático de risk_score (sprint 3)

6. iso_controls/ - Controles ISO 27001 y SoA (Sprint 4)
   - Modelos: ISOControl (codigo A.5.1, etc.), SoAItem (aplicabilidad)
   - Endpoints: /api/iso-controls/ (lectura), /api/soa-items/ (CRUD)
   - Statement of Applicability

6. documents/ - Gestion de documentos y evidencias
   - Modelos: Document (templates, reportes), Evidence (archivos subidos)
   - Endpoints: /api/documents/, /api/evidence/
   - Carga y descarga de archivos

7. reports/ - Generacion de reportes
   - Modelo: Report (Progress, Risk, SoA, Compliance, Executive)
   - Endpoints: /api/reports/ con acciones /generate/ y /send/

### Caracteristicas (SPRINT 1 ✅ Completado)
- ✅ Autenticación JWT con SimpleJWT (access + refresh tokens, 15min + 1day)
- ✅ Sistema de roles (ADMIN, CONSULTANT, CLIENT) con 6 permission classes
- ✅ Permisos granulares (IsAdmin, IsConsultant, IsClient, IsAdminOrReadOnly, IsConsultantOrReadOnly, IsOwnerOrReadOnly)
- ✅ ProjectUser: relación user-project-role con filtrado automático por rol
- ✅ AuditLog automático: Django signals registran CREATE/UPDATE/DELETE sin código adicional
- ✅ CORS habilitado para frontend en localhost:3000
- ✅ Timestamps en todos los modelos (created_at, updated_at)
- ✅ Relaciones ForeignKey y ManyToMany con validaciones
- ✅ Admin panel de Django configurado para todas las apps
- ✅ Serializers anidados para relaciones complejas
- ✅ ViewSets automáticos con CRUD y filtrado por rol
- ✅ 7 endpoints protegidos (usuarios, empresas, proyectos, fases, tareas, project-users, audit-logs)
- ✅ Demo data population script (scripts/populate_demo_data.py)
- ✅ Automated test suite (tests/test_demo_sprint1.py: 5 escenarios, todos passing)
- ✅ Git: v0.1-sprint1 tagged, 12+ commits en Sprint 1

## Como usar

## Como usar

### 1. Configurar Base de Datos
```bash
# PostgreSQL (recomendado)
DB_NAME=proyecto_vit
DB_USER=postgres
DB_PASSWORD=tu_contraseña
DB_HOST=localhost
DB_PORT=5432

# O SQLite (desarrollo local)
# Ya viene configurado por defecto
```

### 2. Aplicar Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear Superusuario
```bash
python manage.py createsuperuser
```

### 4. Ejecutar Servidor
```bash
python manage.py runserver
# Accede a http://localhost:8000/admin
```

### 5. Cargar Datos Iniciales
- Crear controles ISO 27001 (A.5.1 a A.18.2)
- Crear template de documentos
- Configurar permisos por rol

## Estructura de Carpetas
```
backend/
├── manage.py
├── requirements.txt
├── .env
├── .env.example
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── apps/
    ├── users/
    ├── companies/
    ├── projects/
    ├── risks/
    ├── iso_controls/
    ├── documents/
    └── reports/
```

## Variables de Entorno
```
DEBUG=True
SECRET_KEY=tu-clave-secreta
DB_NAME=proyecto_vit
DB_USER=postgres
DB_PASSWORD=contraseña
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Comandos Utiles
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar tests
python manage.py test

# Shell de Django
python manage.py shell
```

## Endpoints API
```
POST   /api/users/                  Crear usuario
GET    /api/users/                  Listar usuarios
POST   /api/users/login/            Login
GET    /api/companies/              Listar empresas
POST   /api/projects/               Crear proyecto
GET    /api/projects/               Listar proyectos
POST   /api/risks/                  Crear riesgo
GET    /api/iso-controls/           Listar controles ISO
POST   /api/soa-items/              Crear SoA
GET    /api/documents/              Listar documentos
POST   /api/evidence/               Subir evidencia
POST   /api/reports/                Crear reporte
```

## Notas
- El modelo User extiende AbstractUser de Django
- Use AUTH_USER_MODEL = 'users.User' en settings.py
- Las apps estan registradas en INSTALLED_APPS
- CORS configurado para localhost:3000
- Usa select_related() y prefetch_related() para optimizar queries
- Los archivos se guardan en media/documents/ y media/evidence/

