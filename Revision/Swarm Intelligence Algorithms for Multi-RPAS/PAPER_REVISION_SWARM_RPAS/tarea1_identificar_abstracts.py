# tarea1_identificar_abstracts.py
import pandas as pd
import fitz
from pathlib import Path
from datetime import datetime
import json

print("=" * 60)
print("TAREA 1: IDENTIFICAR ABSTRACTS FALTANTES")
print("=" * 60)

# 1. Cargar archivo de validacion
archivo = Path("04_BIBLIOGRAFIA/Rescreening_TA_DrGarza.xlsx")
if not archivo.exists():
    print(f"Error: No se encuentra el archivo en {archivo}")
    exit()

# Leemos la hoja correcta y saltamos las filas de instrucciones (el encabezado real esta en la fila 3)
try:
    df = pd.read_excel(archivo, sheet_name='SCREENING_SAMPLE', header=2)
except Exception as e:
    print(f"Error al leer la hoja SCREENING_SAMPLE: {e}")
    exit()

print(f"\nArchivo cargado: {archivo.name}")
print(f"Total registros en tabla: {len(df)}")

# 2. Identificar columnas de interes
col_abstract = 'RESUMEN (extracto)'
col_titulo = 'TÍTULO'
col_id = 'ID Registro'

print(f"Columna de titulo: '{col_titulo}'")
print(f"Columna de abstract: '{col_abstract}'")

# 3. Contar abstracts vacios
# Quitamos filas que sean totalmente vacias
df = df.dropna(subset=[col_id])

# Normalizamos el abstract para detectar vacios (NaN o strings vacios)
df[col_abstract] = df[col_abstract].fillna('')
vacios = df[df[col_abstract].astype(str).str.strip() == '']
print(f"\nAbstracts vacios encontrados: {len(vacios)}")

if len(vacios) == 0:
    print("\nNo hay abstracts faltantes. Tarea completada.")
    exit()

# 5. Buscar PDFs disponibles
carpeta_pdfs = Path("02_PAPERS_ORGANIZADOS")
pdfs_disponibles = list(carpeta_pdfs.rglob("*.pdf"))
print(f"PDFs disponibles en carpeta: {len(pdfs_disponibles)}")

# 6. Verificar cuales abstracts se pueden extraer de PDFs
print("\n" + "=" * 60)
print("VERIFICANDO EXTRACCION DESDE PDFS (sin IA)")
print("=" * 60)

pueden_extraerse = []
no_encontrados = []

for idx, row in vacios.iterrows():
    titulo = str(row[col_titulo])
    id_registro = str(row.get('ID Registro', 'N/A'))
    pdf_encontrado = None
    
    # Buscar PDF por similitud en nombre
    for pdf in pdfs_disponibles:
        # Busqueda mas flexible: si el titulo esta en el nombre o viceversa
        if titulo.lower()[:50] in pdf.stem.lower() or pdf.stem.lower() in titulo.lower():
            pdf_encontrado = pdf
            break
    
    if pdf_encontrado:
        try:
            doc = fitz.open(pdf_encontrado)
            texto = ""
            for i in range(min(2, len(doc))):
                texto += doc[i].get_text()
            
            status = 'PDF encontrado sin seccion abstract'
            if "abstract" in texto.lower() or "resumen" in texto.lower():
                status = 'PDF encontrado con abstract'
                
            pueden_extraerse.append({
                'id': id_registro,
                'indice': int(idx),
                'titulo': titulo[:100],
                'pdf': str(pdf_encontrado.name),
                'status': status
            })
            doc.close()
        except Exception as e:
            pueden_extraerse.append({
                'id': id_registro,
                'indice': int(idx),
                'titulo': titulo[:100],
                'pdf': str(pdf_encontrado.name),
                'status': f'Error al leer: {str(e)[:50]}'
            })
    else:
        no_encontrados.append({
            'id': id_registro,
            'indice': int(idx),
            'titulo': titulo[:100],
            'status': 'PDF no encontrado localmente'
        })

# 7. Mostrar resultados
total_con_abstract = len([x for x in pueden_extraerse if 'con abstract' in x['status'].lower()])
print(f"\nRESULTADOS:")
print(f"  - PDFs con seccion abstract detectable: {total_con_abstract}")
print(f"  - PDFs encontrados pero incompletos: {len(pueden_extraerse) - total_con_abstract}")
print(f"  - Registros sin PDF encontrado: {len(no_encontrados)}")

if no_encontrados:
    print("\nREGISTROS SIN PDF (Requieren busqueda con Gemini/Web):")
    for item in no_encontrados:
        print(f"  - [{item['id']}] {item['titulo']}")

# 8. Guardar reporte
reporte = {
    'fecha': datetime.now().isoformat(),
    'total_vacios': len(vacios),
    'pdf_con_abstract': total_con_abstract,
    'pdf_no_encontrados': len(no_encontrados),
    'detalle_pdfs': pueden_extraerse,
    'detalle_no_encontrados': no_encontrados
}

with open('reporte_abstracts_faltantes.json', 'w', encoding='utf-8') as f:
    json.dump(reporte, f, ensure_ascii=False, indent=2)

print(f"\nReporte detallado guardado en: reporte_abstracts_faltantes.json")

