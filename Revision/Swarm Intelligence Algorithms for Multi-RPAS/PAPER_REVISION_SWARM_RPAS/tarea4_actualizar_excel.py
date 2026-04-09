# tarea4_actualizar_excel.py
import pandas as pd
import json
from pathlib import Path

print("=" * 60)
print("TAREA 4: ACTUALIZAR EXCEL CON ABSTRACTS OBTENIDOS")
print("=" * 60)

# Cargar el archivo Excel
archivo = Path("04_BIBLIOGRAFIA/Rescreening_TA_DrGarza.xlsx")
try:
    # Usamos header=2 para que los nombres de las columnas coincidan con los datos reales
    df = pd.read_excel(archivo, sheet_name='SCREENING_SAMPLE', header=2)
except Exception as e:
    print(f"Error al leer el archivo Excel: {e}")
    exit()

print(f"\nArchivo cargado: {archivo.name}")
print(f"Total registros: {len(df)}")

# Identificar columnas
col_id = 'ID Registro'
col_abstract = 'RESUMEN (extracto)'

if col_id not in df.columns or col_abstract not in df.columns:
    print(f"Error: No se encuentran las columnas necesarias")
    print(f"Columnas disponibles: {list(df.columns)}")
    exit()

# Cargar abstracts consolidados
json_file = Path("todos_los_abstracts_consolidado.json")
if not json_file.exists():
    print(f"Error: No se encuentra el archivo {json_file}")
    exit()

with open(json_file, 'r', encoding='utf-8') as f:
    abstracts = json.load(f)

print(f"\nAbstracts disponibles para insertar: {len(abstracts)}")

# Contar cuantos se van a actualizar
actualizados = 0
ya_tenian = 0

for idx, row in df.iterrows():
    id_registro = str(row[col_id]).strip()
    
    if id_registro in abstracts:
        abstract_texto = abstracts[id_registro]['abstract']
        
        # Verificar si ya tiene abstract o esta vacio
        valor_actual = str(row[col_abstract]) if pd.notna(row[col_abstract]) else ""
        
        # Consideramos vacio si es nan o string vacio
        if valor_actual == "" or valor_actual.lower() == "nan" or len(valor_actual) < 10:
            df.at[idx, col_abstract] = abstract_texto
            actualizados += 1
            print(f"  [+] {id_registro} - Actualizado")
        else:
            ya_tenian += 1
            # print(f"  [.] {id_registro} - Ya tenia contenido, se mantiene")

print("\n" + "=" * 60)
print("RESUMEN ACTUALIZACION")
print("=" * 60)
print(f"Abstracts nuevos insertados: {actualizados}")
print(f"Registros que ya tenian abstract: {ya_tenian}")
print(f"Total procesados del JSON: {len(abstracts)}")

# Guardar archivo actualizado
# Crear backup antes de guardar
backup_file = archivo.with_name(archivo.stem + ".backup" + archivo.suffix)
try:
    # Para guardar manteniendo la estructura, lo ideal es usar un motor de Excel
    # pero como leimos solo una hoja con header=2, el guardado simple de df.to_excel
    # podria perder el formato de las primeras 2 filas (instrucciones).
    
    # OPCION SEGURA: Guardamos el DataFrame actualizado en un archivo temporal primero
    df.to_excel(backup_file, sheet_name='SCREENING_SAMPLE', index=False)
    print(f"\nBackup/Temporal guardado en: {backup_file}")

    # Sobreescribimos el original con la tabla limpia (Nota: Esto limpia los encabezados de adorno)
    df.to_excel(archivo, sheet_name='SCREENING_SAMPLE', index=False)
    print(f"Archivo actualizado guardado en: {archivo}")
except Exception as e:
    print(f"Error al guardar: {e}")

# Mostrar resumen por ID final
print("\n" + "=" * 60)
print("DETALLE DE FUENTES")
print("=" * 60)

fuentes = {}
for id_reg, data in abstracts.items():
    f = data['fuente']
    fuentes[f] = fuentes.get(f, 0) + 1

for f, cant in fuentes.items():
    print(f"  - {f}: {cant} registros")
