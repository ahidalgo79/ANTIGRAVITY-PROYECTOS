# tarea_migrar_tablas.py
import re
from pathlib import Path
import shutil
from datetime import datetime

print("=" * 60)
print("TAREA 1: MIGRACIÓN DE TABLAS A MATERIAL SUPLEMENTARIO")
print("=" * 60)

latex_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")

# Backup
backup = Path(f"PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.backup_migracion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex")
shutil.copy2(latex_path, backup)
print(f"✅ Backup: {backup.name}")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Buscar la tabla de algoritmos (Tabla 2 o similar)
# Asumiendo que está en la sección de resultados
tabla_algoritmos = re.search(r'\\begin\{table\}.*?\\caption\{Algorithm and variant frequency.*?\\end\{table\}', contenido, re.DOTALL)

if tabla_algoritmos:
    tabla_texto = tabla_algoritmos.group(0)
    print(f"📊 Tabla de algoritmos encontrada: {len(tabla_texto.split())} palabras")
    
    # Crear material suplementario
    suplementario = f"""% ============================================================
% SUPPLEMENTARY MATERIAL S1: Detailed Algorithm Distribution
% ============================================================
{tabla_texto}
"""
    suplementario_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/supplementary_algorithm_table.tex")
    with open(suplementario_path, 'w', encoding='utf-8') as f:
        f.write(suplementario)
    print(f"✅ Tabla migrada a: {suplementario_path}")
    
    # Reemplazar en el manuscrito con una nota
    nota_supl = """
% Table migrated to Supplementary Material S1
\\begin{table}[htbp]
\\centering
\\caption{Algorithm distribution across the 33 reviewed studies. For detailed per-algorithm breakdown, see Supplementary Material S1.}
\\begin{tabular}{lr}
\\toprule
\\textbf{Algorithm Category} & \\textbf{Papers (n=33)} \\\\
\\midrule
PSO & 10 (30.3\\%) \\\\
ACO & 3 (9.1\\%) \\\\
ABC & 2 (6.1\\%) \\\\
SSA & 2 (6.1\\%) \\\\
Other SI variants & 6 (18.2\\%) \\\\
Review articles & 7 (21.2\\%) \\\\
\\bottomrule
\\end{tabular}
\\caption{Summary of algorithm distribution. Detailed per-study breakdown available in Supplementary Material S1.}
\\end{table}
"""
    contenido = contenido.replace(tabla_texto, nota_supl)
    print("✅ Tabla reemplazada por resumen en manuscrito")
else:
    print("⚠️ No se encontró la tabla de algoritmos detallada")

# Guardar
with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

print("\n✅ Migración completada")