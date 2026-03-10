# ARQUITECTURA DE GESTIÓN DE RIESGOS — VIT

> **Nota de contexto (al 18-02-2026):** el backend cuenta con Users/Companies/Projects/Phases/Tasks. Los módulos SGSI (Scope, Asset, Risk, ISOControl, SoAItem, Evidence, Report, AuditLog) están definidos a nivel documental y se implementarán en las siguientes iteraciones.
## Alineación con ISO/IEC 27001:2022
Versión: 1.0 | Fecha: febrero de 2026

---

## Tabla de Contenidos

- [Fundamentación ISO 27001](#fundamentación-iso-27001)
- [Modelo de Riesgo Dual](#modelo-de-riesgo-dual)
- [Ciclo de Vida del Riesgo](#ciclo-de-vida-del-riesgo)
- [Escalas de Evaluación](#escalas-de-evaluación)
- [Matriz de Riesgos](#matriz-de-riesgos)
- [Tratamiento de Riesgos](#tratamiento-de-riesgos)
- [Integración con Controles ISO](#integración-con-controles-iso)
- [Casos de Uso](#casos-de-uso)
- [Métricas y KPIs de Riesgo](#métricas-y-kpis-de-riesgo)
- [Integración en Proceso VIT](#integración-en-proceso-vit)

---

## Fundamentación ISO 27001

ISO 27001:2022 define el proceso de gestión de riesgos de seguridad de la información. El modelo VIT implementa las fases clave:

### Fases Mandatorias ISO 27001

- Identificación de riesgos: activos, amenazas, vulnerabilidades
- Análisis de riesgos: calcular riesgo inherente
- Evaluación de riesgos: comparar contra criterios aceptables
- Tratamiento de riesgos: mitigar, evitar, transferir o aceptar
- Comunicación y consulta: documentación y decisiones
- Monitoreo y revisión: seguimiento continuo
- Documentación: trazabilidad en SoAItem y evidencia

**Diferencia crítica**:

- **Incorrecto (modelo simplista)**
```
Puntaje de riesgo = Probabilidad x Impactoo
(Un solo cálculo, no diferencia controles)
```

- **Correcto (ISO 27001 completo)**
```
Riesgo INHERENTE = Probabilidad_sin_controles x Impacto
Riesgo RESIDUAL  = Probabilidad_con_controles x Impacto
Efectividad      = Inherente - Residual
```

---

## Modelo de Riesgo Dual

### Concepto: Antes y Después de Controles

ISO 27001 usa un modelo dual para demostrar el beneficio real de los controles.

#### Fase 1: Riesgo inherente (línea base)

**Pregunta**: «Cuál es el riesgo si no implemento ningún control?»

Ejemplo:
```
Activo: Base de datos de clientes
Amenaza: Acceso no autorizado
Vulnerabilidad: SQL injection en app

Probabilidad: 5 (Muy alta)
Impacto: 5 (Muy alto)
PUNTAJE DE RIESGO INHERENTE = 25
```

#### Fase 2: Controles seleccionados

**Pregunta**: «¿Qué controles ISO 27001 mitigan este riesgo?»

Ejemplo:
```
Riesgo -> A.5.15 Control de acceso / A.5.18 Derechos de acceso
Riesgo -> A.8.24 Uso de criptografía
Riesgo -> A.6.3 Concientización, educación y capacitación
SoAItem.implementation_status = IN_PROGRESS
```

#### Fase 3: Riesgo RESIDUAL (post-controles)

**Pregunta**: «Cuál es el riesgo despues de implementar controles?»

Ejemplo:
```
Probabilidad: 2 (Baja)
Impacto: 5 (Muy alto)
RESIDUAL RISK SCORE = 10
Efectividad = 25 - 10 = 15
```

### Ventajas del modelo dual

- Justifica la inversion (reduccion cuantificable)
- Permite KPIs de seguridad
- Facilita decisiones costo-beneficio
- Documenta riesgos aceptados

---

## Ciclo de Vida del Riesgo

### Estados del Riesgo (Risk.status)

- **IDENTIFIED**: riesgo registrado, sin análisis profundo
- **ASSESSED**: riesgo evaluado con controles seleccionados
- **MITIGATED**: controles implementados y evidencias cargadas
- **MONITORED**: seguimiento continuo post-implementación

**Transiciones**:
```
IDENTIFIED -> ASSESSED -> MITIGATED -> MONITORED
(ACCEPT)   -> MONITORED
```

### Estados vs fases del proyecto

| Fase Proyecto | Estado Riesgo | Actividad |
|---|---|---|
| PLANNING | IDENTIFIED | Identificar riesgos |
| PLANNING | ASSESSED | Analizar y seleccionar controles |
| IN_PROGRESS | MITIGATED | Implementar controles y evidencias |
| COMPLETED | MONITORED | Revision y mejora continua |

---

## Escalas de Evaluación

### Escala de Verosimilitud (Probabilidad)

| Nivel | Valor | Descripción | Ejemplo |
|---|---:|---|---|
| Muy Baja | 1 | Casi nunca ocurre | WAF y MFA en todos los accesos |
| Baja | 2 | Raro pero posible | Phishing con MFA habilitado |
| Media | 3 | Puede ocurrir | Malware ocasional |
| Alta | 4 | Probable | Acceso no autorizado sin logs |
| Muy Alta | 5 | Muy probable | Brecha por credenciales expuestas |

### Escala de Impactoo (Impacto)

| Nivel | Valor | Descripción | Ejemplo |
|---|---:|---|---|
| Muy Bajo | 1 | Daño mínimo | Caida < 1 hora |
| Bajo | 2 | Impactoo limitado | Filtracion no sensible |
| Medio | 3 | Impactoo operacional | Caida 4-8 horas |
| Alto | 4 | Impactoo significativo | Datos sensibles comprometidos |
| Muy Alto | 5 | Catastrófico | Perdida crítica e irreversible |

**Impactoo CIA**: Impacto = max(Impacto_C, Impacto_I, Impacto_A)

---

## Matriz de Riesgos

### Matriz inherente (sin controles)

| Probabilidad \ Impacto | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 1 | 1 | 2 | 3 | 4 | 5 |
| 2 | 2 | 4 | 6 | 8 | 10 |
| 3 | 3 | 6 | 9 | 12 | 15 |
| 4 | 4 | 8 | 12 | 16 | 20 |
| 5 | 5 | 10 | 15 | 20 | 25 |

### Matriz residual (con controles)

La matriz residual usa el mismo cálculo, pero con Probabilidad ajustado por controles:

| Probabilidad \ Impacto | 1 | 2 | 3 | 4 | 5 |
|---|---:|---:|---:|---:|---:|
| 1 | 1 | 2 | 3 | 4 | 5 |
| 2 | 2 | 4 | 6 | 8 | 10 |
| 3 | 3 | 6 | 9 | 12 | 15 |
| 4 | 4 | 8 | 12 | 16 | 20 |
| 5 | 5 | 10 | 15 | 20 | 25 |

### Tolerancia de riesgo (risk appetite)

```
if inherent_risk_score > THRESHOLD:
  treatment != ACCEPT

if residual_risk_score > THRESHOLD:
  require_approval = True
```

---

## Tratamiento de Riesgos

### MITIGATE (Mitigar)

- Implementar controles para reducir Probabilidad o Impacto
- Ejemplo:
```
Riesgo: Acceso no autorizado a BD
Inherente: 25
Controles: MFA, cifrado, logging
Residual: 10
Reduccion: 15
```

### AVOID (Evitar)

- Cambiar proceso o arquitectura para eliminar el riesgo
- Ejemplo:
```
Riesgo: Datos sensibles en servidor publico
Decision: mover a red privada
Residual: 0
```

### TRANSFER (Transferir)

- Transferir responsabilidad a terceros (seguro, proveedor)
- Ejemplo:
```
Riesgo: Incendio en data center
Decision: seguro y DR externo
Residual (empresa): 0
```

### ACCEPT (Aceptar)

- Documentar el riesgo como aceptable
- Ejemplo:
```
Riesgo: Robo fisico de laptop
Inherente: 6
Residual: 6
Decision: ACCEPT (documentado y aprobado)
```

---

## Integración con Controles ISO

### Mapeo N:M: Risk <-> ISOControl

```
Risk --(N:M)--> ISOControl
Risk --(N:M)--> SoAItem (via ISOControl)
```

**Reglas en VIT**:

- Cada Risk puede vincular multiples ISOControl
- Cada ISOControl puede mitigar multiples Risk
- SoAItem refleja la aplicabilidad y estado de implementación
- Evidence valida la mitigacion

**Ejemplo**:
```
Risk: "Acceso no autorizado a BD"
- A.5.15 Control de acceso (y A.5.18 Derechos de acceso)
- A.8.24 Uso de criptografía
- A.6.3 Concientización, educación y capacitación
```

---

## Casos de Uso

### Caso 1: Evaluación de riesgo (e-commerce)

**Contexto**: empresa con pagos en linea y datos PCI.

**Identificación**:
```
Risk.create(
  name="Exposicion de datos de tarjeta",
  category="COMPLIANCE",
  inherent_likelihood=5,
  inherent_impact=5
)
```

**Análisis**:
```
Controles:
- A.5.15 Control de acceso (y A.5.18 Derechos de acceso) (MFA)
- A.8.24 Uso de criptografía (AES)
- A.8.15 Registro de eventos y A.8.16 Monitoreo de actividades

Residual:
- residual_likelihood=2
- residual_impact=5
- residual_risk_score=10
```

**Tratamiento**:
```
Risk.treatment = "MITIGATE"
Risk.mitigation_plan = "MFA + AES + SIEM"
```

**Monitoreo**:
```
SoAItems IMPLEMENTED -> Risk.status = "MITIGATED"
```

### Caso 2: Riesgo aceptado (oficina)

**Contexto**: pyme con riesgo bajo de robo fisico.

```
Risk.create(
  name="Robo fisico de laptops",
  inherent_likelihood=2,
  inherent_impact=2,
  inherent_risk_score=4,
  treatment="ACCEPT",
  status="MONITORED"
)
```

---

## Métricas y KPIs de Riesgo

### Dashboard de riesgos

```
Total riesgos: 24
- IDENTIFIED: 6
- ASSESSED: 10
- MITIGATED: 6
- MONITORED: 2

Promedio:
- inherent_risk_score: 12
- residual_risk_score: 6
- efectividad promedio: 50%
```

### Tendencias

```
Q1: inherent=120, residual=80
Q2: inherent=120, residual=60
Q3: inherent=120, residual=45
Q4: inherent=120, residual=30
```

---

## Integración en Proceso VIT

**Timeline integrado**:

| Semana | Fase | Actividad de Riesgo | Deliverable |
|---:|---|---|---|
| 1-2 | Assessment | Identificación + inventario de activos | Risk register |
| 3-4 | Planning | Análisis inherente + controles | Risk assessment |
| 5-8 | Implementation | Evidencias + residual | Risk mitigado |
| 9+ | Completion | Revision y monitoreo | Risk report |

---

**Documento preparado por el equipo de desarrollo VIT**
**Última revisión**: febrero 2024
**Referencia normativa**: ISO 27001:2022
