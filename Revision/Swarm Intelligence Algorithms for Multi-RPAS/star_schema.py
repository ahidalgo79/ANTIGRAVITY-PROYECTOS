import json
from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class FormulacionSTAR(BaseModel):
    """Esquema de razonamiento basado en Situation, Task, Action, Result"""
    situacion: str = Field(description="Contexto actual y hallazgos del RAG")
    tarea: str = Field(description="Lo que el usuario solicitó específicamente")
    accion: str = Field(description="Pasos de razonamiento para construir la respuesta")
    resultado_tecnico: str = Field(description="Resumen de los hallazgos técnicos antes de redactar")

class RespuestaValidada(BaseModel):
    """Respuesta final estructurada con razonamiento STAR"""
    razonamiento: FormulacionSTAR
    redaccion_final: str = Field(description="Texto académico final para el manuscrito")
    fuentes_usadas: List[str] = Field(default_factory=list, description="Lista de papers citados")

def prompt_star(consulta_usuario: str, contexto_rag: str = "", tipo: str = "redaccion") -> str:
    """Genera el prompt maestro siguiendo el patrón STAR"""
    
    instrucciones_tipo = {
        "redaccion": "Tu objetivo es producir un párrafo de alta calidad para un manuscrito de Elsevier.",
        "analisis": "Tu objetivo es identificar brechas y comparativas técnicas entre los papers.",
        "revision": "Tu objetivo es validar si el texto cumple con los estándares Prisma 2020."
    }
    
    prompt = f"""
    Eres un experto en investigación de Swarm Intelligence y Multi-RPAS.
    
    CONSULTA: {consulta_usuario}
    
    CONTEXTO BIBLIOGRÁFICO:
    {contexto_rag}
    
    {instrucciones_tipo.get(tipo, "")}
    
    DEBES responder siguiendo estrictamente la estructura STAR (Situation, Task, Action, Result) 
    para tu razonamiento interno antes de entregar la redacción final.
    
    FORMATO DE RESPUESTA (JSON):
    {{
        "razonamiento": {{
            "situacion": "Hallazgos clave detectados en el contexto RAG...",
            "tarea": "Objetivo de la redacción...",
            "accion": "Cómo integrarás las fuentes y la teoría...",
            "resultado_tecnico": "Puntos clave que incluirás..."
        }},
        "redaccion_final": "Tu texto académico completo aquí (en español)...",
        "fuentes_usadas": ["Autor1, 2021", "Autor2, 2022"]
    }}
    
    REGLAS:
    - Usa tono académico formal.
    - Cita siempre las fuentes entre paréntesis.
    - El JSON debe ser válido.
    """
    return prompt
