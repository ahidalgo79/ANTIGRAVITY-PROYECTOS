import os
import sys
import io
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel, Field
import operator
import json
from dotenv import load_dotenv

# Configurar la terminal para manejar UTF-8 (evita errores con emojis en Windows)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

# ============ ESTADO DEL AGENTE ============
class EstadoAgente(TypedDict):
    """Estado persistente del orquestador"""
    mensajes: Annotated[list, operator.add]
    tarea_actual: str
    resultados_parciales: dict
    iteracion: int
    errores: list

# ============ ESQUEMAS VALIDADOS ============
class TareaRedaccion(BaseModel):
    """Esquema validado para tareas de redacción"""
    seccion: str = Field(description="Sección del manuscrito a redactar")
    contexto: str = Field(description="Contexto específico")
    palabras_clave: list[str] = Field(default_factory=list)
    tono: str = Field(default="academico", description="academico, tecnico, ejecutivo")

class TareaAnalisis(BaseModel):
    """Esquema validado para tareas de análisis"""
    tipo: str = Field(description="kappa, estadistica, extraccion")
    datos: dict = Field(default_factory=dict)

# ============ NODOS DEL GRAFO ============
class OrquestadorAgentes:
    def __init__(self):
        self.modelos = self._inicializar_modelos()
        self.grafo = self._construir_grafo()
    
    def _inicializar_modelos(self):
        # Integración con tus modelos existentes
        from asistente_triple_final import AsistenteTriple
        return AsistenteTriple()
    
    def _construir_grafo(self):
        """Construye el grafo de decisión con LangGraph"""
        workflow = StateGraph(EstadoAgente)
        
        # Nodos
        workflow.add_node("analizar_intencion", self.analizar_intencion)
        workflow.add_node("seleccionar_agente", self.seleccionar_agente)
        workflow.add_node("ejecutar_tarea", self.ejecutar_tarea)
        workflow.add_node("validar_resultado", self.validar_resultado)
        workflow.add_node("refinar", self.refinar)
        
        # Flujo
        workflow.set_entry_point("analizar_intencion")
        workflow.add_edge("analizar_intencion", "seleccionar_agente")
        workflow.add_edge("seleccionar_agente", "ejecutar_tarea")
        workflow.add_edge("ejecutar_tarea", "validar_resultado")
        
        # Decisión condicional
        workflow.add_conditional_edges(
            "validar_resultado",
            self.decidir_siguiente,
            {
                "aceptar": END,
                "refinar": "refinar",
                "reintentar": "ejecutar_tarea"
            }
        )
        workflow.add_edge("refinar", "ejecutar_tarea")
        
        # Memoria persistente
        return workflow.compile(checkpointer=MemorySaver())
    
    def _call_model(self, model_name, prompt):
        """Llamada segura a los modelos con fallbacks"""
        if model_name == "gemini" and "gemini" in self.modelos.modelos:
            return self.modelos.gemini(prompt)
        elif model_name == "claude" and "claude" in self.modelos.modelos:
            return self.modelos.claude(prompt)
        elif model_name == "qwen" and "qwen" in self.modelos.modelos:
            return self.modelos.qwen(prompt)
        else:
            # Fallback automático
            if "claude" in self.modelos.modelos:
                return self.modelos.claude(prompt)
            elif "qwen" in self.modelos.modelos:
                return self.modelos.qwen(prompt)
            elif "gemini" in self.modelos.modelos:
                return self.modelos.gemini(prompt)
        return "Error: No hay modelos configurados"

    def analizar_intencion(self, estado: EstadoAgente):
        """Analiza la intención del usuario"""
        ultimo_mensaje = estado["mensajes"][-1].content
        
        prompt = f"""
        Analiza la siguiente solicitud y clasifica la tarea:
        
        Solicitud: {ultimo_mensaje}
        
        Responde SOLO con JSON:
        {{
            "tipo": "redaccion|analisis|codigo|extraccion",
            "complejidad": "baja|media|alta",
            "requiere_validacion": true/false
        }}
        """
        
        # Intentar con claude como fallback si gemini no está
        resultado = self._call_model("gemini", prompt)
        
        # Limpiar JSON de markdown si es necesario
        if "```json" in resultado:
            resultado = resultado.split("```json")[1].split("```")[0].strip()
        
        try:
            analisis = json.loads(resultado)
            return {
                "tarea_actual": analisis["tipo"],
                "resultados_parciales": {"analisis": analisis},
                "iteracion": estado.get("iteracion", 0) + 1
            }
        except:
            return {"tarea_actual": "redaccion"}
    
    def seleccionar_agente(self, estado: EstadoAgente):
        """Selecciona el mejor modelo según la tarea"""
        tarea = estado["tarea_actual"]
        
        mapa_modelos = {
            "redaccion": "claude",
            "analisis": "qwen",
            "codigo": "claude",
            "extraccion": "qwen"
        }
        
        modelo_seleccionado = mapa_modelos.get(tarea, "claude")
        
        # Verificar disponibilidad
        if modelo_seleccionado not in self.modelos.modelos:
            modelo_seleccionado = list(self.modelos.modelos.keys())[0] if self.modelos.modelos else "none"
        
        return {
            "resultados_parciales": {
                **estado.get("resultados_parciales", {}),
                "modelo_asignado": modelo_seleccionado
            }
        }
    
    def ejecutar_tarea(self, estado: EstadoAgente):
        """Ejecuta la tarea con el modelo seleccionado"""
        modelo = estado["resultados_parciales"]["modelo_asignado"]
        prompt = estado["mensajes"][-1].content
        
        respuesta = self._call_model(modelo, prompt)
        
        return {
            "resultados_parciales": {
                **estado["resultados_parciales"],
                "ultimo_resultado": respuesta
            }
        }
    
    def validar_resultado(self, estado: EstadoAgente):
        """Valida el resultado usando el modelo contrario"""
        resultado = estado["resultados_parciales"]["ultimo_resultado"]
        
        prompt_validacion = f"""
        Valida la calidad de este resultado académico:
        
        {resultado[:1000]}
        
        Puntúa del 1 al 10 en:
        1. Precisión técnica
        2. Calidad de redacción
        3. Coherencia con el contexto académico
        
        Responde SOLO con JSON: {{"puntaje": 0-10, "aceptar": true/false, "observaciones": ""}}
        """
        
        # Usar modelo diferente para validación cruzada
        modelo_actual = estado["resultados_parciales"]["modelo_asignado"]
        modelo_validador = "qwen" if modelo_actual == "claude" else "claude"
        
        validacion = self._call_model(modelo_validador, prompt_validacion)
        
        if "```json" in validacion:
            validacion = validacion.split("```json")[1].split("```")[0].strip()
        
        try:
            resultado_val = json.loads(validacion)
            return {
                "resultados_parciales": {
                    **estado["resultados_parciales"],
                    "validacion": resultado_val
                }
            }
        except:
            return {"resultados_parciales": estado["resultados_parciales"]}
    
    def decidir_siguiente(self, estado: EstadoAgente):
        """Decide si aceptar, refinar o reintentar"""
        validacion = estado["resultados_parciales"].get("validacion", {})
        iteracion = estado.get("iteracion", 0)
        
        if validacion.get("aceptar", False):
            return "aceptar"
        elif iteracion < 3:
            return "refinar"
        else:
            return "aceptar"  # Forzar aceptar después de 3 intentos
    
    def refinar(self, estado: EstadoAgente):
        """Refina el resultado basado en la validación"""
        resultado_anterior = estado["resultados_parciales"]["ultimo_resultado"]
        validacion = estado["resultados_parciales"].get("validacion", {})
        
        prompt_refinamiento = f"""
        Mejora el siguiente texto académico basado en la validación:
        
        TEXTO ORIGINAL:
        {resultado_anterior[:1500]}
        
        VALIDACION:
        - Puntaje: {validacion.get('puntaje', 5)}/10
        - Observaciones: {validacion.get('observaciones', 'Mejorar calidad')}
        
        Genera una versión mejorada manteniendo el contenido técnico pero mejorando la redacción.
        """
        
        # Usar Claude para refinamiento
        respuesta = self._call_model("claude", prompt_refinamiento)
        
        return {
            "resultados_parciales": {
                **estado["resultados_parciales"],
                "ultimo_resultado": respuesta,
                "refinado": True
            },
            "iteracion": estado.get("iteracion", 0) + 1
        }
    
    async def procesar(self, mensaje: str):
        """Procesa un mensaje a través del grafo"""
        config = {"configurable": {"thread_id": "1"}}
        estado_inicial = {
            "mensajes": [HumanMessage(content=mensaje)],
            "tarea_actual": "",
            "resultados_parciales": {},
            "iteracion": 0,
            "errores": []
        }
        
        resultado_final = await self.grafo.ainvoke(estado_inicial, config=config)
        return resultado_final

# ============ USO ============
async def main():
    orquestador = OrquestadorAgentes()
    
    print("\n" + "=" * 60)
    print("INICIANDO ORQUESTADOR DE AGENTES")
    print("=" * 60)
    
    consulta = "Redacta la sección de discusión para el manuscrito sobre algoritmos de enjambre en drones, destacando los principales hallazgos de los 30 estudios incluidos."
    
    resultado = await orquestador.procesar(consulta)
    
    print("\n[RESULTADO FINAL]:")
    print("-" * 60)
    print(resultado["resultados_parciales"]["ultimo_resultado"])
    print("-" * 60)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
