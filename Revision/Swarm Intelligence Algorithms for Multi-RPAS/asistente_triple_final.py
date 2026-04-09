import os
from dotenv import load_dotenv
import google.generativeai as genai
from anthropic import Anthropic
from openai import OpenAI

import sys

# Configurar la terminal para manejar UTF-8 (evita errores con emojis en Windows)
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

class AsistenteTriple:
    def __init__(self):
        self.modelos = {}
        
        # Gemini (Alta cuota, motor principal)
        if os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            # Usar gemini-2.0-flash para mayor estabilidad y velocidad
            self.modelos["gemini"] = genai.GenerativeModel('gemini-2.0-flash')
            print("[OK] Gemini 2.0 Flash (Principal)")
        
        # Claude (Calidad premium, fallback)
        if os.getenv("ANTHROPIC_API_KEY"):
            self.modelos["claude"] = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
            print("[OK] Claude 3.5 Sonnet (Fallback)")
        
        # Qwen (Respaldo internacional)
        if os.getenv("QWEN_API_KEY"):
            self.modelos["qwen"] = OpenAI(
                api_key=os.getenv("QWEN_API_KEY"),
                base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
            )
            print("[OK] Qwen Max (Respaldo)")
    
    def gemini(self, prompt):
        try:
            resp = self.modelos["gemini"].generate_content(prompt)
            # Manejar correctamente la respuesta
            if hasattr(resp, 'text'):
                return resp.text
            else:
                return str(resp)
        except Exception as e:
            self._log_error("Gemini", str(e))
            raise e
            
    def claude(self, prompt):
        try:
            # Usar modelo estable para evitar 404
            resp = self.modelos["claude"].messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=8192,
                messages=[{"role": "user", "content": prompt}]
            )
            return resp.content[0].text
        except Exception as e:
            self._log_error("Claude", str(e))
            raise e
    
    def qwen(self, prompt):
        try:
            resp = self.modelos["qwen"].chat.completions.create(
                model="qwen-max",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4096
            )
            return resp.choices[0].message.content
        except Exception as e:
            self._log_error("Qwen", str(e))
            raise e

    def _log_error(self, modelo, error):
        from datetime import datetime
        # Asegurarse de que el directorio existe (opcional, pero buena práctica)
        log_path = os.path.join(os.path.dirname(__file__), "debug_errores.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] ERROR en {modelo}: {error}\n")

    def elegir(self, prompt, tarea="auto"):
        """Selecciona el mejor modelo y aplica fallback si es necesario"""
        
        # 1. Determinar el orden de preferencia según la tarea
        # CAMBIO: Gemini es prioridad #1, Qwen es prioridad #2 (más estable que Claude actualmente)
        preferencia = []
        if tarea == "codigo":
            preferencia = ["gemini", "qwen"]
        elif tarea == "redaccion":
            preferencia = ["gemini", "qwen", "claude"] # Qwen antes que Claude
        elif tarea == "alternativa":
            preferencia = ["qwen", "gemini"]
        else:
            # Auto-detección
            if any(p in prompt.lower() for p in ["python", "script", "extraer", "calcular"]):
                preferencia = ["gemini", "qwen"]
            elif any(p in prompt.lower() for p in ["redacta", "escribe", "mejora", "discusion"]):
                preferencia = ["gemini", "qwen", "claude"] # Qwen antes que Claude
            else:
                preferencia = ["gemini", "qwen"]

        # 2. Intentar en cascada
        for i, modelo_nombre in enumerate(preferencia):
            if modelo_nombre in self.modelos:
                try:
                    if i > 0:
                        print(f"   [FALLBACK] Reintentando con {modelo_nombre.capitalize()}...")
                    
                    if modelo_nombre == "gemini": return self.gemini(prompt)
                    if modelo_nombre == "claude": return self.claude(prompt)
                    if modelo_nombre == "qwen":   return self.qwen(prompt)
                    
                except Exception:
                    # Si falla, el loop continúa al siguiente modelo de la lista
                    print(f"   [!] Error en {modelo_nombre.capitalize()}. Pasando al siguiente...")
                    continue
        
        return "[ERROR] Todos los modelos han fallado en este intento."


if __name__ == "__main__":
    # Instanciar
    asistente = AsistenteTriple()
    
    if not asistente.modelos:
        print("[ERROR] No se configuró ningún modelo. Verifica el archivo .env")
    else:
        # Probar con Fallback (simulado)
        print("\n" + "=" * 60)
        print("SISTEMA DE ASISTENTE TRIPLE CON REDUNDANCIA")
        print("=" * 60)
        
        pregunta = "Redacta una oración técnica sobre enjambres de drones."
        print(f"Solicitud: {pregunta}")
        
        resultado = asistente.elegir(pregunta, "redaccion")
        print(f"\nRespuesta Final:\n{resultado}")
