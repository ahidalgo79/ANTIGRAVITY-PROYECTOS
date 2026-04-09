import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargamos el archivo .env
load_dotenv()

try:
    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )

    print("Consultando modelos disponibles en DashScope (OpenAI Compatible)...")
    print("-" * 60)
    
    models = client.models.list()
    for model in models.data:
        print(f"- {model.id}")
        
except Exception as e:
    print(f"Error al listar: {e}")
