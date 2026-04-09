import os
from google import genai
from dotenv import load_dotenv

# 1. Cargar las variables secretas del archivo .env
load_dotenv()

# 2. Obtener la clave de Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or GEMINI_API_KEY == "TU_GEMINI_API_KEY_AQUI":
    print("❌ ERROR: Aún no has configurado tu GEMINI_API_KEY.")
    print("   Por favor, abre el archivo '.env', pega tu clave de API y vuelve a intentar.")
    exit(1)

# 3. Configurar la IA usando la nueva librería oficial (google-genai)
client = genai.Client(api_key=GEMINI_API_KEY)

print("🚀 Tu entorno multi-agente está activo.")
print("🧠 Contactando al cerebro de Gemini 1.5 Flash en los servidores de Google...")

try:
    # 4. Enviar un prompt de prueba
    prompt = "Escribe exactamente 1 oración motivadora para darle la bienvenida a un nuevo Director Creativo Especializado en IA."
    response = client.models.generate_content(
        model='gemini-1.5-flash',
        contents=prompt
    )
    
    print("\n✅ ¡Conexión exitosa! El Agente 01 responde:\n")
    print(f"   => \"{response.text.strip()}\"\n")
    print("¡Ya estás listo para empezar a crear flujos avanzados con LangGraph y CrewAI!")
except Exception as e:
    print(f"\n❌ Ocurrió un error al intentar conectarse: {e}")
