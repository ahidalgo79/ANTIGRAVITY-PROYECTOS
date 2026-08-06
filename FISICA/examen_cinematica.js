const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  AlignmentType, BorderStyle, WidthType, ShadingType, HeadingLevel,
  LevelFormat, UnderlineType, PageNumber, Footer, Header
} = require('docx');
const fs = require('fs');

const border = { style: BorderStyle.SINGLE, size: 1, color: "AAAAAA" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function cell(text, width, shade, bold = false, align = AlignmentType.LEFT) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: shade ? { fill: shade, type: ShadingType.CLEAR } : undefined,
    margins: { top: 80, bottom: 80, left: 120, right: 120 },
    children: [new Paragraph({
      alignment: align,
      children: [new TextRun({ text, bold, font: "Arial", size: 22 })]
    })]
  });
}

function headingPara(text, size = 28, color = "1F3864", bold = true, align = AlignmentType.CENTER) {
  return new Paragraph({
    alignment: align,
    spacing: { before: 160, after: 80 },
    children: [new TextRun({ text, bold, size, color, font: "Arial" })]
  });
}

function bodyPara(text, bold = false, spacing = { before: 60, after: 60 }, align = AlignmentType.LEFT) {
  return new Paragraph({
    alignment: align,
    spacing,
    children: [new TextRun({ text, bold, font: "Arial", size: 22 })]
  });
}

function sectionHeader(text) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 240, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "1F3864" } },
    children: [new TextRun({ text, bold: true, font: "Arial", size: 24, color: "1F3864" })]
  });
}

function questionPara(num, text, pts) {
  return new Paragraph({
    alignment: AlignmentType.LEFT,
    spacing: { before: 120, after: 60 },
    children: [
      new TextRun({ text: `${num}. `, bold: true, font: "Arial", size: 22 }),
      new TextRun({ text: text, font: "Arial", size: 22 }),
      new TextRun({ text: `  (${pts} pts)`, bold: false, italic: true, color: "666666", font: "Arial", size: 20 }),
    ]
  });
}

function option(letter, text) {
  return new Paragraph({
    spacing: { before: 40, after: 40 },
    indent: { left: 720 },
    children: [
      new TextRun({ text: `${letter}) `, bold: true, font: "Arial", size: 22 }),
      new TextRun({ text: text, font: "Arial", size: 22 }),
    ]
  });
}

function trueFalseRow(num, statement, pts) {
  return new TableRow({
    children: [
      new TableCell({
        borders, width: { size: 640, type: WidthType.DXA },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: `${num}`, bold: true, font: "Arial", size: 22 })] })]
      }),
      new TableCell({
        borders, width: { size: 6600, type: WidthType.DXA },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ children: [new TextRun({ text: statement, font: "Arial", size: 22 })] })]
      }),
      new TableCell({
        borders, width: { size: 1000, type: WidthType.DXA },
        shading: { fill: "E8F0FE", type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "V   /   F", font: "Arial", size: 22, color: "333333" })] })]
      }),
      new TableCell({
        borders, width: { size: 1120, type: WidthType.DXA },
        shading: { fill: "FFF3CD", type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 120, right: 120 },
        children: [new Paragraph({ alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: `${pts} pts`, italic: true, font: "Arial", size: 20, color: "666666" })] })]
      }),
    ]
  });
}

function blankLine() {
  return new Paragraph({ spacing: { before: 40, after: 40 }, children: [new TextRun("")] });
}

function answerLine(label) {
  return new Paragraph({
    spacing: { before: 80, after: 60 },
    indent: { left: 360 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: "999999" } },
    children: [new TextRun({ text: label ? `${label}: ` : "", bold: !!label, font: "Arial", size: 22, color: "444444" })]
  });
}

// ─── DOCUMENT ──────────────────────────────────────────────────────────────
const doc = new Document({
  styles: {
    default: {
      document: { run: { font: "Arial", size: 22 } }
    }
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1080, right: 1080, bottom: 1080, left: 1080 }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Table({
            width: { size: 10080, type: WidthType.DXA },
            columnWidths: [6480, 3600],
            rows: [new TableRow({
              children: [
                new TableCell({
                  borders: noBorders,
                  width: { size: 6480, type: WidthType.DXA },
                  margins: { top: 40, bottom: 40, left: 0, right: 120 },
                  children: [
                    new Paragraph({ children: [new TextRun({ text: "Universidad Politécnica de Chihuahua", bold: true, font: "Arial", size: 18, color: "1F3864" })] }),
                    new Paragraph({ children: [new TextRun({ text: "Ingeniería | Física — Unidad 2: Cinemática", font: "Arial", size: 16, color: "555555" })] }),
                  ]
                }),
                new TableCell({
                  borders: noBorders,
                  width: { size: 3600, type: WidthType.DXA },
                  margins: { top: 40, bottom: 40, left: 120, right: 0 },
                  verticalAlign: "center",
                  children: [new Paragraph({ alignment: AlignmentType.RIGHT,
                    children: [new TextRun({ text: "EXAMEN — 100 puntos", bold: true, font: "Arial", size: 18, color: "C00000" })] })]
                })
              ]
            })]
          }),
          new Paragraph({
            spacing: { before: 60, after: 0 },
            border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "1F3864" } },
            children: []
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            border: { top: { style: BorderStyle.SINGLE, size: 4, color: "AAAAAA" } },
            spacing: { before: 80 },
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Ingeniería — Física | UPCh  •  Página ", font: "Arial", size: 18, color: "888888" }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 18, color: "888888" }),
            ]
          })
        ]
      })
    },
    children: [

      // ── TÍTULO ──────────────────────────────────────────────────────────
      blankLine(),
      headingPara("EXAMEN PARCIAL", 32, "1F3864"),
      headingPara("Unidad 2: Cinemática", 26, "2E74B5"),
      blankLine(),

      // ── DATOS DEL ALUMNO ────────────────────────────────────────────────
      new Table({
        width: { size: 10080, type: WidthType.DXA },
        columnWidths: [5040, 5040],
        rows: [
          new TableRow({ children: [
            new TableCell({
              borders,
              width: { size: 10080, type: WidthType.DXA },
              columnSpan: 2,
              shading: { fill: "1F3864", type: ShadingType.CLEAR },
              margins: { top: 80, bottom: 80, left: 160, right: 160 },
              children: [new Paragraph({ alignment: AlignmentType.CENTER,
                children: [new TextRun({ text: "DATOS DEL ALUMNO", bold: true, font: "Arial", size: 22, color: "FFFFFF" })] })]
            })
          ]}),
          new TableRow({ children: [
            cell("Nombre completo:", 5040, "F5F5F5", true),
            new TableCell({
              borders, width: { size: 5040, type: WidthType.DXA },
              margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 22 })] })]
            })
          ]}),
          new TableRow({ children: [
            cell("Matrícula:", 2520, "F5F5F5", true),
            new TableCell({
              borders, width: { size: 2520, type: WidthType.DXA },
              margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 22 })] })]
            }),
            cell("Grupo:", 2520, "F5F5F5", true),
            new TableCell({
              borders, width: { size: 2520, type: WidthType.DXA },
              margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 22 })] })]
            }),
          ]}),
          new TableRow({ children: [
            cell("Carrera:", 5040, "F5F5F5", true),
            new TableCell({
              borders, width: { size: 5040, type: WidthType.DXA },
              margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 22 })] })]
            })
          ]}),
          new TableRow({ children: [
            cell("Docente:", 5040, "F5F5F5", true),
            new TableCell({
              borders, width: { size: 5040, type: WidthType.DXA },
              margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 22 })] })]
            })
          ]}),
          new TableRow({ children: [
            cell("Fecha:", 2520, "F5F5F5", true),
            new TableCell({
              borders, width: { size: 2520, type: WidthType.DXA },
              margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 22 })] })]
            }),
            cell("Calificación:", 2520, "F5F5F5", true),
            new TableCell({
              borders, width: { size: 2520, type: WidthType.DXA },
              shading: { fill: "FFF3CD", type: ShadingType.CLEAR },
              margins: { top: 80, bottom: 80, left: 120, right: 120 },
              children: [new Paragraph({ children: [new TextRun({ text: "", font: "Arial", size: 22 })] })]
            }),
          ]}),
        ]
      }),

      blankLine(),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 60, after: 120 },
        children: [new TextRun({ text: "Lee cuidadosamente cada pregunta antes de responder. Escribe con letra clara y legible.", italic: true, font: "Arial", size: 20, color: "555555" })]
      }),

      // ══════════════════════════════════════════════════════════════════════
      // SECCIÓN I — OPCIÓN MÚLTIPLE
      // ══════════════════════════════════════════════════════════════════════
      sectionHeader("SECCIÓN I. OPCIÓN MÚLTIPLE  (40 puntos — 4 pts cada reactivo)"),
      bodyPara("Instrucciones: Encierra en un círculo la letra que corresponda a la respuesta correcta.", true),
      blankLine(),

      // 1
      questionPara(1, "¿Cuál es la definición correcta de Cinemática?", 4),
      option("a", "Rama de la física que estudia las causas del movimiento."),
      option("b", "Rama de la física que estudia el movimiento sin considerar sus causas."),
      option("c", "Ciencia que analiza únicamente la aceleración de los cuerpos."),
      option("d", "Estudio de las fuerzas que actúan sobre los cuerpos en reposo."),
      blankLine(),

      // 2
      questionPara(2, "¿Cuál de las siguientes afirmaciones distingue correctamente velocidad de rapidez?", 4),
      option("a", "La rapidez es vectorial y la velocidad es escalar."),
      option("b", "Ambas son magnitudes escalares equivalentes."),
      option("c", "La rapidez es escalar (solo magnitud); la velocidad es vectorial (magnitud, dirección y sentido)."),
      option("d", "La velocidad no requiere dirección para expresarse."),
      blankLine(),

      // 3
      questionPara(3, "En el Movimiento Rectilíneo Uniforme (MRU), ¿cuál es el valor de la aceleración?", 4),
      option("a", "9.8 m/s²"),
      option("b", "Variable según el tiempo"),
      option("c", "Igual a la velocidad"),
      option("d", "Cero (a = 0)"),
      blankLine(),

      // 4
      questionPara(4, "Un objeto se suelta desde el reposo y cae libremente. ¿Cuál es su velocidad inicial?", 4),
      option("a", "9.8 m/s"),
      option("b", "0 m/s"),
      option("c", "−9.8 m/s"),
      option("d", "Depende de la masa del objeto"),
      blankLine(),

      // 5
      questionPara(5, "En el movimiento parabólico, ¿qué ocurre con la componente horizontal de la velocidad?", 4),
      option("a", "Aumenta constantemente por efecto de la gravedad."),
      option("b", "Disminuye hasta llegar a cero en la altura máxima."),
      option("c", "Se mantiene constante durante todo el recorrido."),
      option("d", "Es igual a cero en todos los puntos de la trayectoria."),
      blankLine(),

      // 6
      questionPara(6, "Un corredor recorre 400 m en 50 s. ¿Cuál es su rapidez promedio?", 4),
      option("a", "20 m/s"),
      option("b", "8 m/s"),
      option("c", "0.125 m/s"),
      option("d", "450 m/s"),
      blankLine(),

      // 7
      questionPara(7, "¿Cuál de las siguientes fórmulas corresponde a la aceleración media?", 4),
      option("a", "a = d / t"),
      option("b", "a = (Vf − Vi) / Δt"),
      option("c", "a = Vf × t"),
      option("d", "a = d × t²"),
      blankLine(),

      // 8
      questionPara(8, "En el tiro vertical hacia arriba, cuando el objeto alcanza su altura máxima, la velocidad es:", 4),
      option("a", "Máxima, igual a la velocidad inicial"),
      option("b", "Negativa (sentido descendente)"),
      option("c", "Cero (Vf = 0)"),
      option("d", "Igual a 9.8 m/s"),
      blankLine(),

      // 9
      questionPara(9, "¿Qué tipo de magnitud es el desplazamiento?", 4),
      option("a", "Escalar, porque solo tiene magnitud"),
      option("b", "Vectorial, porque tiene magnitud y dirección"),
      option("c", "Escalar, porque se mide en metros"),
      option("d", "Vectorial, porque su valor siempre es positivo"),
      blankLine(),

      // 10
      questionPara(10, "¿Cuál es el valor aproximado de la aceleración gravitacional en la superficie terrestre?", 4),
      option("a", "10.8 m/s²"),
      option("b", "9.8 m/s²"),
      option("c", "8.9 m/s²"),
      option("d", "9.0 m/s²"),
      blankLine(),

      // ══════════════════════════════════════════════════════════════════════
      // SECCIÓN II — FALSO Y VERDADERO
      // ══════════════════════════════════════════════════════════════════════
      sectionHeader("SECCIÓN II. FALSO Y VERDADERO  (20 puntos — 2 pts cada reactivo)"),
      bodyPara("Instrucciones: Escribe V si el enunciado es Verdadero o F si es Falso en la columna correspondiente. Recuerda que un enunciado parcialmente falso se considera Falso.", true),
      blankLine(),

      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [640, 6600, 1000, 1120],
        rows: [
          // Header row
          new TableRow({
            tableHeader: true,
            children: [
              new TableCell({ borders, width: { size: 640, type: WidthType.DXA },
                shading: { fill: "1F3864", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "#", bold: true, font: "Arial", size: 22, color: "FFFFFF" })] })] }),
              new TableCell({ borders, width: { size: 6600, type: WidthType.DXA },
                shading: { fill: "1F3864", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ children: [new TextRun({ text: "Enunciado", bold: true, font: "Arial", size: 22, color: "FFFFFF" })] })] }),
              new TableCell({ borders, width: { size: 1000, type: WidthType.DXA },
                shading: { fill: "1F3864", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Respuesta", bold: true, font: "Arial", size: 22, color: "FFFFFF" })] })] }),
              new TableCell({ borders, width: { size: 1120, type: WidthType.DXA },
                shading: { fill: "1F3864", type: ShadingType.CLEAR },
                margins: { top: 80, bottom: 80, left: 120, right: 120 },
                children: [new Paragraph({ alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: "Puntaje", bold: true, font: "Arial", size: 22, color: "FFFFFF" })] })] }),
            ]
          }),
          trueFalseRow(1,  "La cinemática estudia las causas que producen el movimiento de los cuerpos.", 2),
          trueFalseRow(2,  "El desplazamiento y la distancia recorrida siempre tienen el mismo valor numérico.", 2),
          trueFalseRow(3,  "En el MRU, la velocidad se mantiene constante y la aceleración es igual a cero.", 2),
          trueFalseRow(4,  "La rapidez es una magnitud vectorial porque indica magnitud y dirección.", 2),
          trueFalseRow(5,  "En caída libre, todos los cuerpos caen con la misma aceleración, independientemente de su masa, si se desprecia la resistencia del aire.", 2),
          trueFalseRow(6,  "En el tiro vertical hacia arriba, la velocidad en el punto más alto es igual a la velocidad inicial.", 2),
          trueFalseRow(7,  "En el movimiento parabólico, el componente vertical del movimiento es uniformemente acelerado.", 2),
          trueFalseRow(8,  "La trayectoria es siempre una línea recta para cualquier tipo de movimiento.", 2),
          trueFalseRow(9,  "La fórmula Vf = Vi + at se aplica al movimiento uniformemente acelerado (MRUA).", 2),
          trueFalseRow(10, "El sistema de referencia puede cambiarse libremente en cualquier punto de la resolución de un problema de cinemática.", 2),
        ]
      }),
      blankLine(),

      // ══════════════════════════════════════════════════════════════════════
      // SECCIÓN III — PROBLEMAS
      // ══════════════════════════════════════════════════════════════════════
      sectionHeader("SECCIÓN III. RESOLUCIÓN DE PROBLEMAS  (40 puntos)"),
      bodyPara("Instrucciones: Resuelve cada problema mostrando el procedimiento completo: datos, fórmula, sustitución y resultado con unidades. Se evalúa el proceso, no únicamente la respuesta final.", true),
      blankLine(),

      // PROBLEMA 1 — MRU (10 pts)
      new Paragraph({
        spacing: { before: 120, after: 60 },
        children: [
          new TextRun({ text: "Problema 1. Movimiento Rectilíneo Uniforme", bold: true, font: "Arial", size: 24, color: "1F3864" }),
          new TextRun({ text: "  (10 puntos)", italic: true, font: "Arial", size: 20, color: "777777" }),
        ]
      }),
      new Paragraph({
        spacing: { before: 60, after: 100 },
        children: [new TextRun({
          text: "Un motociclista recorre una distancia de 12 km en dirección este en 9 minutos a velocidad constante. Calcula:",
          font: "Arial", size: 22
        })]
      }),
      new Paragraph({ indent: { left: 480 }, spacing: { before: 60, after: 40 },
        children: [new TextRun({ text: "a) Su velocidad en m/s.", font: "Arial", size: 22 })] }),
      new Paragraph({ indent: { left: 480 }, spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "b) ¿Qué distancia habrá recorrido en 25 minutos a la misma velocidad?", font: "Arial", size: 22 })] }),
      blankLine(),
      bodyPara("Datos:"),
      answerLine(""),
      answerLine(""),
      blankLine(),
      bodyPara("Fórmula y procedimiento:"),
      answerLine(""),
      answerLine(""),
      answerLine(""),
      answerLine(""),
      blankLine(),
      bodyPara("Resultado:"),
      answerLine("a)"),
      answerLine("b)"),
      blankLine(),

      // PROBLEMA 2 — MRUA (10 pts)
      new Paragraph({
        spacing: { before: 160, after: 60 },
        children: [
          new TextRun({ text: "Problema 2. Movimiento Rectilíneo Uniformemente Acelerado", bold: true, font: "Arial", size: 24, color: "1F3864" }),
          new TextRun({ text: "  (10 puntos)", italic: true, font: "Arial", size: 20, color: "777777" }),
        ]
      }),
      new Paragraph({
        spacing: { before: 60, after: 100 },
        children: [new TextRun({
          text: "Un automóvil de carreras parte del reposo y alcanza una velocidad de 56 m/s en 8 segundos con aceleración constante. Determina:",
          font: "Arial", size: 22
        })]
      }),
      new Paragraph({ indent: { left: 480 }, spacing: { before: 60, after: 40 },
        children: [new TextRun({ text: "a) La aceleración del automóvil.", font: "Arial", size: 22 })] }),
      new Paragraph({ indent: { left: 480 }, spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "b) La distancia recorrida durante esos 8 segundos.", font: "Arial", size: 22 })] }),
      blankLine(),
      bodyPara("Datos:"),
      answerLine(""),
      answerLine(""),
      blankLine(),
      bodyPara("Fórmula y procedimiento:"),
      answerLine(""),
      answerLine(""),
      answerLine(""),
      answerLine(""),
      blankLine(),
      bodyPara("Resultado:"),
      answerLine("a)"),
      answerLine("b)"),
      blankLine(),

      // PROBLEMA 3 — CAÍDA LIBRE (10 pts)
      new Paragraph({
        spacing: { before: 160, after: 60 },
        children: [
          new TextRun({ text: "Problema 3. Caída Libre", bold: true, font: "Arial", size: 24, color: "1F3864" }),
          new TextRun({ text: "  (10 puntos)", italic: true, font: "Arial", size: 20, color: "777777" }),
        ]
      }),
      new Paragraph({
        spacing: { before: 60, after: 100 },
        children: [new TextRun({
          text: "Un dron de la UPCh despliega un paquete desde el reposo (v₀ = 0) a una altura de 80 m sobre el suelo. Considera g = 9.8 m/s². Calcula:",
          font: "Arial", size: 22
        })]
      }),
      new Paragraph({ indent: { left: 480 }, spacing: { before: 60, after: 40 },
        children: [new TextRun({ text: "a) El tiempo que tarda el paquete en llegar al suelo.", font: "Arial", size: 22 })] }),
      new Paragraph({ indent: { left: 480 }, spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "b) La velocidad con la que impacta el suelo.", font: "Arial", size: 22 })] }),
      blankLine(),
      bodyPara("Datos:"),
      answerLine(""),
      answerLine(""),
      blankLine(),
      bodyPara("Fórmula y procedimiento:"),
      answerLine(""),
      answerLine(""),
      answerLine(""),
      answerLine(""),
      blankLine(),
      bodyPara("Resultado:"),
      answerLine("a)"),
      answerLine("b)"),
      blankLine(),

      // PROBLEMA 4 — TIRO PARABÓLICO (10 pts)
      new Paragraph({
        spacing: { before: 160, after: 60 },
        children: [
          new TextRun({ text: "Problema 4. Movimiento Parabólico (Tiro Oblicuo)", bold: true, font: "Arial", size: 24, color: "1F3864" }),
          new TextRun({ text: "  (10 puntos)", italic: true, font: "Arial", size: 20, color: "777777" }),
        ]
      }),
      new Paragraph({
        spacing: { before: 60, after: 100 },
        children: [new TextRun({
          text: "Un balón de fútbol es pateado con una velocidad inicial de 22 m/s formando un ángulo de 40° con la horizontal. Considera g = 9.8 m/s². Determina:",
          font: "Arial", size: 22
        })]
      }),
      new Paragraph({ indent: { left: 480 }, spacing: { before: 60, after: 40 },
        children: [new TextRun({ text: "a) Las componentes horizontal y vertical de la velocidad inicial.", font: "Arial", size: 22 })] }),
      new Paragraph({ indent: { left: 480 }, spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "b) La altura máxima alcanzada por el balón.", font: "Arial", size: 22 })] }),
      new Paragraph({ indent: { left: 480 }, spacing: { before: 40, after: 40 },
        children: [new TextRun({ text: "c) El alcance horizontal (distancia total recorrida en x).", font: "Arial", size: 22 })] }),
      blankLine(),
      bodyPara("Datos:"),
      answerLine(""),
      answerLine(""),
      blankLine(),
      bodyPara("Fórmula y procedimiento:"),
      answerLine(""),
      answerLine(""),
      answerLine(""),
      answerLine(""),
      answerLine(""),
      blankLine(),
      bodyPara("Resultado:"),
      answerLine("a) V₀ₓ =                   V₀ᵧ ="),
      answerLine("b)"),
      answerLine("c)"),
      blankLine(),

      // ── RÚBRICA ──────────────────────────────────────────────────────────
      sectionHeader("DISTRIBUCIÓN DE PUNTAJE"),
      new Table({
        width: { size: 9360, type: WidthType.DXA },
        columnWidths: [5760, 2400, 1200],
        rows: [
          new TableRow({ children: [
            cell("Sección", 5760, "1F3864", true, AlignmentType.CENTER),
            cell("Reactivos", 2400, "1F3864", true, AlignmentType.CENTER),
            cell("Puntos", 1200, "1F3864", true, AlignmentType.CENTER),
          ]}),
          new TableRow({ children: [
            cell("I. Opción múltiple (10 reactivos × 4 pts)", 5760, "F0F4FF", false),
            cell("10", 2400, null, false, AlignmentType.CENTER),
            cell("40", 1200, null, false, AlignmentType.CENTER),
          ]}),
          new TableRow({ children: [
            cell("II. Falso y Verdadero (10 reactivos × 2 pts)", 5760, "FFFFFF", false),
            cell("10", 2400, null, false, AlignmentType.CENTER),
            cell("20", 1200, null, false, AlignmentType.CENTER),
          ]}),
          new TableRow({ children: [
            cell("III. Problemas (4 problemas × 10 pts)", 5760, "F0F4FF", false),
            cell("4", 2400, null, false, AlignmentType.CENTER),
            cell("40", 1200, null, false, AlignmentType.CENTER),
          ]}),
          new TableRow({ children: [
            cell("TOTAL", 5760, "1F3864", true, AlignmentType.RIGHT),
            cell("24", 2400, "1F3864", true, AlignmentType.CENTER),
            cell("100", 1200, "C00000", true, AlignmentType.CENTER),
          ]}),
        ]
      }),
      blankLine(),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 60, after: 120 },
        children: [new TextRun({ text: "¡Mucho éxito! — La honestidad académica es parte de tu formación como ingeniero/a.", italic: true, font: "Arial", size: 20, color: "555555" })]
      }),
    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(__dirname + "/Examen_Cinematica_UPCh.docx", buffer);
  console.log("Documento generado correctamente.");
});
