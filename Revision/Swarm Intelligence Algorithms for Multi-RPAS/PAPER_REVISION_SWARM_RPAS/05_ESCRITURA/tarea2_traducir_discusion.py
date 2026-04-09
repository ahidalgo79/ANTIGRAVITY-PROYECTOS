import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
import sys

# Forzar UTF-8 para la salida estándar en Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cargar variables de entorno (buscando niveles arriba si es necesario)
env_path = Path("../../.env")
if not env_path.exists():
    env_path = Path(".env")
load_dotenv(dotenv_path=env_path)

print("=" * 60)
print("TAREA 2: TRADUCCIÓN DE DISCUSIÓN AL INGLÉS")
print("=" * 60)

# Leer la discusión en español
# Intentar rutas relativas según el CWD del proceso
discusion_path = Path("discusion_generada.tex")
if not discusion_path.exists():
    discusion_path = Path("05_ESCRITURA/discusion_generada.tex")

if not discusion_path.exists():
    print(f"❌ ERROR: No se encuentra {discusion_path.absolute()}")
    exit(1)

with open(discusion_path, 'r', encoding='utf-8') as f:
    discusion_espanol = f.read()

print(f"📄 Texto original: {len(discusion_espanol)} caracteres")

# Configurar Claude
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("❌ ERROR: No se encontró ANTHROPIC_API_KEY en el entorno.")
    exit(1)

cliente = Anthropic(api_key=api_key)

prompt_traduccion = f"""
Traduce el siguiente texto académico del español al inglés.

Es un texto técnico para un manuscrito de revista Elsevier sobre inteligencia de enjambre para UAVs en agricultura.

REGLAS:
- Mantén exactamente las mismas ecuaciones LaTeX (todo entre $$ o \\[...\\])
- Mantén las citas \\cite{{...}} exactamente igual
- Conserva la estructura de párrafos
- El tono debe ser académico formal, estilo Elsevier

TEXTO A TRADUCIR:

{discusion_espanol}

RESPONDE SOLO CON EL TEXTO TRADUCIDO, SIN COMENTARIOS ADICIONALES.
"""

print("\n🔄 Traduciendo con Claude 4.6...")

try:
    response = cliente.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        messages=[{"role": "user", "content": prompt_traduccion}]
    )
    
    discusion_ingles = response.content[0].text
    
    # Guardar la versión traducida (en la misma carpeta que el original si es posible)
    output_path = discusion_path.parent / "discusion_ingles.tex"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(discusion_ingles)
    
    print(f"\n✅ Traducción guardada: {output_path}")
    print(f"📏 Longitud: {len(discusion_ingles)} caracteres")
    
    # Mostrar preview
    print("\n📋 PREVIEW (primeros 500 caracteres):")
    print("-" * 60)
    print(discusion_ingles[:500])
    print("-" * 60)

except Exception as e:
    print(f"❌ ERROR durante la traducción: {e}")
