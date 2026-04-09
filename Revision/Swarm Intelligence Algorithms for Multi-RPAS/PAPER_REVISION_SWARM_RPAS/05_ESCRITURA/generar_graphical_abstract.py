import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, ArrowStyle
import os

# Configurar estilo para publicación
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['savefig.bbox'] = 'tight'

# Rutas
ruta_salida = r'C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\PAPER_REVISION_SWARM_RPAS\05_ESCRITURA\figuras'
os.makedirs(ruta_salida, exist_ok=True)

print("🎨 Generando Graphical Abstract...\n")

# Crear figura grande para graphical abstract
fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis('off')

# Título del graphical abstract
ax.text(50, 95, 'Swarm Intelligence for Multi-UAV Path Planning in Precision Agriculture', 
        fontsize=14, fontweight='bold', ha='center', va='top', 
        bbox=dict(boxstyle='round', facecolor='#2E86AB', alpha=0.1, edgecolor='#2E86AB'))

ax.text(50, 91, 'A Systematic Review (2021-2025)', 
        fontsize=10, ha='center', va='top', style='italic')

# === BLOQUE 1: LITERATURA ANALIZADA ===
# Caja principal
box1 = FancyBboxPatch((10, 75), 80, 12, boxstyle='round,pad=0.5', 
                      facecolor='#E8F4F8', edgecolor='#2E86AB', linewidth=2)
ax.add_patch(box1)

ax.text(50, 83, '📚 33 Papers Analizados', fontsize=12, fontweight='bold', ha='center')
ax.text(50, 78, 'IEEE • Springer • ScienceDirect • Research Rabbit', 
        fontsize=9, ha='center', style='italic')

# === BLOQUE 2: ALGORITMOS IDENTIFICADOS ===
# Caja principal
box2 = FancyBboxPatch((10, 58), 80, 12, boxstyle='round,pad=0.5', 
                      facecolor='#FFF2E8', edgecolor='#F18F01', linewidth=2)
ax.add_patch(box2)

ax.text(50, 66, '🔍 14 Algoritmos de Inteligencia de Enjambre', fontsize=12, fontweight='bold', ha='center')

# Mini barras para algoritmos principales
algo_names = ['PSO 30%', 'ACO 9%', 'ABC 6%', 'SSA 6%', 'Otros 49%']
algo_colors = ['#2E86AB', '#F18F01', '#C73E1D', '#6A994E', '#95A5A6']
x_pos = [15, 30, 45, 60, 75]

for x, name, color in zip(x_pos, algo_names, algo_colors):
    ax.bar(x, 4, width=8, color=color, edgecolor='black', linewidth=0.5)
    ax.text(x, 2, name, fontsize=7, ha='center', va='center', fontweight='bold', color='white')

# === BLOQUE 3: GAPS EN 4 DIMENSIONES ===
# Caja principal
box3 = FancyBboxPatch((10, 38), 80, 15, boxstyle='round,pad=0.5', 
                      facecolor='#F0E8F8', edgecolor='#9B59B6', linewidth=2)
ax.add_patch(box3)

ax.text(50, 50, '⚠️ 172 Gaps de Investigación en 4 Dimensiones', fontsize=12, fontweight='bold', ha='center')

# Donut chart simplificado para dimensiones
center_x, center_y = 50, 43
radii = [8, 5]  # outer, inner

# Segmentos del donut: Tecnológica, Práctica, Metodológica, Teórica
dimensions = [
    ('Tecnológica 31%', '#E74C3C', 0, 0.31),
    ('Práctica 28%', '#3498DB', 0.31, 0.59),
    ('Metodológica 23%', '#2ECC71', 0.59, 0.82),
    ('Teórica 18%', '#9B59B6', 0.82, 1.0)
]

for label, color, start_pct, end_pct in dimensions:
    start_angle = start_pct * 360
    end_angle = end_pct * 360
    
    # Dibujar arco exterior
    wedge_outer = patches.Wedge((center_x, center_y), radii[0], start_angle, end_angle, 
                                width=radii[0]-radii[1], facecolor=color, edgecolor='white', linewidth=1)
    ax.add_patch(wedge_outer)
    
    # Etiqueta fuera del donut
    mid_angle = (start_angle + end_angle) / 2
    label_x = center_x + (radii[0] + 2) * 0.015 * 100 * (mid_angle/180 * 3.14159)
    label_y = center_y + (radii[0] + 2) * 0.015 * 100 * (mid_angle/180 * 3.14159)
    ax.text(center_x + 12 * (start_pct - 0.5) * 2, center_y + 3, label, 
            fontsize=7, ha='center', va='center', fontweight='bold')

# === BLOQUE 4: DIRECCIONES PRIORITARIAS ===
# Caja principal
box4 = FancyBboxPatch((10, 15), 80, 18, boxstyle='round,pad=0.5', 
                      facecolor='#E8F8F0', edgecolor='#27AE60', linewidth=2)
ax.add_patch(box4)

ax.text(50, 30, '🎯 3 Direcciones Prioritarias de Investigación', fontsize=12, fontweight='bold', ha='center')

# Tres flechas con contribuciones
contributions = [
    ('1. Benchmark Estandarizado', 'Comparación objetiva de algoritmos', '#27AE60'),
    ('2. Validación Experimental', 'Pruebas con UAVs reales en campo', '#2ECC71'),
    ('3. Entornos Dinámicos', 'Replanificación en tiempo real', '#1ABC9C')
]

for i, (title, desc, color) in enumerate(contributions):
    y_pos = 23 - i * 5
    # Flecha
    ax.arrow(15, y_pos + 1.5, 5, 0, head_width=1, head_length=1, fc=color, ec=color, linewidth=2)
    # Texto
    ax.text(22, y_pos + 2, title, fontsize=9, fontweight='bold', color=color)
    ax.text(22, y_pos, desc, fontsize=8, color='#333')

# === FLECHAS DE CONEXIÓN ===
# Flecha 1->2
ax.annotate('', xy=(50, 75), xytext=(50, 70), 
            arrowprops=dict(arrowstyle='->', color='#2E86AB', linewidth=2, ls='-'))

# Flecha 2->3
ax.annotate('', xy=(50, 58), xytext=(50, 53), 
            arrowprops=dict(arrowstyle='->', color='#F18F01', linewidth=2, ls='-'))

# Flecha 3->4
ax.annotate('', xy=(50, 38), xytext=(50, 33), 
            arrowprops=dict(arrowstyle='->', color='#9B59B6', linewidth=2, ls='-'))

# === FOOTER ===
ax.text(50, 5, 'Key Findings: 84.8% sin validación real • 75.8% sin modelado ambiental • 42.4% con métricas de tiempo', 
        fontsize=8, ha='center', va='bottom', style='italic', 
        bbox=dict(boxstyle='round', facecolor='#F8F9FA', edgecolor='#6C757D', alpha=0.8))

# Guardar figura
output_path = os.path.join(ruta_salida, 'Graphical_Abstract_Systematic_Review.png')
plt.savefig(output_path, format='png', dpi=300, bbox_inches='tight', facecolor='white')
plt.close()

print(f"✅ Graphical Abstract generado: {output_path}")
print(f"   Tamaño: {os.path.getsize(output_path) / 1024:.1f} KB")
print(f"   Resolución: 300 DPI (estándar para publicación)")
print(f"\nUso en el paper:")
print(f"   • Insertar al inicio del manuscrito (después del título/abstract)")
print(f"   • Referenciar como 'Graphical Abstract' en la portada del envío")
print(f"   • Formato compatible con Elsevier, IEEE, Springer")