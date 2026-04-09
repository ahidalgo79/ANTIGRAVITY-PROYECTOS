import google.generativeai as genai
import os
from dotenv import load_dotenv

# Cargar .env
env_path = r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\.env"
load_dotenv(env_path)

key = os.getenv("GEMINI_API_KEY")
if not key:
    print("No se encontro GEMINI_API_KEY")
    exit()

genai.configure(api_key=key)

print("--- Modelos Disponibles para esta Clave ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error al listar modelos: {e}")
