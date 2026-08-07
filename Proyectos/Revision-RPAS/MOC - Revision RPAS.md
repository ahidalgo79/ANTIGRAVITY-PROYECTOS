---
tags: [proyecto, revision-rpas, moc]
project: Revision-RPAS
estado: 🔵 En curso
fecha-inicio: 2026-01-01
fecha-fin:
prioridad: Alta
---

# MOC — Revisión Paper Swarm Intelligence Multi-RPAS

## 🎯 Propósito

Revisión académica del manuscrito **"Swarm Intelligence Algorithms for Multi-RPAS"** (formato Elsevier).

## 🔗 Contenido real del repo

- 📄 Manuscrito: `Revision/Swarm Intelligence Algorithms for Multi-RPAS/main_expanded.tex`
- 📄 Manuscrito raíz: `Revision/main_expanded.tex`
- 🧪 Scripts de auditoría/edición: `Revision/Swarm Intelligence Algorithms for Multi-RPAS/` (47 scripts Python)
- 📋 Screening de coautor: `Lista_51_Screening_Coautor.csv`
- 📁 Flujo completo: `PAPER_REVISION_SWARM_RPAS/`
- 🔬 RAG jerárquico: `rag_jerarquico.py`, `indices_rag_jerarquico/`

## 📋 Tareas pendientes

- [ ] Revisar consistencia BibTeX (`uv run python src/latex_checker.py`)
- [ ] Validar PRISMA/Elsevier (`uv run python src/prisma_checker.py`)
- [ ] Auditar citas finales (`auditoria_citas_final.json`)

## 📈 Progreso / Logros

- Pipeline multi-agente CrewAI + Ollama operativo
- Auditoría de citas completada (JSON de resultados)
- DPO learning y barrido de modelos Claude v2
