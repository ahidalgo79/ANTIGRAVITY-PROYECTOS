import pandas as pd
import glob

dfs = []
for f in glob.glob('*.xlsx'):
    try:
        xl = pd.ExcelFile(f)
        for s in xl.sheet_names:
            df = xl.parse(s)
            if 'ID' in df.columns:
                print(f"File: {f}, Sheet: {s}, unique IDs: {df['ID'].dropna().nunique()}")
                temp = pd.DataFrame()
                temp['ID'] = df['ID']
                if 'Ttulo Completo' in df.columns: temp['Title'] = df['Ttulo Completo']
                elif 'Título Completo' in df.columns: temp['Title'] = df['Título Completo']
                elif len(df.columns)>1: temp['Title'] = df.iloc[:,1]
                temp['Source'] = f
                dfs.append(temp.dropna(subset=['ID']))
    except Exception as e:
        print(f"Error reading {f}: {e}")

if dfs:
    res = pd.concat(dfs).drop_duplicates(subset=['ID']).sort_values('ID')
    print(f"\nTotal Unique IDs across all: {len(res)}")
    print(res.to_string())
