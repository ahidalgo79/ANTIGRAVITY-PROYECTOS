---
name: pkm-enlazar
description: Sugiere enlaces bidireccionales [[ ]] entre notas del vault "antigravity-proyectos" que comparten conceptos, autores o proyectos. Usa cuando el usuario diga "sugiere enlaces", "conecta notas", "enlaza ideas", "encuentra conexiones", "mapea relaciones" o pida romper silos de información. Detecta notas que razonan sobre los mismos conceptos pero no se referencian entre sí.
---

# Enlaces bidireccionales — PKM

Detecta y sugiere conexiones `[[ ]]` entre notas del vault **antigravity-proyectos**
(= repo `/home/andres/Documentos/ANTIGRAVITY-PROYECTOS`). Objetivo: que las
notas atómicas dejen de ser silos y formen una red de conocimiento navegable.

## Flujo

### 1. Determinar el alcance
- Si el usuario da una nota objetivo, parte de ella.
- Si no, barre el vault: `Proyectos/*`, `Clases/*`, `Inbox/` (usa
  `obsidian_search-vault` y `grep` con las herramientas locales).

### 2. Extraer conceptos clave de la(s) nota(s)
Busca términos candidatos: autores citados, nombres de proyectos (CENALTEC,
Revision-RPAS, Tesis, Reto Marte, NVIDIA), métodos (PSO, ACO, enjambres,
PRISMA), materias (navegación aérea, A320, B737) y temas técnicos. No te
limites a palabras repetidas: busca conceptos implícitos.

### 3. Buscar notas relacionadas
Para cada concepto, busca en todo el vault:
- `obsidian_search-vault` con el término (content/both).
- `grep` sobre `*.md` para términos que el MCP no indexe bien.

### 4. Evaluar la relación (no fuerces conexiones)
Una relación válida exige que las notas compartan **concepto real** (no solo
una palabra común genérica como "drones" sin contexto). Prioriza:
- Mismo autor/paper citado en ambas.
- Mismo hito/proyecto con contenido complementario.
- Idea que una nota plantea y otra desarrolla.
- Contraste: nota que matiza o contradice otra.

### 5. Proponer, no editar a ciegas
Presenta las sugerencias con formato:
```
[[Nota A]] ←→ [[Nota B]]
Motivo: <1 línea, concepto compartido>
```
Agrupa por afinidad y confianza. **Pregunta antes de editar** si hay 5+ links
o si la relación no es evidente. Al editar:
- Añade el enlace en la sección "Conecta con:" si la nota la tiene (plantilla
  Paper), o en "🔗 Links a recursos/notas relacionadas" (plantilla Proyecto-Hito),
  o al final como línea `- Conecta con: [[...]]`.
- Nunca toques el frontmatter salvo que el usuario lo pida.

## Reglas

- Usa siempre el vault `antigravity-proyectos`.
- Los `[[ ]]` deben apuntar al nombre de archivo sin `.md` ni ruta.
- No inventes enlaces entre proyectos sin relación temática real.
- Confirma con el usuario la lista final antes de aplicar cambios masivos.
