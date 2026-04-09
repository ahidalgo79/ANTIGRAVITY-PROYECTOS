import pandas as pd
excel_path = r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\04_BIBLIOGRAFIA\Rescreening_TA_DrGarza_v2.xlsx"
df = pd.read_excel(excel_path, sheet_name="SCREENING_SAMPLE")
# Veamos si hay criterios en las primeras filas
print(df.head(2))
# O busque en otra hoja 'Instrucciones'
xl = pd.ExcelFile(excel_path)
print("Hojas disponibles:", xl.sheet_names)
