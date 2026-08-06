# 🗓️ Actividades CENALTEC próximas

```dataview
TABLE WITHOUT ID
  file.link as Actividad,
  fecha as Fecha,
  prioridad as Prioridad
FROM "Proyectos/CENALTEC"
WHERE fecha >= date(today)
SORT fecha ASC
```
