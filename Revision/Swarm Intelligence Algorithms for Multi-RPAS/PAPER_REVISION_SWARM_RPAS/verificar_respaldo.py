# verificar_respaldo.py
import json
import os
from pathlib import Path
from datetime import datetime

print("=" * 60)
print("VERIFICACION DE RESPALDOS Y ARCHIVOS GENERADOS")
print("=" * 60)

# Archivos que deberian existir (ajustados a las rutas reales segun ejecuciones previas)
archivos_esperados = [
    # Reports y resultados
    ("04_BIBLIOGRAFIA/Rescreening_TA_DrGarza.xlsx", "Excel actualizado"),
    ("04_BIBLIOGRAFIA/Rescreening_TA_DrGarza.backup.xlsx", "Backup del Excel"),
    ("todos_los_abstracts_consolidado.json", "Consolidado de abstracts"),
    ("resultado_kappa_final.json", "Resultado Kappa (Final)"),
    ("checkpoint_gemini_abstracts.json", "Checkpoint Gemini"),
    
    # Logs y reportes intermedios
    ("diagnostico_modelos.json", "Diagnostico de modelos"),
    ("reporte_abstracts_faltantes.json", "Reporte de abstracts faltantes"),
]

print("\nArchivos generados:")
print("-" * 60)

archivos_ok = []
archivos_faltan = []

for ruta, desc in archivos_esperados:
    p = Path(ruta)
    if p.exists():
        tamanio = p.stat().st_size
        print(f"  [OK] {desc}: {ruta} ({tamanio} bytes)")
        archivos_ok.append(ruta)
    else:
        print(f"  [FALTA] {desc}: {ruta}")
        archivos_faltan.append(ruta)

# Verificar abstracts pendientes
if Path("checkpoint_gemini_abstracts.json").exists():
    try:
        with open("checkpoint_gemini_abstracts.json", 'r', encoding='utf-8') as f:
            checkpoint = json.load(f)
            generados = checkpoint.get('generados', {})
            # Identificamos con error si el valor de 'abstract' empieza con [ERROR] o si no fue procesado
            pendientes = [k for k, v in generados.items() if "[ERROR]" in str(v.get('abstract', ''))]
            
            print(f"\nResumen Gemini:")
            print(f"  - Abstracts procesados con exito: {len(generados) - len(pendientes)}")
            print(f"  - Abstracts pendientes/error: {len(pendientes)}")
            
            if pendientes:
                print(f"  - IDs con error: {pendientes}")
    except:
        print("\nError al analizar checkpoint_gemini_abstracts.json")

# Resumen final
print("\n" + "=" * 60)
print("RESUMEN FINAL")
print("=" * 60)

print(f"Archivos encontrados: {len(archivos_ok)}/{len(archivos_esperados)}")

if archivos_faltan:
    print(f"\nNota: Algunos archivos (como logs de PRISMA) se generaran en el siguiente paso.")

print(f"\nFecha verificacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("-" * 60)
print("SISTEMA LISTO PARA CONTINUAR")
