import os
import requests
from dotenv import load_dotenv

load_dotenv()

#constantes
MODELO = "gemini-flash-latest"
URL_BASE = "https://generativelanguage.googleapis.com/v1beta/models/"
API_KEY = os.getenv("GEMINI_API_KEY")

#función para crear la solicitud
def armar_peticion(pregunta):
    url = f"{URL_BASE}{MODELO}:generateContent?key={API_KEY}"    
    body = {"contents": [{"parts": [{"text": pregunta}]}]}
    return url, body

#función envía la petición
def enviar_peticion(url, body):
    try:
        respuesta = requests.post(url, json=body)
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


def obtener_dato_de_prueba(pregunta):
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    costo = calcular_costo(datos, 0.00000075, 0.00000375)
    print(f"El costo de la solicitud es: ${costo:.6f} USD")
    return extraer_texto(datos)

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
    
try:
    print(obtener_dato_de_prueba("Confirma en una frase corta que la conexión con la API de Gemini está funcionando"))
except (ValueError, RuntimeError) as error:
    print("No se pudo completar la operación: ", error)

