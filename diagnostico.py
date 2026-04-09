#!/usr/bin/env python3
"""Diagnóstico del entorno Antigravity + recomendaciones inteligentes"""
import sys, platform
import importlib.metadata as metadata
from pathlib import Path

def get_info():
    return {
        "Python": f"{sys.version.split()[0]} ({platform.python_implementation()})",
        "OS": f"{platform.system()} {platform.release()}",
        "Arquitectura": platform.machine(),
        "Entorno": str(Path(sys.prefix).resolve()),
        "Total paquetes": len(list(metadata.distributions()))
    }

def get_packages():
    pkgs = {}
    for dist in metadata.distributions():
        name = dist.metadata.get("Name", "unknown")
        ver = dist.metadata.get("Version", "?")
        pkgs[name.lower().replace("-", "_")] = ver
    return pkgs

def categorize(pkgs):
    cats = {
        "🔬 Investigación/Data": ["polars", "duckdb", "pandas", "numpy", "scipy", "scikit_learn", "statsmodels", "dask", "pyarrow", "plotly", "matplotlib", "seaborn", "optuna", "wandb", "tqdm", "rich"],
        "📄 Ofimática": ["openpyxl", "xlsxwriter", "python_docx", "reportlab", "pdfplumber", "docxtpl", "jinja2"],
        "💻 Dev/Tools": ["jupyterlab", "ipython", "ipykernel", "ipywidgets"],
    }
    res = {}
    for cat, targets in cats.items():
        found = {n: pkgs.get(n) for n in targets if n in pkgs}
        if found: res[cat] = found
    return res

def suggest(pkgs):
    recs = {
        "marimo": ("📊 marimo", "Notebooks reactivos y versionables"),
        "pymc": ("🧮 pymc", "Modelado bayesiano probabilístico"),
        "prefect": ("⚙️ prefect", "Orquestación de pipelines"),
        "pydantic": ("🔒 pydantic", "Validación de datos/config"),
        "great_tables": ("📈 great-tables", "Tablas profesionales"),
        "dvc": ("🔄 dvc", "Versionado de datasets"),
        "hypothesis": ("🧪 hypothesis", "Testing basado en propiedades"),
        "manim": ("🎬 manim", "Animaciones matemáticas"),
        "ruff": ("🧹 ruff", "Linter/formateador ultrarrápido"),
        "pytest": ("🧪 pytest", "Testing profesional")
    }
    return [(disp, desc) for pkg, (disp, desc) in recs.items() if pkg not in pkgs]

def main():
    print("="*60 + "\n🔍 DIAGNÓSTICO ENTORNO ANTIGRAVITY\n" + "="*60)
    info = get_info()
    for k,v in info.items():
        print(f"  {k:18}: {v}")
    
    pkgs = get_packages()
    print("\n📦 INSTALADOS POR CATEGORÍA:")
    for cat, found in categorize(pkgs).items():
        print(f"\n{cat}")
        for n, v in found.items():
            flag = " (rtcompat)" if n=="polars" else ""
            print(f"  ✅ {n} {v}{flag}")
            
    missing = suggest(pkgs)
    if missing:
        print(f"\n{'='*60}\n💡 RECOMENDACIONES PARA AGREGAR:")
        for disp, desc in missing:
            print(f"  ➕ {disp}: {desc}")
        cmd_pkgs = " ".join(pkg.split()[-1].replace("-", "_") for pkg, _ in missing)
        print(f"\n🚀 Instalar todo: uv add {cmd_pkgs}")
    else:
        print(f"\n{'='*60}\n✨ ¡Ya tienes el stack completo recomendado!")
    print("="*60)

if __name__ == "__main__":
    main()
