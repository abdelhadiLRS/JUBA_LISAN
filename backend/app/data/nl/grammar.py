"""Nederlands A1 grammar — expanded learner-ready foundation."""
from app.data._types import GrammarTopic, GrammarExample
def _g(slug,title,summary,explanation,examples,rules=None):
    return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=explanation,structure=None,rules=rules or [],examples=[GrammarExample(text=x) for x in examples],common_mistakes=[],related=[])
GRAMMAR_TOPICS=[
_g("pronouns","Persoonlijke voornaamwoorden","Ik, jij, hij, zij, wij en jullie gebruiken.","Persoonlijke voornaamwoorden geven aan wie iets doet of is.",["Ik ben student.","Zij woont in Amsterdam.","Wij leren Nederlands."]),
_g("word-order","Woordvolgorde","Eenvoudige Nederlandse zinnen bouwen.","In een gewone hoofdzin staat de persoonsvorm op de tweede plaats.",["Ik woon in Brussel.","Vandaag werk ik thuis.","Hij leest een boek."]),
_g("present-tense","Tegenwoordige tijd","Praten over gewoonten en acties.","Gebruik de juiste persoonsvorm van het werkwoord in de tegenwoordige tijd.",["Ik werk vandaag.","Jij woont hier.","Zij leert Nederlands."]),
_g("articles","De en het","Basisartikelen gebruiken.","Nederlandse zelfstandige naamwoorden hebben meestal de of het als bepaald lidwoord.",["de tafel","het huis","de student"]),
_g("questions","Vragen stellen","Wie, wat, waar en hoe gebruiken.","Vraagwoorden en inversie maken eenvoudige vragen.",["Waar woon je?","Wat doe je?","Hoe heet je?"]),
_g("negation","Ontkenning","Niet en geen gebruiken.","Niet ontkent vaak werkwoorden of eigenschappen; geen ontkent een zelfstandig naamwoord zonder bepaald lidwoord.",["Ik werk niet.","Ik heb geen auto.","Hij is niet thuis."]),
_g("plural","Meervoud","Meervouden herkennen en vormen.","Veel zelfstandige naamwoorden krijgen -en of -s in het meervoud.",["boek → boeken","tafel → tafels","student → studenten"]),
_g("adjectives","Bijvoeglijke naamwoorden","Eenvoudige beschrijvingen geven.","Bijvoeglijke naamwoorden krijgen in veel bepaalde naamwoordgroepen een -e.",["een grote stad","een klein huis","de nieuwe auto"]),
_g("present-perfect","Voltooide tijd","Recente of afgeronde gebeurtenissen noemen.","De voltooide tijd gebruikt hebben of zijn met een voltooid deelwoord.",["Ik heb gewerkt.","Zij heeft gegeten.","We zijn gekomen."]),
_g("separable-verbs","Scheidbare werkwoorden","Veelgebruikte scheidbare werkwoorden begrijpen.","In een hoofdzin staat het voorvoegsel vaak aan het einde.",["Ik sta om zeven uur op.","Hij belt mij terug."]),
]