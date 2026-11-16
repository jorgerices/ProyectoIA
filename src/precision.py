from collections import Counter
import json
from pathlib import Path

try:
    from .pipeline_limpieza import procesar_texto
    from .cliente import consultar_modelo
except ImportError:
    from pipeline_limpieza import procesar_texto
    from cliente import consultar_modelo

def contar_coincidencias(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> int:
    """Cuenta las coincidencias entre referencia y respuesta."""
    conteo_referencia = Counter(tokens_referencia)
    conteo_respuesta = Counter(tokens_respuesta)
    interseccion = conteo_referencia & conteo_respuesta
    return sum(interseccion.values())

def calcular_precision_cobertura_f1(
    tokens_referencia: list[str],
    tokens_respuesta: list[str],
) -> dict[str, float]:
    """Calcula precisión, cobertura y F1 de dos listas de tokens."""
    coincidencias = contar_coincidencias(
        tokens_referencia, tokens_respuesta
    )

    if not tokens_respuesta or not tokens_referencia:
        return {"precision": 0.0, "cobertura": 0.0, "f1": 0.0}

    precision = coincidencias / len(tokens_respuesta)
    cobertura = coincidencias / len(tokens_referencia)

    if precision + cobertura == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * cobertura / (precision + cobertura)

    resultado = {
        "precision": precision,
        "cobertura": cobertura,
        "f1": f1,
    }

    return resultado

def calcular_metricas(texto_referencia, texto_respuesta):

    tokens_referencia = procesar_texto(texto_referencia)

    tokens_respuesta = procesar_texto(texto_respuesta)

    return calcular_precision_cobertura_f1(
        tokens_referencia, tokens_respuesta
    )

casos = [

    (
        "¿Qué es la geología?",
        "La geología es la ciencia que estudia la Tierra y sus procesos.",
    ),

    (
        "¿Por qué es importante la geología para las carreras de técnico e ingeniería en minas?",
        "La geología es fundamental para la exploración y explotación de recursos minerales, así como para la planificación de proyectos mineros."
    ),

    (
        "¿Qué rol tiene el geólogo en una faena minera?",
        "Modelar el yacimiento, estimar recursos y guiar la extracción segura y eficiente"
    ),

    (
        "¿Qué herramientas se utilizan en la etapa de prospección geológica?",
        "Se utilizan mapas geológicos, brújulas, GPS, martillos geológicos y software de modelado."
    ),

    (
        "¿Qué diferencia hay entre un mineral y una roca?",
        "Un mineral es una sustancia cristalina natural, inorgánica, sólida con características físicas y químicas determinadas, y una roca es un agregado de uno o más minerales."
    ),

    (
        "Con respecto a su origen, ¿cómo puedo diferenciar entre rocas ígneas, metamórficas y sedimentarias?",
        "Las rocas ígneas se forman por solidificación de un magma, las metamórficas se forman por transformación de rocas preexistentes bajo presión y temperatura, y las sedimentarias se forman por acumulación y litificación de sedimentos."
    ),

    (
        "Con respecto a su textura, ¿cómo se diferencian rocas ígneas, metamórficas y sedimentarias?",
        "A grandes rasgos, las rocas ígneas tienen una textura granular, las metamórficas tienen una textura fibrosa o laminada, y las sedimentarias tienen una textura clástica."
    ),

    (
        "Explica la diferencia textural entre un pórfido y una roca fanerítica, e indica qué revela su historia de enfriamiento",
        "El pórfido presenta una textura porfídica con grandes fenocristales en una matriz de grano fino, lo que sugiere un enfriamiento en dos etapas: una cristalización lenta inicial en profundidad seguida de un ascenso rápido y enfriamento somero. El granito fanerítico muestra cristales uniformemente visibles a simple vista , reflejando un enfriamiento lento y continuo en una cámara magmática profunda."
    ),

    (
        "¿Qué diferencia geométrica y cinemática existe entre una falla normal y una falla inversa?",
        "La falla normal se genera por esfuerzos extensivos (tensión), donde le bloque colgante (hanging wall) se desliza hacia abajo respecto al bloque yacente (footwall). La falla inversa se produce por compresión tectónica, provocando que el bloque colgante ascienda respecto al yacente."
    ),

    (
        "¿Cuál es la diferencia fundamental entre el magma y la lava?",
        "El magma es roca fundida que se encuentra bajo la superficie de la Tierra, mientras que la lava es magma que ya ha emergido a la superficie a través de un volcán o una fisura."
    ),

    (
        "¿Qué es la meteorización?",
        "Es el proceso físico, químico o biológico mediante el cual las rocas expuestas a la atmósfera se fragmentan o descomponen in situ debido al contacto con el agua, el aire y los organismos, sin que los materiales sean transportados."
    ),

    (
        "¿Cómo se produce un terremoto?",
        "Por la liberación repentina de energía acumulada a lo largo de una falla geológica debido al movimiento continuo de las placas tectónicas."
    ),

    (
        "¿Qué tipos de límites existen entre las placas tectónicas?",
        "Existen tres tipos principales de límites: divergentes (las placas se separan y generan nueva corteza), convergentes (las placas chocan provocando subducción o cordilleras) y transformantes (las placas se deslizan lateralmente entre sí)."
    ),

    (
        "¿Cómo se diferencian geoquímicamente los magmas generados en arcos volcánicos de subducción de aquellos formados en dorsales oceánicas",
        "Los magmas de arco muestran un enriquecimiento selectivo en elementos litófilos de radio iónico grande (LILE) y un marcado empobrecimiento en elementos de alta intensidad de campo (HFSE); en contraste, los basaltos de dorsal (MORB) derivan de la fusión un manto superior empobrecido sin componente de slab, con patrones planos o depletados en elementos incompatibles sin anomalías negativas de Nb-Ta."
    ),

    (
        "¿Qué diferencia fundamental existe entre una cuenca de antearco y una cuenca de retroarco",
        "La cuenca de antearco se ubica entre la fosa oceánica y el arco magmático y acumula sedimentos marinos asociados al prisma de acreción; la cuenca de retroarco se ubica detrás del arco magmático respecto a la fosa y suele formarse en regímenes extensivos provocado por el retroceso de la fosa"
    ),

    (
        "¿Cómo se forman las lavas almohadilladas?",
        "Se forman cuando el magma basáltico entra en erupción bajo el agua, típicamente en dorsales oceánicas. El contacto inmediato con el agua fría solidifica instantáneamente la superficie exterior creando una corteza curvadsa con forma de almohada."
    ),

    (
        "¿Cómo se interpreta la presencia de estratificación cruzada en rocas sedimentarias clásticas?",
        "Indica la migración de formas de lecho (como dunas o barras subacuáticas/eólicas) bajo la acción de un flujo unidireccional. Permite deducir la dirección de las paleocorrientes y definir el ambiente de depositación."
    ),

    (
        "¿Qué representa una discordancia angular en una sección o columna estratigráfica?",
        "Representa una superficie de erosión que trunca capas sedimentarias inclinadas o plegadas, sobre las cuales se depositaron horizontalmente sedimentos más jóvenes. Sugiere un hito temporal prolongado y una fase de deformación tectónica."
    ),

    (
        "¿Qué características geomorfológicas permiten distinguir un valle glaciar maduro de un valle fluvial?",
        "El valle glaciar presenta una sección transversal en forma de 'U', caracterizada por fondo plano y laderas abruptas debido a la abrasión y sobreexcavación del hielo. El valle fluvial presenta un perfil en 'V' esculpido principalmente por el agua."
    ),

    (
        "¿Cómo contrasta la dinámica eruptiva entre un magma basáltico y uno riolítico?",
        "El magma basáltico posee baja viscosidad y bajo contenido de sílice y volátiles, lo que propicia erupciones predominantemente efusivas (coladas de lava fluidas). El magma riolítico, rico en sílice y volátiles, presenta alta viscosidad, generando erupciones altamente explosivas con emisión de flujos piroclásticos."
    ),

]

raiz = Path(__file__).resolve().parents[1]
ruta_resultados = raiz / "resultados_metricas.json"

# Recupera las respuestas guardadas en una ejecución anterior.
if ruta_resultados.exists():
    with ruta_resultados.open(
        "r",
        encoding="utf-8"
    ) as archivo:
        resultados = json.load(archivo)
else:
    resultados = []

# Identifica los casos ya completados.
completados = {
    (caso["consulta"], caso["referencia"])
    for caso in resultados
}

for numero, (consulta, referencia) in enumerate(
    casos,
    start=1
):
    # Continúa sin repetir las consultas ya guardadas.
    if (consulta, referencia) in completados:
        print("Ya guardada:", consulta)
        continue

    try:
        respuesta = consultar_modelo(
            consulta,
            system_instruction=(
                "Responde en español con una definición breve, "
                "en una sola oración de máximo 15 palabras. "
                "Sin listas, ejemplos ni introducciones."
            )
        )

    except RuntimeError as error:
        print("\nSe detuvo la generación:", error)
        print(f"Respuestas guardadas: {len(resultados)}")
        break

    metricas = calcular_metricas(referencia, respuesta)

    resultados.append({
        "id": numero,
        "consulta": consulta,
        "referencia": referencia,
        "respuesta": respuesta,
        **metricas,
    })

    # Guarda inmediatamente después de cada respuesta.
    with ruta_resultados.open(
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            resultados,
            archivo,
            indent=2,
            ensure_ascii=False
        )

    completados.add((consulta, referencia))

    print("\nConsulta:", consulta)
    print("Respuesta:", respuesta)
    print("Métricas:", metricas)
    print(f"Guardadas: {len(resultados)}/{len(casos)}")

def resumir_metricas(resultados):
    if not resultados:
        return {
            "precision_promedio": 0,
            "cobertura_promedio": 0,
            "f1_promedio": 0,
        }
    n = len(resultados)
    return {
        "precision_promedio": sum(
            r["precision"] for r in resultados
        ) / n,
        "cobertura_promedio": sum(
            r["cobertura"] for r in resultados
        ) / n,
        "f1_promedio": sum(r["f1"] for r in resultados) / n,
    }
    
print("Promedios")
print(resumir_metricas(resultados))
    
peores_casos = sorted(resultados, key=lambda r: r["f1"])
muestra_para_revisar = peores_casos[:5] + peores_casos[-5:]

print("\n=== MUESTRA PARA REVISAR (5 peores y 5 mejores) ===")
for caso in muestra_para_revisar:
    print(f"\nID: {caso['id']} | F1: {caso['f1']:.4f}")
    print(f"Consulta:   {caso['consulta']}")
    print(f"Referencia: {caso['referencia']}")
    print(f"Respuesta:  {caso['respuesta']}")
    
    
# referencia = procesar_texto(
#     "Python es un lenguaje de programación interpretado."
# )

# texto_respuesta = consultar_modelo("¿Qué es Python?",
#                                    system_instruction="Responde en español con una definición breve, en una sola oración de máximo 15 palabras. Sin listas, ejemplos ni introducciones.")

# respuesta = procesar_texto(texto_respuesta)
# resultado = calcular_precision_cobertura_f1(referencia, respuesta)

# print("Respuesta:", texto_respuesta)
# print("Tokens de referencia:", len(referencia))
# print("Tokens de respuesta:", len(respuesta))
# print(resultado)