# 🚀 Arquitectura de Despliegue en Producción — VIT SGSI Platform

**Documento:** Diseño de infraestructura para producción  
**Fecha:** 23 febrero 2026  
**Versión:** 1.0  
**Estado:** Listo para implementación

---

## 📊 Arquitectura Recomendada

```
┌─────────────────────────────────────────────────────────────────┐
│                         INTERNET (HTTPS)                         │
└─────────────────────────────────────────────────────────────────┘
              │                                    │
              ▼                                    ▼
    ┌──────────────────┐            ┌──────────────────┐
    │  Frontend: Vercel│            │  Backend: Render │
    │  React SPA       │            │  Django + DRF    │
    │  Static + Vite   │            │  Gunicorn        │
    └──────────────────┘            └──────────────────┘
              │                              │
              │                    ┌─────────┼──────────┐
              │                    │         │          │
              ▼                    ▼         ▼          ▼
         (CORS OK)      ┌──────────────┐  PostgreSQL  S3 Compatible
         API Calls      │ Django Apps  │  (Render)    (Supabase/AWS)
                        └──────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
            ┌──────────────┐    ┌──────────────┐
            │  PostgreSQL  │    │  S3 Storage  │
            │  Administrado│    │  (Evidencias)│
            │  (Render)    │    │  (Supabase)  │
            └──────────────┘    └──────────────┘
                   │                    │
            ┌──────┴────────────────────┴──────┐
            │     GitHub Actions (CI/CD)       │
            │  - Tests (push)                  │
            │  - Build (merge master)          │
            │  - Deploy (auto)                 │
            └──────────────────────────────────┘
```

---

## 🏗️ Stack Tecnológico Final

| Componente | Tecnología | Servicio | Costo |
|---|---|---|---|
| **Frontend** | React 18 + Vite | Vercel | Gratis |
| **Backend** | Django 4.2 + DRF | Render | $12/mes (Web) |
| **Base de datos** | PostgreSQL 15 | Render | $15/mes (1GB) |
| **Almacenamiento** | S3 Compatible | Supabase Storage | Gratis (1GB) |
| **CI/CD** | GitHub Actions | GitHub | Gratis |
| **DNS/SSL** | Cloudflare | Cloudflare | Gratis |
| **Monitoreo** | Sentry (opcional) | Sentry | Gratis (plan básico) |
| **Logs** | Render + upstash | Render | Incluido |
| **Total mensual** | | | ~$27/mes |

**Escalabilidad:** Sube a $50-100/mes si necesitas más capacidad (Render suele doblar automaticamente)

---

## 📐 Decisiones Arquitectónicas

### 1️⃣ **Backend en Render (no Heroku/Railway)**

**Por qué Render:**
- ✅ PostgreSQL administrada incluida (muy fácil)
- ✅ Redeploy automático desde GitHub (push master = redeploy)
- ✅ Ambiente separado por rama (staging/production)
- ✅ Variables de entorno en UI
- ✅ Libre de saltos de precio (predictible)
- ✅ Soporte a WebSockets (futuro)
- ✅ HTTPS automático

**Alternativa descartada (Heroku):**
- ❌ Ahora cuesta $7/dynos (antes gratis)
- ❌ PostgreSQL addon caro ($50+)
- ❌ No ideal para presupuesto bajo

---

### 2️⃣ **Frontend en Vercel (no Netlify)**

**Por qué Vercel:**
- ✅ Integración perfecta con Next.js/Vite
- ✅ Build automático en push
- ✅ Aliases/previews por PR
- ✅ CDN global incluido
- ✅ Performance optimizado

---

### 3️⃣ **PostgreSQL Administrada (Render)**

**Por qué no local/SQLite:**
- ❌ SQLite NO soporta concurrencia multi-proceso
- ❌ No hay backups automáticos
- ❌ No escalable

**Por qué Render PostgreSQL:**
- ✅ Backups automáticos diarios
- ✅ SSL habilitado automaticamente
- ✅ Acceso remoto seguro
- ✅ Actualización automática de versiones
- ✅ Snapshots antes de cambios críticos

---

### 4️⃣ **Almacenamiento (Supabase Storage o AWS S3)**

**Problema:** Render utiliza filesystem efímero (se borra en redeploy)

**Solución:** Almacenamiento externo

| Opción | Costo | Pros | Contras |
|--------|-------|------|---------|
| **Supabase Storage** | Gratis (1GB) | Fácil, incluye API | Limitado |
| **AWS S3** | $0.023/GB | Escalable, barato | Setup complejo |
| **Wasabi** | $5.99/mes | Barato, ilimitado | Menos popular |

**Recomendación:** Supabase Storage (gratis inicialmente, escala fácil a AWS S3 luego)

---

### 5️⃣ **CI/CD con GitHub Actions**

**Flujo:**
1. Dev hace push a rama feature
2. GitHub Actions corre tests (pytest)
3. Si pasan → aprobación para merge
4. Merge a `master`
5. Render detecta cambio y redeploya automáticamente

**Ventaja:** Cero configuración manual, todo automático

---

## 🔧 Configuración Django para Producción

### **settings/production.py** (nuevo archivo)

```python
# backend/config/settings/production.py

from .base import *
import os

# Security
DEBUG = False
ALLOWED_HOSTS = [
    'api.midominio.com',  # Tu dominio real
    'vit-plataforma-backend.onrender.com',  # Render default
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT', '5432'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': 600,  # Connection pooling
        'SSL_REQUIRE': True,
    }
}

# JWT (más restrictivo en prod)
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),  # Expiración corta
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,  # Rotación de refresh tokens
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_COOKIE_SECURE': True,  # Solo HTTPS
    'AUTH_COOKIE_HTTP_ONLY': True,  # No accesible desde JS
    'AUTH_COOKIE_SAMESITE': 'Strict',  # Protección CSRF
}

# CORS (restringido)
CORS_ALLOWED_ORIGINS = [
    'https://midominio.com',
    'https://www.midominio.com',
    'https://app.midominio.com',  # Frontend específico
]
CORS_ALLOW_CREDENTIALS = True

# Cache (Redis si está disponible)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

# Logging estructurado
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'json': {
            '()': 'pythonjsonlogger.jsonlogger.JsonFormatter',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'json',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'level': 'INFO',
        },
        'apps': {  # Tu app
            'level': 'DEBUG',
        },
    },
}

# Security headers
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "cdn.example.com"),
}

# Almacenamiento (S3)
if os.environ.get('USE_S3'):
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
            'OPTIONS': {
                'ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
                'SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
                'STORAGE_BUCKET_NAME': os.environ.get('AWS_STORAGE_BUCKET_NAME'),
                'S3_REGION_NAME': os.environ.get('AWS_S3_REGION_NAME', 'us-east-1'),
                'S3_CUSTOM_DOMAIN': os.environ.get('AWS_S3_CUSTOM_DOMAIN'),
                'S3_SIGNATURE_VERSION': 's3v4',
            }
        }
    }
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    # Local fallback
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Gunicorn config
WSGI_APPLICATION = 'config.wsgi.production'

# Sentry (optional error tracking)
if os.environ.get('SENTRY_DSN'):
    import sentry_sdk
    sentry_sdk.init(
        dsn=os.environ.get('SENTRY_DSN'),
        traces_sample_rate=0.1,
    )
```

### **wsgi.py** (producción)

```python
# backend/config/wsgi.py

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_wsgi_application()
```

### **requirements.txt** (agregar)

```
# Production
gunicorn==21.2.0
python-dotenv==1.0.0
psycopg2-binary==2.9.9
django-cors-headers==4.3.1
djangorestframework-simplejwt==5.3.0
boto3==1.28.0
django-storages==1.14.2
python-json-logger==2.0.7
sentry-sdk==1.38.0
```

---

## 🌐 Variables de Entorno Producción

### **Backend (.env en Render)**

```env
# Django
DEBUG=False
SECRET_KEY=tu_secret_key_super_largo_y_aleatorio
DJANGO_SETTINGS_MODULE=config.settings.production

# Database
DATABASE_ENGINE=postgresql
DATABASE_NAME=vit_db
DATABASE_USER=vit_user
DATABASE_PASSWORD=contraseña_super_fuerte
DATABASE_HOST=dpg-xxxxxxx.render.com
DATABASE_PORT=5432

# JWT
JWT_SECRET_KEY=tu_jwt_secret_super_largo
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=3600
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=604800

# CORS
ALLOWED_HOSTS=api.midominio.com,vit-plataforma-backend.onrender.com
CORS_ALLOWED_ORIGINS=https://midominio.com,https://www.midominio.com

# S3 Storage (si usas)
USE_S3=True
AWS_ACCESS_KEY_ID=xxxxx
AWS_SECRET_ACCESS_KEY=xxxxx
AWS_STORAGE_BUCKET_NAME=vit-evidencias
AWS_S3_REGION_NAME=us-east-1
AWS_S3_CUSTOM_DOMAIN=s3.amazonaws.com/vit-evidencias

# Logging
SENTRY_DSN=https://xxxxx@xxxxx.ingest.sentry.io/xxxxx
```

---

## 📦 Proceso de Deploy Paso a Paso

### **Fase 1: Preparación Inicial (1-2 horas)**

#### **1.1 Configurar PostgreSQL en Render**

```bash
# En la UI de Render:
1. Ir a Dashboard → New → PostgreSQL
2. Nombre: vit-database
3. Database: vit_db
4. User: vit_user
5. Region: Frankfurt (o la más cercana)
6. Plan: Free (durante desarrollo)
7. Crear
8. Copiar connection string (la guardarás en backend)
```

#### **1.2 Preparar Backend (Django)**

```bash
# En tu PC (desarrollo)
cd backend

# Crear settings/production.py (usar template arriba)
# Crear settings/__init__.py si no existe

# Instalar dependencias
pip install -r requirements.txt
pip install gunicorn psycopg2-binary boto3 django-storages

# Crear .env.production.example para documentar
cat > .env.production.example << 'EOF'
DEBUG=False
SECRET_KEY=change_me_in_production
DATABASE_URL=postgresql://user:password@host:5432/db
JWT_SECRET_KEY=change_me
EOF

# Commit
git add config/settings/production.py
git add requirements.txt
git add .env.production.example
git commit -m "chore: Add production Django settings"
git push origin master
```

#### **1.3 Configurar Render Web Service**

```
En UI de Render:
1. New → Web Service
2. Conectar repo GitHub
3. Deploy from branch: master
4. Build command: pip install -r requirements.txt
5. Start command: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT

Variables de entorno: (copiar del .env.production)
- DEBUG=False
- SECRET_KEY=<generar uno nuevo con secrets>
- DATABASE_NAME=vit_db
- DATABASE_USER=vit_user
- DATABASE_PASSWORD=<copiar de PostgreSQL creado>
- DATABASE_HOST=<copiar de PostgreSQL>
- ALLOWED_HOSTS=<tu-app>.onrender.com

6. Create Web Service
7. Esperar ~5 min primer deploy
```

#### **1.4 Ejecutar Migraciones**

```bash
# Desde terminal local o Render shell
python manage.py migrate
python manage.py createsuperuser  # Usuario admin inicial
python manage.py collectstatic --no-input
```

---

### **Fase 2: Frontend (30 min)**

```bash
# En frontend/
npm install

# Crear .env.production
VITE_API_URL=https://api.midominio.com

# Build
npm run build

# Vercel via GitHub
1. Ir a vercel.com → New Project
2. Import tu repo
3. Framework: Vite / React
4. Environment: VITE_API_URL=https://tu-backend.onrender.com
5. Deploy
```

---

### **Fase 3: CI/CD Automático**

#### **GitHub Actions (.github/workflows/deploy.yml)**

```yaml
name: Deploy to Production

on:
  push:
    branches: [master]
  pull_request:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_DB: test_db
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_pass
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          cd backend
          python manage.py test
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
      
      - name: Lint
        run: |
          cd backend
          pip install flake8
          flake8 apps/ --count --select=E9,F63,F7,F82 --show-source

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/master' && github.event_name == 'push'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Render
        run: |
          curl -X POST \
            https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_API_KEY }}
```

---

## 🔒 Seguridad en Producción

### **Checklist de Seguridad**

- [ ] DEBUG = False
- [ ] SECRET_KEY único y largo (mínimo 50 caracteres)
- [ ] ALLOWED_HOSTS configurado específicamente
- [ ] HTTPS obligatorio (SECURE_SSL_REDIRECT = True)
- [ ] JWT tokens con expiración corta (1 hora máximo)
- [ ] CORS restringido a dominios específicos
- [ ] CSRF protección activa
- [ ] SQL injection imposible (Django ORM + prepared statements)
- [ ] Rate limiting en endpoints críticos
- [ ] Logging de intentos fallidos
- [ ] Backups automáticos de BD
- [ ] Variables sensibles nunca en código (solo .env)
- [ ] S3 con política de acceso privado
- [ ] Certificado SSL/TLS válido

### **Endpoints Críticos a Rate Limit**

```python
# En views.py
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

class TokenObtainPairView(ModelViewSet):
    @method_decorator(cache_page(60))  # Rate limit: 1 request/60s
    def login(self, request):
        # ...
```

---

## 🚨 Manejo de Migraciones en Producción

### **Flujo seguro:**

```bash
# En desarrollo
python manage.py makemigrations

# En familia que requiere cambio con downtime 0:
# 1. Crear migration reversible
# 2. Testear localmente
# 3. Commit

# En producción (automático):
# Render ejecuta: python manage.py migrate (en build)
```

**Importante:** Siempre testea migraciones localmente antes de pushear a master.

---

## 📁 Manejo de Archivos (Evidencias)

### **Opción 1: Supabase Storage (Recomendado inicialmente)**

```python
# backend/config/settings/production.py

STORAGES = {
    'default': {
        'BACKEND': 'django_storages.backends.http.HttpStorage',
        'OPTIONS': {
            'base_url': 'https://xxxxx.supabase.co/storage/v1/object/public/media/',
        }
    }
}
```

### **Opción 2: AWS S3 (Escalabilidad)**

```python
# Mismo archivo production.py (ya incluido arriba)
```

### **Flujo de carga:**

```python
# models.py
class Evidence(models.Model):
    file = models.FileField(upload_to='evidence/%Y/%m/')  # Auto-organiza
    
    def save(self, *args, **kwargs):
        # Validar tipo archivo
        if not self.file.name.endswith(('.pdf', '.docx', '.xlsx', '.jpg', '.png')):
            raise ValidationError('Solo PDF, Word, Excel, imágenes permitidas')
        super().save(*args, **kwargs)
```

---

## 🔄 Flujo Completo de Despliegue

```
1. Dev en feature branch
   └─→ git push origin feature/auth

2. GitHub Actions:
   ├─ Corre tests
   └─ Corre linter

3. Pull Request (code review)
   ├─ Aprobación requerida
   └─ Merge a master

4. GitHub Actions:
   ├─ Corre tests nuevamente
   ├─ Build Docker (opcional)
   └─ Notifica Render

5. Render (automático):
   ├─ Pull código actualizado
   ├─ pip install -r requirements.txt
   ├─ python manage.py migrate
   ├─ python manage.py collectstatic
   ├─ python manage.py compress (si lo usas)
   └─ Reinicia con gunicorn

6. Vercel (si frontend cambió):
    ├─ Detecta cambios en /frontend
   ├─ npm install
   ├─ npm run build
   └─ Deploy automático

7. Resultado:
   ├─ https://api.midominio.com (backend)
   ├─ https://midominio.com (frontend)
   └─ Aplicación actualizada en producción
```

---

## 📊 Monitoreo en Producción

### **Render Logs**
```bash
# Ver logs en tiempo real
# Dashboard → Tu Web Service → Logs
```

### **Health Check (recomendado)**

```python
# Django endpoint simple
# apps/utils/views.py

from django.http import JsonResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'database': 'connected',
        'timestamp': timezone.now()
    })

# urls.py
path('health/', health_check, name='health-check'),
```

### **Sentry para errores**

```bash
pip install sentry-sdk
# Configurar (ver settings/production.py arriba)
# Dashboard en sentry.io
```

---

## 🚀 Costos Proyectados

| Fase | Componente | Costo/mes | Total |
|------|---|---|---|
| **MVP (1-3 meses)** | Render Web ($12) + DB ($15) | | **$27** |
| **Growth (3-6 meses)** | Render escala x2 ($24) + DB crece ($20) + S3 ($5) | | **$49** |
| **Escala (6+ meses)** | Render dedicado ($50) + DB SSD ($30) + S3 ($10) + CDN ($10) | | **$100** |

**Nota:** Vercel Frontend siempre gratis para este proyecto

---

## ⚠️ Riesgos y Mitigación

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|---|---|---|
| Render redeploy fallido | Media | Alto | GitHub Actions notifica, reverter fácil |
| PostgreSQL cae | Baja | Crítico | Backups automáticos diarios, snapshots |
| S3 bucket compromised | Media | Alto | Política IAM restrictiva, rotación keys |
| JWT token stolen | Media | Medio | Expiración corta, refresh rotation |
| DDoS | Baja | Alto | Cloudflare DDoS protection (free tier) |
| CORS mal configurado | Baja | Medio | Tests en CI validan CORS |

---

## ✅ Checklist Pre-Lanzamiento

- [ ] Tests pasan en CI
- [ ] Settings.production.py configurado
- [ ] SECRET_KEY generada (mínimo 50 chars)
- [ ] Database PostgreSQL creada en Render
- [ ] Variables de entorno en Render UI
- [ ] Migraciones executadas (`python manage.py migrate`)
- [ ] SuperUser creado
- [ ] ALLOWED_HOSTS correcto
- [ ] CORS configurado para frontend específico
- [ ] SSL/HTTPS funcionando
- [ ] Frontend en Vercel deploys correctamente
- [ ] API calls desde frontend al backend funcionan
- [ ] Autenticación JWT funciona end-to-end
- [ ] Carga de archivos funciona
- [ ] Logs aparecen en Render dashboard
- [ ] Health check endpoint responde

---

## 📞 Próximos Pasos

1. **Crear variables de entorno**: Generar SECRET_KEY, JWT_SECRET_KEY
2. **Provisionar PostgreSQL**: En Render (5 min)
3. **Configurar Django settings**: production.py (30 min)
4. **Configurar Render Web Service**: (15 min)
5. **Ejecutar migraciones**: (5 min)
6. **Deploy frontend**: Vercel (10 min)
7. **Testing end-to-end**: Login → CRUD → Upload data
8. **Validación**: Verificar logs, performance, seguridad

---

**¿Estás listo para empezar la implementación?** Me puedo ayudarte con:
- Generación de SECRET_KEY
- Configuración exacta de variables
- Troubleshooting si algo falla
- Optimizaciones de performance
