const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
  HeadingLevel
} = require('docx');
const fs = require('fs');

const CONTENT_W = 9360; // US Letter, 1" margins
const border = { style: BorderStyle.SINGLE, size: 4, color: "2C5F8A" };
const borderThin = { style: BorderStyle.SINGLE, size: 1, color: "AAAAAA" };
const borders = { top: border, bottom: border, left: border, right: border };
const bordersLight = { top: borderThin, bottom: borderThin, left: borderThin, right: borderThin };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

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

function blankRow(label, pts) {
  return new TableRow({ children: [
    cell(p(label, { size: 19 }), { width: Math.round(CONTENT_W * 0.7) }),
    cell(p(pts, { size: 19, align: AlignmentType.RIGHT }), { width: Math.round(CONTENT_W * 0.3) }),
  ]});
}

function spacer(n = 1) {
  return new Paragraph({ spacing: { before: 0, after: n * 80 }, children: [] });
}

// ── Score summary table ──
const scoreSummary = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: [1560, 1560, 1560, 1560, 1560, 1560],
  rows: [
    new TableRow({ children: [
      cell(p("Sección", { bold: true, size: 18, align: AlignmentType.CENTER }), { fill: "1B3A6B", borders }),
      cell(p("A – Coord.", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("B – Horarios", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("C – Escalas", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("D – Navegación", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("TOTAL", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
    ]}),
    new TableRow({ children: [
      cell(p("Puntaje máx.", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("24", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("20", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("4", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("32", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("80", { bold: true, size: 18, align: AlignmentType.CENTER }), { fill: "FFF3CD" }),
    ]}),
    new TableRow({ children: [
      cell(p("Puntaje obtenido", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), { fill: "FFF3CD" }),
    ]}),
  ],
});

// ── Deviation table ──
const forRow  = ["FOR →",  "000°","030°","060°","090°","120°","150°","180°","210°","240°","270°","300°","330°"];
const steerRow= ["STEER →","006°","034°","054°","089°","128°","153°","178°","213°","246°","267°","305°","335°"];
const colW13 = Array(13).fill(Math.round(CONTENT_W / 13));

const devTable = new Table({
  width: { size: CONTENT_W, type: WidthType.DXA },
  columnWidths: colW13,
  rows: [
    new TableRow({ children: forRow.map((v, i) =>
      cell(p(v, { bold: true, size: 17, align: AlignmentType.CENTER }), { fill: i === 0 ? "D6E4F0" : "EEF5FB", borders: bordersLight })
    )}),
    new TableRow({ children: steerRow.map((v, i) =>
      cell(p(v, { bold: true, size: 17, align: AlignmentType.CENTER }), { fill: i === 0 ? "D6E4F0" : "FFFFFF", borders: bordersLight })
    )}),
  ],
});

// ── 4-step navigation calculation box ──
function navCalcTable(label, steps) {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [
      new TableRow({ children: [
        cell([
          p(label, { bold: true, size: 19 }),
          ...steps.map(s => pRuns([
            { text: s.label, bold: true, size: 19 },
            { text: "  " + s.value + "  =  _________°", size: 19 }
          ], { before: 40, after: 40 }))
        ], { fill: "F7FBFF", borders: bordersLight })
      ]})
    ]
  });
}

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
        rows: [new TableRow({ children: [
          cell([
            p("EXAMEN DE RECUPERACIÓN — NAVEGACIÓN AÉREA", { bold: true, size: 28, align: AlignmentType.CENTER, color: "FFFFFF", after: 20 }),
            p("UNIDAD 1   •   Coordenadas Geográficas  •  Husos Horarios  •  Escalas  •  Cálculo de Rumbos", { size: 19, align: AlignmentType.CENTER, color: "E8F0FF", after: 0 }),
          ], { fill: "1B3A6B", borders })
        ]})]}),

      spacer(),

      // ── Student info ──
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [4680, 4680],
        rows: [
          new TableRow({ children: [
            cell(p("Nombre: _________________________________________", { size: 19 }), { borders: bordersLight }),
            cell(pRuns([{text:"Fecha: ____________   Grupo: ___________", size:19}]), { borders: bordersLight }),
          ]}),
          new TableRow({ children: [
            cell(p("Matrícula: _______________________________________", { size: 19 }), { borders: bordersLight }),
            cell(pRuns([{text:"CALIFICACIÓN TOTAL:  _______ / 80", bold:true, size:20}]), { borders, fill: "FFF3CD" }),
          ]}),
        ],
      }),

      spacer(),

      // ── Allowed / Not Allowed ──
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [4680, 4680],
        rows: [new TableRow({ children: [
          cell([
            p("✅  PERMITIDO", { bold: true, size: 19, color: "1B6B2E" }),
            p("• Calculadora científica", { size: 18 }),
            p("• Lápiz y goma", { size: 18 }),
            p("• Fórmulas impresas al dorso", { size: 18 }),
          ], { fill: "EAF7EE", borders: bordersLight }),
          cell([
            p("❌  NO PERMITIDO", { bold: true, size: 19, color: "8B0000" }),
            p("• Celular ni dispositivos electrónicos", { size: 18 }),
            p("• Apuntes, libros o materiales extra", { size: 18 }),
            p("• Comunicación entre estudiantes", { size: 18 }),
          ], { fill: "FDE8E8", borders: bordersLight }),
        ]})]}),

      spacer(),

      // ── Instructions ──
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("📝  INSTRUCCIONES GENERALES", { bold: true, size: 20 }),
            p("1. Justifica todos los procedimientos paso a paso. Las respuestas sin desarrollo no reciben puntaje.", { size: 19 }),
            p("2. Incluye unidades en cada resultado (km, h, °, etc.).", { size: 19 }),
            p("3. Indica la dirección cuando corresponda (N/S/E/O o grados).", { size: 19 }),
            p("4. Duración: 75 minutos   │   Puntaje total: 80 puntos", { size: 19, bold: true }),
          ], { fill: "F0F4FB", borders: bordersLight })
        ]})]}),

      spacer(),

      // ── Formulas ──
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("📐  FÓRMULAS DE CONSULTA (hoja autorizada)", { bold: true, size: 20, after: 60 }),
            new Table({
              width: { size: CONTENT_W - 320, type: WidthType.DXA },
              columnWidths: [400, 2200, 400, 2200, 400, 2200],
              rows: [
                new TableRow({ children: [
                  cell(p("1", {bold:true,size:17,align:AlignmentType.CENTER}),{fill:"D6E4F0",borders:bordersLight}),
                  cell(p("Grados → Decimal:  θ_dec = D + M/60 + S/3600",{size:17}),{fill:"F7FBFF",borders:bordersLight}),
                  cell(p("2", {bold:true,size:17,align:AlignmentType.CENTER}),{fill:"D6E4F0",borders:bordersLight}),
                  cell(p("Diferencia horaria:  Δt = UTC_destino − UTC_origen",{size:17}),{fill:"F7FBFF",borders:bordersLight}),
                  cell(p("3", {bold:true,size:17,align:AlignmentType.CENTER}),{fill:"D6E4F0",borders:bordersLight}),
                  cell(p("Hora destino:  t_dest = t_orig + Δt",{size:17}),{fill:"F7FBFF",borders:bordersLight}),
                ]}),
                new TableRow({ children: [
                  cell(p("4", {bold:true,size:17,align:AlignmentType.CENTER}),{fill:"D6E4F0",borders:bordersLight}),
                  cell(p("Distancia real:  D_real = D_mapa × N",{size:17}),{fill:"F7FBFF",borders:bordersLight}),
                  cell(p("5", {bold:true,size:17,align:AlignmentType.CENTER}),{fill:"D6E4F0",borders:bordersLight}),
                  cell(p("Cadena:  TC ±WCA = TH  ±Var = MH  ±Dev = CH",{size:17}),{fill:"F7FBFF",borders:bordersLight}),
                  cell(p("6", {bold:true,size:17,align:AlignmentType.CENTER}),{fill:"D6E4F0",borders:bordersLight}),
                  cell(p("Longitud-tiempo:  15° = 1 h  →  1° = 4 min",{size:17}),{fill:"F7FBFF",borders:bordersLight}),
                ]}),
              ]
            }),
            spacer(),
            pRuns([
              {text:"Convenciones: ", bold:true, size:17},
              {text:"Este (+) = sumar  │  Oeste (−) = restar  │  WCA = corrección por viento  │  Dev = STEER − FOR", size:17}
            ]),
          ], { fill: "F0F4FB", borders: bordersLight })
        ]})]}),

      spacer(),
      scoreSummary,
      spacer(2),

      // ════════════════════════════════════════
      // SECTION A
      // ════════════════════════════════════════
      sectionHeader("A", "SECCIÓN A: Coordenadas Geográficas", "24 puntos"),
      spacer(),

      qHeader("P1", "Identificación de coordenadas en cuadrícula", "[ 14 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Observa la cuadrícula geográfica. Cada punto está marcado con una forma diferente (● ■ ▲).", { size: 19 }),
            p("Escribe sus coordenadas en formato °N/S, °E/O.", { size: 19, after: 60 }),
            pRuns([{text:"Referencia: ", bold:true, size:18},{text:"Línea vertical oscura = Meridiano de Greenwich (0°)  │  Línea horizontal oscura = Ecuador (0°)", size:18}]),
            spacer(),
            p("a)  Punto 1  (●)   [ 4 pts ]   Lat: ________°    Lon: ________°     ___ / 4", { size: 19 }),
            p("b)  Punto 2  (■)   [ 4 pts ]   Lat: ________°    Lon: ________°     ___ / 4", { size: 19 }),
            p("c)  Punto 3  (▲)   [ 4 pts ]   Lat: ________°    Lon: ________°     ___ / 4", { size: 19 }),
            spacer(),
            pRuns([
              {text:"d)  [ 2 pts ]  ", bold:true, size:19},
              {text:"Un punto en 45°O, 35°N está más próximo a (encierra la opción):  ", size:19},
            ]),
            p("     ☐  Mar Caribe (Cuba)     ☐  Atlántico Norte (Portugal)     ☐  Costa Este EE. UU.     ☐  Golfo de México", { size: 18 }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),

      spacer(),
      qHeader("P2", "Verdadero o Falso — Coordenadas geográficas", "[ 6 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Marca con una ✓ tu respuesta. Si es Falso, escribe la corrección en el espacio indicado.", { size: 19, after: 60 }),
            pRuns([{text:"a  ",bold:true,size:19},{text:"El Ecuador es el único paralelo que constituye un círculo máximo de la Tierra.   [2 pts]",size:19}]),
            p("   ☐  Verdadero   ☐  Falso         Si es Falso, justifique: ________________________________________________", { size: 18 }),
            spacer(),
            pRuns([{text:"b  ",bold:true,size:19},{text:"La longitud máxima posible es 180°, y se mide tanto al Este como al Oeste del meridiano de Greenwich.   [2 pts]",size:19}]),
            p("   ☐  Verdadero   ☐  Falso         Si es Falso, justifique: ________________________________________________", { size: 18 }),
            spacer(),
            pRuns([{text:"c  ",bold:true,size:19},{text:"Todos los meridianos tienen la misma longitud (distancia), mientras que los paralelos varían según la latitud.   [2 pts]",size:19}]),
            p("   ☐  Verdadero   ☐  Falso         Si es Falso, justifique: ________________________________________________", { size: 18 }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),

      spacer(),
      qHeader("P3", "Conversión de coordenadas: DMS → Decimal", "[ 4 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Convierta  95° 30' 00\"  a grados decimales. Muestre cada paso.", { size: 19 }),
            spacer(),
            p("Fórmula:   θ_dec = D + M/60 + S/3600", { bold: true, size: 19 }),
            spacer(),
            p("Procedimiento:", { size: 19 }),
            p("   θ_dec  =  ____ + ____/60 + ____/3600", { size: 19 }),
            p("   θ_dec  =  ____ + _______ + _________", { size: 19 }),
            p("   θ_dec  =  _______________ °", { bold: true, size: 19 }),
            p("                                                                                          ___ / 4", { size: 19, align: AlignmentType.RIGHT }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),

      spacer(2),

      // ════════════════════════════════════════
      // SECTION B
      // ════════════════════════════════════════
      sectionHeader("B", "SECCIÓN B: Husos Horarios y UTC", "20 puntos"),
      spacer(),

      qHeader("P4", "Verdadero o Falso — Husos horarios", "[ 8 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Marca con una ✓ tu respuesta. Si es Falso, escribe la corrección en el espacio indicado.", { size: 19, after: 60 }),
            pRuns([{text:"a  ",bold:true,size:19},{text:"Un huso horario cubre exactamente 15° de longitud y representa una diferencia de 1 hora respecto al huso adyacente.   [4 pts]",size:19}]),
            p("   ☐  Verdadero   ☐  Falso         Si es Falso, justifique: ________________________________________________", { size: 18 }),
            spacer(),
            pRuns([{text:"b  ",bold:true,size:19},{text:"Al cruzar la Línea Internacional de Cambio de Fecha viajando hacia el Este, se retrocede un día en el calendario.   [4 pts]",size:19}]),
            p("   ☐  Verdadero   ☐  Falso         Si es Falso, justifique: ________________________________________________", { size: 18 }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),

      spacer(),
      qHeader("P5", "Cálculo de diferencias horarias", "[ 12 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Resuelve cada situación mostrando todos los pasos. Usa la fórmula de la hoja de fórmulas.", { size: 19, after: 60 }),

            pRuns([{text:"a)  [4 pts]  ", bold:true, size:19},{text:"Si en Moscú (UTC +3) son las 16:00, ¿qué hora es en Ciudad de México (UTC −6)?",size:19}]),
            p("   Procedimiento 5a — espacio de trabajo:", { size: 18 }),
            p("   _______________________________________________________________________________", { size: 18 }),
            p("   Hora en Ciudad de México:  ___ / 4", { size: 19 }),
            spacer(),

            pRuns([{text:"b)  [4 pts]  ", bold:true, size:19},{text:"Un avión sale de Londres (UTC +0) a las 08:00 hora local hacia Singapur (UTC +8). El vuelo dura 13 horas. ¿Qué hora local será en Singapur al aterrizar?",size:19}]),
            p("   Paso 1 — Salida en UTC: ____________", { size: 18 }),
            p("   Paso 2 — Llegada en UTC (+13 h): ____________", { size: 18 }),
            p("   Paso 3 — Hora local Singapur (UTC +8): ____________", { size: 18 }),
            p("   Hora de llegada en Singapur:  ___ / 4", { size: 19 }),
            spacer(),

            pRuns([{text:"c)  [4 pts]  ", bold:true, size:19},{text:"Dos ciudades están separadas por 60° de longitud hacia el Oeste. Si en la ciudad oriental son las 10:00 AM, ¿qué hora solar es en la occidental?",size:19}]),
            p("   Procedimiento 5c — espacio de trabajo:", { size: 18 }),
            p("   _______________________________________________________________________________", { size: 18 }),
            p("   Hora en ciudad occidental:  ___ / 4", { size: 19 }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),

      spacer(2),

      // ════════════════════════════════════════
      // SECTION C
      // ════════════════════════════════════════
      sectionHeader("C", "SECCIÓN C: Escalas y Cartas Aeronáuticas", "4 puntos"),
      spacer(),

      qHeader("P6", "Conversión de escala cartográfica", "[ 4 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("En una carta de escala  1 : 500 000, un recorrido mide  6 cm. Calcula la distancia real en kilómetros.", { size: 19 }),
            p("Muestra cada paso.", { size: 19, after: 60 }),
            p("D_real = D_mapa × N      (recuerda convertir cm → km al final)", { bold: true, size: 19, after: 60 }),
            p("D_real  =  _____ cm  ×  _________  =  _____________ cm", { size: 19 }),
            p("         =  _____________ m   =  _____________ km", { size: 19 }),
            p("Distancia real:                                                                       ___ / 4", { size: 19, align: AlignmentType.RIGHT }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),

      spacer(2),

      // ════════════════════════════════════════
      // SECTION D
      // ════════════════════════════════════════
      sectionHeader("D", "SECCIÓN D: Navegación Práctica — Cálculo del Curso de Brújula (CH)", "32 puntos"),
      spacer(),

      // Context box
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("📌  CONTEXTO DEL VUELO", { bold: true, size: 20 }),
            pRuns([{text:"Variación magnética (Var) = 0°  ", bold:true, size:19},{text:"(se asume 0° para este ejercicio)", size:19}]),
            pRuns([{text:"WCA Tramo A→B = 0°     ", bold:true, size:19},{text:"WCA Tramo B→C = +15°", bold:true, size:19}]),
            spacer(),
            pRuns([{text:"Cadena de cálculo:  ", bold:true, size:19},{text:"TC  ±WCA → TH  ±Var → MH  ±Dev → CH", size:19}]),
            pRuns([{text:"Dev = STEER − FOR  ", bold:true, size:19},{text:"(usar tabla de desviación; NO se requiere interpolación en este examen)", size:19}]),
          ], { fill: "EEF5FB", borders })
        ]})]}),

      spacer(),

      // Deviation table header
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [3000, 4560, 1800],
        rows: [new TableRow({ children: [
          cell(p("Tabla de Desviación", { bold: true, size: 19 }), { fill: "D6E4F0", borders: bordersLight }),
          cell(p("Consulta esta tabla para obtener la desviación  (Dev = STEER − FOR)", { size: 18 }), { fill: "EEF5FB", borders: bordersLight }),
          cell(p("[ Consulta ]", { size: 18, align: AlignmentType.CENTER }), { fill: "EEF5FB", borders: bordersLight }),
        ]})],
      }),
      devTable,

      spacer(),

      // P7a
      qHeader("P7a", "Tramo A → B   (TC = 180°,  WCA = 0°,  Var = 0°)", "[ 8 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W * 0.5, CONTENT_W * 0.5].map(Math.round),
        rows: [new TableRow({ children: [
          cell([
            p("Paso 1 — TH = TC ± WCA", { bold: true, size: 19 }),
            p("         ____° ± ____° = ________°", { size: 19 }),
            spacer(),
            p("Paso 2 — MH = TH ± Var", { bold: true, size: 19 }),
            p("         ____° ± ____° = ________°", { size: 19 }),
          ], { fill: "F7FBFF", borders: bordersLight }),
          cell([
            p("Paso 3 — Dev (de tabla, sin interpolar)", { bold: true, size: 19 }),
            p("         FOR = ____°   STEER = ____°   Dev = ____°", { size: 19 }),
            spacer(),
            p("Paso 4 — CH = MH ± Dev", { bold: true, size: 19 }),
            p("         ____° ± ____° = ________°", { size: 19 }),
            spacer(),
            p("CH Tramo A → B:  ___ / 8", { bold: true, size: 19, align: AlignmentType.RIGHT }),
          ], { fill: "F7FBFF", borders: bordersLight }),
        ]})]}),

      spacer(),

      // P7b
      qHeader("P7b", "Tramo B → C   (TC = 135°,  WCA = +15°,  Var = 0°)", "[ 8 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W * 0.5, CONTENT_W * 0.5].map(Math.round),
        rows: [new TableRow({ children: [
          cell([
            p("Paso 1 — TH = TC ± WCA", { bold: true, size: 19 }),
            p("         ____° ± ____° = ________°", { size: 19 }),
            spacer(),
            p("Paso 2 — MH = TH ± Var", { bold: true, size: 19 }),
            p("         ____° ± ____° = ________°", { size: 19 }),
          ], { fill: "F7FBFF", borders: bordersLight }),
          cell([
            p("Paso 3 — Dev (de tabla, sin interpolar)", { bold: true, size: 19 }),
            p("         FOR = ____°   STEER = ____°   Dev = ____°", { size: 19 }),
            spacer(),
            p("Paso 4 — CH = MH ± Dev", { bold: true, size: 19 }),
            p("         ____° ± ____° = ________°", { size: 19 }),
            spacer(),
            p("CH Tramo B → C:  ___ / 8", { bold: true, size: 19, align: AlignmentType.RIGHT }),
          ], { fill: "F7FBFF", borders: bordersLight }),
        ]})]}),

      spacer(),

      // P7c–d
      qHeader("P7c–d", "Representación gráfica de los rumbos  (8 pts cada gráfica)", "[ 16 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W * 0.5, CONTENT_W * 0.5].map(Math.round),
        rows: [new TableRow({ children: [
          cell([
            p("Gráfica — Tramo A → B  [ 8 pts ]", { bold: true, size: 19 }),
            p("CH = ___°  respecto al Norte Verdadero", { size: 19 }),
            spacer(),
            p("                N ↑", { size: 19, align: AlignmentType.CENTER }),
            p("", { size: 19 }),
            p("                |", { size: 19, align: AlignmentType.CENTER }),
            p("                |", { size: 19, align: AlignmentType.CENTER }),
            p("      __________|__________", { size: 19, align: AlignmentType.CENTER }),
            p("                |", { size: 19, align: AlignmentType.CENTER }),
            p("                |", { size: 19, align: AlignmentType.CENTER }),
            spacer(),
            p("(Traza la línea del CH y anota el ángulo medido desde el Norte)", { size: 17 }),
          ], { fill: "F7FBFF", borders: bordersLight }),
          cell([
            p("Gráfica — Tramo B → C  [ 8 pts ]", { bold: true, size: 19 }),
            p("CH = ___°  respecto al Norte Verdadero", { size: 19 }),
            spacer(),
            p("                N ↑", { size: 19, align: AlignmentType.CENTER }),
            p("", { size: 19 }),
            p("                |", { size: 19, align: AlignmentType.CENTER }),
            p("                |", { size: 19, align: AlignmentType.CENTER }),
            p("      __________|__________", { size: 19, align: AlignmentType.CENTER }),
            p("                |", { size: 19, align: AlignmentType.CENTER }),
            p("                |", { size: 19, align: AlignmentType.CENTER }),
            spacer(),
            p("(Traza la línea del CH y anota el ángulo medido desde el Norte)", { size: 17 }),
          ], { fill: "F7FBFF", borders: bordersLight }),
        ]})]}),

      spacer(2),

      // Footer
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell(
            p("✅  Fin del examen — Revisa que hayas justificado todos tus procedimientos antes de entregar.", { bold: true, size: 19, align: AlignmentType.CENTER, color: "FFFFFF" }),
            { fill: "1B3A6B", borders }
          )
        ]})]}),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('Examen_Recuperacion_NavegacionAerea_U1.docx', buf);
  console.log('Done');
});
