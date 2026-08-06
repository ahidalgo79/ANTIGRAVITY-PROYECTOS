import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import io, os

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, Image, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

W, H = A4
MARGIN = 2*cm

# ── Color palette ──────────────────────────────────────────────────────────
AZUL      = colors.HexColor('#185FA5')
AZUL_CLR  = colors.HexColor('#E6F1FB')
TEAL      = colors.HexColor('#0F6E56')
TEAL_CLR  = colors.HexColor('#E1F5EE')
GRIS      = colors.HexColor('#5F5E5A')
GRIS_CLR  = colors.HexColor('#F1EFE8')
CORAL     = colors.HexColor('#993C1D')
CORAL_CLR = colors.HexColor('#FAECE7')
AMBER     = colors.HexColor('#BA7517')
AMBER_CLR = colors.HexColor('#FAEEDA')
NEGRO     = colors.HexColor('#2C2C2A')
BLANCO    = colors.white
LINEA     = colors.HexColor('#D3D1C7')

# ── Styles ─────────────────────────────────────────────────────────────────
pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))

def make_styles():
    s = {}
    base = dict(fontName='DejaVuSans', fontSize=10, leading=14,
                textColor=NEGRO, spaceAfter=4)
    s['titulo_doc'] = ParagraphStyle('titulo_doc', **{**base,
        'fontName':'DejaVuSans-Bold', 'fontSize':22, 'leading':26,
        'textColor':AZUL, 'alignment':TA_CENTER, 'spaceAfter':6})
    s['subtitulo_doc'] = ParagraphStyle('subtitulo_doc', **{**base,
        'fontSize':11, 'textColor':GRIS, 'alignment':TA_CENTER, 'spaceAfter':4})
    s['prob_titulo'] = ParagraphStyle('prob_titulo', **{**base,
        'fontName':'DejaVuSans-Bold', 'fontSize':13, 'leading':16,
        'textColor':BLANCO, 'spaceAfter':0})
    s['prob_sub'] = ParagraphStyle('prob_sub', **{**base,
        'fontSize':9, 'textColor':GRIS_CLR, 'spaceAfter':0})
    s['paso_titulo'] = ParagraphStyle('paso_titulo', **{**base,
        'fontName':'DejaVuSans-Bold', 'fontSize':9, 'textColor':TEAL,
        'spaceAfter':2, 'spaceBefore':6})
    s['cuerpo'] = ParagraphStyle('cuerpo', **{**base,
        'fontSize':10, 'leading':15, 'spaceAfter':4})
    s['formula'] = ParagraphStyle('formula', **{**base,
        'fontName':'DejaVuSans', 'fontSize':10, 'leading':14,
        'textColor':AZUL, 'leftIndent':12, 'spaceAfter':3})
    s['resultado'] = ParagraphStyle('resultado', **{**base,
        'fontName':'DejaVuSans-Bold', 'fontSize':11, 'textColor':TEAL,
        'leftIndent':12, 'spaceAfter':4})
    s['nota'] = ParagraphStyle('nota', **{**base,
        'fontSize':9, 'textColor':GRIS, 'leftIndent':12, 'spaceAfter':4})
    s['tabla_header'] = ParagraphStyle('tabla_header', **{**base,
        'fontName':'DejaVuSans-Bold', 'fontSize':9, 'textColor':BLANCO,
        'alignment':TA_CENTER})
    s['tabla_cell'] = ParagraphStyle('tabla_cell', **{**base,
        'fontSize':9, 'alignment':TA_CENTER})
    s['seccion'] = ParagraphStyle('seccion', **{**base,
        'fontName':'DejaVuSans-Bold', 'fontSize':11, 'textColor':AZUL,
        'spaceBefore':10, 'spaceAfter':4})
    return s

ST = make_styles()

# ── Matplotlib helpers ─────────────────────────────────────────────────────
FIG_W, FIG_H = 5.5, 2.2

def fig_to_rl(fig, width_cm=14):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight',
                facecolor='#F1EFE8', edgecolor='none')
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

# Problema 1 – lanzamiento horizontal
def fig_p1():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax_base(ax)
    t = np.linspace(0,1,200)
    x = 50*t
    y = 122.5 - 0.5*9.8*(5*t)**2
    ax.plot(x, y, color='#185FA5', lw=2, label='Trayectoria')
    ax.axhline(0, color='#3B6D11', lw=1.5, linestyle='-')
    ax.fill_between([0,50], 0, -5, color='#C0DD97', alpha=0.5)
    ax.annotate('', xy=(50,0), xytext=(0,0),
                arrowprops=dict(arrowstyle='->', color='#BA7517', lw=1.5))
    ax.annotate('', xy=(0,0), xytext=(0,122.5),
                arrowprops=dict(arrowstyle='->', color='#0F6E56', lw=1.5))
    ax.text(25, -8, 'x = 50 m', ha='center', fontsize=7, color='#BA7517', fontweight='bold')
    ax.text(-6, 61, 'h=122.5 m', ha='right', fontsize=7, color='#0F6E56', fontweight='bold')
    ax.scatter([0],[122.5], color='#185FA5', s=30, zorder=5)
    ax.scatter([50],[0], color='#D85A30', s=30, zorder=5)
    ax.text(1, 118, 'v0=10 m/s →', fontsize=7, color='#185FA5')
    ax.set_xlabel('Distancia horizontal (m)', fontsize=7, color='#5F5E5A')
    ax.set_ylabel('Altura (m)', fontsize=7, color='#5F5E5A')
    ax.set_title('Lanzamiento horizontal', fontsize=8, color='#2C2C2A', pad=4)
    ax.set_ylim(-12, 135)
    fig.tight_layout(pad=0.4)
    return fig

# Problema 2 – tiro parabólico bala
def fig_p2():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax_base(ax)
    g=9.8; v0=400; th=np.radians(35)
    v0x=v0*np.cos(th); v0y=v0*np.sin(th)
    T=2*v0y/g
    t=np.linspace(0,T,300)
    x=v0x*t; y=v0y*t-0.5*g*t**2
    ax.plot(x/1000, y/1000, color='#185FA5', lw=2)
    ax.axhline(0, color='#3B6D11', lw=1.2)
    Hmax=v0y**2/(2*g)
    xH=v0x*(v0y/g)
    ax.annotate('', xy=(xH/1000, Hmax/1000), xytext=(xH/1000,0),
                arrowprops=dict(arrowstyle='<->', color='#0F6E56', lw=1.2))
    ax.text(xH/1000+0.15, Hmax/2000, 'H=2685 m', fontsize=6.5, color='#0F6E56')
    ax.annotate('', xy=(x[-1]/1000,0), xytext=(0,0),
                arrowprops=dict(arrowstyle='<->', color='#BA7517', lw=1.2))
    ax.text(x[-1]/2000, -0.1, 'R=15.34 km', ha='center', fontsize=6.5, color='#BA7517')
    arc=mpatches.Arc((0,0),1.2,0.9,angle=0,theta1=0,theta2=35,color='#D85A30',lw=1.2)
    ax.add_patch(arc)
    ax.text(0.65,0.12,'35°',fontsize=7,color='#D85A30')
    ax.set_xlabel('Distancia (km)', fontsize=7, color='#5F5E5A')
    ax.set_ylabel('Altura (km)', fontsize=7, color='#5F5E5A')
    ax.set_title('Tiro parabólico — bala v0=400 m/s, θ=35°', fontsize=8, color='#2C2C2A', pad=4)
    ax.set_ylim(-0.35, 3.1)
    fig.tight_layout(pad=0.4)
    return fig

# Problema 3 – dos ángulos
def fig_p3():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax_base(ax)
    g=9.8; v0=350; R=4000
    for ang, col, lbl in [(9.33,'#185FA5','θ=9.33° (rasante)'),
                          (80.67,'#993C1D','θ=80.67° (alta)')]:
        th=np.radians(ang)
        v0x=v0*np.cos(th); v0y=v0*np.sin(th)
        T=2*v0y/g
        t=np.linspace(0,T,300)
        x=v0x*t; y=v0y*t-0.5*g*t**2
        ax.plot(x, y, color=col, lw=2, label=lbl)
    ax.axhline(0,color='#3B6D11',lw=1.2)
    ax.axvline(R,color='#BA7517',lw=1,linestyle='--')
    ax.text(R+30,200,'R=4000 m',fontsize=6.5,color='#BA7517',rotation=90)
    ax.set_xlabel('Distancia (m)', fontsize=7, color='#5F5E5A')
    ax.set_ylabel('Altura (m)', fontsize=7, color='#5F5E5A')
    ax.set_title('Dos ángulos para el mismo alcance', fontsize=8, color='#2C2C2A', pad=4)
    ax.legend(fontsize=6.5, framealpha=0.5, loc='upper right')
    fig.tight_layout(pad=0.4)
    return fig

# Problema 4 – avión
def fig_p4():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax_base(ax)
    g=9.8; v=222.22; h=500
    t_total=np.sqrt(2*h/g)
    t=np.linspace(0,t_total,200)
    x=v*t; y=h-0.5*g*t**2
    ax.plot(x, y, color='#185FA5', lw=2, label='Proyectil')
    ax.axhline(0, color='#3B6D11', lw=1.4)
    ax.fill_between([0, x[-1]], 0, -20, color='#C0DD97', alpha=0.4)
    ax.annotate('', xy=(0,0), xytext=(0,h),
                arrowprops=dict(arrowstyle='<->', color='#0F6E56', lw=1.2))
    ax.text(-70, h/2, 'h=500 m', fontsize=7, color='#0F6E56', ha='right')
    ax.annotate('', xy=(x[-1],0), xytext=(0,0),
                arrowprops=dict(arrowstyle='<->', color='#BA7517', lw=1.2))
    ax.text(x[-1]/2, -40, 'x=2244 m', ha='center', fontsize=7, color='#BA7517')
    ax.scatter([0],[h],color='#D85A30',s=40,zorder=5,marker='^',label='Lanzamiento')
    ax.text(30, h+20, 'v=800 km/h →', fontsize=7, color='#185FA5')
    ax.set_xlabel('Distancia (m)', fontsize=7, color='#5F5E5A')
    ax.set_ylabel('Altura (m)', fontsize=7, color='#5F5E5A')
    ax.set_title('Lanzamiento horizontal desde avión', fontsize=8, color='#2C2C2A', pad=4)
    ax.set_ylim(-60, 600)
    fig.tight_layout(pad=0.4)
    return fig

# Problema 5 – balón
def fig_p5():
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax_base(ax)
    g=9.8; v0=22; th=np.radians(40)
    v0x=v0*np.cos(th); v0y=v0*np.sin(th)
    T=2*v0y/g
    t=np.linspace(0,T,200)
    x=v0x*t; y=v0y*t-0.5*g*t**2
    ax.plot(x, y, color='#185FA5', lw=2)
    ax.axhline(0, color='#3B6D11', lw=1.4)
    ax.fill_between([0,x[-1]], 0, -1, color='#C0DD97', alpha=0.5)
    Hmax=v0y**2/(2*g); xH=v0x*(v0y/g)
    ax.annotate('', xy=(xH, Hmax), xytext=(xH,0),
                arrowprops=dict(arrowstyle='<->', color='#0F6E56', lw=1.2))
    ax.text(xH+0.5, Hmax/2, 'H=10.2 m', fontsize=7, color='#0F6E56')
    ax.annotate('', xy=(x[-1],0), xytext=(0,0),
                arrowprops=dict(arrowstyle='<->', color='#BA7517', lw=1.2))
    ax.text(x[-1]/2, -1.5, 'R=48.63 m', ha='center', fontsize=7, color='#BA7517')
    arc=mpatches.Arc((0,0),6,4,angle=0,theta1=0,theta2=40,color='#D85A30',lw=1.2)
    ax.add_patch(arc)
    ax.text(3.5,1.2,'40°',fontsize=7,color='#D85A30')
    ax.set_xlabel('Distancia (m)', fontsize=7, color='#5F5E5A')
    ax.set_ylabel('Altura (m)', fontsize=7, color='#5F5E5A')
    ax.set_title('Tiro parabólico — balón v0=22 m/s, θ=40°', fontsize=8, color='#2C2C2A', pad=4)
    ax.set_ylim(-2.5, 13)
    fig.tight_layout(pad=0.4)
    return fig

# ── Flowable helpers ───────────────────────────────────────────────────────

def header_block(num, titulo, subtitulo, color_fondo):
    data = [[
        Paragraph(f"Problema {num}", ST['prob_titulo']),
        Paragraph(titulo, ST['prob_titulo']),
    ]]
    t = Table(data, colWidths=[2.5*cm, 13*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color_fondo),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]))
    return t

def dato_row(items):
    cells = [Paragraph(f"<b>{k}:</b> {v}", ST['nota']) for k,v in items]
    widths = [(W - 2*MARGIN) / len(cells)] * len(cells)
    t = Table([cells], colWidths=widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GRIS_CLR),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('GRID', (0,0), (-1,-1), 0.3, LINEA),
    ]))
    return t

def res_box(label, value, color=TEAL_CLR, text_color=TEAL):
    data = [[Paragraph(f"✔  <b>{label}:</b>  {value}", ParagraphStyle(
        'rb', fontName='DejaVuSans-Bold', fontSize=11, textColor=text_color,
        leading=14))]]
    t = Table(data, colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]))
    return t

def paso(titulo, *contenido_items):
    elems = [Paragraph(titulo.upper(), ST['paso_titulo'])]
    for item in contenido_items:
        elems.append(item)
    return elems

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=LINEA, spaceAfter=6, spaceBefore=6)

# ── Tabla de resumen ───────────────────────────────────────────────────────
def tabla_resumen():
    header = ['Problema', 'Incógnita', 'Resultado']
    rows = [
        ['1a', 'Altura de la ventana', '122.5 m'],
        ['1b', 'Distancia horizontal', '50 m'],
        ['2a', 'Tiempo en el aire', '46.82 s'],
        ['2b', 'Altura máxima', '2 685.6 m'],
        ['2c', 'Alcance horizontal', '15 342 m  (15.34 km)'],
        ['3',  'Ángulo de elevación', '9.33°  ó  80.67°'],
        ['4a', 'Tiempo de caída', '10.10 s'],
        ['4b', 'Distancia horizontal', '2 244 m  (2.24 km)'],
        ['5a', 'Altura máxima', '10.20 m'],
        ['5b', 'Alcance horizontal', '48.63 m'],
    ]
    col_w = [1.8*cm, 8*cm, 5.7*cm]
    data  = [[Paragraph(h, ST['tabla_header']) for h in header]]
    for r in rows:
        data.append([Paragraph(c, ST['tabla_cell']) for c in r])
    t = Table(data, colWidths=col_w, repeatRows=1)
    style = [
        ('BACKGROUND', (0,0), (-1,0), AZUL),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.4, LINEA),
    ]
    for i in range(1, len(data)):
        bg = AZUL_CLR if i % 2 == 0 else BLANCO
        style.append(('BACKGROUND', (0,i), (-1,i), bg))
    t.setStyle(TableStyle(style))
    return t

# ── Build document ─────────────────────────────────────────────────────────
def build_pdf(path):
    doc = SimpleDocTemplate(path, pagesize=A4,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=MARGIN)
    story = []

    # ── Portada / encabezado ──────────────────────────────────────────────
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Cinemática en Dos Dimensiones", ST['titulo_doc']))
    story.append(Paragraph("Apuntes — Movimiento de Proyectiles", ST['subtitulo_doc']))
    story.append(Paragraph("g = 9.8 m/s²  |  Sistema Internacional (SI)", ST['subtitulo_doc']))
    story.append(Spacer(1, 0.2*cm))
    story.append(hr())
    story.append(Spacer(1, 0.3*cm))

    # ════════════════════════════════════════════════════════════════════════
    # PROBLEMA 1
    # ════════════════════════════════════════════════════════════════════════
    story.append(KeepTogether([
        header_block(1, "Lanzamiento horizontal desde una ventana", "", AZUL),
        Spacer(1, 4),
        dato_row([('v₀','10 m/s (horizontal)'),('t','5 s'),('v₀y','0 m/s')]),
        Spacer(1, 6),
    ]))

    story.append(fig_to_rl(fig_p1()))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Concepto clave", ST['paso_titulo']))
    story.append(Paragraph(
        "El movimiento se separa en <b>dos ejes independientes</b>: horizontal (MRU, sin aceleración) "
        "y vertical (caída libre desde reposo, v₀y = 0).", ST['cuerpo']))

    story.extend(paso("a) Altura de la ventana",
        Paragraph("En el eje vertical, la única aceleración es la gravedad:", ST['cuerpo']),
        Paragraph("h = ½ g t²  =  ½ × 9.8 × 5²  =  ½ × 9.8 × 25", ST['formula']),
        res_box("Altura de la ventana", "h = 122.5 m"),
        Spacer(1,4),
    ))
    story.extend(paso("b) Distancia horizontal",
        Paragraph("En el eje horizontal no hay aceleración (MRU):", ST['cuerpo']),
        Paragraph("x = v₀ · t  =  10 × 5", ST['formula']),
        res_box("Distancia horizontal", "x = 50 m"),
        Spacer(1,4),
    ))
    story.append(hr())

    # ════════════════════════════════════════════════════════════════════════
    # PROBLEMA 2
    # ════════════════════════════════════════════════════════════════════════
    story.append(KeepTogether([
        header_block(2, "Tiro parabólico — bala disparada a 35°", "", CORAL),
        Spacer(1, 4),
        dato_row([('v₀','400 m/s'),('θ','35°')]),
        Spacer(1, 6),
    ]))

    story.append(fig_to_rl(fig_p2()))
    story.append(Spacer(1, 6))

    story.extend(paso("Componentes de la velocidad inicial",
        Paragraph("v₀x = v₀ cos θ  =  400 × cos 35°  ≈  327.66 m/s", ST['formula']),
        Paragraph("v₀y = v₀ sin θ  =  400 × sin 35°  ≈  229.43 m/s", ST['formula']),
        Spacer(1,4),
    ))
    story.extend(paso("a) Tiempo total en el aire",
        Paragraph("En el punto más alto v_y = 0. El vuelo es simétrico, por lo que:", ST['cuerpo']),
        Paragraph("t_vuelo  =  2 v₀y / g  =  2 × 229.43 / 9.8", ST['formula']),
        res_box("Tiempo en el aire", "t ≈ 46.82 s"),
        Spacer(1,4),
    ))
    story.extend(paso("b) Altura máxima",
        Paragraph("H = v₀y² / (2g)  =  229.43² / (2 × 9.8)  =  52 637 / 19.6", ST['formula']),
        res_box("Altura máxima", "H ≈ 2 685.6 m  (≈ 2.69 km)"),
        Spacer(1,4),
    ))
    story.extend(paso("c) Alcance horizontal",
        Paragraph("Se puede usar la fórmula directa del alcance:", ST['cuerpo']),
        Paragraph("R = v₀² sin(2θ) / g  =  400² × sin 70° / 9.8  =  160 000 × 0.9397 / 9.8", ST['formula']),
        res_box("Alcance horizontal", "R ≈ 15 342 m  (15.34 km)"),
        Spacer(1,4),
    ))
    story.append(hr())

    # ════════════════════════════════════════════════════════════════════════
    # PROBLEMA 3
    # ════════════════════════════════════════════════════════════════════════
    story.append(KeepTogether([
        header_block(3, "Ángulo de elevación para alcanzar 4 000 m", "", AMBER),
        Spacer(1, 4),
        dato_row([('v₀','350 m/s'),('R','4 000 m')]),
        Spacer(1, 6),
    ]))

    story.append(fig_to_rl(fig_p3()))
    story.append(Spacer(1, 6))

    story.extend(paso("Despejar el ángulo de la fórmula de alcance",
        Paragraph("Partimos de  R = v₀² sin(2θ) / g  y despejamos:", ST['cuerpo']),
        Paragraph("sin(2θ)  =  R·g / v₀²  =  4000 × 9.8 / 350²  =  39 200 / 122 500  ≈  0.32", ST['formula']),
        Spacer(1,4),
    ))
    story.extend(paso("Dos soluciones del arcoseno",
        Paragraph("La función seno tiene dos valores en [0°, 180°] que dan el mismo resultado:", ST['cuerpo']),
        Paragraph("2θ₁ = arcsin(0.32) ≈ 18.66°   →   θ₁ ≈ 9.33°", ST['formula']),
        Paragraph("2θ₂ = 180° − 18.66° = 161.34°  →  θ₂ ≈ 80.67°", ST['formula']),
        res_box("Ángulos válidos", "θ₁ = 9.33°  (trayectoria rasante)   ·   θ₂ = 80.67°  (parábola alta)"),
        Paragraph(
            "Ambos ángulos producen exactamente el mismo alcance. En la práctica se elige el menor, "
            "salvo que se especifique lo contrario.", ST['nota']),
        Spacer(1,4),
    ))
    story.append(hr())

    # ════════════════════════════════════════════════════════════════════════
    # PROBLEMA 4
    # ════════════════════════════════════════════════════════════════════════
    story.append(KeepTogether([
        header_block(4, "Proyectil lanzado desde un avión a 800 km/h", "", GRIS),
        Spacer(1, 4),
        dato_row([('v','800 km/h → 222.22 m/s'),('h','500 m')]),
        Spacer(1, 6),
    ]))

    story.append(fig_to_rl(fig_p4()))
    story.append(Spacer(1, 6))

    story.extend(paso("Conversión de unidades — paso obligatorio",
        Paragraph(
            "Siempre trabaja en SI. Convertir km/h a m/s multiplicando por 1000/3600:", ST['cuerpo']),
        Paragraph("v  =  800 × 1000 / 3600  =  222.22 m/s", ST['formula']),
        Spacer(1,4),
    ))
    story.extend(paso("a) Tiempo de caída",
        Paragraph("El proyectil se lanza horizontalmente (v₀y = 0), por lo que:", ST['cuerpo']),
        Paragraph("h = ½ g t²   →   t = √(2h / g)  =  √(2 × 500 / 9.8)  =  √102.04", ST['formula']),
        res_box("Tiempo de caída", "t ≈ 10.10 s"),
        Spacer(1,4),
    ))
    story.extend(paso("b) Distancia horizontal",
        Paragraph("x = v · t  =  222.22 × 10.10", ST['formula']),
        res_box("Distancia horizontal", "x ≈ 2 244 m  (2.24 km)"),
        Spacer(1,4),
    ))
    story.append(hr())

    # ════════════════════════════════════════════════════════════════════════
    # PROBLEMA 5
    # ════════════════════════════════════════════════════════════════════════
    story.append(KeepTogether([
        header_block(5, "Tiro parabólico — balón de fútbol a 40°", "", TEAL),
        Spacer(1, 4),
        dato_row([('v₀','22 m/s'),('θ','40°')]),
        Spacer(1, 6),
    ]))

    story.append(fig_to_rl(fig_p5()))
    story.append(Spacer(1, 6))

    story.extend(paso("Componentes de la velocidad inicial",
        Paragraph("v₀x = 22 cos 40°  ≈  16.85 m/s", ST['formula']),
        Paragraph("v₀y = 22 sin 40°  ≈  14.14 m/s", ST['formula']),
        Spacer(1,4),
    ))
    story.extend(paso("a) Altura máxima",
        Paragraph("H = v₀y² / (2g)  =  14.14² / (2 × 9.8)  =  199.94 / 19.6", ST['formula']),
        res_box("Altura máxima", "H ≈ 10.20 m"),
        Spacer(1,4),
    ))
    story.extend(paso("b) Alcance horizontal",
        Paragraph("R = v₀² sin(2θ) / g  =  22² × sin 80° / 9.8  =  484 × 0.9848 / 9.8", ST['formula']),
        res_box("Alcance horizontal", "R ≈ 48.63 m"),
        Paragraph(
            "Nota: el alcance máximo se logra con θ = 45°. A 40° estamos muy cerca del óptimo.", ST['nota']),
        Spacer(1,4),
    ))
    story.append(hr())

    # ════════════════════════════════════════════════════════════════════════
    # RESUMEN
    # ════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("Resumen de resultados", ST['seccion']))
    story.append(tabla_resumen())
    story.append(Spacer(1, 0.6*cm))

    # Fórmulas de referencia
    story.append(Paragraph("Fórmulas de referencia", ST['seccion']))
    formulas = [
        ["Magnitud", "Fórmula"],
        ["Tiempo de vuelo",     "t = 2 v₀y / g  =  2 v₀ sinθ / g"],
        ["Altura máxima",       "H = v₀y² / (2g)  =  v₀² sin²θ / (2g)"],
        ["Alcance horizontal",  "R = v₀² sin(2θ) / g"],
        ["Lanzamiento horiz.",  "h = ½ g t²,   x = v₀ t"],
        ["Conversión km/h→m/s", "v(m/s) = v(km/h) × 1000/3600"],
    ]
    col_w2 = [4.5*cm, 11*cm]
    fdata = [[Paragraph(c, ST['tabla_header']) for c in formulas[0]]]
    for r in formulas[1:]:
        fdata.append([Paragraph(r[0], ST['nota']),
                      Paragraph(r[1], ParagraphStyle('fm', fontName='DejaVuSans',
                                fontSize=9, textColor=AZUL, leading=13))])
    ft = Table(fdata, colWidths=col_w2, repeatRows=1)
    ft.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), AZUL),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.4, LINEA),
        ('BACKGROUND', (0,1), (-1,-1), AZUL_CLR),
    ]))
    story.append(ft)
    story.append(Spacer(1, 0.4*cm))
    story.append(Paragraph(
        "Todos los cálculos utilizan g = 9.8 m/s². Las unidades deben ser consistentes (SI) antes de aplicar cualquier fórmula.",
        ST['nota']))

    doc.build(story)
    print("PDF generado:", path)

# ── Run ────────────────────────────────────────────────────────────────────
out = "reports/cinematica_2D_apuntes.pdf"
os.makedirs(os.path.dirname(out), exist_ok=True)
build_pdf(out)
