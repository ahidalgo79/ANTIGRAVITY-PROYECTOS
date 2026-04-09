# ver_todas_las_claves.py
import os
from pathlib import Path
import sys

# Forzar UTF-8 para la salida estándar en Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Ruta de tu archivo .env
env_path = Path(r"C:\Users\HangarUPCH\Documents\Antigravity_Proyectos\Swarm Intelligence Algorithms for Multi-RPAS\.env")

if env_path.exists():
    print("=" * 60)
    print("CLAVES API ENCONTRADAS EN .env")
    print("=" * 60)
    
    with open(env_path, 'r', encoding='utf-8') as f:
        for linea in f:
            linea = linea.strip()
            if linea and not linea.startswith("#"):
                if "API_KEY" in linea or "API" in linea:
                    # Ocultar parte de la clave por seguridad
                    if "=" in linea:
                        partes = linea.split("=", 1)
                        key = partes[0].strip()
                        value = partes[1].strip().strip('"').strip("'")
                        if value and len(value) > 15:
                            value_mostrada = f"{value[:10]}...{value[-6:]}"
                        else:
                            value_mostrada = value[:10] if value else "vacio"
                        print(f"   {key} = {value_mostrada} (longitud: {len(value) if value else 0})")
                    else:
                        print(f"   {linea}")
else:
    print(f"No se encontro el archivo .env en: {env_path}")