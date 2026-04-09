import os
import re
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
import shutil
from datetime import datetime

# Load environment variables from the root .env
load_dotenv(Path("../.env"))

print("=" * 60)
print("NODO 1: CIRUGÍA DE ABSTRACT - CLAUDE 3.7 THINKING MODE")
print("=" * 60)

latex_path = Path("main_expanded.tex")

# Backup
backup = Path(f"main_expanded.pre_cirugia_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex")
shutil.copy2(latex_path, backup)
print(f"[OK] Backup created: {backup.name}")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

abstract_match = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', contenido, re.DOTALL)
abstract_actual = abstract_match.group(1).strip() if abstract_match else ""
print(f"[DATA] Abstract actual: {len(abstract_actual.split())} palabras")

# Configurar Cliente
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    print("[ERROR] ANTHROPIC_API_KEY no encontrada")
    exit(1)

cliente = Anthropic(api_key=api_key)

# Optimized Prompt (SCHEMA + STAR + Thinking Mode)
prompt_abstract = f"""
Actúa como un Senior Academic Editor experto en procesamiento de lenguaje natural y sistemas multi-RPAS.

1. Fase de Pensamiento (Thinking Budget: 2,048 tokens):
- Formulación: Analiza el Abstract actual y prioriza los hallazgos cuantitativos (ej. el gap del 78.8% en validación de campo).
- Modelado: Planifica una estructura de 4-6 frases densas que cubran el objetivo, método, resultados y contribución.
- Verificación: Realiza un conteo interno proyectado para asegurar que la salida final tenga entre 220 y 240 palabras.

2. Fase SCHEMA (Gobernanza):
- Conductor: El objetivo es cumplir con el límite de Elsevier de <250 palabras.
- Guardia de Seguridad: 0 menciones a la palabra 'drone'. Todas las fechas deben ser 2024. Mantén el valor exacto de n=33 estudios. Mantén la mención de 171 research gaps. Enfatiza el AgriSwarm-Bench.
- Unidades SI obligatorias.

3. Acción Agéntica:
Genera el código LaTeX listo para insertar (SOLO EL TEXTO, SIN \\begin{{abstract}} ni \\end{{abstract}}). 
Inyecta el tono académico Elsevier impecable.
Termina la respuesta con el conteo de palabras exacto entre [corchetes].

ABSTRACT ACTUAL:
{abstract_actual}
"""

print("\n[THINKING] Generando nuevo abstract con Claude 3.7 Thinking Mode...")

# Execution with Thinking Mode
try:
    response = cliente.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4000,
        thinking={
            "type": "enabled",
            "budget_tokens": 2048
        },
        messages=[{"role": "user", "content": prompt_abstract}]
    )
    
    nuevo_abstract_raw = response.content[0].text
    
    # Extraer conteo de palabras del final [XXX words]
    word_match = re.search(r'\[(\d+)\s*words?\]', nuevo_abstract_raw, re.IGNORECASE)
    if word_match:
        palabras_reportadas = int(word_match.group(1))
        # Limpiar el texto para que no incluya el bracket del conteo
        nuevo_abstract = re.sub(r'\s*\[\d+\s*words?\]', '', nuevo_abstract_raw, flags=re.IGNORECASE).strip()
    else:
        nuevo_abstract = nuevo_abstract_raw.strip()
        palabras_reportadas = len(nuevo_abstract.split())

    print(f"\n[DATA] Nuevo abstract (reportado): {palabras_reportadas} palabras")
    
    # Conteo real vía Python
    palabras_reales = len(nuevo_abstract.split())
    print(f"[DATA] Nuevo abstract (conteo real): {palabras_reales} palabras")

    if palabras_reales <= 250:
        print("   [OK] CSP CUMPLIDO (<250 palabras)")
    else:
        print(f"   [WARNING] ADVERTENCIA: Excede límite por {palabras_reales - 250} palabras")

    # Reemplazar en el contenido
    nuevo_abstract_latex = f"\\begin{{abstract}}\n{nuevo_abstract}\n\\end{{abstract}}"
    contenido_nuevo = re.sub(r'\\begin{abstract}.*?\\end{abstract}', nuevo_abstract_latex, contenido, flags=re.DOTALL)

    # Guardar
    with open(latex_path, 'w', encoding='utf-8') as f:
        f.write(contenido_nuevo)

    print("\n[OK] main_expanded.tex actualizado con éxito")
    
except Exception as e:
    print(f"[ERROR] ERROR en la llamada a Claude: {e}")
