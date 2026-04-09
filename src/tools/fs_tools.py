"""Herramientas para explorar el sistema de archivos"""
from pathlib import Path
from typing import List, Optional

def list_directory(path: str, max_depth: int = 2) -> List[str]:
    """Lista archivos/directorios con profundidad controlada"""
    root = Path(path).resolve()
    results = []
    
    def _walk(p: Path, depth: int):
        if depth > max_depth or not p.is_dir():
            return
        try:
            for item in sorted(p.iterdir()):
                indent = "  " * (depth - 1)
                suffix = "/" if item.is_dir() else ""
                results.append(f"{indent}{item.name}{suffix}")
                if item.is_dir() and not item.name.startswith(('.venv', '__pycache__', '.git')):
                    _walk(item, depth + 1)
        except PermissionError:
            results.append(f"{indent}[PERMISO DENEGADO]")
    
    _walk(root, 1)
    return [f"📁 {root}"] + results

def read_file(path: str, lines: Optional[str] = None) -> str:
    """Lee un archivo, opcionalmente un rango de líneas"""
    p = Path(path).resolve()
    if not p.exists():
        return f"❌ Archivo no encontrado: {p}"
    
    content = p.read_text(encoding="utf-8", errors="ignore")
    
    if lines:
        try:
            start, end = map(int, lines.split("-"))
            lines_list = content.splitlines()
            content = "\n".join(lines_list[start-1:end])
            content = f"[Líneas {start}-{end} de {p.name}]\n{content}"
        except ValueError:
            pass  # Si no es "1-10", devuelve todo
    
    # Truncar si es muy largo (para no saturar el contexto del LLM)
    if len(content) > 8000:
        content = content[:8000] + "\n\n[... contenido truncado ...]"
    
    return content

def get_env_vars(prefix: str = "") -> dict:
    """Obtiene variables de entorno, opcionalmente filtradas por prefijo"""
    import os
    return {k: ("***" if "KEY" in k or "SECRET" in k else v) 
            for k, v in os.environ.items() 
            if k.startswith(prefix)}