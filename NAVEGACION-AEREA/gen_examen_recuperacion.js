const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
  ImageRun
} = require('docx');
const fs = require('fs');

// Uso: node gen_examen_recuperacion.js reactivos_recu_u1.json [reactivos_recu_u2.json ...]
const FILES = process.argv.slice(2);
if (!FILES.length) {
  console.error('Uso: node gen_examen_recuperacion.js <reactivos_recu_X.json> [...]');
  process.exit(1);
}

const CONTENT_W = 9360; // US Letter, 1" margins
const UPCH_LOGO = fs.readFileSync('assets/upch_logo.png');
const border = { style: BorderStyle.SINGLE, size: 4, color: "2C5F8A" };
const borderThin = { style: BorderStyle.SINGLE, size: 1, color: "AAAAAA" };
const borders = { top: border, bottom: border, left: border, right: border };
const bordersLight = { top: borderThin, bottom: borderThin, left: borderThin, right: borderThin };

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
        italics: opts.italics ?? false,
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

function spacer(n = 1) {
  return new Paragraph({ spacing: { before: 0, after: n * 80 }, children: [] });
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
  const cells = [];
  if (code !== null && code !== undefined && code !== '') {
    cells.push(cell(p(code, { bold: true, size: 20 }), { fill: "D6E4F0", borders: bordersLight }));
  }
  cells.push(cell(p(title, { bold: true, size: 20 }), { fill: "D6E4F0", borders: bordersLight }));
  if (pts) cells.push(cell(p(`[ ${pts} ]`, { bold: true, size: 20, align: AlignmentType.CENTER }), { fill: "D6E4F0", borders: bordersLight }));
  const widths = code ? [780, 6780] : [CONTENT_W];
  if (pts) widths.push(1800);
  return new Table({ width: { size: CONTENT_W, type: WidthType.DXA }, columnWidths: widths, rows: [new TableRow({ children: cells })] });
}

// ── Bloques ──

function bloqueOM(b) {
  const out = [];
  out.push(qHeader(b.codigo ?? 'P', b.titulo ?? '', b.pts));
  out.push(spacer());
  if (b.instruccion) { out.push(p(b.instruccion, { size: 19, italics: true })); }
  (b.items ?? []).forEach((q, i) => {
    out.push(new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [CONTENT_W],
      rows: [new TableRow({ children: [
        cell([
          pRuns([
            { text: `${i + 1}. `, bold: true, size: 19 },
            ...(q.puntos ? [{ text: `(${q.puntos} pts) `, bold: true, size: 19 }] : []),
            { text: q.texto, size: 19 }
          ]),
          ...q.opciones.map(op => p(`  ☐ ${op}`, { size: 19 })),
        ], { fill: "F7FBFF", borders: bordersLight })
      ]})]
    }));
  });
  return out;
}

function bloqueVF(b) {
  return [
    qHeader(b.codigo ?? 'P', b.titulo ?? '', b.pts),
    spacer(),
    new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [CONTENT_W],
      rows: [new TableRow({ children: [
        cell(
          b.items.map((q, i) => [
            p(`${i + 1}. (   ) ${q.texto}`, { size: 19, after: 60 }),
            p('     ☐ Verdadero    ☐ Falso', { size: 18, color: "555555", after: 100 })
          ]).flat(),
          { fill: "F7FBFF", borders: bordersLight }
        )
      ]})]
    }),
  ];
}

function bloqueProblema(b) {
  const out = [
    qHeader(b.codigo ?? 'P', b.titulo ?? '', b.pts),
    spacer(),
    new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [CONTENT_W],
      rows: [new TableRow({ children: [
        cell([
          p(b.enunciado, { size: 19 }),
          ...(b.subproblemas ?? []).map(s => pRuns([
            { text: s.texto, size: 19 }
          ])),
          ...(b.pasos ?? []).map(ps => p(`   ${ps}`, { size: 19 })),
          ...((b.respuesta || (b.subproblemas ?? []).some(s => s.respuesta)) ? [p('', { size: 4 })] : []),
          ...(b.subproblemas ?? []).filter(s => s.respuesta).map(s => p(`${s.respuesta}`, { size: 19, bold: false })),
          ...(b.respuesta ? [pRuns([{ text: b.respuesta, bold: true, size: 19 }])] : []),
        ], { fill: "F7FBFF", borders: bordersLight })
      ]})]}),
  ];
  return out;
}

function bloqueContexto(b) {
  const children = [];
  if (b.titulo) children.push(p(b.titulo, { bold: true, size: 20 }));
  b.lineas.forEach(l => children.push(p(l, { size: 19 })));
  return [new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [cell(children, { fill: "EEF5FB", borders })] })],
  })];
}

function bloqueTabla(b) {
  const n = b.headers.length;
  const w = Math.floor(CONTENT_W / n);
  const widths = Array(n - 1).fill(w);
  widths.unshift(CONTENT_W - w * (n - 1));
  const headRow = new TableRow({
    children: b.headers.map((h, i) =>
      cell(p(h, { bold: true, size: 17, align: AlignmentType.CENTER }),
        { fill: "D6E4F0", borders: bordersLight, width: widths[i] }))
  });
  const bodyRows = b.rows.map(r => new TableRow({
    children: r.map((v, i) =>
      cell(p(v, { bold: i === 0, size: 17, align: AlignmentType.CENTER }),
        { borders: bordersLight, width: widths[i], fill: i === 0 ? "EFF3F8" : undefined }))
  }));
  const out = [];
  if (b.titulo) { out.push(p(b.titulo, { bold: true, size: 19, before: 60 })); }
  out.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [headRow, ...bodyRows],
  }));
  if (b.nota) { out.push(p(b.nota, { size: 17, italics: true, before: 40 })); }
  return out;
}

function bloquePasosCH(b) {
  return [
    qHeader(b.codigo ?? 'P', `${b.titulo}   ${b.pts ? '[ ' + b.pts + ' pts ]' : ''}`, null),
    spacer(),
    new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [2340, 2340, 2340, 2340],
      rows: [new TableRow({ children: b.pasos.map(ps => {
        const [nombre, formula] = ps.split('|').map(s => s.trim());
        return cell([
          p(nombre, { bold: true, size: 18 }),
          p(formula ?? '', { size: 16, color: "666666" }),
          p('', { size: 10 }),
          p('________ °', { size: 19, align: AlignmentType.CENTER }),
        ], { fill: "F7FBFF", borders: bordersLight, vAlign: VerticalAlign.TOP });
      })})]}),
    spacer(),
    new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [7020, 2340],
      rows: [new TableRow({ children: [
        cell(p(b.respuesta ?? '', { bold: true, size: 19, align: AlignmentType.RIGHT }), { borders: bordersLight }),
        cell(p("____ / " + (b.pts ?? ''), { bold: true, size: 19, align: AlignmentType.CENTER }), { borders: bordersLight, fill: "FFF9E6" }),
      ]})]}),
  ];
}

function bloqueGraficaRumbos(b) {
  function rosa() {
    return [
      p('     N ↑', { size: 19, align: AlignmentType.CENTER }),
      p('       |', { size: 19, align: AlignmentType.CENTER }),
      p(' W ---●--- E', { size: 19, align: AlignmentType.CENTER }),
      p('       |', { size: 19, align: AlignmentType.CENTER }),
      p('       S', { size: 19, align: AlignmentType.CENTER }),
    ];
  }
  return [
    qHeader(b.codigo ?? 'P', b.titulo ?? '', b.pts),
    spacer(),
    new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [4680, 4680],
      rows: [new TableRow({ children: [
        cell([p('Tramo A → B — CH = ____°', { bold: true, size: 19 }), ...rosa()], { fill: "F7FBFF", borders: bordersLight }),
        cell([p('Tramo B → C — CH = ____°', { bold: true, size: 19 }), ...rosa()], { fill: "F7FBFF", borders: bordersLight }),
      ]})]}),
  ];
}

function bloqueRelacionar(b) {
  const legend = b.leyenda.map(l => p(l, { size: 19, after: 30 }));
  const defs = b.definiciones.map(d => p(d, { size: 19, after: 60 }));
  return [
    qHeader(b.codigo ?? 'P', b.titulo ?? '', b.pts),
    spacer(),
    new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [3120, 6240],
      rows: [new TableRow({ children: [
        cell([...legend], { fill: "F7FBFF", borders: bordersLight }),
        cell([...defs], { fill: "F7FBFF", borders: bordersLight }),
      ]})]}),
  ];
}

const RENDERERS = {
  om: bloqueOM,
  vf: bloqueVF,
  problema: bloqueProblema,
  contexto: bloqueContexto,
  tabla: bloqueTabla,
  tabla_pasos_ch: bloquePasosCH,
  grafica_rumbos: bloqueGraficaRumbos,
  relacionar: bloqueRelacionar,
};

function buildDoc(R) {
  const totalExamen = R.secciones.reduce((a, s) => a + s.puntos, 0);

  // Score summary
  const summaryWidths = [1560, ...R.secciones.map(() => Math.floor((9360 - 1560 - 1560) / R.secciones.length)), 1560];
  const sumHead = [
    cell(p("Sección", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
    ...R.secciones.map(s => cell(p(s.corto ?? s.letra, { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders })),
    cell(p("TOTAL", { bold: true, size: 18, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
  ];
  const sumMax = [
    cell(p("Puntaje máx.", { size: 18, align: AlignmentType.CENTER }), {}),
    ...R.secciones.map(s => cell(p(`${s.puntos}`, { size: 18, align: AlignmentType.CENTER }), {})),
    cell(p(`${totalExamen}`, { bold: true, size: 18, align: AlignmentType.CENTER }), { fill: "FFF3CD" }),
  ];
  const sumGot = [
    cell(p("Obtenido", { size: 18, align: AlignmentType.CENTER }), {}),
    ...R.secciones.map(() => cell(p("", { size: 18 }), {})),
    cell(p("", { size: 18 }), { fill: "FFF3CD" }),
  ];
  const scoreSummary = new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: summaryWidths,
    rows: [
      new TableRow({ children: sumHead }),
      new TableRow({ children: sumMax }),
      new TableRow({ children: sumGot }),
    ],
  });

  const children = [];

  // Header
  children.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [
      cell([
        p("", { size: 8, after: 0 }),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { before: 0, after: 40 },
          children: [new ImageRun({ data: UPCH_LOGO, transformation: { width: 380, height: 138 }, type: "png" })],
        }),
        p(R.encabezado, { bold: true, size: 28, align: AlignmentType.CENTER, color: "FFFFFF", after: 20 }),
        p(R.subtitulo, { size: 19, align: AlignmentType.CENTER, color: "E8F0FF", after: R.version ? 20 : 0 }),
        ...(R.version ? [p(R.version, { size: 18, align: AlignmentType.CENTER, color: "FFE08A", after: 0 })] : []),
      ], { fill: "1B3A6B", borders })
    ]})]}),
  );
  children.push(spacer());

  // Student info
  children.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [4680, 4680],
    rows: [
      new TableRow({ children: [
        cell(p("Nombre: _________________________________________", { size: 19 }), { borders: bordersLight }),
        cell(pRuns([{ text: "Fecha: ____________   Grupo: ___________", size: 19 }]), { borders: bordersLight }),
      ]}),
      new TableRow({ children: [
        cell(p("Matrícula: _______________________________________", { size: 19 }), { borders: bordersLight }),
        cell(pRuns([{ text: `CALIFICACIÓN TOTAL:  _______ / ${totalExamen}`, bold: true, size: 20 }]), { borders, fill: "FFF3CD" }),
      ]}),
    ],
  }));
  children.push(spacer());

  // Instructions
  children.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [
      cell([
        p("📝  INSTRUCCIONES GENERALES", { bold: true, size: 20 }),
        ...R.instrucciones.map(i => p(i, { size: 19 })),
        p(`⏱ Duración: ${R.duracion ?? '—'}   │   Puntaje total: ${totalExamen} puntos`, { size: 19, bold: true }),
      ], { fill: "F0F4FB", borders: bordersLight })
    ]})]}),
  );
  children.push(spacer());

  // Formulas (optional)
  if (R.formulas?.length) {
    children.push(new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [2800, 6560],
      rows: [
        new TableRow({ children: [
          cell(p("Concepto", { bold: true, size: 18, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
          cell(p("📐 FÓRMULAS DE CONSULTA (hoja autorizada)", { bold: true, size: 18, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
        ]}),
        ...R.formulas.map(([concepto, formula], i) => new TableRow({ children: [
          cell(p(concepto, { bold: true, size: 18 }), { borders: bordersLight, fill: i % 2 ? "F7FBFF" : undefined }),
          cell(p(formula, { size: 18 }), { borders: bordersLight, fill: i % 2 ? "F7FBFF" : undefined }),
        ]})),
      ],
    }));

    children.push(spacer());
  }

  children.push(scoreSummary);
  children.push(spacer(2));

  // Sections
  for (const sec of R.secciones) {
    children.push(sectionHeader(sec.letra, sec.nombre, `${sec.puntos} puntos`));
    children.push(spacer());
    for (const blk of sec.bloques) {
      const render = RENDERERS[blk.tipo];
      if (!render) throw new Error(`Tipo de bloque desconocido: ${blk.tipo}`);
      children.push(...render(blk));
      children.push(spacer(2));
    }
  }

  // Footer
  children.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [
      cell(
        p("✅  Fin del examen — Revisa tus respuestas antes de entregar.", { bold: true, size: 19, align: AlignmentType.CENTER, color: "FFFFFF" }),
        { fill: "1B3A6B", borders }
      )
    ]})]}),
  );

  return new Document({
    styles: { default: { document: { run: { font: "Arial", size: 20 } } } },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
        }
      },
      children,
    }]
  });
}

(async () => {
  for (const f of FILES) {
    const R = JSON.parse(fs.readFileSync(f, 'utf8'));
    const doc = buildDoc(R);
    const buf = await Packer.toBuffer(doc);
    fs.writeFileSync(R.salida, buf);
    console.log(`OK  ${f} -> ${R.salida}`);
  }
})();
