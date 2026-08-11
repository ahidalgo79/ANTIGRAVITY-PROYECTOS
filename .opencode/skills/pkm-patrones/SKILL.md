---
name: pkm-patrones
description: Analiza diarios, bitácoras y notas del vault "antigravity-proyectos" para detectar patrones: temas recurrentes, tendencias en decisiones, bloqueos que se repiten, ideas que reaparecen y conexiones temporales. Usa cuando el usuario diga "analiza patrones", "qué tendencias hay", "revisa mis notas", "socio de pensamiento", "qué vengo trabajando" o pida un resumen inteligente de su actividad.
---

# Análisis de patrones — PKM

Actúa como "socio de pensamiento" sobre el vault **antigravity-proyectos**
(= repo `/home/andres/Documentos/ANTIGRAVITY-PROYECTOS`): revela tendencias,
conexiones y temas que el usuario no ve a simple vista.

## Flujo

### 1. Determinar el alcance
- Diarios/bitácoras: `Inbox/*.md`, notas `Dia` (`Plantillas/Dia.md`) y cualquier
  `*-DD-MM-YYYY*.md`.
- Proyecto concreto: `Proyectos/<X>/**` (MOCs + hitos + notas).
- Todo el vault: `Proyectos/`, `Clases/`, `Inbox/`.
Si el usuario no especifica, pregunta o elige el alcance más razonable y decláralo.

### 2. Recopilar y ordenar cronológicamente
Extrae de cada nota: fecha, tags YAML, estado (`estado:`, `status:`), tareas
(`- [ ]` / `- [x]`) y conceptos principales. Ordena por fecha para ver la
evolución temporal.

### 3. Detectar patrones (categorías)
- **Temas recurrentes**: conceptos que aparecen en varias notas/proyectos
  (ej. "enjambre", "Reto Marte", "PRISMA").
- **Decisiones y su evolución**: cómo cambió un enfoque a lo largo del tiempo
  (comparar `estado`/`status` entre hitos).
- **Bloqueos recurrentes**: problemas técnicos que se repiten (ej. "Ollama en
  CPU sin AVX2", "compilación LaTeX").
- **Ideas sin desarrollar**: capturas que quedaron en Inbox o se anotaron pero
  no se convirtieron en hitos/tareas.
- **Conexiones temporales**: actividad concentrada en ciertas fechas, ciclos de
  trabajo, temas que preceden a otros.

### 4. Producir el informe
Entrega un resumen en Markdown (en la respuesta, no en archivo salvo que se
pida) con:
- 3–6 patrones o tendencias, cada uno con evidencia (`ruta/nota.md`) y una
  línea de interpretación.
- 2–3 conexiones inesperadas entre notas de proyectos distintos.
- Recomendaciones accionables (mover Inbox, crear MOC, desbloquear hito,
  programar sesión).
- Sugerencia de enlaces `[[ ]]` resultantes (remite al skill `pkm-enlazar`).

## Reglas

- Cita siempre la ruta de la nota como evidencia; nunca inventes datos.
- Si no hay datos suficientes, dilo en vez de forzar patrones.
- No modifiques notas durante el análisis; solo informar y sugerir.
