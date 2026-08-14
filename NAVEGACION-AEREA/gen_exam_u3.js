const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
  HeadingLevel, ImageRun
} = require('docx');
const fs = require('fs');

const CONTENT_W = 9360; // US Letter, 1" margins
const UPCH_LOGO = fs.readFileSync('assets/upch_logo.png');
const border = { style: BorderStyle.SINGLE, size: 4, color: "2C5F8A" };
const borderThin = { style: BorderStyle.SINGLE, size: 1, color: "AAAAAA" };
const borders = { top: border, bottom: border, left: border, right: border };
const bordersLight = { top: borderThin, bottom: borderThin, left: borderThin, right: borderThin };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

// ── Reactivos generados por NotebookLM ──────────────────────────────
// Pega aquí (o en reactivos_u3.json) el JSON con estructura:
// {
//   "titulo": "...", "descripcion": "...",
//   "subtitulo": "temas cubiertos",
//   "opcion_multiple": [{ "texto", "opciones": [4], "correcta": idx, "puntos" }],
//   "verdadero_falso": [{ "texto", "correcta": bool, "puntos" }],
//   "caso_estudio": { "escenario", "preguntas": [{ "texto", "opciones", "correcta", "puntos" }] }
// }
let REACTIVOS;
try {
  REACTIVOS = JSON.parse(fs.readFileSync('reactivos_u3.json', 'utf8'));
} catch (e) {
  console.error('No se encontró reactivos_u3.json:', e.message);
  process.exit(1);
}

function cell(children, opts = {}) {
  return new TableCell({
    borders: opts.borders ?? bordersLight,
    width: opts.width ? { size: opts.width, type: WidthType.DXA } : undefined,
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 140, right: 140 },
    columnSpan: opts.span,
    verticalAlign: opts.vAlign ?? VerticalAlign.TOP,
    children: Array.isArray(children) ? children : [children],
  });
}

function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align ?? AlignmentType.LEFT,
    spacing: { before: opts.before ?? 0, after: opts.after ?? 40 },
    children: [
      new TextRun({
        text,
        bold: opts.bold ?? false,
        size: opts.size ?? 20,
        font: "Arial",
        color: opts.color,
      })
    ]
  });
}

function pRuns(runs, opts = {}) {
  return new Paragraph({
    alignment: opts.align ?? AlignmentType.LEFT,
    spacing: { before: opts.before ?? 0, after: opts.after ?? 40 },
    children: runs.map(r => new TextRun({ font: "Arial", size: opts.size ?? 20, ...r }))
  });
}

function sectionHeader(letter, title, pts) {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [780, 6780, 1800],
    rows: [new TableRow({ children: [
      cell(p(letter, { bold: true, size: 22 }), { fill: "1B3A6B", borders }),
      cell(p(title, { bold: true, size: 21, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p(pts, { bold: true, size: 20, color: "FFFFFF", align: AlignmentType.CENTER }), { fill: "1B3A6B", borders }),
    ]})],
  });
}

function qHeader(code, title, pts) {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [780, 6780, 1800],
    rows: [new TableRow({ children: [
      cell(p(code, { bold: true, size: 20 }), { fill: "D6E4F0", borders: bordersLight }),
      cell(p(title, { bold: true, size: 20 }), { fill: "D6E4F0", borders: bordersLight }),
      cell(p(pts, { bold: true, size: 20, align: AlignmentType.CENTER }), { fill: "D6E4F0", borders: bordersLight }),
    ]})],
  });
}

function spacer(n = 1) {
  return new Paragraph({ spacing: { before: 0, after: n * 80 }, children: [] });
}

function opcionesMultiples(preguntas) {
  return preguntas.map((q, i) => {
    const rows = [
      new TableRow({ children: [
        cell([
          pRuns([{ text: `${i + 1}. `, bold: true, size: 19 }, { text: q.texto, size: 19 }]),
          ...q.opciones.map(op => p(`  ☐ ${op}`, { size: 19 })),
        ], { fill: "F7FBFF", borders: bordersLight })
      ]})
    ];
    return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [CONTENT_W], rows });
  });
}

function verdaderoFalso(preguntas) {
  const rows = [
    new TableRow({ children: [
      cell(
        preguntas.map((q, i) => p(`${i + 1}. (   ) ${q.texto}`, { size: 19, after: 60 })),
        { fill: "F7FBFF", borders: bordersLight }
      )
    ]})
  ];
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: [CONTENT_W], rows });
}

// ── Totales por sección (dinámicos) ──
const totalOM = REACTIVOS.opcion_multiple.reduce((a, q) => a + q.puntos, 0);
const totalFV = REACTIVOS.verdadero_falso.reduce((a, q) => a + q.puntos, 0);
const totalCaso = REACTIVOS.caso_estudio.preguntas.reduce((a, q) => a + q.puntos, 0);
const totalExamen = totalOM + totalFV + totalCaso;

// ── Score summary table (3 secciones + total) ──
const scoreSummary = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: [1560, 2340, 2340, 1560, 1560],
  rows: [
    new TableRow({ children: [
      cell(p("Sección", { bold: true, size: 18, align: AlignmentType.CENTER }), { fill: "1B3A6B", borders }),
      cell(p("A – Opción Múltiple", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("B – V / F", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("C – Caso", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("TOTAL", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
    ]}),
    new TableRow({ children: [
      cell(p("Puntaje máx.", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p(`${totalOM}`, { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p(`${totalFV}`, { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p(`${totalCaso}`, { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p(`${totalExamen}`, { bold: true, size: 18, align: AlignmentType.CENTER }), { fill: "FFF3CD" }),
    ]}),
    new TableRow({ children: [
      cell(p("Obtenido", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), { fill: "FFF3CD" }),
    ]}),
  ],
});

const subtitulo = REACTIVOS.subtitulo || "AIP/PIA — Publicación de Información Aeronáutica";

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } }
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
      }
    },
    children: [
      // ─── HEADER ───
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [
          new TableRow({ children: [
            cell([
              p("", { size: 8, after: 0 }),
              new Paragraph({
                alignment: AlignmentType.CENTER,
                spacing: { before: 0, after: 40 },
                children: [
                  new ImageRun({
                    data: UPCH_LOGO,
                    transformation: { width: 380, height: 138 },
                    type: "png",
                  }),
                ],
              }),
              p("EXAMEN DE UNIDAD 3 — NAVEGACIÓN AÉREA", { bold: true, size: 28, align: AlignmentType.CENTER, color: "FFFFFF", after: 20 }),
              p("Publicación de Información Aeronáutica (AIP/PIA)", { size: 19, align: AlignmentType.CENTER, color: "E8F0FF", after: 0 }),
            ], { fill: "1B3A6B", borders })
          ]})],
      }),
      spacer(),
      // ── Student info ──
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [4680, 4680],
        rows: [
          new TableRow({ children: [
            cell(p("Nombre: _________________________________________", { size: 19 }), { borders: bordersLight }),
            cell(pRuns([{ text: "Fecha: ____________   Grupo: ___________", size: 19 }]), { borders: bordersLight }),
          ]}),
          new TableRow({ children: [
            cell(p("Matrícula: _______________________________________", { size: 19 }), { borders: bordersLight }),
            cell(pRuns([{ text: "CALIFICACIÓN TOTAL:  _______ / 100", bold: true, size: 20 }]), { borders, fill: "FFF3CD" }),
          ]}),
        ],
      }),
      spacer(),
      // ── Instructions ──
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("📝  INSTRUCCIONES GENERALES", { bold: true, size: 20 }),
            p("1. Lee detenidamente cada pregunta antes de responder.", { size: 19 }),
            p("2. En los problemas prácticos, justifica tus procedimientos paso a paso. Se permite el uso de computador E6B y calculadora.", { size: 19 }),
            p("3. Duración: 60 minutos   │   Puntaje total: 100 puntos", { size: 19, bold: true }),
          ], { fill: "F0F4FB", borders: bordersLight })
        ]})]}),
      spacer(),
      scoreSummary,
      spacer(2),

      // ════════════════════════════════════════
      // SECTION A — Opción múltiple (50)
      // ════════════════════════════════════════
      sectionHeader("A", "SECCIÓN A: Opción Múltiple — AIP/PIA", `${totalOM} puntos`),
      spacer(),
      qHeader("P1", "Selecciona la respuesta correcta", `[ ${totalOM} pts ]`),
      spacer(),
      ...opcionesMultiples(REACTIVOS.opcion_multiple),
      spacer(2),

      // ════════════════════════════════════════
      // SECTION B — Verdadero/Falso (30)
      // ════════════════════════════════════════
      sectionHeader("B", "SECCIÓN B: Verdadero o Falso", `${totalFV} puntos`),
      spacer(),
      qHeader("P2", "Marca con una X Verdadero (V) o Falso (F)", `[ ${totalFV} pts ]`),
      spacer(),
      verdaderoFalso(REACTIVOS.verdadero_falso),
      spacer(2),

      // ════════════════════════════════════════
      // SECTION C — Caso de estudio (20)
      // ════════════════════════════════════════
      sectionHeader("C", "SECCIÓN C: Caso de Estudio", `${totalCaso} puntos`),
      spacer(),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("📌  CASO PRÁCTICO", { bold: true, size: 20 }),
            p(REACTIVOS.caso_estudio.escenario, { size: 19 }),
          ], { fill: "EEF5FB", borders })
        ]})]}),
      spacer(),
      qHeader("P3", "Responder a partir del escenario", `[ ${totalCaso} pts ]`),
      spacer(),
      ...opcionesMultiples(REACTIVOS.caso_estudio.preguntas),
      spacer(2),

      // Footer
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell(
            p("✅  Fin del examen — Revisa tus respuestas antes de entregar.", { bold: true, size: 19, align: AlignmentType.CENTER, color: "FFFFFF" }),
            { fill: "1B3A6B", borders }
          )
        ]})]}),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('Examen_Unidad3_Navegacion.docx', buf);
  console.log('Documento de examen generado exitosamente en Examen_Unidad3_Navegacion.docx');
});
