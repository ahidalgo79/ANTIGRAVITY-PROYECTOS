import pandas as pd
from datetime import datetime
import os

# Rutas
ruta_excel = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
ruta_salida = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\Borrador_Paper_v1.md'

print("📝 Generando Borrador_Paper_v1.md paso a paso...\n")

# Cargar datos del Excel
df_todos = pd.read_excel(ruta_excel, sheet_name='TODOS_PAPERS')
df_gaps = pd.read_excel(ruta_excel, sheet_name='GAPS_POR_PAPER')
df_metricas = pd.read_excel(ruta_excel, sheet_name='METRICAS_COMPARATIVAS')

# Estadísticas clave
total_papers = len(df_todos)
total_gaps = len(df_gaps)
algo_counts = df_todos['Algoritmo Principal'].value_counts()
pso_count = algo_counts.get('PSO', 0)
pso_pct = (pso_count / total_papers) * 100

# Gaps por dimensión
dim_counts = df_gaps['Dimensión'].value_counts()

# Gaps por prioridad
pri_counts = df_gaps['Prioridad'].value_counts()
critico_count = pri_counts.get('Crítico', 0)

# Métricas disponibles
tiempo_count = df_todos['Métrica: Tiempo'].notna().sum()
energia_count = df_todos['Métrica: Energía'].notna().sum()
conv_count = df_todos['Métrica: Convergencia'].notna().sum()

print(f"✅ Datos cargados:")
print(f"   • Total papers: {total_papers}")
print(f"   • Total gaps: {total_gaps}")
print(f"   • PSO: {pso_count} ({pso_pct:.1f}%)")
print(f"   • Gaps críticos: {critico_count}")
print()