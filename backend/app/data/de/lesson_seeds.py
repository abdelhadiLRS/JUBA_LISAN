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
    ("A2", "a2-unit-1", "listening"): {
        "title": "Am Bahnhof",
        "objective": "Eine kurze Durchsage und ein Gespräch am Bahnhof verstehen und zentrale Reiseinformationen erkennen.",
        "transcript": "Achtung auf Gleis drei: Der Zug nach Bremen fährt heute zehn Minuten später ab. Reisende nach Hannover steigen bitte in den Zug auf Gleis vier um.",
        "questions": [
            ("Wohin fährt der Zug?", ["Nach Bremen", "Nach Hamburg", "Nach Hannover"], "Nach Bremen"),
            ("Wie viel später fährt der Zug ab?", ["Fünf Minuten", "Zehn Minuten", "Zwanzig Minuten"], "Zehn Minuten"),
            ("Wo steigen Reisende nach Hannover um?", ["Auf Gleis zwei", "Auf Gleis drei", "Auf Gleis vier"], "Auf Gleis vier"),
        ],
    },
    ("A2", "a2-unit-1", "speaking"): {
        "title": "Von einer Reise erzählen",
        "objective": "Eine kurze Reiseerfahrung mit Zeitangaben, Aktivitäten und einer persönlichen Bewertung schildern.",
        "prompt": "Erzähle etwa eine Minute lang von einer Reise oder einem Ausflug. Sage, wann und wohin du gefahren bist, was du dort gemacht hast und wie du die Reise fandest.",
        "phrases": ["Letztes Wochenende bin ich nach ... gefahren.", "Dort habe ich ... besucht.", "Am besten hat mir ... gefallen."],
        "examples": ["Letztes Wochenende bin ich nach Köln gefahren. Ich habe die Altstadt besucht. Am besten hat mir der Dom gefallen."],
    },
    ("A2", "a2-unit-1", "writing"): {
        "title": "Eine kurze Reisemail",
        "objective": "Eine einfache persönliche Nachricht über eine Reise in zusammenhängenden Sätzen schreiben.",
        "prompt": "Schreibe 60–80 Wörter an einen Freund oder eine Freundin. Beschreibe, wohin du gereist bist, was du gemacht hast und was dir besonders gefallen hat.",
        "guidance": ["Verwende das Perfekt für vergangene Ereignisse.", "Nenne mindestens zwei Aktivitäten.", "Beende die Nachricht mit einer persönlichen Bewertung."],
        "examples": ["Hallo Maria, ich bin am Wochenende nach Hamburg gefahren. Ich habe den Hafen besucht und ein Museum besichtigt. Die Reise war sehr schön, aber das Wetter war kalt. Besonders gut hat mir die Atmosphäre am Hafen gefallen."],
    },
    ("A2", "a2-unit-1", "review"): {
        "title": "Reise-Check",
        "objective": "Perfekt, Reisevokabular und grundlegende Zeitangaben in einer kurzen Wiederholung anwenden.",
        "questions": [
            ("Welche Form ist korrekt?", ["Wir sind nach Berlin gefahren.", "Wir haben nach Berlin gefahren.", "Wir ist nach Berlin gefahren."], "Wir sind nach Berlin gefahren."),
            ("Was bedeutet „übernachten“?", ["eine Nacht an einem Ort bleiben", "früh abreisen", "ein Museum besuchen"], "eine Nacht an einem Ort bleiben"),
            ("Welche Frage passt zu einer vergangenen Reise?", ["Was hast du gemacht?", "Was machst du morgen?", "Wo arbeitest du gerade?"], "Was hast du gemacht?"),
        ],
    },

    ("B1", "b1-unit-1", "listening"): {
        "title": "Ein neuer Sprachkurs",
        "objective": "Die wichtigsten Informationen aus einem kurzen Gespräch über einen Sprachkurs erfassen.",
        "transcript": "Mara: Ich habe mich für den Abendkurs angemeldet. Der Kurs beginnt nächsten Dienstag und findet zweimal pro Woche statt. Jonas: Warum hast du dich für diesen Kurs entschieden? Mara: Weil ich im nächsten Jahr beruflich öfter mit Kunden aus Deutschland sprechen werde.",
        "questions": [
            ("Wann beginnt der Kurs?", ["Nächsten Dienstag", "Nächsten Freitag", "Im nächsten Monat"], "Nächsten Dienstag"),
            ("Wie oft findet der Kurs statt?", ["Einmal pro Woche", "Zweimal pro Woche", "Jeden Abend"], "Zweimal pro Woche"),
            ("Warum besucht Mara den Kurs?", ["Für eine Reise", "Für ihre Arbeit", "Für ein Studium"], "Für ihre Arbeit"),
        ],
    },
    ("B1", "b1-unit-1", "speaking"): {
        "title": "Eine Entscheidung begründen",
        "objective": "Eine persönliche Entscheidung erklären, Gründe nennen und eine hypothetische Alternative formulieren.",
        "prompt": "Beschreibe eine wichtige Entscheidung aus deinem Alltag. Erkläre, warum du dich so entschieden hast, und sage, was du anders machen würdest, wenn du mehr Zeit oder Geld hättest.",
        "phrases": ["Ich habe mich dafür entschieden, weil ...", "Ein wichtiger Grund war ...", "Wenn ich mehr Zeit hätte, würde ich ..."],
        "examples": ["Ich habe mich für einen Abendkurs entschieden, weil ich tagsüber arbeite. Wenn ich mehr Zeit hätte, würde ich zusätzlich einen Konversationskurs besuchen."],
    },
    ("B1", "b1-unit-1", "writing"): {
        "title": "Eine Entscheidung erklären",
        "objective": "Eine begründete persönliche Stellungnahme mit Konnektoren und einer hypothetischen Alternative schreiben.",
        "prompt": "Schreibe 100–120 Wörter über eine Entscheidung, die du getroffen hast. Erkläre mindestens zwei Gründe und beschreibe anschließend, was du unter anderen Bedingungen tun würdest.",
        "guidance": ["Verbinde Gründe mit weil, deshalb, außerdem oder allerdings.", "Verwende mindestens einen Satz mit Konjunktiv II.", "Formuliere eine klare Schlussfolgerung."],
        "examples": ["Ich habe mich für einen Sprachkurs am Abend entschieden, weil ich tagsüber arbeite. Außerdem möchte ich meine beruflichen Möglichkeiten verbessern. Wenn ich mehr Zeit hätte, würde ich häufiger mit Muttersprachlern sprechen."],
    },
    ("B1", "b1-unit-1", "review"): {
        "title": "Wünsche und Entscheidungen – Review",
        "objective": "Konjunktiv II, Entscheidungswortschatz und begründetes Sprechen wiederholen.",
        "questions": [
            ("Welche Form beschreibt eine hypothetische Situation?", ["Wenn ich mehr Zeit hätte, würde ich reisen.", "Ich reise morgen.", "Ich bin gestern gereist."], "Wenn ich mehr Zeit hätte, würde ich reisen."),
            ("Welche Wendung leitet einen Grund ein?", ["weil", "obwohl", "während"], "weil"),
            ("Welche Aussage drückt Bedauern über eine Möglichkeit aus?", ["Ich hätte die Chance nutzen sollen.", "Ich nutze die Chance.", "Ich werde die Chance nutzen."], "Ich hätte die Chance nutzen sollen."),
        ],
    },

    ("B2", "b2-unit-1", "listening"): {
        "title": "Rückblick auf eine berufliche Entscheidung",
        "objective": "In einem reflektierenden Gespräch Gründe, Folgen und alternative Möglichkeiten unterscheiden.",
        "transcript": "Nora: Rückblickend hätte ich das Angebot vielleicht annehmen sollen. Es hätte mir neue Erfahrungen ermöglicht. Andererseits wäre ein Umzug damals sehr schwierig gewesen, weil meine Familie in der Stadt geblieben ist. Heute sehe ich die Entscheidung deshalb differenzierter.",
        "questions": [
            ("Was bedauert Nora teilweise?", ["Eine berufliche Möglichkeit nicht genutzt zu haben", "Einen Umzug gemacht zu haben", "Zu viel gearbeitet zu haben"], "Eine berufliche Möglichkeit nicht genutzt zu haben"),
            ("Warum wäre ein Umzug schwierig gewesen?", ["Ihre Familie blieb in der Stadt.", "Sie hatte keine Wohnung.", "Sie wollte nicht arbeiten."], "Ihre Familie blieb in der Stadt."),
            ("Wie bewertet Nora die Entscheidung heute?", ["Differenzierter", "Nur negativ", "Ohne weitere Überlegung"], "Differenzierter"),
        ],
    },
    ("B2", "b2-unit-1", "speaking"): {
        "title": "Eine alternative Entscheidung diskutieren",
        "objective": "Eine vergangene Entscheidung analysieren, Konsequenzen abwägen und eine Gegenposition einbeziehen.",
        "prompt": "Wähle eine fiktive berufliche oder persönliche Entscheidung. Erkläre, was passiert ist, welche Alternative möglich gewesen wäre und welche Vor- und Nachteile beide Optionen gehabt hätten.",
        "phrases": ["Rückblickend hätte ich ...", "Andererseits wäre ...", "Unter diesen Umständen wäre es sinnvoller gewesen, ..."],
        "examples": ["Rückblickend hätte ich das Angebot annehmen können. Andererseits wäre der Umzug mit erheblichen Kosten verbunden gewesen. Unter diesen Umständen wäre eine spätere Entscheidung vielleicht sinnvoller gewesen."],
    },
    ("B2", "b2-unit-1", "writing"): {
        "title": "Abwägen und begründen",
        "objective": "Eine differenzierte Stellungnahme mit Gegenargument, Konsequenzen und Schlussfolgerung verfassen.",
        "prompt": "Schreibe 160–200 Wörter über eine Entscheidung mit zwei realistischen Optionen. Stelle beide Möglichkeiten dar, nenne jeweils Vor- und Nachteile und begründe am Ende deine Einschätzung.",
        "guidance": ["Nutze einerseits ... andererseits oder ähnliche Konnektoren.", "Verwende mindestens eine vergangene Hypothese.", "Unterscheide Fakten von deiner persönlichen Bewertung."],
        "examples": ["Einerseits hätte die neue Stelle bessere Aufstiegsmöglichkeiten geboten. Andererseits wäre ein Umzug notwendig gewesen. Rückblickend wäre die Entscheidung vertretbar gewesen, wenn die familiäre Situation weniger kompliziert gewesen wäre."],
    },
    ("B2", "b2-unit-1", "review"): {
        "title": "Vergangene Hypothesen – Review",
        "objective": "Vergangenheitsformen des Konjunktiv II und differenzierte Argumentation festigen.",
        "questions": [
            ("Welche Form ist korrekt?", ["Wenn ich das gewusst hätte, wäre ich früher gekommen.", "Wenn ich das gewusst habe, wäre ich früher gekommen.", "Wenn ich das wusste, bin ich früher gekommen."], "Wenn ich das gewusst hätte, wäre ich früher gekommen."),
            ("Welche Wendung signalisiert einen Gegensatz?", ["andererseits", "deshalb", "nämlich"], "andererseits"),
            ("Welche Aussage beschreibt eine nicht realisierte Möglichkeit?", ["Sie hätte die Gelegenheit nutzen können.", "Sie nutzt die Gelegenheit.", "Sie wird die Gelegenheit nutzen."], "Sie hätte die Gelegenheit nutzen können."),
        ],
    },

    ("C1", "c1-unit-1", "listening"): {
        "title": "Was sagen die Daten wirklich?",
        "objective": "In einem fachsprachlichen Kurzbeitrag zwischen Befund, Interpretation und Einschränkung unterscheiden.",
        "transcript": "Die Untersuchung zeigt einen deutlichen Zusammenhang zwischen kurzen, regelmäßigen Lernphasen und besseren Testergebnissen. Daraus folgt jedoch nicht zwangsläufig, dass die Lernintervalle allein den Unterschied verursachen. Die Forschenden weisen darauf hin, dass Motivation und Vorerfahrung ebenfalls berücksichtigt werden müssen.",
        "questions": [
            ("Was zeigt die Untersuchung?", ["Einen Zusammenhang zwischen Lernintervallen und Ergebnissen", "Eine eindeutige Kausalität", "Dass Motivation unwichtig ist"], "Einen Zusammenhang zwischen Lernintervallen und Ergebnissen"),
            ("Was folgt nicht zwangsläufig aus dem Befund?", ["Eine eindeutige Kausalität", "Dass Daten erhoben wurden", "Dass Lernende getestet wurden"], "Eine eindeutige Kausalität"),
            ("Welche weiteren Faktoren werden genannt?", ["Motivation und Vorerfahrung", "Alter und Wohnort", "Wetter und Verkehr"], "Motivation und Vorerfahrung"),
        ],
    },
    ("C1", "c1-unit-1", "speaking"): {
        "title": "Eine These vorsichtig bewerten",
        "objective": "Eine komplexe These einordnen, Evidenz abwägen und Unsicherheit sprachlich präzise markieren.",
        "prompt": "Nimm Stellung zu einer These aus Bildung, Arbeit oder Technologie. Formuliere zunächst die These, nenne zwei Argumente, schränke mindestens eine Aussage ein und ziehe anschließend eine differenzierte Schlussfolgerung.",
        "phrases": ["Die vorliegenden Hinweise deuten darauf hin, dass ...", "Daraus lässt sich allerdings nicht ohne Weiteres schließen, dass ...", "Unter diesen Voraussetzungen erscheint es plausibel, dass ..."],
        "examples": ["Die Hinweise deuten darauf hin, dass kurze Lernphasen hilfreich sind. Daraus lässt sich allerdings nicht ohne Weiteres schließen, dass sie für alle Lernenden gleichermaßen wirksam sind."],
    },
    ("C1", "c1-unit-1", "writing"): {
        "title": "Eine differenzierte Analyse schreiben",
        "objective": "Eine strukturierte Analyse mit Evidenz, Einschränkungen und Schlussfolgerung verfassen.",
        "prompt": "Schreibe 220–280 Wörter zu einer kontroversen These. Führe mindestens zwei Argumente an, berücksichtige eine Gegenposition und kennzeichne klar, welche Schlussfolgerungen sicher und welche nur plausibel sind.",
        "guidance": ["Verwende präzise epistemische Formulierungen wie vermutlich, offenbar, es ist anzunehmen, dass.", "Trenne Befund und Interpretation.", "Schließe mit einer begründeten, aber nicht überzogenen Schlussfolgerung."],
        "examples": ["Die Ergebnisse legen nahe, dass regelmäßige Lernphasen vorteilhaft sind. Sie belegen jedoch nicht eindeutig, dass die Lernintervalle allein für die Unterschiede verantwortlich sind."],
    },
    ("C1", "c1-unit-1", "review"): {
        "title": "Gewissheit und Schlussfolgerung – Review",
        "objective": "Epistemische Modalverben und vorsichtige Argumentation gezielt wiederholen.",
        "questions": [
            ("Welche Form drückt eine starke Schlussfolgerung aus?", ["Er muss bereits angekommen sein.", "Er könnte angekommen sein.", "Er ist vielleicht angekommen."], "Er muss bereits angekommen sein."),
            ("Welche Form markiert eine vorsichtige Vermutung?", ["Sie könnte Recht haben.", "Sie hat zweifellos Recht.", "Sie hat Recht."], "Sie könnte Recht haben."),
            ("Was ist bei einer wissenschaftlichen Schlussfolgerung wichtig?", ["Befund und Interpretation zu unterscheiden", "Unsicherheit grundsätzlich auszuschließen", "Nur die erste Erklärung zu nennen"], "Befund und Interpretation zu unterscheiden"),
        ],
    },

    ("C2", "c2-unit-1", "listening"): {
        "title": "Befund, Kausalität und Reichweite",
        "objective": "Einen dichten argumentativen Kurzbeitrag hinsichtlich impliziter Annahmen und logischer Reichweite analysieren.",
        "transcript": "Ein beobachteter Zusammenhang besitzt zunächst nur deskriptiven Charakter. Erst wenn konkurrierende Erklärungen geprüft und relevante Störvariablen kontrolliert wurden, kann eine kausale Deutung plausibel werden. Selbst dann bleibt zu klären, inwieweit sich das Ergebnis auf andere Kontexte übertragen lässt.",
        "questions": [
            ("Welchen Charakter besitzt ein beobachteter Zusammenhang zunächst?", ["Deskriptiven", "Kausalen", "Normativen"], "Deskriptiven"),
            ("Was muss vor einer kausalen Deutung geprüft werden?", ["Konkurrierende Erklärungen und Störvariablen", "Nur die Überschrift", "Die Meinung der ersten Person"], "Konkurrierende Erklärungen und Störvariablen"),
            ("Welche weitere Frage bleibt offen?", ["Die Übertragbarkeit auf andere Kontexte", "Ob Daten überhaupt existieren", "Ob Sprache verwendet wurde"], "Die Übertragbarkeit auf andere Kontexte"),
        ],
    },
    ("C2", "c2-unit-1", "speaking"): {
        "title": "Nuanciert argumentieren",
        "objective": "Eine komplexe Position rhetorisch kontrolliert vertreten, Einschränkungen einbauen und Gegenargumente integrieren.",
        "prompt": "Wähle eine anspruchsvolle These. Entwickle eine klare Position, antizipiere ein starkes Gegenargument, relativiere deine eigene Aussage an geeigneter Stelle und formuliere eine präzise Schlussfolgerung.",
        "phrases": ["Die These ist insofern plausibel, als ...", "Allerdings greift diese Erklärung zu kurz, wenn ...", "Es wäre voreilig, daraus abzuleiten, dass ..."],
        "examples": ["Die These ist insofern plausibel, als die Daten einen Zusammenhang erkennen lassen. Allerdings greift diese Erklärung zu kurz, wenn alternative Ursachen unberücksichtigt bleiben."],
    },
    ("C2", "c2-unit-1", "writing"): {
        "title": "Argumentation mit sprachlicher Präzision",
        "objective": "Einen komplexen argumentativen Text mit kontrollierter Moduswahl, Gegenargumenten und präziser Schlussfolgerung verfassen.",
        "prompt": "Schreibe 300–400 Wörter zu einer anspruchsvollen These. Entwickle die Argumentation selbstständig, integriere mindestens ein Gegenargument, relativiere eine eigene Aussage und unterscheide ausdrücklich zwischen Befund, Interpretation und Schlussfolgerung.",
        "guidance": ["Nutze Konjunktiv I bei geeigneter indirekter Wiedergabe.", "Setze Konjunktiv II gezielt für hypothetische oder kontrafaktische Überlegungen ein.", "Vermeide pauschale Aussagen und markiere den Geltungsbereich deiner Schlussfolgerungen."],
        "examples": ["Die Studie lege nahe, dass die Methode wirksam sei; daraus abzuleiten, sie sei unter allen Bedingungen überlegen, wäre jedoch voreilig."],
    },
    ("C2", "c2-unit-1", "review"): {
        "title": "Stilistische Präzision – Review",
        "objective": "Moduswahl, argumentative Einschränkung und logische Reichweite in anspruchsvollen Formulierungen wiederholen.",
        "questions": [
            ("Welche Form eignet sich für eine distanzierte indirekte Wiedergabe?", ["Er erklärte, die Ergebnisse seien vorläufig.", "Er erklärte, die Ergebnisse sind vorläufig.", "Er erklärte, die Ergebnisse werden vorläufig."], "Er erklärte, die Ergebnisse seien vorläufig."),
            ("Welche Form signalisiert eine vorsichtige Schlussfolgerung?", ["Es wäre voreilig, daraus abzuleiten, dass ...", "Es ist immer so, dass ...", "Das beweist ohne Ausnahme, dass ..."], "Es wäre voreilig, daraus abzuleiten, dass ..."),
            ("Was sollte eine präzise Argumentation vermeiden?", ["Pauschale Schlussfolgerungen ohne Prüfung der Reichweite", "Klare Begriffe", "Gegenargumente"], "Pauschale Schlussfolgerungen ohne Prüfung der Reichweite"),
        ],
    },

}


def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict | None:
    return LESSON_SEEDS.get((level.upper(), unit_id, lesson_type))
