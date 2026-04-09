import os
import sys
import io
import google.generativeai as genai
from anthropic import Anthropic
from openai import OpenAI
from dotenv import load_dotenv

# Forzar UTF-8 para la terminal en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cargar .env
env_path = r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\.env"
load_dotenv(env_path)

def test_gemini():
    print("--- Probando Gemini ---")
    # Intentar varios nombres comunes
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("API_KEY")
    if not key: return f"No configurada (No se encontro GEMINI_API_KEY o GOOGLE_API_KEY en {env_path})"
    try:
        genai.configure(api_key=key)
        # Cambiado a gemini-2.0-flash (Alta cuota)
        model = genai.GenerativeModel('gemini-2.0-flash')
        resp = model.generate_content("Hola, responde brevemente.")
        return f"ACTIVA (Respuesta: {resp.text.strip()[:30]}...)"
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_claude():
    print("--- Probando Claude ---")
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key: return "No configurada"
    try:
        client = Anthropic(api_key=key)
        # Usar el nombre de modelo estable 20241022 para evitar 404
        resp = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": "Hola, responde brevemente."}]
        )
        return f"ACTIVA (Respuesta: {resp.content[0].text.strip()[:30]}...)"
    except Exception as e:
        return f"ERROR: {str(e)}"

def test_qwen():
    print("--- Probando Qwen ---")
    key = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")
    if not key: return "No configurada"
    try:
        client = OpenAI(
            api_key=key,
            base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
        )
        resp = client.chat.completions.create(
            model="qwen-max",
            messages=[{"role": "user", "content": "Hola, responde brevemente."}],
            max_tokens=50
        )
        return f"ACTIVA (Respuesta: {resp.choices[0].message.content.strip()[:30]}...)"
    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    print("=" * 60)
    print("DIAGNOSTICO INTEGRAL DE APIS")
    print("=" * 60)
    
    resultados = {
        "Gemini 1.5": test_gemini(),
        "Claude 3.5": test_claude(),
        "Qwen Max": test_qwen()
    }
    
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    for api, status in resultados.items():
        print(f"{api:15} : {status}")
    print("=" * 60)
