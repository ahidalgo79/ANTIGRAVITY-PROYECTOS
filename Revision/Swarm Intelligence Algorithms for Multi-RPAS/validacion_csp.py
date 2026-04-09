import re

class ValidadorNeurosimbólico:
    """ Validador básico para el orquestador (Versión Mock) """
    
    def __init__(self):
        self.reglas_criticas = [
            (r"\d+\s?(m/s|km/h|kg|Newton|Hz|vatios)", "Unidades SI detectadas y consistentes"),
            (r"RPAS|UAV|Drone|Multi-RPAS", "Nomenclatura de dominio correcta")
        ]

    def validar_manuscrito(self, texto):
        """ Valida la consistencia técnica básica """
        violaciones = []
        
        # 1. Verificar si hay números sin unidades después de hablar de parámetros físicos
        if re.search(r"velocidad de \d+(?!\s?(m/s|km/h))", texto.lower()):
            violaciones.append("Falta unidad en parámetro de velocidad")
            
        # 2. Verificar consistencia de citas RAG
        if "Fuente:" not in texto and len(texto) > 100:
             # Nota: No es una violación crítica, pero es una observación
             pass

        puntaje = 10 if not violaciones else 7
        aprobado = len(violaciones) == 0
        
        return {
            "aprobado": aprobado,
            "puntaje": puntaje,
            "violaciones": violaciones,
            "observaciones": "Validación simbólica básica completada."
        }
