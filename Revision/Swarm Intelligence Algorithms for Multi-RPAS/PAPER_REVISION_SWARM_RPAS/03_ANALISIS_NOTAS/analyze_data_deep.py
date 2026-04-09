import pandas as pd
import json

ruta = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'

def analyze():
    analysis = {}
    
    # 1. TODOS_PAPERS - General Overview
    df_todos = pd.read_excel(ruta, sheet_name='TODOS_PAPERS')
    analysis['total_papers'] = len(df_todos)
    analysis['algoritmos'] = df_todos['Algoritmo Principal'].value_counts().to_dict()
    analysis['años'] = df_todos['Año'].value_counts().sort_index().to_dict()
    analysis['relevancia'] = df_todos['Relevancia'].value_counts().to_dict()
    analysis['alta_relevancia'] = df_todos[df_todos['Relevancia'] == 'Alta'][['ID', 'Título Completo', 'Año']].to_dict(orient='records')
    
    # 2. METRICAS_COMPARATIVAS
    try:
        df_metricas = pd.read_excel(ruta, sheet_name='METRICAS_COMPARATIVAS')
        analysis['metricas_resumen'] = {
            'tiempo_count': int(df_metricas['Tiempo (num)'].notna().sum()),
            'energia_count': int(df_metricas['Energía (num)'].notna().sum()),
            'convergencia_count': int(df_metricas['Convergencia (num)'].notna().sum()),
            'complejidad_dist': df_metricas['Complejidad'].value_counts().to_dict()
        }
    except:
        analysis['metricas_resumen'] = "Hoja no encontrada o error"

    # 3. BRECHAS_INVESTIGACION
    try:
        df_brechas = pd.read_excel(ruta, sheet_name='BRECHAS_DETALLADAS')
        analysis['brechas_top'] = df_brechas['Tipo Brecha'].value_counts().to_dict()
    except:
        analysis['brechas_top'] = "Hoja no encontrada o error"

    print(json.dumps(analysis, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    analyze()
