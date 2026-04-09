import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

print("=" * 60)
print("PRUEBA DE CONEXION CON CLAUDE 3.5 SONNET")
print("=" * 60)

# Verificar API key
claude_key = os.getenv("ANTHROPIC_API_KEY")

if not claude_key:
    print("\n[ERROR] No se encuentra ANTHROPIC_API_KEY en el archivo .env")
    print("\nPara obtener una API key:")
    print("1. Ve a https://console.anthropic.com")
    print("2. Crea una cuenta o inicia sesión")
    print("3. Ve a 'API Keys' y crea una nueva")
    print("4. Copia la key y pégala en el archivo .env")
    print("\nFormato en .env:")
    print("ANTHROPIC_API_KEY=sk-ant-api03-...")
    exit()

if claude_key == "tu_api_key_aqui":
    print("\n[!] La API key en .env es el placeholder.")
    print("Reemplázala con tu key real de Anthropic.")
    exit()

print(f"\n[OK] API key encontrada: {claude_key[:20]}...")

# Configurar cliente
try:
    cliente = Anthropic(api_key=claude_key)
    print("[OK] Cliente Claude inicializado correctamente")
except Exception as e:
    print(f"[ERROR] Error al inicializar cliente: {e}")
    exit()

# Probar conexión con un prompt simple
print("\n" + "=" * 60)
print("ENVIANDO PROMPT DE PRUEBA...")
print("=" * 60)

prompt_prueba = """
Escribe una breve oración en español académico sobre la importancia de 
los algoritmos de inteligencia de enjambre en sistemas multi-RPAS.
"""

try:
    respuesta = cliente.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt_prueba}]
    )
    
    print("\n[RESPUESTA DE CLAUDE]:")
    print("-" * 60)
    print(respuesta.content[0].text)
    print("-" * 60)
    print("\n[OK] Prueba exitosa! Claude está funcionando correctamente.")
    
except Exception as e:
    print(f"\n[ERROR] Error al llamar a Claude: {e}")
    
    if "authentication" in str(e).lower():
        print("\n[!] Error de autenticación. Verifica que la API key sea correcta.")
    elif "rate" in str(e).lower():
        print("\n[!] Límite de tasa excedido. Espera unos minutos y reintenta.")
    elif "quota" in str(e).lower():
        print("\n[!] Cuota agotada. Verifica tu plan en Anthropic.")
