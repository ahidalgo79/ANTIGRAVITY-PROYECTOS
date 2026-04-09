import pandas as pd
import numpy as np
import time
from sklearn.metrics import cohen_kappa_score
from asistente_triple_final import AsistenteTriple

# Rutas de archivos
archivo_entrada = r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\04_BIBLIOGRAFIA\Rescreening_TA_DrGarza_v2.xlsx"
archivo_salida = r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\04_BIBLIOGRAFIA\Rescreening_TA_Agente_v3.xlsx"

# Configuración del Prompt y Criterios
PROMPT_SISTEMA = """
Eres el 'Revisor 1', un investigador experto en Ingeniería Aeroespacial y Algoritmos de Inteligencia de Enjambre (Swarm Intelligence).
Tu tarea es realizar un cribado (screening) ciego a doble ciego de registros bibliográficos basándote exclusivamente en el TÍTULO y RESUMEN proporcionados.

Debes aplicar los siguientes CRITERIOS DE INCLUSIÓN Y EXCLUSIÓN.

CRITERIOS DE INCLUSIÓN (deben cumplirse TODOS o insinuarse fuertemente):
─────────────────────────────────────────
I1. Publicado entre 2021 y 2025 (Asume que cumple I1 a menos que el resumen diga lo contrario).
I2. Propone o evalúa al menos un algoritmo de Swarm Intelligence (PSO, ACO, ABC, GWO, SSA, FA, o híbridos reconocibles).
I3. Aplicado a planificación de rutas (path planning) de UAVs.
I4. Contexto de agricultura de precisión (monitoreo, fumigación, mapeo de cultivos).
I5. Accesible en texto completo en inglés (Asume que cumple I5).

CRITERIOS DE EXCLUSIÓN (basta UNO para excluir irremediablemente):
─────────────────────────────────────────
E1. Fuera del rango temporal 2021–2025.
E2. No involucra UAV (robots terrestres, acuáticos, simulaciones puras sin UAV).
E3. No usa algoritmo SI reconocible (RL puro, DL puro, métodos exactos).
E4. El algoritmo SI no se aplica a path planning (solo detección, clasificación, etc.).
E5. Dominio diferente a agricultura (urbano, industrial, militar, nuclear, etc.).
E6. Artículo de opinión, editorial, o sin metodología evaluable.

REGLA ESTRICTA DE SALIDA:
Debes responder con UNA SOLA PALABRA en MAYÚSCULAS:
INCLUIR (si cumple todos los de inclusión y ninguno de exclusión)
EXCLUIR (si incumple al menos un criterio de inclusión o cumple uno de exclusión)

Cualquier otra palabra romperá el sistema estadístico.
"""

def analizar_registro(asistente, titulo: str, resumen: str) -> str:
    prompt_usuario = f"""
    TÍTULO: {titulo}
    
    RESUMEN: {resumen}
    
    EVALUACIÓN: (Escribe solo INCLUIR o EXCLUIR).
    """
    
    try:
        # Usa Claude para un razonamiento superior
        respuesta = asistente.claude(f"{PROMPT_SISTEMA}\n\n{prompt_usuario}")
        texto = respuesta.strip().upper()
        # Filtro de seguridad sintáctico
        if "EXCLUIR" in texto:
            return "EXCLUIR"
        elif "INCLUIR" in texto:
            return "INCLUIR"
        else:
            print(f"[W] Respuesta anómala de LLM: '{texto}'. Forzando exclusión por seguridad cautelar.")
            return "EXCLUIR"
    except Exception as e:
        print(f"[E] Error en evaluación LLM: {e}")
        return "EXCLUIR"

def main():
    print("="*60)
    print("AGENTE AUTÓNOMO DE RESCREENING (PRISMA)")
    print("="*60)
    
    print("[1] Cargando Asistente LLM (Claude)...")
    asistente = AsistenteTriple()
    
    print(f"[2] Cargando dataset: {archivo_entrada}")
    try:
        df = pd.read_excel(archivo_entrada, sheet_name="SCREENING_SAMPLE")
    except Exception as e:
        print(f"Error fatal cargando Excel: {e}")
        return

    # Columnas relevantes (Index: 5 = TÍTULO, 6 = RESUMEN, 10 = DECISIÓN_REVISOR1, 7 = DECISIÓN_REVISOR2)
    # Si la estructura de columnas cambia, buscar por nombres explícitos
    col_titulo = "TÍTULO" if "TÍTULO" in df.columns else df.columns[5]
    col_resumen = "RESUMEN (extracto)" if "RESUMEN (extracto)" in df.columns else df.columns[6]
    col_revisor1 = "DECISIÓN_REVISOR1" if "DECISIÓN_REVISOR1" in df.columns else df.columns[10]
    col_revisor2 = "DECISIÓN_REVISOR2" if "DECISIÓN_REVISOR2" in df.columns else df.columns[7]
    col_acuerdo = "ACUERDO" if "ACUERDO" in df.columns else df.columns[11]

    total = len(df)
    print(f"[3] Evaluando independentemente {total} registros...")
    
    start_time = time.time()
    
    decisiones_agente = []
    
    for i, row in df.iterrows():
        titulo = str(row[col_titulo])
        resumen = str(row[col_resumen])
        
        # Ignorar vacíos catastróficos
        if pd.isna(row[col_titulo]) and pd.isna(row[col_resumen]):
            decisiones_agente.append(np.nan)
            continue
            
        print(f"  Procesando {i+1}/{total} | {titulo[:40]}...")
        
        decision = analizar_registro(asistente, titulo, resumen)
        decisiones_agente.append(decision)
        
        # Pausa para evitar rate limits (Anthropic suele ser restrictivo, espera 1s)
        time.sleep(1)

    print(f"\n[4] Evaluaciones completadas en {time.time() - start_time:.1f} segundos.")
    
    # Inyectar resultados en la columna de Revisor 1
    df[col_revisor1] = decisiones_agente

    # Generar la columna de ACUERDO automático (Revisor 1 vs Revisor 2)
    revisor2_limpio = df[col_revisor2].str.strip().str.upper()
    revisor1_limpio = df[col_revisor1].str.strip().str.upper()
    
    # Escribir la columna ACUERDO
    df[col_acuerdo] = np.where(revisor1_limpio == revisor2_limpio, "✓ Acuerdo", "✗ Discrepancia")
    
    print("\n[5] Análisis Estadístico de Fiabilidad Inter-Evaluador (Inter-rater reliability)")
    # Calcular acuerdo crudo y Kappa de Cohen
    # Limpiamos NaNs para sklearn
    mask = revisor1_limpio.notna() & revisor2_limpio.notna()
    r1 = revisor1_limpio[mask]
    r2 = revisor2_limpio[mask]
    
    if len(r1) > 0:
        acuerdo_crudo = (r1 == r2).mean() * 100
        kappa = cohen_kappa_score(r1, r2)
        
        print(f"    Total evaluados conjuntamente: {len(r1)}")
        print(f"    Porcentaje de Acuerdo Crudo: {acuerdo_crudo:.1f}%")
        print(f"    Índice Kappa de Cohen (k): {kappa:.3f}")
        
        if kappa < 0: interpretacion = "Desacuerdo sistemático"
        elif kappa <= 0.20: interpretacion = "Acuerdo leve"
        elif kappa <= 0.40: interpretacion = "Acuerdo justo"
        elif kappa <= 0.60: interpretacion = "Acuerdo moderado"
        elif kappa <= 0.80: interpretacion = "Acuerdo sustancial"
        else: interpretacion = "Acuerdo casi perfecto"
        print(f"    Interpretación estadística: {interpretacion}")
    else:
        print("    [W] No hay suficientes datos para calcular Kappa.")
        
    print(f"\n[6] Guardando resultados en {archivo_salida}")
    # Guardar en excel, preservando el engine original de pandas
    try:
        # Importante: al usar to_excel de pandas se pierden formatos condicionales del Excel original.
        # Pero como es un rescreening rápido para estadística, es aceptable.
        df.to_excel(archivo_salida, sheet_name="SCREENING_SAMPLE", index=False)
        print("¡Proceso completado con éxito!")
    except Exception as e:
        print(f"Error fatal guardando Excel: {e}")

if __name__ == "__main__":
    main()
