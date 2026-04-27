import re
from typing import Tuple, List
import sys

# Forzar UTF-8
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class CSPGuardrail:
    """
    Validador de restricciones críticas para el manuscrito (Constraint Satisfaction Problem).
    Versión reforzada para detectar variaciones semánticas de errores comunes.
    """
    
    def __init__(self):
        self.config = {
            "n_total": 29,
            "n_primarios": 22,
            "n_reviews": 7,
            "pso_percent": 40.9, # 9 PSO de 22 primarios = 40.9%
            "prohibidos": [r"\bdrone\b", r"\bdrones\b"],
            # Unidades SI: número seguido de unidad (opcional espacio)
            "unidades_si": [r"\d+\s?m/s", r"\d+\s?kg", r"\d+\s?N", r"\d+\s?W", r"\d+\s?J", r"\d+\s?s\b", r"\d+\s?m\b"]
        }
    
    def validar(self, texto: str) -> Tuple[bool, List[str]]:
        violaciones = []
        
        # 1. Validar Tamaño de Muestra (Detectar valores obsoletos)
        patron_n_obsoleto = r"n\s?=\s?(23|26|30|31|32|33)\b"
        if re.search(patron_n_obsoleto, texto, re.IGNORECASE):
            valor = re.search(patron_n_obsoleto, texto, re.IGNORECASE).group()
            violaciones.append(f"❌ Error de Muestra Obsoleto: Valor '{valor}' detectado. Actualizar a 29 (total) o 22 (primarios).")
        
        # 2. Validar Estudios Primarios (n=22)
        if re.search(r"\b(23|26)\b\s?(primarios|estudios\sprimarios)", texto, re.IGNORECASE):
            violaciones.append(f"❌ Error de Clasificación: Se detectaron 23/26 primarios. El número actual es {self.config['n_primarios']}.")
            
        # 3. Validar Estadísticas de Algoritmos (PSO 40.9%)
        if "33.3%" in texto or "30.3%" in texto or "38.5%" in texto:
            violaciones.append(f"❌ Error Estadístico: Datos desactualizados. Ajustar PSO a {self.config['pso_percent']}% (9/22).")
            
        # 4. Validar Terminología Aeronáutica
        for patron in self.config["prohibidos"]:
            if re.search(patron, texto, re.IGNORECASE):
                # Ignorar si es parte de un DOI
                match = re.search(patron, texto, re.IGNORECASE)
                pre_text = texto[max(0, match.start()-10):match.start()]
                if "/" in pre_text or "doi" in pre_text.lower():
                    continue
                termino = match.group()
                violaciones.append(f"⚠️ Terminología: '{termino}' detectado. Reemplazar por 'RPAS' o 'UAV'.")
                break
                
        # 5. Validar Unidades SI (con soporte LaTeX)
        # Soporta: "10 kg", "12 m/s", "3.2\ \text{J}", etc.
        unidades_si_reforzado = [
            r"\d+\s?m/s", r"\d+\s?kg", r"\d+\s?N", r"\d+\s?W", 
            r"\d+(\.\d+)?\\?\s?(\\text\{)?J\}?", 
            r"\d+(\.\d+)?\\?\s?(\\text\{)?s\}?",
            r"\d+(\.\d+)?\\?\s?(\\text\{)?m\}?"
        ]
        if not any(re.search(u, texto) for u in unidades_si_reforzado):
            violaciones.append("📏 Falta Rigor: No se hallaron unidades SI normalizadas (ej: 10 kg, 3.2 J).")
            
        return len(violaciones) == 0, violaciones
            
        return len(violaciones) == 0, violaciones

if __name__ == "__main__":
    g = CSPGuardrail()
    test = "Se revisaron 33 trabajos incluyendo 26 primarios sobre drones."
    pasa, v = g.validar(test)
    print(f"Test simple: {'PASA' if pasa else 'FALLA'}")
    for item in v: print(f" - {item}")