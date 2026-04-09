import pandas as pd
import os

path1 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
path2 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Swarm Drones Path Planning - Papers con DOI.xlsx'
out_path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\dumped_papers.csv'

def dump():
    out_lines = []
    try:
        xl1 = pd.ExcelFile(path1)
        if 'TODOS_PAPERS' in xl1.sheet_names:
            df1 = xl1.parse('TODOS_PAPERS')
            df1['Source_File'] = 'Fichas_Analisis_NUEVO'
            out_lines.append(df1)
    except Exception as e:
        print(f"Error reading {path1}: {e}")

    try:
        xl2 = pd.ExcelFile(path2)
        if 'TODOS_PAPERS' in xl2.sheet_names:
            df2 = xl2.parse('TODOS_PAPERS')
            df2['Source_File'] = 'Swarm_Drones_DOI'
            out_lines.append(df2)
        # Check other sheets just in case
        for s in xl2.sheet_names:
            if s != 'TODOS_PAPERS':
                df_temp = xl2.parse(s)
                if not df_temp.empty and len(df_temp.columns) > 1:
                    df_temp['Source_File'] = f'Swarm_Drones_DOI_{s}'
                    out_lines.append(df_temp)
    except Exception as e:
        print(f"Error reading {path2}: {e}")

    if out_lines:
        merged = pd.concat(out_lines, ignore_index=True)
        merged.to_csv(out_path, index=False)
        print(f"Dumped {len(merged)} total rows to {out_path}")
        
if __name__ == '__main__':
    dump()
