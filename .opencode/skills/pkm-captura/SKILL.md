---
name: pkm-captura
description: Captura rápida de ideas, tareas y referencias al segundo cerebro de Obsidian (vault "antigravity-proyectos"). Usa cuando el usuario diga "captura esto", "guarda/anota esta idea", "apunta esto", "no pierdas esto", "a inbox", o comparta un link/papel/referencia que quiere registrar. También procesa la bandeja de entrada (Inbox) hacia Proyectos/Clases usando plantillas.
---

# Captura PKM — Segundo Cerebro Obsidian

Flujo del método Zettelkasten/GTD aplicado al vault **antigravity-proyectos**
(= el repo `/home/andres/Documentos/ANTIGRAVITY-PROYECTOS`). Todo se maneja con
las herramientas `obsidian_*` sobre el vault `antigravity-proyectos`.

## Estructura del vault

```
Inbox/               # Captura rápida sin procesar (vaciar en cada sesión)
Plantillas/          # Plantillas para procesar: Dia, Paper, Proyecto-Hito, Clase
Proyectos/
  CENALTEC/          # Proyectos institucionales
  Revision-RPAS/     # Paper Swarm Intelligence
  Tesis/             # Tesis doctoral
Clases/
  Navegacion-Aerea/
  Sistemas-de-Aeronaves/
Dashboard - *.md     # Dashboards Dataview (no tocar)
```

## 1. Captura rápida (al vuelo)

Cuando el usuario pida capturar algo rápido (idea, tarea, link, dato), NUNCA
lo guardes en un proyecto todavía. Crea una nota en `Inbox/`:

- **Nombre**: `{{date}} - título-corto.md` (formato fecha `DD-MM-YYYY`), sin
  espacios, en minúsculas y con guiones.
- **Contenido**: frontmatter mínimo + el dato tal cual, sin reformatear mucho
  (el procesado viene después). Preserva links/URLs originales.
- **Frontmatter**:
  ```yaml
  ---
  tags: [inbox]
  fecha: DD-MM-YYYY
  fuente: <si aplica: conversación, web, clase, papel, reunión>
  ---
  ```
- Si el usuario dice que es una tarea, anótala como checkbox `- [ ]` para que
  el Dashboard de Tareas la recoja vía Dataview.

Ejemplo de nota de captura:
```markdown
---
tags: [inbox]
fecha: 07-08-2026
fuente: conversación
---

# Idea sobre enjambres multi-RPAS

- [ ] Implementar detección de colisiones con el artículo de Vásquez et al.
- Link: https://ejemplo.com/paper
- Conecta con: Tesis, paper de Revision-RPAS
```

## 2. Procesar la bandeja (Inbox → destino)

Cuando el usuario diga "procesa el inbox", "vacía inbox", "organiza lo
capturado":

1. Lee cada nota de `Inbox/` con `obsidian_read-note`.
2. Clasifica según su contenido y las etiquetas `conecta con`:
   - Paper → plantilla `Plantillas/Paper - Investigacion.md` en `Proyectos/Revision-RPAS/`
   - Hito de proyecto → `Plantillas/Proyecto - Hito.md` en la carpeta `Proyectos/<X>/`
   - Clase → `Plantillas/Clase - Planificacion.md` en `Clases/<materia>/`
   - Diario/bitácora → plantilla `Plantillas/Dia.md`
3. Si NO encaja claramente, pregunta al usuario antes de moverla. Nunca adivines.
4. Tras mover, borra la nota de `Inbox/` con `obsidian_delete-note` (a .trash).

## 3. Convenciones

- Siempre usa el vault `antigravity-proyectos` en las herramientas obsidian.
- Respetar las plantillas existentes: llenar los campos del frontmatter, no
  inventar campos nuevos que rompan los Dashboards Dataview.
- Preservar los tags existentes del sistema (`inbox`, `paper`, `clase`,
  `proyecto`, `hito`) — son los que filtran los dashboards.
- `obsidian_create-note`: pasar `filename` sin carpeta y `folder` por
  separado (ej. folder `Inbox`).
- Confirmar al usuario con la ruta final de la nota creada o movida.
