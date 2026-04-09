import os
import sys
from typing import Dict, List, Tuple
from dotenv import load_dotenv
from anthropic import Anthropic
from csp_guardrail import CSPGuardrail

# Forzar UTF-8 para la salida estándar en Windows (evita UnicodeEncodeError)
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Fallback para versiones muy antiguas de Python
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class OrquestadorConRAG:
    """
    Orquestador Agéntico con validación de restricciones (Guardrails) 
    y modo de pensamiento extendido (Claude 4.6).
    """
    
    def __init__(self):
        # Cargar variables de entorno
        env_path = os.path.join(os.getcwd(), "..", "..", ".env")
        load_dotenv(dotenv_path=env_path)
        
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY no encontrada en el entorno.")
            
        self.cliente = Anthropic(api_key=api_key)
        self.guardrail = CSPGuardrail()
        self.modelo = "claude-sonnet-4-6"
    
    def generar_con_claude(self, prompt: str, system_prompt: str = "") -> str:
        """Petición base a Claude con Thinking Mode habilitado."""
        try:
            response = self.cliente.messages.create(
                model=self.modelo,
                max_tokens=8192,
                thinking={"type": "enabled", "budget_tokens": 4096},
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extraer solo el texto final
            return "".join([b.text for b in response.content if b.type == "text"])
        except Exception as e:
            return f"Error en la API: {str(e)}"

    def generar_con_validacion(self, prompt: str, max_iteraciones: int = 3) -> Dict:
        """Genera contenido con validación CSP y bucle de autorreflexión."""
        
        system_prompt = "Actúa como un Ingeniero Aeroespacial. Respuesta técnica académica."
        prompt_actual = prompt
        
        print(f"[*] Iniciando orquestacion para: '{prompt[:50]}...'")
        
        for i in range(max_iteraciones):
            print(f"\n[Iteracion {i+1}/{max_iteraciones}] Generando respuesta...")
            
            # 1. Generar contenido
            respuesta = self.generar_con_claude(prompt_actual, system_prompt)
            
            # 2. Validar contra restricciones críticas (CSP)
            es_valido, violaciones = self.guardrail.validar(respuesta)
            
            if es_valido:
                print("[+] Validacion exitosa: El contenido cumple todos los criterios.")
                return {
                    "exito": True,
                    "respuesta": respuesta,
                    "iteraciones": i + 1,
                    "violaciones": []
                }
            
            # 3. Informar y preparar refinamiento
            print(f"[!] Se detectaron {len(violaciones)} violaciones:")
            for v in violaciones:
                # Evitar emojis en el print para estabilidad de consola
                print(f"  - {v}")
            
            if i < max_iteraciones - 1:
                print("[*] Refinando prompt para correccion automatica...")
                prompt_actual = self._generar_prompt_refinamiento(prompt, respuesta, violaciones)
            else:
                print("[-] Se alcanzo el limite de iteraciones sin validacion total.")
                return {
                    "exito": False,
                    "respuesta": respuesta,
                    "iteraciones": i + 1,
                    "violaciones": violaciones
                }

    def _generar_prompt_refinamiento(self, prompt_original: str, respuesta_previa: str, violaciones: List[str]) -> str:
        """Genera instrucciones específicas para que el modelo corrija sus fallos."""
        lista_violaciones = "\n".join([f"- {v}" for v in violaciones])
        
        return f"""
        INSTRUCCIÓN ORIGINAL: {prompt_original}
        
        TU RESPUESTA ANTERIOR FUE RECHAZADA POR UN SISTEMA DE GOBERNANZA TÉCNICA.
        
        VIOLACIONES DETECTADAS:
        {lista_violaciones}
        
        TAREA DE REFINAMIENTO:
        Reescribe el contenido asegurando el cumplimiento estricto de:
        1. Tamaño de muestra n=30 invariablemente (23 primarios, 7 reviews).
        2. Terminología ICAO: Usa RPAS o UAV, NUNCA uses la palabra 'drone'.
        3. Rigor SI: Todas las magnitudes deben tener unidades SI (m/s, kg, s, etc.).
        4. Estadísticas PSO: El porcentaje correcto es 33.3%.
        
        PROPORCIONA EL TEXTO COMPLETO Y CORREGIDO:
        """

if __name__ == "__main__":
    # Prueba del orquestador
    try:
        orquestador = OrquestadorConRAG()
        
        # Un prompt que activará violaciones de drones y n=33
        prompt_prueba = """
        Escribe un breve párrafo técnico sobre la autonomía de drones SAR. 
        Menciona que revisamos 33 estudios y que su masa es de 10 kilos.
        """
        
        resultado = orquestador.generar_con_validacion(prompt_prueba)
        
        print("\n" + "=" * 60)
        print("RESULTADO FINAL DEL ORQUESTADOR")
        print("=" * 60)
        print(f"Exito: {resultado['exito']}")
        print(f"Iteraciones: {resultado['iteraciones']}")
        print("-" * 40)
        print("CONTENIDO FINAL:")
        print(resultado['respuesta'])
        print("-" * 40)
        
    except Exception as e:
        print(f"[-] Error fatal: {e}")
