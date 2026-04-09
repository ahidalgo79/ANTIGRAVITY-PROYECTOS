import re
from pathlib import Path
import sys

# Forzar UTF-8 para la salida estándar en Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("TAREA 3: PREPARACIÓN DE DISCUSIÓN PARA INTEGRACIÓN (V2)")
print("=" * 60)

# Leer la discusión traducida
discusion_path = Path("discusion_ingles.tex")
if not discusion_path.exists():
    discusion_path = Path("05_ESCRITURA/discusion_ingles.tex")

with open(discusion_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

print(f"📄 Original: {len(contenido)} caracteres")

# ============ CORRECCIÓN 1: n=23 → n=26 ============
# Actualizamos el valor estadístico en el texto
contenido = contenido.replace('n_{primarios} = 23', 'n_{primarios} = 26')
contenido = contenido.replace('23 primary studies', '26 primary studies')
# Ajuste de porcentaje estadístico para el "HIL gap" (6 de 26)
contenido = contenido.replace('26.1%', '23.1%') # 6/26 = 23.07%

print("✅ Corregido: n=23 → n=26 y porcentajes asociados")

# ============ CORRECCIÓN 2: Mapeo de placeholders a bibkeys (Extendido y Corregido) ============
mapeo_citas_v2 = {
    # Rangos y grupos encontrados en discusion_ingles.tex
    r'\cite{S1-S8}': r'\cite{chen2021, lin2022, liu2021cassa, liu2021disaster, liu2021, mathew2021, ntakolia2021, pan2022}',
    r'\cite{S3, S7}': r'\cite{liu2021cassa, ntakolia2021}',
    r'\cite{S9-S15}': r'\cite{phung2021, yu2021, chu2022, ji2022, selma2022, shafiq2022, ahmed2021}',
    r'\cite{S4, S11, S16}': r'\cite{liu2021disaster, chu2022, xu2022}',
    r'\cite{S12, S14}': r'\cite{ji2022, shafiq2022}',
    r'\cite{S5, S8}': r'\cite{liu2021, pan2022}',
    r'\cite{R1-R4}': r'\cite{puente2022, sharma2022, fevgas2022, israr2022}',
    r'\cite{R1-R7}': r'\cite{puente2022, sharma2022, fevgas2022, israr2022, aitsaadi2022, yang2023, tang2022}',
    r'\cite{R2, R5}': r'\cite{sharma2022, aitsaadi2022}',
    r'\cite{S2, S6, S17}': r'\cite{lin2022, mathew2021, wang2025}',
    r'\cite{S3, S7, S9, S13, S18, S21, S22}': r'\cite{liu2021cassa, ntakolia2021, phung2021, chu2022, deng2023, xu2022, wang2025}',
    r'\cite{R3, R6}': r'\cite{fevgas2022, yang2023}',
    r'\cite{S9, S14, S15}': r'\cite{phung2021, shafiq2022, ahmed2021}',
    r'\cite{S20-S23, R7}': r'\cite{li2023, rao2024, zhang2022loc, hu2025, tang2022}',
    r'\cite{S22}': r'\cite{wang2025}',
    r'\cite{S18, S22}': r'\cite{deng2023, wang2025}',
}

for placeholder, bibkey in mapeo_citas_v2.items():
    contenido = contenido.replace(placeholder, bibkey)

print("✅ Corregido: Mapeo completo de placeholders (S/R) a bibkeys reales")

# ============ CORRECCIÓN 3: Limpieza de Formato ============
# Títulos de sección
contenido = re.sub(r'^##\s+.+Discussion Section.*$', '', contenido, flags=re.MULTILINE) # Eliminar header principal sobrante
contenido = re.sub(r'^###\s+Paragraph\s+\d+\s+—\s+(.+)$', r'\\subsection{\1}', contenido, flags=re.MULTILINE)

# Negritas y Cursivas
contenido = re.sub(r'\*\*([^*]+)\*\*', r'\\textbf{\1}', contenido)
contenido = re.sub(r'\*([^*]+)\*', r'\\textit{\1}', contenido)

# Separadores y limpieza final
contenido = re.sub(r'^---$', '', contenido, flags=re.MULTILINE)
contenido = re.sub(r'\n{3,}', '\n\n', contenido) # Normalizar saltos de línea

print("✅ Corregido: Formato Markdown → LaTeX (Limpieza V2)")

# ============ GUARDAR ============
output_path = discusion_path.parent / "discusion_preparada.tex"
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

print(f"\n✅ Archivo listo para insertar: {output_path}")
print(f"📏 Longitud final: {len(contenido)} caracteres")

# Preview
print("\n📋 PREVIEW (primeros 600 caracteres):")
print("-" * 60)
print(contenido[:600])
print("-" * 60)
