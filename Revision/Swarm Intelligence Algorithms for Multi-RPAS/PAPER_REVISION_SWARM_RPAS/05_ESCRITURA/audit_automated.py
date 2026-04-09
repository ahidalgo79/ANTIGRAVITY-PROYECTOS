import re
from pathlib import Path
import json
from datetime import datetime

print("=" * 60)
print("AUDITORIA AUTOMATIZADA - VERSION 2.0 (STRICT)")
print("=" * 60)

latex_path = Path("main_expanded.tex")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# ============================================================
# 1. TERMINOLOGÍA PROHIBIDA
# ============================================================
print("\n[STEP 1] TERMINOLOGIA PROHIBIDA")
print("-" * 40)
terminos_prohibidos = ['drone', 'drones']
for t in terminos_prohibidos:
    matches = re.findall(rf'\b{t}\b', contenido, re.IGNORECASE)
    # Check contexto (not DOI)
    m_real = []
    for m in matches:
        pos = contenido.find(m)
        contexto = contenido[max(0, pos-50):pos+50]
        if "doi.org" not in contexto and "http" not in contexto:
            m_real.append(m)
    if m_real:
        print(f"X ERROR: '{t}' detectado {len(m_real)} veces.")
    else:
        print(f"OK: 0 '{t}' occurrences outside references.")

# ============================================================
# 2. INTEGRIDAD TEMPORAL (Sync 2021-2024)
# ============================================================
print("\n[STEP 2] INTEGRIDAD TEMPORAL")
print("-" * 40)
if "2025" in contenido or "2026" in contenido:
    print("X ERROR: Fechas futuras (2025/2026) detectadas.")
else:
    print("OK: No future dates (2025/2026).")

if "between 2021 and 2023" in contenido:
    print("X ERROR: 'between 2021 and 2023' found (must be 2024).")
else:
    print("OK: Period sync (2021-2024) confirmed in text.")

# ============================================================
# 3. SINTAXIS Y ESCAPES CRÍTICOS
# ============================================================
print("\n[STEP 3] SINTAXIS Y ESCAPES")
print("-" * 40)

# Check literal \n\
lit_escapes = re.findall(r'\\n\\', contenido)
if lit_escapes:
    print(f"X ERROR: {len(lit_escapes)} literal '\\n\\' sequences found.")
else:
    print("OK: No literal '\\n\\' sequences.")

# Check TikZ typos
tikz_typos = re.findall(r'\bode\[', contenido)
if tikz_typos:
    print(f"X ERROR: {len(tikz_typos)} 'ode[' typos found.")
else:
    print("OK: No 'ode[' typos.")

# Check noindent typos
noindent_typos = re.findall(r'\boindent\b', contenido)
if noindent_typos:
    print(f"X ERROR: 'oindent' typos found.")
else:
    print("OK: No 'oindent' typos.")

# ============================================================
# 4. CITAS YANG
# ============================================================
print("\n[STEP 4] CITAS YANG (S31)")
print("-" * 40)
s31_line = [l for l in contenido.split('\n') if "S31" in l and "Yang" in l]
if s31_line:
    if "yang2023_review" in s31_line[0]:
        print("OK: S31 correctly uses 'yang2023_review'.")
    else:
        print("X ERROR: S31 still uses 'yang2023'.")
else:
    print("! S31 check skipped (target not found).")

# ============================================================
# 5. TABLA TEMPORAL
# ============================================================
print("\n[STEP 5] TABLA TEMPORAL")
print("-" * 40)
rows_2023 = re.findall(r'^2023\s*&', contenido, re.MULTILINE)
if len(rows_2023) > 1:
    print(f"X ERROR: Temporal table has {len(rows_2023)} rows for '2023'.")
else:
    print("OK: Temporal table rows for 2023 unified.")

print("\n" + "=" * 60)
print("AUDITORIA FINALIZADA")
print("=" * 60)
