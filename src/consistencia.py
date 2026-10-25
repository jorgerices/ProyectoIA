import json
import time
from prompts.banco import BANCO_DE_PROMPT
from consumir_gemini import armar_peticion, enviar_peticion, extraer_texto, parsear_respuesta_json

registro = {}

try:

    for prompt in BANCO_DE_PROMPT:
        exitos = 0
        intentos = 3
        for intento in range(intentos):
            url, body = armar_peticion("gemini-3.5-flash-lite", prompt["ejemplo_usuario"], prompt["system_instruction"], prompt["response_schema"])
            respuesta = enviar_peticion(url, body)
            texto = extraer_texto(respuesta)
            try:
                datos = parsear_respuesta_json(texto, prompt["claves_esperadas"])
                exitos += 1
            except ValueError as error:
                print(f"Error en el intento {intento + 1} para el prompt: {error}")
            time.sleep(5)  # Esperar un segundo entre intentos para evitar sobrecarga
        print(f"{prompt['nombre']}: tuvo {exitos}/{intentos} respuestas exitosas.")            
        registro[prompt["nombre"]] = {"exitos": exitos, "intentos": intentos}
    #cuando termine de recorrer todos los prompts, imprimir el registro final
    with open("src/prompts/registro_resultados.json", "w", encoding="utf-8") as archivo:
        json.dump(registro, archivo, indent=2, ensure_ascii=False)

except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación", error)