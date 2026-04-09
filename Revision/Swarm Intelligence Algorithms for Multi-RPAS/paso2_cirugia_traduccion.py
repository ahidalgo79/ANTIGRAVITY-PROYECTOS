# paso2_cirugia_traduccion.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

print("=" * 60)
print("PASO 2: CIRUGÍA LÓGICA Y TRADUCCIÓN")
print("=" * 60)

# Buscar la API key de Anthropic
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

if not anthropic_key:
    print("⚠️ ANTHROPIC_API_KEY no encontrada. Usando Gemini para traducción...")
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-2.5-flash')
    usar_claude = False
else:
    cliente = Anthropic(api_key=anthropic_key)
    usar_claude = True

latex_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Buscar párrafo en español
spanish_match = re.search(r'Single-reviewer title/abstract screening:.*?[\n]', contenido)
if spanish_match:
    texto_espanol = spanish_match.group(0)
    print(f"📝 Texto en español encontrado: {texto_espanol[:100]}...")

    prompt_traduccion = f"""
Traduce el siguiente texto al inglés académico formal:

"{texto_espanol}"

Mantén el formato \\textbf{{...}} y el tono académico.
RESPONDE SOLO CON EL TEXTO TRADUCIDO.
"""

    if usar_claude:
        response = cliente.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt_traduccion}]
        )
        texto_ingles = response.content[0].text
    else:
        response = model.generate_content(prompt_traduccion)
        texto_ingles = response.text

    contenido = contenido.replace(texto_espanol, texto_ingles)
    print("✅ Párrafo traducido")

# Verificar años de xiao2025 y hu2025
bib_path = Path("PAPER_REVISION_SWARM_RPAS/04_BIBLIOGRAFIA/references_clean.bib")
if bib_path.exists():
    with open(bib_path, 'r', encoding='utf-8') as f:
        bib = f.read()
    
    for cita in ["xiao2025", "hu2025"]:
        if cita in bib:
            # Buscar el año real
            year_match = re.search(rf'@article\{{{cita},.*?year\s*=\s*{{(\d{{4}})}}', bib, re.DOTALL)
            if year_match:
                year = year_match.group(1)
                if year == "2025":
                    print(f"⚠️ {cita} es de {year} - contradice criterio 2021-2024")
                    print("   Sugerencia: justificar como literatura de frontera o excluir")
                else:
                    print(f"✅ {cita} es de {year} - correcto")

# Guardar cambios
with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

print("\n✅ Cirugía lógica completada")