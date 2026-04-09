# tarea5_calcular_kappa.py
import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score, confusion_matrix
from pathlib import Path
import json

print("=" * 60)
print("TAREA 5: CALCULAR COHEN'S KAPPA")
print("=" * 60)

# 1. Cargar el archivo Excel actualizado
archivo = Path("04_BIBLIOGRAFIA/Rescreening_TA_DrGarza.xlsx")
try:
    # Tras la Tarea 4, el archivo ya tiene los encabezados correctos en la fila 0
    df = pd.read_excel(archivo)
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    exit()

print(f"\nArchivo cargado: {archivo.name}")
print(f"Total registros: {len(df)}")

# 2. Identificar columnas (con manejo de nombres exactos con tildes)
col_id = 'ID Registro'
col_rev2 = 'DECISIÓN_REVISOR2'
col_rev1 = 'DECISIÓN_REVISOR1' # Podria no existir en el Excel

# Si falta la columna del Revisor 1, la creamos asumiendo que todos eran EXCLUIR 
if col_rev1 not in df.columns:
    print(f"\nINFO: Columna '{col_rev1}' no encontrada. Asumiendo 'EXCLUIR' para todos.")
    df[col_rev1] = 'EXCLUIR'

# 3. Limpieza y preparacion de datos
df = df.dropna(subset=[col_id])

print(f"\nDatos disponibles:")
print(f"  - Revisor 1 (Original): {df[col_rev1].notna().sum()} decisiones")
print(f"  - Revisor 2 (AI): {df[col_rev2].notna().sum()} decisiones")

# Filtrar solo registros con ambas decisiones
completos = df[df[col_rev1].notna() & df[col_rev2].notna()].copy()

# 4. Normalizacion de etiquetas
completos[col_rev1] = completos[col_rev1].astype(str).str.strip().str.upper()
completos[col_rev2] = completos[col_rev2].astype(str).str.strip().str.upper()

# 5. Calculo de metricas
valores_todos = sorted(list(set(completos[col_rev1].unique()) | set(completos[col_rev2].unique())))
mapeo = {v: i for i, v in enumerate(valores_todos)}

print(f"\nMapeo de valores:")
for label, val in mapeo.items():
    print(f"  - {label} -> {val}")

y_true = completos[col_rev1].map(mapeo)
y_pred = completos[col_rev2].map(mapeo)

kappa = cohen_kappa_score(y_true, y_pred)

# Interpretacion estandar
if kappa < 0: interpretacion = "Sin acuerdo"
elif kappa <= 0.20: interpretacion = "Acuerdo insignificante"
elif kappa <= 0.40: interpretacion = "Acuerdo bajo"
elif kappa <= 0.60: interpretacion = "Acuerdo moderado"
elif kappa <= 0.80: interpretacion = "Acuerdo sustancial"
else: interpretacion = "Acuerdo casi perfecto"

print("\n" + "=" * 60)
print("RESULTADO COHEN'S KAPPA")
print("=" * 60)
print(f"Kappa: {kappa:.4f}")
print(f"Interpretacion: {interpretacion}")
print(f"N (Registros): {len(completos)}")

# 6. Matriz de Confusion
cm = confusion_matrix(y_true, y_pred, labels=list(mapeo.values()))
print("\nMatriz de Confusion:")
print(f"Filas: Revisor 1 | Columnas: Revisor 2")
for i, label in enumerate(valores_todos):
    print(f"  {label:<12}: {cm[i].tolist()}")

# 7. Discordancias
discordantes = completos[completos[col_rev1] != completos[col_rev2]]
print(f"\nDiscordancias encontradas: {len(discordantes)}")

if len(discordantes) > 0:
    for idx, row in discordantes.iterrows():
        print(f"  - {row[col_id]}: R1={row[col_rev1]} vs R2={row[col_rev2]}")

# 8. Guardar JSON final
resultados = {
    'kappa': float(kappa),
    'interpretacion': interpretacion,
    'n': len(completos),
    'matriz': cm.tolist(),
    'etiquetas': valores_todos,
    'discordantes': [row[col_id] for idx, row in discordantes.iterrows()]
}

with open('resultado_kappa_final.json', 'w', encoding='utf-8') as f:
    json.dump(resultados, f, indent=2)


print(f"\nReporte guardado en: resultado_kappa_final.json")
