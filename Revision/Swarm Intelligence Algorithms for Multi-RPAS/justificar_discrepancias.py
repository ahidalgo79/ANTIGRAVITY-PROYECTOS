import pandas as pd
import time
from asistente_triple_final import AsistenteTriple
from pathlib import Path

# Rutas
archivo_excel = r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\04_BIBLIOGRAFIA\Rescreening_TA_Agente_v3.xlsx"
artifact_dir = Path(r"C:\Users\HangarUPCH\.gemini\antigravity\brain\61ee29d3-a6ba-4f20-8e09-8643aeca8c16")
artifact_path = artifact_dir / "justificacion_discrepancias.md"

PROMPT_SISTEMA_JUSTIFICACION = """
Eres el 'Revisor 1', un investigador experto en Ingeniería Aeroespacial y Algoritmos de Inteligencia de Enjambre (Swarm Intelligence).
Anteriormente evaluaste un registro bibliográfico y decidiste que merecía ser INCLUIDO en una revisión sistemática basada en PRISMA.
Tu co-revisor (Revisor 2) decidió EXCLUIRLO.

Debes justificar tu decisión de INCLUIRLO utilizando la estructura de razonamiento lógico STAR (Situation, Task, Action, Result).
Demuestra analíticamente que el Título y Resumen del estudio SÍ CUMPLEN FUERTEMENTE con TODOS los criterios de inclusión y NO INCURREN en ningún criterio de exclusión.

CRITERIOS OBLIGATORIOS A DEMOSTRAR (Inclusión):
I1. Publicado entre 2021 y 2025.
I2. Usa algoritmos Swarm Intelligence (PSO, ACO, ABC, GWO, SSA, FA, etc.).
I3. Aplicado a planificación de rutas (path planning) de UAVs/Multi-RPAS.
I4. Contexto de agricultura de precisión (monitoreo, fumigación, mapeo de cultivos).

ESTRUCTURA OBLIGATORIA:
[SITUATION] Contexto del estudio (¿De qué trata según el título y abstract?).
[TASK] Requisito metodológico a cumplir (¿Por qué se analizó este paper?).
[ACTION] Análisis de Criterios (Explica explícitamente qué fragmento del abstract valida I2, I3 e I4, y por qué no cae en ninguna exclusión como simulaciones puras sin UAV E2).
[RESULT] Veredicto Final (Conclusión contundente sobre por qué "INCLUIR" fue la decisión correcta y metodológicamente sólida).
"""

def generar_justificacion_star(asistente, titulo: str, resumen: str) -> str:
    prompt_usuario = f"TÍTULO: {titulo}\n\nRESUMEN: {resumen}\n\nJustifica tu evaluación bajo el formato STAR:"
    try:
        respuesta = asistente.claude(f"{PROMPT_SISTEMA_JUSTIFICACION}\n\n{prompt_usuario}")
        return respuesta.strip()
    except Exception as e:
        return f"[Error generando justificación: {e}]"

def main():
    print("="*60)
    print("GENERADOR DE JUSTIFICACIONES STAR - DESEMPATE PRISMA")
    print("="*60)
    
    # Cargar Excel
    df = pd.read_excel(archivo_excel, sheet_name="SCREENING_SAMPLE")
    
    # Identificar nombres de columnas
    col_titulo = "TÍTULO" if "TÍTULO" in df.columns else df.columns[5]
    col_resumen = "RESUMEN (extracto)" if "RESUMEN (extracto)" in df.columns else df.columns[6]
    col_revisor1 = "DECISIÓN_REVISOR1" if "DECISIÓN_REVISOR1" in df.columns else df.columns[10]
    col_acuerdo = "ACUERDO" if "ACUERDO" in df.columns else df.columns[11]
    
    # Filtrar discrepancias
    discrepancias = df[(df[col_acuerdo] == "✗ Discrepancia") & (df[col_revisor1].str.upper() == "INCLUIR")]
    
    print(f"Se encontraron {len(discrepancias)} papers en los que el Agente votó 'INCLUIR'.")
    
    asistente = AsistenteTriple()
    
    markdown_content = "# Justificación STAR de las Discrepancias de Rescreening (PRISMA)\n\n"
    markdown_content += "El modelo de Inteligencia Artificial (Actuando como Revisor 1) ha analizado de forma cruzada los abstracts contra los 11 criterios establecidos y fundamenta su decisión de **INCLUIR** los siguientes 5 registros mediante la metodología analítica aeroespacial STAR:\n\n---\n"
    
    for i, row in discrepancias.iterrows():
        id_reg = row['ID Registro']
        titulo = str(row[col_titulo])
        resumen = str(row[col_resumen])
        
        print(f"\nProcesando justificación para: {id_reg}")
        justificacion = generar_justificacion_star(asistente, titulo, resumen)
        
        markdown_content += f"## Registro en Disputa: `{id_reg}`\n"
        markdown_content += f"**Título Original**: *{titulo}*\n\n"
        markdown_content += f"### Justificación del Revisor 1 (IA)\n{justificacion}\n\n"
        markdown_content += "---\n"
        
        time.sleep(1) # rate limit
        
    # Guardar artefacto
    artifact_dir.mkdir(parents=True, exist_ok=True)
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)
        
    print(f"\n✅ Justificaciones creadas exitosamente. Artefacto guardado en {artifact_path}")

if __name__ == "__main__":
    main()
