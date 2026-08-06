const {
    Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
    Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
    Header, Footer, PageNumber, TabStopType, TabStopPosition,
    LevelFormat, convertInchesToTwip, PageOrientation, VerticalAlign,
    Numbering,
} = require("docx");
const fs = require("fs");

// ---------- Paleta ----------
const NAVY = "0B2545";
const STEEL = "13315C";
const TEAL = "1B998B";
const LIGHT = "EFF3F6";
const GRAY = "5A6B7B";
const AMBER = "B9770E";

// ---------- Helpers ----------
function h1(text, opts = {}) {
    return new Paragraph({
        heading: HeadingLevel.HEADING_1,
        spacing: { before: 480, after: 240 },
        border: { bottom: { color: NAVY, space: 4, style: BorderStyle.SINGLE, size: 12 } },
        children: [new TextRun({ text, bold: true, color: NAVY, size: 30 })],
        ...opts,
    });
}
function h2(text) {
    return new Paragraph({
        heading: HeadingLevel.HEADING_2,
        spacing: { before: 360, after: 160 },
        children: [new TextRun({ text, bold: true, color: STEEL, size: 25 })],
    });
}
function h3(text) {
    return new Paragraph({
        spacing: { before: 220, after: 100 },
        children: [new TextRun({ text, bold: true, color: TEAL, size: 22 })],
    });
}
function body(text, opts = {}) {
    return new Paragraph({
        spacing: { after: 160, line: 300 },
        alignment: AlignmentType.JUSTIFIED,
        children: [new TextRun({ text, size: 21, ...opts })],
    });
}
function bullet(text, level = 0) {
    return new Paragraph({
        numbering: { reference: "bullets", level },
        spacing: { after: 90, line: 280 },
        children: [new TextRun({ text, size: 21 })],
    });
}
function note(text) {
    return new Paragraph({
        spacing: { before: 120, after: 200 },
        shading: { type: ShadingType.CLEAR, fill: "FCF3E3" },
        border: {
            left: { color: AMBER, space: 8, style: BorderStyle.SINGLE, size: 18 },
        },
        indent: { left: 120 },
        children: [new TextRun({ text, italics: true, size: 20, color: "7A5300" })],
    });
}

// Bloque de Objetivo (O)
function objetivoPara(id, texto) {
    return new Paragraph({
        spacing: { after: 100, line: 276 },
        indent: { left: convertInchesToTwip(0.55), hanging: convertInchesToTwip(0) },
        children: [
            new TextRun({ text: `${id}:  `, bold: true, color: TEAL, size: 20 }),
            new TextRun({ text: texto, size: 20 }),
        ],
    });
}

// Bloque de Competencia (C) con sus objetivos
function competenciaBlock(comp) {
    const paras = [];
    paras.push(
        new Paragraph({
            spacing: { before: 160, after: 100 },
            indent: { left: convertInchesToTwip(0.25) },
            children: [
                new TextRun({ text: `${comp.id}. `, bold: true, color: STEEL, size: 21 }),
                new TextRun({ text: comp.enunciado, bold: true, size: 21 }),
            ],
        })
    );
    comp.objetivos.forEach((o) => paras.push(objetivoPara(o.id, o.texto)));
    return paras;
}

// Bloque de Función (F) con tabla de encabezado + competencias
function funcionBlock(fn) {
    const paras = [];
    paras.push(
        new Table({
            width: { size: 100, type: WidthType.PERCENTAGE },
            borders: {
                top: { style: BorderStyle.SINGLE, size: 4, color: NAVY },
                bottom: { style: BorderStyle.SINGLE, size: 4, color: NAVY },
                left: { style: BorderStyle.SINGLE, size: 4, color: NAVY },
                right: { style: BorderStyle.SINGLE, size: 4, color: NAVY },
                insideHorizontal: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
                insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            },
            rows: [
                new TableRow({
                    children: [
                        new TableCell({
                            width: { size: 100, type: WidthType.PERCENTAGE },
                            shading: { type: ShadingType.CLEAR, fill: NAVY },
                            margins: { top: 120, bottom: 120, left: 160, right: 160 },
                            children: [
                                new Paragraph({
                                    children: [
                                        new TextRun({ text: `${fn.id}  `, bold: true, color: "FFFFFF", size: 22 }),
                                        new TextRun({ text: fn.enunciado, bold: true, color: "FFFFFF", size: 22 }),
                                    ],
                                }),
                            ],
                        }),
                    ],
                }),
            ],
        })
    );
    paras.push(new Paragraph({ spacing: { after: 60 }, children: [] }));
    fn.competencias.forEach((c) => competenciaBlock(c).forEach((p) => paras.push(p)));
    return paras;
}

function areaSection(area) {
    const out = [];
    out.push(
        new Paragraph({
            pageBreakBefore: true,
            heading: HeadingLevel.HEADING_1,
            spacing: { before: 0, after: 40 },
            children: [new TextRun({ text: `ÁREA ${area.numero}`, bold: true, color: TEAL, size: 20 })],
        })
    );
    out.push(
        new Paragraph({
            spacing: { after: 100 },
            border: { bottom: { color: NAVY, space: 6, style: BorderStyle.SINGLE, size: 14 } },
            children: [new TextRun({ text: area.titulo, bold: true, color: NAVY, size: 30 })],
        })
    );
    if (area.descripcion) out.push(body(area.descripcion));
    area.funciones.forEach((f) => funcionBlock(f).forEach((p) => out.push(p)));
    return out;
}

// ================= DATOS DE CONTENIDO (ACTUALIZADOS CON SUGERENCIAS) =================

const area2 = {
    numero: 2,
    titulo: "Mercado Laboral en Bases de Mantenimiento, Talleres, Aeropuertos y Hangares (Operación en Plataforma Aérea y Logística)",
    descripcion:
        "Comprende las funciones ligadas a la operación diaria de aeronaves en plataforma, hangares y aeropuertos: manejo de sistemas de apoyo técnico y de navegación, monitoreo del desempeño técnico-operativo, y cumplimiento de los marcos normativos de seguridad operacional. Este perfil corresponde al personal que da soporte directo a la aeronavegabilidad en bases de operación, y es directamente relevante para la actividad aeroportuaria y de aviación general del estado de Chihuahua.",
    funciones: [
        {
            id: "F4",
            enunciado:
                "Operar (L3) sistemas de gestión y equipos de apoyo técnico siguiendo protocolos operativos, con el propósito de asegurar la disponibilidad de los vehículos aéreos.",
            competencias: [
                {
                    id: "F4.C1",
                    enunciado: "Identificar (L1) la ubicación y funcionamiento de los sistemas críticos mediante documentación técnica.",
                    objetivos: [
                        { id: "F4.C1.O1", texto: "Nombrar (L1) las secciones principales de la aeronave mediante sistemas de clasificación estándar para localizarlas en manuales de servicio." },
                        { id: "F4.C1.O2", texto: "Identificar (L1) físicamente los componentes de comunicación y energía mediante la inspección técnica para su reconocimiento operativo." },
                        { id: "F4.C1.O3", texto: "Describir (L2) la función de las superficies de mando y control mediante manuales de operación para entender el movimiento del vehículo." },
                    ],
                },
                {
                    id: "F4.C2",
                    enunciado: "Comprender (L2) la disposición general y operatividad de los sistemas de navegación.",
                    objetivos: [
                        { id: "F4.C2.O1", texto: "Identificar (L1) los instrumentos de vuelo en cabina mediante guías visuales para interpretar la información de navegación." },
                        { id: "F4.C2.O2", texto: "Explicar (L2) la interacción entre sistemas de aviónica mediante diagramas para comprender la integración electrónica." },
                        { id: "F4.C2.O3", texto: "Describir (L2) los procedimientos de prueba de sistemas mediante listas de verificación para validar la operatividad previa al vuelo." },
                    ],
                },
                {
                    id: "F4.C3",
                    enunciado: "Reconocer (L1) los componentes de los equipos de apoyo terrestre.",
                    objetivos: [
                        // REENCUADRE INGENIERIL APLICADO
                        { id: "F4.C3.O1", texto: "Especificar (L3) los requerimientos técnicos y protocolos de interfaz de las unidades de potencia externa (GPU) con los sistemas eléctricos de la aeronave, para diseñar procedimientos seguros de operación en plataforma." },
                        { id: "F4.C3.O2", texto: "Identificar (L1) las herramientas de remolque y posicionamiento mediante la observación en rampa para la movilización de aeronaves." },
                        { id: "F4.C3.O3", texto: "Definir (L1) los protocolos de abastecimiento de fluidos mediante normativas de seguridad para prevenir riesgos de contaminación." },
                    ],
                },
                // NUEVA COMPETENCIA AGREGADA (LOGÍSTICA AOG)
                {
                    id: "F4.C4",
                    enunciado: "Gestionar (L3) el flujo de materiales, rotables y consumibles aeronáuticos mediante sistemas ERP/MRO, para minimizar los tiempos de Aircraft On Ground (AOG) y asegurar la continuidad operativa.",
                    objetivos: [
                        { id: "F4.C4.O1", texto: "Clasificar (L2) los componentes aeronáuticos según su criticidad operativa (rotables, reparables, consumibles, life-limited parts) para priorizar su gestión en almacén." },
                        { id: "F4.C4.O2", texto: "Aplicar (L3) procedimientos de control de inventario y trazabilidad de partes (form 8130-3, EASA Form 1) mediante sistemas ERP especializados (ej. AMOS, TRAX, CAMP) para garantizar la disponibilidad técnica." },
                        { id: "F4.C4.O3", texto: "Coordinar (L3) la logística de emergencia AOG (Aircraft On Ground) con proveedores y talleres externos para reducir el tiempo de inoperatividad de la aeronave." },
                    ],
                },
            ],
        },
        {
            id: "F5",
            enunciado:
                "Diferenciar (L4) desviaciones en el desempeño técnico y operativo de los sistemas mediante el análisis de información de vuelo para orientar las intervenciones.",
            competencias: [
                {
                    id: "F5.C1",
                    enunciado: "Identificar (L1) las variables críticas de funcionamiento registradas en sistemas de monitoreo.",
                    objetivos: [
                        { id: "F5.C1.O1", texto: "Enlistar (L1) parámetros de presión, temperatura y flujo mediante la lectura de instrumentos para su registro en bitácoras." },
                        { id: "F5.C1.O2", texto: "Reconocer (L1) los límites operativos de la planta de potencia mediante tablas de rendimiento para detectar sobreesfuerzos." },
                        { id: "F5.C1.O3", texto: "Definir (L1) códigos de anomalías reportados por sistemas de diagnóstico mediante bases de datos técnicas para su interpretación." },
                    ],
                },
                {
                    id: "F5.C2",
                    enunciado: "Describir (L2) el comportamiento aerodinámico y de rendimiento según configuración.",
                    objetivos: [
                        { id: "F5.C2.O1", texto: "Explicar (L2) la variación de la sustentación mediante el análisis de curvas polares para comprender el desempeño en diferentes fases." },
                        { id: "F5.C2.O2", texto: "Resumir (L2) los efectos de la atmósfera estándar en el empuje mediante leyes de propulsión para evaluar la eficiencia del motor." },
                        { id: "F5.C2.O3", texto: "Identificar (L1) las condiciones de estabilidad estática mediante la observación de superficies de control para predecir la respuesta del vehículo." },
                    ],
                },
                {
                    id: "F5.C3",
                    enunciado: "Comprender (L2) la lógica de diagnóstico técnico mediante la consulta de bases de datos.",
                    objetivos: [
                        { id: "F5.C3.O1", texto: "Localizar (L2) fallos intermitentes en sistemas electrónicos mediante software de simulación para su análisis preventivo." },
                        { id: "F5.C3.O2", texto: "Comparar (L2) datos históricos de mantenimiento mediante registros técnicos para identificar patrones de falla." },
                        { id: "F5.C3.O3", texto: "Explicar (L2) el flujo de señales en sistemas digitales mediante lógica de programación para agilizar el diagnóstico." },
                    ],
                },
                // NUEVA F5.C4 (L4) — ESLABÓN PERDIDO: diagnóstico predictivo
                {
                    id: "F5.C4",
                    enunciado: "Diagnosticar (L4) tendencias de degradación de sistemas mediante el análisis estadístico de datos de vuelo (AHM - Aircraft Health Management), para proponer intervenciones de mantenimiento predictivo.",
                    objetivos: [
                        { id: "F5.C4.O1", texto: "Interpretar (L4) series temporales de parámetros de rendimiento (EGT, vibraciones, presiones de combustible) registrados por AHM para identificar desviaciones tempranas." },
                        { id: "F5.C4.O2", texto: "Correlacionar (L4) eventos de mantenimiento correctivo con patrones de datos de vuelo mediante herramientas de análisis estadístico para modelar la tasa de degradación." },
                        { id: "F5.C4.O3", texto: "Recomendar (L4) ventanas de intervención predictiva basadas en umbrales de alerta temprana para optimizar la disponibilidad de la aeronave." },
                    ],
                },
            ],
        },
        {
            id: "F6",
            enunciado: "Aplicar (L3) marcos de gestión de la seguridad y normativas vigentes en las áreas de operación técnica para mitigar riesgos.",
            competencias: [
                {
                    id: "F6.C1",
                    enunciado: "Identificar (L1) los fundamentos de los sistemas de gestión de la seguridad operacional (SMS).",
                    objetivos: [
                        { id: "F6.C1.O1", texto: "Nombrar (L1) los pilares del SMS mediante los anexos de la OACI para conocer la estructura de seguridad." },
                        { id: "F6.C1.O2", texto: "Describir (L2) los procedimientos de reporte de incidentes mediante formatos estandarizados para fomentar la cultura de prevención." },
                        { id: "F6.C1.O3", texto: "Identificar (L1) las zonas de seguridad mediante señalética técnica para evitar accidentes." },
                    ],
                },
                {
                    id: "F6.C2",
                    enunciado: "Reconocer (L1) las reglamentaciones nacionales e internacionales que rigen la operación.",
                    objetivos: [
                        { id: "F6.C2.O1", texto: "Enlistar (L1) las atribuciones de las autoridades aeronáuticas mediante la legislación civil para cumplir con el marco legal." },
                        { id: "F6.C2.O2", texto: "Identificar (L1) las normas de seguridad en el trabajo mediante manuales de prevención de riesgos para proteger la integridad física." },
                        { id: "F6.C2.O3", texto: "Definir (L1) los criterios de aeronavegabilidad continua mediante directivas técnicas para asegurar la vigencia operativa." },
                    ],
                },
                {
                    id: "F6.C3",
                    enunciado: "Clasificar (L2) los factores de riesgo y procedimientos de emergencia en tierra.",
                    objetivos: [
                        { id: "F6.C3.O1", texto: "Identificar (L1) riesgos potenciales de fuego y derrames mediante protocolos de seguridad para su control inmediato." },
                        { id: "F6.C3.O2", texto: "Explicar (L2) el uso de equipos de protección personal mediante medidas sanitarias de instalaciones aeroportuarias." },
                        { id: "F6.C3.O3", texto: "Clasificar (L2) tipos de equipos portátiles de primera respuesta (ejemplo: extintores) mediante especificaciones técnicas para su aplicación en siniestros aeronáuticos." },
                    ],
                },
            ],
        },
    ],
};

const area3 = {
    numero: 3,
    titulo: "Técnicos de Mantenimiento en el Estado de México (Ecosistema MRO)",
    descripcion:
        "Agrupa las funciones propias del ecosistema de Mantenimiento, Reparación y Overhaul (MRO), concentrado principalmente en el Estado de México (hub histórico de MRO de línea aérea y componentes en el país). Cubre desde el mantenimiento de planta motriz hasta la trazabilidad documental necesaria para el retorno al servicio y el aseguramiento de procesos especiales certificados.",
    funciones: [
        {
            id: "F7",
            enunciado: "Ejecutar (L3) programas de mantenimiento técnico y restauración de sistemas de potencia empleando documentación técnica, para garantizar la recuperación operativa.",
            competencias: [
                {
                    id: "F7.C1",
                    enunciado: "Identificar (L1) las secciones y componentes de la planta motriz.",
                    objetivos: [
                        { id: "F7.C1.O1", texto: "Distinguir (L2) entre tipos de plantas motrices mediante esquemas técnicos para su identificación en el taller." },
                        { id: "F7.C1.O2", texto: "Nombrar (L1) los elementos de la sección de combustión y energía mediante manuales de taller para la planificación de inspecciones." },
                        { id: "F7.C1.O3", texto: "Describir (L2) el funcionamiento de sistemas auxiliares de potencia mediante bibliografía técnica para conocer su interrelación." },
                    ],
                },
                // COMPETENCIA F7.C2 REESCRITA COMPLETA PARA SUBIR A NIVEL L3 (EL ESLABÓN PERDIDO)
                {
                    id: "F7.C2",
                    enunciado: "Aplicar (L3) procedimientos de desensamble, inspección dimensional y ensamble de módulos de planta motriz utilizando herramientas especializadas y documentación técnica del fabricante (CMM/AMM), para garantizar la restauración operativa del componente.",
                    objetivos: [
                        { id: "F7.C2.O1", texto: "Ejecutar (L3) el desarmado secuencial de secciones del motor mediante el manual de taller (CMM) para preservar la integridad de los componentes." },
                        { id: "F7.C2.O2", texto: "Utilizar (L3) instrumentos de medición de precisión (micrómetros, calibradores, plastigage) para verificar tolerancias de juego axial y radial contra los límites del fabricante." },
                        // REENCUADRE INGENIERIL APLICADO
                        { id: "F7.C2.O3", texto: "Diseñar (L3) los procedimientos de limpieza, preparación y tratamiento de superficies de componentes críticos, basándose en las especificaciones del OEM y normativas ambientales, para estandarizar el proceso en el taller MRO." },
                    ],
                },
                {
                    id: "F7.C3",
                    enunciado: "Reconocer (L1) los estados de funcionamiento normal y límites de desgaste.",
                    objetivos: [
                        { id: "F7.C3.O1", texto: "Enlistar (L1) las tolerancias de juego axial y radial mediante instrumentos de medición para validar el estado de partes móviles." },
                        { id: "F7.C3.O2", texto: "Identificar (L1) signos de fatiga y corrosión mediante inspección visual para determinar la vida útil remanente." },
                        { id: "F7.C3.O3", texto: 'Definir (L1) los criterios de "vencido por tiempo" mediante registros de mantenimiento para programar reemplazos.' },
                    ],
                },
            ],
        },
        {
            id: "F8",
            enunciado: "Analizar (L4) la integridad y trazabilidad de las intervenciones técnicas realizadas a través del desglose de registros para certificar la aeronavegabilidad.",
            competencias: [
                {
                    id: "F8.C1",
                    enunciado: "Identificar (L1) los requerimientos legales y documentales para la certificación.",
                    objetivos: [
                        { id: "F8.C1.O1", texto: "Enlistar (L1) los registros técnicos necesarios para el retorno al servicio mediante la regulación vigente para certificar el mantenimiento." },
                        { id: "F8.C1.O2", texto: "Reconocer (L1) la validez de certificados de componentes mediante la consulta de registros oficiales para asegurar la legalidad técnica." },
                        { id: "F8.C1.O3", texto: "Definir (L1) el alcance de las alteraciones técnicas mediante directivas de seguridad para cumplir con estándares de vuelo." },
                    ],
                },
                {
                    id: "F8.C2",
                    enunciado: "Comprender (L2) los criterios de aeronavegabilidad y retorno al servicio.",
                    objetivos: [
                        { id: "F8.C2.O1", texto: "Explicar (L2) las condiciones necesarias para la firma de liberación mediante normativas de la autoridad aeronáutica para validar el trabajo." },
                        { id: "F8.C2.O2", texto: "Resumir (L2) las responsabilidades del personal técnico mediante el código de ética profesional para asegurar el cumplimiento regulatorio." },
                        { id: "F8.C2.O3", texto: "Identificar (L1) la jerarquía de la documentación técnica mediante el marco institucional para priorizar fuentes de información." },
                    ],
                },
                {
                    id: "F8.C3",
                    enunciado: "Reconocer (L1) las directivas de aeronavegabilidad y boletines de servicio.",
                    objetivos: [
                        { id: "F8.C3.O1", texto: "Localizar (L2) boletines de servicio urgentes mediante portales de fabricantes para su implementación inmediata." },
                        { id: "F8.C3.O2", texto: "Identificar (L1) el cumplimiento de directivas de aeronavegabilidad mediante el historial de la aeronave para garantizar la seguridad." },
                        { id: "F8.C3.O3", texto: "Enlistar (L1) las reparaciones mayores no programadas mediante registros de taller para evaluar su impacto estructural." },
                    ],
                },
                // NUEVA F8.C4 (L4) — ESLABÓN PERDIDO: auditoría de trazabilidad
                {
                    id: "F8.C4",
                    enunciado: "Auditar (L4) la trazabilidad documental de intervenciones técnicas (logbooks, forms 8130-3, EASA Form 1) mediante sistemas de gestión MRO, para dictaminar la aeronavegabilidad continua de la aeronave.",
                    objetivos: [
                        { id: "F8.C4.O1", texto: "Verificar (L4) la integridad de la cadena de custodia documental de componentes rotables y reparables mediante auditoría cruzada contra registros ERP/MRO para certificar la trazabilidad." },
                        { id: "F8.C4.O2", texto: "Evaluar (L4) el cumplimiento normativo de las liberaciones al servicio (CRS - Certificate of Release to Service) contra la regulación aplicable (FAR 145 / EASA Part 145 / AFAC) para dictaminar la aeronavegabilidad." },
                        { id: "F8.C4.O3", texto: "Dictaminar (L4) la condición de aeronavegabilidad de una aeronave o componente mediante la revisión integrada de su historial de mantenimiento, boletines de servicio y directivas de aeronavegabilidad." },
                    ],
                },
            ],
        },
        {
            id: "F9",
            enunciado: "Implementar (L3) técnicas de aseguramiento de procesos técnicos especializados mediante procedimientos estandarizados para incrementar la confiabilidad.",
            competencias: [
                {
                    id: "F9.C1",
                    enunciado: "Identificar (L1) los métodos de inspección avanzada para la detección de fallos.",
                    objetivos: [
                        { id: "F9.C1.O1", texto: "Nombrar (L1) técnicas de boroscopía y ultrasonido mediante manuales de inspección para la revisión interna de motores." },
                        { id: "F9.C1.O2", texto: "Describir (L2) los criterios de degradación de materiales mediante análisis de fatiga para prevenir fallas estructurales." },
                        { id: "F9.C1.O3", texto: "Explicar (L2) los procesos de calibración de instrumentos mediante normas técnicas para garantizar la precisión diagnóstica." },
                    ],
                },
                {
                    id: "F9.C2",
                    enunciado: "Describir (L2) los principios de gestión de capital humano y capacitación técnica.",
                    objetivos: [
                        { id: "F9.C2.O1", texto: "Identificar (L1) las necesidades de entrenamiento mediante la evaluación de brechas de competencia para mejorar el desempeño del taller." },
                        { id: "F9.C2.O2", texto: "Resumir (L2) los principios de trabajo en equipo mediante dinámicas de grupo para optimizar las reparaciones mayores." },
                        { id: "F9.C2.O3", texto: "Explicar (L2) la importancia del factor humano mediante el estudio de errores típicos para reducir incidentes en mantenimiento." },
                    ],
                },
                {
                    id: "F9.C3",
                    enunciado: "Reconocer (L1) los estándares de calidad internacionales aplicables a procesos especiales.",
                    objetivos: [
                        { id: "F9.C3.O1", texto: "Identificar (L1) los requisitos para procesos de soldadura y tratamientos térmicos mediante normas industriales para validar reparaciones." },
                        { id: "F9.C3.O2", texto: "Listar (L1) las certificaciones de talleres MRO mediante auditorías externas para asegurar la competitividad global." },
                        { id: "F9.C3.O3", texto: "Definir (L1) los protocolos de control de materiales y consumibles mediante manuales de almacén para evitar el uso de partes no aprobadas." },
                    ],
                },
                // NUEVA F9.C4 (L3) — ESLABÓN PERDIDO: inspecciones no destructivas
                {
                    id: "F9.C4",
                    enunciado: "Ejecutar (L3) inspecciones no destructivas (END) mediante técnicas de boroscopía, ultrasonido y partículas magnéticas en componentes críticos, aplicando los criterios de aceptación/rechazo del fabricante para certificar la integridad estructural.",
                    objetivos: [
                        { id: "F9.C4.O1", texto: "Seleccionar (L3) la técnica END apropiada (boroscopía, ultrasonido, partículas magnéticas, líquidos penetrantes) según el tipo de componente y el modo de falla esperado para maximizar la detectabilidad." },
                        { id: "F9.C4.O2", texto: "Ejecutar (L3) el barrido sistemático de inspección en áreas críticas (álabes de turbina, discos de compresor, largueros de ala) siguiendo los procedimientos del fabricante (CMM/NDT Manual) para asegurar la cobertura." },
                        { id: "F9.C4.O3", texto: "Dictaminar (L4) la condición del componente inspeccionado aplicando los criterios de aceptación/rechazo (rejection criteria) del manual de mantenimiento para liberar, reparar o reemplazar la pieza." },
                    ],
                },
            ],
        },
    ],
};

const area4 = {
    numero: 4,
    titulo: "Diseño e Ingeniería Aeroespacial (Enfoque OEM / Tier 1 — Chihuahua)",
    descripcion:
        "Corresponde al perfil de mayor valor agregado y es el que da identidad de ingeniería (y no solo de técnico) al programa: diseño, análisis numérico y validación de componentes y sistemas aeronáuticos bajo requerimientos de manufactura original (OEM). Esta área es la que se alinea de forma directa con el clúster aeroespacial de Chihuahua — el más integrado de México — donde operan de forma simultánea fabricantes OEM (Bell, Honeywell, Textron Aviation, EZ Air —joint venture Safran-Embraer— y Bombardier) y una base amplia de proveedores Tier 1 certificados (entre otros, Safran, GKN, Nordam, Lisi Aerospace, Tighitco, Arnprior Aerospace) especializados en aeroestructuras, mecanizado de precisión, interiores, arneses e integración de sistemas.",
    funciones: [
        {
            id: "F10",
            enunciado: "Diseñar (L3) componentes y sistemas aeronáuticos mediante la integración de requerimientos de manufactura original (OEM), para asegurar la viabilidad técnica y operativa en el ensamblaje final.",
            competencias: [
                {
                    id: "F10.C1",
                    enunciado: "Identificar (L1) los requerimientos de misión y límites operativos bajo estándares técnicos.",
                    objetivos: [
                        { id: "F10.C1.O1", texto: "Enlistar (L1) los parámetros operativos de la aeronave mediante manuales técnicos para definir el alcance del diseño." },
                        { id: "F10.C1.O2", texto: "Definir (L1) los límites de carga y la envolvente de vuelo mediante leyes físicas para establecer restricciones estructurales." },
                        { id: "F10.C1.O3", texto: "Identificar (L1) las restricciones de peso y balance mediante documentación técnica para asegurar la estabilidad del vehículo." },
                    ],
                },
                {
                    id: "F10.C2",
                    enunciado: "Comprender (L2) las normativas de certificación y diseño de ingeniería aplicables al sector.",
                    objetivos: [
                        { id: "F10.C2.O1", texto: "Describir (L2) los criterios de aeronavegabilidad vigentes mediante normas de certificación para validar la seguridad del diseño." },
                        { id: "F10.C2.O2", texto: "Identificar (L1) los estándares internacionales de diseño estructural mediante la regulación civil para garantizar el cumplimiento legal." },
                        { id: "F10.C2.O3", texto: "Enunciar (L1) los protocolos de validación técnica mediante normatividad industrial para asegurar la calidad del proyecto." },
                    ],
                },
                // COMPETENCIA F10.C3 REESCRITA COMPLETA PARA SUBIR A NIVEL L3 (EL ESLABÓN PERDIDO)
                {
                    id: "F10.C3",
                    enunciado: "Desarrollar (L3) modelos paramétricos y planos de ensamble de componentes aeronáuticos utilizando software CAD especializado (CATIA V5/V6, NX, SolidWorks), cumpliendo con los estándares de definición de productos aeroespaciales (GD&T, ASME Y14.5).",
                    objetivos: [
                        { id: "F10.C3.O1", texto: "Modelar (L3) piezas y subensambles aeronáuticos mediante técnicas de parametrización y superficies complejas en software CAD 3D." },
                        { id: "F10.C3.O2", texto: "Generar (L3) planos de manufactura con tolerancias geométricas y dimensionales (GD&T) conforme a normas ASME para asegurar la intercambiabilidad de componentes." },
                        { id: "F10.C3.O3", texto: "Estructurar (L3) el árbol de producto (BOM - Bill of Materials) en el entorno CAD para organizar la jerarquía de ensamble y vincularlo con el sistema ERP/PLM." },
                    ],
                },
            ],
        },
        {
            id: "F11",
            enunciado: "Analizar (L4) la integridad estructural y el comportamiento aerodinámico de prototipos mediante herramientas de simulación avanzada, con la finalidad de optimizar el desempeño y mitigar riesgos.",
            competencias: [
                {
                    id: "F11.C1",
                    enunciado: "Identificar (L1) las variables críticas de interacción entre fluidos y estructuras.",
                    objetivos: [
                        { id: "F11.C1.O1", texto: "Nombrar (L1) las fuerzas aerodinámicas actuantes mediante el análisis de interacción fluido-geometría para predecir cargas." },
                        { id: "F11.C1.O2", texto: "Identificar (L1) las zonas de concentración de esfuerzos mediante el análisis estructural para prevenir fallos mecánicos." },
                        { id: "F11.C1.O3", texto: "Definir (L1) los parámetros térmicos críticos mediante leyes de termodinámica para evaluar la transferencia de energía." },
                    ],
                },
                // COMPETENCIA F11.C2 REESCRITA COMPLETA PARA SUBIR A NIVEL L3 (EL ESLABÓN PERDIDO)
                {
                    id: "F11.C2",
                    enunciado: "Modelar (L3) el comportamiento fluido-estructural y térmico de componentes aeronáuticos mediante software de simulación (CFD/FEA), para predecir su desempeño bajo condiciones operativas reales.",
                    objetivos: [
                        { id: "F11.C2.O1", texto: "Configurar (L3) las condiciones de frontera y cargas en software de elementos finitos (ej. ANSYS, NASTRAN) para simular esfuerzos estructurales en aeroestructuras." },
                        { id: "F11.C2.O2", texto: "Ejecutar (L3) simulaciones de dinámica de fluidos computacional (CFD) para evaluar la distribución de presiones y temperaturas en perfiles aerodinámicos." },
                        { id: "F11.C2.O3", texto: "Interpretar (L4) los resultados de las simulaciones (mapas de esfuerzos, coeficientes de sustentación/arrastre) para validar o rediseñar el prototipo." },
                    ],
                },
                {
                    id: "F11.C3",
                    enunciado: "Diferenciar (L2) las configuraciones de sistemas y selección de materiales avanzados.",
                    objetivos: [
                        { id: "F11.C3.O1", texto: "Comparar (L2) el rendimiento entre distintas configuraciones geométricas mediante pruebas digitales para optimizar la sustentación." },
                        { id: "F11.C3.O2", texto: "Distinguir (L2) las propiedades mecánicas de materiales compuestos y superaleaciones mediante el estudio de microestructuras." },
                        { id: "F11.C3.O3", texto: "Clasificar (L2) los sistemas de control y propulsión mediante su arquitectura técnica para determinar su impacto en el diseño global." },
                    ],
                },
            ],
        },
        {
            id: "F12",
            enunciado: "Validar (L3) la conformidad técnica de diseños y procesos mediante protocolos de verificación y ensayos, para certificar el cumplimiento de estándares de aeronavegabilidad y calidad industrial.",
            competencias: [
                {
                    id: "F12.C1",
                    enunciado: "Reconocer (L1) los procedimientos de prueba y criterios de éxito técnico.",
                    objetivos: [
                        { id: "F12.C1.O1", texto: "Identificar (L1) las etapas del ciclo de desarrollo de producto mediante documentación organizacional para el seguimiento técnico." },
                        { id: "F12.C1.O2", texto: "Enlistar (L1) los requerimientos de funcionalidad mediante especificaciones de diseño para el control de pruebas." },
                        { id: "F12.C1.O3", texto: "Nombrar (L1) los estándares de tolerancia dimensional mediante normas técnicas para la verificación de componentes." },
                    ],
                },
                {
                    id: "F12.C2",
                    enunciado: "Comprender (L2) los procesos de integración y control de configuración.",
                    objetivos: [
                        { id: "F12.C2.O1", texto: "Explicar (L2) la secuencia de ensamble mediante representaciones tridimensionales para evitar interferencias físicas." },
                        { id: "F12.C2.O2", texto: "Resumir (L2) las desviaciones dimensionales mediante reportes de inspección para corregir modelos de ingeniería." },
                        { id: "F12.C2.O3", texto: "Describir (L2) la integración de sistemas de energía y control mediante diagramas lógicos para validar la interoperabilidad." },
                    ],
                },
                {
                    id: "F12.C3",
                    enunciado: "Identificar (L1) los modos de fallo potencial mediante métodos de evaluación predictiva.",
                    objetivos: [
                        { id: "F12.C3.O1", texto: "Definir (L1) los modos de falla comunes mediante el análisis histórico para fortalecer el diseño preventivo." },
                        { id: "F12.C3.O2", texto: "Reconocer (L1) signos de fatiga y degradación estructural mediante simulaciones mecánicas para estimar la vida útil." },
                        { id: "F12.C3.O3", texto: "Identificar (L1) anomalías en el comportamiento esperado del sistema mediante la comparación de datos reales frente a teóricos." },
                    ],
                },
                // NUEVA COMPETENCIA AGREGADA (PLM Y GEMELOS DIGITALES)
                {
                    id: "F12.C4",
                    enunciado: "Administrar (L3) el ciclo de vida del producto aeronáutico (PLM) y la configuración digital del prototipo, para asegurar la trazabilidad desde el diseño hasta la manufactura y el mantenimiento.",
                    objetivos: [
                        { id: "F12.C4.O1", texto: "Configurar (L3) la estructura de datos del producto en un sistema PLM (Teamcenter/ENOVIA) para gestionar revisiones, cambios de ingeniería (ECO/ECN) y la línea base de diseño." },
                        { id: "F12.C4.O2", texto: "Integrar (L3) el modelo CAD 3D con datos de simulación, manufactura y mantenimiento para construir un Gemelo Digital (Digital Twin) del componente aeronáutico." },
                        { id: "F12.C4.O3", texto: "Validar (L4) la coherencia entre el diseño CAD, el BOM de ingeniería (EBOM) y el BOM de manufactura (MBOM) mediante el sistema PLM para evitar interferencias en la producción." },
                    ],
                },
            ],
        },
    ],
};

const doc = new Document({
    numbering: {
        config: [{
            reference: "bullets",
            levels: [
                { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT },
                { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT },
            ],
        }],
    },
    sections: [
        {
            properties: {
                page: {
                    margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
                },
            },
            children: [
                h1("Perfil de Egreso y Competencias Sectoriales", { alignment: AlignmentType.CENTER }),
                ...areaSection(area2),
                ...areaSection(area3),
                ...areaSection(area4),
            ],
        },
    ],
});

// ================= EXPORTACIÓN A ARCHIVO .DOCX =================

Packer.toBuffer(doc).then((buffer) => {
    fs.writeFileSync("Perfil_Egreso_Areas_Corregido.docx", buffer);
    console.log("✅ Documento 'Perfil_Egreso_Areas_Corregido.docx' generado exitosamente.");
    console.log("📋 Cambios integrados:");
    console.log("   • F4.C4: Logística AOG y gestión de rotables (NUEVA)");
    console.log("   • F4.C3.O1: Reencuadre ingenieril (Especificar GPU)");
    console.log("   • F5.C4: Diagnóstico predictivo AHM (NUEVA - L4)");
    console.log("   • F7.C2: Reescrita completa a nivel L3 (Aplicar procedimientos de desensamble)");
    console.log("   • F7.C2.O3: Reencuadre ingenieril (Diseñar procedimientos de limpieza)");
    console.log("   • F8.C4: Auditoría de trazabilidad documental MRO (NUEVA - L4)");
    console.log("   • F9.C4: Inspecciones no destructivas END (NUEVA - L3)");
    console.log("   • F10.C3: Reescrita completa a nivel L3 (Desarrollar modelos paramétricos CAD)");
    console.log("   • F11.C2: Reescrita completa a nivel L3 (Modelar CFD/FEA)");
    console.log("   • F12.C4: PLM y Gemelos Digitales (NUEVA)");
}).catch((err) => {
    console.error("❌ Error al generar el documento:", err);
});