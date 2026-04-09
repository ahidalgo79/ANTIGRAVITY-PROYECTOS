import pandas as pd
import re

tex_path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\main_expanded.tex'
bib_path = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\references.bib'
csv_export = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\02_PAPERS_ORGANIZADOS\export-data.csv'
excel1 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
excel2 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Swarm Drones Path Planning - Papers con DOI.xlsx'

def norm(t):
    return re.sub(r'[^a-z0-9]', '', str(t).lower())

def generate_report():
    # 1. Parse main_expanded.tex for S01-S33
    s_mapping = {}
    with open(tex_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('S'):
                m = re.match(r'(S\d{2})\s*&\s*.*?\\cite\{(.*?)\}', line)
                if m:
                    s_id, cite_key = m.groups()
                    s_mapping[cite_key] = s_id

    # 2. Extract Bib titles and authors
    bib_data = {}
    with open(bib_path, 'r', encoding='utf-8') as f:
        entries = f.read().split('@')
        for e in entries[1:]:
            lines = e.split('\n')
            if not lines: continue
            first = lines[0]
            if '{' in first and ',' in first:
                key = first[first.find('{')+1:first.find(',')]
                t_m = re.search(r'title\s*=\s*[\{"](.*?)[\\}"]', e, re.IGNORECASE)
                a_m = re.search(r'author\s*=\s*[\{"](.*?)[\\}"]', e, re.IGNORECASE)
                y_m = re.search(r'year\s*=\s*[\{"]?(.*?)[\}"]?,', e, re.IGNORECASE)
                
                title = t_m.group(1).replace('{', '').replace('}', '') if t_m else ''
                author = a_m.group(1).replace('{', '').replace('}', '') if a_m else ''
                year = y_m.group(1) if y_m else ''
                
                bib_data[key] = {'Title': title, 'Author': author, 'Year': year}

    included = []
    included_norm_titles = set()
    for k, s_id in s_mapping.items():
        data = bib_data.get(k, {'Title': 'Unknown', 'Author': '', 'Year': ''})
        included.append({'ID': s_id, 'Status': 'Incluido', 'Title': data['Title'], 'Author': data['Author'], 'Year': data['Year']})
        included_norm_titles.add(norm(data['Title']))

    # 3. Process export-data.csv
    df_csv = pd.read_csv(csv_export, encoding='utf-8', on_bad_lines='skip')
    csv_excluded = []
    count = 1
    for _, row in df_csv.iterrows():
        t = str(row['Title'])
        if norm(t) not in included_norm_titles:
            csv_excluded.append({'ID': f'EXC_{count:02d}', 
                                 'Status': 'Excluido', 
                                 'Title': t, 
                                 'Author': row.get('Author', ''), 
                                 'Year': str(row.get('Publication Year', ''))})
            count += 1

    # 4. Process the 10 Excel exclusions
    df_ex = pd.read_excel(excel2, sheet_name='TODOS_PAPERS')
    df1 = pd.read_excel(excel1, sheet_name='TODOS_PAPERS')
    df1_ids = df1['ID'].dropna().tolist()
    
    excel_excluded_df = df_ex[~df_ex['ID'].isin(df1_ids)]
    excel_excluded = []
    for _, row in excel_excluded_df.iterrows():
        t = str(row.get('Título Completo', row.iloc[1]))
        if norm(t) not in included_norm_titles:
            excel_excluded.append({'ID': row['ID'], 
                                   'Status': 'Excluido', 
                                   'Title': t, 
                                   'Author': row.get('Autores', ''), 
                                   'Year': str(row.get('Año', ''))})

    total_records = included + csv_excluded + excel_excluded
    
    # Generate Output Markdown
    out_lines = ["# Lista de 51 Registros Evaluados a Texto Completo (PRISMA 2020)", ""]
    out_lines.append(f"**Total Reconstruido:** {len(total_records)} registros ({len(included)} Incluidos [S01-S33], {len(csv_excluded) + len(excel_excluded)} Excluidos)")
    out_lines.append("")
    out_lines.append("## 33 Estudios Incluidos (Documentados en Manuscrito)")
    out_lines.append("| ID maestro | Autores | Año | Título |")
    out_lines.append("|:---|:---|:---|:---|")
    
    for r in sorted(included, key=lambda x: str(x['ID'])):
        out_lines.append(f"| {r['ID']} | {r['Author'][:40]}... | {r['Year']} | {r['Title']} |")
        
    out_lines.append("")
    out_lines.append("## 18 Estudios Excluidos a Texto Completo")
    out_lines.append("| ID Origen | Autores | Año | Título |")
    out_lines.append("|:---|:---|:---|:---|")
    for r in sorted(csv_excluded + excel_excluded, key=lambda x: str(x['ID'])):
        out_lines.append(f"| {r['ID']} | {str(r['Author'])[:40]}... | {r['Year']} | {r['Title']} |")
        
    out_path = r'C:\Users\HangarUPCH\.gemini\antigravity\brain\a4facafe-be66-4a77-81fb-ed40f9ead70f\lista_51_registros_PRISMA.md'
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(out_lines))
        
    print(f"Generated {out_path} with {len(total_records)} records!")

if __name__ == '__main__':
    generate_report()
