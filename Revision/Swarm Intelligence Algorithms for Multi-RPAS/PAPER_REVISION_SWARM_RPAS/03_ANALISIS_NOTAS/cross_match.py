import pandas as pd

excel2 = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Swarm Drones Path Planning - Papers con DOI.xlsx'
csv_export = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\02_PAPERS_ORGANIZADOS\export-data.csv'

def cross_match():
    # Load 41 records from export CSV
    df_csv = pd.read_csv(csv_export, encoding='utf-8', on_bad_lines='skip')
    csv_titles = set(df_csv['Title'].dropna().str.lower().str.strip())
    
    # Load 43 records from Excel
    df_ex = pd.read_excel(excel2, sheet_name='TODOS_PAPERS')
    ex_titles = df_ex['Título Completo'].dropna().str.lower().str.strip().tolist()
    ex_ids = df_ex['ID'].dropna().tolist()
    
    ex_title_to_id = dict(zip(ex_titles, ex_ids))
    ex_titles_set = set(ex_titles)
    
    # Overlap
    intersection = csv_titles.intersection(ex_titles_set)
    csv_only = csv_titles - ex_titles_set
    ex_only = ex_titles_set - csv_titles
    
    print(f"Total in CSV: {len(csv_titles)}")
    print(f"Total in Excel: {len(ex_titles_set)}")
    print(f"Intersection: {len(intersection)}")
    print(f"Only in CSV: {len(csv_only)}")
    print(f"Only in Excel: {len(ex_only)}")
    
    total_unique = len(csv_titles.union(ex_titles_set))
    print(f"Total Unique across BOTH: {total_unique}")
    
    print("\n--- Only in Excel (probably the 10 unread?): ---")
    for t in ex_only:
        print(f"{ex_title_to_id.get(t, 'N/A')}: {t[:60]}")

if __name__ == '__main__':
    cross_match()
