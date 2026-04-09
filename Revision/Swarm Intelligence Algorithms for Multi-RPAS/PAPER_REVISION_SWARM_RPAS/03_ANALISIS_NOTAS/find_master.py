import os
import glob
import pandas as pd

base_dir = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS'

files_to_check = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.xlsx') or f.endswith('.csv'):
            files_to_check.append(os.path.join(root, f))

print(f"Buscando en {len(files_to_check)} archivos...")

found = False
for path in files_to_check:
    try:
        # Load fast by only reading the first few rows just to check length, or shape if possible.
        if path.endswith('.csv'):
            # Count lines in CSV without loading entirely to be safe, but pandas is fast enough
            df = pd.read_csv(path, on_bad_lines='skip', low_memory=False)
        else:
            df = pd.read_excel(path, sheet_name=0)
            
        rows = len(df)
        if rows > 200 and rows < 1000: # We're looking for ~433 or ~514
            cols = list(df.columns[:5])
            print('-----------------------------------------')
            print(f"ARCHIVO POTENCIAL: {os.path.basename(path)}")
            print(f"RUTA: {path}")
            print(f"FILAS: {rows}")
            print(f"COLUMNAS PRINCIPALES: {cols}")
            found = True
    except Exception as e:
        pass

if not found:
    print("No se encontró ningún archivo con entre 200 y 1000 filas.")
