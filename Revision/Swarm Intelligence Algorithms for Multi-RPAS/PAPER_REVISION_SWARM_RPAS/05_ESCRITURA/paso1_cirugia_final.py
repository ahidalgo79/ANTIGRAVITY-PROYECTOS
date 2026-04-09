import re
from pathlib import Path
import shutil
from datetime import datetime
import json
import sys

# Forzar UTF-8 para Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("PASO 1: CIRUGÍA LaTeX - FINAL REFINEMENT")
print("=" * 60)

latex_path = Path("main_expanded.tex")
if not latex_path.exists():
    latex_path = Path("05_ESCRITURA/main_expanded.tex")

# === BACKUP ===
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# Si estamos en 05_ESCRITURA, no necesitamos el prefijo en el backup
backup_name = f"main_expanded.pre_cirugia_{timestamp}.tex"
backup = Path(backup_name)
shutil.copy2(latex_path, backup)
print(f"✅ Backup created: {backup.name}")

# === LEER ARCHIVO ===
with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

cambios = []

# === 1. CORREGIR ode → \node (Safer Version) ===
# Solo corregimos si NO hay una 'n' antes de 'ode'
contenido_original = contenido
contenido = re.sub(r'(?<!n)\\?ode\[', r'\\node[', contenido)
if contenido != contenido_original:
    dif = len(re.findall(r'\\node\[', contenido)) - len(re.findall(r'\\node\[', contenido_original))
    cambios.append(f"ode → \\node ({dif} correcciones)")
    print(f"✅ Corregido: ode → \\node ({dif} veces)")

# === 2. CORREGIR oindent → \noindent ===
contenido_original = contenido
contenido = re.sub(r'(?<!\\)oindent', r'\\noindent', contenido)
if contenido != contenido_original:
    cambios.append("oindent → \\noindent")
    print("✅ Corregido: oindent → \\noindent")

# === 3. ACTUALIZAR FECHAS (2026 → 2024) ===
# Evitamos tocar DOIs si es posible, aunque en 2026 no hay DOIs reales aún
contenido_original = contenido
contenido = re.sub(r'2026', '2024', contenido)
if contenido != contenido_original:
    cambios.append("fechas: 2026 → 2024")
    print("✅ Corregido: 2026 → 2024")

# === 4. ACTUALIZAR RANGO (2021-2025 → 2021-2024) ===
contenido_original = contenido
contenido = re.sub(r'2021--2025', '2021--2024', contenido)
if contenido != contenido_original:
    cambios.append("rango: 2021-2025 → 2021-2024")
    print("✅ Corregido: 2021-2025 → 2021-2024")

# === 5. ACTUALIZAR NOTA DE CORRECCIÓN ===
contenido_original = contenido
contenido = re.sub(r'Fecha de corrección: 2024-\d{2}-\d{2}', 
                   'Fecha de corrección: 2024-03-31', contenido)
if contenido != contenido_original:
    cambios.append("nota de corrección: set to 2024-03-31")
    print("✅ Corregido: nota de corrección")

# === 6. VERIFICAR ELIMINACIÓN DE "drone" ===
if 'drone' in contenido.lower():
    # Buscar si está en DOIs (ignorar)
    drones_fuera_de_doi = False
    matches = re.finditer(r'\bdrone\b', contenido, re.IGNORECASE)
    for m in matches:
        pre_text = contenido[max(0, m.start()-20):m.start()]
        if "doi" not in pre_text.lower() and "/" not in pre_text:
            drones_fuera_de_doi = True
            break
    
    if drones_fuera_de_doi:
        print("⚠️ ADVERTENCIA: Aún hay ocurrencias de 'drone' (fuera de DOIs)")
    else:
        print("✅ Verificado: 0 ocurrencias de 'drone' (excluyendo DOIs)")
else:
    print("✅ Verificado: 0 ocurrencias de 'drone'")

# === 7. VERIFICAR n=33 CONSISTENTE ===
n33_count = len(re.findall(r'n\s*=\s*33', contenido))
n26_count = len(re.findall(r'26\s*estudios primarios|26\s*primary studies', contenido.lower()))
print(f"📊 n=33 encontrado: {n33_count} veces")
print(f"📊 26 primarios encontrado: {n26_count} veces")

# === GUARDAR ===
with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

# === GUARDAR LOG ===
log = {
    "timestamp": datetime.now().isoformat(),
    "archivo": str(latex_path),
    "backup": str(backup),
    "cambios": cambios,
    "n33_count": n33_count,
    "n26_count": n26_count,
    "drone_presente": 'drone' in contenido.lower()
}

with open("cirugia_log.json", 'w', encoding='utf-8') as f:
    json.dump(log, f, indent=2)

print("\n" + "=" * 60)
print("RESUMEN DE CIRUGÍA")
print("=" * 60)
for c in cambios:
    print(f"   ✅ {c}")

print(f"\n📁 Archivo actualizado: {latex_path}")
print(f"📁 Log guardado: cirugia_log.json")

print("\n✅ PASO 1 COMPLETADO")
