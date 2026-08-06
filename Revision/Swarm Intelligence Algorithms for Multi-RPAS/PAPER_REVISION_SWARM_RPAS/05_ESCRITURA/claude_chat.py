# claude_chat.py - Coloca este archivo en la raíz del proyecto
from anthropic import Anthropic

# Tu clave de Claude (copiada directamente)
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

print("=" * 50)
print("CHAT CON CLAUDE - TERMINAL")
print("=" * 50)
print("Escribe 'salir' para terminar")
print("=" * 50)

cliente = Anthropic(api_key=API_KEY)

while True:
    pregunta = input("\nTú: ")
    
    if pregunta.lower() == "salir":
        print("¡Hasta luego!")
        break
    
    print("Claude está pensando...")
    
    respuesta = cliente.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": pregunta}]
    )
    
    print(f"\nClaude: {respuesta.content[0].text}\n")