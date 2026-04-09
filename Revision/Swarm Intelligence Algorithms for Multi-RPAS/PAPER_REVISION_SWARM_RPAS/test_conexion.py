# test_conexion_final.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("Probando conexiones con tus modelos específicos...\n")

gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    genai.configure(api_key=gemini_key)
    
    # Estos son los nombres exactos que devolvió tu list_models()
    modelos_a_probar = [
        "gemini-2.0-flash",
        "gemini-2.5-flash",
        "gemini-3-flash-preview"
    ]
    
    for modelo in modelos_a_probar:
        try:
            print(f"Probando {modelo}...", end=" ")
            model = genai.GenerativeModel(modelo)
            response = model.generate_content("Responde solo: OK")
            print(f"CONECTADO exitosamente")
            break
        except Exception as e:
            if "429" in str(e):
                print(f"CUOTA excedida (Tienes acceso, pero el límite es 0)")
            else:
                print(f"ERROR: {str(e)[:100]}")
else:
    print("Gemini: API key no configurada")
