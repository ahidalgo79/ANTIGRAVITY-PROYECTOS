# Diagnóstico del Entorno — ANTIGRAVITY-PROYECTOS

**Fecha:** 2026-05-13  
**Sistema:** Linux x86_64

---

## Versiones de Herramientas

| Herramienta | Versión |
|-------------|---------|
| Python      | 3.13.7  |
| uv          | 0.11.8  |
| Ollama      | 0.20.3  |
| opencode    | 1.14.48 |
| Node.js     | 24.15.0 |
| npm         | 11.14.1 |
| pnpm        | 11.1.1  |

---

## OpenCode

| Ítem         | Estado |
|--------------|--------|
| Config       | ⚠️ Vacío (`~/.config/opencode/` solo tiene `node_modules`) |
| `auth.json`  | ⚠️ No existe en `~/.local/share/opencode/` (pero hay modelos gratuitos disponibles) |
| `AGENTS.md`  | ✅ Creado e inicializado |

**Conclusión:** El proyecto ha sido inicializado con `AGENTS.md`. Aunque no hay un archivo `auth.json` explícito, OpenCode tiene acceso a modelos gratuitos (DeepSeek, MiniMax, etc.). Para usar providers premium o "OpenCode Zen", el usuario deberá ejecutar `/connect` manualmente.

---

## Ollama — Modelos Locales

| Modelo        | Tamaño  | Estado |
|---------------|---------|--------|
| qwen2.5:1.5b  | 986 MB  | ✅ Descargado |

**Advertencia:** El modelo `qwen2.5:1.5b` es muy pequeño (1.5B parámetros) para tareas complejas de codificación/análisis. Se recomienda al menos `qwen2.5-coder:7b` o `llama3.2:3b`.

---

## Proyecto: ANTIGRAVITY-PROYECTOS

### Estructura de Directorios

```
├── .env                  # Config: OLLAMA_NUM_THREAD=4, LLM_TIMEOUT=60
├── .git/
├── .venv/                # Entorno virtual Python
├── CENALTEC-PROYECTOS/   # Proyectos CENALTEC
├── Revision/             # Paper: Swarm Intelligence Algorithms for Multi-RPAS
│   └── PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/
├── SISTEMAS-DE-AERONAVES/
├── TAIWAN-2026/
├── Tesis/
├── VIBRACIONES-MECANICAS/
├── agencia-creativa-ia/
├── data/                 # Datos crudos y procesados
├── figures/              # Figuras generadas
├── reports/              # Reportes generados
├── src/                  # Código fuente
│   ├── agents/           # Agentes (CrewAI)
│   ├── mcp/              # Model Context Protocol
│   ├── tools/            # Herramientas personalizadas
│   ├── cli.py            # CLI principal
│   ├── pipeline_tecnico.py
│   ├── prisma_checker.py # Validación PRISMA para LaTeX
│   ├── latex_checker.py  # Consistencia citas/bibliografía
│   ├── auditor_*.py      # Auditores (directo, híbrido, mínimo, real, seguro, simple)
│   ├── crew_creativo.py / crew_minimo.py
│   └── fix_bib.py        # Reparación de .bib
├── pyproject.toml        # Dependencias Python (~45)
├── Makefile              # Comandos unificados
├── a320_report.md        # Reporte técnico A320
├── b737_report.md        # Reporte técnico B737
├── diagnostico.py        # Script de diagnóstico
└── uv.lock
```

### Dependencias Principales (`pyproject.toml`)

- **Ciencia de datos:** numpy, pandas, polars, scipy, scikit-learn, statsmodels, duckdb, dask
- **Visualización:** matplotlib, seaborn, plotly, manim, great-tables
- **IA/Agentes:** crewai, crewai-tools, langchain-ollama, langgraph, litellm, anthropic, google-genai
- **MCP:** mcp >= 1.27.0
- **Ofimática:** openpyxl, xlsxwriter, python-docx, reportlab, pdfplumber, docxtpl, jinja2
- **ML Ops:** optuna, wandb, prefect, dvc
- **Calidad:** ruff, pytest, hypothesis, pydantic
- **Notebooks:** jupyterlab, ipython, ipykernel, ipywidgets, marimo

### Git

- **Rama actual:** `main` (única rama local y remota)
- No hay `AGENTS.md` en el repositorio

---

## Recomendaciones

1. **Conectar un provider en opencode:**
   ```bash
   # En la TUI de opencode
   /connect   # Elegir OpenCode Zen, OpenAI, Anthropic, etc.
   ```

2. **Inicializar el proyecto en opencode:**
   ```bash
   /init   # Crea AGENTS.md con el contexto del proyecto
   ```

3. **Descargar un modelo local más potente (opcional):**
   ```bash
   ollama pull qwen2.5-coder:7b
   # o
   ollama pull llama3.2:3b
   ```

4. **Configurar opencode para usar Ollama local:**
   ```json
   {
     "provider": {
       "ollama": {
         "models": {
           "qwen2.5:1.5b": {}
         }
       }
     }
   }
   ```
