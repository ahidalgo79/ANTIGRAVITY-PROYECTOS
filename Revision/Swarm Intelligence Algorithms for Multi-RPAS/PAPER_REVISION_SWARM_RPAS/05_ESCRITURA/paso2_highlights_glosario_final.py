import os
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import sys
import json
from datetime import datetime
from anthropic import Anthropic

# Forzar UTF-8 para Windows (evita UnicodeEncodeError)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cargar variables de entorno (3 niveles arriba)
env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

print("=" * 60)
print("PASO 2: HIGHLIGHTS Y GLOSARIO - FINAL GENERATION")
print("=" * 60)

# Configurar Modelo (Forzando Claude para fiabilidad)
clp_key = os.getenv("ANTHROPIC_API_KEY")
if not clp_key:
    print("❌ ANTHROPIC_API_KEY no encontrada")
    sys.exit(1)
cliente = Anthropic(api_key=clp_key)
usar_claude = True

# Leer manuscrito final
latex_path = Path("main_expanded.tex")
if not latex_path.exists():
    latex_path = Path("05_ESCRITURA/main_expanded.tex")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Extraer secciones clave para contexto
abstract = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', contenido, re.DOTALL)
abstract_text = abstract.group(1) if abstract else ""

results = re.search(r'\\section{Results}(.*?)\\section{Discussion}', contenido, re.DOTALL)
if not results:
    results = re.search(r'\\section{Analysis and Findings}(.*?)\\section{Discussion}', contenido, re.DOTALL)
results_text = results.group(1) if results else ""

discussion = re.search(r'\\section{Discussion}(.*?)\\section{Conclusions}', contenido, re.DOTALL)
discussion_text = discussion.group(1) if discussion else ""

contexto = f"""
TITLE: Swarm Intelligence Algorithms for Multi-RPAS Path Planning in Precision Agriculture: A Systematic Review (2021--2024)
ABSTRACT:
{abstract_text[:1500]}
RESULTS:
{results_text[:1500]}
DISCUSSION:
{discussion_text[:1500]}
"""

# ============ GENERAR HIGHLIGHTS ============
prompt_highlights = f"""
Actúa como un Editor Académico Senior de Elsevier (Remote Sensing of Environment / Computers and Electronics in Agriculture).
Genera EXACTAMENTE 5 Highlights técnicos para el manuscrito basado en el contexto.

REGLAS CRÍTICAS DE ELSEVIER:
- Cada highlight: MÁXIMO 85 caracteres (contando espacios y puntuación).
- Oraciones completas e impactantes.
- Deben destacar hallazgos cuantitativos (n=33, n=26, PSO 38.5%, etc.).
- Sin preámbulos, solo los 5 bullets.

CONTEXTO:
{contexto}

RESPONDE SOLO CON LOS 5 BULLETS (SIN NÚMEROS, SOLO TEXTO).
"""

print("\n📝 Generando Highlights...")

try:
    if usar_claude:
        response = cliente.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt_highlights}]
        )
        highlights_raw = response.content[0].text
    else:
        response = model.generate_content(prompt_highlights)
        highlights_raw = response.text

    # Limpiar y filtrar
    highlights = [h.strip().lstrip('- ').lstrip('* ') for h in highlights_raw.split('\n') if h.strip()]
    
    validos = []
    print("\n🔍 Validación de longitud (Elsevier Limit: 85 chars):")
    for h in highlights:
        # Remover punto final si ayuda a la longitud
        if len(h) > 85 and h.endswith('.'):
            h = h[:-1]
            
        if len(h) <= 85:
            validos.append(h)
            print(f"  ✅ {len(h):2} ch: {h}")
        else:
            print(f"  ❌ {len(h):2} ch: {h} (REDUCIR!)")
            # Intento de reducción simple para el log
            validos.append(h[:82] + "...")

except Exception as e:
    print(f"❌ Error en generación: {e}")
    validos = ["Error en generación automática. Revisar manualmente."]

# Guardar highlights
output_dir = Path("05_ESCRITURA")
output_dir.mkdir(exist_ok=True)
with open(output_dir / "highlights.txt", 'w', encoding='utf-8') as f:
    for h in validos[:5]:
        f.write(h + "\n")

# ============ GENERAR GLOSARIO ============
print("\n📝 Generando Glosario de Abreviaturas...")
patron_abreviaturas = r'\b([A-Z]{2,})\b'
abreviaturas_raw = set(re.findall(patron_abreviaturas, contenido))

# White list más completa
tecnicas_white_list = {
    'PSO', 'ACO', 'UAV', 'RPAS', 'SI', 'PRISMA', 'CSP', 'DPO',
    'MMAT', 'DRS', 'FAISS', 'RAG', 'BVLOS', 'ICAO', 'NDVI',
    'SAR', 'GWO', 'SSA', 'DBO', 'NOA', 'DOA', 'ABC', 'CFD',
    'ROS', 'SITL', 'GPS', 'RTK', 'LiPo', 'EASA', 'AFAC', 'VRP', 'TAP', 'HIL'
}

glosario = sorted([a for a in abreviaturas_raw if a in tecnicas_white_list])

with open(output_dir / "glosario_abreviaturas.txt", 'w', encoding='utf-8') as f:
    for a in glosario:
        f.write(f"{a}\n")

print(f"✅ Glosario generado: {len(glosario)} abreviaturas ({', '.join(glosario[:10])}...)")

# ============ METADATA ============
metadata = {
    "timestamp": datetime.now().isoformat(),
    "n_total": 33,
    "n_primarios": 26,
    "highlights": validos[:5],
    "glosario": glosario
}
with open(output_dir / "paso2_metadata.json", 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2)

print("\n" + "=" * 60)
print("✅ PASO 2 COMPLETADO")
print(f"📁 Highlights: 05_ESCRITURA/highlights.txt")
print(f"📁 Glosario: 05_ESCRITURA/glosario_abreviaturas.txt")
