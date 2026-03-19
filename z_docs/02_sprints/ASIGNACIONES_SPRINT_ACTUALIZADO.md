# Asignaciones por Sprint (Sprint 1-6)

ESTRUCTURA DEL PROYECTO:
- Sprint 1 (COMPLETADO): objetivos de seguridad backend cerrados; frontend continua en integracion planificada
- Sprints 2-6: En ejecucion con plan operativo por persona y prioridad de base de datos

Responsable Backend core (Juan Jose Jimenez Guardo): Juan Jose Jimenez Guardo.

IMPORTANTE: Todos los sprints estan condicionados por la arquitectura de produccion definida en ARQUITECTURA_DESPLIEGUE_PRODUCCION.md.

---

## SPRINT 1 (19 feb -> 2 mar) - Seguridad Base + Auth [COMPLETADO]

Objetivo: Pasar de API abierta a plataforma con control de acceso real.

Estado: Completado.

---

## SPRINT 2 (11 mar -> 24 mar) - BD + refactor + migraciones [CIERRE TECNICO COMPLETADO]

Nota: documento actualizado retrospectivamente al cierre tecnico de Sprint 2.

Objetivo del sprint:
Cerrar modelo de base de datos para alinearlo con requerimientos del ingeniero y mockups.

Regla del sprint:
Se prioriza cierre de BD, pero se permiten cambios puntuales en API y frontend cuando sean necesarios para validar el modelo y evitar retrabajo.

### Alcance congelado de entidades

- Company
- Contact
- Project
- ProjectUser
- ProjectContact
- Phase
- Task
- Document
- Asset (sin rediseño)

### Asignaciones por rol

#### Juan Jose Jimenez Guardo (Arquitectura + Backend core + implementacion)

- [x] Implementar Contact
- [x] Implementar ProjectContact
- [x] Implementar validaciones de negocio y constraints criticos
- [x] Implementar serializers/viewsets minimos de Contact y ProjectContact
- [x] Cerrar diseno final y aprobar cierre tecnico

#### Osky (Backend persistencia + soporte de integracion)

- [x] Implementar Document
- [x] Agregar fechas planned/actual en Project, Phase y Task
- [x] Agregar work_notes en Task
- [x] Crear migraciones estructurales
- [x] Ejecutar data migration legacy Company -> Contact
- [x] Validar integridad y corregir issues de migracion

#### Luis (Frontend)

- [x] Congelar nuevas pantallas durante etapa de cierre BD
- [x] Corregir solo bugs criticos
- [x] Preparar mapa de pantallas para contrato de datos final
- [x] Iniciar integracion cuando la BD este estable; la aprobacion formal se registra al cierre tecnico

### Plan semanal

Semana 1:
- [x] Dia 1: Juan Jose Jimenez Guardo cierra modelo y arranca Contact; Osky prepara migraciones base y planned/actual; Luis congela nuevas vistas
- [x] Dia 2: Juan Jose Jimenez Guardo termina Contact e inicia ProjectContact; Osky implementa work_notes; Luis mapea payload
- [x] Dia 3: Juan Jose Jimenez Guardo implementa validaciones de ProjectContact; Osky implementa Document; Luis documenta ajustes de contrato
- [x] Dia 4: Juan Jose Jimenez Guardo abre serializers/viewsets minimos; Osky crea migraciones estructurales; Luis hace pruebas de compatibilidad
- [x] Dia 5: Juan Jose Jimenez Guardo prueba constraints criticos; Osky ejecuta data migration legacy; Luis soporta validacion de contrato

Semana 2:
- [x] Dia 6: Juan Jose Jimenez Guardo ajusta validaciones por hallazgos; Osky corrige issues de migracion; Luis corrige bugs criticos
- [x] Dia 7: Juan Jose Jimenez Guardo refina contrato API; Osky valida integridad de relaciones; Luis ajusta mapeo UI/API
- [x] Dia 8: Juan Jose Jimenez Guardo deja endpoints minimos listos; Osky verifica post-migracion; Luis prepara integracion final
- [x] Dia 9: Juan Jose Jimenez Guardo cierra checklist tecnico; Osky verifica migraciones limpias; Luis integra API minima
- [x] Dia 10: Juan Jose Jimenez Guardo aprueba cierre BD; Osky da soporte final; Luis valida integracion funcional

### Criterio de cierre de Sprint 2

- [x] Diagrama final aprobado
- [x] Models definitivos aprobados
- [x] Migraciones limpias
- [x] Data migration legacy validada
- [x] Constraints probados
- [x] API habilitada solo despues de estabilidad de esquema

---

## SPRINT 3 (25 mar -> 7 abr) - API + integracion frontend

Consolidar APIs de entidades del core y cerrar integracion frontend sobre el contrato de datos estabilizado en Sprint 2.

---

## SPRINT 4 (8 abr -> 21 abr) - Riesgos

Inicia con base en BD estable y APIs core integradas.

---

## SPRINT 5 (22 abr -> 5 may) - SoA + ISO Controls

Dependiente de cierre de Sprint 4.

---

## SPRINT 6 (6 may -> 19 may) - Evidence + Audit + Reportes

Dependiente de cierre de Sprint 5 y orientado a demo final.
