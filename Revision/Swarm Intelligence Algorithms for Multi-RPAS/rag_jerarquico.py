import os
import sys
import io
import json
import pickle
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass, field

# Configurar la terminal para manejar UTF-8 (evita errores con emojis en Windows)
# Ahora esto solo se hace si el script se ejecuta directamente
if sys.platform == "win32" and __name__ == "__main__":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

if __name__ == "__main__":
    print("=" * 60)
    print("RAG JERARQUICO - INDICES ESPECIALIZADOS")
    print("=" * 60)

@dataclass
class IndiceRAG:
    """Estructura para cada índice jerárquico"""
    nombre: str
    descripcion: str
    chunks: List[str] = field(default_factory=list)
    metadata: List[Dict] = field(default_factory=list)
    index: Optional[faiss.Index] = None
    embedder: Optional[SentenceTransformer] = None

class RAGJerarquico:
    """
    Sistema RAG con 4 índices especializados:
    1. METADATOS: Dominio RPAS (navegación interior/exterior, tipos de drones)
    2. ESTRUCTURA: Secciones de papers (Metodología, Resultados, Discusión)
    3. CONTENIDO: Fragmentos precisos para búsqueda "needle-in-a-haystack"
    4. REGLAS: Normativas, ecuaciones, unidades SI
    """
    
    def __init__(self, modelo_embeddings: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        print(f"Cargando modelo de embeddings: {modelo_embeddings}...")
        self.embedder = SentenceTransformer(modelo_embeddings)
        self.indices = {
            "metadatos": IndiceRAG(
                nombre="metadatos",
                descripcion="Dominio RPAS: tipos de drones, escenarios, algoritmos principales"
            ),
            "estructura": IndiceRAG(
                nombre="estructura",
                descripcion="Secciones de papers: Metodologia, Resultados, Discusion"
            ),
            "contenido": IndiceRAG(
                nombre="contenido",
                descripcion="Fragmentos tecnicos precisos para recuperacion exacta"
            ),
            "reglas": IndiceRAG(
                nombre="reglas",
                descripcion="Ecuaciones matematicas, unidades SI, normativas"
            )
        }
    
    def clasificar_chunk(self, texto: str) -> str:
        """Clasifica automáticamente el chunk en el índice apropiado"""
        texto_lower = texto.lower()
        
        # Reglas para clasificación
        if any(p in texto_lower for p in ["ecuaci", "formula", "unidad", "si", "kg", "m/s", "newton", "distancia", "velocidad"]):
            return "reglas"
        elif any(p in texto_lower for p in ["metodolog", "experimento", "simulacion", "parametro", "dataset"]):
            return "estructura"
        elif any(p in texto_lower for p in ["drone", "uav", "rpas", "navegacion", "trayectoria", "multirotor", "vtol"]):
            return "metadatos"
        else:
            return "contenido"
    
    def indexar_paper(self, pdf_path: Path):
        """Indexa un paper en los 4 índices jerárquicos"""
        # Convertir a ruta absoluta con prefijo para rutas largas en Windows
        abs_path = os.path.abspath(pdf_path)
        if sys.platform == "win32" and not abs_path.startswith("\\\\?\\"):
            abs_path = "\\\\?\\" + abs_path
        
        print(f"\n[D] Indexando: {pdf_path.name}")
        
        try:
            # Extraer texto
            doc = fitz.open(abs_path)
            texto_completo = ""
            for page in doc:
                texto_completo += page.get_text()
            doc.close()
            
            if not texto_completo.strip():
                print(f"  [W] El archivo {pdf_path.name} parece no tener texto extraible.")
                return

            # Dividir en chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=50,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
            chunks = text_splitter.split_text(texto_completo)
            
            # Clasificar y agregar a índices
            for i, chunk in enumerate(chunks):
                tipo_indice = self.clasificar_chunk(chunk)
                indice = self.indices[tipo_indice]
                
                indice.chunks.append(chunk)
                indice.metadata.append({
                    "fuente": pdf_path.name,
                    "chunk_id": i,
                    "tipo": tipo_indice,
                    "pagina": i // 10  # aproximación
                })
            
            print(f"  [OK] {len(chunks)} chunks clasificados.")
        except Exception as e:
            print(f"  [ERROR] No se pudo procesar {pdf_path.name}: {e}")
    
    def construir_indices(self):
        """Construye índices FAISS para cada categoría"""
        print("\n" + "=" * 60)
        print("CONSTRUYENDO INDICES FAISS")
        print("=" * 60)
        
        for nombre, indice in self.indices.items():
            if not indice.chunks:
                print(f"\n[W] {nombre}: sin chunks para indexar")
                continue
            
            print(f"\n[I] Indexando {nombre} ({len(indice.chunks)} chunks)...")
            
            # Generar embeddings
            embeddings = self.embedder.encode(indice.chunks, show_progress_bar=True)
            
            # Crear índice FAISS
            dimension = embeddings.shape[1]
            indice.index = faiss.IndexFlatL2(dimension)
            indice.index.add(embeddings.astype('float32'))
            
            print(f"  [OK] Indice creado: {indice.index.ntotal} vectores")
    
    def buscar(self, consulta: str, top_k: int = 3, indices_especificos: List[str] = None) -> Dict[str, List[Dict]]:
        """Busca en índices específicos o en todos"""
        
        if indices_especificos is None:
            indices_especificos = list(self.indices.keys())
        
        consulta_embedding = self.embedder.encode([consulta])
        resultados = {}
        
        for nombre in indices_especificos:
            indice = self.indices[nombre]
            if not indice.index:
                continue
            
            distancias, indices = indice.index.search(consulta_embedding.astype('float32'), top_k)
            
            resultados[nombre] = []
            for i, idx in enumerate(indices[0]):
                if idx >= 0 and idx < len(indice.chunks):
                    resultados[nombre].append({
                        "texto": indice.chunks[idx],
                        "metadata": indice.metadata[idx],
                        "relevancia": float(1 / (1 + distancias[0][i]))
                    })
        
        return resultados
    
    def guardar(self, ruta_base: str = "indices_rag_jerarquico"):
        """Guarda todos los índices en disco"""
        ruta = Path(ruta_base)
        ruta.mkdir(exist_ok=True)
        
        for nombre, indice in self.indices.items():
            if indice.index:
                faiss.write_index(indice.index, str(ruta / f"{nombre}.faiss"))
            
            with open(ruta / f"{nombre}_datos.json", "w", encoding="utf-8") as f:
                json.dump({
                    "chunks": indice.chunks,
                    "metadata": indice.metadata,
                    "descripcion": indice.descripcion
                }, f, ensure_ascii=False, indent=2)
        
        print(f"\n[OK] Indices guardados en: {ruta_base}")
    
    def cargar(self, ruta_base: str = "indices_rag_jerarquico"):
        """Carga índices desde disco"""
        ruta = Path(ruta_base)
        
        for nombre, indice in self.indices.items():
            archivo_faiss = ruta / f"{nombre}.faiss"
            archivo_datos = ruta / f"{nombre}_datos.json"
            
            if archivo_faiss.exists() and archivo_datos.exists():
                indice.index = faiss.read_index(str(archivo_faiss))
                
                with open(archivo_datos, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    indice.chunks = data["chunks"]
                    indice.metadata = data["metadata"]
                
                print(f"[OK] {nombre}: {indice.index.ntotal} vectores cargados")

# ============ EJECUCION ============
if __name__ == "__main__":
    rag = RAGJerarquico()
    
    # Ruta ajustada a la estructura de carpetas encontrada
    carpeta_pdfs = Path("PAPER_REVISION_SWARM_RPAS/02_PAPERS_ORGANIZADOS")
    
    if not carpeta_pdfs.exists():
        print(f"[ERROR] No se encuentra la carpeta: {carpeta_pdfs}")
        # Intentar ruta relativa si no funciona la directa
        carpeta_pdfs = Path("02_PAPERS_ORGANIZADOS")
    
    pdfs = list(carpeta_pdfs.rglob("*.pdf"))
    
    print(f"\n[L] Papers encontrados: {len(pdfs)}")
    
    if not pdfs:
        print("[W] No hay PDFs para procesar en la ruta especificada.")
    else:
        for pdf in pdfs:
            # Para evitar errores con st_size en rutas largas (WinError 3)
            abs_path = os.path.abspath(pdf)
            if sys.platform == "win32" and not abs_path.startswith("\\\\?\\"):
                abs_path = "\\\\?\\" + abs_path
                
            try:
                if os.path.getsize(abs_path) > 0:  # Saltar PDFs rotos
                    rag.indexar_paper(pdf)
            except:
                print(f"  [W] Error al acceder a {pdf.name} (posible ruta demasiado larga)")
        
        # Construir índices
        rag.construir_indices()
        
        # Guardar
        rag.guardar()
        
        # Probar búsqueda
        print("\n" + "=" * 60)
        print("PRUEBA DE BUSQUEDA JERARQUICA")
        print("=" * 60)
        
        resultados = rag.buscar("algoritmos PSO para path planning de drones", top_k=2)
        
        for tipo, items in resultados.items():
            if items:
                print(f"\n[R] {tipo.upper()}:")
                for item in items:
                    # Limpiar texto para evitar errores de codificación en print
                    try:
                        print(f"   -> {item['texto'][:150]}...")
                        print(f"      (relevancia: {item['relevancia']:.3f})")
                    except:
                        print(f"   -> [Texto incompatible con codificacion de terminal]")
