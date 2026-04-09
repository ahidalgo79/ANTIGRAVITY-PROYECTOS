import os
from openai import OpenAI
from dotenv import load_dotenv

# Cargamos el archivo .env
load_dotenv()

try:
    client = OpenAI(
        # La clave DASHSCOPE_API_KEY se lee del archivo .env
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-max",  
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Who are you?'}
        ]
    )
    print("\n[RESPUESTA DE QWEN]:")
    print("-" * 60)
    print(completion.choices[0].message.content)
    print("-" * 60)
except Exception as e:
    print(f"Error message: {e}")
    print("See: https://www.alibabacloud.com/help/model-studio/developer-reference/error-code")
