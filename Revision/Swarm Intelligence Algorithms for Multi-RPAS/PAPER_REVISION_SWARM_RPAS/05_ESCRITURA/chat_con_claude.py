# chat_con_claude_fijo.py
import os
from anthropic import Anthropic

# ============================================
# PEGA TU CLAVE REAL DE CLAUDE AQUÍ
# (cópiala de tu archivo .env o de donde la tengas)
# ============================================
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
# ============================================

print("=" * 60)
print("🤖 CHAT CON CLAUDE 4.6 SONNET")
print("=" * 60)
print("Comandos: /salir, /clear, /help")
print("=" * 60)

# Crear cliente con la clave manual
cliente = Anthropic(api_key=ANTHROPIC_API_KEY)

# Historial de conversación
historial = []

while True:
    try:
        user_input = input("\n📝 Tú: ")
        
        if user_input.lower() == "/salir":
            print("\n👋 ¡Hasta luego!")
            break
        
        elif user_input.lower() == "/clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        
        elif user_input.lower() == "/help":
            print("\n📋 Comandos:")
            print("  /salir  - Terminar")
            print("  /clear  - Limpiar pantalla")
            print("  /help   - Mostrar ayuda")
            continue
        
        elif not user_input.strip():
            continue
        
        historial.append({"role": "user", "content": user_input})
        
        print("\n🤔 Claude está pensando...", end="", flush=True)
        
        response = cliente.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            temperature=0.7,
            messages=historial
        )
        
        respuesta = response.content[0].text
        
        print("\r" + " " * 30 + "\r", end="")
        print(f"\n🤖 Claude: {respuesta}")
        
        historial.append({"role": "assistant", "content": respuesta})
        
    except KeyboardInterrupt:
        print("\n\n👋 ¡Hasta luego!")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Si el error persiste, verifica que la API key sea correcta.")