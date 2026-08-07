---
description: Procesa la bandeja del segundo cerebro (Inbox → Proyectos/Clases)
agent: build
---

Usa el skill `pkm-captura` y procesa la bandeja de entrada (Inbox → destino) del vault `antigravity-proyectos`:

1. Lee cada nota de `Inbox/` con `obsidian_read-note`.
2. Clasifica según su contenido y las etiquetas "Conecta con":
   - Paper → plantilla `Plantillas/Paper - Investigacion.md` en `Proyectos/Revision-RPAS/`
   - Hito de proyecto → `Plantillas/Proyecto - Hito.md` en la carpeta `Proyectos/<X>/`
   - Clase → `Plantillas/Clase - Planificacion.md` en `Clases/<materia>/`
   - Diario/bitácora → plantilla `Plantillas/Dia.md`
3. Si NO encaja claramente, pregunta al usuario antes de moverla. Nunca adivines.
4. Tras mover, borra la nota de `Inbox/` con `obsidian_delete-note` (a .trash).
5. Respetar las plantillas existentes: llenar los campos del frontmatter, no inventar campos nuevos que rompan los Dashboards Dataview. Preservar los tags del sistema (`inbox`, `paper`, `clase`, `proyecto`, `hito`).

Argumentos extra del usuario (si hay): $ARGUMENTS
