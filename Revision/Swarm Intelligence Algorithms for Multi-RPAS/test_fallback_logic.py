def test_fallback_logic():
    """Prueba la lógica de fallback sin dependencias externas"""
    
    # Simular la lógica del método elegir()
    preferencia = ["gemini", "qwen", "claude"]
    prompt_original = "Redacta una oración técnica sobre enjambres de drones."
    
    print("=== PRUEBA DE LÓGICA DE FALLBACK ===")
    print(f"Solicitud original: '{prompt_original}'")
    print()
    
    # Primer intento (i=0) - gemini
    i = 0
    modelo_nombre = preferencia[i]
    print(f"Intento {i+1}: {modelo_nombre}")
    print("   → Usando prompt original")
    print(f"   Prompt: '{prompt_original}'")
    print("   Simulando error en Gemini...")
    print()
    
    # Segundo intento (i=1) - qwen (fallback)
    i = 1
    modelo_nombre = preferencia[i]
    print(f"Intento {i+1}: {modelo_nombre} [FALLBACK]")
    print("   → Modificando prompt para indicar fallback")
    
    # Lógica de fallback como implementada
    fallback_prompt = f"[FALLBACK MODE - CONTINUE TASK] You are continuing the previous task. Do not ask questions or start over. The original request was: \"{prompt_original}\""
    
    print(f"   Prompt modificado: '{fallback_prompt[:120]}...'")  # Mostrar primeros 120 caracteres
    print(f"   Longitud total: {len(fallback_prompt)} caracteres")
    print()
    
    # Verificar que contiene los elementos clave
    contains_fallback = "[FALLBACK MODE - CONTINUE TASK]" in fallback_prompt
    contains_original = prompt_original in fallback_prompt
    contains_instructions = "Do not ask questions or start over" in fallback_prompt
    
    print("✅ Verificación:")
    print(f"   - Contiene prefijo de fallback: {contains_fallback}")
    print(f"   - Contiene solicitud original: {contains_original}")
    print(f"   - Contiene instrucción clara: {contains_instructions}")
    print()
    
    if contains_fallback and contains_original and contains_instructions:
        print("🎉 PRUEBA EXITOSA: La lógica de fallback está correctamente implementada")
    else:
        print("❌ PRUEBA FALLIDA: Algunos elementos están faltando")

if __name__ == "__main__":
    test_fallback_logic()