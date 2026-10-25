FORMATO = (
    "Devuelve únicamente un objeto JSON válido, sin texto adicional ni Markdown. Cada STRING no debe superar las 10 palabras"
)

BANCO_DE_PROMPT = [
    {
        "nombre": "verificador_epp_terreno",
        "system_instruction": FORMATO + (
            "Eres un supervisor de seguridad minera. Evalúa si el equipo de protección personal (EPP) declarado por el trabajador es adecuado para la tarea que está realizando y señala qué falta."
            ),
        "ejemplo_usuario": (
            "Tarea: corte de testigos de sondaje con sierra diamantina, "
            "EPP declarado: casco, guantes, zapatos de seguridad."
            ),
        "claves_esperadas": [
            "cumple_epp",
            "epp_faltante"
            ],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "cumple_epp": {"type": "BOOLEAN"},
                "epp_faltante": {"type": "STRING"}
            },
            "required": [
                "cumple_epp",
                "epp_faltante"
            ]
        }
    },
    
    {
        "nombre": "seguridad_posicionamiento_terreno",
        "system_instruction": FORMATO + (
            "Eres un supervisor de seguridad minera en terreno geológico. Evalúa si la posición elegida por el estudiante para mapear un afloramiento o banco de explotación es segura o viola protocolos frente a la caída de rocas."
            ),
        "ejemplo_usuario": (
            "¿Es una posición segura para mapear, medir una diaclasa con la brújula justo en el pie del banco de 15 metros, pegado a la pared bajo una visera rocosa, usando casco y chaleco reflectante?"
            ),
        "claves_esperadas": [
            "posicion_segura",
            "riesgo_operativo"
            ],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "posicion_segura": {"type": "BOOLEAN"},
                "riesgo_operativo": {"type": "STRING"}
            },
            "required": [
                "posicion_segura",
                "riesgo_operativo"
            ]
        }
    },

    {
        "nombre": "clasificador_zona_mineralizacion",
        "system_instruction": FORMATO + (
            "Eres un geólogo de mina en yacimientos de tipo pórfido cuprífero. Evalúa la interpretación del estudiante sobre si la asociación mineral observada corresponde a la zona supérgena (óxidos/enriquecimiento) o hipógena (primaria)."
            ),
        "ejemplo_usuario": (
            "Encontré abundantes vetillas de cuarzo con calcopirita, bornita diseminada y anhidrita en profundidad. "
            "¿Puedo reportar este tramo como parte de la zona de enriquecimiento secundario?"
            ),
        "claves_esperadas": [
            "interpretacion_correcta",
            "zona_mineral"
            ],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "interpretacion_correcta": {"type": "BOOLEAN"},
                "zona_mineral": {"type": "STRING"}
            },
            "required": [
                "interpretacion_correcta",
                "zona_mineral"
            ]
        }
    },
    {
        "nombre": "validador_criterio_textural",
        "system_instruction": FORMATO + (
            "Eres un tutor experto en petrología. Evalúa la clasificación de una roca propuesta por el estudiante analizando su textura, tamaño de grano y mineralogía, indicando si su razonamiento es correcto y cuál es el criterio diagnóstico de reconocimiento de la roca en cuestión. "
            "De errar en la clasificación de la roca, identifica el tipo de error cometido por el estudiante y formula una pregunta o guía socrática orientada a descubrir el nombre de la roca, sin darle realmente el nombre de la roca. "
            "De acertar en la clasificación de la roca, redacta un refuerzo técnico que consolide el criterio aplicado y devuelve 'Ninguno' en la clave 'error_conceptual'. "
            ),
        "ejemplo_usuario": (
            "En un testigo de sondaje observo fenocristales de plagioclasa y biotita inmersos en una matriz o masa fundamental microcristalina a vítrea. "
            "Como contiene cuarzo, plagioclasa y biotita, ¿es correcto clasificarla como granodiorita?"
            ),
        "claves_esperadas": [
            "clasificacion_correcta",
            "textura_dominante",
            "ambiente_formacion",
            "error_conceptual",
            "andamiaje_pedagogico"
            ],
        "response_schema": {
            "type": "OBJECT",
            "properties": {
                "clasificacion_correcta": {"type": "BOOLEAN"},
                "textura_dominante": {"type": "STRING"},
                "ambiente_formacion": {"type": "STRING"},
                "error_conceptual": {"type": "STRING"},
                "andamiaje_pedagogico": {"type": "STRING"}
            },
            "required": [
                "clasificacion_correcta",
                "textura_dominante",
                "ambiente_formacion",
                "error_conceptual",
                "andamiaje_pedagogico"
            ],
        }
    },
]