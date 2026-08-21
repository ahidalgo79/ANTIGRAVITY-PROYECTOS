const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, VerticalAlign,
} = require('docx');
const fs = require('fs');

// Uso: node gen_solucionario_recuperacion.js reactivos_recu_uX.json [...]
const FILES = process.argv.slice(2);
if (!FILES.length) {
  console.error('Uso: node gen_solucionario_recuperacion.js <reactivos.json> [...]');
  process.exit(1);
}

const CONTENT_W = 9360;
const border = { style: BorderStyle.SINGLE, size: 4, color: "2C5F8A" };
const borderThin = { style: BorderStyle.SINGLE, size: 1, color: "AAAAAA" };
const borders = { top: border, bottom: border, left: border, right: border };
const bordersLight = { top: borderThin, bottom: borderThin, left: borderThin, right: borderThin };
const LETRAS = ['a', 'b', 'c', 'd'];

function cell(children, opts = {}) {
  return new TableCell({
    borders: opts.borders ?? bordersLight,
    width: opts.width ? { size: opts.width, type: WidthType.DXA } : undefined,
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 140, right: 140 },
    verticalAlign: opts.vAlign ?? VerticalAlign.TOP,
    children: Array.isArray(children) ? children : [children],
  });
}

function p(text, opts = {}) {
  return new Paragraph({
    alignment: opts.align ?? AlignmentType.LEFT,
    spacing: { before: opts.before ?? 0, after: opts.after ?? 40 },
    children: [new TextRun({
      text, bold: opts.bold ?? false, italics: opts.italics ?? false,
      size: opts.size ?? 20, font: "Arial", color: opts.color,
    })],
  });
}

function pRuns(runs, opts = {}) {
  return new Paragraph({
    alignment: opts.align ?? AlignmentType.LEFT,
    spacing: { before: opts.before ?? 0, after: opts.after ?? 40 },
    children: runs.map(r => new TextRun({ font: "Arial", size: opts.size ?? 20, ...r })),
  });
}

function spacer(n = 1) {
  return new Paragraph({ spacing: { before: 0, after: n * 80 }, children: [] });
}

function tablaFull(children, fill = "F7FBFF") {
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [cell(children, { fill, borders: bordersLight })] })],
  });
}

function qHeader(code, title) {
  const cells = [];
  if (code) cells.push(cell(p(code, { bold: true, size: 20 }), { fill: "D6E4F0", borders: bordersLight }));
  cells.push(cell(p(title, { bold: true, size: 20 }), { fill: "D6E4F0", borders: bordersLight }));
  return new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: code ? [780, 8580] : [CONTENT_W],
    rows: [new TableRow({ children: cells })],
  });
}

function resultadoBox(texto) {
  if (!texto) return [];
  const box = tablaFull([
    pRuns([
      { text: '✔ RESULTADO:  ', bold: true, size: 19 },
      { text: texto, bold: true, size: 19 },
    ]),
  ], "E6F4EA");
  box.borders = borders;
  return [box];
}

const RENDERERS = {

  om(b) {
    const out = [qHeader(b.codigo ?? 'P', b.titulo ?? ''), spacer()];
    b.items.forEach((q, i) => {
      const letra = LETRAS[q.correcta];
      out.push(tablaFull([
        pRuns([
          { text: `${i + 1}. `, bold: true, size: 19 },
          { text: `(${letra}) `, bold: true, size: 19, color: "1B7A3D" },
          { text: q.opciones[q.correcta], size: 19 },
        ]),
        p(q.texto, { size: 17, italics: true, color: "666666" }),
      ]));
    });
    return out;
  },

  vf(b) {
    const inner = b.items.map((q, i) => [
      pRuns([
        { text: `${i + 1}. (`, bold: true, size: 19 },
        { text: q.correcta ? ' V ' : ' F ', bold: true, size: 19, color: q.correcta ? "1B7A3D" : "B00020" },
        { text: ') ', bold: true, size: 19 },
        { text: q.texto, size: 19 },
      ]),
      ...(q.justificacion
        ? [p(`     ↳ Justificación: ${q.justificacion}`, { size: 18, italics: true, color: "555555", after: 100 })]
        : [p('', { size: 8, after: 60 })]),
    ]).flat();
    return [qHeader(b.codigo ?? 'P', b.titulo ?? ''), spacer(), tablaFull(inner)];
  },

  problema(b) {
    const out = [qHeader(b.codigo ?? 'P', b.titulo ?? ''), spacer()];
    const inner = [];
    if (b.solucion?.pasos?.length) {
      inner.push(p('Desarrollo:', { bold: true, size: 19 }));
      b.solucion.pasos.forEach(s => inner.push(p(`   • ${s}`, { size: 19 })));
    }
    (b.subproblemas ?? []).forEach((sub, i) => {
      if (!sub.solucion) return;
      inner.push(p(`${String.fromCharCode(97 + i)}) ${sub.texto}`, { bold: true, size: 19, before: 60 }));
      inner.push(p(`   ${sub.solucion}`, { size: 19 }));
    });
    if (inner.length) {
      out.push(tablaFull(inner));
      out.push(...resultadoBox(b.solucion?.resultado));
    }
    return out;
  },

  relacionar(b) {
    const inner = (b.respuestas ?? []).map((l, i) =>
      p(`${i + 1}. → ${l}`, { bold: true, size: 19, after: 50 })
    );
    return [qHeader(b.codigo ?? 'P', b.titulo ?? ''), spacer(), tablaFull(inner)];
  },

  tabla_pasos_ch(b) {
    const celdas = (b.solucion_pasos ?? []).map(s =>
      cell(p(s, { size: 18, align: AlignmentType.CENTER }), { fill: "F7FBFF", borders: bordersLight })
    );
    const tabla = new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [2340, 2340, 2340, 2340],
      rows: [new TableRow({ children: celdas })],
    });
    const out = [qHeader(b.codigo ?? 'P', `${b.titulo} — SOLUCIÓN`), spacer(), tabla];
    out.push(...resultadoBox(b.resultado));
    return out;
  },

  grafica_rumbos(b) {
    return [
      qHeader(b.codigo ?? 'P', b.titulo ?? ''),
      spacer(),
      new Table({
        width: { size: CONTENT_W, type: WidthType.DXA },
        columnWidths: [4680, 4680],
        rows: [new TableRow({ children: [
          cell([p('Tramo A → B', { bold: true, size: 19 }), p(b.descripcion_a ?? '', { size: 19 })], { fill: "F7FBFF", borders: bordersLight }),
          cell([p('Tramo B → C', { bold: true, size: 19 }), p(b.descripcion_b ?? '', { size: 19 })], { fill: "F7FBFF", borders: bordersLight }),
        ]})]}),
    ];
  },

  contexto() { return []; },
  tabla() { return []; },
};

function buildDoc(R) {
  const totalExamen = R.secciones.reduce((a, s) => a + s.puntos, 0);
  const children = [];

  children.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [
      cell([
        p("", { size: 8, after: 0 }),
        p("SOLUCIONARIO — USO DEL DOCENTE", { bold: true, size: 28, align: AlignmentType.CENTER, color: "FFFFFF", after: 20 }),
        p(R.encabezado.replace(/EXAMEN DE RECUPERACIÓN —?\s*/, '') + '· Navegación Aérea', { size: 19, align: AlignmentType.CENTER, color: "E8F0FF", after: 20 }),
        p(`Referencia del examen: ${R.salida}`, { size: 17, align: AlignmentType.CENTER, color: "FFE08A", after: 0 }),
      ], { fill: "14532D", borders }),
    ]})]})
  );
  children.push(spacer());

  // Claves rápidas
  const resumenRows = [];
  for (const sec of R.secciones) {
    for (const blk of sec.bloques) {
      let clave = '';
      if (blk.tipo === 'om') clave = blk.items.map((q, i) => `${i + 1}-${LETRAS[q.correcta]}`).join('   ');
      else if (blk.tipo === 'vf') clave = blk.items.map(q => q.correcta ? 'V' : 'F').join('  ');
      else if (blk.tipo === 'relacionar') clave = (blk.respuestas ?? []).join('  ');
      else if (blk.tipo === 'tabla_pasos_ch' && blk.resultado) clave = blk.resultado;
      else continue;
      resumenRows.push(new TableRow({ children: [
        cell(p(`${sec.letra}/${blk.codigo ?? ''}`, { bold: true, size: 17 }), { borders: bordersLight }),
        cell(p(clave, { size: 17 }), { borders: bordersLight }),
      ]}));
    }
  }
  if (resumenRows.length) {
    children.push(new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [1400, 7960],
      rows: [
        new TableRow({ children: [
          cell(p("BLOQUE", { bold: true, size: 18, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
          cell(p("CLAVES RÁPIDAS — respuestas correctas", { bold: true, size: 18, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
        ]}),
        ...resumenRows,
      ],
    }));
    children.push(spacer(2));
  }

  for (const sec of R.secciones) {
    children.push(new Table({
      width: { size: CONTENT_W, type: WidthType.DXA },
      columnWidths: [780, 6780, 1800],
      rows: [new TableRow({ children: [
        cell(p(sec.letra, { bold: true, size: 22 }), { fill: "1B3A6B", borders }),
        cell(p(sec.nombre, { bold: true, size: 21, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
        cell(p(`${sec.puntos} puntos`, { bold: true, size: 20, color: "FFFFFF", align: AlignmentType.CENTER }), { fill: "1B3A6B", borders }),
      ]})]})
    );
    children.push(spacer());
    for (const blk of sec.bloques) {
      const render = RENDERERS[blk.tipo];
      if (!render) throw new Error(`Tipo desconocido: ${blk.tipo}`);
      children.push(...render(blk));
      children.push(spacer(2));
    }
  }

  children.push(new Table({
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    rows: [new TableRow({ children: [
      cell(p(`Puntaje total del examen: ${totalExamen} puntos`, { bold: true, size: 19, align: AlignmentType.CENTER, color: "FFFFFF" }), { fill: "1B3A6B", borders }),
    ]})]})
  );

  return new Document({
    styles: { default: { document: { run: { font: "Arial", size: 20 } } } },
    sections: [{
      properties: {
        page: {
          size: { width: 12240, height: 15840 },
          margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 },
        },
      },
      children,
    }],
  });
}

(async () => {
  for (const f of FILES) {
    const R = JSON.parse(fs.readFileSync(f, 'utf8'));
    const salida = R.salida.replace('Examen_', 'Solucionario_');
    const doc = buildDoc(R);
    const buf = await Packer.toBuffer(doc);
    fs.writeFileSync(salida, buf);
    console.log(`OK  ${f} -> ${salida}`);
  }
})();
