# prueba_gemini.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Usar el modelo que funciono en el diagnostico (2.5 flash)
model = genai.GenerativeModel('gemini-2.5-flash')

print("Probando Gemini 2.5 Flash...")
print("-" * 40)

try:
    # Prueba simple
    response = model.generate_content("Escribe una oracion en español sobre inteligencia de enjambre.")
    
    print("RESPUESTA:")
    print(response.text)
    print("-" * 40)
    print("OK: Prueba exitosa. El modelo responde correctamente.")
    
except Exception as e:
    print(f"FAIL: Error: {e}")
