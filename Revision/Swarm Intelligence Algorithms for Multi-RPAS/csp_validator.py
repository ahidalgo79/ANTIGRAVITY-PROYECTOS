import re
from typing import List, Dict, Any, Callable

class CSPManuscrito:
    """Trata el manuscrito como Problema de Satisfacción de Restricciones (Neuro-Simbólico)"""
    
    def __init__(self, target_n=30, target_primary=23, target_pso=10):
        # Objetivos de la revisión sistemática (PRISMA) - Actualizados a n=30 (30-MAR-2026)
        self.targets = {
            "n_total": target_n,
            "n_primarios": target_primary,
            "n_pso": target_pso,
            "pct_pso": round((target_pso / target_n) * 100, 1)
        }
        
    def extraer_datos(self, texto: str) -> Dict[str, Any]:
        """Extrae parámetros numéricos del texto usando Regex"""
        datos = {}
        
        # 1. Total de estudios (N=XX o XX studies)
        match_n = re.search(r"(?:n\s?=\s?|(\d+)\s+studies)", texto.lower())
        datos["n_total"] = int(match_n.group(1)) if match_n and match_n.group(1) else None
        if not datos["n_total"]:
            # Intento alternativo
            match_n_alt = re.search(r"(\d+)\s+studies", texto.lower())
            datos["n_total"] = int(match_n_alt.group(1)) if match_n_alt else None

        # 2. Estudios primarios
        match_prim = re.search(r"(\d+)\s+primary\s+(?:research\s+)?articles", texto.lower())
        datos["n_primarios"] = int(match_prim.group(1)) if match_prim else None

        # 3. Estudios PSO
        match_pso = re.search(r"particle swarm(?:\s+optimis[a-z]+)?\s+dominates\s+\((\d+)", texto.lower())
        datos["n_pso"] = int(match_pso.group(1)) if match_pso else None

        # 4. Porcentaje reportado
        match_pct = re.search(r"(\d+\.?\d*)\%", texto)
        datos["pct_reportado"] = float(match_pct.group(1)) if match_pct else None
        
        return datos

    def validar_unidades(self, texto: str) -> List[str]:
        """Valida que los valores físicos tengan unidades SI"""
        violaciones = []
        # Buscar números seguidos de palabras clave de parámetros sin unidades
        # Ejemplo: "velocidad de 25" -> ERROR. "velocidad de 25 m/s" -> OK.
        patrones = [
            (r"velocidad de\s+(\d+(?!\s?(m/s|km/h)))", "Falta unidad de m/s en velocidad"),
            (r"energy\s+(?:of\s+)?(\d+(?!\s?(J|kJ|W|Wh)))", "Falta unidad de energía (J/W)"),
            (r"time\s+(?:of\s+)?(\d+(?!\s?(s|min|h|ms)))", "Falta unidad de tiempo (s/ms)"),
            (r"altitude\s+(?:of\s+)?(\d+(?!\s?(m|km)))", "Falta unidad de altitud (m)")
        ]
        
        for patron, error in patrones:
            if re.search(patron, texto.lower()):
                violaciones.append(error)
        return violaciones

    def validar_consistencia(self, datos: Dict) -> List[str]:
        """Verifica la consistencia lógica de los datos extraídos"""
        violaciones = []
        
        if datos.get("n_total") and datos.get("n_primarios"):
            # Regla: Los primarios no pueden ser más que el total
            if datos["n_primarios"] > datos["n_total"]:
                violaciones.append(f"Inconsistencia: N_primarios ({datos['n_primarios']}) > N_total ({datos['n_total']})")
        
        if datos.get("n_total") and datos.get("n_pso") and datos.get("pct_reportado"):
            pct_calculado = round((datos["n_pso"] / datos["n_total"]) * 100, 1)
            if abs(pct_calculado - datos["pct_reportado"]) > 0.5:
                violaciones.append(f"Error de cálculo: {datos['n_pso']}/{datos['n_total']} es {pct_calculado}%, pero se reportó {datos['pct_reportado']}%")
        
        return violaciones

    def resolver(self, texto: str) -> Dict:
        """Aplica todas las restricciones sobre el texto"""
        datos = self.extraer_datos(texto)
        violaciones = []
        
        # 1. Validar contra objetivos (Targets)
        if datos.get("n_total") and datos["n_total"] != self.targets["n_total"]:
            violaciones.append(f"Objetivo incumplido: N total es {datos['n_total']}, se esperaba {self.targets['n_total']}.")
            
        # 2. Validar Unidades
        violaciones.extend(self.validar_unidades(texto))
        
        # 3. Validar Consistencia Interna
        violaciones.extend(self.validar_consistencia(datos))
        
        # 4. Validar terminología prohibida
        if "drone" in texto.lower() and "RPAS" not in texto:
             violaciones.append("Uso de término genérico 'drone' sin definir 'RPAS' (estándar ICAO)")

        puntaje = max(0, 10 - len(violaciones))
        
        return {
            "satisfecho": len(violaciones) == 0,
            "puntaje": puntaje,
            "violaciones": violaciones,
            "datos_extraidos": datos,
            "targets": self.targets
        }

if __name__ == "__main__":
    # Prueba rápida con el texto de main.tex
    sample = "Following PRISMA 2020 guidelines, 33 studies (26 primary research articles) met criteria. Particle Swarm dominates (10 of 33, 30.3%). Altitude of 50."
    csp = CSPManuscrito()
    resultado = csp.resolver(sample)
    print(resultado)
