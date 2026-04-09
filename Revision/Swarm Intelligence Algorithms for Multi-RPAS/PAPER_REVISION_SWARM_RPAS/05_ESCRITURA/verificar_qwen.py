import os
import dashscope
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

dashscope.api_key = api_key

print(f"Verificando clave con DashScope SDK: {api_key[:10]}...")

try:
    response = dashscope.Generation.call(
        model=dashscope.Generation.Models.qwen_turbo,
        prompt='Hola Qwen, responde brevemente para confirmar que la API Key es valida.'
    )
    
    if response.status_code == 200:
        print("\n(+) LA CLAVE ES VALIDA")
        print("-" * 50)
        print(f"Respuesta de Qwen: {response.output.text}")
        print("-" * 50)
    else:
        print(f"\n(-) ERROR DE VALIDACION (Code: {response.code})")
        print(f"Mensaje: {response.message}")
except Exception as e:
    print(f"\n(-) ERROR INESPERADO: {str(e)}")
