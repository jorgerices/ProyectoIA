import json
import os
import re
import requests
from dotenv import load_dotenv

import time

load_dotenv()

#constantes
MODELO = "gemini-3.6-flash"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

#función para crear la solicitud
def armar_peticion(modelo, pregunta, system_instruction, response_schema=None): #pregunta = "Confirma la conexión"
    if not pregunta:
        raise ValueError("La pregunta no puede estar vacía.")
    url = f"{URL_BASE}{modelo}:generateContent?key={API_KEY}"    
    body = {
            "systemInstruction": {"parts": [{"text": system_instruction}]},
            "contents": [{"parts": [{"text": pregunta}]}],    
        }

    if response_schema is not None:
        body["generationConfig"] = {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    
    return url, body

#función envía la petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos momentos.")
    except requests.exceptions.Timeout:
        raise RuntimeError("La solicitud ha tardado demasiado tiempo en completarse. Intenta de nuevo.")
    if respuesta.status_code != 200:
        raise RuntimeError(f"Error en la solicitud: {respuesta.status_code}")
        
    try:
        return respuesta.json()
    except requests.exceptions.JSONDecodeError:
        raise RuntimeError("La respuesta del servicio no es un JSON válido. Intenta de nuevo.")

#función procesa y extrae dato
def extraer_texto(datos): #Gemini
    try:
        return datos["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise RuntimeError("La estructura no recibe el texto generado en el lugar definido. Intenta de nuevo.")    


def obtener_dato_de_prueba(pregunta): #pregunta = "Confirma la conexión"
    
    response_schema = {
        "type": "OBJECT",
        "properties": {
            "categoria": {"type": "STRING"},
            "nivel": {"type": "NUMBER"}, 
        },
        "required": ["categoria", "nivel"]
    }
    
    system_instruction = "Eres un asistente amigable y respondes en máximo 2 palabras."
    #Eres un asistente de ingeniería automotriz, que responde a preguntas sobre fallas y errores de vehículos. Responde de manera clara y concisa, proporcionando soluciones prácticas y pasos a seguir para resolver problemas automotrices. Evita respuestas vagas o genéricas, y enfócate en brindar información útil y específica para ayudar al usuario a solucionar su problema.
    url, body = armar_peticion("gemini-3.6-flash",pregunta, system_instruction, response_schema)

    inicio = time.perf_counter() #Empezar el contador

    datos = enviar_peticion(url, body)

    fin = time.perf_counter() #Terminar el contador
    latencia = fin - inicio
    print(f"Tiempo de respuesta: {latencia:.2f} segundos")

    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"El costo de la solicitud es: ${costo:.6f} USD")
    texto = extraer_texto[datos]
    datos_formateados = parsear_respuesta_json(texto, claves_requeridas=["categoria", "nivel"])
    return datos_formateados

#def calcular_costo(datos: dict, precio_entrada: float, precio_Salida: float) -> float:
def calcular_costo(datos, precio_entrada, precio_salida):
    #datos = {dict... "usageMetadata"}
    uso = datos["usageMetadata"]
    '''
    uso: {
        "promptTokenCount": 15,
        "candidatesTokenCount": 684,
        "totalTokenCount": 1474,
        "promptTokensDetails": [
            {
                "modality": "TEXT",
                "tokenCount": 15
            }
        ],
        "thoughtsTokenCount": 775,
        "serviceTier": "standard"
    }
    '''
    tokens_entrada = uso["promptTokenCount"]
    tokens_salida = uso["candidatesTokenCount"]
    tokens_razonamiento = uso["thoughtsTokenCount"] #revisar si existe o no, si no existe, poner 0
    costo = ((tokens_entrada * precio_entrada) + (tokens_salida + tokens_razonamiento) * precio_salida)
    return costo
    
def parsear_respuesta_json(texto, claves_requeridas=None):
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("El texto no es un JSON válido.")
    if claves_requeridas:
        faltantes = [clave for clave in claves_requeridas if clave not in datos]
        if faltantes:
            raise ValueError["La respuesta del modelo no tiene la estructura esperada."]
    return datos

try:
    print(obtener_dato_de_prueba("Confirma en una frase corta que la conexión con la API de Gemini está funcionando"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación: ", error)

'''
Ejecute 4 veces la misma petición y ante cada una se calcule e imprima: latencia, costo, respuesta

Vuelvo a hacer lo mismo con un modelo distinto (3 modelos)

EL objetivo es que elijamos el mejor modelo para mi proyecto 

Prompt debe ser algo relacionado con mi proyecto
'''