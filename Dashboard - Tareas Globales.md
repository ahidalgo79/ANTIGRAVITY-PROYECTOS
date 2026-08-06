# ✅ Tareas pendientes por proyecto

```dataview
TASK
FROM "Proyectos" OR "Clases"
WHERE !completed
GROUP BY file.folder
SORT file.mtime DESC
```
