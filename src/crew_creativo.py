#!/usr/bin/env python3
"""
🚀 Crew Creativo Antigravity - CrewAI 0.100+ compatible
Flujo: Director → Investigador → Redactor
Backend: Ollama local (sin cuotas, offline-ready)
"""
import sys
import time
from pathlib import Path
from crewai import Agent, Task, Crew, Process, LLM

# 🔌 Configuración del LLM para CrewAI moderno
def get_llm_config():
    """Devuelve config compatible con CrewAI 0.100+"""
    return {
        "model": "ollama/qwen2.5:1.5b",  # Prefijo "ollama/" es obligatorio
        "base_url": "http://localhost:11434",
        "temperature": 0.7,
        "timeout": 120,
    }

# 👥 Definición de agentes
def crear_agentes(llm_config):
    return {
        "director": Agent(
            role="Director Creativo",
            goal="Definir el tono, estructura y mensaje clave del contenido",
            backstory="Experto en narrativa y estrategia. Prioriza claridad, coherencia y valor para el lector.",
            llm=llm_config,  # ← Ahora es un dict, no un objeto ChatOllama
            allow_delegation=False,
            verbose=True
        ),
        "investigador": Agent(
            role="Investigador Senior",
            goal="Recopilar datos, referencias y ejemplos concretos para sustentar la idea",
            backstory="Analítico, metódico y obsesionado con fuentes verificables y datos actualizados.",
            llm=llm_config,
            allow_delegation=False,
            verbose=True
        ),
        "redactor": Agent(
            role="Redactor Técnico",
            goal="Transformar la estrategia y datos en un documento listo para publicación",
            backstory="Escribe con precisión, evita relleno y adapta el tono al público objetivo.",
            llm=llm_config,
            allow_delegation=False,
            verbose=True
        )
    }

# 📝 Definición de tareas
def crear_tareas(agentes, tema):
    return [
        Task(
            description=f"Define el mensaje central, audiencia objetivo y estructura recomendada para: '{tema}'",
            expected_output="Documento de 1 párrafo con: tono, público, estructura de 3 secciones y 1 insight clave.",
            agent=agentes["director"],
            async_execution=False
        ),
        Task(
            description="Busca 3 datos, ejemplos o referencias técnicas que respalden el enfoque del director.",
            expected_output="Lista numerada de 3 elementos con fuente o contexto breve.",
            agent=agentes["investigador"],
            async_execution=False
        ),
        Task(
            description="Redacta el contenido final integrando el brief y los datos. Formato Markdown.",
            expected_output="Texto completo en Markdown, listo para publicar o exportar.",
            agent=agentes["redactor"],
            async_execution=False
        )
    ]

# 🚀 Ejecución principal
def main(tema: str = "Automatización de reportes con Python en 2026"):
    print(f"🎯 Tema: {tema}\n" + "="*60, flush=True)
    
    # Verificar conexión con Ollama
    import urllib.request
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=5)
        print("✅ Ollama disponible en localhost:11434\n", flush=True)
    except Exception as e:
        print(f"❌ No se conecta con Ollama: {e}", file=sys.stderr)
        print("💡 Ejecuta: ollama serve", file=sys.stderr)
        sys.exit(1)
    
    # Inicializar componentes
    llm_config = get_llm_config()
    agentes = crear_agentes(llm_config)
    tareas = crear_tareas(agentes, tema)
    
    # Crear y ejecutar Crew
    print("🚀 Iniciando flujo creativo (1-2 min en CPU)...\n", flush=True)
    
    crew = Crew(
        agents=list(agentes.values()),
        tasks=tareas,
        process=Process.sequential,
        verbose=True,
        memory=False,
        cache=False
    )
    
    resultado = crew.kickoff(inputs={"tema": tema})
    
    # Output final
    print("\n" + "="*60)
    print("📄 RESULTADO FINAL")
    print("="*60)
    print(resultado.raw)
    
    # Guardar a archivo
    output_path = Path("reports") / f"crew_{int(time.time())}.md"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(resultado.raw, encoding="utf-8")
    print(f"\n💾 Guardado en: {output_path}")
    
    return resultado.raw

if __name__ == "__main__":
    tema = sys.argv[1] if len(sys.argv) > 1 else "Automatización de reportes con Python en 2026"
    main(tema)