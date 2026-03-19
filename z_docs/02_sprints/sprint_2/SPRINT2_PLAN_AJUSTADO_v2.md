# Sprint 2: Plan Ajustado v2 (con Requerimientos Ingeniero Mauricio)

**Fecha**: 11-24 Mar 2026  
**Estado**: CIERRE TECNICO EN CURSO  
**Ajuste**: Incorpora requerimientos de documentación y despliegue del Ingeniero Mauricio
**Responsable Backend Core (Juan Jose Jimenez Guardo)**: Juan Jose Jimenez Guardo

---

## 📋 Resumen Ejecutivo

El plan original de Sprint 2 es sólido técnicamente. Pero el Ingeniero Mauricio pidió explícitamente:
1. **Explicación del flujo del sistema** (modelo + procesos)
2. **Montaje de PostgreSQL en servidor**

Este ajuste integra esas tareas sin romper el plan técnico existente. Resultado: Backend listo + Documentación + Script deploy.

---

## 🎯 Distribución por Día (Día 1-10)

### **Día 1: Cierre Modelo Contact y Preparación Base**

| Rol | Tarea |
|-----|-------|
| **Juan Jose Jimenez Guardo (Backend core)** | Cerrar modelo Contact final, arreglar relaciones, validaciones básicas |
| **Osky (Backend persistencia)** | Preparar estructura de migraciones, crear campos planned/actual en estructuras |
| **Luis (Frontend)** | Congelar nuevas vistas, revisar impacto UI de cambios BD |

**Objetivo**: Contact cierre técnico + migraciones estructuradas

---

### **Día 2: ProjectContact y Work Notes**

| Rol | Tarea |
|-----|-------|
| **Juan Jose Jimenez Guardo** | Terminar ProjectContact, relaciones con Contact |
| **Osky** | Implementar work_notes, ajustar relaciones existentes |
| **Luis** | Mapear payload esperado de API |

**Objetivo**: ProjectContact completo + work_notes listos

---

### **Día 3: Validaciones y Document**

| Rol | Tarea |
|-----|-------|
| **Juan Jose Jimenez Guardo** | Implementar validaciones de ProjectContact, constraints críticos |
| **Osky** | Implementar modelo Document, campos estructura |
| **Luis** | Documentar ajustes de contrato encontrados |

**Objetivo**: Validaciones core + Document modelo

---

### **Día 4: Serializers/Viewsets y Migraciones Estructurales**

| Rol | Tarea |
|-----|-------|
| **Juan Jose Jimenez Guardo** | Abrir serializers/viewsets mínimos de Contact y ProjectContact |
| **Osky** | Crear migraciones estructurales para Contact, ProjectContact, Document |
| **Luis** | Pruebas de compatibilidad UI/API |

**Objetivo**: DRF endpoints mínimos + migraciones en orden

---

### **Día 5: Constraints Críticos y Data Migration Legacy**

| Rol | Tarea |
|-----|-------|
| **Juan Jose Jimenez Guardo** | Probar constraints críticos, flujo backend core |
| **Osky** | Ejecutar data migration legacy Company → Contact |
| **Luis** | Soporte a validación de contrato |

**Objetivo**: Backend core functiona + datos migrados

---

### **✅ Checkpoint Técnico (Fin Día 5)**
Backend core listo. Ahora: documentación y despliegue.

---

### **Día 6: 📖 DOCUMENTO DE FLUJO DEL SISTEMA** ⭐

| Rol | Tarea |
|-----|-------|
| **Juan Jose Jimenez Guardo (Lead)** | Escribir documento "Flujo del Sistema SGSI ISO 27001": <br> • Diagrama entidades (ERD) <br> • Flujo: Empresa → Proyecto → Fase → Tarea <br> • Flujo: Proyecto → Activo → Documento <br> • Sistema de auditoría (usuario → acción → RegistroAuditoria) |
| **Osky** | Documentar modelo de datos persistencia (campos, relaciones, migraciones) |
| **Luis** | Documentar flujo de UI (cómo se ve en frontend, casos de uso) |

**Entregables**: 
- `SISTEMA_FLUJO_COMPLETO.md` (concepto + diagrama)
- `MODELO_DATOS_REFERENCIA.md` (para BD)
- `FLUJO_UI_CASOS_USO.md` (para frontend)

**¿Por qué?** Ingeniero Mauricio lo pidió explícitamente. Es diferenciador.

---

### **Día 7: 🗄️ PREPARACIÓN POSTGRESQL Y SCRIPT DEPLOY** ⭐

| Rol | Tarea |
|-----|-------|
| **Osky (Lead)** | Crear script SQL para PostgreSQL: <br> • Schema completo de Sprint 2 <br> • Datos iniciales (empresas de prueba) <br> • Instrucciones de montaje paso a paso |
| **Juan Jose Jimenez Guardo** | Preparar requirements.txt final, .env template, verificar todas las migraciones |
| **Luis** | Preparar instrucciones de setup frontend (npm install, env, proxy) |

**Entregables**:
- `POSTGRESQL_SETUP_SCRIPT.sql` (listo para ejecutar)
- `POSTGRESQL_DEPLOYMENT_GUIDE.md` (paso a paso)
- `SETUP_COMPLETO.md` (backend + frontend)
- `.env.example` actualizado

**¿Por qué?** Ingeniero dijo: "montar el motor en servidor". Esto lo permite.

---

### **Día 8: Endpoints Mínimos y Datos de Prueba**

| Rol | Tarea |
|-----|-------|
| **Juan Jose Jimenez Guardo** | Endpoints mínimos para Contact, ProjectContact listos para validación |
| **Osky** | Cargar datos de prueba, verificación post-migración |
| **Luis** | Preparación integración de consumo API |

**Objetivo**: API funciona con datos reales

---

### **Día 9: Cierre Técnico y Checklist**

| Rol | Tarea |
|-----|-------|
| **Juan Jose Jimenez Guardo** | Checklist cierre: constraints, validaciones, flujo core OK |
| **Osky** | Verificación final migraciones, integridad BD |
| **Luis** | Integrar API mínima, validación funcional |

**Objetivo**: Todo funciona, listo para demostración

---

### **Día 10: Reunión con Ingeniero Mauricio** ✅

**Demostrables:**
- ✅ Backend functiona (Contact, ProjectContact, Document)
- ✅ BD lista en PostgreSQL (script en mano)
- ✅ Documento explicando flujo completo del sistema
- ✅ Guía de despliegue paso a paso
- ✅ Frontend conectado a API
- ✅ ERD presentable

**Outcome esperado**: 
- Ingeniero puede ver arquitectura clara
- Puede montar BD en su servidor con script
- Entiende flujo del sistema
- Confía en avance técnico

---

## 📊 Comparación: Plan Original vs Ajustado

| Área | Original | Ajustado | Impacto |
|------|----------|----------|---------|
| Backend core (Día 1-5) | ✅ | ✅ | Mantiene |
| Documentación sistema | ❌ | ✅ (Día 6) | NUEVA |
| Script PostgreSQL | ❌ | ✅ (Día 7) | NUEVA |
| Endpoints + pruebas | ✅ | ✅ (Día 8-9) | Mantiene |
| Reunión list ready | ⚠️ | ✅ | MEJORADO |

---

## 🎬 Acción Inmediata

**Hoy (Día 1 - March 16):**
1. Explorar estado actual: Contact, ProjectContact en models.py
2. Validar migraciones existentes
3. Comenzar implementación Día 1

**Próximas 10 días**: Seguir calendario Día 1-10

**Resultado esperado (March 26)**: Reunión con Ingeniero impresionado ✅

---

## 💡 Lección Aprendida

> "Pasar de proyecto universitario a cliente real = documentación + despliegue son tan importantes como código"

Este plan lo refleja.

