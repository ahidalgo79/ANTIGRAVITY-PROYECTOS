import pandas as pd
import re

tex_path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\main_expanded.tex'
bib_path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\references.bib'
excel1 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
excel2 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Swarm Drones Path Planning - Papers con DOI.xlsx'

def extract_all():
    # 1. Parse main_expanded.tex for S01-S33 table entries
    s_mapping = {}
    with open(tex_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    for line in lines:
        if line.startswith('S'):
            m = re.match(r'(S\d{2})\s*&\s*.*?\\cite\{(.*?)\}', line)
            if m:
                s_id, cite_key = m.groups()
                s_mapping[cite_key] = s_id

    # 2. Extract Bib titles
    bib_titles = {}
    with open(bib_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    entries = content.split('@')
    for e in entries[1:]:
        lines = e.split('\n')
        if not lines: continue
        first = lines[0]
        if '{' in first and ',' in first:
            key = first[first.find('{')+1:first.find(',')]
            title_m = re.search(r'title\s*=\s*[\{"](.*?)[\\}"]', e, re.IGNORECASE)
            if title_m:
                bib_titles[key] = title_m.group(1).replace('{', '').replace('}', '')

    # 3. Create included list
    included = []
    for k, s_id in s_mapping.items():
        title = bib_titles.get(k, 'Title not found')
        included.append({'ID': s_id, 'Status': 'Included', 'Title': title})

    df1 = pd.read_excel(excel1, sheet_name='TODOS_PAPERS')
    df2 = pd.read_excel(excel2, sheet_name='TODOS_PAPERS')
    
    # 33 included IDs
    df1_ids = df1['ID'].dropna().tolist()
    
    # 4. Find all other IDs not in df1
    excluded_df2 = df2[~df2['ID'].isin(df1_ids)]
    
    # Find whatever else we can to form 51
    excluded = []
    for idx, row in excluded_df2.iterrows():
        id_ = row['ID']
        title = row.get('Título Completo', row.iloc[1])
        excluded.append({'ID': id_, 'Status': 'Excluded', 'Title': title})

    res = included + excluded
    print(f"Total reconstructed: {len(res)} (Expected 51)")
    for r in sorted(res, key=lambda x: x['ID']):
        print(f"[{r['Status']}] {r['ID']} - {str(r['Title'])[:80]}")

if __name__ == '__main__':
    extract_all()
