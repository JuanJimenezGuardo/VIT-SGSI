# Estado actual del proyecto VIT (al 18-02-2026)

## Resumen ejecutivo del avance
- **Backend operativo:** Users, Companies, Projects, Phases, Tasks (Django + DRF).
- **Autenticación/autorización:** pendiente activar (JWT/RBAC).
- **Frontend:** estructura base (Vite) sin páginas/componentes.
- **ERD:** existe y debe ampliarse/validarse para cubrir el núcleo SGSI.

## Brechas clave frente a ISO/IEC 27001 (núcleo SGSI)
Pendiente implementar y demostrar en funcionamiento:
- **Scope** (alcance del SGSI por proyecto).
- **Asset** (inventario de activos).
- **Risk** (metodología formal: probabilidad/impacto, inherente/residual, tratamiento).
- **ISOControl** (catálogo de 93 controles) y **SoAItem** (SoA por proyecto).
- **Evidence/Document** (subida, estados, vinculación a controles).
- **Report** (resúmenes y evidencias de avance).
- **AuditLog** (trazabilidad de cambios críticos).

## Próximos pasos recomendados (orden de implementación)
1. **Auth/JWT + RBAC + ProjectUser** (seguridad del sistema y segregación por proyecto).
2. **Scope + Asset** (base del SGSI).
3. **Risk** (inherente/residual) + relación Risk↔Asset.
4. **ISOControl + SoA** autogenerado por proyecto.
5. **Evidence + AuditLog** (toda acción crítica debe quedar registrada).
6. **Reportes** (JSON primero; PDF si el tiempo lo permite) y dashboards.

## Evidencia que se debe mostrar en la próxima revisión
- ERD completo (incluyendo SGSI) + cardinalidades.
- Ejemplo de trazabilidad: **riesgo → control/SoA → evidencia → reporte → auditoría**.
