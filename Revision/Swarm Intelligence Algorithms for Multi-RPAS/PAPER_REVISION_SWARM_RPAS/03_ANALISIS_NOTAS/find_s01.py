import os
import pandas as pd

target_dir = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS'

def search():
    for root, _, files in os.walk(target_dir):
        for f in files:
            if f.endswith('.xlsx'):
                path = os.path.join(root, f)
                try:
                    xl = pd.ExcelFile(path)
                    for s in xl.sheet_names:
                        df = xl.parse(s)
                        if df.astype(str).apply(lambda x: x.str.contains('S01').any()).any():
                            print(f'Found S01 in {path} -> {s}')
                except Exception as e:
                    pass

if __name__ == '__main__':
    search()
