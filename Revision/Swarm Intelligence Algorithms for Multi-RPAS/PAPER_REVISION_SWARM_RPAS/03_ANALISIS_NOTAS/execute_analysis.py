import pandas as pd
import os

file_path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'

if not os.path.exists(file_path):
    print(f"Error: El archivo no existe en {file_path}")
else:
    try:
        xls = pd.ExcelFile(file_path)
        print(f"Archivo cargado. Hojas disponibles: {xls.sheet_names}")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
