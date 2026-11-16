# Límites de la métrica de evaluación

## Qué mide
Coincidencia léxica de palabras (tokens normalizados en minúsculas y sin puntuación) entre la respuesta generada y la referencia geológica, contando repeticiones mediante intersección de multiconjuntos (precisión, cobertura y F1).

## Modos de falla conocidos
- **Sinónimos y paráfrasis técnicas puntúan artificialmente bajo:** Respuestas geológicamente válidas que emplean términos equivalentes caen en falsos negativos. Ejemplo: consulta `"¿Qué representa una discordancia angular en una sección o columna estratigráfica?"`, `f1=0.2222`, la respuesta define correctamente la *"interrupción erosiva entre estratos antiguos inclinados y capas más recientes horizontales"*, pero pierde puntaje frente a *"superficie de erosión que trunca capas sedimentarias"*.
- **Asimetría de longitud entre el prompt (≤15 palabras) y referencias extensas:** La restricción de una oración de máximo 15 palabras trunca la cobertura en referencias de 30 a 45 palabras, incluso con precisión >0.85. Ejemplo: consulta `"¿Qué tipos de límites existen entre las placas tectónicas?"`, `f1=0.2609`, nombra los tres límites (*divergentes, convergentes y transformantes*) pero no cabe la descripción de cada uno.
- **Simplificaciones conceptuales u omisiones clave con F1 alto:** Compartir la estructura gramatical e inicio de frase infla el puntaje aunque falten condiciones técnicas esenciales. Ejemplo: consulta `"¿Qué diferencia hay entre un mineral y una roca?"`, `f1=0.6000`, define mineral solo como *"sustancia pura"*, omitiendo su carácter *natural, inorgánico, sólido y cristalino*; y en `"¿Cómo se produce un terremoto?"`, `f1=0.5714`, omite el concepto de *"falla geológica"*.

## Muestra revisada
10 casos: los 5 con menor F1 (`0.0800` a `0.2609`) y los 5 con mayor F1 (`0.4211` a `0.6667`), sobre 20 respuestas generadas el 2026-11-16.

## Recomendación de uso
Usar F1 solo para monitorear estabilidad en volumen cuando las referencias tengan una extensión similar al límite del prompt (10 a 15 palabras); revisar siempre a mano las preguntas con referencias largas (>25 palabras), enumeraciones de criterios técnicos (como la definición de mineral) y comparaciones geológicas.