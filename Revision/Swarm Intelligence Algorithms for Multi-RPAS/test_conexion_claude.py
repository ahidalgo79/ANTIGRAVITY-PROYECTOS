import os
import sys
import io
from dotenv import load_dotenv
from anthropic import Anthropic

# UTF-8 para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

def test_claude():
    print("=" * 60)
    print("DIAGNOSTICO DIRECTO: ANTHROPIC CLAUDE")
    print("=" * 60)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("[ERROR] No se encontró ANTHROPIC_API_KEY en el .env")
        return

    print(f"API Key detectada (primeros 10): {api_key[:10]}...")
    
    client = Anthropic(api_key=api_key)
    
    # Intentar con Sonnet 3.5 (el estándar actual)
    modelos_a_probar = ["claude-3-5-sonnet-20240620", "claude-3-7-sonnet-20250219"]
    
    for modelo in modelos_a_probar:
        print(f"\n[PROBANDO MODELO]: {modelo}")
        try:
            message = client.messages.create(
                model=modelo,
                max_tokens=100,
                messages=[{"role": "user", "content": "Hola, genera una oración corta de prueba sobre drones."}]
            )
            
            print(f"[STATUS] Mensaje creado exitosamente")
            print(f"[RESPUESTA CONTENT]: {message.content}")
            
            if message.content and len(message.content) > 0:
                texto = message.content[0].text
                print(f"[TEXTO EXTRAIDO]: '{texto}'")
                if not texto:
                    print("[W] El texto extraído está vacío.")
            else:
                print("[W] No se encontró contenido en la respuesta.")
                
            # Si uno funciona, terminamos
            break
            
        except Exception as e:
            print(f"[FAIL] Error con modelo {modelo}: {e}")

if __name__ == "__main__":
    test_claude()
