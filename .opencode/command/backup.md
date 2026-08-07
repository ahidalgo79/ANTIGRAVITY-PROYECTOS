---
description: Backup del vault ANTIGRAVITY-PROYECTOS vía git
agent: build
---

Haz un backup del vault ANTIGRAVITY-PROYECTOS con git:

1. Revisa `git status --short` para ver los cambios pendientes.
2. Añade solo lo que corresponde con `git add -A` (nunca incluyas `.env`, binarios grandes ni `node_modules`; respeta `.gitignore`).
3. Verifica con `git diff --cached --stat` que solo se stagea lo esperado.
4. Haz commit con mensaje en el estilo existente del repo: `vault backup: <YYYY-MM-DD HH:MM:SS>`.
5. No hagas push a menos que el usuario lo pida.

Notas del usuario (si hay): $ARGUMENTS
