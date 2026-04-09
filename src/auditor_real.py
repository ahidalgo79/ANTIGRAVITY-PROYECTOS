#!/usr/bin/env python3
"""Auditor de Sistema REAL - CrewAI 1.6.1 compatible
Lee archivos reales, genera reporte específico y lo guarda."""
import sys
import time
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import DirectoryReadTool, FileReadTool

# 🔌 1. Configuración LLM (Ollama local)
llm = LLM(
    model="ollama/qwen2.5:1.5b",
    base_url="http://localhost:11434",
    temperature=0.2,
    timeout=180
)

# 🛠️ 2. Herramientas seguras y compatibles
tools = [
    DirectoryReadTool(),
    FileReadTool(),
]

# 👥 3. Agente Auditor
auditor = Agent(
    role="Auditor de Sistema Senior",
    goal="Analizar archivos reales del proyecto y generar un reporte preciso en Markdown",
    backstory="""Eres un ingeniero experto en Python, IA y DevOps.
    Tu trabajo es LEER archivos reales, extraer datos concretos y proponer mejoras accionables.
    NUNCA inventes contenido. Si no puedes leer algo, dilo explícitamente.""",
    llm=llm,
    tools=tools,
    verbose=True,
    allow_delegation=False,
    max_iter=6
)

# 📋 4. Tarea con instrucciones estrictas
def crear_tarea(ruta: str, enfoque: str) -> Task:
    return Task(
        description=f"""
        AUDITORÍA TÉCNICA REAL del directorio: '{ruta}'
        Enfoque: {enfoque}

        📋 INSTRUCCIONES OBLIGATORIAS (USA TUS HERRAMIENTAS):
        1. Usa DirectoryReadTool para explorar '{ruta}' (máx. 2 niveles)
        2. Usa FileReadTool para leer y analizar:
           - pyproject.toml (primeras 30 líneas)
           - requirements.txt (si existe)
           - 2 archivos .py que parezcan principales (ej: src/*.py, main.py, app.py)
        3. Extrae datos REALES: versión de Python, gestor (uv/pip), dependencias clave, LLM configurado.
        4. Genera un reporte en Markdown con EXACTAMENTE esta estructura:
           - 🛠️ Estado REAL del entorno (basado en lo leído)
           - 📦 Stack tecnológico detectado (lista de libs principales)
           - 🔍 Archivos clave analizados y su propósito
           - ⚠️ Advertencias específicas (errores, variables faltantes, configs raras)
           - 🚀 3 comandos CONCRETOS para mejorar/continuar este proyecto

        ⛔ REGLAS:
        - NUNCA asumas. Si no lees un archivo, dilo.
        - CITA nombres de archivos cuando sea relevante.
        - Responde en ESPAÑOL.
        - El output DEBE ser solo el Markdown del reporte.
        """,
        expected_output="Reporte en Markdown válido, específico para este proyecto, en español, con comandos listos para copiar.",
        agent=auditor,
        async_execution=False
    )

# �� 5. Ejecución principal
def main(ruta: str = ".", enfoque: str = "ia-agents"):
    print(f"🔍 Auditando: {ruta} | Enfoque: {enfoque}\n", flush=True)
    print("⚙️ Inicializando herramientas y agente...", flush=True)
    
    tarea = crear_tarea(ruta, enfoque)
    
    crew = Crew(
        agents=[auditor],
        tasks=[tarea],
        process=Process.sequential,
        verbose=True,
        memory=False,
        cache=False
    )
    
    print("🚀 Ejecutando auditoría (60-120s en CPU)...\n", flush=True)
    resultado = crew.kickoff()
    
    print("\n" + "="*60)
    print("📄 REPORTE GENERADO")
    print("="*60)
    print(resultado.raw)
    
    # 💾 Guardar
    output_dir = Path("reports")
    output_dir.mkdir(exist_ok=True)
    timestamp = int(time.time())
    output_file = output_dir / f"auditoria_real_{timestamp}.md"
    output_file.write_text(resultado.raw, encoding="utf-8")
    print(f"\n💾 Guardado: {output_file}")
    
    return resultado.raw

if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "."
    enfoque = sys.argv[2] if len(sys.argv) > 2 else "ia-agents"
    main(ruta, enfoque)
