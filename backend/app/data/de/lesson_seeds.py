"""Curated German lesson seeds for deterministic, language-specific lesson generation.

The seeds complement the extensive German grammar/vocabulary datasets with
natural lesson-level material for A2-C2 and provide a deterministic fallback
when the LLM is unavailable.
"""

LESSON_SEEDS = {
    ("A2", "a2-unit-1", "grammar"): {
        "title": "Erlebnisse mit dem Perfekt",
        "objective": "Vergangene Erlebnisse mit haben oder sein und korrektem Partizip II erzählen.",
        "grammar": ["perfekt-mit-haben", "perfekt-mit-sein", "partizip-ii"],
        "phrases": ["Ich habe viel gelernt.", "Wir sind nach Berlin gefahren.", "Sie ist spät angekommen."],
        "examples": ["Ich habe gestern lange gearbeitet.", "Am Wochenende sind wir ans Meer gefahren.", "Er hat seine Freunde getroffen."],
    },
    ("A2", "a2-unit-1", "vocabulary"): {
        "title": "Reisen und Erlebnisse",
        "objective": "Über eine vergangene Reise und wichtige Erlebnisse sprechen.",
        "words": [
            ("die Reise", "trip / journey", "Die Reise nach Hamburg war sehr schön."),
            ("ankommen", "to arrive", "Wir sind um acht Uhr angekommen."),
            ("besuchen", "to visit", "Wir haben ein Museum besucht."),
            ("übernachten", "to stay overnight", "Wir haben in einem kleinen Hotel übernachtet."),
            ("der Ausflug", "excursion", "Am Samstag machen wir einen Ausflug."),
            ("erleben", "to experience", "Ich habe dort viel Neues erlebt."),
        ],
    },
    ("A2", "a2-unit-1", "reading"): {
        "title": "Ein Wochenende in Hamburg",
        "objective": "Einem kurzen Reisebericht Zeit, Ort und Aktivitäten entnehmen.",
        "text": "Letztes Wochenende ist Lena mit ihrer Schwester nach Hamburg gefahren. Sie sind am Samstagmorgen angekommen und haben zuerst den Hafen besucht. Am Nachmittag haben sie ein Museum besichtigt. Am Sonntag sind sie müde, aber zufrieden nach Hause gefahren.",
        "questions": [
            ("Wohin ist Lena gefahren?", ["Nach Hamburg", "Nach München", "Nach Köln"], "Nach Hamburg"),
            ("Was haben die Schwestern zuerst besucht?", ["Den Hafen", "Ein Museum", "Ein Restaurant"], "Den Hafen"),
        ],
    },
    ("B1", "b1-unit-1", "grammar"): {
        "title": "Hypothetische Wünsche und Möglichkeiten",
        "objective": "Mit dem Konjunktiv II Wünsche, höfliche Bitten und hypothetische Situationen ausdrücken.",
        "grammar": ["konjunktiv-ii-wuerde", "konjunktiv-ii-haette-waere", "konjunktiv-ii-wunsch"],
        "phrases": ["Ich würde gern länger bleiben.", "Wenn ich mehr Zeit hätte, würde ich öfter reisen.", "Könnten Sie mir bitte helfen?"],
        "examples": ["Wenn ich in Berlin wäre, würde ich viele Museen besuchen.", "Ich hätte gern einen Termin am Montag.", "Was würdest du an meiner Stelle machen?"],
    },
    ("B1", "b1-unit-1", "vocabulary"): {
        "title": "Wünsche, Gefühle und Entscheidungen",
        "objective": "Wünsche, Zweifel und persönliche Entscheidungen differenziert ausdrücken.",
        "words": [
            ("der Wunsch", "wish", "Mein größter Wunsch ist eine längere Reise."),
            ("die Möglichkeit", "possibility", "Es gibt mehrere Möglichkeiten."),
            ("sich entscheiden", "to decide", "Ich muss mich heute entscheiden."),
            ("hoffen", "to hope", "Ich hoffe, dass alles gut geht."),
            ("vermeiden", "to avoid", "Ich möchte unnötige Kosten vermeiden."),
            ("die Erfahrung", "experience", "Diese Erfahrung hat mir geholfen."),
        ],
    },
    ("B1", "b1-unit-1", "reading"): {
        "title": "Wenn ich mehr Zeit hätte",
        "objective": "In einem persönlichen Text Wünsche und reale Pläne unterscheiden.",
        "text": "Jonas arbeitet viel und hat unter der Woche wenig Freizeit. Wenn er mehr Zeit hätte, würde er gern einen Sprachkurs besuchen. Im Moment versucht er jedoch, jeden Abend wenigstens zwanzig Minuten zu lernen. Er hofft, dass er im nächsten Jahr weniger arbeiten muss.",
        "questions": [
            ("Was würde Jonas bei mehr Zeit machen?", ["Einen Sprachkurs besuchen", "Umziehen", "Ein Unternehmen gründen"], "Einen Sprachkurs besuchen"),
            ("Wie lange lernt er momentan jeden Abend?", ["Zwanzig Minuten", "Eine Stunde", "Zwei Stunden"], "Zwanzig Minuten"),
        ],
    },
    ("B2", "b2-unit-1", "grammar"): {
        "title": "Vergangene Hypothesen",
        "objective": "Irreale Bedingungen der Vergangenheit und Bedauern präzise formulieren.",
        "grammar": ["konjunktiv-ii-vergangenheit", "irreale-bedingungen", "subjektive-modalverben"],
        "phrases": ["Wenn ich das gewusst hätte, wäre ich früher gekommen.", "Du hättest mich anrufen sollen.", "Ich hätte die Gelegenheit nutzen können."],
        "examples": ["Wenn wir früher losgefahren wären, hätten wir den Zug erreicht.", "Sie hätte die Prüfung bestehen können, wenn sie mehr gelernt hätte."],
    },
    ("B2", "b2-unit-1", "vocabulary"): {
        "title": "Bedauern und alternative Entscheidungen",
        "objective": "Über verpasste Möglichkeiten und alternative Handlungen sprechen.",
        "words": [
            ("bedauern", "to regret", "Ich bedauere diese Entscheidung."),
            ("die Gelegenheit", "opportunity", "Er hat die Gelegenheit nicht genutzt."),
            ("der Fehler", "mistake", "Aus dem Fehler können wir lernen."),
            ("rückblickend", "in retrospect", "Rückblickend war die Entscheidung richtig."),
            ("verpassen", "to miss", "Wir haben den Zug verpasst."),
            ("die Folge", "consequence", "Die Entscheidung hatte unerwartete Folgen."),
        ],
    },
    ("B2", "b2-unit-1", "reading"): {
        "title": "Eine verpasste Gelegenheit",
        "objective": "In einem reflektierenden Text Ursache, Bedauern und alternative Folgen erkennen.",
        "text": "Rückblickend hätte Miriam die Stelle wahrscheinlich angenommen, wenn sie damals mehr über das Unternehmen gewusst hätte. Sie hatte jedoch Zweifel und lehnte das Angebot ab. Heute denkt sie, dass sie dadurch eine wichtige berufliche Erfahrung verpasst hat. Gleichzeitig ist sie überzeugt, dass die Entscheidung ihr andere Möglichkeiten eröffnet hat.",
        "questions": [
            ("Warum lehnte Miriam das Angebot ab?", ["Sie hatte Zweifel", "Das Gehalt war zu hoch", "Sie wollte sofort umziehen"], "Sie hatte Zweifel"),
            ("Wie bewertet sie die Entscheidung heute?", ["Sie sieht sowohl einen Verlust als auch neue Möglichkeiten", "Sie hält sie ausschließlich für richtig", "Sie erinnert sich nicht daran"], "Sie sieht sowohl einen Verlust als auch neue Möglichkeiten"),
        ],
    },
    ("C1", "c1-unit-1", "grammar"): {
        "title": "Epistemische Modalverben",
        "objective": "Mit Modalverben unterschiedliche Grade von Gewissheit und Schlussfolgerung ausdrücken.",
        "grammar": ["modalverben-subjektiv", "konnotationen", "argumentation"],
        "phrases": ["Er muss bereits angekommen sein.", "Sie könnte Recht haben.", "Das kann nicht stimmen."],
        "examples": ["Die Verspätung muss mit dem Wetter zusammenhängen.", "Er dürfte inzwischen zu Hause sein.", "Sie kann davon nichts gewusst haben."],
    },
    ("C1", "c1-unit-1", "vocabulary"): {
        "title": "Gewissheit, Vermutung und Zweifel",
        "objective": "Behauptungen und Schlussfolgerungen mit abgestufter Sicherheit formulieren.",
        "words": [
            ("vermutlich", "presumably", "Er ist vermutlich schon unterwegs."),
            ("zweifellos", "undoubtedly", "Das ist zweifellos ein wichtiger Faktor."),
            ("offenbar", "apparently", "Offenbar wurde die Frist verlängert."),
            ("wahrscheinlich", "probably", "Die Änderung ist wahrscheinlich sinnvoll."),
            ("die Schlussfolgerung", "conclusion", "Diese Schlussfolgerung ist nicht zwingend."),
            ("die Annahme", "assumption", "Die Annahme muss überprüft werden."),
        ],
    },
    ("C1", "c1-unit-1", "reading"): {
        "title": "Was lässt sich aus den Daten schließen?",
        "objective": "In einem argumentativen Text zwischen Daten, Schlussfolgerung und Unsicherheit unterscheiden.",
        "text": "Die vorliegenden Daten deuten darauf hin, dass regelmäßige kurze Lernphasen mit besseren Ergebnissen verbunden sind. Daraus lässt sich jedoch nicht ohne Weiteres schließen, dass die Lernmethode allein für den Unterschied verantwortlich ist. Andere Faktoren, etwa Motivation und Vorerfahrung, könnten ebenfalls eine Rolle spielen.",
        "questions": [
            ("Was deuten die Daten an?", ["Einen Zusammenhang mit regelmäßigen kurzen Lernphasen", "Dass nur eine Methode funktioniert", "Dass Motivation keine Rolle spielt"], "Einen Zusammenhang mit regelmäßigen kurzen Lernphasen"),
            ("Warum ist die Schlussfolgerung eingeschränkt?", ["Andere Faktoren könnten ebenfalls relevant sein", "Es gibt keine Daten", "Die Lernenden waren nicht beteiligt"], "Andere Faktoren könnten ebenfalls relevant sein"),
        ],
    },
    ("C2", "c2-unit-1", "grammar"): {
        "title": "Komplexe Satzgefüge und Moduswahl",
        "objective": "Konjunktiv I, Konjunktiv II und Indikativ in komplexem Diskurs gezielt kombinieren.",
        "grammar": ["komplexe-satzgefuege", "alle-modi", "stilistik"],
        "phrases": ["Er erklärte, die Maßnahme sei notwendig, obwohl sie umstritten bleibe.", "Es lässt sich nicht ausschließen, dass die Annahme falsch sein könnte."],
        "examples": ["Die Sprecherin betonte, die Ergebnisse seien vorläufig, weshalb weitere Untersuchungen erforderlich seien.", "Obwohl die These plausibel erscheint, wäre es voreilig, sie als erwiesen zu betrachten."],
    },
    ("C2", "c2-unit-1", "vocabulary"): {
        "title": "Präzision und sprachliche Nuance",
        "objective": "Abstrakte Argumente mit präzisen Verben und vorsichtigen Formulierungen ausdrücken.",
        "words": [
            ("implizieren", "to imply", "Die Aussage impliziert eine weitere Annahme."),
            ("relativieren", "to qualify / put into perspective", "Diese Zahl muss relativiert werden."),
            ("voraussetzen", "to presuppose", "Das Argument setzt bestimmte Kenntnisse voraus."),
            ("widerlegen", "to refute", "Die neuen Daten widerlegen die alte These."),
            ("nachvollziehbar", "comprehensible / plausible", "Die Kritik ist nachvollziehbar."),
            ("zwangsläufig", "inevitably", "Diese Entwicklung führt nicht zwangsläufig zu diesem Ergebnis."),
        ],
    },
    ("C2", "c2-unit-1", "reading"): {
        "title": "Zwischen Befund und Interpretation",
        "objective": "Explizite Befunde, implizite Annahmen und vorsichtige Schlussfolgerungen in einem anspruchsvollen Text analysieren.",
        "text": "Ein statistischer Zusammenhang mag auf den ersten Blick überzeugend erscheinen, impliziert jedoch nicht zwangsläufig einen kausalen Zusammenhang. Erst wenn alternative Erklärungen systematisch geprüft und relevante Störfaktoren berücksichtigt wurden, lässt sich die Reichweite einer solchen Interpretation angemessen beurteilen.",
        "questions": [
            ("Was impliziert ein statistischer Zusammenhang nicht automatisch?", ["Eine Kausalität", "Eine Messung", "Eine Beobachtung"], "Eine Kausalität"),
            ("Was ist für eine angemessene Interpretation erforderlich?", ["Alternative Erklärungen und Störfaktoren zu prüfen", "Nur den ersten Eindruck zu betrachten", "Alle Daten zu ignorieren"], "Alternative Erklärungen und Störfaktoren zu prüfen"),
        ],
    },
}


def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict | None:
    return LESSON_SEEDS.get((level.upper(), unit_id, lesson_type))
