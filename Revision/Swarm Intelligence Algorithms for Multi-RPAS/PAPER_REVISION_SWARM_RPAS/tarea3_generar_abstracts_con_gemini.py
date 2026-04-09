# tarea3_generar_abstracts_con_gemini.py
import os
import pandas as pd
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("=" * 60)
print("TAREA 3: GENERAR ABSTRACTS CON GEMINI 2.5 FLASH")
print("=" * 60)

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# Usamos el nombre verificado en el diagnostico
model = genai.GenerativeModel('gemini-2.5-flash')

# Cargar el archivo Excel
archivo = Path("04_BIBLIOGRAFIA/Rescreening_TA_DrGarza.xlsx")
try:
    df = pd.read_excel(archivo, sheet_name='SCREENING_SAMPLE', header=2)
except Exception as e:
    print(f"Error al leer el archivo Excel: {e}")
    exit()

print(f"\nArchivo cargado: {archivo.name}")
print(f"Total registros en tabla: {len(df)}")

# Identificar columnas
col_titulo = 'TÍTULO'
col_abstract = 'RESUMEN (extracto)'
col_doi = 'DOI / URL'
col_id = 'ID Registro'

# Cargar abstracts ya obtenidos de CrossRef (Tarea 2)
abstracts_existentes = {}
if Path("abstracts_obtenidos_doi.json").exists():
    try:
        with open("abstracts_obtenidos_doi.json", 'r', encoding='utf-8') as f:
            datos_crossref = json.load(f)
            for item in datos_crossref:
                if item.get('exito') and item.get('abstract'):
                    abstracts_existentes[item['id']] = item['abstract']
        print(f"\nAbstracts ya obtenidos via CrossRef: {len(abstracts_existentes)}")
    except:
        print("\nError leyendo abstracts_obtenidos_doi.json, se ignoraran.")

# Encontrar registros sin abstract
df[col_abstract] = df[col_abstract].fillna('')
vacios = df[df[col_abstract].astype(str).str.strip() == '']
print(f"Registros sin abstract en Excel: {len(vacios)}")

# Filtrar los que ya tenemos via CrossRef
pendientes = []
for idx, row in vacios.iterrows():
    id_registro = row[col_id]
    if id_registro not in abstracts_existentes:
        pendientes.append({
            'indice': int(idx),
            'id': id_registro,
            'titulo': row[col_titulo],
            'doi': row[col_doi] if pd.notna(row[col_doi]) else ''
        })

print(f"Abstracts pendientes de generar con Gemini: {len(pendientes)}")

if len(pendientes) == 0:
    print("\nNo hay abstracts pendientes. Tarea completada.")
    exit()

# Checkpoint para no perder progreso
checkpoint_file = "checkpoint_gemini_abstracts.json"
resultados_generados = {}

if Path(checkpoint_file).exists():
    try:
        with open(checkpoint_file, 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
            resultados_generados = checkpoint.get('generados', {})
            print(f"\nRetomando desde checkpoint: {len(resultados_generados)} ya generados")
    except:
        print("\nCheckpoint corrupto, iniciando desde cero.")

# Funcion para generar abstract con Gemini
def generar_abstract_con_gemini(titulo, doi=None):
    """Genera un abstract academico usando Gemini"""
    
    contexto = f"Titulo: {titulo}"
    if doi and doi != 'nan' and len(str(doi)) > 5:
        contexto += f"\nDOI/URL: {doi}"
    
    prompt = f"""
    Eres un experto en drones y agricultura de precision. 
    Escribe un abstract academico en espanol para el siguiente paper cientifico:
    
    {contexto}
    
    Requisitos del abstract:
    - Lenguaje academico formal y preciso.
    - Idioma: Espanol.
    - Estructura: Contexto breve, objetivo del estudio, metodologia (especifica algoritmo swarm si aplica), resultados y conclusion.
    - Longitud: 150 a 250 palabras.
    
    IMPORTANTE: Genera UNICAMENTE el texto del abstract. No incluyas titulos como 'Abstract:' o introducciones.
    """
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # Limpiar posibles prefijos que el modelo agregue a veces
        text = re.sub(r'^(Abstract|Resumen|Resumen Ejecutivo|Sintesis):\s*', '', text, flags=re.IGNORECASE)
        return {'exito': True, 'abstract': text}
    except Exception as e:
        return {'exito': False, 'error': str(e)[:100]}

# Procesar pendientes
import re
print("\n" + "=" * 60)
print("GENERANDO ABSTRACTS CON GEMINI")
print("=" * 60)

for i, item in enumerate(pendientes):
    id_registro = item['id']
    
    # Saltar si ya se genero en checkpoint
    if id_registro in resultados_generados:
        continue
    
    print(f"\n[{i+1}/{len(pendientes)}] {id_registro}: {item['titulo'][:60]}...")
    
    resultado = generar_abstract_con_gemini(item['titulo'], item['doi'])
    
    if resultado['exito']:
        resultados_generados[id_registro] = {
            'titulo': item['titulo'],
            'abstract': resultado['abstract'],
            'generado_en': time.strftime("%Y-%m-%d %H:%M:%S")
        }
        print(f"  -> OK: Abstract generado ({len(resultado['abstract'])} caracteres)")
    else:
        print(f"  -> FAIL: {resultado['error']}")
        # No guardamos el error en el diccionario final para permitir reintentos, 
        # pero si lo guardamos en el checkpoint si quieres
    
    # Guardar checkpoint cada 3 registros
    if (i + 1) % 3 == 0:
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump({
                'generados': resultados_generados,
                'ultimo_procesado': i + 1
            }, f, ensure_ascii=False, indent=2)
        print(f"  [Checkpoint guardado]")
    
    # Pausa entre llamadas
    time.sleep(2)

# Guardar consolidado final
print("\n" + "=" * 60)
print("CONSOLIDANDO RESULTADOS FINALES")
print("=" * 60)

consolidado = {}

# 1. Agregar abstracts de CrossRef
for id_reg, abstract in abstracts_existentes.items():
    consolidado[id_reg] = {
        'fuente': 'CrossRef API',
        'abstract': abstract
    }

# 2. Agregar abstracts de Gemini
for id_reg, data in resultados_generados.items():
    if id_reg not in consolidado:
        consolidado[id_reg] = {
            'fuente': 'Gemini 2.5 Flash',
            'abstract': data['abstract']
        }

with open('todos_los_abstracts_consolidado.json', 'w', encoding='utf-8') as f:
    json.dump(consolidado, f, ensure_ascii=False, indent=2)

# Finalizar reporte final
with open(checkpoint_file, 'w', encoding='utf-8') as f:
    json.dump({
        'generados': resultados_generados,
        'completado': True,
        'fecha': time.strftime("%Y-%m-%d %H:%M:%S")
    }, f, ensure_ascii=False, indent=2)

print(f"Tarea completada.")
print(f"Abstracts en consolidado: {len(consolidado)}")
print(f"Consolidado guardado en: todos_los_abstracts_consolidado.json")
