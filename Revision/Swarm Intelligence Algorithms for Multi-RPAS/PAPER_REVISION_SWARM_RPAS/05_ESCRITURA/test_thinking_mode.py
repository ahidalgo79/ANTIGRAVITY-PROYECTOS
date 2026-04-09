import os
from dotenv import load_dotenv
from anthropic import Anthropic
import sys

# Forzar UTF-8 para la salida estándar en Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cargar variables de entorno
env_path = os.path.join(os.getcwd(), "..", "..", ".env")
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("❌ No se encontró ANTHROPIC_API_KEY en el entorno.")
    exit(1)

cliente = Anthropic(api_key=api_key)

prompt_sistema = """
Actúa como un Ingeniero de Sistemas Aeroespaciales y Arquitecto Agéntico.

Tarea: Realiza un análisis exhaustivo de la eficiencia de los algoritmos de enjambre 
(PSO vs. ACO) en misiones de búsqueda y rescate (SAR) para sistemas multi-RPAS.

Instrucciones de Pensamiento (STAR):

1. Formulación: Define el estado del sistema y las variables de costo 
   (energía, tiempo, cobertura).

2. Modelado: Utiliza tu presupuesto de pensamiento para derivar la función 
   de optimización en LaTeX.

3. Verificación: Valida que tus conclusiones respeten la muestra de n=30 
   estudios primarios y utilicen unidades del Sistema Internacional (SI).

4. Gobernanza: Tu respuesta final debe ser una síntesis técnica de grado 
   Elsevier, sin preámbulos innecesarios.

Restricciones críticas:
- No uses términos no estándar como "drone", usa "RPAS" o "UAV"
- Todas las magnitudes deben incluir unidades SI
- La muestra total es n=30 (23 primarios + 7 reviews)
"""

try:
    print(f"🚀 Iniciando petición a Claude Sonnet 4.6 (Latest March 2026) con Thinking Mode...")
    print("-" * 60)
    
    # Usando el identificador de modelo correcto para marzo de 2026
    response = cliente.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        thinking={"type": "enabled", "budget_tokens": 4096},
        messages=[{"role": "user", "content": prompt_sistema}]
    )
    
    print("=" * 60)
    print("RESULTADO DE LA PRUEBA - THINKING MODE")
    print("=" * 60)
    
    thinking_content = ""
    final_text = ""
    
    for block in response.content:
        if block.type == "thinking":
            thinking_content = block.thinking
        elif block.type == "text":
            final_text = block.text
    
    if thinking_content:
        print("\n🧠 BLOQUE DE PENSAMIENTO:")
        print("-" * 40)
        print(thinking_content)
        print("-" * 40)
        print(f"Tokens de pensamiento utilizados: {len(thinking_content.split()) * 1.3:.0f}")
    
    print("\n📝 RESPUESTA FINAL (Nivel Elsevier):")
    print("-" * 40)
    print(final_text)
    print("-" * 40)
    
    print("\n✅ FASE 1 COMPLETADA - Thinking mode ejecutado exitosamente")
    
except Exception as e:
    print(f"❌ Error durante la ejecución: {e}")