"""Polski A1 grammar — expanded learner-ready foundation."""
from app.data._types import GrammarTopic, GrammarExample
def _g(slug,title,summary,explanation,examples,rules=None):
    return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=explanation,structure=None,rules=rules or [],examples=[GrammarExample(text=x) for x in examples],common_mistakes=[],related=[])
GRAMMAR_TOPICS=[
_g("pronouns","Zaimki osobowe","Ja, ty, on, ona, my, wy, oni.","Zaimki wskazują osobę i liczbę.",["Jestem studentem.","Ona jest nauczycielką.","Mieszkamy w Polsce."]),
_g("gender","Rodzaj gramatyczny","Rozpoznawać rodzaj rzeczowników.","Polski ma rodzaj męski, żeński i nijaki; wpływa on na zgodę.",["dobry dom","dobra książka","dobre słowo"]),
_g("present-tense","Czas teraźniejszy","Mówić o teraźniejszości.","Czasowniki odmieniają się przez osoby i liczby.",["Czytam książkę.","Mieszkasz w Warszawie.","Pracujemy tutaj."]),
_g("negation","Przeczenie","Tworzyć zdania z nie.","Nie zwykle stoi przed czasownikiem lub innym negowanym elementem.",["Nie rozumiem.","On nie pracuje.","Nie jestem w domu."]),
_g("questions","Podstawowe pytania","Pytać o osobę, miejsce i rzecz.","Słowa kto, co, gdzie i jak tworzą podstawowe pytania.",["Jak masz na imię?","Gdzie mieszkasz?","Co to jest?"]),
_g("cases","Podstawowe przypadki","Rozumieć najczęstsze formy przypadków.","Końcówki rzeczowników zmieniają się zależnie od funkcji w zdaniu.",["To jest mój dom.","Idę do szkoły.","Lubię kawę."]),
_g("adjectives","Przymiotniki","Dopasowywać opis do rzeczownika.","Przymiotnik zgadza się z rzeczownikiem w rodzaju i liczbie.",["duży dom","duża kawa","duże miasto"]),
_g("numbers","Liczby","Używać liczb w codziennych sytuacjach.","Liczby są potrzebne przy wieku, cenie, czasie i ilości.",["Mam dwadzieścia lat.","To kosztuje dziesięć złotych.","Jest trzecia."]),
_g("past-tense","Czas przeszły","Mówić o prostych wydarzeniach z przeszłości.","Czas przeszły zmienia się zależnie od rodzaju i liczby.",["Byłem w domu.","Była w pracy.","Czytaliśmy książkę."]),
_g("future-tense","Czas przyszły","Mówić o planach.","Przyszłość może być wyrażana przez będę oraz bezokolicznik.",["Będę pracować.","Będziemy się uczyć."]),
]