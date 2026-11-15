from pipeline_limpieza import procesar_texto

def test_procesar_texto_normaliza_mayusculas_y_puntuacion():
    resultado = procesar_texto(" ¡¡La Tierra tiene 4600 millones de años!.")
    assert resultado == ["la", "tierra", "tiene", "4600", "millones", "de", "años"]

def test_procesar_texto_solo_puntuacion_devuelve_lista_vacia(): 
    resultado = procesar_texto("¡¡¡...!!!")  
    assert resultado == [] 