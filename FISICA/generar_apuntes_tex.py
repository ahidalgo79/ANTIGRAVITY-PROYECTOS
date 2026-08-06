#!/usr/bin/env python3
"""Genera PDF profesional de apuntes de cinemática 2D vía XeLaTeX + matplotlib."""

import subprocess, io, os, sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'axes.unicode_minus': False,
})

FIG_W, FIG_H = 5.5, 2.2

def ax_base(ax, bg='#F1EFE8'):
    ax.set_facecolor(bg)
    ax.tick_params(labelsize=7, colors='#5F5E5A')
    for sp in ax.spines.values():
        sp.set_color('#D3D1C7')
    ax.grid(True, color='#D3D1C7', linewidth=0.4, linestyle='--', alpha=0.7)

# ── Figuras ─────────────────────────────────────────────────────────────

def fig_p1(path):
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
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#F1EFE8', edgecolor='none')
    plt.close(fig)

def fig_p2(path):
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
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#F1EFE8', edgecolor='none')
    plt.close(fig)

def fig_p3(path):
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
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#F1EFE8', edgecolor='none')
    plt.close(fig)

def fig_p4(path):
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
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#F1EFE8', edgecolor='none')
    plt.close(fig)

def fig_p5(path):
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
    fig.savefig(path, dpi=150, bbox_inches='tight', facecolor='#F1EFE8', edgecolor='none')
    plt.close(fig)

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
\definecolor{coral}{HTML}{993C1D}
\definecolor{amber}{HTML}{BA7517}
\definecolor{negro}{HTML}{2C2C2A}

\setmainfont{Arial}
\setsansfont{Arial}
\renewcommand{\familydefault}{\sfdefault}

\titleformat{\section}{\bfseries\Large\color{azul}}{}{0em}{}[\vspace{-2pt}]

\pagestyle{fancy}
\fancyhf{}
\fancyhead[C]{\color{gris}\small\textbf{Cinemática en Dos Dimensiones — Apuntes}}
\fancyfoot[C]{\color{gris}\thepage}
\renewcommand{\headrule}{\color{azul}\rule{\textwidth}{0.4pt}}

\newcolumntype{L}{>{\raggedright\arraybackslash}X}
\newcolumntype{C}{>{\centering\arraybackslash}X}

\newcommand{\resbox}[2]{%
  \begin{tcolorbox}[colback=tealclr, colframe=teal, arc=4pt, boxrule=0.5pt,
    left=10pt, right=10pt, top=6pt, bottom=6pt, width=\textwidth]
    \textbf{\textcolor{teal}{#1:}} \textcolor{teal}{#2}
  \end{tcolorbox}}

\newcommand{\probheader}[3]{%
  \begin{tcolorbox}[colback=#3, colframe=#3, arc=4pt, boxrule=0.5pt,
    left=8pt, right=8pt, top=7pt, bottom=7pt, width=\textwidth]
    \textbf{\large\textcolor{white}{Problema #1}} \hfill \textbf{\large\textcolor{white}{#2}}
  \end{tcolorbox}}

\newcommand{\databox}[1]{%
  \begin{tcolorbox}[colback=grisclr, colframe=gris, arc=4pt, boxrule=0.3pt,
    left=6pt, right=6pt, top=4pt, bottom=4pt, width=\textwidth]
    \small\textcolor{gris}{#1}
  \end{tcolorbox}}

\newcommand{\paso}[1]{%
  \vspace{4pt}\textbf{\textcolor{teal}{#1}}}
"""


def build_tex(tex_path, img_dir):
    img_dir.mkdir(parents=True, exist_ok=True)
    fig_p1(img_dir / "p1.png")
    fig_p2(img_dir / "p2.png")
    fig_p3(img_dir / "p3.png")
    fig_p4(img_dir / "p4.png")
    fig_p5(img_dir / "p5.png")

    lines = [TEX_PREAMBLE]
    lines.append(r"\begin{document}")
    lines.append(r"\thispagestyle{fancy}")
    lines.append(r"\begin{center}")
    lines.append(r"  {\Huge\bfseries\color{azul} Cinemática en Dos Dimensiones}\\[4pt]")
    lines.append(r"  {\large\color{gris} Apuntes — Movimiento de Proyectiles}\\[4pt]")
    lines.append(r"  {\color{gris} $g = 9.8$ m/s$^2$ $|$ Sistema Internacional (SI)}")
    lines.append(r"\end{center}")
    lines.append(r"\vspace{6pt}\hrule height 0.5pt\vspace{10pt}")

    # ══════════════════════════════════════════════════════════════
    # PROBLEMA 1
    # ══════════════════════════════════════════════════════════════
    lines.append(r"\probheader{1}{Lanzamiento horizontal desde una ventana}{azul}")
    lines.append(r"\databox{$v_0$: 10 m/s (horizontal)  $|$  $t$: 5 s  $|$  $v_{0y}$: 0 m/s}")
    lines.append(r"\begin{center}")
    lines.append(r"  \includegraphics[width=14cm]{" + str(img_dir / "p1.png") + "}")
    lines.append(r"\end{center}")
    lines.append(r"\paso{Concepto clave}")
    lines.append(r"El movimiento se separa en \textbf{dos ejes independientes}: horizontal (MRU, sin aceleración)")
    lines.append(r"y vertical (caída libre desde reposo, $v_{0y} = 0$).")
    lines.append(r"\paso{a) Altura de la ventana}")
    lines.append(r"En el eje vertical, la única aceleración es la gravedad:")
    lines.append(r"\begin{align*}")
    lines.append(r"  h &= \frac{1}{2} g t^2 = \frac{1}{2} \times 9.8 \times 5^2 \\")
    lines.append(r"    &= \frac{1}{2} \times 9.8 \times 25 = 122.5\ \text{m}")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Altura de la ventana}{$h = 122.5$ m}")
    lines.append(r"\paso{b) Distancia horizontal}")
    lines.append(r"En el eje horizontal no hay aceleración (MRU):")
    lines.append(r"\begin{align*}")
    lines.append(r"  x &= v_0 \cdot t = 10 \times 5 = 50\ \text{m}")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Distancia horizontal}{$x = 50$ m}")
    lines.append(r"\vspace{6pt}\hrule height 0.5pt\vspace{10pt}")

    # ══════════════════════════════════════════════════════════════
    # PROBLEMA 2
    # ══════════════════════════════════════════════════════════════
    lines.append(r"\probheader{2}{Tiro parabólico — bala disparada a 35°}{coral}")
    lines.append(r"\databox{$v_0$: 400 m/s  $|$  $\theta$: 35°}")
    lines.append(r"\begin{center}")
    lines.append(r"  \includegraphics[width=14cm]{" + str(img_dir / "p2.png") + "}")
    lines.append(r"\end{center}")
    lines.append(r"\paso{Componentes de la velocidad inicial}")
    lines.append(r"\begin{align*}")
    lines.append(r"  v_{0x} &= v_0 \cos\theta = 400 \cos 35^\circ \approx 327.66\ \text{m/s} \\")
    lines.append(r"  v_{0y} &= v_0 \sin\theta = 400 \sin 35^\circ \approx 229.43\ \text{m/s}")
    lines.append(r"\end{align*}")
    lines.append(r"\paso{a) Tiempo total en el aire}")
    lines.append(r"En el punto más alto $v_y = 0$. El vuelo es simétrico:")
    lines.append(r"\begin{align*}")
    lines.append(r"  t_{\text{vuelo}} &= \frac{2 v_{0y}}{g} = \frac{2 \times 229.43}{9.8} \approx 46.82\ \text{s}")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Tiempo en el aire}{$t \approx 46.82$ s}")
    lines.append(r"\paso{b) Altura máxima}")
    lines.append(r"\begin{align*}")
    lines.append(r"  H &= \frac{v_{0y}^2}{2g} = \frac{229.43^2}{2 \times 9.8} = \frac{52637}{19.6} \\")
    lines.append(r"    &\approx 2685.6\ \text{m} \approx 2.69\ \text{km}")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Altura máxima}{$H \approx 2685.6$ m ($\approx 2.69$ km)}")
    lines.append(r"\paso{c) Alcance horizontal}")
    lines.append(r"\begin{align*}")
    lines.append(r"  R &= \frac{v_0^2 \sin(2\theta)}{g} = \frac{400^2 \times \sin 70^\circ}{9.8} \\")
    lines.append(r"    &= \frac{160000 \times 0.9397}{9.8} \approx 15342\ \text{m} \approx 15.34\ \text{km}")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Alcance horizontal}{$R \approx 15342$ m (15.34 km)}")
    lines.append(r"\vspace{6pt}\hrule height 0.5pt\vspace{10pt}")

    # ══════════════════════════════════════════════════════════════
    # PROBLEMA 3
    # ══════════════════════════════════════════════════════════════
    lines.append(r"\probheader{3}{Ángulo de elevación para alcanzar 4000 m}{amber}")
    lines.append(r"\databox{$v_0$: 350 m/s  $|$  $R$: 4000 m}")
    lines.append(r"\begin{center}")
    lines.append(r"  \includegraphics[width=14cm]{" + str(img_dir / "p3.png") + "}")
    lines.append(r"\end{center}")
    lines.append(r"\paso{Despejar el ángulo de la fórmula de alcance}")
    lines.append(r"Partimos de $R = v_0^2 \sin(2\theta) / g$ y despejamos:")
    lines.append(r"\begin{align*}")
    lines.append(r"  \sin(2\theta) &= \frac{R \cdot g}{v_0^2} = \frac{4000 \times 9.8}{350^2} \\")
    lines.append(r"               &= \frac{39200}{122500} \approx 0.32")
    lines.append(r"\end{align*}")
    lines.append(r"\paso{Dos soluciones del arcoseno}")
    lines.append(r"La función seno tiene dos valores en $[0^\circ, 180^\circ]$:")
    lines.append(r"\begin{align*}")
    lines.append(r"  2\theta_1 &= \arcsin(0.32) \approx 18.66^\circ \quad\to\quad \theta_1 \approx 9.33^\circ \\")
    lines.append(r"  2\theta_2 &= 180^\circ - 18.66^\circ = 161.34^\circ \quad\to\quad \theta_2 \approx 80.67^\circ")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Ángulos válidos}{$\theta_1 = 9.33^\circ$ (rasante)  $\cdot$  $\theta_2 = 80.67^\circ$ (parábola alta)}")
    lines.append(r"\begin{tcolorbox}[colback=grisclr, colframe=gris, arc=4pt, boxrule=0.3pt,")
    lines.append(r"  left=8pt, right=8pt, top=4pt, bottom=4pt, width=\textwidth]")
    lines.append(r"  \small\textcolor{gris}{Ambos ángulos producen exactamente el mismo alcance.}")
    lines.append(r"\end{tcolorbox}")
    lines.append(r"\vspace{6pt}\hrule height 0.5pt\vspace{10pt}")

    # ══════════════════════════════════════════════════════════════
    # PROBLEMA 4
    # ══════════════════════════════════════════════════════════════
    lines.append(r"\probheader{4}{Proyectil lanzado desde un avión a 800 km/h}{gris}")
    lines.append(r"\databox{$v$: 800 km/h $\to$ 222.22 m/s  $|$  $h$: 500 m}")
    lines.append(r"\begin{center}")
    lines.append(r"  \includegraphics[width=14cm]{" + str(img_dir / "p4.png") + "}")
    lines.append(r"\end{center}")
    lines.append(r"\paso{Conversión de unidades — paso obligatorio}")
    lines.append(r"Siempre trabaja en SI. Convertir km/h a m/s:")
    lines.append(r"\begin{align*}")
    lines.append(r"  v &= 800 \times \frac{1000}{3600} = 222.22\ \text{m/s}")
    lines.append(r"\end{align*}")
    lines.append(r"\paso{a) Tiempo de caída}")
    lines.append(r"El proyectil se lanza horizontalmente ($v_{0y} = 0$):")
    lines.append(r"\begin{align*}")
    lines.append(r"  h &= \frac{1}{2} g t^2 \\")
    lines.append(r"  t &= \sqrt{\frac{2h}{g}} = \sqrt{\frac{2 \times 500}{9.8}} = \sqrt{102.04} \approx 10.10\ \text{s}")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Tiempo de caída}{$t \approx 10.10$ s}")
    lines.append(r"\paso{b) Distancia horizontal}")
    lines.append(r"\begin{align*}")
    lines.append(r"  x &= v \cdot t = 222.22 \times 10.10 \approx 2244\ \text{m} \approx 2.24\ \text{km}")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Distancia horizontal}{$x \approx 2244$ m (2.24 km)}")
    lines.append(r"\vspace{6pt}\hrule height 0.5pt\vspace{10pt}")

    # ══════════════════════════════════════════════════════════════
    # PROBLEMA 5
    # ══════════════════════════════════════════════════════════════
    lines.append(r"\probheader{5}{Tiro parabólico — balón de fútbol a 40°}{teal}")
    lines.append(r"\databox{$v_0$: 22 m/s  $|$  $\theta$: 40°}")
    lines.append(r"\begin{center}")
    lines.append(r"  \includegraphics[width=14cm]{" + str(img_dir / "p5.png") + "}")
    lines.append(r"\end{center}")
    lines.append(r"\paso{Componentes de la velocidad inicial}")
    lines.append(r"\begin{align*}")
    lines.append(r"  v_{0x} &= 22 \cos 40^\circ \approx 16.85\ \text{m/s} \\")
    lines.append(r"  v_{0y} &= 22 \sin 40^\circ \approx 14.14\ \text{m/s}")
    lines.append(r"\end{align*}")
    lines.append(r"\paso{a) Altura máxima}")
    lines.append(r"\begin{align*}")
    lines.append(r"  H &= \frac{v_{0y}^2}{2g} = \frac{14.14^2}{2 \times 9.8} = \frac{199.94}{19.6} \\")
    lines.append(r"    &\approx 10.20\ \text{m}")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Altura máxima}{$H \approx 10.20$ m}")
    lines.append(r"\paso{b) Alcance horizontal}")
    lines.append(r"\begin{align*}")
    lines.append(r"  R &= \frac{v_0^2 \sin(2\theta)}{g} = \frac{22^2 \times \sin 80^\circ}{9.8} \\")
    lines.append(r"    &= \frac{484 \times 0.9848}{9.8} \approx 48.63\ \text{m}")
    lines.append(r"\end{align*}")
    lines.append(r"\resbox{Alcance horizontal}{$R \approx 48.63$ m}")
    lines.append(r"\begin{tcolorbox}[colback=grisclr, colframe=gris, arc=4pt, boxrule=0.3pt,")
    lines.append(r"  left=8pt, right=8pt, top=4pt, bottom=4pt, width=\textwidth]")
    lines.append(r"  \small\textcolor{gris}{El alcance máximo se logra con $\theta = 45^\circ$. A $40^\circ$ estamos muy cerca del óptimo.}")
    lines.append(r"\end{tcolorbox}")
    lines.append(r"\vspace{6pt}\hrule height 0.5pt\vspace{10pt}")

    # ══════════════════════════════════════════════════════════════
    # RESUMEN
    # ══════════════════════════════════════════════════════════════
    lines.append(r"\section{Resumen de resultados}")
    lines.append(r"\begin{tabularx}{\textwidth}{CCC}")
    lines.append(r"  \toprule\rowcolor{azul}")
    lines.append(r"  \textbf{\textcolor{white}{Problema}} & \textbf{\textcolor{white}{Incógnita}} & \textbf{\textcolor{white}{Resultado}} \\")
    lines.append(r"  \midrule")
    rows = [
        ("1a", "Altura de la ventana",  "122.5 m"),
        ("1b", "Distancia horizontal",  "50 m"),
        ("2a", "Tiempo en el aire",     "46.82 s"),
        ("2b", "Altura máxima",         "2685.6 m"),
        ("2c", "Alcance horizontal",    "15 342 m (15.34 km)"),
        ("3",  "Ángulo de elevación",   "$9.33^\\circ$  o  $80.67^\\circ$"),
        ("4a", "Tiempo de caída",       "10.10 s"),
        ("4b", "Distancia horizontal",  "2 244 m (2.24 km)"),
        ("5a", "Altura máxima",         "10.20 m"),
        ("5b", "Alcance horizontal",    "48.63 m"),
    ]
    for i, (a, b, c) in enumerate(rows):
        if i % 2 == 1:
            lines.append(r"  \rowcolor{azulclr}")
        lines.append(f"  {a} & {b} & {c} \\\\")
    lines.append(r"  \bottomrule")
    lines.append(r"\end{tabularx}")
    lines.append(r"\vspace{10pt}")

    # Fórmulas de referencia
    lines.append(r"\section{Fórmulas de referencia}")
    lines.append(r"\begin{tabularx}{\textwidth}{LC}")
    lines.append(r"  \toprule\rowcolor{azul}")
    lines.append(r"  \textbf{\textcolor{white}{Magnitud}} & \textbf{\textcolor{white}{Fórmula}} \\")
    lines.append(r"  \midrule\rowcolor{azulclr}")
    lines.append(r"  Tiempo de vuelo    & $t = \dfrac{2 v_{0y}}{g} = \dfrac{2 v_0 \sin\theta}{g}$ \\")
    lines.append(r"  \rowcolor{azulclr}")
    lines.append(r"  Altura máxima      & $H = \dfrac{v_{0y}^2}{2g} = \dfrac{v_0^2 \sin^2\theta}{2g}$ \\")
    lines.append(r"  \rowcolor{azulclr}")
    lines.append(r"  Alcance horizontal & $R = \dfrac{v_0^2 \sin(2\theta)}{g}$ \\")
    lines.append(r"  \rowcolor{azulclr}")
    lines.append(r"  Lanzamiento horiz. & $h = \dfrac{1}{2} g t^2,\quad x = v_0 t$ \\")
    lines.append(r"  \rowcolor{azulclr}")
    lines.append(r"  Conversi\'on km/h $\to$ m/s & $v(\text{m/s}) = v(\text{km/h}) \times \dfrac{1000}{3600}$ \\")
    lines.append(r"  \bottomrule")
    lines.append(r"\end{tabularx}")

    lines.append(r"\vspace{10pt}")
    lines.append(r"\begin{tcolorbox}[colback=grisclr, colframe=gris, arc=4pt, boxrule=0.3pt,")
    lines.append(r"  left=8pt, right=8pt, top=4pt, bottom=4pt, width=\textwidth]")
    lines.append(r"  \small\textcolor{gris}{Todos los cálculos utilizan $g = 9.8$ m/s$^2$. Las unidades deben ser consistentes (SI).}")
    lines.append(r"\end{tcolorbox}")
    lines.append(r"\end{document}")

    tex_path.write_text("\n".join(lines), encoding="utf-8")
    return tex_path


def main():
    base = Path(__file__).parent
    tex_path = base / "cinematica_2D_apuntes.tex"
    img_dir = base / "img_apuntes"
    build_tex(tex_path, img_dir)
    print(f"📄 .tex generado: {tex_path}")

    result = subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-output-directory", str(base), str(tex_path)],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        log = tex_path.with_suffix(".log")
        if log.exists():
            print(log.read_text(encoding="utf-8")[-1500:])
        sys.exit(1)
    print(f"✅ PDF: {(base / 'cinematica_2D_apuntes.pdf').resolve()}")


if __name__ == "__main__":
    main()
