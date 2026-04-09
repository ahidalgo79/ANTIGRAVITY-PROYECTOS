import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

print("=" * 60)
print("PRUEBA DE MODELOS CLAUDE DISPONIBLES")
print("=" * 60)

claude_key = os.getenv("ANTHROPIC_API_KEY")

if not claude_key or claude_key == "tu_api_key_aqui":
    print("\nAPI key no configurada correctamente")
    exit()

cliente = Anthropic(api_key=claude_key)

# Lista de modelos a probar
modelos_a_probar = [
    "claude-3-opus-20240229",
    "claude-3-sonnet-20240229",
    "claude-3-haiku-20240307",
    "claude-2.1",
    "claude-2.0",
    "claude-instant-1.2",
]

print("\nProbando modelos...")
print("-" * 60)

for modelo in modelos_a_probar:
    print(f"Probando {modelo}...", end=" ", flush=True)
    try:
        respuesta = cliente.messages.create(
            model=modelo,
            max_tokens=50,
            messages=[{"role": "user", "content": "Hola"}]
        )
        print("[OK] FUNCIONA")
        print(f"   Respuesta: {respuesta.content[0].text[:50]}...")
        break  # Si uno funciona, salimos
    except Exception as e:
        if "404" in str(e):
            print("[X] Modelo no disponible")
        elif "401" in str(e):
            print("[X] Error de autenticacion")
            break
        else:
            msg = str(e).replace("\n", " ")[:50]
            print(f"[X] {msg}")
