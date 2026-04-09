from pathlib import Path
import shutil
from datetime import datetime
import sys

# Forzar UTF-8 en Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Archivo original
original = Path("main_expanded.tex")

# Verificar que existe
if not original.exists():
    print(f"❌ ERROR: No se encuentra {original.absolute()}")
    exit()

# Crear backup con fecha
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = Path(f"main_expanded.backup_{timestamp}.tex")

shutil.copy2(original, backup)
print(f"✅ Backup creado: {backup.name}")
print(f"📁 Ubicación: {backup.absolute()}")
print(f"📏 Tamaño: {original.stat().st_size} bytes")
