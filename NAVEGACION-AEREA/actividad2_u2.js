const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, HeadingLevel, BorderStyle, WidthType, ShadingType,
  LevelFormat, PageNumber, NumberFormat, Footer, Header
} = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "AAAAAA" };
const borders = { top: border, bottom: border, left: border, right: border };
const thickBorder = { style: BorderStyle.SINGLE, size: 4, color: "1F497D" };
const thickBorders = { top: thickBorder, bottom: thickBorder, left: thickBorder, right: thickBorder };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

const cellMargin = { top: 100, bottom: 100, left: 150, right: 150 };

function heading1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 300, after: 120 },
    children: [new TextRun({ text, bold: true, size: 28, font: "Arial", color: "1F497D" })]
  });
}

function heading2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 200, after: 80 },
    children: [new TextRun({ text, bold: true, size: 24, font: "Arial", color: "2E74B5" })]
  });
}

function body(text, options = {}) {
  return new Paragraph({
    spacing: { before: 60, after: 60 },
    alignment: options.justify ? AlignmentType.JUSTIFIED : AlignmentType.LEFT,
    children: [new TextRun({ text, font: "Arial", size: 22, ...options })]
  });
}

function bold(text) {
  return new Paragraph({
    spacing: { before: 60, after: 60 },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 22 })]
  });
}

function bullet(text, ref = "bullets") {
  return new Paragraph({
    numbering: { reference: ref, level: 0 },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, font: "Arial", size: 22 })]
  });
}

function bulletBold(label, rest) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { before: 40, after: 40 },
    children: [
      new TextRun({ text: label, bold: true, font: "Arial", size: 22 }),
      new TextRun({ text: rest, font: "Arial", size: 22 })
    ]
  });
}

function spacer() {
  return new Paragraph({ spacing: { before: 60, after: 60 }, children: [new TextRun("")] });
}

function sectionDivider(text) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [
      new TableRow({
        children: [
          new TableCell({
            borders: noBorders,
            shading: { fill: "1F497D", type: ShadingType.CLEAR },
            margins: cellMargin,
            width: { size: 9360, type: WidthType.DXA },
            children: [new Paragraph({
              alignment: AlignmentType.LEFT,
              children: [new TextRun({ text, bold: true, font: "Arial", size: 24, color: "FFFFFF" })]
            })]
          })
        ]
      })
    ]
  });
}

// ─── CARTA INFO TABLE ─────────────────────────────────────────────────────────
function cartasTable() {
  function hCell(text, width) {
    return new TableCell({
      borders,
      shading: { fill: "2E74B5", type: ShadingType.CLEAR },
      margins: cellMargin,
      width: { size: width, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text, bold: true, font: "Arial", size: 20, color: "FFFFFF" })] })]
    });
  }
  function dCell(text, width, shade = "FFFFFF") {
    return new TableCell({
      borders,
      shading: { fill: shade, type: ShadingType.CLEAR },
      margins: cellMargin,
      width: { size: width, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 20 })] })]
    });
  }

  const cartas = [
    ["1", "Carta de Aeródromo (AD)", "Identificar pista en uso, elevación del aeropuerto y ubicación del estacionamiento (Parking) de salida."],
    ["2", "SID — Salida por Instrumentos", "Elegir una salida para la pista activa. Identificar: nombre, primer waypoint, rumbo inicial y altitud de restricción."],
    ["3", "Carta En-ruta (Low / High)", "Trazar la ruta. Identificar al menos 2 VORs/NDBs, 2 intersecciones (fixes) y el airway que conecta ambos aeropuertos."],
    ["4", "STAR — Llegada Estándar", "Seleccionar una llegada al destino. Identificar: transición, último waypoint antes de la aproximación y altitud esperada."],
    ["5", "Carta de Aproximación por Instrumentos", "Elegir ILS, VOR o RNAV/GPS. Identificar: frecuencia del ayudante, curso final, altitud de decisión (DA) o altitud mínima de descenso (MDA)."],
  ];

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [500, 2300, 6560],
    rows: [
      new TableRow({
        children: [
          hCell("#", 500),
          hCell("Tipo de Carta", 2300),
          hCell("Qué debe hacer el equipo", 6560),
        ]
      }),
      ...cartas.map(([num, tipo, que], i) =>
        new TableRow({
          children: [
            dCell(num, 500, i % 2 === 0 ? "EBF3FB" : "FFFFFF"),
            dCell(tipo, 2300, i % 2 === 0 ? "EBF3FB" : "FFFFFF"),
            dCell(que, 6560, i % 2 === 0 ? "EBF3FB" : "FFFFFF"),
          ]
        })
      )
    ]
  });
}

// ─── BITÁCORA TABLE (IDA) ────────────────────────────────────────────────────
function bitacoraIdaTable() {
  function hCell(text, width) {
    return new TableCell({
      borders,
      shading: { fill: "D6E4F0", type: ShadingType.CLEAR },
      margins: cellMargin,
      width: { size: width, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text, bold: true, font: "Arial", size: 18 })] })]
    });
  }
  function emptyCell(width) {
    return new TableCell({
      borders, margins: cellMargin, width: { size: width, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 18 })] })]
    });
  }

  const tramos = ["Salida (SID)", "En-ruta (Fix 1)", "En-ruta (Fix 2)", "Llegada (STAR)", "Aproximación Final"];

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1400, 1600, 1200, 1200, 1200, 2760],
    rows: [
      new TableRow({
        children: [
          hCell("Tramo / Waypoint", 1400),
          hCell("Carta de Ref.", 1600),
          hCell("Altitud (ft)", 1200),
          hCell("Rumbo (°)", 1200),
          hCell("Dist. (nm)", 1200),
          hCell("Observaciones (viento, desviaciones, notas)", 2760),
        ]
      }),
      ...tramos.map(tramo =>
        new TableRow({
          children: [
            emptyCell(1400),
            emptyCell(1600),
            emptyCell(1200),
            emptyCell(1200),
            emptyCell(1200),
            emptyCell(2760),
          ]
        })
      )
    ]
  });
}

// ─── BITÁCORA TABLE (REGRESO) ────────────────────────────────────────────────
function bitacoraRegresoTable() {
  function hCell(text, width) {
    return new TableCell({
      borders,
      shading: { fill: "D6E4F0", type: ShadingType.CLEAR },
      margins: cellMargin,
      width: { size: width, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text, bold: true, font: "Arial", size: 18 })] })]
    });
  }
  function emptyCell(width) {
    return new TableCell({
      borders, margins: cellMargin, width: { size: width, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 18 })] })]
    });
  }

  const tramos = ["Salida (SID)", "En-ruta", "Aproximación"];

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [1400, 1600, 1400, 1400, 3560],
    rows: [
      new TableRow({
        children: [
          hCell("Tramo / Waypoint", 1400),
          hCell("Carta de Ref.", 1600),
          hCell("Altitud (ft)", 1400),
          hCell("Rumbo (°)", 1400),
          hCell("Observaciones", 3560),
        ]
      }),
      ...tramos.map(tramo =>
        new TableRow({
          children: [
            emptyCell(1400),
            emptyCell(1600),
            emptyCell(1400),
            emptyCell(1400),
            emptyCell(3560),
          ]
        })
      )
    ]
  });
}

// ─── RÚBRICA TABLE ────────────────────────────────────────────────────────────
function rubricaTable() {
  function hCell(text, width) {
    return new TableCell({
      borders,
      shading: { fill: "1F497D", type: ShadingType.CLEAR },
      margins: cellMargin,
      width: { size: width, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text, bold: true, font: "Arial", size: 20, color: "FFFFFF" })] })]
    });
  }
  function dCell(text, width, shade = "FFFFFF") {
    return new TableCell({
      borders,
      shading: { fill: shade, type: ShadingType.CLEAR },
      margins: cellMargin,
      width: { size: width, type: WidthType.DXA },
      children: [new Paragraph({ children: [new TextRun({ text, font: "Arial", size: 20 })] })]
    });
  }

  const criteria = [
    ["1. Bitácora de Vuelo", "Está impresa, llenada a mano, firmada y los datos coinciden lógicamente con el reporte y el video. Incluye vuelo de ida (MMMZ→MMCN) y regreso (MMCN→MMMZ).", "20"],
    ["2. Uso de Cartas", "Identifica y describe correctamente las 5 cartas para ambos aeropuertos. Las imágenes de las cartas son legibles y el texto explica el dato crítico extraído de cada una.", "20"],
    ["3. Interpretación G1000", "Las capturas de pantalla del PFD/MFD están correctamente etiquetadas. El análisis explica claramente la relación entre lo que dice la carta y lo que muestra el instrumento en la ruta Mazatlán–Ciudad Obregón.", "20"],
    ["4. Reporte Escrito", "Sigue la estructura solicitada, redacción profesional, sin faltas de ortografía, conclusiones reflexivas y referencias APA 7. Peso del archivo < 5 MB.", "20"],
    ["5. Evidencia en Video", "El video (mín. 5 min) muestra claramente las pantallas del G1000 durante las transiciones clave. Se aprecia la programación del FMS y la ejecución de la aproximación en MMMZ y MMCN.", "20"],
  ];

  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [2500, 4900, 1960],
    rows: [
      new TableRow({
        children: [
          hCell("Criterio", 2500),
          hCell("Descripción Detallada", 4900),
          hCell("Puntaje", 1960),
        ]
      }),
      ...criteria.map(([crit, desc, pts], i) =>
        new TableRow({
          children: [
            dCell(crit, 2500, i % 2 === 0 ? "EBF3FB" : "FFFFFF"),
            dCell(desc, 4900, i % 2 === 0 ? "EBF3FB" : "FFFFFF"),
            dCell(pts, 1960, i % 2 === 0 ? "EBF3FB" : "FFFFFF"),
          ]
        })
      ),
      new TableRow({
        children: [
          new TableCell({
            borders,
            shading: { fill: "1F497D", type: ShadingType.CLEAR },
            margins: cellMargin,
            columnSpan: 2,
            width: { size: 7400, type: WidthType.DXA },
            children: [new Paragraph({ children: [new TextRun({ text: "TOTAL", bold: true, font: "Arial", size: 22, color: "FFFFFF" })] })]
          }),
          new TableCell({
            borders,
            shading: { fill: "1F497D", type: ShadingType.CLEAR },
            margins: cellMargin,
            width: { size: 1960, type: WidthType.DXA },
            children: [new Paragraph({ children: [new TextRun({ text: "100", bold: true, font: "Arial", size: 22, color: "FFFFFF" })] })]
          }),
        ]
      })
    ]
  });
}

// ─── DOCUMENT ─────────────────────────────────────────────────────────────────
const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2022",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers2",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers3",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "numbers4",
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: "%1.",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
      {
        reference: "checklist",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "\u2610",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      },
    ]
  },
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial", color: "1F497D" },
        paragraph: { spacing: { before: 300, after: 120 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial", color: "2E74B5" },
        paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 1 }
      },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "2E74B5", space: 1 } },
            spacing: { after: 100 },
            children: [
              new TextRun({ text: "Navegación Aérea  |  Unidad 2  |  MMMZ ↔ MMCN", font: "Arial", size: 18, color: "555555" }),
            ]
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            border: { top: { style: BorderStyle.SINGLE, size: 6, color: "2E74B5", space: 1 } },
            alignment: AlignmentType.RIGHT,
            children: [
              new TextRun({ text: "Página ", font: "Arial", size: 18, color: "555555" }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "555555" }),
              new TextRun({ text: " de ", font: "Arial", size: 18, color: "555555" }),
              new TextRun({ children: [PageNumber.TOTAL_PAGES], font: "Arial", size: 18, color: "555555" }),
            ]
          })
        ]
      })
    },
    children: [

      // ── PORTADA ──────────────────────────────────────────────────────────────
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [9360],
        rows: [
          new TableRow({
            children: [new TableCell({
              borders: thickBorders,
              shading: { fill: "1F497D", type: ShadingType.CLEAR },
              margins: { top: 400, bottom: 400, left: 400, right: 400 },
              width: { size: 9360, type: WidthType.DXA },
              children: [
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  spacing: { before: 200, after: 80 },
                  children: [new TextRun({ text: "UNIVERSIDAD POLITÉCNICA DE CHIHUAHUA", bold: true, font: "Arial", size: 26, color: "FFFFFF" })]
                }),
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  spacing: { before: 0, after: 200 },
                  children: [new TextRun({ text: "Navegación Aérea — Unidad 2", font: "Arial", size: 22, color: "D0E8FF" })]
                }),
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  spacing: { before: 0, after: 100 },
                  children: [new TextRun({ text: "Actividad 2", bold: true, font: "Arial", size: 40, color: "FFFFFF" })]
                }),
                new Paragraph({
                  alignment: AlignmentType.CENTER,
                  spacing: { before: 0, after: 200 },
                  children: [new TextRun({ text: "Planificación y Ejecución de Vuelo con Cartas Aeronáuticas y Garmin G1000", font: "Arial", size: 26, color: "D0E8FF" })]
                }),
              ]
            })]
          })
        ]
      }),

      spacer(),

      // Datos de identificación
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [3000, 4360, 2000],
        rows: [
          new TableRow({
            children: [
              new TableCell({
                borders, margins: cellMargin, width: { size: 7360, type: WidthType.DXA },
                columnSpan: 2,
                shading: { fill: "EBF3FB", type: ShadingType.CLEAR },
                children: [
                  new Paragraph({ children: [new TextRun({ text: "Integrantes (Nombre completo y matrícula):", bold: true, font: "Arial", size: 20 })] }),
                  new Paragraph({ children: [new TextRun({ text: "1. ___________________________________________", font: "Arial", size: 20 })] }),
                  new Paragraph({ children: [new TextRun({ text: "2. ___________________________________________", font: "Arial", size: 20 })] }),
                  new Paragraph({ children: [new TextRun({ text: "3. ___________________________________________", font: "Arial", size: 20 })] }),
                ]
              }),
              new TableCell({
                borders, margins: cellMargin, width: { size: 2000, type: WidthType.DXA },
                shading: { fill: "EBF3FB", type: ShadingType.CLEAR },
                children: [
                  new Paragraph({ children: [new TextRun({ text: "Grupo:", bold: true, font: "Arial", size: 20 })] }),
                  new Paragraph({ children: [new TextRun({ text: "___________", font: "Arial", size: 20 })] }),
                  new Paragraph({ spacing: { before: 80 }, children: [new TextRun({ text: "Fecha entrega:", bold: true, font: "Arial", size: 20 })] }),
                  new Paragraph({ children: [new TextRun({ text: "___________", font: "Arial", size: 20 })] }),
                ]
              }),
            ]
          }),
          new TableRow({
            children: [
              new TableCell({
                borders, margins: cellMargin, width: { size: 9360, type: WidthType.DXA },
                columnSpan: 3,
                shading: { fill: "FFF2CC", type: ShadingType.CLEAR },
                children: [new Paragraph({
                  children: [
                    new TextRun({ text: "Nombre del archivo a entregar: ", bold: true, font: "Arial", size: 20 }),
                    new TextRun({ text: "U2_Act2_GrupoX_EquipoY_MMMZ_MMCN.pdf", font: "Arial", size: 20, color: "CC0000" }),
                  ]
                })]
              }),
            ]
          }),
        ]
      }),

      spacer(),
      spacer(),

      // ── 1. INTRODUCCIÓN ─────────────────────────────────────────────────────
      sectionDivider("1. Introducción"),
      spacer(),
      new Paragraph({
        spacing: { before: 60, after: 60 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "Las cartas aeronáuticas son documentos esenciales para la planificación y ejecución segura de cualquier vuelo. En esta actividad, el equipo realizará un vuelo simulado de ida y vuelta entre Mazatlán (MMMZ) y Ciudad Obregón (MMCN) en Microsoft Flight Simulator X (FSX) a bordo de una aeronave equipada con el sistema aviónico Garmin G1000. El objetivo es identificar, interpretar y aplicar en tiempo real los diferentes tipos de cartas que intervienen en cada fase del vuelo, cruzando esta información con lo que muestra el equipo de navegación.",
          font: "Arial", size: 22
        })]
      }),
      spacer(),

      // ── 2. OBJETIVO DE APRENDIZAJE ──────────────────────────────────────────
      sectionDivider("2. Objetivo de Aprendizaje"),
      spacer(),
      body("Al finalizar la actividad, el alumno será capaz de:"),
      spacer(),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "Buscar, descargar e interpretar correctamente 5 tipos de cartas aeronáuticas reales (Aeródromo, SID, En-ruta, STAR y Aproximación) desde fuentes oficiales.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "Programar un plan de vuelo completo (incluyendo procedimientos de salida y llegada) en el FMS del Garmin G1000.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        numbering: { reference: "numbers", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "Ejecutar un vuelo simulado respetando las altitudes, rumbos y restricciones publicadas en las cartas, documentando el proceso mediante bitácora, reporte y evidencia en video.", font: "Arial", size: 22 })]
      }),
      spacer(),

      // ── 3. MATERIALES Y RECURSOS REQUERIDOS ─────────────────────────────────
      sectionDivider("3. Materiales y Recursos Requeridos"),
      spacer(),
      new Paragraph({
        numbering: { reference: "numbers2", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [
          new TextRun({ text: "Simulador: ", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: "Microsoft Flight Simulator X (FSX) o Prepar3D. ", font: "Arial", size: 22 }),
          new TextRun({ text: "Aeronave obligatoria:", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: "Cessna 172 SP con Garmin G1000 o Beechcraft Baron G58 con Garmin G1000.", font: "Arial", size: 22 }),
        ]
      }),
      new Paragraph({
        numbering: { reference: "numbers2", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [
          new TextRun({ text: "Cartas Aeronáuticas (Reales y vigentes): ", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: "Deben descargarse de fuentes oficiales o confiables como:", font: "Arial", size: 22 }),
        ]
      }),
      new Paragraph({
        spacing: { before: 20, after: 20 },
        indent: { left: 720 },
        children: [          new TextRun({ text: "- eAIP México: https://www.aip.gob.mx/ (Buscar cartas de MMMZ y MMCN).", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { before: 20, after: 20 },
        indent: { left: 720 },
        children: [          new TextRun({ text: "- SkyVector: https://skyvector.com/ (Configurar región a México).", font: "Arial", size: 22 })] }),
      new Paragraph({
        spacing: { before: 20, after: 20 },
        indent: { left: 720 },
        children: [new TextRun({ text: "- AIRMATE.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        numbering: { reference: "numbers2", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [
          new TextRun({ text: "Software de captura: ", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: "OBS Studio, Xbox Game Bar o NVIDIA ShadowPlay para grabar la pantalla del simulador.", font: "Arial", size: 22 }),
        ]
      }),
      new Paragraph({
        numbering: { reference: "numbers2", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [
          new TextRun({ text: "Procesador de texto: ", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: "Word o Google Docs para el reporte escrito (exportar finalmente a PDF).", font: "Arial", size: 22 }),
        ]
      }),
      new Paragraph({
        numbering: { reference: "numbers2", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [
          new TextRun({ text: "Bitácora de vuelo: ", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: "Debe imprimirse y llenarse a mano con bolígrafo durante o inmediatamente después del vuelo (ver Sección 6).", font: "Arial", size: 22 }),
        ]
      }),
      spacer(),

      // ── 4. INSTRUCCIONES DETALLADAS ─────────────────────────────────────────
      sectionDivider("4. Instrucciones Detalladas"),
      spacer(),

      heading2("Fase 1: Planificación en Tierra (Antes de encender el simulador)"),
      new Paragraph({
        spacing: { before: 60, after: 60 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({
          text: "El equipo debe trabajar en conjunto para definir la ruta. No se permite volar \"Direct-To\" en todo el trayecto; deben seguir airways o una ruta RNAV publicada.",
          font: "Arial", size: 22, italics: true, color: "555555"
        })]
      }),
      spacer(),

      new Paragraph({
        numbering: { reference: "numbers3", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [
          new TextRun({ text: "Selección de Aeropuertos: ", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: "Vuelo de ida: ", font: "Arial", size: 22 }),
          new TextRun({ text: "MMMZ (Mazatlán)", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: " → ", font: "Arial", size: 22 }),
          new TextRun({ text: "MMCN (Ciudad Obregón)", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: ". Vuelo de regreso: ", font: "Arial", size: 22 }),
          new TextRun({ text: "MMCN (Ciudad Obregón)", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: " → ", font: "Arial", size: 22 }),
          new TextRun({ text: "MMMZ (Mazatlán)", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: ".", font: "Arial", size: 22 }),
        ]
      }),
      new Paragraph({
        numbering: { reference: "numbers3", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "Análisis de Cartas: Descarguen e impriman las siguientes cartas. Para cada una, identifiquen y anoten los datos críticos:", font: "Arial", size: 22 })]
      }),
      spacer(),
      cartasTable(),
      spacer(),
      new Paragraph({
        numbering: { reference: "numbers3", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({
          text: "Plan de Vuelo: Anoten en la bitácora (Sección 6) la ruta completa en formato ICAO (ej. MMMZ DCT LMM UA301 MMCN).",
          font: "Arial", size: 22
        })]
      }),
      spacer(),

      heading2("Fase 2: Ejecución del Vuelo Simulado en FSX con Garmin G1000"),
      spacer(),
      new Paragraph({
        numbering: { reference: "numbers3", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "Configuración: Inicien la grabación de video ", bold: true, font: "Arial", size: 22 }),
          new TextRun({ text: "antes", bold: true, font: "Arial", size: 22, underline: { type: "single" } }),
          new TextRun({ text: " de encender los motores. La grabación debe mostrar claramente las pantallas del G1000 (PFD y MFD).", font: "Arial", size: 22 }),
        ]
      }),
      new Paragraph({
        numbering: { reference: "numbers3", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "Programación del FMS (G1000):", bold: true, font: "Arial", size: 22 }),
        ]
      }),
      new Paragraph({
        spacing: { before: 20, after: 20 },
        indent: { left: 720 },
        children: [new TextRun({ text: "a) Presionar el botón FPL.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { before: 20, after: 20 },
        indent: { left: 720 },
        children: [new TextRun({ text: "b) Ingresar aeropuerto de salida (MMMZ) y destino (MMCN).", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { before: 20, after: 20 },
        indent: { left: 720 },
        children: [new TextRun({ text: "c) Presionar el botón PROC para seleccionar e insertar la SID elegida para MMMZ.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { before: 20, after: 20 },
        indent: { left: 720 },
        children: [new TextRun({ text: "d) Insertar manualmente los waypoints de la ruta En-ruta (si no se cargan automáticamente).", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        spacing: { before: 20, after: 20 },
        indent: { left: 720 },
        children: [new TextRun({ text: "e) Presionar PROC nuevamente para pre-cargar la STAR y la Aproximación a MMCN. Activar con ACTV solo cuando el ATC o la fase del vuelo lo indiquen.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        numbering: { reference: "numbers3", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({
          text: "Ejecución y Capturas: Durante el vuelo, asegúrense de que el video capture (o tomen capturas de pantalla adicionales para el reporte) los siguientes momentos clave:",
          font: "Arial", size: 22
        })]
      }),
      bullet("Momento 1 (Salida): Pantalla MFD mostrando la SID activa y el avión siguiendo el rumbo."),
      bullet("Momento 2 (Crucero): Pantalla PFD mostrando altitud y rumbo estabilizados, y MFD mostrando la posición sobre el Airway."),
      bullet("Momento 3 (Transición a Llegada): Pantalla MFD mostrando la activación de la STAR a MMCN."),
      bullet("Momento 4 (Aproximación Final): Pantalla PFD mostrando el localizador/glideslope (ILS) o la barra de desviación (RNAV) centrada."),
      bullet("Momento 5 (Finalización): Avión detenido en el parking de MMCN, motores apagados."),
      new Paragraph({
        numbering: { reference: "numbers3", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({
          text: "Regreso: Repetir el proceso para el vuelo de regreso MMCN → MMMZ, utilizando una SID diferente desde MMCN, una ruta en-ruta distinta si es posible y una STAR / aproximación diferente a MMMZ.",
          font: "Arial", size: 22
        })]
      }),
      spacer(),

      heading2("Fase 3: Llenado de Bitácora y Elaboración del Reporte"),
      new Paragraph({
        numbering: { reference: "numbers3", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({
          text: "Bitácora: Completen la bitácora impresa a mano con los datos reales obtenidos del simulador (no los planeados, sino los ejecutados). Debe estar firmada por el \"Piloto al Mando\" y el \"Copiloto\". Escanearla o tomarle una foto de alta calidad.",
          font: "Arial", size: 22
        })]
      }),
      new Paragraph({
        numbering: { reference: "numbers3", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({
          text: "Reporte Escrito: Elaboren un documento en PDF siguiendo estrictamente la estructura de la Sección 5.",
          font: "Arial", size: 22
        })]
      }),
      spacer(),

      // ── 5. ESTRUCTURA OBLIGATORIA DEL REPORTE ESCRITO ──────────────────────
      sectionDivider("5. Estructura Obligatoria del Reporte Escrito (Máx. 5 MB)"),
      spacer(),
      body("El reporte debe contener las siguientes secciones en este orden:"),
      spacer(),
      new Paragraph({
        numbering: { reference: "numbers4", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "Portada: Datos de la universidad, materia, actividad, integrantes, grupo y fecha.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        numbering: { reference: "numbers4", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [          new TextRun({ text: "Resumen del Plan de Vuelo: Tabla con aeropuertos (MMMZ y MMCN), aeronave, ruta completa (string de navegación), altitud de crucero y aeropuerto alternativo seleccionado.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        numbering: { reference: "numbers4", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [          new TextRun({ text: "Análisis de Cartas Aeronáuticas: Por cada una de las 5 cartas (para el vuelo de ida MMMZ→MMCN):", font: "Arial", size: 22 })]
      }),
      bullet("Insertar una imagen clara de la carta."),
      bullet("Texto breve explicando: ¿Qué dato crítico extrajeron de esta carta? (ej. \"De la carta de aproximación ILS RWY 04 de MMCN, tomamos la frecuencia 110.3 y la altitud de decisión de 2400 ft\")."),
      new Paragraph({
        numbering: { reference: "numbers4", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "Análisis del Garmin G1000:", font: "Arial", size: 22 })]
      }),
      bullet("Insertar las 5 capturas de pantalla solicitadas en la Fase 2."),
      bullet("Debajo de cada captura, explicar qué están mostrando los instrumentos y cómo coinciden con la carta aeronáutica (ej. \"En la imagen se observa el cursor magenta del FMS alineado con el radial 045° del VOR LMM, tal como indica la carta en-ruta entre MMMZ y MMCN\")."),
      new Paragraph({
        numbering: { reference: "numbers4", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "Conclusiones del Equipo: Mínimo 2 párrafos reflexionando sobre la importancia de la verificación cruzada (cross-check) entre la carta en papel/digital y lo que muestra el G1000, y los errores comunes que evitaron.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        numbering: { reference: "numbers4", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [          new TextRun({ text: "Enlace al Video: Hipervínculo visible y funcional al video de YouTube (No listado) o Google Drive. El video debe tener una duración mínima de 5 minutos y, de preferencia, incluir audio del equipo narrando brevemente las transiciones en la ruta MMMZ-MMCN.", font: "Arial", size: 22 })]
      }),
      new Paragraph({
        numbering: { reference: "numbers4", level: 0 },
        spacing: { before: 40, after: 40 },
        children: [          new TextRun({ text: "Referencias: Formato APA 7ª edición (incluir la cita de las cartas del AIP de México o SkyVector para MMMZ y MMCN).", font: "Arial", size: 22 })]
      }),
      spacer(),

      // ── 6. BITÁCORA DE VUELO ─────────────────────────────────────────────────
      sectionDivider("6. Bitácora de Vuelo (Para imprimir y llenar a mano)"),
      spacer(),
      body("Nota: Esta hoja debe anexarse escaneada o fotografiada al final del reporte PDF.", { color: "444444", italics: true }),
      spacer(),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [4680, 4680],
        rows: [
          new TableRow({ children: [
            new TableCell({ borders, margins: cellMargin, shading: { fill: "EBF3FB", type: ShadingType.CLEAR }, width: { size: 4680, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "Aeropuerto de Salida: Mazatlán", bold: true, font: "Arial", size: 20 })] })] }),
            new TableCell({ borders, margins: cellMargin, width: { size: 4680, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "ICAO: MMMZ", bold: true, font: "Arial", size: 20 })] })] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ borders, margins: cellMargin, shading: { fill: "EBF3FB", type: ShadingType.CLEAR }, width: { size: 4680, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "Aeropuerto Destino: Ciudad Obregón", bold: true, font: "Arial", size: 20 })] })] }),
            new TableCell({ borders, margins: cellMargin, width: { size: 4680, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "ICAO: MMCN", bold: true, font: "Arial", size: 20 })] })] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ borders, margins: cellMargin, shading: { fill: "EBF3FB", type: ShadingType.CLEAR }, width: { size: 4680, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "Aeronave (Modelo FSX):", bold: true, font: "Arial", size: 20 })] })] }),
            new TableCell({ borders, margins: cellMargin, width: { size: 4680, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "Matrícula Sim:", bold: true, font: "Arial", size: 20 })] })] }),
          ]}),
          new TableRow({ children: [
            new TableCell({ borders, margins: cellMargin, shading: { fill: "EBF3FB", type: ShadingType.CLEAR }, width: { size: 4680, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "Altitud de Crucero Planeada:", bold: true, font: "Arial", size: 20 })] })] }),
            new TableCell({ borders, margins: cellMargin, width: { size: 4680, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "Aeropuerto Alternativo:", bold: true, font: "Arial", size: 20 })] })] }),
          ]}),
        ]
      }),
      spacer(),

      bold("Registro de Tramos (Vuelo de Ida: MMMZ → MMCN):"),
      spacer(),
      bitacoraIdaTable(),
      spacer(),

      bold("Registro de Tramos (Vuelo de Regreso: MMCN → MMMZ):"),
      spacer(),
      bitacoraRegresoTable(),
      spacer(),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [4680, 4680],
        rows: [new TableRow({ children: [
          new TableCell({ borders, margins: { top: 200, bottom: 200, left: 150, right: 150 }, width: { size: 4680, type: WidthType.DXA }, shading: { fill: "EBF3FB", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "Firma del Piloto al Mando: ________________________", font: "Arial", size: 20 })] })] }),
          new TableCell({ borders, margins: { top: 200, bottom: 200, left: 150, right: 150 }, width: { size: 4680, type: WidthType.DXA }, shading: { fill: "EBF3FB", type: ShadingType.CLEAR }, children: [new Paragraph({ children: [new TextRun({ text: "Firma del Copiloto: ________________________", font: "Arial", size: 20 })] })] }),
        ]})]
      }),
      spacer(),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [9360],
        rows: [new TableRow({ children: [
          new TableCell({ borders, margins: cellMargin, shading: { fill: "FFF2CC", type: ShadingType.CLEAR }, width: { size: 9360, type: WidthType.DXA }, children: [new Paragraph({ children: [new TextRun({ text: "Hora Total de Bloque (Sim): _________ hrs", bold: true, font: "Arial", size: 20 })] })] }),
        ]})]
      }),
      spacer(),

      // ── 7. CRITERIOS DE EVALUACIÓN ────────────────────────────────────────────
      sectionDivider("7. Criterios de Evaluación (Rúbrica)"),
      spacer(),
      rubricaTable(),
      spacer(),

      // ── 8. PUNTOS CRÍTICOS PARA CONSIDERAR ─────────────────────────────────
      sectionDivider("8. Puntos Críticos para Considerar (Checklist antes de entregar)"),
      spacer(),
      bullet("¿El video es accesible? (Si es Drive, verificar permisos en \"Cualquier persona con el enlace puede ver\").", "checklist"),
      bullet("¿Las capturas de pantalla del G1000 son legibles? (Si no, usar zoom o añadir anotaciones con flechas).", "checklist"),
      bullet("¿Se respetó el límite de 5 MB del PDF? (Comprimir imágenes si es necesario).", "checklist"),
      bullet("¿Se declaró el uso de herramientas de IA en el reporte, si se utilizaron para corrección de estilo? (Obligatorio por honestidad académica).", "checklist"),
      bullet("¿La bitácora está firmada a mano?", "checklist"),
      bullet("¿Todos los códigos ICAO en el reporte y bitácora son MMMZ y MMCN? (sin confusiones con MMCS o MMCU).", "checklist"),
      spacer(),

    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("Actividad_2_U2_Cartas_Aeronauticas.docx", buffer);
  console.log("Done");
});
