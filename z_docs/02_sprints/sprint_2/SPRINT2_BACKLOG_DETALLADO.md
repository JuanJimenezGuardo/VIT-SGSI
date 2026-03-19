# Sprint 2 - Backlog Detallado (BD-First)

Duracion: 2 semanas (11-24 marzo)
Objetivo: Cerrar el modelo de datos solicitado por ingenieria y dejar BD estable.
Responsable Backend core (Juan Jose Jimenez Guardo): Juan Jose Jimenez Guardo

Nota: documento actualizado retrospectivamente al cierre tecnico de Sprint 2.

## Politica de Prioridad

Durante este sprint se trabaja primero persistencia.

API y frontend pueden recibir ajustes puntuales si son necesarios para validar el esquema y reducir retrabajo.

## Alcance Tecnico Congelado

- Company
- Contact
- Project
- ProjectUser
- ProjectContact
- Phase
- Task
- Document
- Asset (sin rediseño)

## Backlog Operativo por Persona y Dia

| Dia | Juan Jose Jimenez Guardo (Backend core + arquitectura) | Osky (Backend persistencia) | Luis (Frontend) |
| --- | --- | --- | --- |
| Dia 1 | Cerrar modelo final y arrancar Contact | Preparar base de migraciones y campos planned/actual | Congelar nuevas vistas y revisar impacto UI |
| Dia 2 | Terminar Contact y empezar ProjectContact | Implementar work_notes y ajustar relaciones existentes | Mapear payload esperado |
| Dia 3 | Implementar validaciones de ProjectContact | Implementar Document | Documentar ajustes de contrato |
| Dia 4 | Abrir serializers/viewsets minimos de Contact y ProjectContact | Crear migraciones estructurales | Pruebas de compatibilidad |
| Dia 5 | Probar constraints criticos y flujo backend core | Ejecutar data migration legacy Company -> Contact | Soporte a validacion de contrato |
| Dia 6 | Ajustes por hallazgos de migracion | Corregir issues de migracion y consistencia | Corregir bugs criticos |
| Dia 7 | Refinar contrato API para apertura minima | Validar integridad de relaciones en BD | Ajustar mapeo UI/API |
| Dia 8 | Endpoints minimos listos para validacion | Datos de prueba y verificacion post-migracion | Preparar integracion de consumo API |
| Dia 9 | Cierre tecnico de backend core y checklist | Verificacion final de migraciones limpias | Integrar API minima |
| Dia 10 | Aprobacion de cierre BD y handoff a Sprint 3 | Soporte de estabilizacion final | Validacion funcional de integracion |

## Lista de Tareas Operativas

- [x] Actualizar models de companies/projects/phases/tasks.
- [x] Crear app contacts (o modulo en companies, segun decision final).
- [x] Crear app documents (o modulo en projects, segun decision final).
- [x] Crear y ejecutar migraciones.
- [x] Ejecutar data migration legacy.
- [x] Ejecutar validaciones tecnicas.

## Responsables por Rol en Sprint 2

### Juan Jose Jimenez Guardo - Arquitectura + Backend core + implementacion

- Implementar Contact.
- Implementar ProjectContact.
- Implementar validaciones de negocio y constraints criticos.
- Implementar serializers/viewsets minimos de Contact y ProjectContact.
- Revisar diseno final y aprobar cierre tecnico.

### Osky - Backend persistencia + soporte de integracion

- Implementar Document.
- Aplicar cambios planned/actual y work_notes donde corresponde.
- Crear migraciones estructurales y ejecutar data migration legacy.
- Validar constraints y consistencia de relaciones en BD.
- Corregir issues de migracion y estabilidad.

### Luis - Frontend

- Freeze de nuevas pantallas durante cierre BD (salvo bugs criticos).
- Preparar mapeo de pantallas contra contrato de datos final.
- Integrar API minima cuando backend este estable.
- Reportar ajustes necesarios de contrato durante integracion.

## Validaciones Obligatorias

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py check
python manage.py showmigrations
```

## Definicion de BD Cerrada

- [x] Diagrama final aprobado.
- [x] Models definitivos aprobados.
- [x] Migraciones limpias.
- [x] Data migration legacy validada.
- [x] Constraints probados.
- [x] Sin cambios pendientes en nombres, relaciones o enums.

## Riesgo que Evita este Plan

- Cambios de payload a mitad de desarrollo.
- Retrabajo de frontend por cambios de API.
- Rotura de migraciones por cambios tardios de esquema.
