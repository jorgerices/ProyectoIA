import os
import requests
from dotenv import load_dotenv

import time

import json
import re

load_dotenv()

#Constantes
MODELO = "gemini-3.5-flash-lite"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

#Función para crear la solicitud
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

#Función envía la petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body, timeout=30)
    except requests.exceptions.ConnectionError:
        raise RuntimeError("No se pudo conectar con el servicio. Intenta de nuevo en unos momentos.")
    except requests.exceptions.Timeout:
        raise TimeoutError("Se agotó el tiempo. Intenta de nuevo en unos momentos.")

    if respuesta.status_code in(401, 403):
        raise ValueError("Credencial inválida o sin permiso. Revisa tu GEMINI_API_KEY")
    if respuesta.status_code >= 500:
        raise TimeoutError("El proveedor no pudo procesar la petición. Hay que esperar y reintentar")
    if respuesta.status_code == 429:
        segundos = respuesta.headers.get("Retry-After")
        mensaje = f"Límite excedido. Reintentar en {segundos}s" if segundos else "Límite excedido."
        raise TimeoutError(mensaje)
    
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
    url, body = armar_peticion(MODELO, pregunta, system_instruction, response_schema)

    inicio = time.perf_counter() #Empezar el contador

    datos = enviar_peticion(url, body)

    fin = time.perf_counter() #Terminar el contador
    latencia = fin - inicio
    print(f"Tiempo de respuesta: {latencia:.2f} segundos")

    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"El costo de la solicitud es: ${costo:.6f} USD")
    texto = extraer_texto(datos)
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
    costo = (tokens_entrada * precio_entrada) + ((tokens_salida + tokens_razonamiento) * precio_salida)
    return costo
    
def parsear_respuesta_json(texto, claves_requeridas=None):
    
    texto_limpio = texto.strip()
    texto_limpio = re.sub(r"^```(?:json)?\s*", "", texto_limpio)
    texto_limpio = re.sub(r"\s*```$", "", texto_limpio)
    
    try:
        datos = json.loads(texto_limpio)
    except json.JSONDecodeError:
        raise ValueError("La respuesta del modelo no es JSON válido")

    if  claves_requeridas:
        faltantes = [clave for clave in claves_requeridas if clave not in datos]
        if faltantes:
            raise ValueError("La respuesta del modelo no tiene la estructura esperada.")
    return datos

if __name__ == "__main__":
    for i in range(15):
        print(f"\n-- Intento {i+1} ---")
        try:
            print(obtener_dato_de_prueba("Confirma en una frase corta que la conexión con la API de Gemini está funcionando"))
        except TimeoutError as error:
            print(f"Límite alcanzado: {error}. Esperando 10 segundos adicionales...")
            time.sleep(10) #Espera 3 segundos antes de la siguiente petición
        except (ValueError, RuntimeError) as error:
            print(f"No se pudo completar la operación: ", error)