# nodo1_abstract_gemini.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("=" * 60)
print("NODO 1: CIRUGÍA DE ABSTRACT - GEMINI")
print("=" * 60)

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

latex_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")

# Backup
import shutil
from datetime import datetime
backup = Path(f"PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex")
shutil.copy2(latex_path, backup)
print(f"✅ Backup: {backup.name}")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

abstract_match = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', contenido, re.DOTALL)
abstract_actual = abstract_match.group(1) if abstract_match else ""
print(f"📊 Abstract actual: {len(abstract_actual.split())} palabras")

model = genai.GenerativeModel('gemini-1.5-flash')

prompt_abstract = f"""
Actúa como Editor Senior de Elsevier.

Condensa el siguiente abstract a menos de 250 palabras.

REGLAS:
- Mantén: n=33, 171 research gaps, 100% validation gap, AgriSwarm-Bench
- Prohibido: "drone" (usa "UAV" o "RPAS")
- Fechas: 2021-2024
- Estructura: Background, Objective, Methods, Results, Conclusions

ABSTRACT ACTUAL:
{abstract_actual}

RESPONDE SOLO CON EL NUEVO ABSTRACT EN TEXTO PLANO (sin formato LaTeX).
Al final, indica el número de palabras entre [corchetes].
"""

print("\n🔄 Generando nuevo abstract...")
response = model.generate_content(prompt_abstract)
resultado = response.text

word_match = re.search(r'\[(\d+)\s*words?\]', resultado, re.IGNORECASE)
if word_match:
    palabras = int(word_match.group(1))
    nuevo_abstract = re.sub(r'\s*\[\d+\s*words?\]', '', resultado, flags=re.IGNORECASE)
else:
    palabras = len(resultado.split())
    nuevo_abstract = resultado

print(f"\n📊 Nuevo abstract: {palabras} palabras")

if palabras <= 250:
    print("   ✅ Límite cumplido (<250 palabras)")
else:
    print(f"   ⚠️ Excede: {palabras - 250} palabras")

# Reemplazar
nuevo_abstract_latex = f"\\begin{{abstract}}\n{nuevo_abstract.strip()}\n\\end{{abstract}}"
contenido = re.sub(r'\\begin{abstract}.*?\\end{abstract}', nuevo_abstract_latex, contenido, flags=re.DOTALL)

with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

print("\n✅ Abstract actualizado")