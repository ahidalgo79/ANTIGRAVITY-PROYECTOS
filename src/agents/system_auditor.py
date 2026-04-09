"""Agente que analiza tu entorno y genera reportes estructurados"""
from crewai import Agent, Task, Crew, Process, LLM
from src.tools.fs_tools import list_directory, read_file, get_env_vars
from src.mcp.client import mcp_call

# 🔌 LLM local (Ollama)
llm = LLM(
    model="ollama/qwen2.5:1.5b",
    base_url="http://localhost:11434",
    temperature=0.3,  # Bajo para análisis preciso
    timeout=180
)

# 👥 Agente especializado
auditor = Agent(
    role="Auditor de Sistema Senior",
    goal="Analizar el entorno de trabajo y generar un reporte estructurado con recomendaciones accionables",
    backstory="""Eres un ingeniero de DevOps experto en Python, IA y flujos de investigación.
    Tu estilo es claro, técnico pero accesible, y siempre propones próximos pasos concretos.""",
    llm=llm,
    tools=[list_directory, read_file, get_env_vars],  # ← Herramientas nativas
    verbose=True,
    allow_delegation=False
)

# 📝 Tarea principal
def crear_tarea_auditoria(ruta_base: str, enfoque: str = "general") -> Task:
    return Task(
        description=f"""
        Analiza el entorno en '{ruta_base}' con enfoque en: {enfoque}.
        
        Pasos obligatorios:
        1. Lista la estructura de directorios (máx. 2 niveles de profundidad)
        2. Lee y resume: pyproject.toml, requirements.txt (primeras 20 líneas)
        3. Busca archivos .py clave y lee sus primeras 30 líneas
        4. Consulta variables de entorno relevantes (filtra secretos)
        5. Si hay integración con NotebookLM, usa MCP para listar notebooks disponibles
        6. Genera un reporte en Markdown con:
           - 🛠️ Estado del entorno y proyectos
           - 📦 Stack tecnológico detectado
           - 🔍 Hallazgos relevantes (archivos clave, configuraciones)
           - ⚠️ Advertencias (dependencias faltantes, variables sin definir)
           - 🚀 3 recomendaciones concretas de próximos pasos
        """,
        expected_output="""
        Reporte en Markdown con secciones claras, emojis para escaneo visual,
        y comandos listos para copiar/pegar cuando sea aplicable.
        """,
        agent=auditor,
        async_execution=False
    )

# 🚀 Función principal
def auditar_entorno(ruta: str = ".", enfoque: str = "ia-agents") -> str:
    """Ejecuta la auditoría completa"""
    print(f"🔍 Auditando: {ruta} | Enfoque: {enfoque}\n", flush=True)
    
    tarea = crear_tarea_auditoria(ruta, enfoque)
    
    crew = Crew(
        agents=[auditor],
        tasks=[tarea],
        process=Process.sequential,
        verbose=True,
        memory=False,
        cache=False
    )
    
    resultado = crew.kickoff()
    return resultado.raw