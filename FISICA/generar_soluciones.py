import os
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, Image
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

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

# ── Estilos de texto ───────────────────────────────────────────────────────
def make_styles():
    s = {}
    base = dict(fontName='DejaVuSans', fontSize=10, leading=14, textColor=NEGRO, spaceAfter=4)

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
        'fontName': 'Courier', 'fontSize': 10, 'leading': 14,
        'textColor': AZUL, 'leftIndent': 12, 'spaceAfter': 3})

    s['resultado'] = ParagraphStyle('resultado', **{**base,
        'fontName': 'Helvetica-Bold', 'fontSize': 11, 'textColor': TEAL,
        'leftIndent': 12, 'spaceAfter': 6})

    s['tabla_header'] = ParagraphStyle('tabla_header', **{**base,
        'fontName': 'Helvetica-Bold', 'fontSize': 9, 'textColor': BLANCO,
        'alignment': TA_CENTER})

    s['tabla_cell'] = ParagraphStyle('tabla_cell', **{**base,
        'fontSize': 9, 'alignment': TA_LEFT})

    s['nota'] = ParagraphStyle('nota', **{**base,
        'fontSize': 9, 'textColor': GRIS, 'leftIndent': 12, 'spaceAfter': 4})

    return s

ST = make_styles()

# ── Helpers de diseño ──────────────────────────────────────────────────────
def header_block(titulo, color_fondo):
    data = [[Paragraph(titulo, ParagraphStyle(
        'hb', fontName='DejaVuSans-Bold', fontSize=12, textColor=BLANCO, leading=16))]]
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

def dato_row(items):
    cells = [Paragraph(f"<b>{k}:</b> {v}", ST['nota']) for k, v in items]
    widths = [(W - 2 * MARGIN) / len(cells)] * len(cells)
    t = Table([cells], colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), GRIS_CLR),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.3, LINEA),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return t

def res_box(label, value, color=TEAL_CLR, text_color=TEAL):
    data = [[Paragraph(f"✔  <b>{label}:</b>  {value}", ParagraphStyle(
        'rb', fontName='DejaVuSans-Bold', fontSize=11, textColor=text_color, leading=16))]]
    t = Table(data, colWidths=[W - 2 * MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), color),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
    ]))
    return t


FIG_W, FIG_H = 5.0, 2.0

def fig_to_rl(fig, width_cm=13):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#F1EFE8', edgecolor='none')
    buf.seek(0)
    plt.close(fig)
    img = Image(buf, width=width_cm*cm, height=width_cm*cm*(FIG_H/FIG_W))
    return img

def ax_base(ax, bg='#F1EFE8'):
    ax.set_facecolor(bg)
    ax.tick_params(labelsize=7, colors='#5F5E5A')
    for sp in ax.spines.values():
        sp.set_color('#D3D1C7')
    ax.grid(True, color='#D3D1C7', linewidth=0.4, linestyle='--', alpha=0.7)

def plot_velocidad(v, t):
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax_base(ax)
    time = np.linspace(0, float(t), 100)
    dist = float(v) * time
    ax.plot(time, dist, color='#185FA5', lw=2)
    ax.set_xlabel('Tiempo (s)', fontsize=7, color='#5F5E5A')
    ax.set_ylabel('Distancia (m)', fontsize=7, color='#5F5E5A')
    ax.set_title('Gráfico Distancia vs Tiempo (MRU)', fontsize=8, color='#2C2C2A', pad=4)
    fig.tight_layout(pad=0.4)
    return fig_to_rl(fig)

def plot_aceleracion(vi, a, t):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(FIG_W*1.2, FIG_H))
    ax_base(ax1)
    ax_base(ax2)
    time = np.linspace(0, float(t), 100)
    vel = float(vi) + float(a) * time
    dist = float(vi) * time + 0.5 * float(a) * time**2
    
    ax1.plot(time, vel, color='#993C1D', lw=2)
    ax1.set_xlabel('Tiempo (s)', fontsize=7)
    ax1.set_ylabel('Velocidad (m/s)', fontsize=7)
    ax1.set_title('Velocidad vs Tiempo', fontsize=8)
    
    ax2.plot(time, dist, color='#0F6E56', lw=2)
    ax2.set_xlabel('Tiempo (s)', fontsize=7)
    ax2.set_ylabel('Distancia (m)', fontsize=7)
    ax2.set_title('Distancia vs Tiempo', fontsize=8)
    
    fig.tight_layout(pad=0.4)
    return fig_to_rl(fig, width_cm=14)

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=LINEA, spaceAfter=8, spaceBefore=8)

def problema_block(num, titulo, datos, formulas, desarrollo, resultados, pdata=None):
    elems = [
        header_block(f"Problema {num}: {titulo}", AZUL),
        Spacer(1, 6),
        dato_row(datos),
        Spacer(1, 6),
        Paragraph("Fórmulas:", ST['paso_titulo'])
    ]
    for f in formulas:
        elems.append(Paragraph(f, ST['formula']))

    elems.append(Spacer(1, 4))
    elems.append(Paragraph("Desarrollo:", ST['paso_titulo']))
    for d in desarrollo:
        elems.append(Paragraph(d, ST['cuerpo']))

    elems.append(Spacer(1, 4))
    for label, value in resultados:
        elems.append(res_box(label, value))

    if pdata:
        elems.append(Spacer(1, 6))
        if pdata['type'] == 'v':
            elems.append(plot_velocidad(pdata['v'], pdata['t']))
        elif pdata['type'] == 'a':
            elems.append(plot_aceleracion(pdata['vi'], pdata['a'], pdata['t']))
        elems.append(Spacer(1, 4))

    return KeepTogether(elems)

# ── Datos de los problemas ─────────────────────────────────────────────────

CONCEPTOS_DATA = [
    ["Concepto", "Definición", "Ejemplo aplicado a mecánica"],
    ["Posición", "Lugar donde se encuentra un objeto en un sistema de referencia.", "Posición del pistón dentro del cilindro."],
    ["Desplazamiento", "Cambio de posición, representado por un vector.", "El pistón se mueve 10 cm del punto muerto superior al inferior."],
    ["Rapidez", "Magnitud escalar que indica qué tan rápido se mueve un objeto.", "Una llanta gira a 30 m/s."],
    ["Velocidad", "Rapidez con dirección; magnitud vectorial.", "Un auto avanza a 60 km/h hacia el norte."],
    ["Aceleración lineal", "Cambio de velocidad en línea recta.", "El auto pasa de 0 a 100 km/h en 8 s."],
    ["Aceleración", "Cambio de velocidad en magnitud y dirección.", "Una moto acelera mientras toma una curva."],
    ["Masa", "Cantidad de materia de un cuerpo.", "Un motor tiene una masa de 120 kg."],
    ["Peso", "Fuerza con que la gravedad atrae a un cuerpo: P = m·g.", "El motor ejerce un peso de ≈1176 N."],
    ["Gravedad", "Constante de 9.8 m/s² hacia el centro de la Tierra.", "Una herramienta cae del elevador con esa aceleración."],
    ["Movimiento rectilíneo", "Trayectoria en línea recta, velocidad constante o variable.", "Un auto circula en carretera recta."],
    ["MRUA", "Movimiento recto con aceleración constante.", "Un coche acelera desde reposo hasta 80 km/h en 10 s."]
]

VELOCIDAD_PROBLEMAS = [
    {
        "num": 1, "titulo": "Rapidez de un corredor",
        "datos": [("d", "3 km"), ("t", "10 min = 1/6 hr = 600 s")],
        "formulas": ["v = d / t"],
        "desarrollo": [
            "<b>a) En km/hr:</b> v = 3 km / (1/6 hr) = 3 × 6 = 18 km/hr",
            "<b>b) En m/s:</b> v = 3,000 m / 600 s = 5 m/s"
        ],
        "resultados": [("Rapidez", "18 km/hr"), ("Rapidez", "5 m/s")], "pdata": {"type": "v", "v": 5, "t": 600}
    },
    {
        "num": 2, "titulo": "Tiempo de un corredor",
        "datos": [("v", "7 m/s (Norte)"), ("d", "3 km = 3,000 m")],
        "formulas": ["t = d / v"],
        "desarrollo": ["t = 3,000 m / 7 m/s = 428.57 s", "En minutos: 428.57 / 60 = 7.14 min"],
        "resultados": [("Tiempo", "428.57 s (7.14 min)")], "pdata": {"type": "v", "v": 7, "t": 428.57}
    },
    {
        "num": 3, "titulo": "Distancia de una chita",
        "datos": [("v", "130 km/h"), ("t", "4 min = 4/60 hr = 1/15 hr")],
        "formulas": ["d = v × t"],
        "desarrollo": ["d = 130 km/h × (1/15) h = 8.67 km", "En metros: 8.67 × 1,000 = 8,670 m"],
        "resultados": [("Distancia", "8.67 km (8,670 m)")], "pdata": {"type": "v", "v": 36.11, "t": 240}
    },
    {
        "num": 4, "titulo": "Velocidad de un bebé gateando",
        "datos": [("d", "8 m"), ("t", "10 min = 600 s")],
        "formulas": ["v = d / t"],
        "desarrollo": ["v = 8 m / 600 s = 0.0133 m/s", "En km/h: 0.0133 × 3.6 = 0.048 km/h"],
        "resultados": [("Velocidad", "0.0133 m/s (0.048 km/h)")], "pdata": {"type": "v", "v": 0.0133, "t": 600}
    },
    {
        "num": 5, "titulo": "Distancia de un ciclista",
        "datos": [("v", "10 m/s"), ("t", "125 s")],
        "formulas": ["d = v × t"],
        "desarrollo": ["d = 10 m/s × 125 s = 1,250 m", "En km: 1,250 / 1,000 = 1.25 km"],
        "resultados": [("Distancia", "1,250 m (1.25 km)")], "pdata": {"type": "v", "v": 10, "t": 125}
    },
    {
        "num": 6, "titulo": "Velocidad de un motociclista",
        "datos": [("d", "8 km = 8,000 m (Este)"), ("t", "9 min = 540 s")],
        "formulas": ["v = d / t"],
        "desarrollo": ["v = 8,000 m / 540 s = 14.81 m/s"],
        "resultados": [("Velocidad", "14.81 m/s hacia el Este")], "pdata": {"type": "v", "v": 14.81, "t": 540}
    },
    {
        "num": 7, "titulo": "Desplazamiento de un automóvil",
        "datos": [("v", "80 km/h (Norte)"), ("t", "0.8 min = 0.8/60 hr ≈ 0.0133 hr")],
        "formulas": ["d = v × t"],
        "desarrollo": ["d = 80 km/h × 0.0133 hr = 1.067 km", "En metros: 1.067 × 1,000 = 1,067 m"],
        "resultados": [("Desplazamiento", "1,067 m hacia el Norte")], "pdata": {"type": "v", "v": 22.22, "t": 48}
    }
]

ACELERACION_PROBLEMAS = [
    {
        "num": 1, "titulo": "Avión aterrizando en portaaviones",
        "datos": [("Vi", "90 m/s"), ("Vf", "0 m/s"), ("d", "100 m")],
        "formulas": ["Vf² = Vi² + 2ad", "Vf = Vi + at"],
        "desarrollo": [
            "<b>a) Aceleración:</b> 0² = 90² + 2a(100) → 0 = 8,100 + 200a → a = -8,100 / 200 = -40.5 m/s²",
            "<b>b) Tiempo:</b> 0 = 90 + (-40.5)t → t = 90 / 40.5 = 2.22 s"
        ],
        "resultados": [("Aceleración", "-40.5 m/s² (desaceleración)"), ("Tiempo", "2.22 s")], "pdata": {"type": "a", "vi": 90, "a": -40.5, "t": 2.22}
    },
    {
        "num": 2, "titulo": "Tren acelerando constantemente",
        "datos": [("Vi", "16 m/s"), ("a", "2 m/s²"), ("t", "20 s")],
        "formulas": ["d = Vit + ½at²", "Vf = Vi + at"],
        "desarrollo": [
            "<b>a) Distancia:</b> d = (16)(20) + ½(2)(20)² = 320 + 400 = 720 m",
            "<b>b) Velocidad final:</b> Vf = 16 + (2)(20) = 16 + 40 = 56 m/s"
        ],
        "resultados": [("Distancia", "720 m"), ("Velocidad final", "56 m/s")], "pdata": {"type": "a", "vi": 16, "a": 2, "t": 20}
    },
    {
        "num": 3, "titulo": "Lancha de motor desde el reposo",
        "datos": [("Vi", "0 m/s"), ("Vf", "15 m/s"), ("t", "6 s")],
        "formulas": ["a = (Vf - Vi) / t", "d = Vit + ½at²"],
        "desarrollo": [
            "<b>a) Aceleración:</b> a = (15 - 0) / 6 = 2.5 m/s²",
            "<b>b) Distancia:</b> d = 0 + ½(2.5)(6)² = 1.25 × 36 = 45 m"
        ],
        "resultados": [("Aceleración", "2.5 m/s²"), ("Distancia", "45 m")], "pdata": {"type": "a", "vi": 0, "a": 2.5, "t": 6}
    },
    {
        "num": 4, "titulo": "Automóvil de carreras",
        "datos": [("Vi", "20 m/s"), ("Vf", "37 m/s"), ("t", "2.5 s")],
        "formulas": ["a = (Vf - Vi) / t"],
        "desarrollo": ["a = (37 - 20) / 2.5 = 17 / 2.5 = 6.8 m/s²"],
        "resultados": [("Aceleración", "6.8 m/s²")], "pdata": {"type": "a", "vi": 20, "a": 6.8, "t": 2.5}
    },
    {
        "num": 5, "titulo": "Motociclista frenando",
        "datos": [("Vi", "35 m/s"), ("Vf", "0 m/s"), ("t", "1.8 s")],
        "formulas": ["a = (Vf - Vi) / t"],
        "desarrollo": ["a = (0 - 35) / 1.8 = -35 / 1.8 = -19.44 m/s²"],
        "resultados": [("Desaceleración", "-19.44 m/s²")], "pdata": {"type": "a", "vi": 35, "a": -19.44, "t": 1.8}
    },
    {
        "num": 6, "titulo": "Automóvil de carreras (2)",
        "datos": [("Vi", "18.5 m/s"), ("Vf", "46.1 m/s"), ("t", "2.47 s")],
        "formulas": ["a = (Vf - Vi) / t"],
        "desarrollo": ["a = (46.1 - 18.5) / 2.47 = 27.6 / 2.47 = 11.17 m/s²"],
        "resultados": [("Aceleración", "11.17 m/s²")], "pdata": {"type": "a", "vi": 18.5, "a": 11.17, "t": 2.47}
    },
    {
        "num": 7, "titulo": "Motociclista frenando (2)",
        "datos": [("Vi", "22.4 m/s"), ("Vf", "0 m/s"), ("t", "2.55 s")],
        "formulas": ["a = (Vf - Vi) / t"],
        "desarrollo": ["a = (0 - 22.4) / 2.55 = -22.4 / 2.55 = -8.78 m/s²"],
        "resultados": [("Desaceleración", "-8.78 m/s²")], "pdata": {"type": "a", "vi": 22.4, "a": -8.78, "t": 2.55}
    },
    {
        "num": 8, "titulo": "Camión de bomberos",
        "datos": [("Vi", "0 m/s"), ("Vf", "21 m/s (Este)"), ("t", "3.5 s")],
        "formulas": ["a = (Vf - Vi) / t"],
        "desarrollo": ["a = (21 - 0) / 3.5 = 21 / 3.5 = 6 m/s²"],
        "resultados": [("Aceleración", "6 m/s² hacia el Este")], "pdata": {"type": "a", "vi": 0, "a": 6, "t": 3.5}
    },
    {
        "num": 9, "titulo": "Automóvil en autopista",
        "datos": [("Vi", "80 km/h = 22.22 m/s"), ("Vf", "110 km/h = 30.56 m/s"), ("a", "1.8 m/s²")],
        "formulas": ["t = (Vf - Vi) / a"],
        "desarrollo": ["t = (30.56 - 22.22) / 1.8 = 8.34 / 1.8 = 4.63 s"],
        "resultados": [("Tiempo", "4.63 s")], "pdata": {"type": "a", "vi": 22.22, "a": 1.8, "t": 4.63}
    }
]

RESUMEN_DATA = [
    ["Ejercicio", "Resultado Principal"],
    ["Velocidad 1", "18 km/hr (5 m/s)"],
    ["Velocidad 2", "428.57 s (7.14 min)"],
    ["Velocidad 3", "8.67 km (8,670 m)"],
    ["Velocidad 4", "0.0133 m/s"],
    ["Velocidad 5", "1,250 m"],
    ["Velocidad 6", "14.81 m/s al Este"],
    ["Velocidad 7", "1,067 m al Norte"],
    ["Aceleración 1", "a = -40.5 m/s², t = 2.22 s"],
    ["Aceleración 2", "d = 720 m, Vf = 56 m/s"],
    ["Aceleración 3", "a = 2.5 m/s², d = 45 m"],
    ["Aceleración 4", "a = 6.8 m/s²"],
    ["Aceleración 5", "a = -19.44 m/s²"],
    ["Aceleración 6", "a = 11.17 m/s²"],
    ["Aceleración 7", "a = -8.78 m/s²"],
    ["Aceleración 8", "a = 6 m/s² al Este"],
    ["Aceleración 9", "t = 4.63 s"]
]

# ── Construcción del documento ─────────────────────────────────────────────
def build_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN)
    story = []

    # ── Encabezado ─────────────────────────────────────────────────────────
    story.append(Spacer(1, 0.5 * cm))
    story.append(Paragraph("UNIDAD 2: CINEMÁTICA", ST['titulo_doc']))
    story.append(Paragraph("Soluciones Detalladas Paso a Paso", ST['subtitulo_doc']))
    story.append(Paragraph("Docente: Silvia de la Cruz | Universidad Politécnica de Chihuahua", ST['subtitulo_doc']))
    story.append(Spacer(1, 0.4 * cm))
    story.append(hr())
    story.append(Spacer(1, 0.4 * cm))

    # ── Ejercicio 1: Cuadro de Conceptos ───────────────────────────────────
    story.append(Paragraph("Ejercicio 1: Cuadro de Conceptos", ST['seccion']))

    col_w = [3.5 * cm, 8 * cm, 6 * cm]
    data = [[Paragraph(h, ST['tabla_header']) for h in CONCEPTOS_DATA[0]]]
    for r in CONCEPTOS_DATA[1:]:
        data.append([Paragraph(c, ST['tabla_cell']) for c in r])

    t = Table(data, colWidths=col_w, repeatRows=1)
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
    story.append(t)
    story.append(Spacer(1, 0.6 * cm))
    story.append(hr())

    # ── Ejercicios de Velocidad ────────────────────────────────────────────
    story.append(Paragraph("Ejercicios de Velocidad", ST['seccion']))
    story.append(Spacer(1, 0.3 * cm))

    for p in VELOCIDAD_PROBLEMAS:
        story.append(problema_block(
            num=p["num"], titulo=p["titulo"], datos=p["datos"],
            formulas=p["formulas"], desarrollo=p["desarrollo"], resultados=p["resultados"], pdata=p.get("pdata")
        ))
        story.append(Spacer(1, 0.4 * cm))

    story.append(hr())

    # ── Ejercicios de Aceleración ──────────────────────────────────────────
    story.append(Paragraph("Ejercicios de Aceleración", ST['seccion']))
    story.append(Spacer(1, 0.3 * cm))

    for p in ACELERACION_PROBLEMAS:
        story.append(problema_block(
            num=p["num"], titulo=p["titulo"], datos=p["datos"],
            formulas=p["formulas"], desarrollo=p["desarrollo"], resultados=p["resultados"], pdata=p.get("pdata")
        ))
        story.append(Spacer(1, 0.4 * cm))

    story.append(hr())

    # ── Resumen de Resultados ──────────────────────────────────────────────
    story.append(Paragraph("Resumen de Resultados", ST['seccion']))

    col_w2 = [4 * cm, 11.5 * cm]
    rdata = [[Paragraph(h, ST['tabla_header']) for h in RESUMEN_DATA[0]]]
    for r in RESUMEN_DATA[1:]:
        rdata.append([Paragraph(r[0], ST['tabla_cell']), Paragraph(r[1], ST['cuerpo'])])

    rt = Table(rdata, colWidths=col_w2, repeatRows=1)
    rstyle = [
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('GRID', (0, 0), (-1, -1), 0.4, LINEA),
    ]
    for i in range(1, len(rdata)):
        bg = TEAL_CLR if i % 2 == 0 else BLANCO
        rstyle.append(('BACKGROUND', (0, i), (-1, i), bg))
    rt.setStyle(TableStyle(rstyle))
    story.append(rt)

    story.append(Spacer(1, 0.6 * cm))
    story.append(Paragraph(
        "Nota: Todos los cálculos utilizan el Sistema Internacional de Unidades (SI). "
        "Las desaceleraciones se representan con signo negativo para indicar que la aceleración "
        "actúa en dirección opuesta al movimiento.", ST['nota']))

    # ── Generar PDF ────────────────────────────────────────────────────────
    doc.build(story)
    print(f"✅ PDF generado exitosamente en: {os.path.abspath(path)}")

# ── Ejecución ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Ruta relativa para que funcione en Windows, Mac o Linux sin errores de permisos
    output_path = "reports/soluciones_cinematica_1D.pdf"
    build_pdf(output_path)
