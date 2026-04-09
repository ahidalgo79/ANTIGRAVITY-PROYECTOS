import re
from pathlib import Path

def actualizar_latex():
    print("=" * 60)
    print("SINCRONIZACIÓN LATEX: rescreening n=33 -> n=30")
    print("=" * 60)

    # Ruta específica del archivo principal expandido
    latex_path = Path("PAPER_REVISION_SWARM_RPAS/05_ESCRITURA/main_expanded.tex")

    if not latex_path.exists():
        print(f"ERROR: No se encontró el archivo en: {latex_path}")
        return

    # Leer contenido
    with open(latex_path, 'r', encoding='utf-8') as f:
        contenido = f.read()

    # Crear backup
    backup_path = latex_path.with_suffix('.backup_n30.tex')
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(contenido)
    print(f"OK: Backup creado en: {backup_path.name}")

    # Definir transformaciones masivas
    reemplazos = [
        # Cardinalidad Total
        (r'n=33', 'n=30'),
        (r'33 studies', '30 studies'),
        (r'33 artículos', '30 artículos'),
        (r'33 papers', '30 papers'),
        
        # Sub-cardinalidad (Primarios)
        (r'26 primary research articles', '23 primary research articles'),
        (r'26 artículos de investigación primaria', '23 artículos de investigación primaria'),
        (r'26 estudios primarios', '23 estudios primarios'),
        
        # Estadísticas de PSO (10/33=30.3% -> 10/30=33.3%)
        (r'30\.3%', '33.3%'),
        (r'10 of 33', '10 of 30'),
        
        # PRISMA y Flujo
        (r'33 included studies', '30 included studies'),
        (r'33 estudios incluidos', '30 estudios incluidos'),
    ]

    # Aplicar cambios
    contenido_actualizado = contenido
    cambios = 0
    for patron, nuevo in reemplazos:
        # Usar re.sub con ignore case para mayor robustez
        nuevo_contenido, n = re.subn(patron, nuevo, contenido_actualizado, flags=re.IGNORECASE)
        if n > 0:
            cambios += n
            print(f"   [+] Aplicado: {patron} -> {nuevo} ({n} ocurrencias)")
        contenido_actualizado = nuevo_contenido

    # Insertar nota técnica de rescreening
    nota_tecnica = """
% --- NOTA DE CONTROL DE CALIDAD (30-MAR-2026) ---
% Durante la fase final de revisión se procedió a un rescreening detallado.
% Se identificó que 3 estudios (anteriormente S34, S35, S36) no cumplían
% con los criterios de exclusión por duplicidad de datos en versiones posteriores.
% El corpus final se ajusta a n=30 estudios.
% -----------------------------------------------
"""
    if "% NOTA DE CONTROL DE CALIDAD" not in contenido_actualizado:
        # Insertar al principio del documento, después de \documentclass o al inicio
        contenido_actualizado = nota_tecnica + "\n" + contenido_actualizado
        print("   [+] Nota técnica de rescreening insertada al inicio.")

    # Guardar cambios
    with open(latex_path, 'w', encoding='utf-8') as f:
        f.write(contenido_actualizado)

    print("\n" + "-" * 60)
    print(f"OK: SINCRONIZACIÓN COMPLETADA: {cambios} cambios realizados.")
    print(f"📄 Archivo actualizado: {latex_path}")
    print("-" * 60)

if __name__ == "__main__":
    actualizar_latex()
