import pandas as pd

ruta = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
df = pd.read_excel(ruta, sheet_name='TODOS_PAPERS')

nueva_fila = {
    'ID': 'PAPER_020',
    'Título Completo': 'An Intelligently Enhanced Ant Colony Optimization Algorithm for Global Path Planning of Mobile Robots in Engineering Applications',
    'Autores': 'Peng Li, Lei Wei, Dongsu Wu',
    'Año': 2025,
    'Fuente': 'Sensors (MDPI)',
    'DOI': '10.3390/s25051326',
    'URL': 'https://doi.org/10.3390/s25051326',
    'Algoritmo Principal': 'ACO',
    'Aplicación Principal': 'Otro',
    'Validación': 'Simulación+Experimentos',
    'Relevancia': 'Alta',
    'Estado Lectura': 'Abstract leído',
    'Fecha Análisis': '2026-01-30'
}

df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
df.to_excel(ruta, sheet_name='TODOS_PAPERS', index=False)

print(f"✅ PAPER_020 agregado")
print(f"Total papers: {len(df)}")