#!/usr/bin/env python3
"""Auditor seguro con pre-flight check + timeout extendido + prompt optimizado."""
import sys
import time
import urllib.request
import tomllib
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM

# 🔌 Pre-flight: Verifica Ollama antes de iniciar CrewAI
def verificar_ollama():
    url = "http://localhost:11434/api/tags"
    try:
        resp = urllib.request.urlopen(url, timeout=10)
        if resp.status == 200:
            print("✅ Ollama responde en localhost:11434", flush=True)
            return True
    except Exception:
        print("❌ Ollama NO responde. Ejecuta: ollama serve", file=sys.stderr)
        sys.exit(1)

# 📊 Extrae datos REALES (Python hace lo que mejor sabe)
def extraer_datos(ruta: str) -> str:
    p = Path(ruta).resolve()
    py_ver = sys.version.split()[0]
    toml = p / "pyproject.toml"
    deps = "NO ENCONTRADO"
    if toml.exists():
        try:
            with open(toml, "rb") as f:
                data = tomllib.load(f)
            deps = "\n".join(f"- {d}" for d in data.get("project", {}).get("dependencies", []))
        except Exception: deps = "Error leyendo pyproject.toml"
    estructura = "\n".join(sorted([f.name for f in p.iterdir() if not f.name.startswith('.')]))
    return f"""RUTA: {p}
PYTHON: {py_ver}
DEPENDENCIAS (pyproject.toml):\n{deps}
ARCHIVOS/DIRS:\n{estructura}"""

# 🧠 LLM con timeout extendido para CPU
llm = LLM(
    model="ollama/qwen2.5:1.5b",
    base_url="http://localhost:11434",
    temperature=0.1,
    timeout=300,  # 5 minutos (suficiente para carga fría + inferencia)
    max_retries=2
)

auditor = Agent(
    role="Formateador Técnico",
    goal="Convertir datos crudos en un reporte Markdown limpio y accionable",
    backstory="Eres preciso. NUNCA inventas datos. Usas SOLO la información proporcionada.",
    llm=llm, verbose=True, max_iter=3, allow_delegation=False
)

def main(ruta: str = ".", enfoque: str = "ia-agents"):
    verificar_ollama()
    print(f"📊 Extrayendo datos reales de: {ruta}...", flush=True)
    datos_crudos = extraer_datos(ruta)
    
    tarea = Task(
        description=f"""
        Genera un reporte de auditoría en Markdown.
        DATOS REALES DEL SISTEMA (USA EXACTAMENTE ESTO):
        {datos_crudos}
        
        ESTRUCTURA OBLIGATORIA:
        # 🛠️ Estado del Entorno
        # �� Stack Detectado
        # 🔍 Estructura de Archivos
        # ⚠️ Observaciones
        # 🚀 3 Comandos Concretos
        
        REGLAS: Responde en ESPAÑOL. No inventes versiones ni librerías. Si algo falta, dilo.
        """,
        expected_output="Markdown válido y preciso.",
        agent=auditor, async_execution=False
    )
    
    print("🤖 Generando reporte (puede tardar 1-3 min en CPU)...", flush=True)
    crew = Crew(agents=[auditor], tasks=[tarea], process=Process.sequential, verbose=True, memory=False, cache=False)
    resultado = crew.kickoff()
    
    print("\n" + "="*60 + "\n📄 REPORTE\n" + "="*60 + "\n" + resultado.raw)
    out = Path("reports") / f"auditoria_segura_{int(time.time())}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(resultado.raw, encoding="utf-8")
    print(f"\n💾 Guardado: {out}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "ia-agents")
