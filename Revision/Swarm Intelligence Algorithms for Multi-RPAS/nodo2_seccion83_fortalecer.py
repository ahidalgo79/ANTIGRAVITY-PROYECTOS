# nodo2_seccion83_fortalecer.py
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

print("=" * 60)
print("NODO 2: FORTALECIMIENTO DE SECCIÓN 8.3")
print("=" * 60)

# Configurar Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

latex_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")

# Backup
import shutil
from datetime import datetime
backup = Path(f"PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.backup_seccion83_{datetime.now().strftime('%Y%m%d_%H%M%S')}.tex")
shutil.copy2(latex_path, backup)
print(f"✅ Backup: {backup.name}")

with open(latex_path, 'r', encoding='utf-8') as f:
    contenido = f.read()

# Buscar la sección de limitaciones
limitaciones_match = re.search(r'\\subsection{Limitations}.*?(?=\\subsection{|\Z)', contenido, re.DOTALL)
contexto_limitaciones = limitaciones_match.group(0) if limitaciones_match else ""

print("📖 Contexto de limitaciones encontrado")

model = genai.GenerativeModel('gemini-2.5-flash')

prompt_justificacion = """
Actúa como un Editor Académico Senior.

Escribe un párrafo justificativo para la limitación de "single-reviewer screening" en una revisión sistemática.

INFORMACIÓN CLAVE:
- La búsqueda booleana fue validada con un gold-standard set de 5 papers, logrando 100% de recall.
- Se utilizó screening liberal: los registros borderline fueron promovidos a full-text.
- Full-text assessment con segundo revisor logró acuerdo casi perfecto (kappa=0.91).
- Protocolo registrado en OSF: DOI 10.17605/OSF.IO/64DQ9 (trazabilidad completa).
- Auditoría asistida por IA garantiza consistencia y repetitividad.

REGLAS:
- Reconocer la limitación (transparencia)
- Mitigar con argumentos sólidos
- Tono académico formal, conciso (80-100 palabras)
- Prohibido: "drone" (usa "UAV" o "RPAS")

RESPONDE SOLO CON EL PÁRRAFO EN TEXTO PLANO.
"""

print("\n🔄 Generando justificación...")
response = model.generate_content(prompt_justificacion)
justificacion = response.text.strip()

print(f"\n📝 Justificación generada ({len(justificacion.split())} palabras)")
print("-" * 50)
print(justificacion[:400] + "..." if len(justificacion) > 400 else justificacion)
print("-" * 50)

# Formato LaTeX
justificacion_latex = f"\\textbf{{Single-reviewer title/abstract screening:}} {justificacion}"

# Reemplazar en el manuscrito
if "Single-reviewer title/abstract screening" in contenido:
    contenido = re.sub(
        r'\\textbf\{Single-reviewer title/abstract screening:.*?(?=\\item|\\end\{itemize\}|\n\n)',
        justificacion_latex + "\n\n",
        contenido,
        flags=re.DOTALL
    )
    print("✅ Sección 8.3 actualizada")
else:
    # Buscar itemize para agregar
    itemize_match = re.search(r'\\begin{itemize}(.*?)\\end{itemize}', contenido, re.DOTALL)
    if itemize_match:
        nuevo_item = f"\\item {justificacion_latex}\n"
        contenido = contenido.replace(itemize_match.group(1), itemize_match.group(1) + nuevo_item)
        print("✅ Limitación agregada a itemize")
    else:
        print("⚠️ No se encontró sección de limitaciones")

with open(latex_path, 'w', encoding='utf-8') as f:
    f.write(contenido)

print("\n✅ Sección 8.3 fortalecida")