#!/usr/bin/env python3
"""Auditor mínimo - CrewAI 1.6.1 compatible, sin dependencias frágiles"""
import sys
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM

# 🔌 LLM local (Ollama) - configuración robusta
llm = LLM(
    model="ollama/qwen2.5:1.5b",
    base_url="http://localhost:11434",
    temperature=0.2,
    timeout=180
)

# 👥 Agente SIN herramientas externas (evita errores de import)
auditor = Agent(
    role="Auditor de Sistema",
    goal="Analizar el entorno y generar un reporte estructurado en Markdown",
    backstory="""Eres un ingeniero experto en Python, IA y DevOps.
    Analizas código, configuraciones y estructuras de proyecto.
    Tu estilo es claro, técnico pero accesible.""",
    llm=llm,
    verbose=True,
    allow_delegation=False,
    max_iter=4
)

# 📝 Tarea: el agente "simula" la auditoría con su conocimiento
def crear_tarea(ruta: str, enfoque: str) -> Task:
    return Task(
        description=f"""
        Basándote en tu conocimiento técnico, describe cómo auditarías 
        un proyecto Python en '{ruta}' con enfoque en: {enfoque}.
        
        Estructura tu respuesta como un reporte real con:
        - 🛠️ Estado del entorno (uv/pip, Python version, OS)
        - 📦 Stack tecnológico típico para {enfoque}
        - 🔍 Qué archivos buscarías y por qué
        - ⚠️ Errores comunes a verificar
        - 🚀 3 comandos concretos para empezar
        
        Nota: No ejecutes código real, solo describe el flujo profesional.
        """,
        expected_output="Reporte en Markdown con secciones claras, emojis y comandos listos para copiar.",
        agent=auditor,
        async_execution=False
    )

# 🚀 Ejecución principal
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
    
    print("🚀 Ejecutando agente (60-90s en CPU)...\n", flush=True)
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
