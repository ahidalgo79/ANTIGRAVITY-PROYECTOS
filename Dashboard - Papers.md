# 📄 Papers leídos esta semana

```dataview
TABLE WITHOUT ID
  file.link as Título,
  author as Autor,
  journal as Revista,
  status as Estado
FROM #paper AND -"Plantillas"
WHERE status != "📖 Por leer"
SORT file.ctime DESC
LIMIT 10
```
