# ESTRATEGIA DE AUDITORÍA Y SEGURIDAD — VIT

> **Nota de contexto (al 18-02-2026):** el backend cuenta con Users/Companies/Projects/Phases/Tasks. Los módulos SGSI (Scope, Asset, Risk, ISOControl, SoAItem, Evidence, Report, AuditLog) están definidos a nivel documental y se implementarán en las siguientes iteraciones.
## Trazabilidad, registro de eventos, monitoreo e integridad (alineado con ISO/IEC 27001:2022)
**Versión:** 1.1  
**Fecha:** 18-02-2026

---

## Tabla de contenidos
1. [Alcance](#alcance)  
2. [Referentes normativos](#referentes-normativos)  
3. [Objetivos de la auditoría en VIT](#objetivos-de-la-auditoría-en-vit)  
4. [Diseño del registro de auditoría (AuditLog)](#diseño-del-registro-de-auditoría-auditlog)  
5. [Eventos auditables (qué se registra)](#eventos-auditables-qué-se-registra)  
6. [Implementación técnica (Django)](#implementación-técnica-django)  
7. [Monitoreo y revisión periódica](#monitoreo-y-revisión-periódica)  
8. [Integridad criptográfica y sincronización de reloj](#integridad-criptográfica-y-sincronización-de-reloj)  
9. [Retención y archivamiento](#retención-y-archivamiento)  
10. [Seguridad de los registros (acceso y segregación)](#seguridad-de-los-registros-acceso-y-segregación)  
11. [Evidencia típica para auditoría externa](#evidencia-típica-para-auditoría-externa)  
12. [Mapa ISO → VIT (controles y evidencias)](#mapa-iso--vit-controles-y-evidencias)

---

## Alcance
Esta estrategia aplica a la plataforma **VIT** (backend REST en Django/DRF y cualquier servicio auxiliar) y cubre:

- Registro de actividades relevantes y eventos de seguridad.
- Monitoreo y revisión para detección de comportamientos anómalos.
- Integridad, retención y control de acceso de los registros.

> Nota de consistencia: en ISO/IEC 27001:2022 las **cláusulas** corresponden a los apartados 4–10 del estándar; **los controles** están en el **Anexo A**. En este documento se citan controles del Anexo A (p. ej., *8.15, 8.16*), no «Clause A.8…».

---

## Referentes normativos
### ISO/IEC 27001:2022 (Anexo A)
Los controles del Anexo A en la edición 2022 se reorganizan (alineados con ISO/IEC 27002:2022) y se consolidan en **93 controles** agrupados en **cuatro temas**.  
En particular, para auditoría y trazabilidad, VIT se apoya en:

- **A.8.15 — Registro (logs)**: producir, proteger y analizar registros de eventos relevantes.
- **A.8.16 — Actividades de monitoreo**: monitorear redes, sistemas y aplicaciones para detectar comportamientos anómalos y evaluar incidentes potenciales.
- **A.8.17 — Sincronización de reloj**: mantener sincronía temporal para que los registros sean comparables y confiables.
- **A.8.24 — Uso de criptografía**: proteger información (incluyendo registros) en tránsito y en reposo, según el riesgo.

### Normativa colombiana (si aplica por jurisdicción / datos personales)
Si VIT trata **datos personales** en Colombia, el marco general es la **Ley 1581 de 2012** y su reglamentación (p. ej., Decreto 1377 de 2013, con compilaciones posteriores). Para datos financieros/crediticios, aplica la **Ley 1266 de 2008** (según el caso de uso).

---

## Objetivos de la auditoría en VIT
1. **Trazabilidad completa**: «quién / qué / cuándo / dónde / sobre qué» para cambios y acciones críticas.
2. **Soporte de investigación**: facilitar análisis forense y respuesta a incidentes.
3. **Evidencia de cumplimiento**: demostrar controles operando (SGSI) durante auditorías internas/externas.
4. **Detección temprana**: habilitar monitoreo y alertas frente a patrones inusuales.

---

## Diseño del registro de auditoría (AuditLog)
### Principios de diseño
- **Cobertura**: registrar acciones críticas + eventos de seguridad (incluye intentos fallidos).
- **Inmutabilidad lógica (append-only)**: se permite **insertar**, no **editar** ni **borrar**.
- **Integridad**: posibilidad de verificar que los registros no fueron alterados (hash/HMAC y/o restricciones en BD).
- **Contexto**: incluir metadatos mínimos de sesión/red (IP, agente de usuario, request_id) para correlación.

### Campos recomendados (mínimo viable)
| Campo | Tipo | Ejemplo | Propósito |
|---|---|---|---|
| timestamp_utc | datetime | 2026-02-18T13:44:10Z | Línea de tiempo unificada |
| actor_user_id | FK nullable | 12 | Actor (si existe) |
| actor_snapshot | texto | «jose@empresa.com» | Persistir identidad aunque cambie el usuario |
| action | enum | CREATE/UPDATE/DELETE/APPROVE/REJECT/VIEW/EXPORT | Tipo de evento |
| entity | texto | Risk / Evidence / SoAItem | Modelo o recurso afectado |
| object_id | UUID/int | 9381 | Registro afectado |
| changes | JSON | before/after | Evidencia del cambio |
| outcome | enum | SUCCESS / FAIL | Resultado |
| ip_address | texto | 181.55.x.x | Correlación y detección |
| user_agent | texto | Chrome/… | Correlación |
| request_id | UUID | «…» | Trazabilidad transversal |

---

## Eventos auditables (qué se registra)
### 1) Autenticación y sesión
- Inicio/cierre de sesión (SUCCESS/FAIL)
- Cambios de contraseña / recuperación
- Bloqueo/desbloqueo de usuario
- Elevación de privilegios / cambio de rol

### 2) Cambios sobre entidades críticas del SGSI
- **Project / Scope**
- **Risk / Asset**
- **ISOControl (catálogo)**: lectura y asociación (no modificación si es «read-only»)
- **SoAItem** (aplicabilidad/justificación/estado)
- **Evidence / Document**: carga, reemplazo, versionado, descarga/expedición

### 3) Accesos de alto riesgo (lectura)
Cuando el riesgo lo amerite (por sensibilidad o auditoría), registrar eventos de tipo **VIEW / EXPORT / DOWNLOAD** sobre:
- PII (si aplica), evidencias, reportes, exportaciones masivas, archivos descargados.

### 4) Eventos de seguridad
- Denegaciones por permisos (403), accesos a endpoints restringidos
- Cambios de configuración de seguridad (p. ej., parámetros de retención, llaves, MFA)
- Actividad anómala detectada (evento sintético generado por el motor de monitoreo)

---

## Implementación técnica (Django)

### Modelo sugerido (Django ORM)
```python
from django.conf import settings
from django.db import models
from django.utils import timezone

class AuditAction(models.TextChoices):
    CREATE = "CREATE", "Crear"
    UPDATE = "UPDATE", "Actualizar"
    DELETE = "DELETE", "Eliminar"
    APPROVE = "APPROVE", "Aprobar"
    REJECT = "REJECT", "Rechazar"
    VIEW = "VIEW", "Ver"
    EXPORT = "EXPORT", "Exportar"
    LOGIN = "LOGIN", "Inicio de sesión"
    LOGOUT = "LOGOUT", "Cierre de sesión"

class AuditOutcome(models.TextChoices):
    SUCCESS = "SUCCESS", "Exitoso"
    FAIL = "FAIL", "Fallido"

class AuditLog(models.Model):
    # Tiempo (usar UTC en toda la plataforma)
    timestamp_utc = models.DateTimeField(default=timezone.now, db_index=True)

    # Actor
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="audit_events",
    )
    actor_snapshot = models.CharField(
        max_length=254,
        blank=True,
        help_text="Email/username al momento del evento (para trazabilidad histórica).",
    )

    # Qué ocurrió
    action = models.CharField(max_length=16, choices=AuditAction.choices, db_index=True)
    entity = models.CharField(max_length=64, db_index=True)  # p. ej., "Risk"
    object_id = models.CharField(max_length=64, blank=True, db_index=True)

    # Evidencia del cambio
    changes = models.JSONField(null=True, blank=True)  # {"field": {"before": ..., "after": ...}}
    outcome = models.CharField(
        max_length=8, choices=AuditOutcome.choices, default=AuditOutcome.SUCCESS
    )
    reason = models.CharField(max_length=255, blank=True)

    # Contexto técnico
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, blank=True)
    request_id = models.UUIDField(null=True, blank=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=["entity", "object_id", "timestamp_utc"]),
            models.Index(fields=["action", "timestamp_utc"]),
        ]

    def __str__(self):
        return f"{self.timestamp_utc} {self.action} {self.entity}:{self.object_id} ({self.outcome})"
```

### Cómo garantizar «append-only»
Recomendación por capas (se pueden combinar):

1. **Capa de aplicación**: no exponer endpoints de UPDATE/DELETE para AuditLog.
2. **Capa de permisos**: negar por defecto cualquier operación distinta de CREATE (interna).
3. **Capa de base de datos**: revocar UPDATE/DELETE a roles de aplicación y/o usar triggers de PostgreSQL que impidan modificaciones.

---

## Monitoreo y revisión periódica
### Objetivo
Convertir el registro (A.8.15) en una capacidad de **detección** (A.8.16): identificar anomalías y tomar acciones.

### Esquema recomendado
- **Diario (automático)**: reglas simples (alertas) para actividad anómala.
- **Semanal (operativo)**: revisión puntual de alertas y cierres.
- **Mensual (gestión)**: reporte consolidado (tendencias, hallazgos, acciones).

### Ejemplo de reglas (pseudocódigo Django)
```python
from datetime import timedelta
from django.utils import timezone
from django.db.models import Count

def audit_monitoring_review():
    since = timezone.now() - timedelta(days=1)

    # 1) Múltiples fallos de login por IP
    suspicious_ips = (
        AuditLog.objects.filter(action="LOGIN", outcome="FAIL", timestamp_utc__gte=since)
        .values("ip_address")
        .annotate(n=Count("id"))
        .filter(n__gte=10)
    )

    # 2) Actividad fuera de horario (ejemplo 00:00–05:00)
    after_hours = AuditLog.objects.filter(
        timestamp_utc__gte=since,
        timestamp_utc__hour__in=[0, 1, 2, 3, 4, 5],
        action__in=["UPDATE", "DELETE", "EXPORT"],
    )

    # 3) Cambios sensibles en SoA por usuarios no administradores
    soa_changes = AuditLog.objects.filter(
        timestamp_utc__gte=since,
        entity="SoAItem",
        action="UPDATE",
    ).exclude(actor__role="ADMIN")  # ajustar a tu modelo de roles

    return {
        "suspicious_ips": list(suspicious_ips),
        "after_hours": after_hours.count(),
        "soa_changes": soa_changes.count(),
    }
```

> Importante: el monitoreo debe generar **evidencias**: tickets, actas, correos o «issue logs» con fecha, analista, conclusión y acción correctiva.

---

## Integridad criptográfica y sincronización de reloj
### Sincronización de reloj (A.8.17)
- Usar NTP/servicio de tiempo en los servidores.
- Registrar siempre en **UTC**.
- Documentar el estándar de reloj (fuente NTP, tolerancia, verificación).

### Protección criptográfica (A.8.24)
- **En tránsito**: TLS (HTTPS) en toda comunicación.
- **En reposo**: cifrado de disco/volumen y/o cifrado a nivel de campo si aplica.
- **Integridad del registro** (opcional avanzado): hash encadenado o HMAC.

Ejemplo de hash encadenado (conceptual):
```python
import hashlib

def compute_hash(prev_hash: str, payload: str) -> str:
    data = (prev_hash + payload).encode("utf-8")
    return hashlib.sha256(data).hexdigest()
```

---

## Retención y archivamiento
ISO plantea conservar registros por un **«periodo acordado»** (definido por riesgo, contractual y normativa). En VIT se propone:

- **Online (consultable)**: 12 meses
- **Archivo (backup protegido)**: 24–36 meses
- **Eliminación segura**: al cumplir el periodo y si no hay investigación/hold legal

Estos valores se parametrizan por cliente/proyecto cuando sea necesario.

---

## Seguridad de los registros (acceso y segregación)
- Acceso por rol: **ADMIN/AUDITOR** (mínimo privilegio).
- **Meta-auditoría**: registrar también quién consulta/exporta AuditLog (evento VIEW/EXPORT sobre entity=AuditLog).
- Protección contra exfiltración: límites de exportación, ofuscación de IP si aplica, y aprobación para descargas masivas.

---

## Evidencia típica para auditoría externa
Un auditor normalmente pedirá:

- Política/procedimiento de registros y monitoreo (este documento + procedimientos operativos).
- Evidencia de que se generan registros (capturas, consultas, volumen, trazas).
- Evidencia de revisión (actas mensuales, tickets, hallazgos y acciones).
- Prueba de integridad (controles de acceso, configuración BD, hash/HMAC si aplica).
- Retención y respaldos (política, pruebas de restauración, bitácoras).

---

## Mapa ISO → VIT (controles y evidencias)
| Control ISO/IEC 27001:2022 | Qué pide (paráfrasis) | Evidencia en VIT | Artefacto |
|---|---|---|---|
| A.8.15 Registro (logs) | Registrar eventos relevantes y protegerlos para análisis | AuditLog + reglas de inmutabilidad | Tabla AuditLog, permisos BD |
| A.8.16 Monitoreo | Monitorear para detectar anomalías y evaluar incidentes | Reglas + revisiones periódicas | Reporte diario/semanal/mensual |
| A.8.17 Sincronización de reloj | Mantener timestamps confiables | UTC + NTP | Configuración servidor + verificación |
| A.8.24 Criptografía | Proteger información con criptografía según riesgo | TLS + cifrado en reposo + (opcional) hash | Config TLS, KMS/keys, evidencia técnica |
