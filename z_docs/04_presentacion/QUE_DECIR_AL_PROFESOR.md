# 🎤 GUÍA: QUÉ DECIR AL PROFESOR
## Intro + Presentación Verbal

---

## APERTURA (1 minuto)

**Tono:** Profesional, honesto, con confianza en lo hecho

```
"Buenos días Profesor. 

Hoy le presento el progreso de VIT en las últimas 8 semanas.

El proyecto está en buen camino: completé la capa de seguridad (Sprint 1),
ahora voy en la capa de ISO 27001 (Sprint 2), y tendré todo listo para fin de mayo.

Le muestro qué funciona hoy, qué está en desarrollo, y qué falta completar."
```

---

## CONTEXTO (1 minuto)

**Referencia a la retroalimentación anterior:**

```
"En la última entrega, usted indicó que me faltaba:
- ✅ Modelos de riesgos (Risk)
- ✅ Controles ISO (ISOControl)
- ✅ Statement of Applicability (SoAItem)
- ✅ Gestión de evidencias
- ✅ Seguridad detallada (roles, auditoría)

Estos 6 meses trabajé en dos focos:

1. PRIMERO: Construir una seguridad SÓLIDA (JWT, RBAC, Auditoría)
   Porque sin esto, todo lo demás es débil.
   
2. SEGUNDO: Documentar la arquitectura ISO correctamente
   Porque el código de Riesgos necesita estar bien diseñado.

El resultado: Backend seguro, documentación profesional, y ahora entro en el corazón ISO."
```

---

## DEMO (15 minutos)

**Estructura:**

```
"Voy a mostrar 4 cosas que ya funcionan:"

1. SEGURIDAD (3 min)
   - Login y JWT token
   - Token usado en endpoint protegido
   
2. CONTROL DE ACCESO (3 min)
   - 3 usuarios diferentes (Admin, Consultant, Client)
   - Cada uno ve solo lo que debe ver
   
3. AUDITORÍA (3 min)
   - Hago una acción (crear proyecto)
   - AuditLog registra automáticamente quién/qué/cuándo
   
4. BASE DE DATOS (3-5 min)
   - Mostrar relaciones en BD
   - Explicar normalización

Total: 15 minutos de demo funcional"
```

---

## EXPLICACIÓN SOBRE RISK/SOA (2 minutos)

**Cuando pregunte: "¿Por qué Risk/SoA no están?"**

**Respuesta modelo:**

```
"Risk y SoA no están codificados todavía (eso es Sprint 2).

PERO están 100% diseñados. 

Mostré en z_docs/ cómo se ve cada modelo:
- Risk tiene: probability (1-5), impact (1-5), score inherent,
  luego probability_residual, impact_residual, score_residual
  
- ISOControl tiene: código (A.5.1, etc), nombre, descripción, categoría
  
- SoAItem tiene: proyecto, control, es_aplicable, razionale, estado

Esto es CRUD puro. No es complejo. 

Estimé 4 días de código (3 modelos + endpoints + tests).

Empecé esta semana. 14 de Marzo tendré Risk funcional, 
17 de Marzo SoA, y 24 de Marzo Sprint 2 100% completado."
```

---

## EXPLICACIÓN SOBRE TIMING (2 minutos)

**Cuando pregunte: "¿Cómo justificas el progreso?"**

**Respuesta modelo:**

```
"Venimos en 8 de 12 semanas (67% del tiempo).
Tenemos 4.6 de 10 de funcionalidad (46%).

Parece lento, pero es coherente:

Sprint 1 fue CIMENTACIÓN: JWT, RBAC, Auditoría, BD normalizada.
Esto consume tiempo porque es arquitectura, no es CRUD.

Sprint 2 en adelante sube más rápido porque es funcionalidad ISO:
Risk, SoA, Evidence, Assets, Reports.

Proyección:
- Hoy (10 Mar):     4.6/10
- Fin Sprint 2 (24 Mar): 7.0/10
- Fin Sprint 4 (21 Abr): 8.5/10 ← corazón ISO completo
- Fin Sprint 6 (19 May): 9.5/10 ← listo para producción"
```

---

## HONESTIDAD (1 minuto)

**Puntos que debes reconocer:**

```
"Seré honesto:

✅ LO QUE ESTÁ BIEN:
- Seguridad: nivel empresarial (JWT, RBAC, Auditoría)
- Documentación: 200+ páginas, profesional
- Código: limpio, testeado (~40% cobertura)
- Plan: realista y ejecutable

❌ LO QUE FALTA:
- Risk/SoA: diseño 100%, código 0% (2-3 semanas)
- Frontend: infraestructura lista, UI sin lógica
- Testing formal: tengo 8 casos, falta pytest completo
- Reportes: completamente por hacer (Sprint 4)

Pero esto está EN PLAN. No es sorpresa. No descarrilé."
```

---

## CIERRE (1 minuto)

**Propuesta clara:**

```
"Mi proposta es:

1. Aceptar que Risk/SoA son Sprint 2 (próximas 2 semanas)
2. Aceptar que Frontend es Sprint 3-4 (Abril)
3. Confiar en mi plan: 6 sprints, timeline clara, código funcional

Resultado esperado fin de mayo: 7.5-8.0 de 10.

¿Le parece bien el plan? ¿Necesita que ajuste algo?"
```

---

## PREGUNTAS COMUNES Y RESPUESTAS

### P: "¿Está en producción?"

**R:** "No aún. Backend está listo para producir (Render.com), 
pero Frontend todavía no tiene UI. Sprint 6 (19 May) es deployment completo."

---

### P: "¿Cuántas líneas de código?"

**R:** "Tengo ~2,000 líneas back, ~100 líneas front.
Pero '2,000 líneas' engaña. Lo importante es que los 28 endpoints funcionan
y tienen auditoría automática."

---

### P: "¿Quién más trabaja en esto?"

**R:** "Ahorita solo yo. Pero la documentación está hecha para que otro dev
entre en cualquier momento. Código está limpio y comentado."

---

### P: "¿Cuáles son los riesgos?"

**R:** "Principales:
1. Risk dataset: si tenemos 100 riesgos × 5 proyectos = parsing lento
   → Solución: índices en BD, optimización SQL
   
2. Frontend: si no empiezo pronto, se atrasa
   → Solución: Sprint 2 reservé 1 día para login, es disciplina
   
3. Testing: si no hago pytest, cobertura queda en 40%
   → Solución: Sprint 5 dedicado a testing formal
   
Todos son manejables."

---

### P: "¿Comparte el código en GitHub?"

**R:** "Sí, 100% público: https://github.com/JuanJimenezGuardo/Proyecto_VIT

Todos los commits están documentados en español.
Puede clonar, probar, ver el historial completo."

---

## DOCUMENTOS QUE PUEDE VER

**Dile al profesor: "Preparé estos documentos para que profundice si quiere"**

```
En `z_docs/04_presentacion/` encontrará:

1. INFORME_PROGRESO_ACTUAL_PROFESOR.md
   → Completo (12 secciones, todas las métricas)
   
2. RESUMEN_EJECUTIVO_1PAG.md
   → 1 página, para imprimir y llevar
   
3. GUIA_DEMO_PROFESOR.md
   → Paso a paso para repetir demo
   
4. COMPARACION_ANTES_DESPUES.md
   → Tablas visuales de progreso
   
5. z_docs/
   → Toda la arquitectura detallada
```

---

## TONO Y LENGUAJE

**Usar:**
- Específico ("JWT tokens de 1 hora" vs "seguridad")
- Honesto ("Risk: diseño 100%, código 0%" vs "Risk está hecho")
- Accionable ("Sprint 2: Risk en 2 días" vs "próximo Risk")
- Profesional ("endpoints CRUD" vs "cosas del API")

**Evitar:**
- Excusas ("No tuve tiempo" → "Prioricé seguridad")
- Vagas ("Casi está" → "Falta 2 días de código")
- Defensivas ("Creo que está bien" → "Esto funciona, lo probé")

---

## SEQUENCIA RECOMENDADA

1. **Apertura (1 min):** Quién soy, qué hice, qué le muestro
2. **Contexto (1 min):** Referencia a tu retroalimentación anterior
3. **Demo (15 min):** Postman + BD + 4 demos
4. **Deuda técnica (2 min):** Honestidad sobre lo que falta
5. **Timeline (2 min):** Proyección realista
6. **Preguntas (5 min):** Esperar y responder
7. **Cierre (1 min):** "¿Vamos bien? ¿Ajusto algo?"

**Total: 27 minutos**

---

## FALLBACK (Si algo no funciona en demo)

```
Si Postman falla:
"Déjeme mostrarle el código en IDE. Acá está el endpoint [abre archivo].
Esto funciona, lo probé hace 10 minutos. Es problema de Postman ahora."

Si BD no abre:
"El logeo está en .env. Pero la estructura está acá [muestra archivo].
23 columnas validadas, 8 modelos relacionales, todo normalizado."

Si GitHub no carga:
"Te paso el código en pendrive. Está completo."
```

---

## DESPUÉS DE LA PRESENTACIÓN

**Ofrécele:**
```
"¿Le gustaría que:
1. Le envíe documentación adicional?
2. Grabe un video de la demo?
3. Haga checkpoint en Sprint 2 (24 Marzo)?
4. Le comparta el acceso a GitHub para revisar commits?"
```

---

## ÚLTIMA RECOMENDACIÓN

**Di esto con seguridad y sin dudas:**

> "El trabajo que hice es real. 
> Los endpoints funcionan. 
> La auditoría registra. 
> Los datos están seguros.
> 
> Risk/SoA son próximas 2 semanas.
> No descarrilé. 
> Tengo plan.
> 
> Vamos a terminar esto bien."

---

