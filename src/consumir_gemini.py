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
    respuesta = requests.post(url, json=body)
    return respuesta.json()

#función procesa y extrae dato
def extraer_texto(datos):
    return datos["candidates"][0]["content"]["parts"][0]["text"]    

def obtener_dato_de_prueba(pregunta):
    url, body = armar_peticion(pregunta)
    datos = enviar_peticion(url, body)
    return extraer_texto(datos)

print(obtener_dato_de_prueba("Confirma en una frase corta que esta conexión funciona"))

#def obtener_dato_de_prueba(pregunta):
#    api_key = os.getenv("GEMINI_API_KEY")
#    modelo = "gemini-flash-latest"
#
#    url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
#    }
#    body = {
#        "contents": [
#        {
#            "parts": [
#            {
#                "text": pregunta
#            }
#            ]
#        }
#        ]
#    }
#
#    respuesta = requests.post(url, json=body)
#    print(respuesta)
#    datos = respuesta.json()
#    return datos["candidates"][0]["content"]["parts"][0]["text"]
#
#print(obtener_dato_de_prueba("Confirma en una frase corta que la conexión con la API de Gemini está funcionando"))