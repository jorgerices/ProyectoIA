from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI #Modelo
from langchain_core.prompts import PromptTemplate #Plantilla -> Prompt dinámico
from langchain_core.output_parsers import StrOutputParser #Parsea la respuesta y la transforma en solo textos
from langchain_core.runnables import (RunnableBranch, RunnablePassthrough, RunnableLambda) #Bifurcaciones/Branches/Ramificaciones

import logging #Generar un archivo de log con los errores que se presenten

logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s", #2026-11-04 16:40 [WARNING] main: No se pudo ejecutar x
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="error.log",
    filemode="a", #Agrega al final del archivo la nueva línea
    encoding="utf-8",
    force=True
)
logger = logging.getLogger(__name__)

load_dotenv()

modelo = ChatGoogleGenerativeAI(model="gemini-3.6-flash")

plantilla_clasificacion = PromptTemplate.from_template(
    "Clasifica el siguiente mensaje de soporte en una sola palabra: "
    "pregunta, queja o sugerencia. Responde solo con esa palabra. \n\n {mensaje}"
)

def construir_paso_clasificacion(modelo_actual=modelo):
    return (
        plantilla_clasificacion
        | modelo_actual
        | StrOutputParser()
        | (lambda texto: texto.strip().lower())
    )

paso_clasificacion = construir_paso_clasificacion(modelo)

# mensaje_prueba = "Dame el nombre de tu creador."

# clasificacion = paso_clasificacion.invoke(
#     {"mensaje": mensaje_prueba}
# )

# print(clasificacion)

cadena_pregunta = (
    PromptTemplate.from_template("Responde esta pregunta técnica con precisión: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_queja = (
    PromptTemplate.from_template("Responde esta queja con empatía, reconociendo el problema antes de ofrecer una solución: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

cadena_sugerencia = (
    PromptTemplate.from_template("Agradece esta sugerencia y explica cómo se evaluará dentro del producto: \n\n {mensaje}")
    | modelo
    | StrOutputParser()
)

#Fallback: cadena de respaldo. Captura las caídas de mi LLM (RateLimitError, 401, APIConnectionError, respuestas vacías)

def fallback_con_log(x):
    error = x.get("error") if isinstance(x, dict) else None
    logger.warning("Cadena principal falló. Activando respuesta genérica, Error: %s", error)
    return "Gracias por tu mensaje. Un miembro de nuestro equipo te va a responder pronto."

respuesta_generica = RunnableLambda(
    fallback_con_log
)

def construir_cadena_queja_segura(cadena_queja):
    return cadena_queja.with_fallbacks([respuesta_generica])

cadena_queja_segura = construir_cadena_queja_segura(cadena_queja)

#Sintaxis RunnableBranch
# caminos = RunnableBranch(
#     (condicion_1, rama_1), #if
#     (condicion_2, rama_2), #elif
#     (condicion_3, rama_3), #elif
#     rama_por_defecto #else
# ) #Cada condicion debe ser una función; suele ser un lambda

#x = {"clasificacion": "queja", "mensaje": "Mi teléfono no funciona"}
bifurcacion = RunnableBranch(
    (lambda x: x["clasificacion"] == "queja", cadena_queja_segura), #if x["clasificacion"] == "queja": cadena_queja
    (lambda x: x["clasificacion"] == "sugerencia", cadena_sugerencia), #elif x["clasificacion"] == "sugerencia": cadena_sugerencia
    cadena_pregunta #else: cadena_pregunta
)

def construir_cadena_con_enrutamiento(
    paso_clasificacion=paso_clasificacion,
    cadena_queja=cadena_queja_segura,
    cadena_sugerencia=cadena_sugerencia,
    cadena_pregunta=cadena_pregunta,
):
    bifurcacion_actual = RunnableBranch(
        (lambda x: x["clasificacion"] == "queja", cadena_queja),
        (lambda x: x["clasificacion"] == "sugerencia", cadena_sugerencia),
        cadena_pregunta
    )
    return (
        RunnablePassthrough.assign(clasificacion=paso_clasificacion)
        | bifurcacion_actual
    )

cadena_con_enrutamiento = construir_cadena_con_enrutamiento()

cadena_robusta = cadena_con_enrutamiento.with_fallbacks([respuesta_generica], exception_key="error")

def procesar_mensaje_seguro(cadena, mensaje):
    try:
        return cadena.invoke({"mensaje": mensaje})
    except Exception as error:
        print(f"Error procesando mensaje: {error}")
        logger.error("Error procesando mensaje: %s", error)
        return (
            "No pudimos procesar tu mensaje en este "
            "momento. Intenta de nuevo más tarde."
        )

if __name__ == "__main__": #Solamente ejecuta el siguiente bloque de código si la ejecución es directa del archivo. NO EJECUTES si es import
    mensaje = "Llevo varios días sin poder entrar a mi cuenta."
    print(procesar_mensaje_seguro(cadena_robusta, mensaje))