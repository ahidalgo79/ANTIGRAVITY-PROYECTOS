import pandas as pd
import os
import fitz
import re
from datetime import datetime

# Rutas
ruta_excel = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
ruta_base = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\02_PAPERS_ORGANIZADOS'

# Papers problemáticos con nombres REALES de archivos
PAPERS_FIX = {
    'PAPER_023': ('Algoritmos_Otros', 'PAPER_023 - Research on Path Planning Method for Mob.pdf'),
    'PAPER_028': ('Algoritmos_PSO', 'PAPER_028 - UAV Path Planning Algorithm Based on Imp.pdf'),
    'PAPER_029': ('Algoritmos_PSO', 'PAPER_029 - Improved Particle Swarm Optimization Bas.pdf'),
    'PAPER_030': ('Algoritmos_PSO', 'PAPER_030 - Hybrid APF–PSO Algorithm for Regional Dy.pdf'),
    'PAPER_031': ('Algoritmos_Otros', 'PAPER_031 - Three-Dimensional Path Planning of UAV B.pdf'),
    'PAPER_034': ('Revisiones_Existentes', 'PAPER_034 - Swarm intelligence algorithms for multip.pdf'),
}

# Cargar Excel
df = pd.read_excel(ruta_excel, sheet_name='TODOS_PAPERS')

print(f"🔧 Reparando {len(PAPERS_FIX)} papers con abstracts vacíos...\n")

for paper_id, (carpeta, nombre_archivo) in PAPERS_FIX.items():
    # Buscar índice en DataFrame
    idx = df[df['ID'] == paper_id].index
    if len(idx) == 0:
        print(f"⚠️ {paper_id}: No encontrado en Excel")
        continue
    idx = idx[0]
    
    ruta_pdf = os.path.join(ruta_base, carpeta, nombre_archivo)
    
    if not os.path.exists(ruta_pdf):
        print(f"❌ {paper_id}: Archivo no existe: {nombre_archivo}")
        continue
    
    try:
        pdf_doc = fitz.open(ruta_pdf)
        
        # Extraer texto de primeras 5 páginas
        texto_completo = ""
        for p in range(min(5, len(pdf_doc))):
            texto_completo += pdf_doc[p].get_text()
        
        # Extraer abstract buscando "Abstract:"
        abstract = ""
        for keyword in ['Abstract:', 'ABSTRACT:']:
            if keyword in texto_completo:
                start = texto_completo.find(keyword)
                # Buscar fin: Keywords, Introduction, o 600 chars después
                end_keywords = texto_completo.find('Keywords:', start)
                end_intro = texto_completo.find('1. Introduction', start)
                end_default = start + 600
                
                end = min([x for x in [end_keywords, end_intro, end_default] if x > start], default=end_default)
                abstract = texto_completo[start:end].strip()[:600]
                break
        
        # Extraer DOI
        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', texto_completo)
        doi = doi_match.group() if doi_match else ""
        
        # Actualizar fila
        if abstract and len(abstract) > 30:
            df.at[idx, 'Abstract Resumido'] = abstract
            df.at[idx, 'Estado Lectura'] = 'Abstract extraído'
            print(f"✅ {paper_id}: Abstract ({len(abstract)} chars)")
        else:
            # Si no se encontró abstract, guardar primer párrafo como fallback
            first_para = texto_completo.split('\n\n')[0][:300] if '\n\n' in texto_completo else texto_completo[:300]
            df.at[idx, 'Abstract Resumido'] = f"[Fallback] {first_para}"
            df.at[idx, 'Estado Lectura'] = 'Abstract extraído (fallback)'
            print(f"⚠️ {paper_id}: Abstract fallback ({len(first_para)} chars)")
        
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