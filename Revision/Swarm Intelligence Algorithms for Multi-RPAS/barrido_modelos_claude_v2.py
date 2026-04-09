import os
import sys
import io
from anthropic import Anthropic
from dotenv import load_dotenv

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

load_dotenv()

def sweep_new_naming():
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # Probando la nomenclatura que funcionó en el Turno 9
    candidatos = [
        "claude-sonnet-4-5-20250920",
        "claude-sonnet-4-6-20260217",
        "claude-sonnet-4-6",
        "claude-3-7-sonnet-20260217"
    ]
    
    print("=" * 60)
    print("RE-DIAGNOSTICO: NOMENCLATURA SONNET-FIRST")
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
            print(f"[ERROR] {e}")
    return None

if __name__ == "__main__":
    sweep_new_naming()
