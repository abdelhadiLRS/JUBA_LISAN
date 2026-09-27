"""Curated Spanish lesson seeds for the A2-C2 CEFR curriculum.

These authored seeds keep Spanish lessons language-specific when the LLM is
unavailable and provide grounded material to the lesson generator.
"""

from __future__ import annotations

from typing import Any


_SEEDS: dict[tuple[str, str, str], dict[str, Any]] = {
    ("A2", "a2-unit-1", "grammar"): {
        "title": "Pretérito indefinido para contar experiencias",
        "objective": "Narrar acciones pasadas y terminadas con el pretérito indefinido.",
        "grammar": ["preterito-indefinido-regular", "preterito-irregular", "marcadores-temporales"],
        "examples": ["Ayer fui al mercado.", "El sábado compramos los billetes.", "En 2024 viajé a Valencia."],
    },
    ("A2", "a2-unit-1", "vocabulary"): {
        "title": "Viajes y experiencias",
        "objective": "Hablar de viajes recientes y experiencias sencillas.",
        "words": [
            ("viaje", "desplazamiento a otro lugar", "El viaje duró tres horas."),
            ("billete", "documento para viajar", "Compré el billete ayer."),
            ("llegar", "alcanzar un lugar", "Llegamos a Madrid por la tarde."),
            ("visitar", "ir a un lugar para conocerlo", "Visitamos el museo."),
        ],
    },
    ("A2", "a2-unit-1", "reading"): {
        "title": "Un fin de semana en Valencia",
        "objective": "Identificar acciones principales en una narración breve.",
        "text": "El viernes llegué a Valencia con mi hermana. El sábado visitamos el centro, comimos paella y paseamos por el puerto. El domingo volvimos a casa después de desayunar.",
        "questions": ["¿Con quién viajó la persona?", "¿Qué comieron el sábado?"],
    },
    ("A2", "a2-unit-1", "listening"): {
        "title": "Una experiencia reciente",
        "objective": "Reconocer fechas, acciones y lugares en un relato oral.",
        "transcript": "Ayer fui al centro con unos amigos. Tomamos un café, visitamos una librería y volvimos a casa a las ocho.",
        "questions": ["¿Con quién fue al centro?", "¿A qué hora volvieron?"],
    },
    ("A2", "a2-unit-1", "speaking"): {
        "title": "Cuenta un día especial",
        "objective": "Contar una experiencia pasada con una secuencia clara.",
        "prompt": "Cuenta qué hiciste el último fin de semana.",
        "phrases": ["Primero...", "Después...", "Finalmente..."],
        "examples": ["Primero fui al centro, después comí con mis amigos y finalmente volví a casa."],
    },
    ("A2", "a2-unit-1", "writing"): {
        "title": "Mi último viaje",
        "objective": "Escribir una narración breve usando el pretérito indefinido.",
        "prompt": "Escribe 60-80 palabras sobre un viaje reciente.",
        "guidance": ["Incluye cuándo viajaste.", "Menciona dos actividades.", "Termina explicando cómo fue la experiencia."],
        "examples": ["El mes pasado viajé a Sevilla con mi familia. Visitamos el centro y probamos comida local."],
    },
    ("A2", "a2-unit-1", "review"): {
        "title": "Repaso de experiencias pasadas",
        "objective": "Consolidar el pretérito indefinido y los marcadores temporales.",
        "questions": ["Completa: Ayer ___ (ir) al cine.", "Escribe una frase con el año pasado."],
    },

    ("B1", "b1-unit-1", "grammar"): {
        "title": "Presente de subjuntivo: deseos y emociones",
        "objective": "Usar el subjuntivo después de deseos y expresiones emocionales.",
        "grammar": ["subjuntivo-presente", "expresiones-deseo", "emociones"],
        "examples": ["Quiero que vengas.", "Me alegra que estés aquí.", "Ojalá tengas suerte."],
    },
    ("B1", "b1-unit-1", "vocabulary"): {
        "title": "Deseos y emociones",
        "objective": "Expresar deseos, sentimientos y reacciones.",
        "words": [
            ("esperar", "desear que algo ocurra", "Espero que todo salga bien."),
            ("alegrarse", "sentir alegría", "Me alegro de que estés aquí."),
            ("preocupar", "causar inquietud", "Me preocupa que llegue tarde."),
            ("ojalá", "expresión de deseo", "Ojalá podamos ir."),
        ],
    },
    ("B1", "b1-unit-1", "reading"): {
        "title": "Un nuevo comienzo",
        "objective": "Comprender deseos y emociones expresados en un texto.",
        "text": "Laura empieza un nuevo trabajo y espera que sus compañeros la reciban bien. Le alegra que la empresa ofrezca formación y desea que el proyecto tenga buenos resultados.",
        "questions": ["¿Qué espera Laura de sus compañeros?", "¿Qué le alegra de la empresa?"],
    },
    ("B1", "b1-unit-1", "listening"): {
        "title": "Planes y deseos",
        "objective": "Identificar deseos y valoraciones en una conversación.",
        "transcript": "Espero que el curso sea útil. Me alegra que podamos practicar juntos y ojalá tengamos tiempo para hablar al final.",
        "questions": ["¿Qué espera la persona del curso?", "¿Qué desea para el final?"],
    },
    ("B1", "b1-unit-1", "speaking"): {
        "title": "Expresa tus deseos",
        "objective": "Hablar de planes y deseos usando el subjuntivo.",
        "prompt": "Habla de tres cosas que esperas que ocurran este año.",
        "phrases": ["Espero que...", "Me gustaría que...", "Ojalá..."],
        "examples": ["Espero que encuentre un buen trabajo y ojalá pueda viajar este verano."],
    },
    ("B1", "b1-unit-1", "writing"): {
        "title": "Un objetivo personal",
        "objective": "Escribir sobre un objetivo y las condiciones que deseas para conseguirlo.",
        "prompt": "Escribe 100-120 palabras sobre un objetivo personal o profesional.",
        "guidance": ["Explica tu objetivo.", "Usa al menos tres estructuras con subjuntivo.", "Incluye una reacción emocional."],
        "examples": ["Quiero que mi próximo proyecto sea útil. Espero que el equipo trabaje bien y me alegra que todos participen."],
    },
    ("B1", "b1-unit-1", "review"): {
        "title": "Repaso del subjuntivo",
        "objective": "Distinguir deseo, emoción y certeza en estructuras con que.",
        "questions": ["Completa: Espero que ___ (venir) mañana.", "Explica por qué usamos subjuntivo en 'Me alegra que estés aquí'."],
    },

    ("B2", "b2-unit-3", "grammar"): {
        "title": "Conectores para construir argumentos",
        "objective": "Organizar argumentos y expresar causa, contraste y consecuencia con precisión.",
        "grammar": ["conectores-avanzados", "cohesion-textual", "registro-formal"],
        "examples": ["Sin embargo, los resultados son limitados.", "Por lo tanto, conviene revisar el método.", "Aunque el coste sea alto, la medida puede ser útil."],
    },
    ("B2", "b2-unit-3", "vocabulary"): {
        "title": "Lenguaje académico y argumentativo",
        "objective": "Usar vocabulario para estructurar argumentos formales.",
        "words": [
            ("evidencia", "información que apoya una conclusión", "La evidencia disponible es limitada."),
            ("consecuencia", "resultado de una acción", "La medida tuvo una consecuencia inesperada."),
            ("planteamiento", "forma de presentar un problema", "El planteamiento requiere más datos."),
            ("matizar", "hacer una afirmación más precisa", "Conviene matizar esta conclusión."),
        ],
    },
    ("B2", "b2-unit-3", "reading"): {
        "title": "El trabajo híbrido",
        "objective": "Identificar tesis, argumentos y contraargumentos en un texto.",
        "text": "El trabajo híbrido ofrece flexibilidad y puede reducir los desplazamientos. Sin embargo, también exige una coordinación cuidadosa. Aunque algunos equipos funcionan bien a distancia, otros necesitan encuentros presenciales frecuentes para resolver problemas complejos.",
        "questions": ["¿Qué ventaja se menciona?", "¿Qué limitación presenta el texto?"],
    },
    ("B2", "b2-unit-3", "listening"): {
        "title": "Evaluar una propuesta",
        "objective": "Reconocer relaciones de causa, contraste y consecuencia en un discurso.",
        "transcript": "La propuesta puede reducir costes. Sin embargo, requiere una inversión inicial importante. Por lo tanto, antes de aplicarla conviene analizar los datos disponibles.",
        "questions": ["¿Qué ventaja tiene la propuesta?", "¿Qué recomienda hacer antes de aplicarla?"],
    },
    ("B2", "b2-unit-3", "speaking"): {
        "title": "Defiende una posición",
        "objective": "Presentar una opinión, conceder un punto y formular una conclusión.",
        "prompt": "Defiende una posición sobre el trabajo híbrido y responde a una objeción.",
        "phrases": ["Es cierto que...", "Sin embargo...", "Por lo tanto..."],
        "examples": ["Es cierto que la comunicación puede ser más difícil; sin embargo, una buena organización puede reducir ese problema."],
    },
    ("B2", "b2-unit-3", "writing"): {
        "title": "Texto argumentativo",
        "objective": "Redactar un texto coherente con tesis, argumentos y conclusión.",
        "prompt": "Escribe 200-250 palabras sobre una ventaja y una desventaja del trabajo híbrido.",
        "guidance": ["Formula una tesis.", "Incluye un contraargumento.", "Usa al menos cinco conectores.", "Concluye con una posición matizada."],
        "examples": ["El trabajo híbrido puede mejorar la flexibilidad, aunque sus beneficios dependen de la organización del equipo."],
    },
    ("B2", "b2-unit-3", "review"): {
        "title": "Repaso de coherencia textual",
        "objective": "Reforzar conectores, cohesión y registro formal.",
        "questions": ["Elige un conector de contraste adecuado.", "Reescribe una conclusión demasiado absoluta para hacerla más prudente."],
    },

    ("C1", "c1-unit-1", "grammar"): {
        "title": "Precisión y cautela en el análisis",
        "objective": "Formular conclusiones prudentes mediante estructuras de evidencia, posibilidad y concesión.",
        "grammar": ["subjuntivo-avanzado", "conectores-discursivos", "matizadores"],
        "examples": ["Los datos parecen indicar que...", "No puede descartarse que...", "Si bien los resultados son prometedores, conviene interpretarlos con cautela."],
    },
    ("C1", "c1-unit-1", "vocabulary"): {
        "title": "Investigación y análisis",
        "objective": "Usar léxico preciso para describir resultados, evidencia y limitaciones.",
        "words": [
            ("hallazgo", "resultado obtenido mediante investigación", "El principal hallazgo fue inesperado."),
            ("sesgo", "inclinación que afecta a una observación", "El estudio presenta un posible sesgo."),
            ("limitación", "factor que restringe una conclusión", "La muestra es una limitación importante."),
            ("inferir", "deducir algo a partir de datos", "No podemos inferir causalidad de estos datos."),
        ],
    },
    ("C1", "c1-unit-1", "reading"): {
        "title": "Interpretar resultados de investigación",
        "objective": "Distinguir resultados, interpretación y límites de una conclusión.",
        "text": "Los resultados muestran una asociación moderada entre las variables estudiadas. No obstante, el diseño no permite establecer una relación causal. Por ello, cualquier interpretación debe considerar el tamaño de la muestra y las posibles fuentes de sesgo.",
        "questions": ["¿Qué relación encuentran los resultados?", "¿Por qué no puede afirmarse causalidad?"],
    },
    ("C1", "c1-unit-1", "listening"): {
        "title": "Presentar resultados con cautela",
        "objective": "Reconocer matizadores y límites en una presentación académica.",
        "transcript": "Los resultados parecen indicar una tendencia clara, aunque la muestra es relativamente pequeña. Por tanto, sería prematuro generalizar estos datos a toda la población.",
        "questions": ["¿Qué tendencia se observa?", "¿Por qué sería prematuro generalizar?"],
    },
    ("C1", "c1-unit-1", "speaking"): {
        "title": "Presenta y matiza un resultado",
        "objective": "Explicar una conclusión y señalar sus límites sin perder claridad.",
        "prompt": "Presenta un resultado hipotético y explica qué puede y qué no puede demostrar.",
        "phrases": ["Los datos sugieren que...", "No obstante...", "Sería prematuro afirmar que..."],
        "examples": ["Los datos sugieren una mejora, no obstante, sería prematuro afirmar que el cambio explica por sí solo el resultado."],
    },
    ("C1", "c1-unit-1", "writing"): {
        "title": "Comentario analítico",
        "objective": "Redactar un comentario crítico que diferencie evidencia, interpretación y limitaciones.",
        "prompt": "Escribe 250-300 palabras comentando un resultado de investigación hipotético.",
        "guidance": ["Presenta el resultado.", "Explica una interpretación posible.", "Señala al menos dos limitaciones.", "Usa lenguaje prudente."],
        "examples": ["Aunque los resultados son coherentes con la hipótesis, no permiten establecer una relación causal definitiva."],
    },
    ("C1", "c1-unit-1", "review"): {
        "title": "Repaso del análisis crítico",
        "objective": "Consolidar lenguaje de evidencia, inferencia, cautela y limitación.",
        "questions": ["Transforma 'esto demuestra' en una formulación más prudente.", "Explica la diferencia entre asociación y causalidad."],
    },

    ("C2", "c2-unit-1", "grammar"): {
        "title": "Matiz, registro y significado implícito",
        "objective": "Ajustar estructuras y registro para expresar grados de certeza, distancia y crítica.",
        "grammar": ["pragmatica-avanzada", "registro", "matizadores", "ironía"],
        "examples": ["No deja de ser una posibilidad.", "Conviene no perder de vista que...", "Por así decirlo, la propuesta resuelve el problema a medias."],
    },
    ("C2", "c2-unit-1", "vocabulary"): {
        "title": "Retórica y precisión estilística",
        "objective": "Distinguir matices léxicos y elegir formulaciones según intención y registro.",
        "words": [
            ("ambivalente", "que presenta dos aspectos o valores opuestos", "Su reacción fue deliberadamente ambivalente."),
            ("contundente", "claro y difícil de refutar", "La respuesta fue contundente."),
            ("eufemismo", "expresión que suaviza una realidad", "La expresión funciona como eufemismo."),
            ("subyacente", "que está implícito o debajo de lo visible", "Hay una tensión subyacente en el discurso."),
        ],
    },
    ("C2", "c2-unit-1", "reading"): {
        "title": "Leer entre líneas",
        "objective": "Inferir intención, distancia irónica y presupuestos implícitos.",
        "text": "El informe celebra que, después de meses de deliberación, finalmente se haya tomado una decisión. El tono aparentemente elogioso deja entrever, sin embargo, cierta ironía: la demora se presenta como si fuera una virtud.",
        "questions": ["¿Qué contraste existe entre el tono y la intención?", "¿Qué hecho permite inferir ironía?"],
    },
    ("C2", "c2-unit-1", "listening"): {
        "title": "Crítica matizada",
        "objective": "Interpretar intención y grado de compromiso en una crítica oral.",
        "transcript": "No diría que la propuesta carece de mérito. Ahora bien, presentarla como una solución definitiva quizá sea llevar el argumento demasiado lejos.",
        "questions": ["¿La persona rechaza totalmente la propuesta?", "¿Qué crítica formula?"],
    },
    ("C2", "c2-unit-1", "speaking"): {
        "title": "Criticar sin caricaturizar",
        "objective": "Formular una crítica sofisticada reconociendo los méritos de la posición contraria.",
        "prompt": "Critica una propuesta compleja sin reducirla a una posición extrema.",
        "phrases": ["No se trata tanto de..., cuanto de...", "Concedo que...", "La dificultad reside en..."],
        "examples": ["Concedo que la propuesta ofrece una ventaja evidente; la dificultad reside en sus consecuencias a largo plazo."],
    },
    ("C2", "c2-unit-1", "writing"): {
        "title": "Ensayo crítico de alto nivel",
        "objective": "Construir un ensayo preciso, matizado y estilísticamente controlado.",
        "prompt": "Escribe 350-450 palabras sobre una cuestión controvertida, distinguiendo hechos, interpretaciones y presupuestos.",
        "guidance": ["Evita afirmaciones absolutas cuando no estén justificadas.", "Integra una objeción seria.", "Usa variación sintáctica y registro formal.", "Explicita una conclusión matizada."],
        "examples": ["La cuestión no admite una respuesta unívoca: parte del desacuerdo procede de supuestos distintos sobre lo que debe considerarse una solución eficaz."],
    },
    ("C2", "c2-unit-1", "review"): {
        "title": "Repaso de pragmática y precisión",
        "objective": "Consolidar inferencia, registro, ironía y matización.",
        "questions": ["Explica qué información implícita contiene una frase aparentemente elogiosa.", "Reformula una crítica directa para hacerla más diplomática sin perder precisión."],
    },
}


def get_lesson_seed(cefr_level: str, unit_id: str, lesson_type: str) -> dict[str, Any] | None:
    """Return the authored Spanish seed for a scheduled lesson, when available."""
    seed = _SEEDS.get((cefr_level.upper(), unit_id, lesson_type))
    return dict(seed) if seed else None
