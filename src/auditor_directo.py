#!/usr/bin/env python3
"""Auditor directo: Python extrae datos → POST crudo a Ollama → Reporte Markdown.
   Cero dependencias frágiles. Timeout explícito. Funciona en CPU antigua."""
import sys, time, json, requests, tomllib
from pathlib import Path

# 🔌 Configuración fija
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"
TIMEOUT = 150  # 2.5 min (suficiente para CPU sin AVX2)

def extraer_datos(ruta: str) -> str:
    p = Path(ruta).resolve()
    py_ver = sys.version.split()[0]
    deps = "NO ENCONTRADO"
    toml = p / "pyproject.toml"
    if toml.exists():
        try:
            with open(toml, "rb") as f:
                data = tomllib.load(f)
            deps = "\n".join(f"- {d}" for d in data.get("project", {}).get("dependencies", []))
        except Exception as e:
            deps = f"Error: {e}"
    estructura = "\n".join(sorted([f.name for f in p.iterdir() if not f.name.startswith('.')]))
    return f"RUTA: {p}\nPYTHON: {py_ver}\nDEPENDENCIAS:\n{deps}\nARCHIVOS:\n{estructura}"

def llamar_ollama(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.1, "num_ctx": 4096}
    }
    print(f"📡 Enviando petición a Ollama ({MODEL})... (espera hasta {TIMEOUT}s)", flush=True)
    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.json().get("response", "").strip()
    except requests.exceptions.Timeout:
        return f"⏱️ Timeout ({TIMEOUT}s). Ollama está procesando pero tardó más de lo esperado."
    except Exception as e:
        return f"❌ Error: {e}"

def main(ruta: str = ".", enfoque: str = "ia-agents"):
    print("🔍 Extrayendo datos reales del proyecto...", flush=True)
    datos = extraer_datos(ruta)
    
    prompt = f"""Genera un reporte Markdown técnico y preciso.
DATOS REALES DEL SISTEMA:
{datos}

ESTRUCTURA OBLIGATORIA:
# 🛠️ Estado del Entorno
# 📦 Stack Detectado
# 🔍 Archivos Clave
# ⚠️ Observaciones
# �� 3 Comandos Concretos para '{enfoque}'

REGLAS:
- Responde en ESPAÑOL.
- NUNCA inventes versiones, librerías o comandos.
- Si un dato falta, menciónalo explícitamente.
- Output: SOLO el Markdown."""
    
    reporte = llamar_ollama(prompt)
    print("\n" + "="*60 + "\n📄 REPORTE GENERADO\n" + "="*60 + "\n" + reporte)
    
    out = Path("reports") / f"auditoria_directa_{int(time.time())}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(reporte, encoding="utf-8")
    print(f"\n💾 Guardado: {out}")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv)>1 else ".", sys.argv[2] if len(sys.argv)>2 else "ia-agents")
