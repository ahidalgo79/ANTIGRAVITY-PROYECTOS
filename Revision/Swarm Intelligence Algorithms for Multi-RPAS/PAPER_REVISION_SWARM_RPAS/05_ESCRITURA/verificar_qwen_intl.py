import os
from openai import OpenAI
from dotenv import load_dotenv
import sys
import io

# Forzar UTF-8 para la salida en Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cargar .env desde la raíz
env_path = r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\.env"
load_dotenv(env_path)

api_key = os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY")

if not api_key:
    print("Error: No se encontro la clave QWEN_API_KEY o DASHSCOPE_API_KEY en el .env")
    exit(1)

print(f"Verificando clave con OpenAI SDK (DashScope Intl): {api_key[:10]}...")

try:
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    )
    
    response = client.chat.completions.create(
        model="qwen-max",
        messages=[{"role": "user", "content": "Hola Qwen, responde brevemente para confirmar que la API Key es valida."}],
        max_tokens=50
    )
    
    print("\n(+) LA CLAVE ES VALIDA (Internacional)")
    print("-" * 50)
    print(f"Respuesta de Qwen: {response.choices[0].message.content}")
    print("-" * 50)
    
except Exception as e:
    print(f"\n(-) ERROR DE VALIDACION (Internacional): {str(e)}")
