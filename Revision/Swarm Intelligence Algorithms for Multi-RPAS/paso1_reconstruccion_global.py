# paso1_reconstruccion_global.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("=" * 60)
print("PASO 1: RECONSTRUCCIÓN GLOBAL - GEMINI 2.5 PRO")
print("=" * 60)

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

latex_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Listar secciones existentes
secciones_existentes = re.findall(r'\\section\{([^}]+)\}', contenido)
print(f"📋 Secciones existentes: {secciones_existentes}")

# Verificar secciones faltantes
secciones_requeridas = [
    "Introduction",
    "Materials and Methods",
    "Search Strategy",
    "Results",
    "Discussion",
    "Conclusions"
]

faltantes = [s for s in secciones_requeridas if s not in str(secciones_existentes)]
print(f"⚠️ Secciones faltantes: {faltantes}")

# Prompt para reconstrucción
prompt_reconstruccion = f"""
Actúa como un Editor Senior de Elsevier.

Analiza el manuscrito actual y prepara un plan de integración.

MANUSCRITO ACTUAL (primeras 5000 caracteres):
{contenido[:5000]}

SECCIONES EXISTENTES: {secciones_existentes}
SECCIONES REQUERIDAS: {secciones_requeridas}
SECCIONES FALTANTES: {faltantes}

TAREA:
1. Identificar dónde insertar las secciones faltantes
2. Mantener el orden lógico: Introduction → Materials and Methods → Search Strategy → Results → Discussion → Conclusions
3. Asegurar que todas las referencias y citas permanezcan intactas

RESPONDE CON UN PLAN DE INSERCIÓN ESTRUCTURADO.
"""

response = model.generate_content(prompt_reconstruccion)
print(response.text)