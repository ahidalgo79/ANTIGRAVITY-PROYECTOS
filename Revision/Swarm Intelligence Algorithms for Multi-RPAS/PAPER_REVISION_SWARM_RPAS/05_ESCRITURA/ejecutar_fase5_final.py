import os
import sys
import json
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from csp_guardrail import CSPGuardrail

# Configurar UTF-8 para Windows (evita UnicodeEncodeError)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cargar variables de entorno (2 niveles arriba según estructura del proyecto)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("=" * 70)
print("🚀 FASE 5: REDACCIÓN DE DISCUSIÓN CIENTÍFICA")
print("=" * 70)
print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Modelo: Claude Sonnet 4.6 (Thinking Mode: 4096 tokens)")
print(f"LangSmith Tracing: {os.getenv('LANGSMITH_TRACING', 'false')}")
print("=" * 70)

# Inicializar
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ Error: ANTHROPIC_API_KEY no encontrada.")
    exit(1)

cliente = Anthropic(api_key=api_key)
guardrail = CSPGuardrail()

# Prompt maestro STAR + SCHEMA
PROMPT_MAESTRO = """
Actúa como un Senior Systems Engineer y Orquestador de Redacción para un manuscrito Elsevier.

=== FASE DE PENSAMIENTO EXTENDIDO (Thinking Mode - 4096 tokens) ===

STAR Reasoning:
1. Formulación: Formula el impacto de los algoritmos PSO y ACO detectados en el RAG 
   sobre la eficiencia energética en misiones de búsqueda y rescate (SAR) para sistemas multi-RPAS.

2. Modelado: Deriva en LaTeX la relación entre el tamaño del enjambre y la latencia de comunicación:
   
   \\tau_{total} = \\alpha \\cdot N_{agentes} \\cdot d_{interagente} / v_{signal} + \\beta \\cdot \\zeta_{energia} \\cdot N_{transmisiones}
   
   Donde:
   - \\tau_{total}: tiempo total de comunicación (s)
   - N_{agentes}: número de RPAS en el enjambre
   - d_{interagente}: distancia media entre agentes (m)
   - v_{signal}: velocidad de propagación de la señal (m/s)
   - \\zeta_{energia}: consumo energético por transmisión (J)
   - \\alpha, \\beta: coeficientes de eficiencia algorítmica

3. Validación CSP Interna (OBLIGATORIA): 
   - Verifica explícitamente que n=30 (23 primarios + 7 reviews)
   - Asegura unidades SI: tiempo (s), energía (J), distancia (m), velocidad (m/s)
   - Confirma terminología ICAO: RPAS/UAV, NUNCA "drone"

=== FASE SCHEMA (Directrices de Gobernanza) ===

Conductor: Sintetiza la brecha entre la teoría de enjambres y la implementación 
real en misiones SAR, basado en los 23 estudios primarios del corpus.

Arquitecto de Interfaz: 
- Formato LaTeX compatible con Elsevier
- Prohibido "drone", usar "RPAS" o "UAV"
- Unidades SI obligatorias en todas las magnitudes

Aprendizaje DPO: Inyecta preferencias de estilo (tono académico formal, conciso, citas integradas)

=== ACCIÓN AGÉNTICA ===

Redacta 3 párrafos de alta densidad técnica con citas del corpus indexado:

PÁRRAFO 1 - Hallazgos principales de algoritmos de enjambre:
- Comparativa cuantitativa PSO vs ACO en eficiencia energética
- Identificación de métricas clave reportadas en los estudios

PÁRRAFO 2 - Comparativa con literatura existente:
- Contextualización dentro del estado del arte
- Identificación de contribuciones novedosas del corpus

PÁRRAFO 3 - Implicaciones y direcciones futuras:
- Limitaciones metodológicas detectadas
- Propuestas para investigación futura

Restricción crítica: Cada afirmación técnica debe estar anclada a un paper del corpus (cita implícita o explícita).

Formato de salida: Texto continuo en español académico, con ecuaciones en $$...$$ o \\[...\\].
"""

print("\n[1/4] Enviando prompt a Claude con Thinking Mode...")
print("-" * 70)

try:
    response = cliente.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        thinking={"type": "enabled", "budget_tokens": 4096},
        messages=[{"role": "user", "content": PROMPT_MAESTRO}]
    )
    
    # Extraer bloques
    thinking_content = ""
    final_text = ""
    
    for block in response.content:
        if block.type == "thinking":
            thinking_content = block.thinking
        elif block.type == "text":
            final_text = block.text
    
    print("\n[2/4] Validando con CSP Guardrail...")
    es_valido, violaciones = guardrail.validar(final_text)
    
    # Directorio de salida (el mismo que el script)
    output_dir = Path(__file__).parent
    
    print("\n[3/4] Guardando resultados...")
    
    # Guardar bloque de pensamiento
    with open(output_dir / "thinking_log.txt", "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write("BLOQUE DE PENSAMIENTO - CLAUDE 4.6\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write("=" * 70 + "\n\n")
        f.write(thinking_content)
    
    # Guardar discusión
    with open(output_dir / "discusion_generada.tex", "w", encoding="utf-8") as f:
        f.write("% ============================================================\n")
        f.write(f"% DISCUSIÓN GENERADA - {datetime.now().strftime('%Y-%m-%d')}\n")
        f.write("% Modelo: Claude Sonnet 4.6 (Thinking Mode)\n")
        f.write("% Validación CSP: " + ("APROBADA" if es_valido else "RECHAZADA") + "\n")
        f.write("% ============================================================\n\n")
        f.write(final_text)
    
    # Guardar metadata
    metadata = {
        "timestamp": datetime.now().isoformat(),
        "modelo": "claude-sonnet-4-6",
        "thinking_budget_tokens": 4096,
        "max_tokens": 8192,
        "longitud_respuesta": len(final_text),
        "longitud_pensamiento": len(thinking_content),
        "valido_csp": es_valido,
        "violaciones": violaciones
    }
    
    with open(output_dir / "discusion_metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    
    print("\n[4/4] Resultado final:")
    print("=" * 70)
    
    print(f"\n🧠 BLOQUE DE PENSAMIENTO:")
    print("-" * 50)
    print(f"Longitud: {len(thinking_content)} caracteres")
    print(f"Tokens estimados: {len(thinking_content.split()) * 1.3:.0f}")
    
    print(f"\n📝 DISCUSIÓN GENERADA:")
    print("-" * 50)
    print(f"Longitud: {len(final_text)} caracteres")
    print(f"Válida CSP: {'✅ SÍ' if es_valido else '❌ NO'}")
    
    if violaciones:
        print(f"\n⚠️ Violaciones detectadas:")
        for v in violaciones:
            print(f"   - {v}")
    
    print(f"\n📁 Archivos generados en {output_dir}:")
    print(f"   - discusion_generada.tex")
    print(f"   - thinking_log.txt")
    print(f"   - discusion_metadata.json")
    
    print("\n" + "=" * 70)
    print("✅ FASE 5 COMPLETADA")
    print("=" * 70)
    
    # Mostrar preview
    print("\n📋 PREVIEW DE LA DISCUSIÓN:")
    print("-" * 70)
    print(final_text[:800] + "..." if len(final_text) > 800 else final_text)
    print("-" * 70)
    
except Exception as e:
    print(f"\n❌ Error durante la ejecución: {e}")
