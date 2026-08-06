import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

W, H = A4
MARGIN = 2 * cm

# ── Paleta de colores ──────────────────────────────────────────────────────
AZUL = colors.HexColor('#185FA5')
AZUL_CLR = colors.HexColor('#E6F1FB')
TEAL = colors.HexColor('#0F6E56')
TEAL_CLR = colors.HexColor('#E1F5EE')
GRIS = colors.HexColor('#5F5E5A')
GRIS_CLR = colors.HexColor('#F1EFE8')
CORAL = colors.HexColor('#993C1D')
CORAL_CLR = colors.HexColor('#FAECE7')
NEGRO = colors.HexColor('#2C2C2A')
BLANCO = colors.white
LINEA = colors.HexColor('#D3D1C7')
ALERTA = colors.HexColor('#D32F2F')
ALERTA_CLR = colors.HexColor('#FFEBEE')

# ── Estilos de texto ───────────────────────────────────────────────────────
def make_styles():
    s = {}
    base = dict(fontName='Helvetica', fontSize=10, leading=14, textColor=NEGRO, spaceAfter=4)

    s['titulo_doc'] = ParagraphStyle('titulo_doc', **{**base,
        'fontName': 'Helvetica-Bold', 'fontSize': 20, 'leading': 24,
        'textColor': AZUL, 'alignment': TA_CENTER, 'spaceAfter': 6})

    s['subtitulo_doc'] = ParagraphStyle('subtitulo_doc', **{**base,
        'fontSize': 11, 'textColor': GRIS, 'alignment': TA_CENTER, 'spaceAfter': 4})

    s['seccion'] = ParagraphStyle('seccion', **{**base,
        'fontName': 'Helvetica-Bold', 'fontSize': 14, 'textColor': AZUL,
        'spaceBefore': 12, 'spaceAfter': 6})

    s['paso_titulo'] = ParagraphStyle('paso_titulo', **{**base,
        'fontName': 'Helvetica-Bold', 'fontSize': 10, 'textColor': TEAL,
        'spaceAfter': 2, 'spaceBefore': 6})

    s['cuerpo'] = ParagraphStyle('cuerpo', **{**base,
        'fontSize': 10, 'leading': 15, 'spaceAfter': 4})

    s['formula'] = ParagraphStyle('formula', **{**base,
        'fontName': 'Courier', 'fontSize': 11, 'leading': 16,
        'textColor': AZUL, 'leftIndent': 12, 'spaceAfter': 4})

    s['tabla_header'] = ParagraphStyle('tabla_header', **{**base,
        'fontName': 'Helvetica-Bold', 'fontSize': 10, 'textColor': BLANCO,
        'alignment': TA_CENTER})

    s['tabla_cell'] = ParagraphStyle('tabla_cell', **{**base,
        'fontSize': 10, 'alignment': TA_LEFT})

    s['nota'] = ParagraphStyle('nota', **{**base,
        'fontSize': 9, 'textColor': GRIS, 'leftIndent': 12, 'spaceAfter': 4})

    s['alerta'] = ParagraphStyle('alerta', **{**base,
        'fontName': 'Helvetica-Bold', 'fontSize': 9, 'textColor': ALERTA,
        'leftIndent': 12, 'spaceAfter': 4})

    return s

ST = make_styles()

# ── Helpers de diseño ──────────────────────────────────────────────────────
def header_block(titulo, color_fondo):
    data = [[Paragraph(titulo, ParagraphStyle(
        'hb', fontName='Helvetica-Bold', fontSize=12, textColor=BLANCO, leading=16))]]
    t = Table(data, colWidths=[W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color_fondo),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return t

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=LINEA, spaceAfter=8, spaceBefore=8)

def formula_table(headers, rows, col_widths):
    data = [[Paragraph(h, ST['tabla_header']) for h in headers]]
    for r in rows:
        data.append([Paragraph(c, ST['tabla_cell']) for c in r])

    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), AZUL),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.4, LINEA),
    ]
    for i in range(1, len(data)):
        bg = AZUL_CLR if i % 2 == 0 else BLANCO
        style.append(('BACKGROUND', (0, i), (-1, i), bg))
    t.setStyle(TableStyle(style))
    return t

# ── Datos de las fórmulas ──────────────────────────────────────────────────

MRU_DATA = [
    ["Magnitud", "Fórmula", "Cuándo usarla"],
    ["Velocidad", "v = Δd / t", "Conocemos desplazamiento y tiempo"],
    ["Desplazamiento", "Δd = v · t", "Conocemos velocidad y tiempo"],
    ["Tiempo", "t = Δd / v", "Conocemos desplazamiento y velocidad"]
]

MRUA_DATA = [
    ["Ecuación", "Fórmula", "Falta conocer..."],
    ["1ª Ecuación", "Vf = Vi + a·t", "El desplazamiento (d)"],
    ["2ª Ecuación", "d = Vi·t + ½·a·t²", "La velocidad final (Vf)"],
    ["3ª Ecuación", "Vf² = Vi² + 2·a·d", "El tiempo (t)"],
    ["4ª Ecuación", "d = (Vi + Vf)/2 · t", "La aceleración (a)"]
]

CAIDA_LIBRE_DATA = [
    ["Magnitud", "Fórmula (desde el reposo, Vi = 0)"],
    ["Velocidad final", "Vf = g · t"],
    ["Altura caída", "h = ½ · g · t²"],
    ["Velocidad vs Altura", "Vf² = 2 · g · h"],
    ["Tiempo de caída", "t = √(2h / g)"]
]

TIRO_VERTICAL_DATA = [
    ["Fase", "Fórmulas"],
    ["Subida (desacelera)", "Vf = Vi - g·t  |  h = Vi·t - ½·g·t²  |  Vf² = Vi² - 2·g·h"],
    ["Punto más alto", "Vf = 0 m/s  |  t_subida = Vi / g  |  H_max = Vi² / (2g)"],
    ["Bajada (acelera)", "Vf = g·t_bajada  |  h = ½·g·t_bajada²"]
]

TIRO_PARABOLICO_DATA = [
    ["Componente", "Fórmula"],
    ["Velocidad inicial X", "V0x = V0 · cos(θ)  (Se mantiene constante)"],
    ["Velocidad inicial Y", "V0y = V0 · sin(θ)  (Cambia por la gravedad)"],
    ["Posición en X (MRU)", "x = V0x · t"],
    ["Posición en Y (MRUA)", "y = V0y · t - ½·g·t²"],
    ["Velocidad en Y", "Vy = V0y - g·t"],
    ["Tiempo de vuelo total", "T = 2 · V0 · sin(θ) / g"],
    ["Altura máxima", "H = V0² · sin²(θ) / (2g)"],
    ["Alcance horizontal", "R = V0² · sin(2θ) / g"]
]

# ── Construcción del documento ─────────────────────────────────────────────
def build_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN)
    story = []

    # ── Encabezado ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("HOJA DE FÓRMULAS DE CINEMÁTICA", ST['titulo_doc']))
    story.append(Paragraph("Unidad 2: Correcciones y Complementos", ST['subtitulo_doc']))
    story.append(Paragraph("g = 9.8 m/s² | Sistema Internacional de Unidades (SI)", ST['subtitulo_doc']))
    story.append(Spacer(1, 0.4 * cm))
    story.append(hr())
    story.append(Spacer(1, 0.4 * cm))

    # ── Nota Importante sobre Distancia vs Desplazamiento ──────────────────
    story.append(header_block("⚠️ CORRECCIÓN IMPORTANTE: Distancia vs. Desplazamiento", ALERTA))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "En los apuntes originales se definía la velocidad como 'desplazamiento / tiempo', pero se usaba 'd = distancia' en la fórmula. "
        "Esto es un error conceptual. La fórmula correcta es:", ST['cuerpo']))
    story.append(Paragraph("Velocidad (vectorial):  v = Δd / t   (usa DESPLAZAMIENTO, cambio neto de posición)", ST['formula']))
    story.append(Paragraph("Rapidez (escalar):      v = d / t    (usa DISTANCIA, espacio total recorrido)", ST['formula']))
    story.append(Spacer(1, 6))
    story.append(hr())

    # ── MRU ────────────────────────────────────────────────────────────────
    story.append(Paragraph("1. Movimiento Rectilíneo Uniforme (MRU)", ST['seccion']))
    story.append(Paragraph("La velocidad es constante, por lo tanto, la aceleración es cero (a = 0).", ST['cuerpo']))
    story.append(Spacer(1, 4))
    story.append(formula_table(MRU_DATA[0], MRU_DATA[1:], [4*cm, 6*cm, 7.5*cm]))
    story.append(Spacer(1, 0.6 * cm))

    # ── MRUA ───────────────────────────────────────────────────────────────
    story.append(Paragraph("2. Movimiento Rectilíneo Uniformemente Acelerado (MRUA)", ST['seccion']))
    story.append(Paragraph("La aceleración es constante. Estas son las 4 ecuaciones fundamentales que faltaban en los apuntes:", ST['cuerpo']))
    story.append(Spacer(1, 4))
    story.append(formula_table(MRUA_DATA[0], MRUA_DATA[1:], [5*cm, 6*cm, 6.5*cm]))
    story.append(Spacer(1, 0.6 * cm))

    # ── Caída Libre ────────────────────────────────────────────────────────
    story.append(Paragraph("3. Caída Libre", ST['seccion']))
    story.append(Paragraph("Movimiento bajo la única influencia de la gravedad (g = 9.8 m/s² hacia abajo). Fórmulas para un objeto que se deja caer desde el reposo (Vi = 0):", ST['cuerpo']))
    story.append(Spacer(1, 4))
    story.append(formula_table(CAIDA_LIBRE_DATA[0], CAIDA_LIBRE_DATA[1:], [7*cm, 10.5*cm]))
    story.append(Spacer(1, 0.6 * cm))

    # ── Tiro Vertical ──────────────────────────────────────────────────────
    story.append(Paragraph("4. Tiro Vertical", ST['seccion']))
    story.append(Paragraph("Cuando se lanza un objeto hacia arriba, la gravedad actúa en sentido contrario al movimiento (desaceleración). En el punto más alto, la velocidad es momentáneamente cero (Vf = 0).", ST['cuerpo']))
    story.append(Spacer(1, 2))

    # Tabla especial para Tiro Vertical (2 columnas)
    tv_data = [[Paragraph(h, ST['tabla_header']) for h in TIRO_VERTICAL_DATA[0]]]
    for r in TIRO_VERTICAL_DATA[1:]:
        tv_data.append([Paragraph(r[0], ST['tabla_cell']), Paragraph(r[1], ST['formula'])])

    tv_table = Table(tv_data, colWidths=[4*cm, 13.5*cm], repeatRows=1)
    tv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.4, LINEA),
        ('BACKGROUND', (0, 1), (-1, -1), TEAL_CLR),
    ]))
    story.append(tv_table)
    story.append(Spacer(1, 0.6 * cm))

    # ── Tiro Parabólico ────────────────────────────────────────────────────
    story.append(Paragraph("5. Tiro Parabólico", ST['seccion']))
    story.append(Paragraph(
        "Es la superposición de un MRU en el eje X y un MRUA en el eje Y. "
        "Lo primero que se debe hacer es descomponer la velocidad inicial, algo que faltaba en los apuntes originales:", ST['cuerpo']))
    story.append(Spacer(1, 4))
    story.append(formula_table(TIRO_PARABOLICO_DATA[0], TIRO_PARABOLICO_DATA[1:], [5.5*cm, 12*cm]))
    story.append(Spacer(1, 0.6 * cm))

    # ── Recordatorios de Conversión ────────────────────────────────────────
    story.append(hr())
    story.append(Paragraph("Recordatorios de Conversión de Unidades", ST['seccion']))
    story.append(Paragraph("• De km/h a m/s:  dividir entre 3.6  (ej: 72 km/h ÷ 3.6 = 20 m/s)", ST['cuerpo']))
    story.append(Paragraph("• De m/s a km/h:  multiplicar por 3.6  (ej: 15 m/s × 3.6 = 54 km/h)", ST['cuerpo']))
    story.append(Paragraph("• De minutos a segundos:  multiplicar por 60", ST['cuerpo']))
    story.append(Spacer(1, 0.4 * cm))

    story.append(Paragraph(
        "Nota: Esta hoja complementa los apuntes de la Unidad 2, corrigiendo las omisiones y errores conceptuales "
        "para garantizar que los cálculos en los ejercicios se realicen con las ecuaciones físicas correctas.", ST['nota']))

    # ── Generar PDF ────────────────────────────────────────────────────────
    doc.build(story)
    print(f"✅ PDF generado exitosamente en: {os.path.abspath(path)}")

# ── Ejecución ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    output_path = "./formulas_cinematica_corregidas.pdf"
    build_pdf(output_path)
