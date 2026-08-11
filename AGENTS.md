# ANTIGRAVITY-PROYECTOS — Project Guide

## Overview
Monorepo de investigación académica y ofimática enfocado en: (1) enjambres multi-RPAS (Vehículos Aéreos No Tripulados) con inteligencia de enjambre, (2) sistemas de aeronaves (Airbus A320 / Boeing B737), (3) revisión de literatura académica asistida por IA, y (4) proyectos institucionales CENALTEC. Propietario: Andrés Hidalgo Morales.

## Tech Stack
- **Lenguaje**: Python >=3.12, ejecutado vía `uv run python`
- **Package Manager**: `uv` 0.11.8
- **Formateo/Linting**: Ruff (config pendiente en `pyproject.toml`)
- **Testing**: pytest, hypothesis (disponibles pero sin tests aún)

## Dependencias Clave
- **CrewAI** `>=1.6.1` — orquestación multi-agente
- **LangChain Ollama** `>=1.1.0` / **LangGraph** `>=1.1.10` — flujos de agentes
- **LiteLLM** `>=1.83.0` — interfaz unificada LLM
- **MCP** `>=1.27.0` — protocolo de herramientas/servidores
- **Polars** (pandas/sklearn/numpy/scipy) — ciencia de datos
- **DuckDB** — consultas SQL analíticas
- **Prefect** `>=3.6.25` — orquestación de pipelines
- **Optuna** + **wandb** — optimización y tracking
- **Typer** — CLI
- **python-docx / reportlab / docxtpl** — generación de documentos
- **Manim** `>=0.20.1` — animaciones matemáticas

## Estructura del Proyecto
```
├── src/                    # Código Python principal
│   ├── cli.py              # CLI Typer (make audit)
│   ├── pipeline_tecnico.py # Pipeline de datos (CSV → Parquet → DuckDB)
│   ├── prisma_checker.py   # Validador PRISMA/Elsevier para LaTeX
│   ├── latex_checker.py    # Consistencia BibTeX
│   ├── fix_bib.py          # Reparación de .bib vía Crossref API
│   ├── auditor_*.py        # 6 variantes de auditores CrewAI+Ollama
│   ├── crew_*.py           # Pipelines generativos multi-agente
│   ├── agents/
│   │   └── system_auditor.py  # Agente auditor reutilizable
│   ├── mcp/
│   │   └── client.py       # Cliente MCP asíncrono
│   └── tools/
│       └── fs_tools.py     # Herramientas de sistema de archivos
├── Revision/               # Paper académico (Swarm Intelligence for Multi-RPAS)
│   ├── main_expanded.tex   # Manuscrito LaTeX (formato Elsevier)
│   └── Swarm Intelligence Algorithms for Multi-RPAS/
│       ├── 47 scripts Python
│       └── PAPER_REVISION_SWARM_RPAS/  # Flujo completo del paper
├── Tesis/                  # Tesis doctoral
│   ├── main.tex            # Archivo principal LaTeX
│   ├── ito.cls             # Clase personalizada
│   ├── Makefile            # Compilación XeLaTeX + Biber
│   └── contenido/          # Capítulos, preámbulo, epílogo
├── CENALTEC-PROYECTOS/     # Proyectos institucionales
├── SISTEMAS-DE-AERONAVES/  # Materiales de capacitación A320/B737
├── data/raw/               # Datos de entrada (CSV)
├── data/processed/         # Datos procesados (Parquet)
├── figures/                # Figuras generadas
└── reports/                # Reportes generados (MD, DOCX)
```

## Segundo Cerebro (Obsidian + OpenCode)

El vault Obsidian **antigravity-proyectos** ES la raíz de este repo. OpenCode lo
trata como un *AI Knowledge OS* local-first: las notas son Markdown plano (sin
capa propietaria, soberanía total de datos) y el agente razona sobre ellas con
las herramientas `read`/`edit`/`glob`/`grep` y las `obsidian_*` del MCP. Procesa
con modelos locales (Ollama) para coste cero y privacidad total.

### Arquitectura del vault (híbrido PARA + Zettelkasten)

```
Inbox/                # Captura bruta sin procesar → se vacía con /inbox
Plantillas/           # Dia, Paper, Proyecto-Hito, Clase (respetar frontmatter)
Proyectos/            # Proyectos activos: CENALTEC, Revision-RPAS, Tesis
  ├── <X>/MOC - <X>.md  # Mapas de contenido del proyecto
Clases/               # Áreas de conocimiento: Navegacion-Aerea, Sistemas-de-Aeronaves
  ├── <X>/MOC - <X>.md
Dashboard - *.md      # Dashboards Dataview (NO modificar)
Proyectos/memoria-opencode.md  # Memoria de sesiones (la gestiona MemoriaPlugin)
```

### Convenciones de etiquetado (propiedades YAML)

- Tags del sistema (filtran los dashboards Dataview): `inbox`, `paper`, `clase`,
  `proyecto`, `hito`, `memoria`. No inventes tags nuevos salvo que el usuario lo
  pida.
- Fechas en formato `DD-MM-YYYY`.
- Campos comunes: `fecha`, `fuente`, `estado`, `prioridad`, `project`.
- Nunca añadas campos que rompan los dashboards: usa SOLO los de la plantilla
  correspondiente. Preserva tags y frontmatter al mover notas.

### Protocolos de automatización

- **`/captura`** — guardar idea/tarea/referencia en `Inbox/` sin procesar.
- **`/inbox`** — clasificar cada nota según plantilla y moverla a su destino.
- **`/enlazar`** — sugerir enlaces bidireccionales `[[ ]]` entre notas que
  comparten conceptos (búsqueda semántica con grep/obsidian_search).
- **`/patrones`** — analizar diarios y notas para detectar tendencias, temas
  recurrentes y conexiones temporales ("socio de pensamiento").
- **`/backup`** — commit git del vault (nunca push sin pedir).
- Regla de oro: si una nota no encaja claramente en un destino, PREGUNTA antes
  de moverla. Nunca adivines.

## Convenciones de Código

### Naming & Estilo
- `snake_case` para funciones/variables, `PascalCase` para clases
- Type hints obligatorios en firmas de funciones
- `pathlib.Path` para rutas (nunca strings planos)
- Docstrings triples al inicio de cada módulo
- `flush=True` en prints para visibilidad en tiempo real

### CrewAI (patrón consistente en todos los auditores)
```python
llm = LLM(model="ollama/qwen2.5:1.5b", base_url="http://localhost:11434",
          temperature=0.1, timeout=120)
agent = Agent(role="...", goal="...", backstory="...", llm=llm,
              verbose=True, allow_delegation=False)
task = Task(description="...", expected_output="...", agent=agent)
crew = Crew(agents=[agent], tasks=[task], process=Process.sequential,
            verbose=True, memory=False, cache=False)
resultado = crew.kickoff()
```

### Pipeline de Datos
1. Lectura: `polars.read_csv()` / `polars.read_excel()`
2. Limpieza: `.unique()`, `.fill_null()`, selectores polars
3. Escritura: `df.write_parquet()`
4. Análisis: DuckDB SQL

### Manejo de Errores
- Degradación graceful (nunca crashes silenciosos)
- Timeouts generosos (120-300s) para Ollama en CPU sin AVX2
- try/except en todas las operaciones de red y archivo

## Comandos Útiles
```bash
uv run python src/cli.py           # Ejecutar CLI auditor
uv run python src/prisma_checker.py # Validar PRISMA
uv run python src/latex_checker.py  # Verificar BibTeX
uv run python src/pipeline_tecnico.py # Pipeline de datos
uv run python src/fix_bib.py        # Reparar .bib
make compile                        # Compilar paper LaTeX
make -C Tesis compile               # Compilar tesis
```

## LLM y Configuración
- **Local**: Ollama con `qwen2.5:1.5b` (CPU sin AVX2)
- **Cloud**: Anthropic Claude + Google Gemini (vía LiteLLM)
- **Timeout**: 60-300 segundos
- `.env` con limits de recursos Ollama
- API keys template en `agencia-creativa-ia/.env`

## Testing
- pytest + hypothesis disponibles en dependencias
- Sin tests implementados aún
- Validación implícita vía prisma_checker / latex_checker

## Git
- Rama única: `main`
- Remote: `hidalmora79-coder/ANTIGRAVITY-PROYECTOS`
- Commits convencionales: initial commit, feat, chore
