import consumir_gemini
import time

def evaluar_modelo(nombre_modelo, pregunta, precio_entrada, precio_salida, repeticiones=4):
    """
    Ejecuta 'repeticiones' veces la misma petición para un modelo específico.
    Calcula e imprime Latencia, Costo y Respuesta de cada intento,
    además del promedio de latencia al final.
    """
    print("=" * 70)
    print(f" EVALUANDO MODELO: {nombre_modelo}")
    print("=" * 70)
    
    latencias = []
    costos = []
    instruccion = "Eres un asistente amigable y respondes en máximo 2 palabras."

    for i in range(1, repeticiones + 1):
        print(f"\n--- Intento {i} de {repeticiones} ({nombre_modelo}) ---")
        
        try:
            # 1. Armar petición (Respetando el orden: modelo, pregunta, system_instruction)
            url, body = consumir_gemini.armar_peticion(
                modelo=nombre_modelo, 
                pregunta=pregunta, 
                system_instruction=instruccion
            )

            # 2. Medir latencia
            inicio = time.perf_counter()
            datos = consumir_gemini.enviar_peticion(url, body)
            fin = time.perf_counter()
            
            latencia = fin - inicio
            latencias.append(latencia)
            
            # 3. Calcular costo
            costo = consumir_gemini.calcular_costo(datos, precio_entrada, precio_salida)
            costos.append(costo)
            
            # 4. Extraer respuesta
            respuesta = consumir_gemini.extraer_texto(datos)
            
            # 5. Imprimir resultados de la petición actual
            print(f"Latencia:  {latencia:.2f} segundos")
            print(f"Costo:     ${costo:.6f} USD")
            print(f"Respuesta: {respuesta.strip()}")

        except (ValueError, RuntimeError, TimeoutError) as error:
            print(f"Error en el intento {i}: {error}")

        # Pausa de 5 segundos para evitar el error 429 (Límite excedido)
        time.sleep(5)

    # Resumen acumulado del modelo (solo si hubo al menos 1 intento exitoso)
    print("\n" + "-" * 40)
    print(f" RESUMEN {nombre_modelo}:")
    if latencias:
        latencia_promedio = sum(latencias) / len(latencias)
        costo_total = sum(costos)
        print(f" Peticiones exitosas: {len(latencias)} de {repeticiones}")
        print(f" Latencia promedio: {latencia_promedio:.2f} segundos")
        print(f" Costo acumulado: ${costo_total:.6f} USD")
    else:
        print(" No se pudo completar ninguna petición con éxito para este modelo.")
    print("-" * 40 + "\n")


pregunta_prueba = "Confirma la conexion"
modelos = [
    {
        "nombre": "gemini-3.6-flash",
        "precio_entrada": 0.00000010,
        "precio_salida": 0.00000030
    },
    {
        "nombre": "gemini-3.1-flash-lite",
        "precio_entrada": 0.00000075,
        "precio_salida": 0.00000375
    },
    {
        "nombre": "gemini-3.8-flash",
        "precio_entrada": 0.00000250,
        "precio_salida": 0.00001000
    }
]

if __name__ == "__main__":
    # Procesar los 3 modelos consecutivamente
    for config in modelos:
        evaluar_modelo(
            nombre_modelo=config["nombre"],
            pregunta=pregunta_prueba,
            precio_entrada=config["precio_entrada"],
            precio_salida=config["precio_salida"],
            repeticiones=4
        )