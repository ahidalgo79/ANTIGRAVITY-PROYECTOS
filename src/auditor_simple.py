#!/usr/bin/env python3
"""Auditor de sistema mínimo - CrewAI 1.6.1 compatible"""
import sys
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import DirectoryReadTool, FileReadTool, ShellTool

# 🔌 LLM local (Ollama)
llm = LLM(
    model="ollama/qwen2.5:1.5b",
    base_url="http://localhost:11434",
    temperature=0.3,
    timeout=180
)

# 🛠️ Herramientas integradas (ya son BaseTool compatibles)
tools = [
    DirectoryReadTool(),  # Lista directorios
    FileReadTool(),       # Lee archivos
    ShellTool(),          # Ejecuta comandos shell (opcional, útil para git, du, etc.)
]

# 👥 Agente
auditor = Agent(
    role="Auditor de Sistema",
    goal="Analizar el entorno y generar un reporte estructurado en Markdown",
    backstory="""Eres un ingeniero experto en Python, IA y DevOps.
    Tu estilo es claro, técnico pero accesible. Siempre propones próximos pasos concretos.""",
    llm=llm,
    tools=tools,  # ← Ahora son instancias de BaseTool ✅
    verbose=True,
    allow_delegation=False,
    max_iter=5  # Evita bucles infinitos en CPU
)

# 📝 Tarea
def crear_tarea(ruta: str, enfoque: str) -> Task:
    return Task(
        description=f"""
        Analiza el directorio '{ruta}' con enfoque en: {enfoque}.
        
        Pasos:
        1. Lista la estructura (usa DirectoryReadTool, máx. 2 niveles)
        2. Lee pyproject.toml y requirements.txt (primeras 20 líneas)
        3. Identifica archivos .py clave y resume su propósito
        4. Revisa si hay .env y qué variables faltan (sin mostrar valores secretos)
        5. Genera un reporte en Markdown con:
           - 🛠️ Estado del entorno
           - 📦 Stack detectado
           - 🔍 Hallazgos clave
           - ⚠️ Advertencias
           - 🚀 3 recomendaciones accionables
        """,
        expected_output="Reporte en Markdown con emojis, secciones claras y comandos listos para copiar.",
        agent=auditor,
        async_execution=False
    )

# 🚀 Ejecución
def main(ruta: str = ".", enfoque: str = "ia-agents"):
    print(f"🔍 Auditando: {ruta} | Enfoque: {enfoque}\n", flush=True)
    
    tarea = crear_tarea(ruta, enfoque)
    
    crew = Crew(
        agents=[auditor],
        tasks=[tarea],
        process=Process.sequential,
        verbose=True,
        memory=False,
        cache=False
    )
    
    resultado = crew.kickoff()
    
    print("\n" + "="*60)
    print("📄 REPORTE DE AUDITORÍA")
    print("="*60)
    print(resultado.raw)
    
    # Guardar
    output = Path("reports") / f"auditoria_{int(__import__('time').time())}.md"
    output.parent.mkdir(exist_ok=True)
    output.write_text(resultado.raw, encoding="utf-8")
    print(f"\n💾 Guardado: {output}")
    
    return resultado.raw

if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "."
    enfoque = sys.argv[2] if len(sys.argv) > 2 else "ia-agents"
    main(ruta, enfoque)
