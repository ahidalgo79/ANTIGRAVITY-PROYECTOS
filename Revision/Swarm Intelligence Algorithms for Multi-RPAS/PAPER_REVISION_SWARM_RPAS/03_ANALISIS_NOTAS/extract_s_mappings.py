import pandas as pd
import re

tex_path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\main_expanded.tex'
bib_path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\references.bib'
excel1 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
excel2 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Swarm Drones Path Planning - Papers con DOI.xlsx'

def extract():
    # 1. Parse main_expanded.tex for S01-S33 table entries
    s_mapping = {}
    with open(tex_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        if line.startswith('S'):
            # Example: S01 & Phung \u0026 Ha \cite{phung2021}$^\dagger$
            m = re.match(r'(S\d{2})\s*&\s*.*?\\cite\{(.*?)\}', line)
            if m:
                s_id, cite_key = m.groups()
                s_mapping[cite_key] = s_id

    # 2. Extract 43 unique rows from Excel
    df1 = pd.read_excel(excel1, sheet_name='TODOS_PAPERS')
    df2 = pd.read_excel(excel2, sheet_name='TODOS_PAPERS')
    
    included_ids = df1['ID'].dropna().tolist()
    
    print(f"Total mapped from tex: {len(s_mapping)}")
    print(f"Total included in df1: {len(included_ids)}")
    print(f"Total pool in df2: {len(df2['ID'].dropna().unique())}")
    
    # Analyze exclusions from df2
    excluded = df2[~df2['ID'].isin(included_ids)]
    print(f"\nExcluded in df2 ({len(excluded)} records):")
    cols = ['ID', 'Ttulo Completo'] if 'Ttulo Completo' in df2.columns else df2.columns[:2]
    # For excluded, maybe they have relevance info or reason?
    for idx, row in excluded.iterrows():
        id_ = row['ID']
        title = row.get('Título Completo', row.iloc[1])
        rel = row.get('Relevancia', 'N/A')
        state = row.get('Estado Lectura', 'N/A')
        print(f" - {id_}: {str(title)[:60]} | Rel: {rel} | {state}")

if __name__ == '__main__':
    extract()
