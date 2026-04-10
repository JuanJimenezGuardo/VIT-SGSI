# Plataforma SGSI ISO 27001:2022

Repositorio publico de portafolio para mostrar la implementacion tecnica de una plataforma web orientada a la gestion de SGSI bajo ISO 27001:2022.

El desarrollo operativo y la coordinacion del proyecto se realizaron en un repositorio privado. Esta version publica conserva el codigo y la documentacion tecnica utiles para evaluacion profesional, sin exponer activos sensibles.

## Objetivo

Desarrollar una plataforma que permita estructurar el trabajo de implementacion de SGSI con foco en:

- gestion de proyectos, fases y tareas
- control de usuarios por rol
- trazabilidad y auditoria
- gestion de activos y riesgos
- base para controles, SoA y evidencia documental

## Rol Tecnico

- liderazgo tecnico y coordinacion de entregables
- definicion de alcance y criterios de cierre por sprint
- implementacion de modulos backend y validaciones de negocio
- integracion y estabilizacion de flujos backend/frontend

## Arquitectura

La solucion se planteo desde fases tempranas con criterios de despliegue real:

- frontend: React + Vite
- backend: Django + Django REST Framework
- autenticacion: JWT con SimpleJWT
- base de datos: PostgreSQL
- despliegue previsto: Vercel (frontend) y Render (backend)
- almacenamiento de archivos: S3 compatible

## Estado del Proyecto

El proyecto se trabaja por sprints con avances funcionales acumulativos. El repositorio publico incluye implementaciones y pruebas representativas de los modulos principales.

## Alcance de Esta Version Publica

- codigo de aplicacion backend y frontend
- pruebas de validacion por modulo
- documentos tecnicos de referencia para portafolio

No se publica documentacion interna de gestion, credenciales ni contenido confidencial.

## Ejecucion Local

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Pruebas

Ejemplo de ejecucion de suites por app:

```bash
cd backend
python manage.py test apps.users.tests apps.companies.tests apps.projects.tests apps.phases.tests apps.tasks.tests
```

## Referencias

- Django: https://docs.djangoproject.com/en/4.2/
- Django REST Framework: https://www.django-rest-framework.org/
- SimpleJWT: https://django-rest-framework-simplejwt.readthedocs.io/
- ISO 27001: https://www.iso.org/standard/27001

Estado: repositorio publico de portafolio tecnico.
