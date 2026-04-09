import re
from pathlib import Path
import sys

# Forzar UTF-8 para la salida estándar en Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("TAREA 3: PREPARACIÓN DE DISCUSIÓN PARA INTEGRACIÓN")
print("=" * 60)

# Leer la discusión traducida
discusion_path = Path("discusion_ingles.tex")
if not discusion_path.exists():
    discusion_path = Path("05_ESCRITURA/discusion_ingles.tex")

if not discusion_path.exists():
    print(f"❌ ERROR: No se encuentra {discusion_path.absolute()}")
    exit(1)

with open(discusion_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

print(f"📄 Original: {len(contenido)} caracteres")

# ============ CORRECCIÓN 1: n=23 → n=26 ============
contenido = re.sub(r'n=23', 'n=26', contenido)
contenido = re.sub(r'n_{primarios} = 23', 'n_{primarios} = 26', contenido)
contenido = re.sub(r'23 primary studies', '26 primary studies', contenido)
contenido = re.sub(r'23 studies', '26 studies', contenido)

print("✅ Corregido: n=23 → n=26")

# ============ CORRECCIÓN 2: Mapeo de placeholders a bibkeys ============
# Mapeo según la Tabla 2 del manuscrito
mapeo_citas = {
    # PSO (S01-S??)
    r'\\cite\{S1-S8\}': r'\\cite{chen2021,lin2022,liu2021cassa,liu2021disaster,liu2021,mathew2021,ntakolia2021,pan2022}',
    r'\\cite\{S9-S14\}': r'\\cite{phung2021,puente2022,sharma2022,yu2021,chu2022,fevgas2022}',
    r'\\cite\{S15-S20\}': r'\\cite{israr2022,ji2022,aitsaadi2022,selma2022,shafiq2022,ahmed2021}',
    r'\\cite\{S21-S23\}': r'\\cite{xu2022,wang2025,deng2023}',
    r'\\cite\{R1-R7\}': r'\\cite{puente2022,sharma2022,fevgas2022,israr2022,aitsaadi2022,yang2023,tang2022}',
    # Placeholders genéricos
    r'\\cite\{S1-S23\}': r'\\cite{chen2021,lin2022,liu2021cassa,liu2021disaster,liu2021,mathew2021,ntakolia2021,pan2022,phung2021,puente2022,sharma2022,yu2021,chu2022,fevgas2022,israr2022,ji2022,aitsaadi2022,selma2022,shafiq2022,ahmed2021,xu2022,wang2025,deng2023}',
}

for placeholder, bibkey in mapeo_citas.items():
    contenido = contenido.replace(placeholder.replace('\\\\', '\\'), bibkey.replace('\\\\', '\\'))

# Placeholder genérico "all"
if r'\cite{all}' in contenido:
    bib_all = r'\cite{chen2021,lin2022,liu2021cassa,liu2021disaster,liu2021,mathew2021,ntakolia2021,pan2022,phung2021,puente2022,sharma2022,yu2021,chu2022,fevgas2022,israr2022,ji2022,aitsaadi2022,selma2022,shafiq2022,ahmed2021,xu2022,wang2025,deng2023,xiao2025,li2023,rao2024,zhang2022loc,hu2025,zuo2025,yang2025}'
    contenido = contenido.replace(r'\cite{all}', bib_all)

print("✅ Corregido: Placeholders mapeados a bibkeys reales")

# ============ CORRECCIÓN 3: Convertir Markdown a LaTeX ============
# Títulos de sección
contenido = re.sub(r'^##\s+(.+)$', r'\\subsection{\1}', contenido, flags=re.MULTILINE)
contenido = re.sub(r'^###\s+(.+)$', r'\\subsubsection{\1}', contenido, flags=re.MULTILINE)

# Negritas
contenido = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', contenido)

# Cursivas (evitando conflictos con LaTeX)
# Notar que en LaTeX \textit es preferible
# El regex del usuario era re.sub(r'\*([^*]+)\*', r'\\textit{\1}', contenido)
# Sin embargo, * se usa en matemáticas, así que hay que ser cuidadoso.
# El contenido generado parece usar *...* para énfasis de texto.
contenido = re.sub(r'\*([^*]+)\*', r'\\textit{\1}', contenido)

# Eliminar líneas separadoras de Markdown
contenido = re.sub(r'^---$', '', contenido, flags=re.MULTILINE)

# Eliminar encabezados Markdown residuales o duplicados
contenido = re.sub(r'#+\s+', '', contenido)

print("✅ Corregido: Formato Markdown → LaTeX")

# ============ GUARDAR ============
output_path = discusion_path.parent / "discusion_preparada.tex"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

print(f"\n✅ Archivo preparado: {output_path}")
print(f"📏 Longitud final: {len(contenido)} caracteres")

# Mostrar preview de la primera sección
print("\n📋 PREVIEW (primeros 600 caracteres):")
print("-" * 60)
print(contenido[:600])
print("-" * 60)
