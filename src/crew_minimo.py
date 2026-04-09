#!/usr/bin/env python3
"""Crew mínimo con CrewAI 1.6.1 + Ollama + litellm"""
import sys
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM

# 🔌 Configuración LLM (formato compatible con CrewAI 1.x + litellm)
llm = LLM(
    model="ollama/qwen2.5:1.5b",
    base_url="http://localhost:11434",
    temperature=0.7,
    timeout=120
)

# 👥 Agentes
director = Agent(
    role="Director Creativo",
    goal="Definir estructura y tono del contenido",
    backstory="Experto en narrativa clara y coherente.",
    llm=llm,
    verbose=True
)

redactor = Agent(
    role="Redactor Técnico",
    goal="Escribir contenido listo para publicar",
    backstory="Preciso, adapta el tono al público objetivo.",
    llm=llm,
    verbose=True
)

# 📝 Tareas
tema = sys.argv[1] if len(sys.argv) > 1 else "IA local en investigación"

t1 = Task(
    description=f"Crea un brief de 3 puntos clave para: '{tema}'",
    expected_output="Lista numerada de 3 puntos.",
    agent=director
)

t2 = Task(
    description="Redacta un párrafo introductorio basado en el brief.",
    expected_output="Párrafo en formato Markdown.",
    agent=redactor
)

# 🚀 Ejecutar
print(f"🎯 Tema: {tema}\n🚀 Iniciando crew (1-2 min en CPU)...\n", flush=True)

crew = Crew(
    agents=[director, redactor],
    tasks=[t1, t2],
    process=Process.sequential,
    verbose=True,
    memory=False,
    cache=False
)

resultado = crew.kickoff()

print("\n" + "="*60)
print("📄 RESULTADO")
print("="*60)
print(resultado.raw)

# Guardar
output = Path("reports") / f"crew_{Path.cwd().name}_{int(__import__('time').time())}.md"
output.parent.mkdir(exist_ok=True)
output.write_text(resultado.raw, encoding="utf-8")
print(f"\n💾 Guardado: {output}")
