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

class AsistenteTripleTest:
    def __init__(self):
        self.modelos = {}
        
        # Gemini (Alta cuota, motor principal)
        if os.getenv("GEMINI_API_KEY"):
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
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
        # Simular error en Gemini para probar fallback
        print(f"[SIMULADO] Error en Gemini con prompt: {prompt[:50]}...")
        raise Exception("Simulated quota exceeded error")
    
    def claude(self, prompt):
        try:
            # Solo para prueba, devolver el prompt modificado
            print(f"[CLAUDEx] Recibido prompt con fallback: {prompt[:80]}...")
            return f"✅ FALLBACK EXITOSO - Respuesta simulada para: {prompt[:30]}..."
        except Exception as e:
            self._log_error("Claude", str(e))
            raise e
    
    def qwen(self, prompt):
        try:
            print(f"[QWENx] Recibido prompt con fallback: {prompt[:80]}...")
            return f"✅ FALLBACK EXITOSO - Respuesta Qwen simulada: {prompt[:30]}..."
        except Exception as e:
            self._log_error("Qwen", str(e))
            raise e

    def _log_error(self, modelo, error):
        from datetime import datetime
        log_path = os.path.join(os.path.dirname(__file__), "debug_errores_test.txt")
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] ERROR en {modelo}: {error}\n")

    def elegir(self, prompt, tarea="auto"):
        """Selecciona el mejor modelo y aplica fallback si es necesario"""
        
        # 1. Determinar el orden de preferencia según la tarea
        preferencia = ["gemini", "qwen", "claude"]

        # 2. Intentar en cascada
        for i, modelo_nombre in enumerate(preferencia):
            if modelo_nombre in self.modelos:
                try:
                    if i > 0:
                        print(f"   [FALLBACK] Reintentando con {modelo_nombre.capitalize()}...")
                        # Modificar el prompt para indicar que es un fallback y debe continuar la tarea
                        fallback_prompt = f"[FALLBACK MODE - CONTINUE TASK] You are continuing the previous task. Do not ask questions or start over. The original request was: \"{prompt}\""
                    else:
                        fallback_prompt = prompt
                    
                    if modelo_nombre == "gemini": return self.gemini(fallback_prompt)
                    if modelo_nombre == "claude": return self.claude(fallback_prompt)
                    if modelo_nombre == "qwen":   return self.qwen(fallback_prompt)
                    
                except Exception:
                    print(f"   [!] Error en {modelo_nombre.capitalize()}. Pasando al siguiente...")
                    continue
        
        return "[ERROR] Todos los modelos han fallado en este intento."

if __name__ == "__main__":
    # Instanciar
    asistente = AsistenteTripleTest()
    
    if not asistente.modelos:
        print("[ERROR] No se configuró ningún modelo. Verifica el archivo .env")
    else:
        print("\n" + "=" * 60)
        print("PRUEBA DE CAMBIO DE MODELO CON FALLBACK")
        print("=" * 60)
        
        pregunta = "Redacta una oración técnica sobre enjambres de drones."
        print(f"Solicitud original: {pregunta}")
        
        resultado = asistente.elegir(pregunta, "redaccion")
        print(f"\nResultado final: {resultado}")