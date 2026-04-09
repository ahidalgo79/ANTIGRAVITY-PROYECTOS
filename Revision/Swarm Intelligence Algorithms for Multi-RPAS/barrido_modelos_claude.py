import os
import sys
import io
from anthropic import Anthropic
from dotenv import load_dotenv

# UTF-8 para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

def sweep_models():
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Candidatos basados en lanzamientos de 2026 y aliases "latest"
    candidatos = [
        "claude-4-sonnet",
        "claude-4-0-sonnet-20260217",
        "claude-3-7-sonnet-20260217",
        "claude-3-5-sonnet-latest",
        "claude-3-5-sonnet-20241022",
        "claude-3-sonnet-20240229"
    ]
    
    print("=" * 60)
    print("BARRIDO DE MODELOS ANTHROPIC (SIN EMOJIS)")
    print("=" * 60)
    
    for modelo in candidatos:
        try:
            print(f"Probando: {modelo:30}", end=" ")
            client.messages.create(
                model=modelo,
                max_tokens=10,
                messages=[{"role": "user", "content": "hi"}]
            )
            print("[OK] SUCCESS")
            return modelo
        except Exception as e:
            if "not_found_error" in str(e):
                print("[404] NOT FOUND")
            else:
                print(f"[ERROR] {e}")
    return None

if __name__ == "__main__":
    sweep_models()
