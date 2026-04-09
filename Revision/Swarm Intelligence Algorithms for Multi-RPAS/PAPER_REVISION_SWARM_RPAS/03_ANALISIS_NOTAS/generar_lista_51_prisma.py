#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generar Lista de 51 Registros para Revisión Independiente — PRISMA 2020
Manuscrito: Swarm Intelligence for Multi-UAV Path Planning in Precision Agriculture (2021–2025)

CORRECCIÓN: Extracción de año mejorada para manejar formatos como "2021b", "2022a", etc.
"""

import pandas as pd
import re
from datetime import datetime
import os

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

BASE_DIR = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS'

ARCHIVO_INCLUIDOS = os.path.join(BASE_DIR, 'PRISMA_Incluidos_33.csv')
ARCHIVO_EXCLUIDOS = os.path.join(BASE_DIR, 'PRISMA_Excluidos_21.csv')
ARCHIVO_SALIDA = os.path.join(BASE_DIR, 'Lista_51_Screening_Coautor.csv')
ARCHIVO_LOG = os.path.join(BASE_DIR, 'log_procesamiento.txt')

# IDs de estudios que deben eliminarse (fuera de período 2021-2025)
# Según Lista_51_Registros_PRISMA_Reconciliada.docx
IDS_FUERA_PERIODO = ['EXC_15', 'EXC_19', 'EXC_20']

# ============================================================================
# FUNCIÓN 1: Cargar estudios incluidos
# ============================================================================

def cargar_incluidos(ruta_archivo):
    """Carga los 33 estudios incluidos desde CSV"""
    try:
        df = pd.read_csv(ruta_archivo, encoding='utf-8-sig')
        
        incluidos = []
        for _, row in df.iterrows():
            incluidos.append({
                'ID': row.get('ID_Manuscrito', ''),
                'Título': row.get('Título', ''),
                'Autor_Principal': row.get('Referencia', '').split(',')[0] if pd.notna(row.get('Referencia', '')) else '',
                'Año': int(row.get('Año', 0)),
                'Fuente': row.get('Referencia', ''),
                'DOI': row.get('DOI', '') if 'DOI' in row else '',
                'Algoritmo': row.get('Algoritmo', ''),
                'Validación': row.get('Validación', ''),
                'UAVs': row.get('UAVs', ''),
                'Aplicación': row.get('Aplicación', ''),
                'Decisión_Tú': 'Incluir',
                'Criterio_Exclusión': '',
                'Justificación_Breve': '',
                'Decisión_Coautor': '',
                'Notas_Coautor': ''
            })
        
        print(f"✅ Cargados {len(incluidos)} estudios incluidos")
        return incluidos
    
    except Exception as e:
        print(f"❌ Error cargando incluidos: {e}")
        return []

# ============================================================================
# FUNCIÓN 2: Extraer año de referencia (CORREGIDA)
# ============================================================================

def extraer_año(referencia):
    """
    Extrae el año de una referencia como "Ntakolia & Lyridis (2021b)" o "Baghal (2016)"
    Maneja formatos con letras adicionales: 2021a, 2021b, 2022a, etc.
    """
    if pd.isna(referencia) or not isinstance(referencia, str):
        return 0
    
    # Buscar patrón de año entre paréntesis: (2021), (2021a), (2021b), etc.
    match = re.search(r'\((\d{4})[a-z]?\)', referencia, re.IGNORECASE)
    
    if match:
        return int(match.group(1))
    
    # Fallback: buscar cualquier año de 4 dígitos
    match = re.search(r'(\d{4})', referencia)
    if match:
        return int(match.group(1))
    
    return 0

# ============================================================================
# FUNCIÓN 3: Cargar y filtrar estudios excluidos
# ============================================================================

def cargar_y_filtrar_excluidos(ruta_archivo, ids_fuera_periodo):
    """Carga los 21 excluidos y filtra los 3 fuera de período"""
    try:
        df = pd.read_csv(ruta_archivo, encoding='utf-8-sig')
        
        excluidos = []
        excluidos_filtrados = []
        
        for _, row in df.iterrows():
            id_original = row.get('ID', '')
            
            # Extraer año usando la función corregida
            referencia = str(row.get('Referencia', ''))
            año = extraer_año(referencia)
            
            # Verificar si está fuera de período (antes de 2021 o después de 2025)
            fuera_periodo = año < 2021 or año > 2025
            
            # También verificar por ID explícito (lista manual de reconciliación)
            if id_original in ids_fuera_periodo:
                fuera_periodo = True
            
            excluido = {
                'ID_Original': id_original,
                'Título': row.get('Título', ''),
                'Autor_Principal': referencia.split(',')[0] if ',' in referencia else referencia,
                'Año': año,
                'Fuente': referencia,
                'DOI': row.get('DOI', '') if 'DOI' in row else '',
                'Razón_Exclusión': row.get('Razón_Exclusión', ''),
                'Criterio_PRISMA': row.get('Criterio_PRISMA', ''),
                'Decisión_Tú': 'Excluir',
                'Decisión_Coautor': '',
                'Notas_Coautor': ''
            }
            
            if fuera_periodo:
                excluidos_filtrados.append(excluido)
            else:
                excluidos.append(excluido)
        
        print(f"✅ Cargados {len(excluidos) + len(excluidos_filtrados)} estudios excluidos totales")
        print(f"⚠️  Filtrados {len(excluidos_filtrados)} estudios fuera de período (2021-2025)")
        print(f"✅ Quedan {len(excluidos)} estudios excluidos a texto completo")
        
        if excluidos_filtrados:
            print("\n📋 Estudios filtrados (fuera de período):")
            for exc in excluidos_filtrados:
                print(f"   - {exc['ID_Original']}: {exc['Fuente']} ({exc['Año']})")
        
        return excluidos, excluidos_filtrados
    
    except Exception as e:
        print(f"❌ Error cargando excluidos: {e}")
        return [], []

# ============================================================================
# FUNCIÓN 4: Estandarizar IDs de excluidos (EXC_01 a EXC_18)
# ============================================================================

def estandarizar_ids_excluidos(excluidos):
    """Renombra IDs para que sean consecutivos EXC_01 a EXC_18"""
    
    for i, exc in enumerate(excluidos, start=1):
        exc['ID'] = f'EXC_{i:02d}'
        exc['Criterio_Exclusión'] = exc.get('Criterio_PRISMA', '')
        exc['Justificación_Breve'] = exc.get('Razón_Exclusión', '')
    
    print(f"✅ IDs estandarizados: EXC_01 a EXC_{len(excluidos):02d}")
    return excluidos

# ============================================================================
# FUNCIÓN 5: Verificar duplicados por DOI
# ============================================================================

def verificar_duplicados(incluidos, excluidos):
    """Verifica que no haya DOIs duplicados entre incluidos y excluidos"""
    
    duplicados = []
    
    dois_incluidos = {}
    for inc in incluidos:
        doi = str(inc.get('DOI', '')).strip()
        if doi and doi != 'nan' and doi != '':
            dois_incluidos[doi.lower()] = inc['Título'][:50]
    
    for exc in excluidos:
        doi = str(exc.get('DOI', '')).strip()
        if doi and doi != 'nan' and doi != '':
            if doi.lower() in dois_incluidos:
                duplicados.append({
                    'DOI': doi,
                    'Incluido': dois_incluidos[doi.lower()],
                    'Excluido': exc['Título'][:50]
                })
    
    if duplicados:
        print(f"\n⚠️  ALERTA: {len(duplicados)} duplicados por DOI detectados:")
        for dup in duplicados:
            print(f"   - DOI: {dup['DOI']}")
            print(f"     Incluido: {dup['Incluido']}...")
            print(f"     Excluido: {dup['Excluido']}...")
    else:
        print("\n✅ No hay duplicados por DOI entre incluidos y excluidos")
    
    return duplicados

# ============================================================================
# FUNCIÓN 6: Generar CSV final para coautor
# ============================================================================

def generar_csv_final(incluidos, excluidos, ruta_salida):
    """Genera el CSV final listo para enviar al coautor"""
    
    todos = incluidos + excluidos
    
    df = pd.DataFrame(todos)
    
    columnas = [
        'ID', 'Título', 'Autor_Principal', 'Año', 'Fuente', 'DOI',
        'Algoritmo', 'Validación', 'UAVs', 'Aplicación',
        'Decisión_Tú', 'Criterio_Exclusión', 'Justificación_Breve',
        'Decisión_Coautor', 'Notas_Coautor'
    ]
    
    for col in columnas:
        if col not in df.columns:
            df[col] = ''
    
    df = df[columnas]
    
    df.to_csv(ruta_salida, index=False, encoding='utf-8-sig')
    
    print(f"\n{'='*70}")
    print(f"✅ ARCHIVO GENERADO: {ruta_salida}")
    print(f"{'='*70}")
    print(f"📊 Resumen:")
    print(f"   - Estudios incluidos: {len(incluidos)}")
    print(f"   - Estudios excluidos: {len(excluidos)}")
    print(f"   - Total registros: {len(todos)}")
    
    if len(todos) == 51:
        print(f"   ✅ Total CORRECTO: 51 registros (33 incluidos + 18 excluidos)")
    else:
        print(f"   ❌ Total INCORRECTO: {len(todos)} registros (se esperan 51)")
    
    print(f"\n📋 Conteos por criterio de exclusión:")
    
    criterios = {}
    for exc in excluidos:
        c = exc.get('Criterio_Exclusión', 'N/A')
        criterios[c] = criterios.get(c, 0) + 1
    
    for c, count in sorted(criterios.items()):
        print(f"   - {c}: {count} estudios")
    
    print(f"\n⚠️  INSTRUCCIONES PARA EL COAUTOR:")
    print(f"   1. NO consultar la columna 'Decisión_Tú' durante la revisión")
    print(f"   2. Completar columna 'Decisión_Coautor' con: Incluir / Excluir")
    print(f"   3. Si excluye, completar 'Criterio_Exclusión' con: E1, E2, E3, E4, o E5")
    print(f"   4. Añadir notas en 'Notas_Coautor' si la decisión no es obvia")
    print(f"{'='*70}\n")
    
    return df

# ============================================================================
# FUNCIÓN 7: Generar log de procesamiento
# ============================================================================

def generar_log(incluidos, excluidos, excluidos_filtrados, duplicados, ruta_log):
    """Genera un archivo de log con el resumen del procesamiento"""
    
    with open(ruta_log, 'w', encoding='utf-8') as f:
        f.write("="*70 + "\n")
        f.write("LOG DE PROCESAMIENTO — Lista 51 Registros PRISMA\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*70 + "\n\n")
        
        f.write("1. ESTUDIOS INCLUIDOS\n")
        f.write(f"   Total cargados: {len(incluidos)}\n\n")
        
        f.write("2. ESTUDIOS EXCLUIDOS\n")
        f.write(f"   Total cargados: {len(excluidos) + len(excluidos_filtrados)}\n")
        f.write(f"   Filtrados (fuera de período): {len(excluidos_filtrados)}\n")
        f.write(f"   Mantenidos (texto completo): {len(excluidos)}\n\n")
        
        if excluidos_filtrados:
            f.write("   Estudios filtrados:\n")
            for exc in excluidos_filtrados:
                f.write(f"   - {exc['ID_Original']}: {exc['Fuente']} ({exc['Año']})\n")
            f.write("\n")
        
        f.write("3. VERIFICACIÓN DE DUPLICADOS\n")
        f.write(f"   Duplicados por DOI: {len(duplicados)}\n\n")
        
        if duplicados:
            f.write("   Duplicados detectados:\n")
            for dup in duplicados:
                f.write(f"   - DOI: {dup['DOI']}\n")
                f.write(f"     Incluido: {dup['Incluido']}\n")
                f.write(f"     Excluido: {dup['Excluido']}\n")
            f.write("\n")
        
        f.write("4. RESUMEN FINAL\n")
        f.write(f"   Total registros en archivo final: {len(incluidos) + len(excluidos)}\n")
        f.write(f"   Esperado: 51 (33 incluidos + 18 excluidos)\n")
        
        if len(incluidos) + len(excluidos) == 51:
            f.write("   ✅ VALIDACIÓN EXITOSA\n")
        else:
            f.write("   ❌ VALIDACIÓN FALLIDA — Revisar manualmente\n")
        
        f.write("\n" + "="*70 + "\n")
    
    print(f"📝 Log generado: {ruta_log}")

# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def main():
    print(f"\n{'='*70}")
    print(f"GENERAR LISTA DE 51 REGISTROS — PRISMA 2020")
    print(f"Manuscrito: Swarm Intelligence for Multi-UAV Path Planning")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    print("📂 Paso 1: Cargando 33 estudios incluidos...")
    incluidos = cargar_incluidos(ARCHIVO_INCLUIDOS)
    
    if len(incluidos) != 33:
        print(f"⚠️  ALERTA: Se esperaban 33 incluidos, se cargaron {len(incluidos)}")
    
    print("\n📂 Paso 2: Cargando y filtrando estudios excluidos...")
    excluidos, excluidos_filtrados = cargar_y_filtrar_excluidos(
        ARCHIVO_EXCLUIDOS, 
        IDS_FUERA_PERIODO
    )
    
    print("\n📂 Paso 3: Estandarizando IDs de excluidos...")
    excluidos = estandarizar_ids_excluidos(excluidos)
    
    print("\n📂 Paso 4: Verificando duplicados por DOI...")
    duplicados = verificar_duplicados(incluidos, excluidos)
    
    print("\n📂 Paso 5: Generando CSV final para coautor...")
    df_final = generar_csv_final(incluidos, excluidos, ARCHIVO_SALIDA)
    
    print("\n📂 Paso 6: Generando log de procesamiento...")
    generar_log(incluidos, excluidos, excluidos_filtrados, duplicados, ARCHIVO_LOG)
    
    print("\n📋 Validación final:")
    total = len(incluidos) + len(excluidos)
    if total == 51:
        print(f"   ✅ Total correcto: {total} registros (33 incluidos + 18 excluidos)")
        print(f"   ✅ Archivo listo para enviar al coautor")
    else:
        print(f"   ❌ Total incorrecto: {total} registros (se esperan 51)")
        print(f"   ⚠️  Revisar manualmente antes de enviar")
    
    return df_final

# ============================================================================
# EJECUCIÓN
# ============================================================================

if __name__ == '__main__':
    df = main()