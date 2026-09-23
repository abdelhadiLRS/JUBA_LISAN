"""Polski A1 vocabulary — expanded thematic content."""
from app.data._types import VocabularySet, VocabularyEntry

def _w(word,pos,definition,example): return VocabularyEntry(word=word,pos=pos,definition=definition,example=example)

VOCABULARY_SETS=[
    VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="a1-unit-1",words=[_w("cześć","phrase","hello","Cześć!"),_w("dzień dobry","phrase","good morning / hello","Dzień dobry!"),_w("do widzenia","phrase","goodbye","Do widzenia!"),_w("proszę","phrase","please / you're welcome","Proszę."),_w("dziękuję","phrase","thank you","Dziękuję bardzo.")]),
    VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="a1-unit-1",words=[_w("imię","noun","name","Mam na imię Anna."),_w("student","noun","student","Jestem studentem."),_w("nauczyciel","noun","teacher","On jest nauczycielem."),_w("kraj","noun","country","Polska to mój kraj."),_w("język","noun","language","Uczę się polskiego.")]),
    VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="a1-unit-1",words=[_w("mama","noun","mother","Moja mama jest w domu."),_w("tata","noun","father","Mój tata pracuje."),_w("brat","noun","brother","Mam brata."),_w("siostra","noun","sister","Mam siostrę.")]),
    VocabularySet(id="daily-life_a1",level="A1",topic="daily life",unit_ref="a1-unit-1",words=[_w("wstawać","verb","to get up","Wstaję o siódmej."),_w("pracować","verb","to work","Pracuję w domu."),_w("uczyć się","verb","to study","Uczę się codziennie."),_w("spać","verb","to sleep","Śpię w nocy.")]),
    VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="a1-unit-1",words=[_w("woda","noun","water","Poproszę wodę."),_w("chleb","noun","bread","Kupuję chleb."),_w("kawa","noun","coffee","Piję kawę."),_w("jabłko","noun","apple","Chcę jabłko.")]),
    VocabularySet(id="daily_a2",level="A2",topic="Daily life",unit_ref="a2-unit-1",words=[]),
    VocabularySet(id="work_b1",level="B1",topic="Work",unit_ref="b1-unit-1",words=[]),
    VocabularySet(id="formal_c1",level="C1",topic="Formal language",unit_ref="c1-unit-1",words=[]),
    VocabularySet(id="advanced_c2",level="C2",topic="Advanced communication",unit_ref="c2-unit-1",words=[]),
]
