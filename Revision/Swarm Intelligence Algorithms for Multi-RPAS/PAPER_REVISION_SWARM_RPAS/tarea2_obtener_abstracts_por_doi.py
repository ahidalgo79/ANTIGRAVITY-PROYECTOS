# tarea2_obtener_abstracts_por_doi.py
import pandas as pd
import requests
import json
import time
import re
from pathlib import Path
from datetime import datetime

print("=" * 60)
print("TAREA 2: OBTENER ABSTRACTS POR DOI")
print("=" * 60)

# Cargar el archivo Excel con la hoja correcta
archivo = Path("04_BIBLIOGRAFIA/Rescreening_TA_DrGarza.xlsx")
try:
    df = pd.read_excel(archivo, sheet_name='SCREENING_SAMPLE', header=2)
except Exception as e:
    print(f"Error al leer el archivo: {e}")
    exit()

print(f"\nArchivo cargado: {archivo.name}")
print(f"Total registros: {len(df)}")

# Identificar columnas exactas
col_titulo = 'TÍTULO'
col_abstract = 'RESUMEN (extracto)'
col_doi = 'DOI / URL'
col_id = 'ID Registro'

# Verificar que existan
for col in [col_titulo, col_abstract, col_doi, col_id]:
    if col not in df.columns:
        print(f"Error: No se encuentra la columna '{col}'")
        exit()

print(f"\nColumnas identificadas:")
print(f"  - ID: {col_id}")
print(f"  - Titulo: {col_titulo}")
print(f"  - DOI/URL: {col_doi}")
print(f"  - Abstract: {col_abstract}")

# Encontrar registros sin abstract
df[col_abstract] = df[col_abstract].fillna('')
vacios = df[df[col_abstract].astype(str).str.strip() == '']
print(f"\nRegistros sin abstract (vacios): {len(vacios)}")

if len(vacios) == 0:
    print("No hay abstracts faltantes. Tarea completada.")
    exit()

# Verificar cuales tienen DOI
con_doi = []
sin_doi = []

for idx, row in vacios.iterrows():
    doi_val = str(row[col_doi]) if pd.notna(row[col_doi]) else ""
    
    # Limpiar DOI (quitar URL si es necesario)
    if 'doi.org/' in doi_val:
        doi_val = doi_val.split('doi.org/')[-1]
    elif 'dx.doi.org/' in doi_val:
        doi_val = doi_val.split('dx.doi.org/')[-1]
    
    # Quitar posibles parametros de URL o espacios
    doi_val = doi_val.strip().split(' ')[0]
    
    if doi_val and doi_val != 'nan' and len(doi_val) > 5 and "/" in doi_val:
        con_doi.append({
            'indice': int(idx),
            'id': row[col_id],
            'titulo': row[col_titulo],
            'doi': doi_val.strip()
        })
    else:
        sin_doi.append({
            'indice': int(idx),
            'id': row[col_id],
            'titulo': row[col_titulo],
            'doi': None
        })

print(f"\nCon DOI valido para consulta: {len(con_doi)}")
print(f"Sin DOI (no se pueden consultar): {len(sin_doi)}")

# Funcion para obtener abstract de CrossRef
def obtener_abstract_crossref(doi):
    """Consulta CrossRef API y extrae el abstract"""
    try:
        url = f"https://api.crossref.org/works/{doi}"
        headers = {
            'User-Agent': 'ResearchAssistant/1.0 (mailto:revisor@swarm-agriculture.org)'
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            abstract = data.get('message', {}).get('abstract')
            
            if abstract:
                # Limpiar HTML si viene con etiquetas
                abstract_clean = re.sub('<[^<]+?>', '', abstract)
                # Quitar prefijtos comunes como "Abstract" o "Summary" al inicio
                abstract_clean = re.sub(r'^(Abstract|Summary|Background|Introduction|Objective|Methods|Results|Conclusions):\s*', '', abstract_clean, flags=re.IGNORECASE)
                return {'exito': True, 'abstract': abstract_clean.strip()}
            else:
                return {'exito': False, 'error': 'No tiene registro de abstract en CrossRef'}
        elif response.status_code == 404:
            return {'exito': False, 'error': 'DOI no encontrado en CrossRef'}
        else:
            return {'exito': False, 'error': f'HTTP {response.status_code}'}
            
    except Exception as e:
        return {'exito': False, 'error': str(e)[:100]}

# Procesar los DOIs
print("\n" + "=" * 60)
print("OBTENIENDO ABSTRACTS DESDE CROSSREF")
print("=" * 60)

resultados = []
checkpoint_file = "checkpoint_abstracts_doi.json"

# Verificar checkpoint
iniciar_desde = 0
if Path(checkpoint_file).exists():
    try:
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
            iniciar_desde = checkpoint.get('ultimo_procesado', 0)
            resultados = checkpoint.get('resultados', [])
            print(f"\nRetomando desde checkpoint: {iniciar_desde} DOIs ya procesados")
    except:
        print("\nError leyendo checkpoint, iniciando desde cero.")

# Procesar DOIs
for i, item in enumerate(con_doi):
    if i < iniciar_desde:
        continue
    
    print(f"\n[{i+1}/{len(con_doi)}] ID: {item['id']} | DOI: {item['doi'][:50]}...")
    
    resultado = obtener_abstract_crossref(item['doi'])
    
    res_entry = {
        'indice': item['indice'],
        'id': item['id'],
        'titulo': str(item['titulo'])[:100],
        'doi': item['doi'],
        'exito': resultado['exito'],
        'abstract': resultado.get('abstract', ''),
        'error': resultado.get('error', '')
    }
    resultados.append(res_entry)
    
    if resultado['exito']:
        print(f"  -> OK: Abstract obtenido ({len(resultado['abstract'])} caracteres)")
    else:
        print(f"  -> FAIL: {resultado['error']}")
    
    # Guardar checkpoint cada 5 DOIs
    if (i + 1) % 5 == 0:
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump({
                'ultimo_procesado': i + 1,
                'resultados': resultados
            }, f, ensure_ascii=False, indent=2)
        print(f"  [Checkpoint guardado]")
    
    # Pequeña pausa para ser amigables con la API
    time.sleep(1)

# Resumen de resultados
exitos = sum(1 for r in resultados if r['exito'])
fallos = len(resultados) - exitos

print("\n" + "=" * 60)
print("RESUMEN DE TAREA 2")
print("=" * 60)
print(f"DOIs consultados: {len(resultados)}")
print(f"Abstracts recuperados: {exitos}")
print(f"Abstracts no encontrados: {fallos}")

# Guardar resultados completos finales
with open('abstracts_obtenidos_doi.json', 'w', encoding='utf-8') as f:
    json.dump(resultados, f, ensure_ascii=False, indent=2)

print(f"\nResultados guardados en: abstracts_obtenidos_doi.json")

# Mostrar ejemplos de lo obtenido
if exitos > 0:
    print("\n" + "=" * 60)
    print("MUESTRA DE RESULTADOS")
    print("=" * 60)
    count = 0
    for r in resultados:
        if r['exito'] and count < 2:
            print(f"\n[{r['id']}] {r['titulo']}")
            print(f"Abstract: {r['abstract'][:250]}...")
            count += 1
