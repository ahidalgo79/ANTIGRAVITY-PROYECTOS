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
      cell(p("A – Cartas", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("B – Sistemas", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("C – Alt/Vel", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("D – E6B", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
      cell(p("TOTAL", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
    ]}),
    new TableRow({ children: [
      cell(p("Puntaje máx.", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("20", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("20", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("20", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("40", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("100", { bold: true, size: 18, align: AlignmentType.CENTER }), { fill: "FFF3CD" }),
    ]}),
    new TableRow({ children: [
      cell(p("Obtenido", { size: 18, align: AlignmentType.CENTER }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), {}),
      cell(p("", { size: 18 }), { fill: "FFF3CD" }),
    ]}),
  ],
});

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
            p("EXAMEN DE UNIDAD 2 — NAVEGACIÓN AÉREA", { bold: true, size: 28, align: AlignmentType.CENTER, color: "FFFFFF", after: 20 }),
            p("Cartas Aeronáuticas • Radionavegación • Velocidades y Altimetría • Uso del E6B", { size: 19, align: AlignmentType.CENTER, color: "E8F0FF", after: 0 }),
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
            cell(pRuns([{text:"CALIFICACIÓN TOTAL:  _______ / 100", bold:true, size:20}]), { borders, fill: "FFF3CD" }),
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
            p("3. Duración: 90 minutos   │   Puntaje total: 100 puntos", { size: 19, bold: true }),
          ], { fill: "F0F4FB", borders: bordersLight })
        ]})]}),
      spacer(),
      scoreSummary,
      spacer(2),

      // ════════════════════════════════════════
      // SECTION A
      // ════════════════════════════════════════
      sectionHeader("A", "SECCIÓN A: Cartas Aeronáuticas (Anexo 4 OACI)", "20 puntos"),
      spacer(),

      qHeader("P1", "Relaciona columnas sobre los tipos de cartas", "[ 10 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Escribe la letra correspondiente dentro del paréntesis.", { size: 19, after: 60 }),
            p("A) SID          (   ) Facilita la navegación a lo largo de rutas ATS (FIR).", { size: 19 }),
            p("B) STAR         (   ) Proporciona información para pasar de fase de ruta a la aproximación.", { size: 19 }),
            p("C) En-Ruta      (   ) Proporciona info. para la salida normalizada desde el despegue hasta la ruta.", { size: 19 }),
            p("D) Plano de Aeródromo (   ) Muestra las instalaciones terrestres, pistas y plataforma desde vista general.", { size: 19 }),
            p("E) IAC          (   ) Procedimiento de aproximación por instrumentos a la pista prevista.", { size: 19 }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),
      spacer(),

      qHeader("P2", "Preguntas de opción múltiple", "[ 10 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            pRuns([{text:"2.1 ", bold:true},{text:"De acuerdo al Anexo 4 OACI, ¿Cuáles son ejemplos de cartas obligatorias? (2 pts)"}]),
            p("  ☐ a) Tipo A, Carta Topográfica Precisión, Carta En Ruta, IAC, Plano Aeródromo y Mundial.", { size: 19 }),
            p("  ☐ b) Tipo B, Movimientos en tierra, Estacionamiento y Atraque.", { size: 19 }),
            p("  ☐ c) Carta de Área, SID, STAR, Aproximación Visual.", { size: 19 }),
            spacer(),
            pRuns([{text:"2.2 ", bold:true},{text:"¿Cuál es la función del Plano de Estacionamiento y Atraque de Aeronaves? (2 pts)"}]),
            p("  ☐ a) Movimiento general entre pistas y plataformas.", { size: 19 }),
            p("  ☐ b) Movimiento entre rodajes de acceso y puestos de estacionamiento específicos.", { size: 19 }),
            p("  ☐ c) Identificar obstáculos en el área de despegue.", { size: 19 }),
            spacer(),
            pRuns([{text:"2.3 ", bold:true},{text:"En cartas náuticas, ¿qué tipo de fondo se indica más comúnmente en las zonas costeras seguras? (2 pts)"}]),
            p("  ☐ a) Vegetación   ☐ b) Arena   ☐ c) Bosque", { size: 19 }),
            spacer(),
            pRuns([{text:"2.4 ", bold:true},{text:"¿Cuál es la escala principal utilizada en las Cartas Seccionales Aeronáuticas? (2 pts)"}]),
            p("  ☐ a) 1:500,000    ☐ b) 1:1,000,000    ☐ c) 1:100,000", { size: 19 }),
            spacer(),
            pRuns([{text:"2.5 ", bold:true},{text:"Método de navegación basado en cálculos matemáticos de velocidad y tiempo sin referencias visuales externas: (2 pts)"}]),
            p("  ☐ a) Radionavegación    ☐ b) Navegación visual    ☐ c) Navegación a estima", { size: 19 }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),
      spacer(2),

      // ════════════════════════════════════════
      // SECTION B
      // ════════════════════════════════════════
      sectionHeader("B", "SECCIÓN B: Sistemas y Radionavegación", "20 puntos"),
      spacer(),
      qHeader("P3", "Identificación de sistemas", "[ 20 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Selecciona la respuesta correcta para cada descripción. (4 pts c/u)", { size: 19, after: 60 }),
            pRuns([{text:"3.1 ", bold:true},{text:"Sistema de radionavegación que proporciona información de distancia (slant range) a la estación:"}]),
            p("  ☐ a) VOR    ☐ b) DME    ☐ c) ADF", { size: 19 }),
            spacer(),
            pRuns([{text:"3.2 ", bold:true},{text:"Sistema que utiliza satélites para determinar la posición tridimensional de la aeronave:"}]),
            p("  ☐ a) GPS    ☐ b) INS    ☐ c) VOR", { size: 19 }),
            spacer(),
            pRuns([{text:"3.3 ", bold:true},{text:"Sistema utilizado principalmente para aproximación y aterrizaje en condiciones de baja visibilidad, compuesto por localizador y senda de planeo:"}]),
            p("  ☐ a) ILS    ☐ b) DME    ☐ c) ADF", { size: 19 }),
            spacer(),
            pRuns([{text:"3.4 ", bold:true},{text:"Funciona emitiendo señales de radio en la banda VHF, permitiendo al piloto volar radiales magnéticos desde o hacia la estación:"}]),
            p("  ☐ a) VOR    ☐ b) INS    ☐ c) Satélite", { size: 19 }),
            spacer(),
            pRuns([{text:"3.5 ", bold:true},{text:"Sistema de navegación inercial que utiliza giroscopios y acelerómetros sin necesidad de señales externas:"}]),
            p("  ☐ a) INS    ☐ b) ILS    ☐ c) VOR", { size: 19 }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),
      spacer(2),

      // ════════════════════════════════════════
      // SECTION C
      // ════════════════════════════════════════
      sectionHeader("C", "SECCIÓN C: Velocidades y Altimetría", "20 puntos"),
      spacer(),
      qHeader("P4", "Verdadero o Falso", "[ 20 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Marca con una X indicando si la afirmación es verdadera (V) o falsa (F). (2 pts c/u)", { size: 19, after: 60 }),
            p("1. (   ) IAS (Indicated Airspeed) es la velocidad que el piloto lee directamente en su instrumento.", { size: 19 }),
            p("2. (   ) TAS (True Airspeed) es la velocidad real de la aeronave con respecto a la masa de aire circundante.", { size: 19 }),
            p("3. (   ) GS (Ground Speed) es igual a la TAS sumando o restando el efecto del viento.", { size: 19 }),
            p("4. (   ) V1 es la velocidad de decisión durante la carrera de despegue.", { size: 19 }),
            p("5. (   ) QNH es la presión atmosférica ajustada para que el altímetro indique cero en el terreno.", { size: 19 }),
            p("6. (   ) Al ajustar el altímetro a QNE (1013.25 hPa) se lee la altitud de presión (niveles de vuelo).", { size: 19 }),
            p("7. (   ) La altitud de densidad disminuye cuando la temperatura exterior aumenta.", { size: 19 }),
            p("8. (   ) La altura es la distancia vertical desde el nivel medio del mar.", { size: 19 }),
            p("9. (   ) Vmcg es la velocidad mínima de control en tierra si falla un motor.", { size: 19 }),
            p("10.(   ) La velocidad GS es la utilizada para estimar la hora de llegada (ETA).", { size: 19 }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),
      spacer(2),

      // ════════════════════════════════════════
      // SECTION D
      // ════════════════════════════════════════
      sectionHeader("D", "SECCIÓN D: Planificación con Computador de Vuelo E6B", "40 puntos"),
      spacer(),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("📌  CASO PRÁCTICO: BÚSQUEDA Y RESCATE", { bold: true, size: 20 }),
            pRuns([{text:"Aeronave: ", bold:true, size:19},{text:"Cessna 182T Skylane", size:19}]),
            pRuns([{text:"Condiciones: ", bold:true, size:19},{text:"VFR marginal en terreno montañoso", size:19}]),
            p("Muestra el procedimiento o cálculos para validar cada respuesta.", { size: 18, color: "555555" }),
          ], { fill: "EEF5FB", borders })
        ]})]}),
      spacer(),

      qHeader("P5", "Problema 1: Cálculo de GS y WCA", "[ 12 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Viento: 270° / 20 kts       TAS: 125 kts       Rumbo de búsqueda (Course): 090°", { bold: true, size: 19 }),
            spacer(),
            pRuns([{text:"1. Determina el WCA (Wind Correction Angle): ", bold:true, size:19}]),
            p("   WCA = ________°  (Indica si es corrección L/R o nula)", { size: 19 }),
            spacer(),
            pRuns([{text:"2. Determina el Ground Speed (GS): ", bold:true, size:19}]),
            p("   GS = ________ kts", { size: 19 }),
            spacer(),
            pRuns([{text:"3. ¿A qué se debe el resultado del WCA en esta situación específica? ", bold:true, size:19}]),
            p("   ____________________________________________________________________________________", { size: 19 }),
            p("   ____________________________________________________________________________________", { size: 19 }),
            spacer(),
            p("___ / 12", { bold: true, size: 19, align: AlignmentType.RIGHT }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),
      spacer(),

      qHeader("P6", "Problema 2: Gestión de Combustible", "[ 16 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Tiempo de búsqueda: 147 min         Consumo: 12 gal/h          Dist. de regreso: 45 NM @ 140 kts GS", { bold: true, size: 19 }),
            spacer(),
            pRuns([{text:"a) Combustible consumido durante la búsqueda (147 min):", bold:true, size:19}]),
            p("   Procedimiento: ______________________________________________________________________", { size: 19 }),
            p("   Gasto = ________ galones", { size: 19 }),
            spacer(),
            pRuns([{text:"b) Combustible para el regreso (45 NM a 140 kts de GS):", bold:true, size:19}]),
            p("   Procedimiento: ______________________________________________________________________", { size: 19 }),
            p("   Gasto = ________ galones", { size: 19 }),
            spacer(),
            pRuns([{text:"c) Combustible de reserva legal (1 h 30 min):", bold:true, size:19}]),
            p("   Procedimiento: ______________________________________________________________________", { size: 19 }),
            p("   Gasto = ________ galones", { size: 19 }),
            spacer(),
            pRuns([{text:"d) Total requerido vs Total a bordo (Asumiendo tanques llenos a 84 gal):", bold:true, size:19}]),
            p("   Total Requerido = ________ galones       ¿Es suficiente el combustible? (Sí/No): _________", { size: 19 }),
            spacer(),
            p("___ / 16", { bold: true, size: 19, align: AlignmentType.RIGHT }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),
      spacer(),

      qHeader("P7", "Problema 3: Corrección por Densidad Altitud", "[ 12 pts ]"),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell([
            p("Condiciones: Temperatura Exterior (OAT) = 25°C, Presión = 1013 hPa, Altitud Presión = 8,500 ft", { bold: true, size: 19 }),
            spacer(),
            pRuns([{text:"a) Calcula la Densidad Altitud aproximada (usando E6B o fórmula estándar):", bold:true, size:19}]),
            p("   Procedimiento: ______________________________________________________________________", { size: 19 }),
            p("   ____________________________________________________________________________________", { size: 19 }),
            p("   Densidad Altitud ≈ ____________ ft", { size: 19 }),
            spacer(),
            pRuns([{text:"b) Pregunta de reflexión:", bold:true, size:19}]),
            p("   Si despegas de un aeropuerto alto y caluroso, ¿cómo se ven afectados la TAS real, el consumo de combustible y la carrera de despegue con respecto al nivel del mar?", { size: 19 }),
            p("   ____________________________________________________________________________________", { size: 19 }),
            p("   ____________________________________________________________________________________", { size: 19 }),
            p("   ____________________________________________________________________________________", { size: 19 }),
            spacer(),
            p("___ / 12", { bold: true, size: 19, align: AlignmentType.RIGHT }),
          ], { fill: "F7FBFF", borders: bordersLight })
        ]})]}),
      spacer(2),

      // Footer
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [CONTENT_W],
        rows: [new TableRow({ children: [
          cell(
            p("✅  Fin del examen — Revisa tus respuestas y cálculos de E6B antes de entregar.", { bold: true, size: 19, align: AlignmentType.CENTER, color: "FFFFFF" }),
            { fill: "1B3A6B", borders }
          )
        ]})]}),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync('Examen_Unidad2_NavegacionAerea.docx', buf);
  console.log('Documento de examen generado exitosamente en Examen_Unidad2_NavegacionAerea.docx');
});
