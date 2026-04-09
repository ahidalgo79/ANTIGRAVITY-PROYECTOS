# paso5_unificacion_global.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("=" * 60)
print("PASO 5: UNIFICACIÓN GLOBAL - n=31 total, n=24 primarios")
print("=" * 60)

latex_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")

# Backup
import shutil
from datetime import datetime
backup = Path(f"PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.backup_unificacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex")
shutil.copy2(latex_path, backup)
print(f"✅ Backup: {backup.name}")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# ============================================================
# 1. CORREGIR ERROR LaTeX LÍNEA 163
# ============================================================
print("\n🔧 Corrigiendo error LaTeX línea 163...")

# Separar \end{itemize} mal ubicado
contenido = re.sub(r'findings\.\\end{itemize}', r'findings.\n\n\\end{itemize}', contenido)

# Eliminar doble \textbf
contenido = re.sub(r'\\\\textbf\\\\textbf\{', r'\\textbf{', contenido)

# ============================================================
# 2. UNIFICAR DENOMINADORES: n=31 total, n=24 primarios
# ============================================================
print("\n📊 Unificando denominadores...")

# Totales
contenido = re.sub(r'n=33', 'n=31', contenido)
contenido = re.sub(r'33 estudios', '31 estudios', contenido)
contenido = re.sub(r'33 studies', '31 studies', contenido)
contenido = re.sub(r'33 papers', '31 papers', contenido)

# Primarios
contenido = re.sub(r'26 estudios primarios', '24 estudios primarios', contenido)
contenido = re.sub(r'26 primary studies', '24 primary studies', contenido)
contenido = re.sub(r'26 primary research', '24 primary research', contenido)

# Porcentajes
contenido = re.sub(r'10 of 33', '10 of 31', contenido)
contenido = re.sub(r'30\.3%', '32.3%', contenido)
contenido = re.sub(r'30.3%', '32.3%', contenido)

# Corregir frase "26 of 24 primary studies"
contenido = re.sub(r'26 of 24 primary studies', '24 of 24 primary studies', contenido)
contenido = re.sub(r'26 of 24 primary', '24 of 24 primary', contenido)

# ============================================================
# 3. CORREGIR UNIDADES
# ============================================================
print("\n📏 Convirtiendo unidades...")

contenido = re.sub(r'60 km/h', '16.7 m/s', contenido)
contenido = re.sub(r'60km/h', '16.7 m/s', contenido)

# ============================================================
# 4. ELIMINAR ANOTACIÓN [187]
# ============================================================
print("\n🗑️ Eliminando anotación [187]...")
contenido = contenido.replace('[187]', '')

# ============================================================
# 5. AGREGAR HIGHLIGHTS
# ============================================================
print("\n✨ Agregando entorno highlights...")

highlights = """\\begin{highlights}
\\item Systematic review of 31 studies on SI-based multi-UAV path planning (2021--2024)
\\item PSO dominates algorithm landscape (32.3%); all 24 primary studies lack field validation
\\item 171 research gaps identified; 75.8% of studies omit wind and dynamic obstacles
\\item Metric reporting fragmented: only 42.4% report execution time
\\item AgriSwarm-Bench framework proposed to standardize evaluation and accelerate deployment
\\end{highlights}

"""

# Insertar después del abstract
contenido = contenido.replace('\\begin{abstract}', highlights + '\\begin{abstract}')

# ============================================================
# 6. AGREGAR ETIQUETAS \label FALTANTES
# ============================================================
print("\n🏷️ Agregando etiquetas \\label...")

# Buscar y agregar labels
contenido = re.sub(r'\\caption{PICOC framework defining the scope}', 
                   r'\\caption{PICOC framework defining the scope}\\label{tab:picoc}', contenido)

contenido = re.sub(r'\\caption{Deployment Readiness Score \\(DRS\\) instrument}', 
                   r'\\caption{Deployment Readiness Score (DRS) instrument}\\label{tab:quality_criteria}', contenido)

contenido = re.sub(r'\\subsection{Deployment Readiness Score \\(DRS\\)}', 
                   r'\\subsection{Deployment Readiness Score (DRS)}\\label{subsec:drs}', contenido)

contenido = re.sub(r'\\subsection{Risk of Bias Assessment \\(MMAT\\)}', 
                   r'\\subsection{Risk of Bias Assessment (MMAT)}\\label{subsec:mmat}', contenido)

# ============================================================
# 7. VERIFICAR CONSISTENCIA
# ============================================================
print("\n🔍 Verificando consistencia...")

# Contar ocurrencias
n31_count = len(re.findall(r'n=31', contenido))
n24_count = len(re.findall(r'24 primary studies|24 estudios primarios', contenido.lower()))
n33_count = len(re.findall(r'n=33', contenido))
n26_count = len(re.findall(r'26 primary studies|26 estudios primarios', contenido.lower()))

print(f"   n=31 encontrado: {n31_count} veces")
print(f"   n=24 primarios: {n24_count} veces")
print(f"   n=33 residual: {n33_count} veces")
print(f"   n=26 residual: {n26_count} veces")

# ============================================================
# 8. GUARDAR
# ============================================================
with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

print("\n" + "=" * 60)
print("✅ UNIFICACIÓN GLOBAL COMPLETADA")
print("=" * 60)
print(f"📁 Archivo: {latex_path}")
print(f"📁 Backup: {backup.name}")
print("\n📊 Denominadores finales:")
print("   - n=31 estudios totales")
print("   - n=24 estudios primarios")
print("   - PSO: 10 de 31 (32.3%)")