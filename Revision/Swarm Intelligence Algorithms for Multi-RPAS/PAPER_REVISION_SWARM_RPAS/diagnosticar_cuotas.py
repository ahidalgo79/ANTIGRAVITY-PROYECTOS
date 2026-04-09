# diagnosticar_cuotas.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
import time
import json

load_dotenv()

print("[INFO] DIAGNOSTICO DE CUOTAS Y MODELOS DISPONIBLES\n" + "="*60)

gemini_key = os.getenv("GEMINI_API_KEY")
resultados = {}

if gemini_key and gemini_key != "tu_api_key_aqui":
    genai.configure(api_key=gemini_key)
    
    # Modelos a probar con sus características (Basado en tu lista y en lo que funciona)
    modelos = [
        {"nombre": "gemini-2.5-flash", "tipo": "flash", "esperado": "alta cuota"},
        {"nombre": "gemini-2.5-pro", "tipo": "pro", "esperado": "cuota limitada"},
        {"nombre": "gemini-2.0-flash", "tipo": "flash", "esperado": "experimental"},
        {"nombre": "gemini-1.5-flash", "tipo": "flash", "esperado": "cuota generosa"},
        {"nombre": "gemini-1.5-pro", "tipo": "pro", "esperado": "cuota limitada"},
    ]
    
    print("\n[INFO] Probando disponibilidad de modelos:\n")
    
    for modelo in modelos:
        try:
            start = time.time()
            model = genai.GenerativeModel(modelo["nombre"])
            response = model.generate_content("Responde: ok")
            elapsed = time.time() - start
            
            resultados[modelo["nombre"]] = {
                "estado": "OK",
                "tiempo_ms": round(elapsed * 1000, 2),
                "tipo": modelo["tipo"]
            }
            print(f"OK: {modelo['nombre']:<35} -> {resultados[modelo['nombre']]['tiempo_ms']}ms")
            
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                estado = "CUOTA_EXCEDIDA"
                print(f"WARN: {modelo['nombre']:<35} -> CUOTA EXCEDIDA (limite alcanzado)")
            elif "404" in error_str:
                estado = "NO_DISPONIBLE"
                print(f"FAIL: {modelo['nombre']:<35} -> MODELO NO DISPONIBLE (404)")
            else:
                estado = f"ERROR: {error_str[:50]}"
                print(f"FAIL: {modelo['nombre']:<35} -> {estado}")
            
            resultados[modelo["nombre"]] = {
                "estado": estado,
                "tipo": modelo["tipo"]
            }
    
    # Identificar mejor modelo disponible
    modelos_ok = [m for m in resultados if resultados[m]["estado"] == "OK"]
    
    print("\n" + "="*60)
    print("RECOMENDACION:")
    
    if modelos_ok:
        # Priorizar flash por cuota, luego el más rápido
        flash_ok = [m for m in modelos_ok if resultados[m]["tipo"] == "flash"]
        if flash_ok:
            mejor = flash_ok[0]
            print(f"TARGET: Usar {mejor}")
            print(f"   - Tipo: Flash (mas cuota disponible)")
            print(f"   - Tiempo respuesta: {resultados[mejor]['tiempo_ms']}ms")
        else:
            mejor = modelos_ok[0]
            print(f"TARGET: Usar {mejor}")
            print(f"   WARN: Es modelo Pro, tiene cuota mas limitada")
        
        print(f"\nTIP: Usa este modelo para tareas puntuales.")
        print(f"   Para procesos largos, considera esperar a que se resetee la cuota.")
        
    else:
        print("WARN: No hay modelos Gemini funcionales actualmente.")
        print("\nSOLUCIONES:")
        print("1. Ve a https://aistudio.google.com/")
        print("2. Verifica tu proyecto y sus cuotas")
        print("3. En 'Usage' revisa los limites diarios")
        print("4. Si es cuenta nueva, espera 24h a que se activen las cuotas")
        print("5. Considera usar Qwen como alternativa")
    
else:
    print("FAIL: No hay API key de Gemini configurada")
    print("   Agrega GEMINI_API_KEY=tu_key en el archivo .env")

# Verificar Qwen como respaldo
print("\n" + "="*60)
print("VERIFICANDO RESPALDO: QWEN")
print("="*60)

qwen_key = os.getenv("QWEN_API_KEY")
if qwen_key and qwen_key != "tu_api_key_aqui":
    print("OK: API Key de Qwen configurada")
    print("   (Se puede usar como alternativa si Gemini tiene cuota limitada)")
else:
    print("WARN: Qwen no configurado")
    print("   Si Gemini tiene cuotas muy bajas, considera configurar Qwen")

print("\n" + "="*60)
print("GUARDANDO CONFIGURACION...")

# Guardar diagnóstico
with open("diagnostico_modelos.json", "w") as f:
    json.dump(resultados, f, indent=2)

print("OK: Diagnostico guardado en: diagnostico_modelos.json")
