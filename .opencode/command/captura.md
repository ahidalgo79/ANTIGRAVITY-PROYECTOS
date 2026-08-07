---
description: Captura rápida de una idea/tarea/referencia al Inbox del segundo cerebro
agent: build
---

Usa el skill `pkm-captura` para guardar en el Inbox del vault `antigravity-proyectos` la siguiente captura rápida:

$ARGUMENTS

Sigue el flujo de "Captura rápida" del skill:
- Crea la nota en `Inbox/` con nombre `{{date}} - título-corto.md` (formato `DD-MM-YYYY`, minúsculas y con guiones).
- Frontmatter mínimo: `tags: [inbox]`, `fecha: DD-MM-YYYY`, `fuente: <si aplica>`.
- Si es una tarea, anótala como `- [ ]` para que el Dashboard de Tareas la recoja vía Dataview.
- Preserva links/URLs originales y las notas de "Conecta con".
- NO la muevas a un proyecto todavía.
- Confirma al usuario con la ruta final de la nota creada.
