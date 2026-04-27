#!/usr/bin/env python3
"""Revisor PRISMA/Elsevier para main_expanded.tex
Valida: consistencia numérica, British English, labels, abstract, change log, estructura."""
import re, sys, time
from pathlib import Path
from collections import defaultdict

# 🔒 Valores oficiales inmutables
OFFICIAL = {
    "total": 29, "primary": 22, "reviews": 7,
    "sim_only": 22, "hardware": 0,
    "mmat": "6/14/2", "drs": "4/14/4", "gaps": 115,
    "pso": 9, "aco": 2, "abc": 2
}
ALGOS = ["PSO", "ACO", "ABC", "SSA", "GWO", "DBO", "NOA", "DOA"]

def load_tex(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

def check_abstract(content: str) -> list:
    m = re.search(r'\\begin{abstract}(.*?)\\end{abstract}', content, re.DOTALL)
    if not m: return ["❌ Abstract no encontrado"]
    text = m.group(1)
    words = len(re.findall(r'\b\w+\b', text))
    issues = []
    if words > 250: issues.append(f"❌ Abstract excede 250 palabras (actual: {words})")
    if re.search(r'\\cite', text): issues.append("⚠️ Abstract contiene citas (no permitido en Elsevier)")
    return issues

def check_numbers(content: str) -> list:
    issues = []
    # Buscar patrones numéricos sospechosos
    for match in re.finditer(r'(n\s*=\s*\d+|(\d+(?:\.\d+)?)\s*%)', content):
        val = match.group(1).replace(" ", "")
        # Validar contra tabla oficial
        if "n=33" in val or "n=23" in val:
            issues.append(f"❌ Número inconsistente detectado: `{val}` (oficial: n=29 total / n=22 primarios)")
        if re.search(r'\b100\b.*?%', content) and "sim" not in match.group(0).lower():
            issues.append("⚠️ Revisar porcentaje 100% fuera de contexto de simulación/hardware")
    return issues

def check_british_english(content: str) -> list:
    us_forms = {
        "analyze": "analyse", "organize": "organise", "behavior": "behaviour",
        "modeling": "modelling", "optimization": "optimisation", "center": "centre",
        "standardize": "standardise", "recognize": "recognise"
    }
    issues = []
    for us, uk in us_forms.items():
        if re.search(rf'\b{us}\w*\b', content, re.IGNORECASE):
            issues.append(f"⚠️ US English detectado: `{us}` → usar `{uk}`")
    return issues

def check_labels(content: str) -> list:
    issues = []
    subsections = re.finditer(r'\\subsubsection\*?\{([^}]+)\}', content)
    for m in subsections:
        start = m.end()
        chunk = content[start:start+300]
        if not re.search(r'\\label\{', chunk):
            issues.append(f"⚠️ Subsección sin label: `{m.group(1)}`")
    return issues

def check_change_log(content: str) -> list:
    issues = []
    if not content.startswith(r"%% ["):
        issues.append("❌ Falta registro de cambios en encabezado (formato: `%% [YYYY-MM-DD] - ACTION: desc (line: X)`)")
    return issues

def run_checks(tex_path: str) -> str:
    print(f"🔍 Revisando {Path(tex_path).name} bajo reglas Elsevier/PRISMA...", flush=True)
    content = load_tex(tex_path)
    
    all_issues = []
    all_issues.extend(check_abstract(content))
    all_issues.extend(check_numbers(content))
    all_issues.extend(check_british_english(content))
    all_issues.extend(check_labels(content))
    all_issues.extend(check_change_log(content))
    
    # Resumen estructural
    sec_count = len(re.findall(r'\\section\{', content))
    sub_count = len(re.findall(r'\\subsection\{', content))
    
    report = f"""# 📄 Revisión PRISMA/Elsevier
## 📊 Métricas Estructurales
- Secciones: {sec_count} | Subsecciones: {sub_count}
- Algoritmos mencionados: {', '.join([a for a in ALGOS if re.search(rf'\\b{a}\\b', content)])}

## 🚦 Incidencias Detectadas
{chr(10).join(all_issues) if all_issues else '✅ Sin incidencias críticas. Listo para compilación.'}

## 📋 Checklist de Consistencia Oficial
- [ ] n=29 (total) declarado explícitamente donde corresponda
- [ ] n=22 (primarios) usado solo para análisis cuantitativo
- [ ] 22 simulación + 7 revisiones = 29 (verificado)
- [ ] Validación hardware: 0/22 (0%)
- [ ] AgriSwarm-Bench citado como contribución principal
- [ ] Guiones largos: `---` usados consistentemente
- [ ] Números 1-9 en letras (five algorithms, two authors...)

## 💡 Próximos Pasos
1. Corregir `❌` antes de compilar.
2. Revisar `⚠️` manualmente (contexto dependiente).
3. Ejecutar `xelatex main_expanded.tex` → `bibtex main_expanded` → `xelatex` (x2)
"""
    return report

if __name__ == "__main__":
    tex = sys.argv[1] if len(sys.argv)>1 else "main_expanded.tex"
    report = run_checks(tex)
    print("\n" + "="*60 + "\n" + report)
    out = Path("reports") / f"prisma_check_{int(time.time())}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(report, encoding="utf-8")
    print(f"💾 Guardado: {out}")
