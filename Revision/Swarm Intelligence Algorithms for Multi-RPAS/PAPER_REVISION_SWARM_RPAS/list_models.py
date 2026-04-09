# list_models.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
gemini_key = os.getenv("GEMINI_API_KEY")

if gemini_key:
    genai.configure(api_key=gemini_key)
    print("Listing available models for the provided key...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model: {m.name} | Version: {m.version}")
    except Exception as e:
        print(f"Error listing models: {e}")
else:
    print("API key not found in .env")
