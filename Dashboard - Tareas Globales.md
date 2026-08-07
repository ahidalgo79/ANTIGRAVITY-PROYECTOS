# ✅ Tareas pendientes por proyecto

```dataview
TASK
FROM "Inbox" OR "Proyectos" OR "Clases"
WHERE !completed
GROUP BY file.folder
SORT file.mtime DESC
```
