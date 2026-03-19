# Sprint 2 - Quick Reference (BD-First)

Periodo: 11-24 marzo 2026
Objetivo: Cerrar y validar el modelo de base de datos antes de abrir API y frontend.

Nota: documento actualizado retrospectivamente al cierre tecnico de Sprint 2.

## Regla Operativa del Sprint

Se prioriza cierre de BD.

Se permiten cambios puntuales en API y frontend cuando sean necesarios para validar el modelo y estabilizar el contrato de datos.

Durante la etapa de cierre BD (dias 1-8) se evita abrir nuevas pantallas; se permiten solo ajustes puntuales para validar contrato de datos.

## Estado Real de Avance

- Sprint 1: Completado.
- Assets: Integrado en backend y migrado.
- Contact, ProjectContact y Document: implementados.
- Fechas planned/actual en Project-Phase-Task: implementadas.
- Migraciones estructurales: creadas y aplicadas en entorno local.
- Sprint 2: cierre tecnico completado y handoff operativo a Sprint 3.

## Alcance Congelado de Modelo

- Company
- Contact
- Project
- ProjectUser
- ProjectContact
- Phase
- Task
- Document
- Asset (sin rediseño en esta iteracion)

## Cambios de Esquema Obligatorios

- Company deja de ser dueno de contact_person y contact_position.
- Project, Phase y Task incorporan planned_start_date, planned_end_date, actual_start_date, actual_end_date.
- Task incorpora work_notes.
- Document entra como entidad formal de trazabilidad.

## Registro Diario de Avance (10 dias)

La siguiente tabla refleja avance operativo real por dia para evitar mezclar pendientes con tareas ya ejecutadas.

| Dia | Juan Jose Jimenez Guardo (Backend core + arquitectura) | Osky (Backend persistencia) | Luis (Frontend) |
| --- | --- | --- | --- |
| Dia 1 | Se cerro modelo final y se arranco Contact | Se preparo base de migraciones y campos planned/actual | Se congelaron nuevas vistas y se reviso impacto UI |
| Dia 2 | Se termino Contact y se inicio ProjectContact | Se implemento work_notes y se ajustaron relaciones existentes | Se mapeo payload esperado por pantalla |
| Dia 3 | Se implementaron validaciones de ProjectContact | Se implemento Document | Se documentaron ajustes de contrato UI/API |
| Dia 4 | Se abrieron serializers/viewsets minimos de Contact y ProjectContact | Se crearon migraciones estructurales | Se realizaron pruebas de compatibilidad de payload |
| Dia 5 | Se probaron constraints criticos y flujo backend core | Se ejecuto data migration legacy Company -> Contact | Se dio soporte a validacion de contrato |
| Dia 6 | Se ajustaron validaciones por hallazgos de migracion | Se corrigieron issues de migracion y consistencia | Se corrigieron bugs criticos |
| Dia 7 | Se refino contrato API para apertura minima | Se valido integridad de relaciones en BD | Se ajusto mapeo UI/API con contrato final |
| Dia 8 | Se dejaron endpoints minimos listos para validacion | Se cargaron datos de prueba y verificacion post-migracion | Se preparo integracion final de consumo API |
| Dia 9 | Se ejecuto cierre tecnico de backend core y checklist | Se realizo verificacion final de migraciones limpias | Se integro consumo de API minima |
| Dia 10 | Se formalizo cierre BD y handoff a Sprint 3 | Se dio soporte de estabilizacion final | Se valido integracion funcional |

## Asignacion Operativa por Persona (Sprint 2)

### Juan Jose Jimenez Guardo - Arquitectura + Backend core + implementacion

- Implementar Contact.
- Implementar ProjectContact.
- Implementar validaciones de negocio y constraints criticos.
- Implementar serializers/viewsets minimos de Contact y ProjectContact.
- Revisar diseno final y aprobar cierre tecnico del sprint.

### Osky - Backend persistencia + soporte de integracion

- Implementar Document.
- Agregar campos planned_start_date, planned_end_date, actual_start_date, actual_end_date.
- Agregar work_notes.
- Crear migraciones estructurales.
- Ejecutar data migration legacy Company -> Contact.
- Validar integridad y corregir issues de migracion.

### Luis - Frontend

- Freeze de nuevas pantallas durante fase de cierre BD.
- Correccion de bugs criticos.
- Mapeo de contrato UI/API.
- Integracion final cuando backend este estable.

## Comandos Clave

```bash
cd backend

# 1) Crear migraciones del cambio de modelo
python manage.py makemigrations

# 2) Aplicar migraciones
python manage.py migrate

# 3) Validar proyecto
python manage.py check

# 4) Inspeccion de modelo
python manage.py shell

# 5) Ver estado de migraciones
python manage.py showmigrations
```

## Checklist de Cierre de BD

- [x] Diagrama final aprobado.
- [x] Models definitivos aprobados.
- [x] Migraciones limpias en entorno local.
- [x] Data migration legacy validada.
- [x] Constraints probados.
- [x] Sin cambios pendientes en nombres, relaciones ni enums.

## Criterio de Hecho del Sprint 2

Sprint 2 se considera exitoso si la BD queda estable y aprobada, incluso si API y frontend quedan para la siguiente iteracion.

Esto minimiza retrabajo y evita romper contratos de datos.
