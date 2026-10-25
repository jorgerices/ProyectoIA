# Decisión de arquitectura: elección de modelo

Fecha de la comparación: Sábado 24 de Octubre del 2026
Nombre de la miniaplicación: "Motor de simulación operativa para certificar competencias (para educación técnico-profesional y empresas)"
  
## Modelo elegido

Elegí el modelo: Gemini 3.6 Flash

Mi miniaplicación sirve para: Simular escenarios operativos y, a través de preguntas situadas, certificar competencias laborales que sean requeridas en el perfil de egreso de instituciones de educación técnico-profesional y capacitaciones de inducción laboral.

Los requisitos que necesito cumplir son:

* Requisito uno: ser estable.
* Requisito dos: ser rápido.
* Requisito tres: tener menor costo.
  
## Diagrama de arquitectura

[Diagrama de Arquitectura] - (docs/diagrama_arquitectura.png)
  
## Comparación de candidatos

- Estas son las preguntas y condiciones con las cuales se midieron ambos modelos:

* Preguntas y/o condiciones:

1. Estabilidad
2. Velocidad
3. Costo

RESUMEN gemini-3.1-flash-lite:
Peticiones exitosas: 3 de 4
Latencia promedio: 11.97 segundos
Costo acumulado: $0.000104 USD

RESUMEN gemini-3.6-flash:
Peticiones exitosas: 4 de 4
Latencia promedio: 7.44 segundos
Costo acumulado: $0.000393 USD

RESUMEN gemini-3.8-flash:
Peticiones exitosas: 1 de 4
Latencia promedio: 13.52 segundos
Costo acumulado: $0.003455 USD

Fuente de las tarifas:
<https://ai.google.dev/gemini-api/docs/pricing?hl=es-419#standard_1>

Observación sobre las pruebas:
El modelo 3.1 Flash lite presentó 3/4 solicitudes exitosas, mientras que el modelo 3.8 Flash solo 1/4.

## Justificación

Elegimos el modelo Gemini 3.6 Flash porque para nuestra aplicación es más estable y rápida.
Lo que observé en las pruebas fue que todas las peticiones fueron exiitosas y la latencia fue menor en ese modelo.
El criterio más relevante para mi decisión fue estabilidad y latencia.
Una limitación que encontré en mi elección fue el costo.
  
## Alternativa descartada y por qué

Descarté los modelos 3.1 Flash lite y 3.8 Flash porque presentaron menos solicitudes exitosas y la latencia fue mayor.