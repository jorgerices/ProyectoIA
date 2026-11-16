from unittest.mock import MagicMock
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableLambda

from src.enrutamiento import (
    construir_paso_clasificacion,
    construir_cadena_con_enrutamiento,
    construir_cadena_queja_segura,
    procesar_mensaje_seguro,
)


# ================= TESTS CLASIFICACIÓN =================

def test_clasificacion_normaliza_antes_de_comparar():
    modelo_falso = MagicMock()
    modelo_falso.return_value = AIMessage(content=" Queja \n")

    resultado = construir_paso_clasificacion(modelo_falso).invoke(
        {"mensaje": "algo salió mal"}
    )

    assert resultado == "queja"


# ================= TESTS ENRUTAMIENTO =================

def test_enrutamiento_va_a_cadena_queja():
    clasificacion_falsa = RunnableLambda(lambda _: "queja")
    cadena_queja_falsa = RunnableLambda(lambda _: "respuesta_queja")
    cadena_sugerencia_falsa = RunnableLambda(lambda _: "respuesta_sugerencia")
    cadena_pregunta_falsa = RunnableLambda(lambda _: "respuesta_pregunta")

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
        cadena_queja=cadena_queja_falsa,
        cadena_sugerencia=cadena_sugerencia_falsa,
        cadena_pregunta=cadena_pregunta_falsa,
    )

    resultado = cadena.invoke({"mensaje": "no funciona la app"})
    assert resultado == "respuesta_queja"


def test_enrutamiento_va_a_cadena_sugerencia():
    clasificacion_falsa = RunnableLambda(lambda _: "sugerencia")
    cadena_queja_falsa = RunnableLambda(lambda _: "respuesta_queja")
    cadena_sugerencia_falsa = RunnableLambda(lambda _: "respuesta_sugerencia")
    cadena_pregunta_falsa = RunnableLambda(lambda _: "respuesta_pregunta")

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
        cadena_queja=cadena_queja_falsa,
        cadena_sugerencia=cadena_sugerencia_falsa,
        cadena_pregunta=cadena_pregunta_falsa,
    )

    resultado = cadena.invoke({"mensaje": "agreguen modo oscuro"})
    assert resultado == "respuesta_sugerencia"


def test_enrutamiento_va_a_cadena_pregunta():
    clasificacion_falsa = RunnableLambda(lambda _: "pregunta")
    cadena_queja_falsa = RunnableLambda(lambda _: "respuesta_queja")
    cadena_sugerencia_falsa = RunnableLambda(lambda _: "respuesta_sugerencia")
    cadena_pregunta_falsa = RunnableLambda(lambda _: "respuesta_pregunta")

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
        cadena_queja=cadena_queja_falsa,
        cadena_sugerencia=cadena_sugerencia_falsa,
        cadena_pregunta=cadena_pregunta_falsa,
    )

    resultado = cadena.invoke({"mensaje": "¿cómo recupero mi clave?"})
    assert resultado == "respuesta_pregunta"


def test_enrutamiento_usa_default_ante_categoria_desconocida():
    clasificacion_falsa = RunnableLambda(lambda _: "otro_no_reconocido")
    cadena_queja_falsa = RunnableLambda(lambda _: "respuesta_queja")
    cadena_sugerencia_falsa = RunnableLambda(lambda _: "respuesta_sugerencia")
    cadena_pregunta_falsa = RunnableLambda(lambda _: "respuesta_por_defecto")

    cadena = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
        cadena_queja=cadena_queja_falsa,
        cadena_sugerencia=cadena_sugerencia_falsa,
        cadena_pregunta=cadena_pregunta_falsa,
    )

    resultado = cadena.invoke({"mensaje": "hola"})
    assert resultado == "respuesta_por_defecto"


# ================= TESTS MANEJO DE ERRORES Y FALLBACKS =================

def test_cadena_queja_usa_fallback_ante_fallo_del_modelo():
    def fallar_a_proposito(x):
        raise ConnectionError("simulado")

    cadena_queja_falsa = RunnableLambda(fallar_a_proposito)
    cadena_queja_segura = construir_cadena_queja_segura(
        cadena_queja_falsa
    )

    resultado = cadena_queja_segura.invoke(
        {"mensaje": "esto no funciona"}
    )

    assert "equipo" in resultado.lower()


def test_procesar_mensaje_seguro_no_propaga_excepciones():
    clasificacion_falsa = MagicMock()
    clasificacion_falsa.side_effect = ConnectionError(
        "simulado"
    )

    cadena_falsa = construir_cadena_con_enrutamiento(
        paso_clasificacion=clasificacion_falsa,
    )

    resultado = procesar_mensaje_seguro(
        cadena_falsa, "mensaje de prueba"
    )

    assert "no pudimos procesar" in resultado.lower()