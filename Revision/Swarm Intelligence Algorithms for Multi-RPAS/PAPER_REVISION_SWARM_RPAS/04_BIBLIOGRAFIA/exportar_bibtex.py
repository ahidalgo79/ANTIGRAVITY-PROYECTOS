import pandas as pd
import re
import os
from datetime import datetime

# Rutas
ruta_excel = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
ruta_salida = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\04_BIBLIOGRAFIA'

# Crear carpeta de salida si no existe
os.makedirs(ruta_salida, exist_ok=True)

print("📚 Exportando referencias a formato BibTeX...\n")

# Cargar datos del Excel
df = pd.read_excel(ruta_excel, sheet_name='TODOS_PAPERS')

# Función para limpiar y formatear autores para BibTeX
def format_authors(authors_str):
    if pd.isna(authors_str) or authors_str == '':
        return 'Unknown'
    
    # Separar por comas o "and"
    authors = re.split(r',\s*| and |; ', str(authors_str))
    formatted = []
    
    for author in authors:
        author = author.strip()
        if not author:
            continue
        # Formato BibTeX: "Apellido, Nombre" o "Nombre Apellido"
        parts = author.split()
        if len(parts) >= 2:
            # Asumir último elemento es apellido
            lastname = parts[-1]
            firstname = ' '.join(parts[:-1])
            formatted.append(f"{lastname}, {firstname}")
        else:
            formatted.append(author)
    
    return ' and '.join(formatted) if formatted else 'Unknown'

# Función para generar clave BibTeX única
def generate_bibtex_key(paper_id, title, year):
    # Limpiar título: solo letras, números, espacios
    clean_title = re.sub(r'[^a-zA-Z0-9\s]', '', str(title))
    # Tomar primeras 3-4 palabras significativas
    words = [w.lower() for w in clean_title.split() if len(w) > 3]
    key_words = '_'.join(words[:3]) if words else 'paper'
    
    # Extraer año
    year_str = str(year) if pd.notna(year) else '2024'
    year_clean = re.search(r'\d{4}', year_str)
    year_clean = year_clean.group() if year_clean else '2024'
    
    # Extraer número de paper (001, 002, etc.)
    paper_num = re.search(r'\d+', str(paper_id))
    paper_num = paper_num.group() if paper_num else '000'
    
    return f"{key_words}_{year_clean}_{paper_num}"

# Función para determinar tipo de entrada BibTeX
def determine_entry_type(row):
    title = str(row.get('Título Completo', '')).lower()
    if 'review' in title or 'survey' in title:
        return 'article'  # Para reviews en journals
    elif 'conference' in title or 'proceedings' in title:
        return 'inproceedings'
    else:
        return 'article'  # Default para papers de journal

# Función para escapar caracteres especiales en BibTeX
def escape_bibtex(text):
    if pd.isna(text):
        return ''
    text = str(text)
    # Escapar caracteres especiales de BibTeX
    text = text.replace('&', r'\&')
    text = text.replace('%', r'\%')
    text = text.replace('$', r'\$')
    text = text.replace('#', r'\#')
    text = text.replace('_', r'\_')
    text = text.replace('{', r'\{')
    text = text.replace('}', r'\}')
    return text

# Lista para almacenar entradas BibTeX
bibtex_entries = []

print(f"Procesando {len(df)} papers...\n")

for idx, row in df.iterrows():
    paper_id = row.get('ID', f'PAPER_{idx+1:03d}')
    
    # Extraer campos
    title = escape_bibtex(row.get('Título Completo', 'Sin título'))
    authors = format_authors(row.get('Autores', ''))
    year = str(row.get('Año', '2024'))
    journal = escape_bibtex(row.get('Revista/Conferencia', 'Unknown Journal'))
    doi = row.get('DOI', '')
    url = row.get('URL', '')
    abstract = escape_bibtex(row.get('Abstract Resumido', ''))
    keywords = escape_bibtex(row.get('Palabras Clave', ''))
    
    # Generar clave BibTeX
    bibtex_key = generate_bibtex_key(paper_id, title, year)
    
    # Determinar tipo de entrada
    entry_type = determine_entry_type(row)
    
    # Construir entrada BibTeX
    entry = f"@{entry_type}{{{bibtex_key},\n"
    entry += f"  title        = {{{title}}},\n"
    entry += f"  author       = {{{authors}}},\n"
    entry += f"  year         = {{{year}}},\n"
    
    if pd.notna(journal) and journal != 'Unknown Journal':
        if entry_type == 'inproceedings':
            entry += f"  booktitle    = {{{journal}}},\n"
        else:
            entry += f"  journal      = {{{journal}}},\n"
    
    if pd.notna(doi) and doi != '':
        entry += f"  doi          = {{{doi}}},\n"
    
    if pd.notna(url) and url != '':
        entry += f"  url          = {{{url}}},\n"
    
    if pd.notna(abstract) and abstract != '':
        # Truncar abstract si es muy largo (>500 chars)
        abstract_short = abstract[:497] + '...' if len(abstract) > 500 else abstract
        entry += f"  abstract     = {{{abstract_short}}},\n"
    
    if pd.notna(keywords) and keywords != '':
        entry += f"  keywords     = {{{keywords}}},\n"
    
    # Agregar nota con ID original para referencia cruzada
    entry += f"  note         = {{Original ID: {paper_id}}},\n"
    
    entry += "}\n"
    
    bibtex_entries.append(entry)
    print(f"  ✅ {paper_id}: {bibtex_key}")

# Guardar archivo .bib
filename = os.path.join(ruta_salida, 'Referencias_Master.bib')
with open(filename, 'w', encoding='utf-8') as f:
    f.write("% ============================================================\n")
    f.write("% BIBLIOGRAFÍA MAESTRA - Swarm Intelligence for Multi-RPAS\n")
    f.write("% Generado automáticamente desde Fichas_Analisis_NUEVO.xlsx\n")
    f.write(f"% Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
    f.write("% Total de referencias: {}\n".format(len(bibtex_entries)))
    f.write("% ============================================================\n\n")
    
    for entry in bibtex_entries:
        f.write(entry)
        f.write("\n")

print(f"\n{'='*60}")
print(f"✅ EXPORTACIÓN COMPLETADA")
print(f"{'='*60}")
print(f"\nArchivo creado: {filename}")
print(f"Referencias exportadas: {len(bibtex_entries)}")
print(f"\nUso en LaTeX:")
print(f"  \\bibliography{{Referencias_Master}}")
print(f"  \\bibliographystyle{{ieeetr}}  % o plain, alpha, apalike, etc.")
print(f"\nUso en Word (con Zotero/Mendeley):")
print(f"  1. Abrir Referencias_Master.bib en el gestor de referencias")
print(f"  2. Importar a tu biblioteca personal")
print(f"  3. Insertar citas desde el plugin de Word")