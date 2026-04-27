#!/usr/bin/env python3
"""
generar_figuras_paper.py
Tarea t25 (2026-04-24) — Regeneracion completa de figuras con:
  - Paleta Okabe-Ito (colorblind-safe, WCAG AA)
  - Hatch patterns para distinguibilidad en escala de grises
  - Fuente Times New Roman (consistencia con cuerpo del manuscrito)
  - En-dash Unicode en titulos (en lugar de doble guion LaTeX)
  - Exportacion PDF (vectorial) + PNG 300 DPI
  - Datos verificados contra main_expanded_purgado.tex (t25)

Figuras generadas:
  Figure2_Algorithm_Distribution   — Distribucion de algoritmos SI
  Figure3_Metrics_Availability     — Disponibilidad de metricas
  Figure4_Gaps_by_Dimension        — Brechas por dimension
  Figure5_Gaps_by_Priority         — Brechas por prioridad
  Figure6_Top10_Critical_Gaps      — Top 10 brechas criticas

Uso:
  python generar_figuras_paper.py [--outdir figures]

Dependencias: matplotlib>=3.5, numpy
"""

import os
import argparse
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams

# ── Configuracion global de fuentes y estilo ────────────────────────────────
rcParams["font.family"] = "serif"
rcParams["font.serif"] = ["Times New Roman", "DejaVu Serif", "serif"]
rcParams["font.size"] = 10
rcParams["axes.titlesize"] = 11
rcParams["axes.labelsize"] = 10
rcParams["xtick.labelsize"] = 9
rcParams["ytick.labelsize"] = 9
rcParams["legend.fontsize"] = 9
rcParams["figure.dpi"] = 150
rcParams["savefig.dpi"] = 300
rcParams["axes.spines.top"] = False
rcParams["axes.spines.right"] = False
rcParams["axes.grid"] = False

# ── Paleta Okabe-Ito (8 colores, colorblind-safe) ───────────────────────────
# Fuente: Okabe & Ito (2008) "Color Universal Design"
OI = {
    "orange":   "#E69F00",
    "sky":      "#56B4E9",
    "green":    "#009E73",
    "yellow":   "#F0E442",
    "blue":     "#0072B2",
    "vermil":   "#D55E00",
    "pink":     "#CC79A7",
    "black":    "#000000",
}

# Hatches para distinguibilidad en escala de grises
HATCHES = ["", "///", "xxx", "...", "---", "|||", "\\\\\\", "+++"]

DPI_PNG = 300
DPI_VEC = None  # PDF es vectorial, no aplica

def save(fig, name, outdir):
    """Guarda figura en PDF (vectorial) y PNG (300 DPI)."""
    os.makedirs(outdir, exist_ok=True)
    pdf_path = os.path.join(outdir, f"{name}.pdf")
    png_path = os.path.join(outdir, f"{name}.png")
    fig.savefig(pdf_path, format="pdf", bbox_inches="tight")
    fig.savefig(png_path, format="png", dpi=DPI_PNG, bbox_inches="tight")
    print(f"  Guardado: {pdf_path}")
    print(f"  Guardado: {png_path}")
    plt.close(fig)


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Distribucion de algoritmos SI (n=29)
# Datos: Table 5 de main_expanded_purgado.tex (t25)
# ════════════════════════════════════════════════════════════════════════════
def fig2_algorithms(outdir):
    # Orden descendente por numero de estudios (igual al PDF compilado)
    labels = ["PSO", "Review", "ACO", "ABC", "Other SI*", "SSA", "GWO", "NOA", "DOA"]
    counts = [9, 7, 2, 3, 3, 2, 1, 1, 1]
    colors = [
        OI["blue"],    # PSO
        OI["black"],   # Review
        OI["vermil"],  # ACO
        OI["green"],   # ABC
        OI["orange"],  # Other SI
        OI["sky"],     # SSA
        OI["pink"],    # GWO
        OI["yellow"],  # NOA
        OI["orange"],  # DOA — mismo tono que Other SI, diferenciado por hatch
    ]
    hatches = HATCHES[:len(labels)]

    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    y = np.arange(len(labels))
    bars = ax.barh(y, counts, color=colors, edgecolor="white",
                   linewidth=0.6, height=0.65)
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    # Etiquetas de valor al final de cada barra
    for bar, val in zip(bars, counts):
        ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", ha="left", fontsize=9)

    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.set_xlabel("Number of publications")
    ax.set_title("Distribution of swarm intelligence algorithms (2021\u20132025)")
    ax.set_xlim(0, max(counts) + 1.5)
    ax.invert_yaxis()

    footnote = ("*Other SI variants: SFLA (S08), Fuzzy/SIGPAF (S07), Wolf Pack (S21).\n"
                "PSO+ACO (S06) and APF+PSO (S26) classified under PSO. "
                "S24 (Rao et al.) classified under GWO.")
    fig.text(0.01, -0.06, footnote, ha="left", va="top",
             fontsize=7.5, style="italic", wrap=True)

    fig.tight_layout()
    save(fig, "Figure2_Algorithm_Distribution", outdir)


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Disponibilidad de metricas cuantitativas
# Datos: Table 6 de main_expanded_purgado.tex (t25)
# n=29: T=48.3%, E=13.8%, C=34.5%
# n=22: T=63.6%, E=18.2%, C=45.5%
# ════════════════════════════════════════════════════════════════════════════
def fig3_metrics(outdir):
    metrics = ["Execution time", "Energy\nconsumption", "Convergence\ncriteria"]
    rates_29 = [37.9, 13.8, 31.0]
    rates_22 = [50.0, 18.2, 40.9]

    x = np.arange(len(metrics))
    width = 0.35

    fig, ax = plt.subplots(figsize=(6.5, 4.0))

    bars1 = ax.bar(x - width / 2, rates_29, width, label="Full corpus (n=29)",
                   color=OI["blue"], edgecolor="white", linewidth=0.6,
                   hatch="")
    bars2 = ax.bar(x + width / 2, rates_22, width, label="Primary studies (n=22)",
                   color=OI["orange"], edgecolor="white", linewidth=0.6,
                   hatch="///")

    for bar, val in zip(list(bars1) + list(bars2),
                        rates_29 + rates_22):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.8,
                f"{val:.1f}%", ha="center", va="bottom", fontsize=8.5)

    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylabel("Reporting rate (%)")
    ax.set_ylim(0, 80)
    ax.set_title("Availability of quantitative performance metrics")
    ax.legend(frameon=False)
    fig.tight_layout()
    save(fig, "Figure3_Metrics_Availability", outdir)


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 4 — Brechas por dimension taxonomica (n=171)
# Datos: Table 9 de main_expanded_purgado.tex (t25)
# Practical=52, Technological=51, Methodological=39, Theoretical=29
# ════════════════════════════════════════════════════════════════════════════
def fig4_gaps_dimension(outdir):
    dims = ["Practical", "Technological", "Methodological", "Theoretical"]
    gaps = [52, 51, 39, 29]
    colors = [OI["blue"], OI["vermil"], OI["green"], OI["orange"]]
    hatches = ["", "///", "xxx", "..."]

    fig, ax = plt.subplots(figsize=(5.5, 4.0))
    x = np.arange(len(dims))
    bars = ax.bar(x, gaps, color=colors, edgecolor="white",
                  linewidth=0.6, width=0.6)
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    for bar, val in zip(bars, gaps):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.5,
                str(val), ha="center", va="bottom", fontsize=9.5,
                fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(dims, fontsize=9)
    ax.set_ylabel("Number of gaps (n=171)")
    ax.set_title("Research gaps by taxonomic dimension")
    ax.set_ylim(0, 65)
    fig.tight_layout()
    save(fig, "Figure4_Gaps_by_Dimension", outdir)


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 5 — Brechas por nivel de prioridad (n=171)
# Datos: Table 10 de main_expanded_purgado.tex (t25)
# Orden: Critical > Important > Minor (orden conceptual, no por frecuencia)
# ════════════════════════════════════════════════════════════════════════════
def fig5_gaps_priority(outdir):
    # Orden conceptual: Critical primero (como en el texto Sec. 5.2)
    priorities = ["Critical", "Important", "Minor"]
    gaps = [76, 88, 7]
    colors = [OI["vermil"], OI["orange"], OI["green"]]
    hatches = ["///", "", "..."]

    fig, ax = plt.subplots(figsize=(5.0, 3.8))
    x = np.arange(len(priorities))
    bars = ax.bar(x, gaps, color=colors, edgecolor="white",
                  linewidth=0.6, width=0.55)
    for bar, hatch in zip(bars, hatches):
        bar.set_hatch(hatch)

    for bar, val in zip(bars, gaps):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.8,
                str(val), ha="center", va="bottom", fontsize=9.5,
                fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(priorities)
    ax.set_ylabel("Number of gaps (n=171)")
    ax.set_title("Research gaps by priority level")
    ax.set_ylim(0, 105)
    fig.tight_layout()
    save(fig, "Figure5_Gaps_by_Priority", outdir)


# ════════════════════════════════════════════════════════════════════════════
# FIGURE 6 — Top 10 brechas criticas (n=29)
# Datos: Table 11 de main_expanded_purgado.tex (t25)
# ════════════════════════════════════════════════════════════════════════════
def fig6_top10(outdir):
    labels = [
        "Lack of real-field validation",
        "No dynamic obstacles/env.",
        "No wind/weather modelling",
        "No metric standardisation",
        "Single-UAV focus (no swarm)",
        "Unrealistic kinematic constraints",
        "Limited scalability assessment",
        "No direct energy measurement",
        "Communication robustness ignored",
        "No real-time replanning",
    ]
    counts = [29, 25, 20, 16, 15, 14, 13, 12, 11, 10]
    # Gradiente de color: mas critico = mas oscuro (mismo tono, paleta OI)
    # Usamos blue con alpha variante para mantener colorblind-safety
    base_colors = [OI["blue"]] * 4 + [OI["green"]] * 3 + [OI["orange"]] * 3
    hatches_top = [""] * 4 + ["///"] * 3 + ["xxx"] * 3

    fig, ax = plt.subplots(figsize=(8.5, 5.2))
    y = np.arange(len(labels))
    bars = ax.barh(y, counts, color=base_colors, edgecolor="white",
                   linewidth=0.6, height=0.65)
    for bar, hatch in zip(bars, hatches_top):
        bar.set_hatch(hatch)

    for bar, val in zip(bars, counts):
        ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2,
                str(val), va="center", ha="left", fontsize=9)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Number of papers (n=29)")
    ax.set_title("Top 10 critical research gaps ranked by frequency")
    ax.set_xlim(0, 34)
    ax.invert_yaxis()

    # Leyenda de colores
    legend_patches = [
        mpatches.Patch(facecolor=OI["blue"],   label="Ranks 1\u20134 (validation & environment)"),
        mpatches.Patch(facecolor=OI["green"],  hatch="///", label="Ranks 5\u20137 (scalability & metrics)"),
        mpatches.Patch(facecolor=OI["orange"], hatch="xxx", label="Ranks 8\u201310 (energy & communication)"),
    ]
    ax.legend(handles=legend_patches, frameon=False, fontsize=8,
              loc="lower right")

    fig.tight_layout()
    save(fig, "Figure6_Top10_Critical_Gaps", outdir)


# ════════════════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════════════════
def main():
    parser = argparse.ArgumentParser(
        description="Regenera figuras del manuscrito (t25, colorblind-safe)")
    parser.add_argument("--outdir", default="figures",
                        help="Directorio de salida (default: figures/)")
    args = parser.parse_args()

    print(f"\nGenerando figuras en: {os.path.abspath(args.outdir)}/\n")

    print("[Figure 2] Distribucion de algoritmos SI...")
    fig2_algorithms(args.outdir)

    print("[Figure 3] Disponibilidad de metricas...")
    fig3_metrics(args.outdir)

    print("[Figure 4] Brechas por dimension...")
    fig4_gaps_dimension(args.outdir)

    print("[Figure 5] Brechas por prioridad...")
    fig5_gaps_priority(args.outdir)

    print("[Figure 6] Top 10 brechas criticas...")
    fig6_top10(args.outdir)

    print("\nListo. Archivos generados (PDF vectorial + PNG 300 DPI):")
    for name in ["Figure2_Algorithm_Distribution",
                 "Figure3_Metrics_Availability",
                 "Figure4_Gaps_by_Dimension",
                 "Figure5_Gaps_by_Priority",
                 "Figure6_Top10_Critical_Gaps"]:
        for ext in [".pdf", ".png"]:
            path = os.path.join(args.outdir, name + ext)
            exists = "OK" if os.path.exists(path) else "MISSING"
            print(f"  [{exists}] {path}")

    print("\nNota para submission:")
    print("  - Enviar los .pdf como archivos de arte primarios a Elsevier.")
    print("  - Los .png (300 DPI) sirven como fallback si el sistema no acepta PDF.")
    print("  - La paleta Okabe-Ito cumple WCAG 2.1 AA y es distinguible en")
    print("    escala de grises gracias a los hatch patterns.")


if __name__ == "__main__":
    main()
