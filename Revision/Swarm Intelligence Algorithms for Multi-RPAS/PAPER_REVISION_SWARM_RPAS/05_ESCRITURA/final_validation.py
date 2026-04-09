from csp_guardrail import CSPGuardrail
from pathlib import Path
import sys

# Forzar UTF-8
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("=" * 60)
print("VALIDACIÓN FINAL DEL MANUSCRITO")
print("=" * 60)

manuscrito_path = Path("main_expanded.tex")
if not manuscrito_path.exists():
    manuscrito_path = Path("05_ESCRITURA/main_expanded.tex")

if not manuscrito_path.exists():
    print(f"❌ ERROR: No se encuentra {manuscrito_path}")
    exit(1)

with open(manuscrito_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

guardrail = CSPGuardrail()
es_valido, violaciones = guardrail.validar(contenido)

if es_valido:
    print("✅ EL MANUSCRITO CUMPLE TODAS LAS RESTRICCIONES CSP.")
    print(f"   - n_total: {guardrail.config['n_total']}")
    print(f"   - n_primarios: {guardrail.config['n_primarios']}")
    print(f"   - Terminología: OK (No 'drones')")
    print(f"   - Unidades SI: OK")
else:
    print(f"⚠️ SE DETECTARON {len(violaciones)} VIOLACIONES:")
    for v in violaciones:
        print(f"   - {v}")

print("=" * 60)
