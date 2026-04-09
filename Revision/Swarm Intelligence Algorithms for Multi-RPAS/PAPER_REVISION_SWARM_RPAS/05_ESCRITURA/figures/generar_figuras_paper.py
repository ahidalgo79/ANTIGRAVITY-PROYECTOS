import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
from datetime import datetime

# Configurar matplotlib para estilo académico (publicación)
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
matplotlib.rcParams['figure.dpi'] = 300  # Alta resolución para publicación
matplotlib.rcParams['savefig.dpi'] = 300
matplotlib.rcParams['savefig.bbox'] = 'tight'
matplotlib.rcParams['savefig.pad_inches'] = 0.1
matplotlib.rcParams['axes.linewidth'] = 1.0
matplotlib.rcParams['xtick.major.width'] = 0.8
matplotlib.rcParams['ytick.major.width'] = 0.8

# Rutas
ruta_excel = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\03_ANALISIS_NOTAS\Fichas_Analisis_NUEVO.xlsx'
ruta_salida = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\figuras'

# Crear carpeta de salida si no existe
os.makedirs(ruta_salida, exist_ok=True)

print("📊 Generando figuras para el paper...\n")

# Cargar datos del Excel
df_todos = pd.read_excel(ruta_excel, sheet_name='TODOS_PAPERS')
df_gaps = pd.read_excel(ruta_excel, sheet_name='GAPS_POR_PAPER')
df_estadisticas = pd.read_excel(ruta_excel, sheet_name='ESTADISTICAS')

# =============================================================================
# FIGURA 1: DISTRIBUCIÓN DE ALGORITMOS (Bar Chart Horizontal)
# =============================================================================
print("📈 Generando Figura 1: Distribución de Algoritmos...")

# Contar algoritmos
algo_counts = df_todos['Algoritmo Principal'].value_counts()

# Crear figura
fig1, ax1 = plt.subplots(figsize=(8, 6))

# Colores personalizados para algoritmos
colors_algo = {
    'PSO': '#2E86AB', 'Review': '#A23B72', 'ACO': '#F18F01', 
    'ABC': '#C73E1D', 'SSA': '#6A994E', 'Otro': '#577590',
    'GA': '#BC4B51', 'SFLA': '#7B68EE', 'WPA': '#9370DB',
    'Híbrido': '#FF6B6B', 'NOA': '#4ECDC4', 'DBO': '#45B7D1',
    'GWO': '#96CEB4', 'DOA': '#FECA57'
}

# Crear barras horizontales
y_pos = range(len(algo_counts))
bars = ax1.barh(y_pos, [algo_counts[algo] for algo in algo_counts.index], 
                color=[colors_algo.get(algo, '#95A5A6') for algo in algo_counts.index],
                edgecolor='black', linewidth=0.5)

# Etiquetas y títulos
ax1.set_yticks(y_pos)
ax1.set_yticklabels([f'{algo} (n={algo_counts[algo]})' for algo in algo_counts.index], fontsize=9)
ax1.set_xlabel('Número de Papers', fontsize=10, fontweight='bold')
ax1.set_title('A) Distribución de Algoritmos de Inteligencia de Enjambre (n=33)', 
              fontsize=11, fontweight='bold', pad=15)

# Agregar valores en las barras
for i, (algo, count) in enumerate(zip(algo_counts.index, algo_counts.values)):
    percentage = (count / len(df_todos)) * 100
    ax1.text(count + 0.15, i, f'{percentage:.1f}%', va='center', fontsize=8, fontweight='normal')

# Grid sutil y límites
ax1.xaxis.grid(True, linestyle='--', alpha=0.3)
ax1.set_axisbelow(True)
ax1.set_xlim(0, max(algo_counts.values) * 1.3)

plt.tight_layout()
plt.savefig(os.path.join(ruta_salida, 'Fig1_Algorithm_Distribution.png'), 
            format='png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Fig1_Algorithm_Distribution.png guardado")

# =============================================================================
# FIGURA 2: GAPS POR DIMENSIÓN (Donut Chart)
# =============================================================================
print("📈 Generando Figura 2: Gaps por Dimensión...")

# Contar gaps por dimensión
dim_counts = df_gaps['Dimensión'].value_counts()
dim_order = ['Tecnológica', 'Práctica', 'Metodológica', 'Teórica']
dim_counts = dim_counts.reindex([d for d in dim_order if d in dim_counts.index])

# Colores para dimensiones
colors_dim = ['#E74C3C', '#3498DB', '#2ECC71', '#9B59B6']

# Crear figura
fig2, ax2 = plt.subplots(figsize=(6, 6))

# Donut chart
wedges, texts, autotexts = ax2.pie(dim_counts.values, 
                                    labels=[f'{dim}\n({count} gaps)' for dim, count in zip(dim_counts.index, dim_counts.values)],
                                    autopct='%1.1f%%',
                                    colors=colors_dim,
                                    startangle=90,
                                    counterclock=False,
                                    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=2),
                                    textprops={'fontsize': 9, 'weight': 'bold'})

# Estilizar porcentajes
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(10)

# Título
ax2.set_title('B) Distribución de Gaps por Dimensión (n=172)', 
              fontsize=11, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(os.path.join(ruta_salida, 'Fig2_Gaps_by_Dimension.png'), 
            format='png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Fig2_Gaps_by_Dimension.png guardado")

# =============================================================================
# FIGURA 3: GAPS POR PRIORIDAD (Stacked Bar + Percentages)
# =============================================================================
print("📈 Generando Figura 3: Gaps por Prioridad...")

# Contar gaps por prioridad
pri_counts = df_gaps['Prioridad'].value_counts()
pri_order = ['Crítico', 'Importante', 'Menor']
pri_counts = pri_counts.reindex([p for p in pri_order if p in pri_counts.index])

# Colores para prioridades
colors_pri = {'Crítico': '#E74C3C', 'Importante': '#F39C12', 'Menor': '#2ECC71'}

# Crear figura
fig3, ax3 = plt.subplots(figsize=(7, 5))

# Barras verticales
bars = ax3.bar(pri_counts.index, pri_counts.values, 
               color=[colors_pri[pri] for pri in pri_counts.index],
               edgecolor='black', linewidth=0.8)

# Agregar valores y porcentajes encima de cada barra
total_gaps = len(df_gaps)
for bar in bars:
    height = bar.get_height()
    percentage = (height / total_gaps) * 100
    ax3.text(bar.get_x() + bar.get_width()/2., height + 2, 
             f'{int(height)}\n({percentage:.1f}%)',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

# Etiquetas y título
ax3.set_ylabel('Número de Gaps', fontsize=10, fontweight='bold')
ax3.set_title('C) Distribución de Gaps por Prioridad (n=172)', 
              fontsize=11, fontweight='bold', pad=15)
ax3.set_ylim(0, max(pri_counts.values) * 1.3)
ax3.grid(axis='y', linestyle='--', alpha=0.3)
ax3.set_axisbelow(True)

plt.tight_layout()
plt.savefig(os.path.join(ruta_salida, 'Fig3_Gaps_by_Priority.png'), 
            format='png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Fig3_Gaps_by_Priority.png guardado")

# =============================================================================
# FIGURA 4: TOP 10 GAPS CRÍTICOS (Horizontal Bar Chart con % de papers)
# =============================================================================
print("📈 Generando Figura 4: Top 10 Gaps Críticos...")

# Filtrar gaps críticos y contar por descripción de gap
critical_gaps = df_gaps[df_gaps['Prioridad'] == 'Crítico']
gap_freq = critical_gaps['Gap'].value_counts().head(10)

# Calcular % de papers afectados para cada gap
gap_paper_pct = []
for gap_desc in gap_freq.index:
    papers_affected = critical_gaps[critical_gaps['Gap'] == gap_desc]['ID'].nunique()
    pct = (papers_affected / len(df_todos)) * 100
    gap_paper_pct.append(pct)

# Crear figura
fig4, ax4 = plt.subplots(figsize=(9, 7))

# Barras horizontales con gradiente de color
y_pos = range(len(gap_freq))
colors_top = plt.cm.Reds([0.3 + i*0.07 for i in range(len(gap_freq))])

bars = ax4.barh(y_pos, gap_freq.values, color=colors_top, edgecolor='black', linewidth=0.5)

# Etiquetas de ejes (truncar texto largo)
gap_labels = []
for gap in gap_freq.index:
    if len(gap) > 50:
        gap_labels.append(gap[:47] + '...')
    else:
        gap_labels.append(gap)

ax4.set_yticks(y_pos)
ax4.set_yticklabels(gap_labels, fontsize=8, ha='right')
ax4.set_xlabel('Frecuencia del Gap Crítico', fontsize=10, fontweight='bold')
ax4.set_title('D) Top 10 Gaps Críticos Más Frecuentes', 
              fontsize=11, fontweight='bold', pad=15)

# Agregar valores y % de papers
for i, (count, pct) in enumerate(zip(gap_freq.values, gap_paper_pct)):
    ax4.text(count + 0.3, i, f'{count} ({pct:.1f}% papers)', 
             va='center', fontsize=8, fontweight='normal')

# Grid y límites
ax4.xaxis.grid(True, linestyle='--', alpha=0.3)
ax4.set_axisbelow(True)
ax4.set_xlim(0, max(gap_freq.values) * 1.25)

plt.tight_layout()
plt.savefig(os.path.join(ruta_salida, 'Fig4_Top10_Critical_Gaps.png'), 
            format='png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Fig4_Top10_Critical_Gaps.png guardado")

# =============================================================================
# FIGURA 5 (OPCIONAL): MÉTRICAS COMPARATIVAS (Small Multiples)
# =============================================================================
print("📈 Generando Figura 5: Métricas Comparativas Extraídas...")

# Preparar datos de métricas (usar nombres sin espacios)
metrics_data = {
    'Metrica': ['Tiempo', 'Energia', 'Convergencia'],
    'Papers': [
        df_todos['Métrica: Tiempo'].notna().sum(),
        df_todos['Métrica: Energía'].notna().sum(), 
        df_todos['Métrica: Convergencia'].notna().sum()
    ],
    'Porcentaje': [
        (df_todos['Métrica: Tiempo'].notna().sum() / len(df_todos)) * 100,
        (df_todos['Métrica: Energía'].notna().sum() / len(df_todos)) * 100,
        (df_todos['Métrica: Convergencia'].notna().sum() / len(df_todos)) * 100
    ]
}
df_metrics = pd.DataFrame(metrics_data)

# Crear figura con 3 subplots pequeños
fig5, axes = plt.subplots(1, 3, figsize=(10, 4))
colors_metrics = ['#3498DB', '#2ECC71', '#9B59B6']

for idx, ax in enumerate(axes):
    row = df_metrics.iloc[idx]
    color = colors_metrics[idx]
    
    # Barra principal
    ax.bar([0], [row['Papers']], color=color, edgecolor='black', linewidth=0.8)
    
    # Línea de referencia (total papers)
    ax.axhline(y=len(df_todos), color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    
    # Etiquetas
    ax.set_xticks([0])
    ax.set_xticklabels([row['Metrica']], fontsize=9, fontweight='bold')
    ax.set_ylabel('Papers', fontsize=8)
    ax.set_ylim(0, len(df_todos) * 1.2)
    
    # Texto con porcentaje
    ax.text(0, row['Papers'] + 1, f"{row['Porcentaje']:.1f}%", 
            ha='center', fontsize=10, fontweight='bold', 
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Grid sutil
    ax.grid(axis='y', linestyle='--', alpha=0.2)
    ax.set_axisbelow(True)

# Título general
fig5.suptitle('E) Disponibilidad de Métricas Numéricas en los 33 Papers Analizados', 
              fontsize=11, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig(os.path.join(ruta_salida, 'Fig5_Metrics_Availability.png'), 
            format='png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Fig5_Metrics_Availability.png guardado")

# =============================================================================
# RESUMEN FINAL
# =============================================================================
print(f"\n{'='*60}")
print(f"✅ FIGURAS GENERADAS EXITOSAMENTE")
print(f"{'='*60}")
print(f"\nArchivos creados en: {ruta_salida}")
print(f"  1. Fig1_Algorithm_Distribution.png  → Distribución de 14 algoritmos")
print(f"  2. Fig2_Gaps_by_Dimension.png       → Gaps por dimensión (4 categorías)")
print(f"  3. Fig3_Gaps_by_Priority.png        → Gaps por prioridad (3 niveles)")
print(f"  4. Fig4_Top10_Critical_Gaps.png     → Top 10 gaps críticos")
print(f"  5. Fig5_Metrics_Availability.png    → Métricas comparativas extraídas")
print(f"\nEspecificaciones técnicas:")
print(f"  • Resolución: 300 DPI (estándar para publicación)")
print(f"  • Formato: PNG con fondo transparente")
print(f"  • Estilo: Académico, apto para IEEE/Elsevier/Springer")
print(f"  • Fuentes: Sans-serif (Arial/DejaVu) para legibilidad")
print(f"\nUso en el paper:")
print(f"  • Insertar en secciones: Results (Fig1, Fig5), Discussion (Fig2-4)")
print(f"  • Referenciar como: 'Fig. 1', 'Fig. 2', etc. en el texto")
print(f"  • Leyendas autocontenidas: cada figura es comprensible sin texto adicional")