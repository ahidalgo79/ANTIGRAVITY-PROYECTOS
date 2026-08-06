import os
from pathlib import Path
from datetime import datetime

BASE = Path("/home/andres/Documentos/ANTIGRAVITY-PROYECTOS/Comea/Black_Bears_Proyecto_FPV_2026")

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✔ {path.relative_to(BASE)}")

TODAY = "2026-07-06"

# ========================
# 00 — GESTIÓN Y ADMINISTRACIÓN
# ========================

write(BASE / "00_Gestion_y_Administracion/02_Presupuesto/Formas_Pago_Alumnos/Forma_Pago_Alumnos.md", f"""# Forma de Pago — Alumnos Black Bears 2026

## Datos del alumno
- Nombre completo: ___________________________________________
- Matrícula: _________________________________________________
- Grupo/Equipo: ______________________________________________
- Teléfono: __________________________________________________
- Correo institucional: ______________________________________

## Concepto de pago
- [ ] Inscripción al proyecto Black Bears FPV 2026
- [ ] Compra de componentes (motores, ESC, FC, frame, etc.)
- [ ] Repuestos / Reparaciones
- [ ] Logística (transporte, hospedaje, alimentación)
- [ ] Otro: __________________________________________________

## Monto
- Cantidad: $ _______________
- Fecha de pago: ___ / ___ / 2026
- Método de pago: [ ] Efectivo  [ ] Transferencia  [ ] Tarjeta

## Comprobante
- Folio de comprobante: _______________
- Recibido por: ________________________

---
*Generado: {TODAY} — Proyecto Black Bears FPV 2026*
""")

write(BASE / "00_Gestion_y_Administracion/03_Viaje_y_Logistica/Datos_Hospedaje_Alumnos/Datos_Hospedaje.md", f"""# Datos de Hospedaje — Alumnos Black Bears 2026

## Información personal
- Nombre: ____________________________________________________
- Teléfono emergencia: ________________________________________
- Alergias / condiciones médicas: ______________________________

## Hospedaje
- Lugar: _____________________________________________________
- Dirección: _________________________________________________
- Check-in: ___ / ___ / 2026  ___ : ___ hrs
- Check-out: ___ / ___ / 2026  ___ : ___ hrs
- Habitación #: _______________
- Contacto del lugar: _________________________________________

## Compañeros de habitación
1. ___________________________________________________________
2. ___________________________________________________________
3. ___________________________________________________________

## Transporte
- Llegada: [ ] Propio  [ ] Grupo  [ ] Otro: __________________
- Salida:  [ ] Propio  [ ] Grupo  [ ] Otro: __________________

## Observaciones
_______________________________________________________________
_______________________________________________________________

---
*Generado: {TODAY} — Proyecto Black Bears FPV 2026*
""")

write(BASE / "00_Gestion_y_Administracion/03_Viaje_y_Logistica/Autorizaciones_Firmadas/Autorizacion_Viaje.md", f"""# AUTORIZACIÓN DE VIAJE Y PARTICIPACIÓN
## Proyecto Black Bears — Drones FPV 2026

Yo, __________________________________________________________,
padre/madre/tutor del alumno __________________________________
matrícula ____________________, autorizo su participación en las
actividades del proyecto Black Bears FPV 2026, incluyendo:

- [ ] Talleres de armado y configuración
- [ ] Pruebas de vuelo en campo
- [ ] Competencia oficial
- [ ] Viaje a sede de competencia

 así como el uso de su imagen para fines documentales del proyecto.

Firma del tutor: ___________________________  
Fecha: ___ / ___ / 2026  
Teléfono de contacto: ______________________

---
*Generado: {TODAY} — Proyecto Black Bears FPV 2026*
""")

# ========================
# 01 — INVESTIGACIÓN Y VINCULACIÓN
# ========================

write(BASE / "01_Investigacion_y_Vinculacion/Cluster_Aeroespacial/Contacto_Inicial/Registro_Contacto_Cluster.md", f"""# Registro de Contacto Inicial
## Clúster Aeroespacial de Sonora

- Fecha: {TODAY}
- Contacto: ___________________________________________________
- Cargo/Organización: _________________________________________
- Medio: [ ] Correo  [ ] Llamada  [ ] Reunión presencial  [ ] Otro

## Asunto
_______________________________________________________________

## Acuerdos iniciales
1. ___________________________________________________________
2. ___________________________________________________________
3. ___________________________________________________________

## Próximos pasos
- [ ] Enviar documentación del proyecto
- [ ] Agendar reunión de seguimiento
- Fecha tentativa: ___ / ___ / 2026

---
*Proyecto Black Bears FPV 2026*
""")

write(BASE / "01_Investigacion_y_Vinculacion/Cluster_Aeroespacial/Memorias_Reunion/Minuta_Reunion_Cluster.md", f"""# Minuta de Reunión — Clúster Aeroespacial

- Fecha: ___ / ___ / 2026
- Hora: ___ : ___ hrs
- Lugar: _____________________________________________________
- Asistentes: _________________________________________________
_______________________________________________________________

## Orden del día
1. ___________________________________________________________
2. ___________________________________________________________
3. ___________________________________________________________

## Acuerdos
| # | Acuerdo | Responsable | Fecha límite |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## Próxima reunión
- Fecha: ___ / ___ / 2026
- Hora: ___ : ___ hrs

---
*Proyecto Black Bears FPV 2026*
""")

write(BASE / "01_Investigacion_y_Vinculacion/Cluster_Aeroespacial/Compromisos_y_Seguimiento/Seguimiento_Compromisos.md", f"""# Seguimiento de Compromisos — Clúster Aeroespacial

| # | Compromiso | Responsable | Fecha | Estatus | Notas |
|---|---|---|---|---|---|
| 1 | | | | ⬜ Pendiente | |
| 2 | | | | ⬜ Pendiente | |
| 3 | | | | ⬜ Pendiente | |
| 4 | | | | ⬜ Pendiente | |
| 5 | | | | ⬜ Pendiente | |

**Leyenda:** ✅ Completado  🔄 En proceso  ⬜ Pendiente  ❌ Cancelado

---
*Generado: {TODAY} — Proyecto Black Bears FPV 2026*
""")

# ========================
# 02 — INGENIERÍA TÉCNICA
# ========================

write(BASE / "02_Ingenieria_Tecnica/01_Diseno/Diagramas_Electricos/README.md", """# Diagramas Eléctricos

Colocar aquí los diagramas electrónicos del dron:
- Conexión de ESC a motor
- Distribución de potencia (PDB)
- Conexión de receptor FC
- Diagrama de cableado general
- Esquema de baterías y BEC

Formato sugerido: PDF, PNG o archivos de KiCad/Eagle/Fritzing.
""")

write(BASE / "02_Ingenieria_Tecnica/01_Diseno/Planos_Frame/README.md", """# Planos del Frame

Colocar aquí los planos del frame del dron:
- Planos CAD (DXF, STEP, STL)
- Medidas y dimensiones
- Especificaciones de materiales
- Puntos de montaje de componentes

Formato sugerido: PDF, DXF, STEP.
""")

write(BASE / "02_Ingenieria_Tecnica/02_Armado_Dron_Principal/Fotos_Proceso/README.md", """# Fotos del Proceso — Dron Principal

Colocar aquí las fotografías del proceso de armado del dron principal,
ordenadas cronológicamente.

Formato: JPEG/PNG. Nombrar con prefijo numérico (01_preparacion_base.jpg,
02_montaje_motores.jpg, etc.)
""")

write(BASE / "02_Ingenieria_Tecnica/03_Armado_Dron_Repuesto/Fotos_Proceso/README.md", """# Fotos del Proceso — Dron de Repuesto

Colocar aquí las fotografías del proceso de armado del dron de repuesto.

Formato: JPEG/PNG. Nombrar con prefijo numérico.
""")

write(BASE / "02_Ingenieria_Tecnica/04_Configuracion_Software/BetaFlight_Config_Backup/README.md", """# BetaFlight — Config Backup

Colocar aquí los respaldos de configuración de BetaFlight:
- Archivos .txt con dump de CLI
- Diferencias entre versiones
- Perfiles de configuración

Formato: .txt o .md con el dump de configuración.
""")

write(BASE / "02_Ingenieria_Tecnica/04_Configuracion_Software/PIDs_Tuning/Registro_PIDs.md", f"""# Registro de Ajuste de PIDs — Black Bears FPV

## Configuración base
- FC: __________________  |  Firmware: BetaFlight ___ . ___ . ___
- Frame: ________________ |  Peso: ________ g
- Motores: ______________ |  ESC: ____________
- Hélice: _______________ |  Batería: _________

## Historial de ajustes

| Fecha | Vuelo | Roll P/I/D | Pitch P/I/D | Yaw P/I/D | Notas |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

## Observaciones

---
*Proyecto Black Bears FPV 2026 — {TODAY}*
""")

write(BASE / "02_Ingenieria_Tecnica/05_Seguridad/Bolsa_Transporte_Baterias/Checklist_Seguridad_Baterias.md", f"""# Checklist de Seguridad — Baterías LiPo

## Antes del vuelo
- [ ] Batería sin abolladuras ni deformaciones
- [ ] Voltaje de celda: ___ V / ___ V / ___ V / ___ V  (mín 3.7V)
- [ ] Conectores limpios y sin daños
- [ ] Bolsa ignífuga disponible

## Durante el vuelo
- [ ] Monitor de voltaje activado (alarma < 3.5V/celda)
- [ ] Tiempo de vuelo programado: ___ min

## Después del vuelo
- [ ] Voltaje post-vuelo: ___ V / ___ V / ___ V / ___ V
- [ ] Batería almacenada en modo STORAGE (3.8V/celda)
- [ ] Guardada en bolsa ignífuga

## Transporte
- [ ] Baterías en bolsa ignífuga individual
- [ ] Terminales protegidas (cinta aislante o caps)
- [ ] No transportar con carga completa (>80%)

---
*Proyecto Black Bears FPV 2026 — {TODAY}*
""")

# ========================
# 03 — PRUEBAS Y VUELOS
# ========================

write(BASE / "03_Pruebas_y_Vuelos/Vuelo_01_2026-07-02/Clips_Relevantes/README.md", """# Clips Relevantes — Vuelo 01 (2026-07-02)

Colocar aquí los videos del primer vuelo de pruebas.
Nombre sugerido: `vuelo01_take01.mp4`, `vuelo01_take02.mp4`, etc.
""")

write(BASE / "03_Pruebas_y_Vuelos/Vuelo_01_2026-07-02/Fotos/README.md", """# Fotos — Vuelo 01 (2026-07-02)

Colocar aquí las fotografías del primer vuelo de pruebas.
""")

write(BASE / "03_Pruebas_y_Vuelos/Vuelo_02_2026-07-02/Clips_Relevantes/README.md", """# Clips Relevantes — Vuelo 02 (2026-07-02)

Colocar aquí los videos del segundo vuelo de pruebas.
""")

write(BASE / "03_Pruebas_y_Vuelos/Vuelo_02_2026-07-02/Fotos/README.md", """# Fotos — Vuelo 02 (2026-07-02)

Colocar aquí las fotografías del segundo vuelo de pruebas.
""")

write(BASE / "03_Pruebas_y_Vuelos/Pruebas_Laberinto/Registro_Pruebas_Laberinto.md", f"""# Registro de Pruebas — Circuito Laberinto

## Configuración
- Tamaño del laberinto: ___ x ___ m
- Altura de paredes: ___ cm
- Número de obstáculos: ___
- Tiempo límite: ___ s

## Resultados

| Vuelo | Tiempo | Toques/Colisiones | Penalización | Tiempo final | Piloto | Notas |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |
| 4 | | | | | | |
| 5 | | | | | | |

## Observaciones
_______________________________________________________________
_______________________________________________________________

---
*Proyecto Black Bears FPV 2026 — {TODAY}*
""")

# ========================
# 04 — REPORTE A1
# ========================

write(BASE / "04_Reporte_A1/00_Plantilla_IEEE/Referencia_Plantilla_IEEE.md", """# Plantilla IEEE — Reporte A1

El reporte A1 debe seguir el formato IEEE Transaction style.

## Recursos
- Plantilla oficial LaTeX: https://www.ieee.org/conferences/publishing/templates.html
- Plantilla oficial Word: Misma URL
- Overleaf: Buscar "IEEE Conference Template"

## Estructura sugerida
1. **Abstract** — Resumen del proyecto (150-250 palabras)
2. **Introduction** — Contexto, motivación, objetivo
3. **Methodology** — Diseño, componentes, configuración
4. **Results** — Pruebas de vuelo, desempeño, laberinto
5. **Conclusions** — Resultados, aprendizajes, trabajo futuro
6. **References** — Formato IEEE

## Formato
- Dos columnas
- Times New Roman 10pt
- Figuras en PNG/JPG a 300 DPI
- Referencias en formato IEEE [1], [2], etc.
""")

write(BASE / "04_Reporte_A1/01_Borradores_Seccion/Miguel_Circuito_Laberintos/evidencias/README.md", """# Evidencias — Miguel: Circuito Laberintos

Colocar aquí las evidencias del trabajo de Miguel Andujo sobre
el circuito de laberintos: fotos, videos, diagramas, código.
""")

write(BASE / "04_Reporte_A1/03_Capturas_Figuras/README.md", """# Capturas y Figuras — Reporte A1

Colocar aquí las figuras, gráficas y capturas de pantalla para
el reporte A1. Nombrar como `fig01_descripcion.png`, etc.

Formatos: PNG (300 DPI), JPG, SVG.
""")

# ========================
# 05 — BITÁCORA GENERAL
# ========================

write(BASE / "05_Bitacora_General/Bitacora_Semanal/Bitacora_Semana_01.md", f"""# Bitácora Semanal — Semana 1

**Período:** {TODAY} al ___ / ___ / 2026

## Actividades realizadas
- Lunes: ______________________________________________________
- Martes: _____________________________________________________
- Miércoles: __________________________________________________
- Jueves: _____________________________________________________
- Viernes: ____________________________________________________
- Sábado: _____________________________________________________

## Acuerdos de la semana
1. ___________________________________________________________
2. ___________________________________________________________
3. ___________________________________________________________

## Pendientes para la siguiente semana
- [ ] ________________________________________________________
- [ ] ________________________________________________________
- [ ] ________________________________________________________

---
*Black Bears FPV 2026*
""")

write(BASE / "05_Bitacora_General/Minutas_Reunion/Minuta_Reunion_01.md", f"""# Minuta de Reunión 01

- Fecha: ___ / ___ / 2026
- Hora: ___ : ___ hrs
- Lugar / Modalidad: _________________________________________
- Convocada por: ______________________________________________

## Asistentes
- [ ] Andrés Hidalgo (Asesor)
- [ ] Tamara Peinado (Coordinadora)
- [ ] Miguel Andujo
- [ ] Oswaldo _____________
- [ ] Otros: __________________________________________________

## Temas tratados
1. ___________________________________________________________
2. ___________________________________________________________
3. ___________________________________________________________

## Acuerdos y compromisos

| Actividad | Responsable | Fecha |
|---|---|---|
| | | |
| | | |
| | | |

## Próxima reunión
- Fecha: ___ / ___ / 2026  —  ___ : ___ hrs

---
*Black Bears FPV 2026*
""")

write(BASE / "05_Bitacora_General/Decisiones_Tecnicas/Registro_Decisiones_Tecnicas.md", f"""# Registro de Decisiones Técnicas — Black Bears FPV

| # | Fecha | Decisión | Justificación | Responsable | Estatus |
|---|---|---|---|---|---|
| 1 | | | | | ✅ |
| 2 | | | | | ✅ |
| 3 | | | | | ✅ |

## Detalle de decisiones

### Decisión 1: _______________________________________________

_______________________________________________________________

### Decisión 2: _______________________________________________

_______________________________________________________________

### Decisión 3: _______________________________________________

_______________________________________________________________

---
*Proyecto Black Bears FPV 2026 — Iniciado: {TODAY}*
""")

# ========================
# 06 — COMUNICACIONES
# ========================

write(BASE / "06_Comunicaciones/Correos_Institucionales/Plantilla_Correo.md", """# Plantilla de Correo Institucional

**Para:** [destinatario]
**CC:** [copias]
**Asunto:** Proyecto Black Bears FPV 2026 — [asunto específico]

---

Estimado/a [nombre],

Por medio del presente, [mensaje...]

Quedo atento a su respuesta.

Atentamente,

[Nombre]
[Teléfono]
[Correo]
Black Bears FPV 2026 — COMEA
""")

write(BASE / "06_Comunicaciones/Mensajes_Tamara_Coordinacion/README.md", """# Mensajes — Coordinación con Tamara Peinado

Colocar aquí capturas de pantalla o transcripciones de mensajes
importantes con Tamara (coordinadora del proyecto).

Incluir fecha y asunto en el nombre del archivo.
""")

# ========================
# 09 — BACKUP Y ARCHIVO
# ========================

write(BASE / "09_Backup_y_Archivo/Respaldos_Automaticos/README.md", """# Respaldos Automáticos

Colocar aquí los respaldos automáticos del proyecto.
Incluir fecha en el nombre del archivo: `backup_YYYY-MM-DD.zip`
""")

write(BASE / "09_Backup_y_Archivo/Versiones_Antiguas/README.md", """# Versiones Antiguas

Colocar aquí versiones anteriores de documentos y archivos
que han sido reemplazados por versiones más recientes.

Nombrar como: `documento_vX.Y_YYYY-MM-DD.ext`
""")

print(f"\n✅ Todos los documentos generados en: {BASE}")
