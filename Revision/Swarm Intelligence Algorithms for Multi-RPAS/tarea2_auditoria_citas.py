# tarea2_auditoria_citas.py
import re
import json
from pathlib import Path
import bibtexparser
from datetime import datetime

print("=" * 60)
print("TAREA 2: AUDITORÍA FORENSE DE CITAS")
print("=" * 60)

# Ruta absoluta del archivo LaTeX
latex_path = Path(r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\main_expanded.tex")

# Ruta absoluta del archivo .bib
bib_path = Path(r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\04_BIBLIOGRAFIA\references_clean.bib")

print(f"📁 LaTeX: {latex_path}")
print(f"📁 Bib: {bib_path}")
print()

# 1. Extraer todas las citas del manuscrito
print("📖 Extrayendo citas del manuscrito...")
with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

citas_raw = re.findall(r'\\cite\{([^}]+)\}', contenido)
citas_unicas = set()
for c in citas_raw:
    citas_unicas.update([x.strip() for x in c.split(',')])

print(f"   Citas únicas encontradas: {len(citas_unicas)}")

# 2. Cargar bibliografía
print("\n📚 Cargando archivo .bib...")
if not bib_path.exists():
    print(f"❌ Error: No se encuentra {bib_path}")
    print("Archivos disponibles en la carpeta:")
    for f in bib_path.parent.glob("*.bib"):
        print(f"   - {f.name}")
    exit()

with open(bib_path, 'r', encoding='utf-8') as f:
    biblioteca = bibtexparser.load(f)

entradas_bib = {entry['ID']: entry for entry in biblioteca.entries}
print(f"   Entradas en .bib: {len(entradas_bib)}")

# 3. Verificar cada cita
print("\n🔍 Verificando citas...")
citas_faltantes = []
citas_presentes = []

for cita in citas_unicas:
    if cita in entradas_bib:
        citas_presentes.append(cita)
    else:
        citas_faltantes.append(cita)

# 4. Resultados
print("\n" + "=" * 60)
print("RESULTADO DE LA AUDITORÍA")
print("=" * 60)
print(f"✅ Citas presentes: {len(citas_presentes)}")
print(f"❌ Citas faltantes: {len(citas_faltantes)}")

if citas_faltantes:
    print("\n⚠️ CITAS FALTANTES EN .bib:")
    for c in citas_faltantes[:15]:
        print(f"   - {c}")
else:
    print("\n🎉 AUDITORÍA APROBADA: Todas las citas tienen entrada en .bib")

# 5. Guardar log
log = {
    "timestamp": datetime.now().isoformat(),
    "total_citas_unicas": len(citas_unicas),
    "citas_presentes": len(citas_presentes),
    "citas_faltantes": len(citas_faltantes),
    "lista_faltantes": citas_faltantes
}

with open("auditoria_citas_final.json", 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2)

print(f"\n📁 Log guardado: auditoria_citas_final.json")