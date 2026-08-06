const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const fs = require("fs");
const path = require("path");
const readline = require("readline");

// ---------- LOGO UPCh (base64 embebido) ----------
function loadLogoBase64() {
    const candidates = [
        path.join(__dirname, "logo_upch.png"),
        path.join(__dirname, "OIC-28.png"),
    ];
    for (const p of candidates) {
        if (fs.existsSync(p)) {
            return "image/png;base64," + fs.readFileSync(p).toString("base64");
        }
    }
    return null;
}

const {
    FaMicrophone, FaClock, FaUserGraduate, FaQuestionCircle, FaBomb,
    FaCheckCircle, FaExclamationTriangle, FaBullseye, FaComments,
    FaLayerGroup, FaClipboardList, FaBan, FaRandom, FaLink, FaVideo, FaFileVideo
} = require("react-icons/fa");

// ---------- HELPERS PARA ICONOS ----------
function renderIconSvg(IconComponent, color = "#000000", size = 256) {
    return ReactDOMServer.renderToStaticMarkup(
        React.createElement(IconComponent, { color, size: String(size) })
    );
}
async function iconToBase64Png(IconComponent, color, size = 256) {
    const svg = renderIconSvg(IconComponent, color, size);
    const pngBuffer = await sharp(Buffer.from(svg)).png().toBuffer();
    return "image/png;base64," + pngBuffer.toString("base64");
}

// ---------- PALETA DE COLORES ----------
const DEEP = "152C5B";
const TEAL = "8DBA35";
const MIDNIGHT = "0F1F40";
const ICE = "EAF2F6";
const WHITE = "FFFFFF";
const INK = "1B2733";
const MUTED = "5B6B79";
const GOLD = "E0A458";
const SAFE_RED = "C0392B";
const SAFE_GREEN = "2E7D32";

const FONT_HEAD = "Cambria";
const FONT_BODY = "Calibri";

// ---------- DIBUJAR ICONO DENTRO DE CÍRCULO ----------
function iconCircle(slide, IconData, x, y, d, bg, padFactor = 0.32) {
    slide.addShape("ellipse", { x, y, w: d, h: d, fill: { color: bg }, line: { type: "none" } });
    const inner = d * (1 - padFactor * 2);
    slide.addImage({ data: IconData, x: x + d * padFactor, y: y + d * padFactor, w: inner, h: inner });
}

// ---------- INTERFAZ POR TERMINAL (READLINE) ----------
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

function ask(question, defaultValue = "") {
    return new Promise((resolve) => {
        rl.question(question + ` [${defaultValue}]: `, (answer) => {
            resolve(answer.trim() || defaultValue);
        });
    });
}

// ---------- FUNCIÓN PRINCIPAL PARA GENERAR LA PRESENTACIÓN ----------
async function generatePresentation(config, icons, iconsDark) {
    const W = 13.33, H = 7.5;
    let pres = new pptxgen();
    pres.layout = "LAYOUT_WIDE";
    pres.author = "UPCh";
    pres.title = config.title || "Evaluación de Desempeño";

    // Helper para agregar logo (base64 embebido, siempre funciona)
    function addLogo(slide, x, y, w, h) {
        if (config.logoData) {
            try {
                slide.addImage({ data: config.logoData, x, y, w, h, sizing: { type: "contain", w, h } });
            } catch (e) {
                console.warn("⚠️ No se pudo insertar el logo:", e.message);
            }
        }
    }

    // ---------- SLIDE 1: TITLE ----------
    {
        let s = pres.addSlide();
        s.background = { color: MIDNIGHT };
        s.addShape("ellipse", { x: 9.5, y: -2, w: 7, h: 7, fill: { color: DEEP, transparency: 70 }, line: { type: "none" } });
        s.addShape("ellipse", { x: -2.5, y: 4.5, w: 6, h: 6, fill: { color: TEAL, transparency: 75 }, line: { type: "none" } });

        addLogo(s, 0.6, 0.5, 1.7, 0.78);

        s.addText(config.title || "EVALUACIÓN DE DESEMPEÑO", {
            x: 0.7, y: 2.55, w: 11.5, h: 0.9, fontFace: FONT_HEAD, fontSize: 40, bold: true,
            color: WHITE, align: "left", margin: 0
        });
        s.addText("Defensa Grabada Asincrónica (Formato Video)", {
            x: 0.7, y: 3.45, w: 11.5, h: 0.6, fontFace: FONT_BODY, fontSize: 22, italic: true,
            color: GOLD, align: "left", margin: 0
        });
        s.addText(`${config.course || "Asignatura"}  •  Grabación individual de 18 minutos máximo`, {
            x: 0.7, y: 4.15, w: 11, h: 0.5, fontFace: FONT_BODY, fontSize: 15,
            color: ICE, align: "left", margin: 0
        });

        const stats = [
            ["18 min", "Duración máxima del video"],
            ["4 + 1", "Preguntas personalizadas + Bomba"],
            ["100 pts", "Criterio: Desempeño en video"],
        ];
        let sx = 0.7;
        const gap = 0.35, cw = (11.9 - gap * 2) / 3;
        stats.forEach(([num, lbl]) => {
            s.addText(num, { x: sx, y: 5.65, w: cw, h: 0.55, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: WHITE, margin: 0 });
            s.addText(lbl, { x: sx, y: 6.2, w: cw, h: 0.7, fontFace: FONT_BODY, fontSize: 12, color: ICE, margin: 0 });
            sx += cw + gap;
        });
    }

    // ---------- SLIDE 2: FICHA TÉCNICA ----------
    {
        let s = pres.addSlide();
        s.background = { color: WHITE };
        addLogo(s, 11.2, 0.2, 1.9, 0.78);
        s.addText("Ficha técnica de la actividad (No presencial)", { x: 0.7, y: 0.45, w: 10.3, h: 0.7, fontFace: FONT_HEAD, fontSize: 30, bold: true, color: MIDNIGHT, margin: 0 });
        s.addText("Actividad 2 — Evaluación de Desempeño (Grabación asincrónica)", { x: 0.7, y: 1.05, w: 11.9, h: 0.4, fontFace: FONT_BODY, fontSize: 14, italic: true, color: MUTED, margin: 0 });

        const rows = [
            ["clock", "Duración", "18 minutos máximo por estudiante (video MP4)"],
            ["grad", "Modalidad", "Individual — grabación en casa o espacio académico"],
            ["video", "Insumo previo", "Expediente de Resolución Integral entregado (Actividad 1)"],
            ["target", "Qué se evalúa", "Razonamiento aplicado, fluidez verbal y conexión entre unidades"],
            ["clipboard", "Apoyos visuales", "No se permiten notas ni lectura; solo una hoja en blanco"],
            ["link", "Punto crítico", "Debe responder a las preguntas \"¿qué pasaría si?\" integradas en la presentación"],
        ];
        const colW = 5.75, gapX = 0.4, gapY = 0.32, rh = 1.0;
        let positions = [[0.7, 1.75], [6.85, 1.75], [0.7, 1.75 + rh + gapY], [6.85, 1.75 + rh + gapY], [0.7, 1.75 + 2 * (rh + gapY)], [6.85, 1.75 + 2 * (rh + gapY)]];
        rows.forEach(([icon, title, desc], i) => {
            const [x, y] = positions[i];
            s.addShape("roundRect", {
                x, y, w: colW, h: rh, rectRadius: 0.08, fill: { color: ICE }, line: { type: "none" },
                shadow: { type: "outer", color: "000000", blur: 5, offset: 1.5, angle: 90, opacity: 0.08 }
            });
            iconCircle(s, icons[icon], x + 0.22, y + (rh - 0.56) / 2, 0.56, DEEP);
            s.addText(title, { x: x + 0.95, y: y + 0.13, w: colW - 1.15, h: 0.35, fontFace: FONT_HEAD, fontSize: 14, bold: true, color: MIDNIGHT, margin: 0 });
            s.addText(desc, { x: x + 0.95, y: y + 0.46, w: colW - 1.15, h: 0.48, fontFace: FONT_BODY, fontSize: 11.5, color: INK, margin: 0 });
        });
    }

    // ---------- SLIDE 3: LA DINÁMICA ----------
    {
        let s = pres.addSlide();
        s.background = { color: MIDNIGHT };
        s.addText("La dinámica: grabar, no leer", { x: 0.7, y: 0.5, w: 11.9, h: 0.7, fontFace: FONT_HEAD, fontSize: 30, bold: true, color: WHITE, margin: 0 });

        s.addShape("roundRect", { x: 0.7, y: 1.5, w: 11.9, h: 1.7, rectRadius: 0.1, fill: { color: DEEP }, line: { type: "none" } });
        iconCircle(s, icons.mic, 1.0, 1.86, 1.0, MIDNIGHT, 0.26);
        s.addText([
            { text: "No se trata de leer el expediente frente a la cámara. ", options: { bold: true, color: WHITE } },
            { text: "El estudiante debe simular una defensa ante un jurado, respondiendo a escenarios hipotéticos planteados en esta presentación, demostrando que domina las 4 unidades como un sistema.", options: { color: ICE } }
        ], { x: 2.2, y: 1.66, w: 10.1, h: 1.4, fontFace: FONT_BODY, fontSize: 16, valign: "middle", margin: 0, lineSpacingMultiple: 1.15 });

        const why = [
            ["ban", "Sin apuntes en cámara", "El video debe mostrar al estudiante sin leer (mirada a cámara)."],
            ["random", "Preguntas personalizadas", "Cada alumno recibe preguntas únicas basadas en su expediente."],
            ["link", "Cierre integrador", "La pregunta bomba exige conectar el principio (U1) con la conclusión (U4)."],
        ];
        const cw = 3.73, gap = 0.36;
        let x0 = 0.7;
        why.forEach(([icon, t, d]) => {
            s.addShape("roundRect", { x: x0, y: 3.55, w: cw, h: 2.85, rectRadius: 0.08, fill: { color: DEEP }, line: { type: "none" } });
            iconCircle(s, icons[icon], x0 + (cw - 0.7) / 2, 3.85, 0.7, MIDNIGHT, 0.27);
            s.addText(t, { x: x0 + 0.25, y: 4.75, w: cw - 0.5, h: 0.6, fontFace: FONT_HEAD, fontSize: 15, bold: true, color: WHITE, align: "center", margin: 0 });
            s.addText(d, { x: x0 + 0.3, y: 5.35, w: cw - 0.6, h: 0.95, fontFace: FONT_BODY, fontSize: 12, color: ICE, align: "center", margin: 0 });
            x0 += cw + gap;
        });
    }

    // ---------- SLIDE 4: LÍNEA DE TIEMPO ----------
    {
        let s = pres.addSlide();
        s.background = { color: WHITE };
        addLogo(s, 11.2, 0.2, 1.9, 0.78);
        s.addText("Estructura del video (18 minutos)", { x: 0.7, y: 0.45, w: 10.3, h: 0.7, fontFace: FONT_HEAD, fontSize: 30, bold: true, color: MIDNIGHT, margin: 0 });

        const lineY = 2.35, lineX1 = 1.1, lineX2 = 12.2;
        s.addShape("line", { x: lineX1, y: lineY, w: lineX2 - lineX1, h: 0, line: { color: "C9D6DD", width: 3 } });

        const stops = [
            { t: "Min 0", label: "Inicio grabación", frac: 0.0 },
            { t: "Min 5", label: "Fin resumen", frac: 0.28 },
            { t: "Min 6", label: "Inicio preguntas", frac: 0.33 },
            { t: "Min 15", label: "Fin preguntas", frac: 0.83 },
            { t: "Min 18", label: "Fin + Bomba", frac: 1.0 },
        ];
        stops.forEach(st => {
            const cx = lineX1 + (lineX2 - lineX1) * st.frac;
            s.addShape("ellipse", { x: cx - 0.09, y: lineY - 0.09, w: 0.18, h: 0.18, fill: { color: DEEP }, line: { color: WHITE, width: 2 } });
            s.addText(st.t, { x: cx - 0.6, y: lineY - 0.55, w: 1.2, h: 0.3, fontFace: FONT_BODY, fontSize: 10, bold: true, color: MUTED, align: "center", margin: 0 });
            s.addText(st.label, { x: cx - 0.75, y: lineY + 0.18, w: 1.5, h: 0.4, fontFace: FONT_BODY, fontSize: 10.5, color: INK, align: "center", margin: 0 });
        });

        s.addShape("roundRect", { x: 0.7, y: 3.2, w: 5.65, h: 3.6, rectRadius: 0.1, fill: { color: ICE }, line: { type: "none" } });
        iconCircle(s, iconsDark.mic, 1.0, 3.5, 0.7, "FFFFFF", 0.05);
        s.addShape("ellipse", { x: 1.0, y: 3.5, w: 0.7, h: 0.7, fill: { color: DEEP }, line: { type: "none" } });
        s.addImage({ data: icons.mic, x: 1.19, y: 3.69, w: 0.32, h: 0.32 });
        s.addText("FASE 1  ·  Minutos 0–5", { x: 1.85, y: 3.55, w: 4.3, h: 0.35, fontFace: FONT_HEAD, fontSize: 14, bold: true, color: DEEP, margin: 0 });
        s.addText("Resumen ejecutivo sin apoyos", { x: 1.85, y: 3.85, w: 4.3, h: 0.35, fontFace: FONT_BODY, fontSize: 12, italic: true, color: MUTED, margin: 0 });
        s.addText([
            { text: "Mira fijamente a la cámara (simula contacto con el jurado).", options: { breakLine: true, bullet: true } },
            { text: "Sin diapositivas, sin notas, sin el documento abierto.", options: { breakLine: true, bullet: true } },
            { text: "Debe reconstruir la secuencia lógica de la U1 a la U4.", options: { bullet: true } },
        ], { x: 1.0, y: 4.35, w: 5.05, h: 2.3, fontFace: FONT_BODY, fontSize: 12.5, color: INK, margin: 0, paraSpaceAfter: 8 });

        s.addShape("roundRect", { x: 6.65, y: 3.2, w: 5.95, h: 3.6, rectRadius: 0.1, fill: { color: ICE }, line: { type: "none" } });
        s.addShape("ellipse", { x: 6.95, y: 3.5, w: 0.7, h: 0.7, fill: { color: TEAL }, line: { type: "none" } });
        s.addImage({ data: icons.q, x: 7.14, y: 3.69, w: 0.32, h: 0.32 });
        s.addText("FASE 2  ·  Minutos 6–18", { x: 7.8, y: 3.55, w: 4.6, h: 0.35, fontFace: FONT_HEAD, fontSize: 14, bold: true, color: TEAL, margin: 0 });
        s.addText("Respuesta a preguntas grabadas", { x: 7.8, y: 3.85, w: 4.6, h: 0.35, fontFace: FONT_BODY, fontSize: 12, italic: true, color: MUTED, margin: 0 });
        s.addText([
            { text: "Responde a las 4 preguntas personalizadas (U1 a U4).", options: { breakLine: true, bullet: true } },
            { text: "Cada respuesta debe ser fluida y sin cortes de edición.", options: { breakLine: true, bullet: true } },
            { text: "Concluye con la pregunta bomba integradora (U1↔U4).", options: { bullet: true } },
        ], { x: 6.95, y: 4.35, w: 5.35, h: 2.3, fontFace: FONT_BODY, fontSize: 12.5, color: INK, margin: 0, paraSpaceAfter: 8 });
    }

    // ---------- SLIDE 5: FASE 1 DETALLE ----------
    {
        let s = pres.addSlide();
        s.background = { color: WHITE };
        s.addShape("rect", { x: 0, y: 0, w: 4.2, h: H, fill: { color: DEEP }, line: { type: "none" } });
        iconCircle(s, icons.mic, 1.4, 0.9, 1.4, MIDNIGHT, 0.27);
        s.addText("FASE 1", { x: 0.5, y: 2.55, w: 3.2, h: 0.55, fontFace: FONT_HEAD, fontSize: 24, bold: true, color: WHITE, align: "center", margin: 0 });
        s.addText("Resumen ejecutivo\nsin apoyos visuales", { x: 0.5, y: 3.1, w: 3.2, h: 0.9, fontFace: FONT_BODY, fontSize: 14, italic: true, color: ICE, align: "center", margin: 0 });
        s.addText("Minutos 0 – 5", { x: 0.5, y: 4.2, w: 3.2, h: 0.4, fontFace: FONT_BODY, fontSize: 13, bold: true, color: GOLD, align: "center", margin: 0 });

        s.addText("Qué debe lograr el estudiante (en cámara)", { x: 4.7, y: 0.55, w: 8.0, h: 0.5, fontFace: FONT_HEAD, fontSize: 22, bold: true, color: MIDNIGHT, margin: 0 });
        const items = [
            "Solo su rostro y voz: sin diapositivas, sin expediente, sin notas en mano.",
            "Recorrer la secuencia lógica completa: U1 (marco) → U2 (cálculo) → U3 (diseño) → U4 (evaluación).",
            "Explicar el hilo conductor del proyecto: por qué cada unidad llevó a la siguiente.",
            "Mantener un tiempo controlado de 5 minutos; la concisión es clave.",
        ];
        let y = 1.25;
        items.forEach((txt, i) => {
            s.addShape("ellipse", { x: 4.7, y: y, w: 0.42, h: 0.42, fill: { color: ICE }, line: { color: DEEP, width: 1.25 } });
            s.addText(String(i + 1), { x: 4.7, y: y, w: 0.42, h: 0.42, fontFace: FONT_HEAD, fontSize: 14, bold: true, color: DEEP, align: "center", valign: "middle", margin: 0 });
            s.addText(txt, { x: 5.3, y: y - 0.04, w: 7.3, h: 0.85, fontFace: FONT_BODY, fontSize: 13.5, color: INK, valign: "middle", margin: 0 });
            y += 1.05;
        });

        s.addShape("roundRect", { x: 4.7, y: 5.55, w: 7.9, h: 1.35, rectRadius: 0.08, fill: { color: "FCEFE3" }, line: { type: "none" } });
        iconCircle(s, icons.warn, 4.95, 5.78, 0.55, GOLD, 0.22);
        s.addText([
            { text: "Si el estudiante desvía la mirada constantemente o hace pausas largas, ", options: { color: INK } },
            { text: "es señal de que está leyendo un guion oculto", options: { bold: true, color: SAFE_RED } },
            { text: ". Se penaliza.", options: { color: INK } },
        ], { x: 5.65, y: 5.68, w: 6.75, h: 1.0, fontFace: FONT_BODY, fontSize: 12.5, valign: "middle", margin: 0 });
    }

    // ---------- SLIDE 6: FASE 2 - REGLA DE ORO ----------
    {
        let s = pres.addSlide();
        s.background = { color: WHITE };
        addLogo(s, 11.2, 0.2, 1.9, 0.78);
        s.addText("Fase 2: preguntas personalizadas integradas", { x: 0.7, y: 0.45, w: 10.3, h: 0.7, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: MIDNIGHT, margin: 0 });
        s.addText("El estudiante debe responder a 4 preguntas únicas (una por unidad) presentadas en este documento", { x: 0.7, y: 1.05, w: 11.9, h: 0.4, fontFace: FONT_BODY, fontSize: 14, italic: true, color: MUTED, margin: 0 });

        s.addShape("roundRect", { x: 0.7, y: 1.7, w: 5.7, h: 3.0, rectRadius: 0.1, fill: { color: "FCEAEA" }, line: { type: "none" } });
        iconCircle(s, icons.ban, 1.0, 2.0, 0.6, SAFE_RED, 0.24);
        s.addText("Lo que NO debe hacer el alumno", { x: 1.75, y: 2.08, w: 4.4, h: 0.45, fontFace: FONT_HEAD, fontSize: 16, bold: true, color: SAFE_RED, margin: 0 });
        s.addText([
            { text: "Leer textualmente la respuesta preparada.", options: { breakLine: true, italic: true } },
            { text: "Cortar la grabación entre pregunta y pregunta (edición).", options: { breakLine: true } },
            { text: "Usar apuntes fuera del encuadre de la cámara.", options: {} },
        ], { x: 1.0, y: 2.7, w: 5.05, h: 1.85, fontFace: FONT_BODY, fontSize: 13, color: INK, margin: 0, paraSpaceAfter: 6 });

        s.addShape("roundRect", { x: 6.9, y: 1.7, w: 5.7, h: 3.0, rectRadius: 0.1, fill: { color: "E7F4EC" }, line: { type: "none" } });
        iconCircle(s, icons.check, 7.2, 2.0, 0.6, SAFE_GREEN, 0.24);
        s.addText("Lo que SÍ debe hacer", { x: 7.95, y: 2.08, w: 4.4, h: 0.45, fontFace: FONT_HEAD, fontSize: 16, bold: true, color: SAFE_GREEN, margin: 0 });
        s.addText([
            { text: "Leer la pregunta en voz alta, pensar 5 segundos y responder.", options: { breakLine: true, italic: true } },
            { text: "Grabar la sesión entera en un solo take (sin pausas).", options: { breakLine: true } },
            { text: "Apoyarse en el razonamiento, no en la memoria textual.", options: {} },
        ], { x: 7.2, y: 2.7, w: 5.05, h: 1.85, fontFace: FONT_BODY, fontSize: 13, color: INK, margin: 0, paraSpaceAfter: 6 });

        s.addShape("roundRect", { x: 0.7, y: 4.95, w: 11.9, h: 1.9, rectRadius: 0.1, fill: { color: ICE }, line: { type: "none" } });
        iconCircle(s, iconsDark.random, 1.0, 5.25, 0.7, "FFFFFF", 0.05);
        s.addShape("ellipse", { x: 1.0, y: 5.25, w: 0.7, h: 0.7, fill: { color: TEAL }, line: { type: "none" } });
        s.addImage({ data: icons.random, x: 1.19, y: 5.44, w: 0.32, h: 0.32 });
        s.addText("Formato de las preguntas (ejemplo)", { x: 1.85, y: 5.1, w: 10.4, h: 0.4, fontFace: FONT_HEAD, fontSize: 15, bold: true, color: MIDNIGHT, margin: 0 });
        s.addText("\u201C\u00bfQu\u00e9 pasar\u00eda si...?\u201D   ·   \u201C\u00bfC\u00f3mo modificar\u00eda su soluci\u00f3n de la U3 si el dato de la U2 cambiara en un 20%?\u201D   ·   \u201C\u00bfQu\u00e9 har\u00eda diferente si...?\u201D", { x: 1.85, y: 5.55, w: 10.4, h: 1.15, fontFace: FONT_BODY, fontSize: 13, color: INK, margin: 0, valign: "top" });
    }

    // ---------- SLIDE 7: LAS 4 PREGUNTAS POR UNIDAD (Dinámico) ----------
    {
        let s = pres.addSlide();
        s.background = { color: WHITE };
        addLogo(s, 11.2, 0.2, 1.9, 0.78);
        s.addText("Preguntas integradas — una por unidad", { x: 0.7, y: 0.45, w: 10.3, h: 0.6, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: MIDNIGHT, margin: 0 });
        s.addText("El alumno debe responder TODAS estas preguntas en su video de defensa.", { x: 0.7, y: 0.95, w: 11.9, h: 0.4, fontFace: FONT_BODY, fontSize: 13, italic: true, color: MUTED, margin: 0 });

        const colors = [
            { c: DEEP, bg: "E2EEF4" },
            { c: SAFE_GREEN, bg: "E7F4EC" },
            { c: "B5651D", bg: "FBEADB" },
            { c: SAFE_RED, bg: "FCEAEA" },
        ];
        const units = config.units || [
            { name: "U1: Marco Teórico", question: "Si la probabilidad de fallo exigida por FAR/CS cambiara de 10⁻⁹ a 10⁻⁶, ¿qué tipo de fallo dejaría de exigir esa certificación en su diseño?" },
            { name: "U2: Cálculo Termodinámico", question: "¿Cómo cambiaría su validación de la ACM si la temperatura de entrada del aire de sangrado subiera un 20%?" },
            { name: "U3: Diseño FBW", question: "Si el sensor de ángulo de ataque fallara durante la maniobra que describió, ¿qué ley de control tomaría el mando?" },
            { name: "U4: Evaluación y Mejora", question: "¿Cómo cambiaría su estrategia de protección si la temperatura exterior bajara de -20°C a -35°C?" },
        ];

        const cw = 2.85, gap = 0.27;
        let x0 = 0.7;
        units.forEach((u, idx) => {
            const col = colors[idx] || colors[0];
            s.addShape("roundRect", { x: x0, y: 1.6, w: cw, h: 4.7, rectRadius: 0.1, fill: { color: col.bg }, line: { type: "none" } });
            s.addShape("ellipse", { x: x0 + (cw - 0.85) / 2, y: 1.9, w: 0.85, h: 0.85, fill: { color: col.c }, line: { type: "none" } });
            s.addText(`U${idx + 1}`, { x: x0 + (cw - 0.85) / 2, y: 1.9, w: 0.85, h: 0.85, fontFace: FONT_HEAD, fontSize: 20, bold: true, color: WHITE, align: "center", valign: "middle", margin: 0 });
            s.addText(u.name.replace(/^U\d+:\s*/, ''), { x: x0 + 0.15, y: 2.9, w: cw - 0.3, h: 0.65, fontFace: FONT_HEAD, fontSize: 13, bold: true, color: col.c, align: "center", margin: 0 });
            s.addShape("line", { x: x0 + 0.5, y: 3.6, w: cw - 1.0, h: 0, line: { color: col.c, width: 1, dashType: "dash" } });
            s.addText("Tu pregunta:", { x: x0 + 0.18, y: 3.75, w: cw - 0.36, h: 0.3, fontFace: FONT_BODY, fontSize: 10, bold: true, color: MIDNIGHT, margin: 0 });
            s.addText(u.question, { x: x0 + 0.18, y: 4.05, w: cw - 0.36, h: 2.1, fontFace: FONT_BODY, fontSize: 10.5, color: INK, margin: 0 });
            x0 += cw + gap;
        });
    }

    // ---------- SLIDE 8: PREGUNTA BOMBA (Dinámica) ----------
    {
        let s = pres.addSlide();
        s.background = { color: MIDNIGHT };
        s.addShape("ellipse", { x: 9.7, y: -1.5, w: 6, h: 6, fill: { color: SAFE_RED, transparency: 80 }, line: { type: "none" } });

        iconCircle(s, icons.bomb, 0.9, 1.0, 1.6, SAFE_RED, 0.25);
        s.addText("PREGUNTA BOMBA (Integradora)", { x: 2.9, y: 1.15, w: 9.6, h: 0.6, fontFace: FONT_HEAD, fontSize: 30, bold: true, color: WHITE, margin: 0 });
        s.addText("Obligatoria al final del video (minutos 15-18)", { x: 2.9, y: 1.75, w: 9.6, h: 0.45, fontFace: FONT_BODY, fontSize: 15, italic: true, color: GOLD, margin: 0 });

        s.addShape("roundRect", { x: 0.7, y: 2.9, w: 11.9, h: 1.95, rectRadius: 0.1, fill: { color: DEEP }, line: { type: "none" } });
        s.addText("Debe forzar la conexión entre el principio de apertura (Unidad 1) y la conclusión de cierre (Unidad 4).", { x: 1.1, y: 3.1, w: 11.1, h: 0.5, fontFace: FONT_BODY, fontSize: 15, bold: true, color: WHITE, margin: 0 });
        s.addText(config.bombQuestion || "\u201CRetomando el concepto base de la U1 (probabilidad de fallo catastr\u00f3fico), \u00bfc\u00f3mo valida usted que su conclusi\u00f3n de la U4 sobre la estrategia anti-hielo no contradice ese principio?\u201D", {
            x: 1.1, y: 3.7, w: 11.1, h: 1.0, fontFace: FONT_BODY, fontSize: 14, italic: true, color: ICE, margin: 0, valign: "top"
        });

        iconCircle(s, icons.link, 0.9, 5.3, 0.6, TEAL, 0.24);
        s.addText("Por qué importa: una buena respuesta demuestra que el estudiante entendió el expediente como un sistema, no como cuatro tareas sueltas. En el video, debe sonar natural y convincente.", {
            x: 1.7, y: 5.25, w: 10.9, h: 1.1, fontFace: FONT_BODY, fontSize: 13, color: ICE, valign: "middle", margin: 0
        });
    }

    // ---------- SLIDE 9: RUBRICA ----------
    {
        let s = pres.addSlide();
        s.background = { color: WHITE };
        addLogo(s, 11.2, 0.2, 1.9, 0.78);
        s.addText("Rúbrica de evaluación — Desempeño en video (100 puntos)", { x: 0.55, y: 0.4, w: 10.5, h: 0.6, fontFace: FONT_HEAD, fontSize: 24, bold: true, color: MIDNIGHT, margin: 0 });

        const headers = ["Criterio", "Excelente", "Bueno", "Suficiente", "Insuficiente"];
        const rows = [
            ["Resumen ejecutivo\n(Fase 1) — 20 pts",
                "18-20. Secuencia completa U1→U4, sin apoyos, fluida y en tiempo.",
                "14-17. Secuencia correcta con pausas o mirada a notas.",
                "10-13. Secuencia incompleta o desordenada.",
                "0-9. No logra reconstruir la secuencia sin el documento."],
            ["Respuestas U1-U4\n(Fase 2) — 50 pts",
                "45-50. Responde las 4 con razonamiento aplicado y sin lectura.",
                "35-44. Responde 3 de 4 bien, alguna pausa para recordar.",
                "25-34. Responde 2 de 4 o se nota que lee textualmente.",
                "0-24. Responde 0-1 correctamente o usa guion visible."],
            ["Pregunta bomba\nintegradora — 20 pts",
                "18-20. Conecta U1 y U4 con argumento sólido y coherente.",
                "14-17. Conecta ambas unidades con argumento parcial.",
                "10-13. Menciona ambas sin conectarlas realmente.",
                "0-9. No logra relacionar U1 con U4."],
            ["Calidad técnica\ny tiempo — 10 pts",
                "9-10. Audio claro, encuadre correcto, respeta los 18 min.",
                "7-8. Audio aceptable, alguna distracción visual.",
                "5-6. Problemas de audio o exceso de tiempo.",
                "0-4. Grabación ininteligible o incompleta."],
        ];
        const colW = [2.45, 2.46, 2.46, 2.46, 2.47];
        const tableData = [
            headers.map((h, i) => ({ text: h, options: { bold: true, color: "FFFFFF", fill: { color: i === 0 ? MIDNIGHT : [DEEP, SAFE_GREEN, "B5651D", SAFE_RED][i - 1] }, align: "center", fontSize: 11, valign: "middle" } }))
        ];
        rows.forEach(r => {
            tableData.push(r.map((cell, i) => ({
                text: cell,
                options: {
                    fontSize: 9.5, color: i === 0 ? MIDNIGHT : INK, bold: i === 0,
                    fill: { color: i === 0 ? ICE : "FFFFFF" }, align: "left", valign: "top",
                    margin: [4, 5, 4, 5]
                }
            })));
        });
        s.addTable(tableData, {
            x: 0.55, y: 1.15, w: 12.3, colW,
            border: { pt: 0.75, color: "D7DEE3" },
            autoPage: false,
            rowH: [0.5, 1.3, 1.3, 1.3, 1.3]
        });
    }

    // ---------- SLIDE 10: GUÍA PARA REVISIÓN DEL VIDEO ----------
    {
        let s = pres.addSlide();
        s.background = { color: ICE };
        addLogo(s, 11.2, 0.15, 1.9, 0.78);
        s.addText("Guía para la revisión del video (docente)", { x: 0.7, y: 0.5, w: 10.3, h: 0.65, fontFace: FONT_HEAD, fontSize: 28, bold: true, color: MIDNIGHT, margin: 0 });

        const dos = [
            "Revisa la mirada del estudiante: si lee, suele desviarla a los lados o hacia abajo.",
            "Verifica la duración total; debe ser ≤ 18 min. Si excede, penaliza en la rúbrica.",
            "Compara las respuestas con el expediente entregado (Actividad 1) para ver coherencia.",
            "Toma notas en la rúbrica mientras ves el video; no lo hagas de memoria.",
        ];
        s.addShape("roundRect", {
            x: 0.7, y: 1.35, w: 11.9, h: 2.5, rectRadius: 0.1, fill: { color: WHITE }, line: { type: "none" },
            shadow: { type: "outer", color: "000000", blur: 6, offset: 2, angle: 90, opacity: 0.08 }
        });
        s.addText(dos.map((t, i) => ({ text: t, options: { bullet: { code: "2713" }, breakLine: i < dos.length - 1, color: INK } })),
            { x: 1.05, y: 1.6, w: 11.2, h: 2.1, fontFace: FONT_BODY, fontSize: 13, valign: "top", margin: 0, paraSpaceAfter: 10 });

        s.addShape("roundRect", { x: 0.7, y: 4.15, w: 11.9, h: 2.7, rectRadius: 0.1, fill: { color: "FCEAEA" }, line: { type: "none" } });
        s.addText("Señales de alerta (posible falta de autenticidad)", { x: 1.05, y: 4.35, w: 11.2, h: 0.4, fontFace: FONT_HEAD, fontSize: 15, bold: true, color: SAFE_RED, margin: 0 });
        const donts = [
            "Movimientos oculares que indican lectura de un guion fuera de cámara.",
            "Cortes bruscos de edición entre pregunta y pregunta.",
            "Respuestas idénticas al texto literal del expediente (memorización).",
            "Falta de coherencia entre la respuesta verbal y el análisis escrito.",
        ];
        s.addText(donts.map((t, i) => ({ text: t, options: { bullet: { code: "2717" }, breakLine: i < donts.length - 1, color: INK } })),
            { x: 1.05, y: 4.8, w: 11.2, h: 1.9, fontFace: FONT_BODY, fontSize: 13, valign: "top", margin: 0, paraSpaceAfter: 10 });
    }

    // ---------- SLIDE 11: PREPARACIÓN TÉCNICA PARA EL ALUMNO ----------
    {
        let s = pres.addSlide();
        s.background = { color: WHITE };
        addLogo(s, 11.2, 0.2, 1.9, 0.78);
        s.addText("Requisitos técnicos para la grabación (alumno)", { x: 0.7, y: 0.5, w: 10.3, h: 0.65, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: MIDNIGHT, margin: 0 });

        const tips = [
            ["video", "Formato y duración", "MP4 o MOV. Máximo 18 minutos (pasa de los 18' y se descuenta)."],
            ["mic", "Audio y entorno", "Usa auriculares con micrófono. Busca un lugar sin ruido de fondo."],
            ["comments", "Cámara y encuadre", "Cámara a la altura de los ojos. Muestra tu rostro completo, sin sombras."],
            ["clock", "Cronómetro", "Ten un cronómetro visible (puede ser tu teléfono) para controlar el tiempo."],
        ];
        const cw = 5.7, gapX = 0.5, gapY = 0.4, rh = 1.65;
        const pos = [[0.7, 1.4], [6.9, 1.4], [0.7, 1.4 + rh + gapY], [6.9, 1.4 + rh + gapY]];
        tips.forEach(([icon, t, d], i) => {
            const [x, y] = pos[i];
            s.addShape("roundRect", { x, y, w: cw, h: rh, rectRadius: 0.08, fill: { color: ICE }, line: { type: "none" } });
            s.addShape("ellipse", { x: x + 0.25, y: y + (rh - 0.65) / 2, w: 0.65, h: 0.65, fill: { color: DEEP }, line: { type: "none" } });
            s.addImage({ data: icons[icon], x: x + 0.41, y: y + (rh - 0.65) / 2 + 0.16, w: 0.33, h: 0.33 });
            s.addText(t, { x: x + 1.1, y: y + 0.18, w: cw - 1.3, h: 0.4, fontFace: FONT_HEAD, fontSize: 13.5, bold: true, color: MIDNIGHT, margin: 0 });
            s.addText(d, { x: x + 1.1, y: y + 0.58, w: cw - 1.3, h: rh - 0.7, fontFace: FONT_BODY, fontSize: 11.5, color: INK, margin: 0 });
        });
    }

    // ---------- SLIDE 12: CIERRE ----------
    {
        let s = pres.addSlide();
        s.background = { color: MIDNIGHT };
        s.addShape("ellipse", { x: -2, y: -2, w: 6.5, h: 6.5, fill: { color: DEEP, transparency: 70 }, line: { type: "none" } });
        iconCircle(s, icons.check, W / 2 - 0.75, 1.0, 1.5, TEAL, 0.26);
        s.addText("Dominar las cuatro unidades como un sistema integrado", {
            x: 1.5, y: 2.85, w: 10.33, h: 1.0, fontFace: FONT_HEAD, fontSize: 26, bold: true, color: WHITE, align: "center", margin: 0
        });
        s.addText("— la cámara no miente; evalúa la auténtica capacidad de razonamiento técnico.", {
            x: 1.5, y: 3.75, w: 10.33, h: 0.6, fontFace: FONT_BODY, fontSize: 15, italic: true, color: GOLD, align: "center", margin: 0
        });
        addLogo(s, W / 2 - 0.95, 5.6, 1.9, 0.87);
    }

    // Guardar archivo
    const outputFile = config.outputFile || "Evaluacion_Desempeno_Defensa_Grabada.pptx";
    await pres.writeFile({ fileName: outputFile });
    console.log(`✅ Presentación generada exitosamente: ${outputFile}`);
}

// ---------- PROGRAMA PRINCIPAL (INTERACTIVO) ----------
async function main() {
    console.log("\n🚀 GENERADOR DE PRESENTACIÓN - EVALUACIÓN DE DESEMPEÑO (VIDEO)");
    console.log("=".repeat(60));
    console.log("Presiona Enter para usar el valor predeterminado [mostrado entre corchetes].\n");

    // Valores predeterminados (ejemplo aeronáutico)
    const defaults = {
        logo: "logo_upch.png",
        title: "EVALUACIÓN DE DESEMPEÑO",
        course: "Sistemas en Aeronaves - Ingeniería Aeronáutica",
        units: [
            { name: "U1: Marco Teórico", question: "Si la probabilidad de fallo exigida por FAR/CS cambiara de 10⁻⁹ a 10⁻⁶, ¿qué tipo de fallo dejaría de exigir esa certificación en su diseño?" },
            { name: "U2: Cálculo Termodinámico", question: "¿Cómo cambiaría su validación de la ACM si la temperatura de entrada del aire de sangrado subiera un 20%?" },
            { name: "U3: Diseño FBW", question: "Si el sensor de ángulo de ataque fallara durante la maniobra que describió, ¿qué ley de control tomaría el mando?" },
            { name: "U4: Evaluación y Mejora", question: "¿Cómo cambiaría su estrategia de protección si la temperatura exterior bajara de -20°C a -35°C?" },
        ],
        bomb: "Retomando el concepto base de la U1 (probabilidad de fallo catastrófico), ¿cómo valida usted que su conclusión de la U4 sobre la estrategia anti-hielo no contradice ese principio?",
        output: "Evaluacion_Desempeno_Defensa_Grabada.pptx"
    };

    // 1. Logo
    const logoPath = await ask("Ruta del logo (dejar vacío para omitir)", defaults.logo);

    // 2. Título principal
    const title = await ask("Título de la presentación", defaults.title);

    // 3. Curso / Asignatura
    const course = await ask("Nombre del curso / asignatura", defaults.course);

    // 4. Unidades (4 preguntas)
    const units = [];
    console.log("\n📚 Ahora ingresa las 4 unidades (título y pregunta de ejemplo):");
    for (let i = 0; i < 4; i++) {
        console.log(`\n--- Unidad ${i + 1} ---`);
        const defaultName = defaults.units[i]?.name || `Unidad ${i + 1}`;
        const defaultQ = defaults.units[i]?.question || "Escribe aquí la pregunta de ejemplo para esta unidad.";
        const name = await ask(`Título de la Unidad ${i + 1}`, defaultName);
        const question = await ask(`Pregunta para la Unidad ${i + 1}`, defaultQ);
        units.push({ name, question });
    }

    // 5. Pregunta Bomba
    console.log("\n💣 Pregunta Bomba (integradora U1 ↔ U4):");
    const bomb = await ask("Texto de la pregunta bomba", defaults.bomb);

    // 6. Nombre del archivo de salida
    const output = await ask("Nombre del archivo de salida (.pptx)", defaults.output);

    // Cerrar interfaz readline
    rl.close();

    // ---------- GENERAR ICONOS ----------
    console.log("\n⏳ Generando iconos y presentación...");
    const icons = {};
    const specs = [
        ["mic", FaMicrophone, WHITE],
        ["clock", FaClock, WHITE],
        ["grad", FaUserGraduate, WHITE],
        ["q", FaQuestionCircle, WHITE],
        ["bomb", FaBomb, WHITE],
        ["check", FaCheckCircle, WHITE],
        ["warn", FaExclamationTriangle, WHITE],
        ["target", FaBullseye, WHITE],
        ["comments", FaComments, WHITE],
        ["layers", FaLayerGroup, WHITE],
        ["clipboard", FaClipboardList, WHITE],
        ["ban", FaBan, WHITE],
        ["random", FaRandom, WHITE],
        ["link", FaLink, WHITE],
        ["video", FaVideo, WHITE],
        ["file-video", FaFileVideo, WHITE],
    ];
    for (const [key, comp] of specs) {
        icons[key] = await iconToBase64Png(comp, WHITE, 256);
    }
    const iconsDark = {};
    for (const [key, comp] of specs) {
        iconsDark[key] = await iconToBase64Png(comp, DEEP, 256);
    }

    // ---------- CARGAR LOGO ----------
    const logoData = loadLogoBase64();
    if (logoData) {
        console.log("✅ Logo UPCh cargado correctamente.");
    } else {
        console.warn("⚠️  No se encontró logo_upch.png — la presentación se generará sin logo.");
    }

    // ---------- GENERAR PRESENTACIÓN ----------
    const config = { logoData, title, course, units, bombQuestion: bomb, outputFile: output };
    await generatePresentation(config, icons, iconsDark);

    console.log("\n🎉 ¡Proceso completado!");
}

main().catch(e => {
    console.error("❌ Error:", e);
    process.exit(1);
});