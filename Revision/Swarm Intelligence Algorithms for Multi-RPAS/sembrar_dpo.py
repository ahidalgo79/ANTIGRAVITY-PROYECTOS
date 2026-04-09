from dpo_learning import DPOLearningLoop

def sembrar():
    dpo = DPOLearningLoop()
    
    # Registro de una preferencia manual previa (Simulación de aprendizaje)
    consulta_simulada = "Redacta un párrafo sobre algoritmos de enjambre en drones"
    original = "El PSO es un algoritmo común para UAVs (Ait Saadi, 2021)."
    corregida = "La Optimización por Enjambre de Partículas (PSO, por sus siglas en inglés) constituye uno de los enfoques metaheurísticos más robustos para la navegación de UAVs, permitiendo una convergencia eficiente en espacios de búsqueda tridimensionales (Ait Saadi et al., 2021; Yu et al., 2021)."
    motivo = "Preferencia por usar el nombre completo al inicio y citación múltiple detallada."
    
    print(f"\n[DPO] Sembrando corrección de ejemplo...")
    dpo.registrar_feedback(consulta_simulada, original, corregida, motivo)
    print("[OK] Semilla registrada en dpo_feedback.json")

if __name__ == "__main__":
    sembrar()
