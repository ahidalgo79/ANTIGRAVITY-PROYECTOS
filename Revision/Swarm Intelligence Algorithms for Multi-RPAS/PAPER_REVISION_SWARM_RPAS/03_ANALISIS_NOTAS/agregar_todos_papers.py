import pandas as pd
import os
import fitz
import re
from datetime import datetime

# Rutas
ruta_excel = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
ruta_pdfs = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\02_PAPERS_ORGANIZADOS'

# Cargar Excel existente
df = pd.read_excel(ruta_excel, sheet_name='TODOS_PAPERS')
ids_existentes = df['ID'].tolist()

# IDs faltantes
faltantes = ['PAPER_021', 'PAPER_022', 'PAPER_023', 'PAPER_024', 'PAPER_025', 
             'PAPER_026', 'PAPER_027', 'PAPER_028', 'PAPER_029', 'PAPER_030', 
             'PAPER_031', 'PAPER_033', 'PAPER_034']

# Mapeo de carpetas por algoritmo
MAPEO_CARPETAS = {
    'PAPER_021': 'Algoritmos_PSO',
    'PAPER_022': 'Algoritmos_Otros',
    'PAPER_023': 'Algoritmos_Otros',
    'PAPER_024': 'Algoritmos_PSO',
    'PAPER_025': 'Algoritmos_Otros',
    'PAPER_026': 'Algoritmos_Otros',
    'PAPER_027': 'Algoritmos_Otros',
    'PAPER_028': 'Algoritmos_PSO',
    'PAPER_029': 'Algoritmos_PSO',
    'PAPER_030': 'Algoritmos_PSO',
    'PAPER_031': 'Algoritmos_Otros',
    'PAPER_033': 'Revisiones_Existentes',
    'PAPER_034': 'Revisiones_Existentes',
}

# Mapeo de algoritmo principal por carpeta
ALGORITMO_POR_CARPETA = {
    'Algoritmos_PSO': 'PSO',
    'Algoritmos_ACO': 'ACO',
    'Algoritmos_Otros': 'Otro',
    'Revisiones_Existentes': 'Otro',
}

nuevas_filas = []

for paper_id in faltantes:
    carpeta = MAPEO_CARPETAS.get(paper_id, 'Algoritmos_Otros')
    ruta_carpeta = os.path.join(ruta_pdfs, carpeta)
    
    # Buscar PDF
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
        # Extraer metadatos del PDF
        pdf_doc = fitz.open(ruta_pdf)
        metadata = pdf_doc.metadata
        texto_primera_pagina = pdf_doc[0].get_text() if len(pdf_doc) > 0 else ""
        
        # Extraer título
        titulo = metadata.get('title', '')
        if not titulo and texto_primera_pagina:
            lines = texto_primera_pagina.split('\n')
            for line in lines[:20]:
                if len(line) > 30 and len(line) < 200:
                    titulo = line.strip()
                    break
        
        # Extraer año de fecha de creación
        ano = 2025
        if metadata.get('modDate'):
            match = re.search(r'D:(\d{4})', metadata.get('modDate', ''))
            if match:
                ano = int(match.group(1))
        
        # Extraer DOI del texto
        doi = ''
        doi_match = re.search(r'10\.\d{4,9}/[-._;()/:A-Z0-9]+', texto_primera_pagina)
        if doi_match:
            doi = doi_match.group()
        
        # Determinar algoritmo
        algoritmo = ALGORITMO_POR_CARPETA.get(carpeta, 'Otro')
        
        # Crear fila
        nueva_fila = {
            'ID': paper_id,
            'Título Completo': titulo[:200] if titulo else f'{paper_id} - Título no extraído',
            'Autores': metadata.get('author', 'No especificado'),
            'Año': ano,
            'Fuente': metadata.get('producer', 'No especificado'),
            'Tipo Publicación': 'Journal',
            'Factor Impacto': 'No especificado',
            'DOI': doi,
            'URL': f'https://doi.org/{doi}' if doi else '',
            'Base de Datos': 'Otro',
            'Citaciones': 0,
            'Algoritmo Principal': algoritmo,
            'Algoritmo Secundario': None,
            'Variante Específica': 'No especificada',
            'Aplicación Principal': 'Otro',
            'Aplicación Específica': 'Path planning para UAV/robots',
            'Tamaño Flota': 'No especificado',
            'Tipo Ambiente': 'No especificado',
            'Obstáculos': 'No especificado',
            'Métrica: Tiempo': 'No especificada',
            'Métrica: Energía': 'No especificada',
            'Métrica: Cobertura': 'No especificada',
            'Métrica: Convergencia': 'No especificada',
            'Complejidad Computacional': 'No especificada',
            'Validación': 'No especificada',
            'Entorno Simulación': 'No especificado',
            'Pruebas Reales': 'No especificado',
            'Tamaño Dataset': 'No aplica',
            'Ventajas Identificadas': 'Por revisar',
            'Limitaciones': 'Por revisar',
            'Comparación Con': 'No especificado',
            'Contribución Original': 'Por revisar',
            'Trabajo Futuro': 'Por revisar',
            'Relevancia': 'Media',
            'Sección Paper': 'Multiple',
            'Citación BibTeX': f'@article{{{paper_id.lower()}, title={{{titulo[:50]}}}, year={{{ano}}}}}',
            'Palabras Clave': metadata.get('keywords', 'No especificadas'),
            'Abstract Resumido': 'Por extraer',
            'Figuras Relevantes': 'No extraídas',
            'Citar: Introducción': 'Por extraer',
            'Citar: Metodología': 'Por extraer',
            'Citar: Análisis': 'Por extraer',
            'Citar: Conclusiones': 'Por extraer',
            'Estado Lectura': 'Pendiente',
            'Fecha Análisis': datetime.now().strftime('%Y-%m-%d'),
            'Notas Personales': f'Agregado automáticamente desde {carpeta}',
            'Conflictos/Dudas': 'Por revisar'
        }
        
        nuevas_filas.append(nueva_fila)
        print(f"✅ {paper_id}: {titulo[:60]}... ({ano})")
        
        pdf_doc.close()
        
    except Exception as e:
        print(f"❌ {paper_id}: Error - {str(e)}")

# Agregar todas las filas al DataFrame
if nuevas_filas:
    df_nuevos = pd.DataFrame(nuevas_filas)
    df = pd.concat([df, df_nuevos], ignore_index=True)
    
    # Guardar Excel
    df.to_excel(ruta_excel, sheet_name='TODOS_PAPERS', index=False)
    
    print(f"\n{'='*60}")
    print(f"✅ PROCESO COMPLETADO")
    print(f"{'='*60}")
    print(f"Papers agregados: {len(nuevas_filas)}")
    print(f"Total en Excel: {len(df)}")
    print(f"Archivo guardado: {ruta_excel}")
else:
    print("\n❌ No se agregaron papers")