import pandas as pd
import sys
import os

# Set execution encoding to utf-8
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

file_path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'

if not os.path.exists(file_path):
    print(f"Error: El archivo no existe en {file_path}")
else:
    try:
        xl = pd.ExcelFile(file_path)
        print(f"Hojas encontradas: {xl.sheet_names}")
        
        for sheet in xl.sheet_names:
            print(f"\n--- Analizando hoja: {sheet} ---")
            df = xl.parse(sheet)
            print(f"Filas: {len(df)}, Columnas: {list(df.columns)}")
            
            # Print first 3 rows, handling potential encoding issues in content
            content = df.head(3).to_string()
            print("Primeras 3 filas (resumen):")
            print(content)
            
            # Additional summary logic
            if 'Algoritmo Principal' in df.columns:
                print("\nConteo de Algoritmos Principales:")
                print(df['Algoritmo Principal'].value_counts().head(5))
            
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
