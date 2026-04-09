import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

ruta = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'

# Cargar Excel
df = pd.read_excel(ruta, sheet_name='TODOS_PAPERS')

# Clasificación manual basada en títulos (los que ya identificamos)
CLASIFICACION = {
    'PAPER_003': {'Algoritmo': 'SSA', 'Variante': 'CASSA (Chaotic Adaptive Sparrow Search)'},
    'PAPER_005': {'Algoritmo': 'SSA', 'Variante': 'SSA + Bioinspired Neural Network'},
    'PAPER_007': {'Algoritmo': 'Fuzzy', 'Variante': 'SIGPAF (Fuzzy Logic Pathfinding)'},
    'PAPER_008': {'Algoritmo': 'SFLA', 'Variante': 'ISFLA (Improved Shuffled Frog Leaping)'},
    'PAPER_010': {'Algoritmo': 'Review', 'Variante': 'Survey de AI para UAV Path Planning'},
    'PAPER_011': {'Algoritmo': 'Review', 'Variante': 'Survey de SI para Multi-Target Interception'},
    'PAPER_012': {'Algoritmo': 'PSO', 'Variante': 'SPSA (Sparrow Particle Swarm Algorithm)'},
    'PAPER_014': {'Algoritmo': 'Coverage', 'Variante': 'Energy-Efficient Coverage Methods'},
    'PAPER_015': {'Algoritmo': 'Review', 'Variante': 'Survey de Optimization para Motion Planning'},
    'PAPER_017': {'Algoritmo': 'Review', 'Variante': 'Survey de Optimization Approaches'},
    'PAPER_022': {'Algoritmo': 'WPA', 'Variante': 'Multi-Discrete Wolf Pack Algorithm'},
    'PAPER_023': {'Algoritmo': 'Hybrid', 'Variante': 'Hybrid Swarm Intelligence (por verificar)'},
    'PAPER_025': {'Algoritmo': 'NOA', 'Variante': 'Improved Nutcracker Optimization Algorithm'},
    'PAPER_026': {'Algoritmo': 'DBO', 'Variante': 'Improved Dung Beetle Optimization'},
    'PAPER_027': {'Algoritmo': 'GWO', 'Variante': 'Multi-Strategy Collaborative GWO'},
    'PAPER_031': {'Algoritmo': 'DOA', 'Variante': 'Multi-Strategy Dream Optimization'},
    'PAPER_033': {'Algoritmo': 'Review', 'Variante': 'Survey de Formation Trajectory Planning'},
    'PAPER_034': {'Algoritmo': 'Review', 'Variante': 'Comprehensive Review de SI para Multi-UAV'},
}

# Mapeo de algoritmo a categoría principal
ALGORITMO_PRINCIPAL = {
    'SSA': 'SSA', 'Fuzzy': 'Otro', 'SFLA': 'SFLA', 'Review': 'Review',
    'PSO': 'PSO', 'Coverage': 'Otro', 'WPA': 'WPA', 'Hybrid': 'Híbrido',
    'NOA': 'NOA', 'DBO': 'DBO', 'GWO': 'GWO', 'DOA': 'DOA',
}

print("🔄 Clasificando 18 papers 'Otro'...\n")

for paper_id, clasif in CLASIFICACION.items():
    idx = df[df['ID'] == paper_id].index
    if len(idx) == 0:
        print(f"⚠️ {paper_id}: No encontrado")
        continue
    idx = idx[0]
    
    algo_principal = ALGORITMO_PRINCIPAL.get(clasif['Algoritmo'], 'Otro')
    
    # Actualizar fila
    df.at[idx, 'Algoritmo Principal'] = algo_principal
    df.at[idx, 'Algoritmo Secundario'] = clasif['Algoritmo']
    df.at[idx, 'Variante Específica'] = clasif['Variante']
    df.at[idx, 'Fecha Análisis'] = datetime.now().strftime('%Y-%m-%d')
    
    print(f"✅ {paper_id}: {algo_principal} - {clasif['Variante'][:50]}...")

# Guardar Excel
df.to_excel(ruta, sheet_name='TODOS_PAPERS', index=False)

# Actualizar hoja ESTADISTICAS
print(f"\n{'='*60}")
print(f"✅ CLASIFICACIÓN COMPLETADA")
print(f"{'='*60}")

# Mostrar nueva distribución
print("\nNueva distribución por Algoritmo Principal:")
print(df['Algoritmo Principal'].value_counts())