#!/usr/bin/env python3
"""Pipeline técnico: Datos → Estadísticas → Reporte Word/PDF"""
import sys, os, time
from pathlib import Path
import polars as pl
import polars.selectors as cs  # ✅ Forma moderna (Polars 1.0+)
import duckdb

def procesar(input_path: str, domain: str = "aeronautica"):
    p = Path(input_path).resolve()
    if not p.exists():
        print(f"❌ No encontrado: {p}")
        sys.exit(1)
        
    print(f"📥 Cargando {p.name}...", flush=True)
    df = pl.read_csv(p) if p.suffix == ".csv" else pl.read_excel(p)
    
    print("🧹 Limpieza básica...", flush=True)
    df_clean = df.unique()
    
    # ✅ Relleno seguro solo numéricos
    num_cols = df_clean.select(cs.numeric()).columns
    if num_cols:
        df_clean = df_clean.with_columns(
            pl.col(num_cols).fill_null(pl.col(num_cols).mean())
        )
        
    out = Path("data/processed") / f"{domain}_limpio.parquet"
    out.parent.mkdir(exist_ok=True)
    df_clean.write_parquet(out)
    print(f"✅ Guardado: {out}", flush=True)
    
    # 📊 Resumen con DuckDB (sintaxis SQL válida)
    print("\n📈 Resumen (DuckDB):")
    con = duckdb.connect()
    stats = con.execute(f"SELECT COUNT(*) as registros FROM read_parquet('{out}')").fetchdf()
    print(stats.to_markdown(index=False))
    
    # 🤖 Verificación LLM opcional
    print("\n🔍 Verificando LLM...", flush=True)
    try:
        import requests
        start = time.time()
        r = requests.post("http://localhost:11434/api/generate", 
                          json={"model":"qwen2.5:0.5b","prompt":"test","stream":False}, 
                          timeout=8)
        if time.time() - start < 5 and r.status_code == 200:
            print("✅ LLM responde rápido. Listo para análisis con IA.")
        else:
            print("⏱️ LLM lento. Continuando en modo offline.")
    except Exception:
        print("🔌 Ollama no responde. Pipeline completado sin IA.")
        
    print(f"\n💡 Siguiente paso: make audit-word f={domain}")
    return str(out)

if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv)>1 else "data/raw/datos.csv"
    dom = sys.argv[2] if len(sys.argv)>2 else "aeronautica"
    procesar(inp, dom)
