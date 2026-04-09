# paso4_purga_integridad.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("=" * 60)
print("PASO 4: PURGA DE INTEGRIDAD - n=33 → n=31")
print("=" * 60)

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

latex_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")
bib_path = Path("PAPER_REVISION_SWARM_RPAS/04_BIBLIOGRAFIA/references_clean.bib")

# Backup
import shutil
from datetime import datetime
backup = Path(f"PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.backup_purga_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex")
shutil.copy2(latex_path, backup)
print(f"✅ Backup: {backup.name}")

# Leer contenido
with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# ============================================================
# 1. ELIMINAR CITAS xiao2025 y hu2025 del manuscrito
# ============================================================
print("\n📖 Eliminando citas de 2025...")

# Eliminar citas individuales
contenido = re.sub(r'\\cite\{[^}]*xiao2025[^}]*\}', '', contenido)
contenido = re.sub(r'\\cite\{[^}]*hu2025[^}]*\}', '', contenido)

# Limpiar citas vacías que quedaron
contenido = re.sub(r'\\cite\{\}', '', contenido)

# ============================================================
# 2. ACTUALIZAR n=33 → n=31 y 26 primarios → 24 primarios
# ============================================================
print("\n📊 Actualizando denominadores...")

contenido = re.sub(r'n=33', 'n=31', contenido)
contenido = re.sub(r'33 estudios', '31 estudios', contenido)
contenido = re.sub(r'33 papers', '31 papers', contenido)
contenido = re.sub(r'33 included studies', '31 included studies', contenido)

contenido = re.sub(r'26 estudios primarios', '24 estudios primarios', contenido)
contenido = re.sub(r'26 primary studies', '24 primary studies', contenido)
contenido = re.sub(r'26 primary research', '24 primary research', contenido)

# Actualizar porcentajes (10 de 31 = 32.3%)
contenido = re.sub(r'30\.3%', '32.3%', contenido)
contenido = re.sub(r'30.3%', '32.3%', contenido)

# Actualizar 10 de 33 → 10 de 31
contenido = re.sub(r'10 of 33', '10 of 31', contenido)

# ============================================================
# 3. ELIMINAR REFERENCIAS DEL ARCHIVO .bib
# ============================================================
print("\n📚 Eliminando referencias del .bib...")

if bib_path.exists():
    with open(bib_path, 'r', encoding='utf-8') as f:
        bib = f.read()
    
    # Eliminar entradas completas de xiao2025 y hu2025
    bib = re.sub(r'@article\{xiao2025,.*?\n\}', '', bib, flags=re.DOTALL)
    bib = re.sub(r'@article\{hu2025,.*?\n\}', '', bib, flags=re.DOTALL)
    
    with open(bib_path, 'w', encoding='utf-8') as f:
        f.write(bib)
    print("✅ Referencias eliminadas del .bib")

# ============================================================
# 4. VERIFICAR QUE NO QUEDAN REFERENCIAS A 2025
# ============================================================
print("\n🔍 Verificando ausencia de 2025...")

if '2025' in contenido:
    print("⚠️ ADVERTENCIA: Aún hay referencias a 2025")
    # Mostrar contexto
    matches = re.findall(r'.{0,50}2025.{0,50}', contenido)
    for m in matches[:3]:
        print(f"   ...{m}...")
else:
    print("✅ 0 referencias a 2025 en el manuscrito")

# ============================================================
# 5. VERIFICAR ABSTRACT PALABRAS
# ============================================================
abstract_match = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', contenido, re.DOTALL)
if abstract_match:
    abstract = abstract_match.group(1)
    palabras = len(abstract.split())
    print(f"\n📊 Abstract: {palabras} palabras {'✅' if palabras < 250 else '❌'}")

# ============================================================
# GUARDAR
# ============================================================
with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

print("\n" + "=" * 60)
print("✅ PURGA DE INTEGRIDAD COMPLETADA")
print("=" * 60)
print(f"📁 Archivo: {latex_path}")
print(f"📁 Backup: {backup.name}")
print("\n📊 Nuevos denominadores:")
print("   - n=31 estudios totales")
print("   - 24 estudios primarios")
print("   - PSO: 10 de 31 (32.3%)")