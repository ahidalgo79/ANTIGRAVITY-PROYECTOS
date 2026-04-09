import pandas as pd

ruta_excel = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'

# Cargar TODOS_PAPERS
df_todos = pd.read_excel(ruta_excel, sheet_name='TODOS_PAPERS')

# Filtrar PSO
df_pso = df_todos[df_todos['Algoritmo Principal'] == 'PSO'].copy()

# Cargar Excel completo
with pd.ExcelWriter(ruta_excel, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
    df_pso.to_excel(writer, sheet_name='PSO_ALGORITMOS', index=False)

print(f"✅ PSO_ALGORITMOS actualizado")
print(f"Papers PSO: {len(df_pso)}")
print(f"IDs: {df_pso['ID'].tolist()}")