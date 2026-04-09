# nodo3_seccion63_condensar.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("=" * 60)
print("NODO 3: CONDENSACIÓN DE SECCIÓN 6.3")
print("=" * 60)

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

latex_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")

# Backup
import shutil
from datetime import datetime
backup = Path(f"PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.backup_seccion63_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex")
shutil.copy2(latex_path, backup)
print(f"✅ Backup: {backup.name}")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Buscar la sección 6.3
seccion63_match = re.search(r'\\subsection\{Metric Inconsistency.*?(?=\\subsection\{|\Z)', contenido, re.DOTALL)
if not seccion63_match:
    print("❌ No se encontró la sección 6.3")
    exit()

seccion63_original = seccion63_match.group(0)
palabras_original = len(seccion63_original.split())
print(f"📊 Sección 6.3 original: {palabras_original} palabras")

model = genai.GenerativeModel('gemini-2.5-flash')

prompt_condensacion = f"""
Actúa como un Editor Senior de Elsevier.

Condensa la siguiente sección de métricas, manteniendo los datos clave.

REGLAS:
- Mantén: n=33, 26 primarios, porcentajes: 42.4% tiempo, 39.4% energía, 21.2% convergencia
- Mantén: AgriSwarm-Bench como solución
- Reduce texto redundante sin perder rigor técnico
- Prohibido: "drone" (usa "UAV" o "RPAS")
- Objetivo: reducir ~40-50% del texto

SECCIÓN ORIGINAL:
{seccion63_original}

RESPONDE SOLO CON LA SECCIÓN CONDENSADA EN FORMATO LATEX (con \\subsection y todo).
Al final, indica entre [corchetes] el número de palabras.
"""

print("\n🔄 Condensando sección...")
response = model.generate_content(prompt_condensacion)
resultado = response.text

# Extraer conteo
word_match = re.search(r'\[(\d+)\s*words?\]', resultado, re.IGNORECASE)
if word_match:
    palabras_nuevas = int(word_match.group(1))
    nueva_seccion = re.sub(r'\s*\[\d+\s*words?\]', '', resultado, flags=re.IGNORECASE)
else:
    palabras_nuevas = len(resultado.split())
    nueva_seccion = resultado

print(f"\n📊 Nueva sección: {palabras_nuevas} palabras")
reduccion = palabras_original - palabras_nuevas
porcentaje = (reduccion / palabras_original) * 100
print(f"   Reducción: {reduccion} palabras ({porcentaje:.1f}%)")

# Reemplazar en el manuscrito
contenido = contenido.replace(seccion63_original, nueva_seccion)

with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

print("\n✅ Sección 6.3 condensada")