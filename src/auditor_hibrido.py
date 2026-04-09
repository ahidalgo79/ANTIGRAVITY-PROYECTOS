#!/usr/bin/env python3
"""Auditor Híbrido: Python extrae datos reales → CrewAI formatea reporte. Cero alucinaciones."""
import sys
import time
import tomllib
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM

# 🔌 1. Recopilar datos REALES del sistema (sin LLM)
def extraer_datos_reales(ruta: str) -> dict:
    p = Path(ruta).resolve()
    
    # Python y SO
    py_ver = sys.version.split()[0]
    os_info = f"{sys.platform} {sys.implementation.name}"
    
    # pyproject.toml
    toml_path = p / "pyproject.toml"
    deps = "NO ENCONTRADO"
    if toml_path.exists():
        try:
            with open(toml_path, "rb") as f:
                data = tomllib.load(f)
            deps_list = data.get("project", {}).get("dependencies", [])
            deps = "\n".join(f"- {d}" for d in deps_list) if deps_list else "Sin dependencias explícitas"
        except Exception as e:
            deps = f"Error leyendo toml: {e}"
            
    # Estructura de archivos (nivel raíz, sin ocultos)
    archivos = sorted([f.name for f in p.iterdir() if not f.name.startswith('.') and not f.is_dir()])
    dirs = sorted([d.name + "/" for d in p.iterdir() if d.is_dir() and not d.name.startswith('.')])
    estructura = "\n".join(dirs + archivos)
    
    return {
        "python": py_ver,
        "os": os_info,
        "deps": deps,
        "estructura": estructura or "Directorio vacío",
        "ruta": str(p)
    }

# 🧠 2. Configuración LLM
llm = LLM(
    model="ollama/qwen2.5:1.5b",
    base_url="http://localhost:11434",
    temperature=0.1,  # Mínimo para evitar alucinaciones
    timeout=120
)

# 👥 3. Agente (SOLO formatea, NO lee archivos)
auditor = Agent(
    role="Redactor Técnico de Auditorías",
    goal="Formatear datos crudos en un reporte Markdown profesional, preciso y accionable",
    backstory="""Eres experto en documentación técnica para ingenieros.
    TU ÚNICA TAREA es organizar los datos proporcionados.
    ⛔ PROHIBIDO inventar versiones, librerías o comandos no presentes en los datos.""",
    llm=llm,
    verbose=True,
    max_iter=3,
    allow_delegation=False
)

# 📝 4. Tarea con datos inyectados
def crear_tarea(datos: dict, enfoque: str) -> Task:
    prompt = f"""
    Genera un REPORTE DE AUDITORÍA en Markdown para un proyecto Python.
    Enfoque del análisis: {enfoque}
    
    📊 DATOS EXTRAÍDOS DEL SISTEMA (USA SOLO ESTO):
    - Ruta: {datos['ruta']}
    - Python: {datos['python']}
    - SO: {datos['os']}
    - Dependencias (pyproject.toml):
    {datos['deps']}
    
    - Estructura de archivos:
    {datos['estructura']}
    
    📋 ESTRUCTURA OBLIGATORIA DEL REPORTE:
    # 🛠️ Estado REAL del Entorno
    # 📦 Stack Tecnológico Detectado
    # 🔍 Estructura y Archivos Clave
    # ⚠️ Observaciones y Recomendaciones
    # 🚀 3 Comandos Concretos para este proyecto
    
    ⛔ REGLAS ERICTAS:
    1. Responde en ESPAÑOL.
    2. NUNCA menciones Flask, pip, uvicorn, SQLAlchemy ni versiones no listadas arriba.
    3. Si faltan datos (ej: no hay .env), menciónalo como observación.
    4. Los comandos deben usar `uv` si el proyecto lo usa.
    5. Output: SOLO el Markdown. Sin preámbulos ni explicaciones extra.
    """
    
    return Task(
        description=prompt,
        expected_output="Markdown válido, preciso y estructurado según las reglas.",
        agent=auditor,
        async_execution=False
    )

# 🚀 5. Ejecución
def main(ruta: str = ".", enfoque: str = "ia-agents"):
    print(f"🔍 Recopilando datos reales de: {ruta}...", flush=True)
    datos = extraer_datos_reales(ruta)
    
    print("🤖 Generando reporte con CrewAI...", flush=True)
    tarea = crear_tarea(datos, enfoque)
    
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
    print("📄 REPORTE PRECISO")
    print("="*60)
    print(resultado.raw)
    
    # 💾 Guardar
    out = Path("reports") / f"auditoria_hibrida_{int(time.time())}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(resultado.raw, encoding="utf-8")
    print(f"\n💾 Guardado: {out}")
    
    return resultado.raw

if __name__ == "__main__":
    ruta = sys.argv[1] if len(sys.argv) > 1 else "."
    enfoque = sys.argv[2] if len(sys.argv) > 2 else "ia-agents"
    main(ruta, enfoque)
