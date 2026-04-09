import pandas as pd
archivo_salida = r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\04_BIBLIOGRAFIA\Rescreening_TA_Agente_v3.xlsx"
df = pd.read_excel(archivo_salida, sheet_name="SCREENING_SAMPLE")
print("Decisiones de ASISTENTE (Claude):")
print(df["DECISIÓN_REVISOR1"].value_counts(dropna=False))
print("\nDecisiones de REVISOR 2 (Humano):")
print(df["DECISIÓN_REVISOR2"].value_counts(dropna=False))

# Show the discrepancies
discrepancias = df[df["ACUERDO"] == "✗ Discrepancia"]
print(f"\nDiscrepancias encontradas: {len(discrepancias)}")
for i, row in discrepancias.iterrows():
    print(f"- ID: {row['ID Registro']} | R2(Humano): {row['DECISIÓN_REVISOR2']} | R1(Claude): {row['DECISIÓN_REVISOR1']}")

