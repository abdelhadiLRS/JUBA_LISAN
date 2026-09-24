"""Polski assessment bank A1-C2."""
from app.data._types import AssessmentQuestion

def _q(id,skill,level,question,options,correct,grammar=None):
    return AssessmentQuestion(id=id,skill=skill,difficulty=level,question=question,options=options,correct=correct,grammar_slug=grammar)

ASSESSMENT_BANK = [
_q("pl-a1-g-001","grammar","A1","Wybierz poprawne zdanie.",["Ona pracuje tutaj.","Ona pracować tutaj.","Ona pracują tutaj.","Ona pracowa tutaj."],"Ona pracuje tutaj.","present-tense"),
_q("pl-a1-g-002","grammar","A1","Wybierz poprawną formę.",["dobra książka","dobry książka","dobre książka","dobrą książka"],"dobra książka","gender"),
_q("pl-a1-v-001","vocabulary","A1","Jak powiedzieć „thank you”?",["dziękuję","proszę","przepraszam","do widzenia"],"dziękuję"),
_q("pl-a1-v-002","vocabulary","A1","Co znaczy „dworzec”?",["station","school","shop","office"],"station"),
_q("pl-a2-g-001","grammar","A2","Wybierz poprawne zdanie.",["Jadę autobusem.","Jadę autobus.","Jadę autobusa.","Jadę autobusemem."],"Jadę autobusem.","instrumental-case"),
_q("pl-a2-g-002","grammar","A2","Wybierz poprawną formę czasu przyszłego.",["Będę pracować.","Będę pracuję.","Będę pracowałem.","Będę pracujesz."],"Będę pracować.","future-tense"),
_q("pl-a2-v-001","vocabulary","A2","Co znaczy „opóźnienie”?",["delay","ticket","station","suitcase"],"delay"),
_q("pl-a2-v-002","vocabulary","A2","Wybierz słowo związane ze zdrowiem.",["gorączka","walizka","dworzec","harmonogram"],"gorączka"),
_q("pl-b1-g-001","grammar","B1","Która para pokazuje różnicę aspektu?",["czytałem / przeczytałem","czytam / czytam","jestem / jestem","mam / mam"],"czytałem / przeczytałem","aspect"),
_q("pl-b1-g-002","grammar","B1","Wybierz poprawne zdanie względne.",["To książka, którą kupiłem.","To książka, który kupiłem.","To książka, które kupiłem.","To książka, której kupiłem."],"To książka, którą kupiłem.","relative-clauses"),
_q("pl-b1-v-001","vocabulary","B1","Co znaczy „doświadczenie”?",["experience","decision","headline","conflict"],"experience"),
_q("pl-b1-v-002","vocabulary","B1","Wybierz słowo związane z mediami.",["nagłówek","przyjaźń","stypendium","ryzyko"],"nagłówek"),
_q("pl-b2-g-001","grammar","B2","Wybierz poprawne zdanie w stronie biernej.",["Raport został opublikowany.","Raport został publikować.","Raport był opublikować.","Raport został opublikować."],"Raport został opublikowany.","passive"),
_q("pl-b2-g-002","grammar","B2","Który spójnik wprowadza ustępstwo?",["chociaż","ponieważ","dlatego","więc"],"chociaż","concessive-clauses"),
_q("pl-b2-v-001","vocabulary","B2","Co znaczy „przesłanka”?",["premise","salary","heritage","delay"],"premise"),
_q("pl-b2-v-002","vocabulary","B2","Wybierz termin związany z polityką publiczną.",["regulacja","walizka","kawa","rodzina"],"regulacja"),
_q("pl-c1-g-001","grammar","C1","Która forma łagodzi twierdzenie?",["Wydaje się, że...","Na pewno jest tak...","Bez wątpienia...","To oczywiste..."],"Wydaje się, że...","hedging"),
_q("pl-c1-g-002","grammar","C1","Co najlepiej opisuje styl akademicki?",["jawne relacje logiczne","wyłącznie slang","brak struktury","same krótkie zdania"],"jawne relacje logiczne","academic-syntax"),
_q("pl-c1-v-001","vocabulary","C1","Co znaczy „hipoteza”?",["hypothesis","headline","hobby","neighbour"],"hypothesis"),
_q("pl-c1-v-002","vocabulary","C1","Wybierz słowo związane z badaniami.",["korelacja","kompromis","walizka","zupa"],"korelacja"),
_q("pl-c2-g-001","grammar","C2","Która konstrukcja wyraża kontrast?",["Z jednej strony..., z drugiej...","Przede wszystkim...","Na przykład...","W rezultacie..."],"Z jednej strony..., z drugiej...","syntactic-variation"),
_q("pl-c2-g-002","grammar","C2","Co pomaga zwiększyć precyzję semantyczną?",["dobór słowa zgodny z kontekstem","więcej wykrzykników","losowa zmiana szyku","usuwanie wszystkich spójników"],"dobór słowa zgodny z kontekstem","semantic-precision"),
_q("pl-c2-v-001","vocabulary","C2","Co znaczy „presupozycja”?",["presupposition","agreement","salary","journey"],"presupposition"),
_q("pl-c2-v-002","vocabulary","C2","Wybierz słowo związane z syntezą.",["zestawienie","gorączka","przystanek","zakupy"],"zestawienie"),
]
