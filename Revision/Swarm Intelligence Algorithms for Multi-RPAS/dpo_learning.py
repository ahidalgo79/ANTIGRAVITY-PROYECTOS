import json
import hashlib
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from sentence_transformers import SentenceTransformer

class DPOLearningLoop:
    """Registra y alinea el comportamiento del agente mediante alineación semántica (DPO-style) e IDs únicos."""
    
    def __init__(self, ruta_registro: str = "dpo_feedback.json", model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.ruta = Path(ruta_registro)
        self.model_name = model_name
        self.embedder = SentenceTransformer(self.model_name)
        self.feedback: List[Dict] = []
        self._cargar()
    
    def _cargar(self):
        """Carga el historial de feedback"""
        if self.ruta.exists():
            try:
                with open(self.ruta, "r", encoding="utf-8") as f:
                    self.feedback = json.load(f)
                print(f"[DPO] {len(self.feedback)} ejemplos de aprendizaje cargados.")
            except Exception as e:
                print(f"[W] Error cargando DPO feedback: {e}")
                self.feedback = []
        else:
            self.feedback = []

    def _guardar(self):
        """Guarda el historial actualizado"""
        try:
            with open(self.ruta, "w", encoding="utf-8") as f:
                json.dump(self.feedback, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"[ERROR] No se pudo guardar DPO feedback: {e}")

    def registrar_feedback(self, prompt: str, rechazada: str, preferida: str, seccion: str = "general", motivo: str = "corrección manual"):
        """Registra un par Preferido vs Rechazado con ID único y métricas"""
        
        # Generar embedding del prompt original para búsquedas futuras
        embedding = self.embedder.encode(prompt).tolist()
        
        # Generar ID único usando hashlib
        id_unico = hashlib.md5(f"{prompt}{datetime.now()}".encode()).hexdigest()[:8]
        
        nuevo_item = {
            "id": id_unico,
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt,
            "seccion": seccion,
            "rechazada": rechazada,
            "preferida": preferida,
            "motivo": motivo,
            "diferencia_longitud": len(preferida) - len(rechazada),
            "embedding": embedding
        }
        
        self.feedback.append(nuevo_item)
        self._guardar()
        print(f"[DPO] Nuevo aprendizaje registrado (ID: {id_unico}): '{motivo}'")

    def alinear_prompt(self, prompt_actual: str, seccion_actual: str = None, k: int = 2) -> str:
        """Busca ejemplos semánticamente similares y los inyecta en el prompt"""
        
        if not self.feedback:
            return prompt_actual
            
        # 1. Calcular embedding del prompt actual
        emb_query = self.embedder.encode(prompt_actual)
        
        # 2. Calcular similitudes
        scores = []
        indices = []
        for i, item in enumerate(self.feedback):
            # Priorizar misma sección si se especifica
            weight = 1.2 if seccion_actual and item.get("seccion") == seccion_actual else 1.0
            
            emb_item = np.array(item["embedding"])
            sim = np.dot(emb_query, emb_item) / (np.linalg.norm(emb_query) * np.linalg.norm(emb_item))
            scores.append(sim * weight)
            indices.append(i)
            
        # 3. Obtener los K mejores
        idx_top = np.argsort(scores)[-k:][::-1]
        ejemplos_relevantes = [self.feedback[indices[i]] for i in idx_top if scores[i] > 0.6] # Umbral de relevancia
        
        if not ejemplos_relevantes:
            return prompt_actual
            
        # 4. Construir bloque de alineación
        bloque = "\n\n### INSTRUCCIONES DE ALINEACIÓN (Basadas en feedback previo):\n"
        bloque += "Sigue estos ejemplos de preferencias del usuario para tareas similares:\n"
        
        for i, ej in enumerate(ejemplos_relevantes):
            bloque += f"\nEjemplo {i+1} [ID: {ej['id']}]:\n"
            bloque += f"  - INPUT: {ej['prompt'][:100]}...\n"
            bloque += f"  - EVITAR (RECHAZADA): {ej['rechazada'][:150]}...\n"
            bloque += f"  - PREFERIR (CORREGIDA): {ej['preferida'][:150]}...\n"
            bloque += f"  - RAZÓN: {ej['motivo']}\n"
            
        bloque += "\nAplica el estilo y rigor de las versiones 'CORREGIDAS' en tu respuesta actual.\n"
        
        return prompt_actual + bloque

if __name__ == "__main__":
    dpo = DPOLearningLoop()
    p = "Comparativa de algoritmos de enjambre en drones"
    print(dpo.alinear_prompt(p))
