import pandas as pd
import sys

path1 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
path2 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Swarm Drones Path Planning - Papers con DOI.xlsx'

def analyze():
    print("--- Fichas_Analisis_NUEVO.xlsx Sheets ---")
    try:
        xl1 = pd.ExcelFile(path1)
        print(xl1.sheet_names)
        if 'TODOS_PAPERS' in xl1.sheet_names:
            df = xl1.parse('TODOS_PAPERS')
            print("\nColumns in TODOS_PAPERS:", df.columns.tolist())
            print("\nSample of ID and Title from TODOS_PAPERS:")
            cols_to_print = [c for c in df.columns if 'id' in str(c).lower() or 'tit' in str(c).lower() or 'stat' in str(c).lower() or 'inc' in str(c).lower() or 'exc' in str(c).lower()]
            if cols_to_print:
                print(df[cols_to_print].head(10).to_string())
            print(f"\nTotal rows in TODOS_PAPERS: {len(df)}")
    except Exception as e:
        print(f"Error reading path1: {e}")

    print("\n--- Swarm Drones Path Planning - Papers con DOI.xlsx Sheets ---")
    try:
        xl2 = pd.ExcelFile(path2)
        print(xl2.sheet_names)
        for s in xl2.sheet_names:
            df = xl2.parse(s)
            print(f"\nColumns in {s}:", df.columns.tolist()[:10]) # just first 10 columns
            print(f"Total rows in {s}: {len(df)}")
    except Exception as e:
        print(f"Error reading path2: {e}")

if __name__ == '__main__':
    analyze()
