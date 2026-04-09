# verificar_env.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar el archivo .env desde la raíz
env_path = Path("C:/Users/HangarUPCH/Documents/Antigravity_Proyectos/Swarm Intelligence Algorithms for Multi-RPAS/.env")
load_dotenv(env_path)

print("=" * 50)
print("ESTADO DE TUS API KEYS")
print("=" * 50)

# Gemini
gemini = os.getenv("GEMINI_API_KEY")
if gemini:
    print(f"✅ Gemini: {gemini[:20]}... (longitud: {len(gemini)})")
else:
    print("❌ Gemini: No encontrada")

# Claude
claude = os.getenv("ANTHROPIC_API_KEY")
if claude:
    print(f"✅ Claude: {claude[:20]}... (longitud: {len(claude)})")
else:
    print("❌ Claude: No encontrada")

# Qwen
qwen = os.getenv("QWEN_API_KEY")
if qwen:
    print(f"✅ Qwen: {qwen[:15]}... (longitud: {len(qwen)})")
else:
    print("❌ Qwen: No encontrada")

# LangSmith
langsmith = os.getenv("LANGCHAIN_API_KEY")
if langsmith:
    print(f"✅ LangSmith: {langsmith[:15]}... (longitud: {len(langsmith)})")
else:
    print("⚠️ LangSmith: No configurada (opcional)")