import pandas as pd
import re
import os
from datetime import datetime

# Rutas
ruta_excel = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
ruta_borrador = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\Borrador_Paper_v1.md'

print("🔍 VALIDACIÓN FINAL DE NÚMEROS")
print("="*60)
print()

# === CARGAR DATOS DEL EXCEL ===
print("📊 Cargando datos del Excel...")
df_todos = pd.read_excel(ruta_excel, sheet_name='TODOS_PAPERS')
df_gaps = pd.read_excel(ruta_excel, sheet_name='GAPS_POR_PAPER')
df_estadisticas = pd.read_excel(ruta_excel, sheet_name='ESTADISTICAS')

# Estadísticas clave desde Excel
excel_stats = {
    'total_papers': len(df_todos),
    'total_gaps': len(df_gaps),
    'pso_count': df_todos['Algoritmo Principal'].value_counts().get('PSO', 0),
    'review_count': df_todos['Algoritmo Principal'].value_counts().get('Review', 0),
    'aco_count': df_todos['Algoritmo Principal'].value_counts().get('ACO', 0),
    'abc_count': df_todos['Algoritmo Principal'].value_counts().get('ABC', 0),
    'ssa_count': df_todos['Algoritmo Principal'].value_counts().get('SSA', 0),
    'gwo_count': df_todos['Algoritmo Principal'].value_counts().get('GWO', 0),
    'dbo_count': df_todos['Algoritmo Principal'].value_counts().get('DBO', 0),
    'noa_count': df_todos['Algoritmo Principal'].value_counts().get('NOA', 0),
    'doa_count': df_todos['Algoritmo Principal'].value_counts().get('DOA', 0),
    'tiempo_count': df_todos['Métrica: Tiempo'].notna().sum(),
    'energia_count': df_todos['Métrica: Energía'].notna().sum(),
    'conv_count': df_todos['Métrica: Convergencia'].notna().sum(),
    'critico_count': df_gaps['Prioridad'].value_counts().get('Crítico', 0),
    'importante_count': df_gaps['Prioridad'].value_counts().get('Importante', 0),
    'menor_count': df_gaps['Prioridad'].value_counts().get('Menor', 0),
    'tec_count': df_gaps['Dimensión'].value_counts().get('Tecnológica', 0),
    'pra_count': df_gaps['Dimensión'].value_counts().get('Práctica', 0),
    'met_count': df_gaps['Dimensión'].value_counts().get('Metodológica', 0),
    'teo_count': df_gaps['Dimensión'].value_counts().get('Teórica', 0),
}

# Calcular porcentajes
excel_stats['pso_pct'] = (excel_stats['pso_count'] / excel_stats['total_papers']) * 100
excel_stats['review_pct'] = (excel_stats['review_count'] / excel_stats['total_papers']) * 100
excel_stats['critico_pct'] = (excel_stats['critico_count'] / excel_stats['total_gaps']) * 100
excel_stats['tec_pct'] = (excel_stats['tec_count'] / excel_stats['total_gaps']) * 100
excel_stats['pra_pct'] = (excel_stats['pra_count'] / excel_stats['total_gaps']) * 100
excel_stats['met_pct'] = (excel_stats['met_count'] / excel_stats['total_gaps']) * 100
excel_stats['teo_pct'] = (excel_stats['teo_count'] / excel_stats['total_gaps']) * 100
excel_stats['tiempo_pct'] = (excel_stats['tiempo_count'] / excel_stats['total_papers']) * 100
excel_stats['energia_pct'] = (excel_stats['energia_count'] / excel_stats['total_papers']) * 100
excel_stats['conv_pct'] = (excel_stats['conv_count'] / excel_stats['total_papers']) * 100

print(f"   ✅ {excel_stats['total_papers']} papers cargados")
print(f"   ✅ {excel_stats['total_gaps']} gaps cargados")
print()

# === CARGAR Y ANALIZAR EL BORRADOR ===
print("📝 Analizando Borrador_Paper_v1.md...")
with open(ruta_borrador, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Función para extraer números del texto
def extraer_numero(texto, patron):
    match = re.search(patron, texto)
    if match:
        return float(match.group(1))
    return None

# Extraer números del borrador
draft_stats = {}

# Total papers
match = re.search(r'analyzed\s+(\d+)\s+peer-reviewed', contenido, re.I)
if match:
    draft_stats['total_papers'] = int(match.group(1))

# Total gaps
match = re.search(r'identified\s+(\d+)\s+research\s+gaps', contenido, re.I)
if match:
    draft_stats['total_gaps'] = int(match.group(1))

# PSO count y porcentaje
match = re.search(r'PSO\)\s+dominates.*?\((\d+)\s*papers,\s*([\d.]+)%\)', contenido, re.I)
if match:
    draft_stats['pso_count'] = int(match.group(1))
    draft_stats['pso_pct'] = float(match.group(2))

# Review count
match = re.search(r'review\s+articles\s+\((\d+)\s*papers', contenido, re.I)
if match:
    draft_stats['review_count'] = int(match.group(1))

# Critical gaps
match = re.search(r'with\s+(\d+)\s+classified\s+as\s+critical\s+\(([\d.]+)%\)', contenido, re.I)
if match:
    draft_stats['critico_count'] = int(match.group(1))
    draft_stats['critico_pct'] = float(match.group(2))

# Time metrics
match = re.search(r'only\s+([\d.]+)%\s+report\s+quantitative\s+time\s+metrics', contenido, re.I)
if match:
    draft_stats['tiempo_pct'] = float(match.group(1))

# Hardware validation gap
match = re.search(r'(\d+\.?\d*)%\s+of\s+studies\s+lack\s+hardware\s+validation', contenido, re.I)
if match:
    draft_stats['sin_validacion_pct'] = float(match.group(1))

# Environmental modeling gap
match = re.search(r'(\d+\.?\d*)%\s+do\s+not\s+model\s+environmental\s+variability', contenido, re.I)
if match:
    draft_stats['sin_ambiente_pct'] = float(match.group(1))

# Dimensions percentages
match = re.search(r'Technological\s+\((\d+)\s*gaps,\s*([\d.]+)%\)', contenido, re.I)
if match:
    draft_stats['tec_count'] = int(match.group(1))
    draft_stats['tec_pct'] = float(match.group(2))

match = re.search(r'Practical\s+\((\d+)\s*gaps,\s*([\d.]+)%\)', contenido, re.I)
if match:
    draft_stats['pra_count'] = int(match.group(1))
    draft_stats['pra_pct'] = float(match.group(2))

match = re.search(r'Methodological\s+\((\d+)\s*gaps,\s*([\d.]+)%\)', contenido, re.I)
if match:
    draft_stats['met_count'] = int(match.group(1))
    draft_stats['met_pct'] = float(match.group(2))

match = re.search(r'Theoretical\s+\((\d+)\s*gaps,\s*([\d.]+)%\)', contenido, re.I)
if match:
    draft_stats['teo_count'] = int(match.group(1))
    draft_stats['teo_pct'] = float(match.group(2))

print(f"   ✅ {len(draft_stats)} números extraídos del borrador")
print()

# === COMPARAR Y REPORTAR ===
print("🔎 Comparando Excel vs. Borrador...")
print("="*60)

discrepancias = []
coincidencias = []

# Lista de métricas a validar
metricas_a_validar = [
    ('total_papers', 'Total papers analizados', '{:.0f}'),
    ('total_gaps', 'Total gaps documentados', '{:.0f}'),
    ('pso_count', 'PSO: número de papers', '{:.0f}'),
    ('pso_pct', 'PSO: porcentaje', '{:.1f}%'),
    ('critico_count', 'Gaps críticos: cantidad', '{:.0f}'),
    ('critico_pct', 'Gaps críticos: porcentaje', '{:.1f}%'),
    ('tec_pct', 'Dimensión Tecnológica', '{:.1f}%'),
    ('pra_pct', 'Dimensión Práctica', '{:.1f}%'),
    ('met_pct', 'Dimensión Metodológica', '{:.1f}%'),
    ('teo_pct', 'Dimensión Teórica', '{:.1f}%'),
    ('tiempo_pct', 'Métricas de tiempo reportadas', '{:.1f}%'),
    ('sin_validacion_pct', 'Papers sin validación hardware', '{:.1f}%'),
    ('sin_ambiente_pct', 'Papers sin modelado ambiental', '{:.1f}%'),
]

for key, descripcion, formato in metricas_a_validar:
    excel_val = excel_stats.get(key)
    draft_val = draft_stats.get(key)
    
    if excel_val is None:
        print(f"⚠️  {descripcion}: No encontrado en Excel")
        continue
    if draft_val is None:
        print(f"❌ {descripcion}: No encontrado en borrador (Excel: {formato.format(excel_val)})")
        discrepancias.append((key, descripcion, excel_val, None))
        continue
    
    # Comparar con tolerancia para porcentajes
    if isinstance(excel_val, float) and isinstance(draft_val, float):
        if abs(excel_val - draft_val) < 0.2:  # Tolerancia de 0.2%
            print(f"✅ {descripcion}: {formato.format(excel_val)} = {formato.format(draft_val)}")
            coincidencias.append(key)
        else:
            print(f"❌ {descripcion}: Excel={formato.format(excel_val)} vs Borrador={formato.format(draft_val)}")
            discrepancias.append((key, descripcion, excel_val, draft_val))
    else:
        if excel_val == draft_val:
            print(f"✅ {descripcion}: {excel_val} = {draft_val}")
            coincidencias.append(key)
        else:
            print(f"❌ {descripcion}: Excel={excel_val} vs Borrador={draft_val}")
            discrepancias.append((key, descripcion, excel_val, draft_val))

print()
print("="*60)
print("📊 RESUMEN DE VALIDACIÓN")
print("="*60)
print(f"Coincidencias: {len(coincidencias)}/{len(metricas_a_validar)}")
print(f"Discrepancias: {len(discrepancias)}/{len(metricas_a_validar)}")

if len(discrepancias) == 0:
    print()
    print("🎉 ¡TODOS LOS NÚMEROS COINCIDEN!")
    print("   Tu borrador está listo para el siguiente paso.")
else:
    print()
    print("⚠️  Se encontraron discrepancias. Revisa manualmente:")
    for key, desc, excel_val, draft_val in discrepancias:
        print(f"   • {desc}: Excel={excel_val} vs Borrador={draft_val}")

print()
print("📋 Próximos pasos recomendados:")
if len(discrepancias) == 0:
    print("   1. ✅ Validación completada")
    print("   2. Preparar Supplementary Material (ZIP)")
    print("   3. Completar PRISMA Checklist")
    print("   4. Revisión final de estilo académico")
    print("   5. SUBMIT a Computers and Electronics in Agriculture")
else:
    print("   1. ⚠️ Corregir discrepancias en Borrador_Paper_v1.md")
    print("   2. Re-ejecutar esta validación")
    print("   3. Continuar con Supplementary Material")

# Guardar reporte de validación
reporte_path = os.path.join(os.path.dirname(ruta_borrador), 'Validacion_Numeros_Reporte.txt')
with open(reporte_path, 'w', encoding='utf-8') as f:
    f.write(f"Reporte de Validación de Números\n")
    f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write(f"{'='*60}\n\n")
    f.write(f"Coincidencias: {len(coincidencias)}/{len(metricas_a_validar)}\n")
    f.write(f"Discrepancias: {len(discrepancias)}/{len(metricas_a_validar)}\n\n")
    if discrepancias:
        f.write("Discrepancias encontradas:\n")
        for key, desc, excel_val, draft_val in discrepancias:
            f.write(f"  • {desc}: Excel={excel_val} vs Borrador={draft_val}\n")
    else:
        f.write("✅ Todos los números coinciden correctamente.\n")

print(f"\n📄 Reporte guardado: {reporte_path}")
