import os
import sys
import io
import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass
from dotenv import load_dotenv

# Configurar la terminal para manejar UTF-8 (evita errores con emojis en Windows)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langsmith import Client

# Importar tu asistente triple
from asistente_triple_final import AsistenteTriple

# Importar el RAG jerárquico
from rag_jerarquico import RAGJerarquico

# Importar validador CSP completo
from csp_validator import CSPManuscrito

# Importar esquema STAR
from star_schema import prompt_star, FormulacionSTAR, RespuestaValidada

# Importar motor DPO
from dpo_learning import DPOLearningLoop

print("=" * 60)
print("ORQUESTADOR CON RAG JERARQUICO")
print("=" * 60)

class OrquestadorConRAG:
    """Orquestador con capacidades de búsqueda en papers"""
    
    def __init__(self):
        # Cargar asistentes
        self.asistente = AsistenteTriple()
        
        # Cargar RAG
        print("\n[RAG] Cargando índices RAG...")
        self.rag = RAGJerarquico()
        # Verificar si existe el índice, si no, lo cargará con advertencia
        self.rag.cargar("indices_rag_jerarquico")
        
        # Cargar validador CSP completo (Actualizado a n=30, Primarios=23 tras rescreening)
        self.validador = CSPManuscrito(target_n=30, target_primary=23, target_pso=10)
        
        # Cargar motor de aprendizaje DPO
        self.dpo = DPOLearningLoop()
        
        # Construir grafo
        self.grafo = self._construir_grafo()
        
        print("\n[OK] Orquestador listo")
    
    def _construir_grafo(self):
        """Construye el grafo de decisión con RAG integrado"""
        
        # El estado base debe ser TypedDict o dict con anotaciones para LangGraph
        workflow = StateGraph(dict)
        
        # Nodos
        workflow.add_node("analizar_intencion", self.analizar_intencion)
        workflow.add_node("buscar_en_papers", self.buscar_en_papers)
        workflow.add_node("generar_con_contexto", self.generar_con_contexto)
        workflow.add_node("validar_resultado", self.validar_resultado)
        workflow.add_node("refinar", self.refinar)
        
        # Flujo
        workflow.set_entry_point("analizar_intencion")
        workflow.add_edge("analizar_intencion", "buscar_en_papers")
        workflow.add_edge("buscar_en_papers", "generar_con_contexto")
        workflow.add_edge("generar_con_contexto", "validar_resultado")
        
        workflow.add_conditional_edges(
            "validar_resultado",
            self.decidir_siguiente,
            {
                "aceptar": END,
                "refinar": "refinar"
            }
        )
        workflow.add_edge("refinar", "generar_con_contexto")
        
        # Memoria persistente
        return workflow.compile(checkpointer=MemorySaver())
    
    def analizar_intencion(self, state: Dict) -> Dict:
        """Analiza la intención y determina qué índices RAG usar"""
        
        prompt = state.get("prompt", "")
        print(f"\n[AI] Analizando intención: {prompt[:50]}...")
        
        # Determinar qué índices buscar según tipo de consulta
        indices_relevantes = ["metadatos", "contenido", "reglas"]
        
        if any(p in prompt.lower() for p in ["metodolog", "experimento", "simulacion"]):
            indices_relevantes.append("estructura")
        
        return {
            "indices_busqueda": indices_relevantes,
            "top_k": 5,
            "mensajes": [{"role": "user", "content": prompt}]
        }
    
    def buscar_en_papers(self, state: Dict) -> Dict:
        """Busca información relevante en los papers indexados"""
        
        prompt = state.get("prompt", "")
        indices = state.get("indices_busqueda", ["metadatos", "contenido", "reglas"])
        top_k = state.get("top_k", 5)
        
        print(f"[RAG] Buscando en índices: {indices}")
        
        try:
            resultados = self.rag.buscar(prompt, top_k=top_k, indices_especificos=indices)
        except Exception as e:
            print(f"[ERROR] Busqueda RAG fallida: {e}")
            resultados = {}
        
        # Extraer texto relevante
        contexto_rag = []
        for tipo, items in resultados.items():
            if items:
                contexto_rag.append(f"\n=== {tipo.upper()} ===\n")
                for item in items[:3]:  # Top 3 por índice
                    contexto_rag.append(f"Fuente: {item['metadata'].get('fuente', 'desconocido')}")
                    contexto_rag.append(f"Texto: {item['texto'][:300]}...")
                    contexto_rag.append("")
        
        contexto_completo = "\n".join(contexto_rag) if contexto_rag else "No se encontraron resultados relevantes en los papers."
        
        return {
            "contexto_rag": contexto_completo,
            "resultados_busqueda": resultados
        }
    
    def generar_prompt_star(self, consulta: str, contexto_rag: str) -> str:
        """Genera prompt con estructura STAR obligatoria (Ingeniería RPAS)"""
        return f"""
        ACTÚA COMO UN INGENIERO DE SISTEMAS AEROESPACIALES ESPECIALIZADO EN RPAS.
        
        TAREA A REALIZAR: {consulta}
        
        CONTEXTO DE LOS PAPERS INDEXADOS:
        {contexto_rag}
        
        ================================================
        INSTRUCCIÓN OBLIGATORIA: ESTRUCTURA STAR (RAZONAMIENTO CIENTÍFICO)
        ================================================
        
        ANTES DE ESCRIBIR TU RESPUESTA FINAL, DEBES DESGLOSAR TU RAZONAMIENTO EN ESTAS 4 SECCIONES:
        
        [SITUATION]
        Describe el contexto técnico actual en el campo de swarm intelligence para RPAS.
        ¿Qué problema se aborda? ¿Cuál es el estado del arte según los papers recuperados?
        
        [TASK]
        Define el objetivo específico de esta sección del manuscrito.
        ¿Qué restricciones técnicas o metodológicas (n=30, PRISMA) deben considerarse?
        
        [ACTION]
        Formula las ecuaciones relevantes en formato LaTeX si corresponde.
        Describe la metodología paso a paso que se utilizará.
        ¿Qué algoritmos específicos (PSO, ACO, etc.) son relevantes?
        
        [RESULT]
        ¿Qué resultado se espera presentar?
        Especifica UNIDADES SI (m/s, kg, N, W, Pa, etc.) obligatoriamente.
        ¿Qué métricas cuantitativas se utilizarán?
        
        ================================================
        DESPUÉS DE COMPLETAR EL ANÁLISIS STAR, ESCRIBE TU RESPUESTA FINAL
        ================================================
        
        IMPORTANTE: LA RESPUESTA FINAL DEBE ESTAR EN FORMATO ACADÉMICO PARA ELSEVIER.
        
        RESPUESTA FINAL:
        """

    def generar_con_contexto(self, state: Dict) -> Dict:
        """Genera respuesta usando Claude con contexto RAG y estructura STAR"""
        
        prompt = state.get("prompt", "")
        contexto = state.get("contexto_rag", "")
        
        print(f"[GEN] Generando respuesta con Claude (Estructura STAR)...")
        
        # Usar la nueva función de prompt STAR integrada
        prompt_star_base = self.generar_prompt_star(prompt, contexto)
        
        # Alinear con feedback histórico (DPO)
        prompt_completo = self.dpo.alinear_prompt(prompt_star_base)
        
        # Usar Claude para redacción
        respuesta_cruda = self.asistente.claude(prompt_completo)
        
        # Procesar y validar respuesta STAR
        try:
            # Extraer JSON de la respuesta
            if "```json" in respuesta_cruda:
                json_str = respuesta_cruda.split("```json")[1].split("```")[0].strip()
            else:
                json_str = respuesta_cruda.strip()
            
            datos = json.loads(json_str)
            star = RespuestaValidada(**datos)
            
            respuesta_final = star.redaccion_final
            razonamiento = star.razonamiento.dict()
            fuentes = star.fuentes_usadas
        except Exception as e:
            print(f"[W] Error al parsear STAR JSON: {e}. Usando texto crudo como respaldo.")
            respuesta_final = respuesta_cruda
            razonamiento = {"error": "JSON no válido", "crudo": respuesta_cruda[:200]}
            fuentes = []
        
        # Mostrar avance en tiempo real
        print(f"\n[OK] Claude generó redacción de {len(respuesta_final)} caracteres.")
        print("-" * 30)
        print(f"RAZONAMIENTO STAR (Resumen): {razonamiento.get('resultado_tecnico', 'N/A')}")
        print("-" * 30)
        
        return {
            "respuesta_generada": respuesta_final,
            "razonamiento_star": razonamiento,
            "fuentes_usadas": fuentes,
            "modelo_usado": "claude-sonnet-4-6-star"
        }
    
    def validar_resultado(self, state: Dict) -> Dict:
        """Valida el resultado con Qwen y el motor CSP"""
        
        respuesta = state.get("respuesta_generada", "")
        print(f"[VAL] Validando resultado con motor CSP...")
        
        # 1. Validación CSP (Simbólica/Lógica)
        informe_csp = self.validador.resolver(respuesta)
        violaciones_csp = informe_csp["violaciones"]
        
        # 2. Validación con Qwen (Redacción/Calidad)
        prompt_validacion = f"""
        Evalúa la calidad académica de este texto:
        
        TEXTO: {respuesta[:1500]}
        
        Criterios:
        1. Precisión técnica (0-10)
        2. Claridad lingüística (0-10)
        3. Adecuación Elsevier (0-10)
        
        Responde SOLO con JSON: {{"precision": 0-10, "claridad": 0-10, "adecuacion": 0-10}}
        """
        
        try:
            validacion_qwen = self.asistente.qwen(prompt_validacion)
            # Limpiar markdown
            if "```json" in validacion_qwen:
                validacion_qwen = validacion_qwen.split("```json")[1].split("```")[0].strip()
            
            metricas = json.loads(validacion_qwen)
            puntaje_qwen = sum(metricas.values()) / 3
        except Exception as e:
            print(f"[W] Error en validación Qwen: {e}")
            puntaje_qwen = 7.0
            metricas = {"error": str(e)}
        
        # 3. Decisión Final Multi-Criterio
        # Aprobada si puntaje Qwen >= 7 y no hay violaciones críticas de CSP
        aprobada = puntaje_qwen >= 7.0 and len(violaciones_csp) == 0
        
        print(f"      Puntaje Qwen: {puntaje_qwen:.1f} | Violaciones CSP: {len(violaciones_csp)}")
        if violaciones_csp:
            for v in violaciones_csp: print(f"      [!] {v}")
            
        return {
            "aprobada": aprobada,
            "puntaje": puntaje_qwen,
            "metricas": metricas,
            "informe_csp": informe_csp,
            "respuesta_generada": respuesta # Preservar
        }
    
    def decidir_siguiente(self, state: Dict) -> str:
        """Decide si aceptar o refinar"""
        
        if state.get("aprobada", False):
            return "aceptar"
        else:
            return "refinar"
    
    def refinar(self, state: Dict) -> Dict:
        """Refina la respuesta basado en validación"""
        
        respuesta_actual = state.get("respuesta_generada", "")
        metricas = state.get("metricas", {})
        informe_csp = state.get("informe_csp", {})
        
        print(f"[REF] Refinando respuesta basada en observaciones...")
        
        prompt_refinamiento = f"""
        Mejora el siguiente texto académico basado en la evaluación:
        
        TEXTO ACTUAL:
        {respuesta_actual[:1500]}
        
        EVALUACIÓN:
        - Precisión técnica: {metricas.get('precision', 7)}/10
        - Claridad: {metricas.get('claridad', 7)}/10
        
        VIOLACIONES DETECTADAS O SUGERENCIAS:
        {informe_csp.get('violaciones', [])}
        
        Genera una versión mejorada manteniendo el contenido técnico pero corrigiendo las posibles inconsistencias de unidades y mejorando la fluidez académica.
        """
        
        respuesta_refinada = self.asistente.claude(prompt_refinamiento)
        
        return {
            "respuesta_generada": respuesta_refinada,
            "refinado": True
        }
    
    async def procesar(self, prompt: str) -> Dict:
        """Procesa una consulta a través del grafo"""
        
        # Configuración requerid para MemorySaver en LangGraph nuevo
        config = {"configurable": {"thread_id": "rpas_review_1"}}
        
        estado_inicial = {
            "prompt": prompt,
            "indices_busqueda": [],
            "top_k": 5,
            "mensajes": [],
            "respuesta_generada": "",
            "aprobada": False,
            "refinado": False
        }
        
        # Invocar el grafo
        await self.grafo.ainvoke(estado_inicial, config=config)
        
        # Recuperar el estado final real desde el checkpointer
        estado_final = self.grafo.get_state(config).values
        
        return {
            "respuesta": estado_final.get("respuesta_generada", ""),
            "aprobada": estado_final.get("aprobada", False),
            "puntaje": estado_final.get("puntaje", 0),
            "modelo_usado": estado_final.get("modelo_usado", "claude")
        }

# ============ PRUEBA ============
async def main():
    orquestador = OrquestadorConRAG()
    
    print("\n" + "=" * 60)
    print("PRUEBA DEL ORQUESTADOR CON RAG JERARQUICO DE PAPERS")
    print("=" * 60)
    
    consulta = """
    Redacta un párrafo para la sección de Resultados del manuscrito
    sobre los algoritmos de enjambre (Swarm Intelligence) más utilizados (ej. PSO, ACO)
    para el problema de path planning en drones basado en los papers indexados.
    Destaca los hallazgos principales de los estudios revisados.
    """
    
    resultado = await orquestador.procesar(consulta)
    
    print("\n" + "=" * 60)
    print("MUESTRA DE RESPUESTA FINAL:")
    print("=" * 60)
    if resultado["respuesta"]:
        print(resultado["respuesta"])
    else:
        print("[AVISO] La respuesta generada está vacía. Verifica la conexión con Claude.")
    
    print("-" * 60)
    sys.stdout.flush() # Forzar que el texto aparezca en la terminal
    
    print(f"\n[SUMARIO]")
    print(f"✅ Aprobada: {resultado['aprobada']}")
    print(f"📊 Puntaje Validador: {resultado['puntaje']:.1f}/10")
    print(f"🤖 Orquestador: Sistema RPAS (March 2026)")
    sys.stdout.flush()

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except EOFError:
        # Manejar posibles errores de stdin en terminales no interactivas
        pass
