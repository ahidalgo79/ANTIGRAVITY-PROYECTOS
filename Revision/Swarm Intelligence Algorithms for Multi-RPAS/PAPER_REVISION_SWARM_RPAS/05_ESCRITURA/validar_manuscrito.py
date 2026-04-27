
from csp_guardrail import CSPGuardrail
from pathlib import Path

latex_path = Path("/home/andres/Documentos/ANTIGRAVITY-PROYECTOS/Revision/Swarm Intelligence Algorithms for Multi-RPAS/PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

guardrail = CSPGuardrail()
es_valido, violaciones = guardrail.validar(contenido)

print("=" * 60)
print("VALIDACIÓN CSP PARA main_expanded.tex")
print("=" * 60)
if es_valido:
    print("✅ MANUSCRITO CUMPLE TODAS LAS RESTRICCIONES.")
else:
    print(f"❌ SE ENCONTRARON {len(violaciones)} VIOLACIONES:")
    for v in violaciones:
        print(f"   - {v}")
print("=" * 60)
