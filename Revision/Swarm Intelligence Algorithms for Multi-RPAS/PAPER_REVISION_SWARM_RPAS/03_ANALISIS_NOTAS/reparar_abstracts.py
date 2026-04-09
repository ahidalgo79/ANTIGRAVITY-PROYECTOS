import pandas as pd
import os
import fitz
import re
from datetime import datetime

# Rutas
ruta_excel = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
ruta_pdfs = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\02_PAPERS_ORGANIZADOS'

# Papers con abstracts vacíos
PAPERS_FALLIDOS = ['PAPER_023', 'PAPER_028', 'PAPER_029', 'PAPER_030', 'PAPER_031', 'PAPER_034']

# Mapeo de carpetas
MAPEO_CARPETAS = {
    'PAPER_023': 'Algoritmos_Otros', 'PAPER_028': 'Algoritmos_PSO',
    'PAPER_029': 'Algoritmos_PSO', 'PAPER_030': 'Algoritmos_PSO',
    'PAPER_031': 'Algoritmos_Otros', 'PAPER_034': 'Revisiones_Existentes',
}

# Cargar Excel
df = pd.read_excel(ruta_excel, sheet_name='TODOS_PAPERS')

print(f"🔧 Reparando {len(PAPERS_FALLIDOS)} papers con abstracts vacíos...\n")

for paper_id in PAPERS_FALLIDOS:
    carpeta = MAPEO_CARPETAS.get(paper_id)
    if not carpeta:
        print(f"⚠️ {paper_id}: Carpeta no mapeada")
        continue
    
    # Buscar índice en DataFrame
    idx = df[df['ID'] == paper_id].index
    if len(idx) == 0:
        print(f"⚠️ {paper_id}: No encontrado en Excel")
        continue
    idx = idx[0]
    
    # Buscar PDF
    ruta_carpeta = os.path.join(ruta_pdfs, carpeta)
    pdf_encontrado = None
    for pdf in os.listdir(ruta_carpeta):
        if pdf.startswith(paper_id) and pdf.endswith('.pdf'):
            pdf_encontrado = pdf
            break
    
    if not pdf_encontrado:
        print(f"⚠️ {paper_id}: PDF no encontrado")
        continue
    
    ruta_pdf = os.path.join(ruta_carpeta, pdf_encontrado)
    
    try:
        pdf_doc = fitz.open(ruta_pdf)
        
        # Extraer texto de primeras 5 páginas
        texto_completo = ""
        for p in range(min(5, len(pdf_doc))):
            texto_completo += pdf_doc[p].get_text()
        
        # Método 1: Buscar por "Abstract"
        abstract = ""
        for keyword in ['Abstract:', 'ABSTRACT:', 'abstract:']:
            if keyword in texto_completo:
                start = texto_completo.find(keyword)
                end = texto_completo.find('Keywords:', start)
                if end == -1:
                    end = texto_completo.find('1. Introduction', start)
                if end == -1:
                    end = start + 600
                abstract = texto_completo[start:end].strip()[:600]
                break
        
        # Método 2: Si no hay Abstract, buscar DOI y título
        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', texto_completo)
        doi = doi_match.group() if doi_match else ""
        
        # Actualizar fila
        if abstract:
            df.at[idx, 'Abstract Resumido'] = abstract
            df.at[idx, 'Estado Lectura'] = 'Abstract extraído'
            print(f"✅ {paper_id}: Abstract extraído ({len(abstract)} chars)")
        else:
            df.at[idx, 'Abstract Resumido'] = f"Abstract no detectado automáticamente. Revisar PDF: {pdf_encontrado}"
            df.at[idx, 'Estado Lectura'] = 'Requiere revisión manual'
            print(f"⚠️ {paper_id}: Abstract no detectado (requiere revisión manual)")
        
        if doi:
            df.at[idx, 'DOI'] = doi
            df.at[idx, 'URL'] = f"https://doi.org/{doi}"
        
        df.at[idx, 'Fecha Análisis'] = datetime.now().strftime('%Y-%m-%d')
        pdf_doc.close()
        
    except Exception as e:
        print(f"❌ {paper_id}: Error - {str(e)[:100]}")

# Guardar Excel
df.to_excel(ruta_excel, sheet_name='TODOS_PAPERS', index=False)

print(f"\n{'='*60}")
print(f"✅ PROCESO COMPLETADO")
print(f"{'='*60}")
print(f"Archivo guardado: {ruta_excel}")