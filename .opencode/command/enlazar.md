---
description: Sugiere enlaces bidireccionales [[ ]] entre notas del segundo cerebro
agent: build
---

Usa el skill `pkm-enlazar` para sugerir enlaces bidireccionales entre notas del vault `antigravity-proyectos`:

1. Determina el alcance (nota objetivo si se indica, o barrido del vault: Proyectos/, Clases/, Inbox/).
2. Extrae los conceptos clave de las notas (autores, proyectos, métodos, materias).
3. Busca notas relacionadas con `obsidian_search-vault` y `grep`.
4. Evalúa relaciones reales (concepto compartido, complemento o contraste) — no fuerces conexiones.
5. Presenta las sugerencias como `[[Nota A]] ←→ [[Nota B]]` con motivo en 1 línea.
6. Pregunta antes de editar si hay 5+ enlaces o la relación no es evidente; al editar, añade los enlaces en la sección "Conecta con" o "Links a recursos" de la nota, sin tocar el frontmatter.

Argumentos del usuario (si hay): $ARGUMENTS
