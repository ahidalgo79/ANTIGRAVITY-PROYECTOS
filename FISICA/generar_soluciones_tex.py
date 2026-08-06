#!/usr/bin/env python3
"""Genera PDF profesional de soluciones de cinemática 1D vía XeLaTeX + matplotlib."""

import subprocess, io, os, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

# ── Matplotlib config ───────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'axes.unicode_minus': False,
})

FIG_W, FIG_H = 5.0, 2.0

def ax_base(ax, bg='#F1EFE8'):
    ax.set_facecolor(bg)
    ax.tick_params(labelsize=7, colors='#5F5E5A')
    for sp in ax.spines.values():
        sp.set_color('#D3D1C7')
    ax.grid(True, color='#D3D1C7', linewidth=0.4, linestyle='--', alpha=0.7)

def plot_velocidad(v, t, path):
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H))
    ax_base(ax)
    time = np.linspace(0, float(t), 100)
    dist = float(v) * time
    ax.plot(time, dist, color='#185FA5', lw=2)
    ax.set_xlabel('Tiempo (s)', fontsize=7, color='#5F5E5A')
    ax.set_ylabel('Distancia (m)', fontsize=7, color='#5F5E5A')
    ax.set_title('Gráfico Distancia vs Tiempo (MRU)', fontsize=8, color='#2C2C2A', pad=4)
    fig.tight_layout(pad=0.4)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#F1EFE8', edgecolor='none', format='pdf')
    plt.close(fig)

def plot_aceleracion(vi, a, t, path):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(FIG_W*1.2, FIG_H))
    ax_base(ax1); ax_base(ax2)
    time = np.linspace(0, float(t), 100)
    vel = float(vi) + float(a) * time
    dist = float(vi) * time + 0.5 * float(a) * time**2
    ax1.plot(time, vel, color='#993C1D', lw=2)
    ax1.set_xlabel('Tiempo (s)', fontsize=7); ax1.set_ylabel('Velocidad (m/s)', fontsize=7)
    ax1.set_title('Velocidad vs Tiempo', fontsize=8)
    ax2.plot(time, dist, color='#0F6E56', lw=2)
    ax2.set_xlabel('Tiempo (s)', fontsize=7); ax2.set_ylabel('Distancia (m)', fontsize=7)
    ax2.set_title('Distancia vs Tiempo', fontsize=8)
    fig.tight_layout(pad=0.4)
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#F1EFE8', edgecolor='none', format='pdf')
    plt.close(fig)

# ── Datos ───────────────────────────────────────────────────────────────

CONCEPTOS = [
    ["Concepto", "Definición", "Ejemplo aplicado a mecánica"],
    ["Posición", "Lugar donde se encuentra un objeto en un sistema de referencia.", "Posición del pistón dentro del cilindro."],
    ["Desplazamiento", "Cambio de posición, representado por un vector.", "El pistón se mueve 10 cm del punto muerto superior al inferior."],
    ["Rapidez", "Magnitud escalar que indica qué tan rápido se mueve un objeto.", "Una llanta gira a 30 m/s."],
    ["Velocidad", "Rapidez con dirección; magnitud vectorial.", "Un auto avanza a 60 km/h hacia el norte."],
    ["Aceleración lineal", "Cambio de velocidad en línea recta.", "El auto pasa de 0 a 100 km/h en 8 s."],
    ["Aceleración", "Cambio de velocidad en magnitud y dirección.", "Una moto acelera mientras toma una curva."],
    ["Masa", "Cantidad de materia de un cuerpo.", "Un motor tiene una masa de 120 kg."],
    ["Peso", "Fuerza con que la gravedad atrae a un cuerpo: $P = m\\cdot g$.", "El motor ejerce un peso de $\\approx 1176$ N."],
    ["Gravedad", "Constante de $9.8$ m/s$^2$ hacia el centro de la Tierra.", "Una herramienta cae del elevador con esa aceleración."],
    ["Movimiento rectilíneo", "Trayectoria en línea recta, velocidad constante o variable.", "Un auto circula en carretera recta."],
    ["MRUA", "Movimiento recto con aceleración constante.", "Un coche acelera desde reposo hasta 80 km/h en 10 s."],
]

VEL_PROBLEMAS = [
    (1, "Rapidez de un corredor",
     [("d", "3 km"), ("t", "10 min = 1/6 h = 600 s")],
     ["$v = d / t$"],
     ["a) En km/h: $v = 3 / (1/6) = 3 \\times 6 = 18$ km/h",
      "b) En m/s: $v = 3000 / 600 = 5$ m/s"],
     [("Rapidez", "18 km/h"), ("Rapidez", "5 m/s")], ("v", 5, 600)),
    (2, "Tiempo de un corredor",
     [("v", "7 m/s (Norte)"), ("d", "3 km = 3000 m")],
     ["$t = d / v$"],
     ["$t = 3000 / 7 = 428.57$ s",
      "En minutos: $428.57 / 60 = 7.14$ min"],
     [("Tiempo", "428.57 s (7.14 min)")], ("v", 7, 428.57)),
    (3, "Distancia de una chita",
     [("v", "130 km/h"), ("t", "4 min = 1/15 h")],
     ["$d = v \\times t$"],
     ["$d = 130 \\times 1/15 = 8.67$ km",
      "En metros: $8.67 \\times 1000 = 8670$ m"],
     [("Distancia", "8.67 km (8670 m)")], ("v", 36.11, 240)),
    (4, "Velocidad de un bebé gateando",
     [("d", "8 m"), ("t", "10 min = 600 s")],
     ["$v = d / t$"],
     ["$v = 8 / 600 = 0.0133$ m/s",
      "En km/h: $0.0133 \\times 3.6 = 0.048$ km/h"],
     [("Velocidad", "0.0133 m/s (0.048 km/h)")], ("v", 0.0133, 600)),
    (5, "Distancia de un ciclista",
     [("v", "10 m/s"), ("t", "125 s")],
     ["$d = v \\times t$"],
     ["$d = 10 \\times 125 = 1250$ m",
      "En km: $1250 / 1000 = 1.25$ km"],
     [("Distancia", "1250 m (1.25 km)")], ("v", 10, 125)),
    (6, "Velocidad de un motociclista",
     [("d", "8 km = 8000 m (Este)"), ("t", "9 min = 540 s")],
     ["$v = d / t$"],
     ["$v = 8000 / 540 = 14.81$ m/s"],
     [("Velocidad", "14.81 m/s hacia el Este")], ("v", 14.81, 540)),
    (7, "Desplazamiento de un automóvil",
     [("v", "80 km/h (Norte)"), ("t", "0.8 min = 48 s")],
     ["$d = v \\times t$"],
     ["$v = 80 / 3.6 = 22.22$ m/s",
      "$d = 22.22 \\times 48 = 1067$ m"],
     [("Desplazamiento", "1067 m hacia el Norte")], ("v", 22.22, 48)),
]

ACEL_PROBLEMAS = [
    (1, "Avión aterrizando en portaaviones",
     [("$V_i$", "90 m/s"), ("$V_f$", "0 m/s"), ("$d$", "100 m")],
     ["$V_f^2 = V_i^2 + 2ad$", "$V_f = V_i + at$"],
     ["a) Aceleración: $0^2 = 90^2 + 2a(100) \\to a = -8100/200 = -40.5$ m/s$^2$",
      "b) Tiempo: $0 = 90 + (-40.5)t \\to t = 90/40.5 = 2.22$ s"],
     [("Aceleración", "$-40.5$ m/s$^2$ (desaceleración)"), ("Tiempo", "2.22 s")], ("a", 90, -40.5, 2.22)),
    (2, "Tren acelerando constantemente",
     [("$V_i$", "16 m/s"), ("$a$", "2 m/s$^2$"), ("$t$", "20 s")],
     ["$d = V_i t + \\frac{1}{2} a t^2$", "$V_f = V_i + at$"],
     ["a) Distancia: $d = 16(20) + \\frac{1}{2}(2)(20)^2 = 320 + 400 = 720$ m",
      "b) Velocidad final: $V_f = 16 + 2(20) = 56$ m/s"],
     [("Distancia", "720 m"), ("Velocidad final", "56 m/s")], ("a", 16, 2, 20)),
    (3, "Lancha de motor desde el reposo",
     [("$V_i$", "0 m/s"), ("$V_f$", "15 m/s"), ("$t$", "6 s")],
     ["$a = (V_f - V_i) / t$", "$d = V_i t + \\frac{1}{2} a t^2$"],
     ["a) Aceleración: $a = (15 - 0)/6 = 2.5$ m/s$^2$",
      "b) Distancia: $d = 0 + \\frac{1}{2}(2.5)(6)^2 = 1.25 \\times 36 = 45$ m"],
     [("Aceleración", "2.5 m/s$^2$"), ("Distancia", "45 m")], ("a", 0, 2.5, 6)),
    (4, "Automóvil de carreras",
     [("$V_i$", "20 m/s"), ("$V_f$", "37 m/s"), ("$t$", "2.5 s")],
     ["$a = (V_f - V_i) / t$"],
     ["$a = (37 - 20) / 2.5 = 17 / 2.5 = 6.8$ m/s$^2$"],
     [("Aceleración", "6.8 m/s$^2$")], ("a", 20, 6.8, 2.5)),
    (5, "Motociclista frenando",
     [("$V_i$", "35 m/s"), ("$V_f$", "0 m/s"), ("$t$", "1.8 s")],
     ["$a = (V_f - V_i) / t$"],
     ["$a = (0 - 35) / 1.8 = -35 / 1.8 = -19.44$ m/s$^2$"],
     [("Desaceleración", "$-19.44$ m/s$^2$")], ("a", 35, -19.44, 1.8)),
    (6, "Automóvil de carreras (2)",
     [("$V_i$", "18.5 m/s"), ("$V_f$", "46.1 m/s"), ("$t$", "2.47 s")],
     ["$a = (V_f - V_i) / t$"],
     ["$a = (46.1 - 18.5) / 2.47 = 27.6 / 2.47 = 11.17$ m/s$^2$"],
     [("Aceleración", "11.17 m/s$^2$")], ("a", 18.5, 11.17, 2.47)),
    (7, "Motociclista frenando (2)",
     [("$V_i$", "22.4 m/s"), ("$V_f$", "0 m/s"), ("$t$", "2.55 s")],
     ["$a = (V_f - V_i) / t$"],
     ["$a = (0 - 22.4) / 2.55 = -22.4 / 2.55 = -8.78$ m/s$^2$"],
     [("Desaceleración", "$-8.78$ m/s$^2$")], ("a", 22.4, -8.78, 2.55)),
    (8, "Camión de bomberos",
     [("$V_i$", "0 m/s"), ("$V_f$", "21 m/s (Este)"), ("$t$", "3.5 s")],
     ["$a = (V_f - V_i) / t$"],
     ["$a = (21 - 0) / 3.5 = 6$ m/s$^2$"],
     [("Aceleración", "6 m/s$^2$ hacia el Este")], ("a", 0, 6, 3.5)),
    (9, "Automóvil en autopista",
     [("$V_i$", "80 km/h = 22.22 m/s"), ("$V_f$", "110 km/h = 30.56 m/s"), ("$a$", "1.8 m/s$^2$")],
     ["$t = (V_f - V_i) / a$"],
     ["$t = (30.56 - 22.22) / 1.8 = 8.34 / 1.8 = 4.63$ s"],
     [("Tiempo", "4.63 s")], ("a", 22.22, 1.8, 4.63)),
]

RESUMEN = [
    ["Ejercicio", "Resultado Principal"],
    ["Velocidad 1", "18 km/h (5 m/s)"],
    ["Velocidad 2", "428.57 s (7.14 min)"],
    ["Velocidad 3", "8.67 km (8670 m)"],
    ["Velocidad 4", "0.0133 m/s"],
    ["Velocidad 5", "1250 m"],
    ["Velocidad 6", "14.81 m/s al Este"],
    ["Velocidad 7", "1067 m al Norte"],
    ["Aceleración 1", "$a = -40.5$ m/s$^2$, $t = 2.22$ s"],
    ["Aceleración 2", "$d = 720$ m, $V_f = 56$ m/s"],
    ["Aceleración 3", "$a = 2.5$ m/s$^2$, $d = 45$ m"],
    ["Aceleración 4", "$a = 6.8$ m/s$^2$"],
    ["Aceleración 5", "$a = -19.44$ m/s$^2$"],
    ["Aceleración 6", "$a = 11.17$ m/s$^2$"],
    ["Aceleración 7", "$a = -8.78$ m/s$^2$"],
    ["Aceleración 8", "$a = 6$ m/s$^2$ al Este"],
    ["Aceleración 9", "$t = 4.63$ s"],
]

TEX_PREAMBLE = r"""\documentclass[10pt,a4paper]{article}
\usepackage{fontspec}
\usepackage[margin=2cm]{geometry}
\usepackage{xcolor}
\usepackage{array,booktabs,tabularx,colortbl}
\usepackage{amsmath,amssymb}
\usepackage{enumitem}
\usepackage{fancyhdr}
\usepackage{titlesec}
\usepackage[most]{tcolorbox}
\usepackage{parskip}
\usepackage{graphicx}
\usepackage{hyperref}

\definecolor{azul}{HTML}{185FA5}
\definecolor{azulclr}{HTML}{E6F1FB}
\definecolor{teal}{HTML}{0F6E56}
\definecolor{tealclr}{HTML}{E1F5EE}
\definecolor{gris}{HTML}{5F5E5A}
\definecolor{grisclr}{HTML}{F1EFE8}
\definecolor{negro}{HTML}{2C2C2A}
\definecolor{coral}{HTML}{993C1D}
\definecolor{alerta}{HTML}{D32F2F}
\definecolor{alertaclr}{HTML}{FFEBEE}

\setmainfont{Arial}
\setsansfont{Arial}
\renewcommand{\familydefault}{\sfdefault}

\titleformat{\section}{\bfseries\Large\color{azul}}{}{0em}{}[\vspace{-2pt}]

\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\color{gris}\small\textbf{Unidad 2: Cinemática — Soluciones Detalladas}}
\fancyfoot[C]{\color{gris}\thepage}
\renewcommand{\headrule}{\color{azul}\rule{\textwidth}{0.4pt}}

\newcolumntype{L}{>{\raggedright\arraybackslash}X}
\newcolumntype{C}{>{\centering\arraybackslash}X}

\newcommand{\resbox}[2]{%
  \begin{tcolorbox}[colback=tealclr, colframe=teal, arc=4pt, boxrule=0.5pt,
    left=10pt, right=10pt, top=6pt, bottom=6pt, width=\textwidth]
    \textbf{\textcolor{teal}{#1:}} \textcolor{teal}{#2}
  \end{tcolorbox}}
"""


def build_tex(tex_path, img_dir):
    # ── Generate images ────────────────────────────────────────────
    img_dir.mkdir(parents=True, exist_ok=True)

    for typ, *args in [
        *[("v", n, v, t) for n, (_, _, _, _, _, _, p) in enumerate(VEL_PROBLEMAS) for (typ, v, t) in [p] if typ == "v"],
    ]:
        pass  # handled inline below

    for i, (num, tit, dat, frm, des, res, pdata) in enumerate(VEL_PROBLEMAS):
        if pdata[0] == "v":
            plot_velocidad(pdata[1], pdata[2], img_dir / f"vel_{i}.pdf")

        for i, (num, tit, dat, frm, des, res, pdata) in enumerate(ACEL_PROBLEMAS):
            if pdata[0] == "a":
                plot_aceleracion(pdata[1], pdata[2], pdata[3], img_dir / f"acel_{i}.pdf")

    # ── Build LaTeX ────────────────────────────────────────────────
    lines = [TEX_PREAMBLE]
    lines.append(r"\begin{document}")
    lines.append(r"\thispagestyle{fancy}")
    lines.append(r"\begin{center}")
    lines.append(r"  {\Huge\bfseries\color{azul} UNIDAD 2: CINEMÁTICA}\\[4pt]")
    lines.append(r"  {\large\color{gris} Soluciones Detalladas Paso a Paso}\\[4pt]")
    lines.append(r"  {\color{gris} Docente: Silvia de la Cruz $|$ Universidad Politécnica de Chihuahua}")
    lines.append(r"\end{center}")
    lines.append(r"\vspace{6pt}\hrule height 0.5pt\vspace{10pt}")

    # ── Conceptos ──────────────────────────────────────────────────
    lines.append(r"\section{Ejercicio 1: Cuadro de Conceptos}")
    lines.append(r"\begin{tabularx}{\textwidth}{LLL}")
    lines.append(r"  \toprule\rowcolor{azul}")
    cols = " & ".join(r"\textbf{\textcolor{white}{" + c + "}}" for c in CONCEPTOS[0])
    lines.append(f"  {cols} \\\\")
    lines.append(r"  \midrule")
    for i, row in enumerate(CONCEPTOS[1:]):
        if i % 2 == 1:
            lines.append(r"  \rowcolor{azulclr}")
        lines.append("  " + " & ".join(row) + " \\\\")
    lines.append(r"  \bottomrule")
    lines.append(r"\end{tabularx}")
    lines.append(r"\vspace{8pt}\hrule height 0.5pt\vspace{10pt}")

    # ── Problemas de velocidad ─────────────────────────────────────
    lines.append(r"\section{Ejercicios de Velocidad}")
    for i, (num, tit, dat, frm, des, res, pdata) in enumerate(VEL_PROBLEMAS):
        lines.append(r"\begin{tcolorbox}[colback=azul, colframe=azul, arc=4pt, boxrule=0.5pt,")
        lines.append(r"  left=8pt, right=8pt, top=6pt, bottom=6pt, width=\textwidth]")
        lines.append(f"  \\textbf{{\\color{{white}} Problema {num}: {tit}}}")
        lines.append(r"\end{tcolorbox}")
        # Datos
        items = "  $|$  ".join(f"${{{k}}}$: {v}" for k, v in dat)
        lines.append(r"\begin{tcolorbox}[colback=grisclr, colframe=gris, arc=4pt, boxrule=0.3pt,")
        lines.append(r"  left=8pt, right=8pt, top=4pt, bottom=4pt, width=\textwidth]")
        lines.append(f"  \\small\\textcolor{{gris}}{{{items}}}")
        lines.append(r"\end{tcolorbox}")
        # Fórmulas
        for f in frm:
            lines.append(f"\\hspace{{12pt}}{f}")
        # Desarrollo
        lines.append(r"\vspace{4pt}\textbf{\textcolor{teal}{Desarrollo:}}")
        for d in des:
            lines.append(f"\\hspace{{12pt}}{d}")
        # Resultados
        lines.append(r"\vspace{4pt}")
        for k, v in res:
            lines.append(f"\\resbox{{{k}}}{{{v}}}")
        # Gráfica
        if pdata[0] == "v":
            lines.append(r"\begin{center}")
            lines.append("  \\includegraphics[width=12cm]{" + str(img_dir.name) + f"/vel_{i}.pdf" + "}")
            lines.append(r"\end{center}")
        lines.append(r"\vspace{6pt}")

    lines.append(r"\hrule height 0.5pt\vspace{10pt}")

    # ── Problemas de aceleración ───────────────────────────────────
    lines.append(r"\section{Ejercicios de Aceleración}")
    for i, (num, tit, dat, frm, des, res, pdata) in enumerate(ACEL_PROBLEMAS):
        lines.append(r"\begin{tcolorbox}[colback=coral, colframe=coral, arc=4pt, boxrule=0.5pt,")
        lines.append(r"  left=8pt, right=8pt, top=6pt, bottom=6pt, width=\textwidth]")
        lines.append(f"  \\textbf{{\\color{{white}} Problema {num}: {tit}}}")
        lines.append(r"\end{tcolorbox}")
        items = "  $|$  ".join(f"${k}$: {v}" for k, v in dat)
        lines.append(r"\begin{tcolorbox}[colback=grisclr, colframe=gris, arc=4pt, boxrule=0.3pt,")
        lines.append(r"  left=8pt, right=8pt, top=4pt, bottom=4pt, width=\textwidth]")
        lines.append(f"  \\small\\textcolor{{gris}}{{{items}}}")
        lines.append(r"\end{tcolorbox}")
        for f in frm:
            lines.append(f"\\hspace{{12pt}}{f}")
        lines.append(r"\vspace{4pt}\textbf{\textcolor{teal}{Desarrollo:}}")
        for d in des:
            lines.append(f"\\hspace{{12pt}}{d}")
        lines.append(r"\vspace{4pt}")
        for k, v in res:
            lines.append(f"\\resbox{{{k}}}{{{v}}}")
        if pdata[0] == "a":
            lines.append(r"\begin{center}")
            lines.append("  \\includegraphics[width=14cm]{" + str(img_dir.name) + f"/acel_{i}.pdf" + "}")
            lines.append(r"\end{center}")
        lines.append(r"\vspace{6pt}")

    lines.append(r"\hrule height 0.5pt\vspace{10pt}")

    # ── Resumen ────────────────────────────────────────────────────
    lines.append(r"\section{Resumen de Resultados}")
    lines.append(r"\begin{tabularx}{\textwidth}{LC}")
    lines.append(r"  \toprule\rowcolor{teal}")
    cols = " & ".join(r"\textbf{\textcolor{white}{" + c + "}}" for c in RESUMEN[0])
    lines.append(f"  {cols} \\\\")
    lines.append(r"  \midrule")
    for i, row in enumerate(RESUMEN[1:]):
        if i % 2 == 1:
            lines.append(r"  \rowcolor{tealclr}")
        lines.append("  " + " & ".join(row) + " \\\\")
    lines.append(r"  \bottomrule")
    lines.append(r"\end{tabularx}")

    lines.append(r"\vspace{8pt}")
    lines.append(r"\begin{tcolorbox}[colback=grisclr, colframe=gris, arc=4pt, boxrule=0.3pt,")
    lines.append(r"  left=8pt, right=8pt, top=4pt, bottom=4pt, width=\textwidth]")
    lines.append(r"  \small\textcolor{gris}{Nota: Todos los cálculos utilizan el Sistema Internacional de Unidades (SI).}")
    lines.append(r"  \small\textcolor{gris}{Las desaceleraciones se representan con signo negativo.}")
    lines.append(r"\end{tcolorbox}")
    lines.append(r"\end{document}")

    tex_path.write_text("\n".join(lines), encoding="utf-8")
    return tex_path


def main():
    base = Path(__file__).parent
    tex_path = base / "soluciones_cinematica_1D.tex"
    img_dir = base / "img_soluciones"
    build_tex(tex_path, img_dir)
    print(f"📄 .tex generado: {tex_path}")

    result = subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-output-directory", str(base), str(tex_path)],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        log = (tex_path.with_suffix(".log"))
        if log.exists():
            print(log.read_text(encoding="utf-8")[-1500:])
        sys.exit(1)
    print(f"✅ PDF: {(base / 'soluciones_cinematica_1D.pdf').resolve()}")


if __name__ == "__main__":
    main()
