import os

# Estructura de carpetas
estructura = {
    "00_Gestion_y_Administracion": [
        "01_Planeacion",
        "02_Presupuesto/Comprobantes_Pago",
        "02_Presupuesto/Formas_Pago_Alumnos",
        "03_Viaje_y_Logistica/Datos_Hospedaje_Alumnos",
        "03_Viaje_y_Logistica/Autorizaciones_Firmadas"
    ],
    "01_Investigacion_y_Vinculacion": [
        "Cluster_Aeroespacial/Contacto_Inicial",
        "Cluster_Aeroespacial/Memorias_Reunion",
        "Cluster_Aeroespacial/Compromisos_y_Seguimiento",
        "Estado_del_Arte",
        "Normativa_y_Rubricas"
    ],
    "02_Ingenieria_Tecnica": [
        "01_Diseno/Diagramas_Electricos",
        "01_Diseno/Planos_Frame",
        "01_Diseno/Seleccion_Componentes",
        "02_Armado_Dron_Principal/Fotos_Proceso",
        "03_Armado_Dron_Repuesto/Fotos_Proceso",
        "04_Configuracion_Software/BetaFlight_Config_Backup",
        "04_Configuracion_Software/PIDs_Tuning",
        "05_Seguridad/Bolsa_Transporte_Baterias"
    ],
    "03_Pruebas_y_Vuelos": [
        "Vuelo_01_2026-07-02/Clips_Relevantes",
        "Vuelo_01_2026-07-02/Fotos",
        "Vuelo_02_2026-07-02/Clips_Relevantes",
        "Vuelo_02_2026-07-02/Fotos",
        "Pruebas_Laberinto"
    ],
    "04_Reporte_A1": [
        "00_Plantilla_IEEE",
        "01_Borradores_Seccion/Miguel_Circuito_Laberintos/evidencias",
        "02_Versiones_Integradas",
        "03_Capturas_Figuras"
    ],
    "05_Bitacora_General": [
        "Bitacora_Semanal",
        "Minutas_Reunion",
        "Decisiones_Tecnicas"
    ],
    "06_Comunicaciones": [
        "WhatsApp_Capturas/Evidencias_Acuerdos",
        "Correos_Institucionales",
        "Mensajes_Tamara_Coordinacion"
    ],
    "09_Backup_y_Archivo": [
        "Respaldos_Automaticos",
        "Versiones_Antiguas"
    ]
}

# Crear carpeta raíz
raiz = "Black_Bears_Proyecto_FPV_2026"
os.makedirs(raiz, exist_ok=True)

# Crear subcarpetas
for carpeta_principal, subcarpetas in estructura.items():
    for sub in subcarpetas:
        ruta_completa = os.path.join(raiz, carpeta_principal, sub)
        os.makedirs(ruta_completa, exist_ok=True)
        print(f"Creada: {ruta_completa}")

# Crear archivo README
readme = """# Proyecto Black Bears - Drones FPV 2026

## Equipo
- Asesor: Ing. Andres Hidalgo
- Coordinadora: Tamara Peinado
- Integrantes: Miguel Andujo, Oswaldo, [completar]

## Objetivo
Desarrollo de drones FPV para competencias de velocidad y laberintos,
con reporte academico A1 en formato IEEE y vinculacion con el
Cluster Aeroespacial de Sonora.

## Estructura del Proyecto
- 00_Gestion_y_Administracion/ - Logistica, viaje, presupuesto
- 01_Investigacion_y_Vinculacion/ - Cluster, estado del arte, rubricas
- 02_Ingenieria_Tecnica/ - Diseno, armado, configuracion
- 03_Pruebas_y_Vuelos/ - Evidencias de vuelos organizadas por fecha
- 04_Reporte_A1/ - Documento IEEE y borradores por alumno
- 05_Bitacora_General/ - Minutas, bitacora semanal
- 06_Comunicaciones/ - Capturas de acuerdos importantes
- 09_Backup_y_Archivo/ - Respaldos

## Convenciones
- Fechas: AAAA-MM-DD
- Versiones: vX.X_AAAA-MM-DD
- Sin espacios en nombres de archivos (usar guion bajo _)

## Contacto
- Asesor: [correo]
- Coordinadora: [correo]
"""

with open(os.path.join(raiz, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)

print(f"\nEstructura creada exitosamente en: {os.path.abspath(raiz)}")