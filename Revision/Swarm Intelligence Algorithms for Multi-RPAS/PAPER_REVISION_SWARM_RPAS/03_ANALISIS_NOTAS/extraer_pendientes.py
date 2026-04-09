import pandas as pd
import os
import fitz
import re
from datetime import datetime

# Rutas
ruta_excel = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
ruta_pdfs = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\02_PAPERS_ORGANIZADOS'

# Cargar Excel
df = pd.read_excel(ruta_excel, sheet_name='TODOS_PAPERS')

# Mapeo de carpetas por ID
MAPEO_CARPETAS = {
    'PAPER_021': 'Algoritmos_PSO', 'PAPER_022': 'Algoritmos_Otros',
    'PAPER_023': 'Algoritmos_Otros', 'PAPER_024': 'Algoritmos_PSO',
    'PAPER_025': 'Algoritmos_Otros', 'PAPER_026': 'Algoritmos_Otros',
    'PAPER_027': 'Algoritmos_Otros', 'PAPER_028': 'Algoritmos_PSO',
    'PAPER_029': 'Algoritmos_PSO', 'PAPER_030': 'Algoritmos_PSO',
    'PAPER_031': 'Algoritmos_Otros', 'PAPER_033': 'Revisiones_Existentes',
    'PAPER_034': 'Revisiones_Existentes',
}

# Filtrar pendientes
pendientes = df[df['Estado Lectura'] == 'Pendiente'].copy()
print(f"📋 Procesando {len(pendientes)} papers pendientes...\n")

for idx, row in pendientes.iterrows():
    paper_id = row['ID']
    carpeta = MAPEO_CARPETAS.get(paper_id)
    
    if not carpeta:
        print(f"⚠️ {paper_id}: Carpeta no mapeada")
        continue
    
    # Buscar PDF
    ruta_carpeta = os.path.join(ruta_pdfs, carpeta)
    pdf_encontrado = None
    for pdf in os.listdir(ruta_carpeta):
        if pdf.startswith(paper_id) and pdf.endswith('.pdf'):
            pdf_encontrado = pdf
            break
    
    if not pdf_encontrado:
        print(f"⚠️ {paper_id}: PDF no encontrado en {carpeta}")
        continue
    
    ruta_pdf = os.path.join(ruta_carpeta, pdf_encontrado)
    
    try:
        pdf_doc = fitz.open(ruta_pdf)
        metadata = pdf_doc.metadata
        texto_inicio = "".join([pdf_doc[p].get_text() for p in range(min(3, len(pdf_doc)))])
        texto_fin = "".join([pdf_doc[p].get_text() for p in range(max(0, len(pdf_doc)-3), len(pdf_doc))])
        
        # Extraer abstract
        abstract = ""
        if "Abstract:" in texto_inicio:
            start = texto_inicio.find("Abstract:")
            end = texto_inicio.find("Keywords:", start)
            if end == -1: end = start + 500
            abstract = texto_inicio[start:end].strip()[:500]
        
        # Extraer conclusiones
        conclusiones = ""
        if "Conclusion" in texto_fin:
            start = texto_fin.find("Conclusion")
            conclusiones = texto_fin[start:start+400].strip()
        
        # Extraer DOI
        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', texto_inicio)
        doi = doi_match.group() if doi_match else ""
        
        # Actualizar fila (usando str() para evitar errores con NaN)
        df.at[idx, 'Abstract Resumido'] = abstract if abstract else str(row.get('Abstract Resumido', ''))
        df.at[idx, 'Citar: Conclusiones'] = conclusiones[:200] if conclusiones else str(row.get('Citar: Conclusiones', ''))
        df.at[idx, 'DOI'] = doi if doi else str(row.get('DOI', ''))
        df.at[idx, 'URL'] = f"https://doi.org/{doi}" if doi else str(row.get('URL', ''))
        df.at[idx, 'Estado Lectura'] = 'Abstract extraído'
        df.at[idx, 'Fecha Análisis'] = datetime.now().strftime('%Y-%m-%d')
        df.at[idx, 'Notas Personales'] = f"Metadatos auto-extraídos desde {carpeta}"
        
        print(f"✅ {paper_id}: Abstract ({len(abstract)} chars) + DOI: {doi[:30] if doi else 'N/A'}...")
        pdf_doc.close()
        
    except Exception as e:
        print(f"❌ {paper_id}: Error - {str(e)[:100]}")

# Guardar Excel
df.to_excel(ruta_excel, sheet_name='TODOS_PAPERS', index=False)

# Actualizar estadísticas
analizados = len(df[df['Estado Lectura'] != 'Pendiente'])
total = len(df)
progreso = (analizados / total * 100) if total > 0 else 0

print(f"\n{'='*60}")
print(f"✅ PROCESO COMPLETADO")
print(f"{'='*60}")
print(f"Papers procesados: {len(pendientes)}")
print(f"Progreso actual: {analizados}/{total} ({progreso:.1f}%)")
print(f"Archivo guardado: {ruta_excel}")