import subprocess
import re
from pathlib import Path
import shutil
from datetime import datetime
import json
import sys

# Forzar UTF-8 para Windows (evita UnicodeEncodeError)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("PASO 3: COMPILACIÓN Y VALIDACIÓN CSP FINAL")
print("=" * 60)

latex_path = Path("main_expanded.tex")
if not latex_path.exists():
    latex_path = Path("05_ESCRITURA/main_expanded.tex")

# === BACKUP FINAL ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = Path(f"main_expanded.pre_compilacion_{timestamp}.tex")
shutil.copy2(latex_path, backup)
print(f"✅ Backup pre-compilación: {backup.name}")

# === 1. LEER ARCHIVO ===
with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# === 2. VERIFICAR enumitem ===
if "\\usepackage{enumitem}" not in contenido:
    contenido = re.sub(r'(\\documentclass.*?\n)', r'\1\\usepackage{enumitem}\n', contenido)
    print("✅ Paquete enumitem añadido al preámbulo")

# === 3. INYECTAR GLOSARIO ===
glosario_path = Path("glosario_abreviaturas.txt")
if not glosario_path.exists():
     glosario_path = Path("05_ESCRITURA/glosario_abreviaturas.txt")

with open(glosario_path, 'r', encoding='utf-8') as f:
    abreviaturas = [line.strip() for line in f if line.strip()]

# Crear tabla de abreviaturas en LaTeX
glosario_latex = "\n\\section*{List of Abbreviations}\n"
glosario_latex += "\\begin{description}[leftmargin=3.5cm, style=nextline]\n"

# Definiciones completas
definiciones = {
    "ABC": "Artificial Bee Colony",
    "ACO": "Ant Colony Optimization",
    "BVLOS": "Beyond Visual Line of Sight",
    "CFD": "Computational Fluid Dynamics",
    "CSP": "Constraint Satisfaction Problem",
    "DBO": "Dung Beetle Optimizer",
    "DOA": "Dandelion Optimizer Algorithm",
    "DPO": "Direct Preference Optimization",
    "DRS": "Deployment Readiness Score",
    "EASA": "European Union Aviation Safety Agency",
    "FAISS": "Facebook AI Similarity Search",
    "GPS": "Global Positioning System",
    "GWO": "Grey Wolf Optimizer",
    "HIL": "Hardware-in-the-Loop",
    "ICAO": "International Civil Aviation Organization",
    "MMAT": "Mixed Methods Appraisal Tool",
    "NDVI": "Normalized Difference Vegetation Index",
    "NOA": "Nutcracker Optimization Algorithm",
    "PRISMA": "Preferred Reporting Items for Systematic Reviews and Meta-Analyses",
    "PSO": "Particle Swarm Optimization",
    "RAG": "Retrieval-Augmented Generation",
    "ROS": "Robot Operating System",
    "RPAS": "Remotely Piloted Aircraft Systems",
    "RTK": "Real-Time Kinematic",
    "SAR": "Search and Rescue",
    "SI": "Swarm Intelligence",
    "SITL": "Software-in-the-Loop",
    "SSA": "Salp Swarm Algorithm",
    "TAP": "Task Allocation Problem",
    "UAV": "Unmanned Aerial Vehicle",
    "VRP": "Vehicle Routing Problem"
}

for abr in abreviaturas:
    if abr in definiciones:
        glosario_latex += f"    \\item[{abr}] {definiciones[abr]}\n"
    else:
        glosario_latex += f"    \\item[{abr}] \\textit{{To be defined}}\n"

glosario_latex += "\\end{description}\n"

# Insertar glosario después de frontmatter
if "\\end{frontmatter}" in contenido:
    if "\\section*{List of Abbreviations}" not in contenido:
        end_frontmatter = contenido.find("\\end{frontmatter}")
        insert_pos = end_frontmatter + len("\\end{frontmatter}")
        contenido = contenido[:insert_pos] + "\n\n" + glosario_latex + "\n" + contenido[insert_pos:]
        print("✅ Glosario inyectado después de frontmatter")
    else:
        print("⚠️ Glosario ya presente. Omitiendo inyección.")

# === 4. GUARDAR ARCHIVO ACTUALIZADO ===
with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(contenido)
print(f"✅ Archivo actualizado: {latex_path}")

# === 5. COMPILAR CON XELATEX ===
print("\n📄 Compilando con XeLaTeX...")
try:
    # Primera vuelta
    subprocess.run(["xelatex", "-interaction=nonstopmode", latex_path.name], cwd=latex_path.parent, capture_output=True, check=True)
    print("✅ Primera vuelta: OK")
    # Segunda vuelta (referencias/glosario)
    subprocess.run(["xelatex", "-interaction=nonstopmode", latex_path.name], cwd=latex_path.parent, capture_output=True, check=True)
    print("✅ Segunda vuelta: OK")
except subprocess.CalledProcessError as e:
    print(f"❌ Error en compilación: {e}")
    # Mostrar final del log
    log_path = latex_path.with_suffix('.log')
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            print("--- LOG PREVIEW ---")
            print(f.read()[-1000:])

# === 6. VALIDACIÓN CSP FINAL ===
print("\n🔍 VALIDACIÓN CSP FINAL...")
from csp_guardrail import CSPGuardrail
guardrail = CSPGuardrail()
es_valido, violaciones = guardrail.validar(contenido)

print("\n" + "=" * 60)
print("RESULTADO DE VALIDACIÓN CSP")
print("=" * 60)
if es_valido:
    print("✅ MANUSCRITO CUMPLE TODAS LAS RESTRICCIONES.")
else:
    for v in violaciones:
        print(f"   - {v}")

# === 7. LOG FINAL ===
log_data = {
    "timestamp": datetime.now().isoformat(),
    "highlights": [],
    "csp_valid": es_valido,
    "violaciones": violaciones,
    "pdf_size": 0
}

pdf_path = latex_path.with_suffix('.pdf')
if pdf_path.exists():
    log_data["pdf_size"] = pdf_path.stat().st_size
    print(f"✅ PDF Generado: {pdf_path.name} ({log_data['pdf_size']} bytes)")

with open("paso3_log_final.json", 'w', encoding='utf-8') as f:
    json.dump(log_data, f, indent=2)

print("\n✅ PASO 3 COMPLETADO")
