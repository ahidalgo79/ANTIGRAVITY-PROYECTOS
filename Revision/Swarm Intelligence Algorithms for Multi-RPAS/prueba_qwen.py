import os
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

load_dotenv()

print("=" * 60)
print("PRUEBA DE QWEN")
print("=" * 60)

qwen_key = os.getenv("QWEN_API_KEY")

if not qwen_key or qwen_key == "tu_api_key_aqui":
    print("[X] API key no configurada")
    exit()

print(f"[OK] API key: {qwen_key[:15]}...")

dashscope.api_key = qwen_key

try:
    response = Generation.call(
        model='qwen3-max-2026-01-23',
        prompt="Escribe una oracion academica en español sobre inteligencia de enjambre.",
        result_format='message'
    )
    
    if response.status_code == 200:
        print("\n[OK] Qwen funciona!")
        print("\n[M] Respuesta:")
        print(response.output.choices[0].message.content)
    else:
        print(f"[X] Error: {response.message}")
        print(f"Detalles HTTP: {response.code}")
        
except Exception as e:
    print(f"[X] Error: {e}")
