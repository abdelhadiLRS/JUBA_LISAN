"""Nederlands A1 vocabulary — expanded thematic content."""
from app.data._types import VocabularySet, VocabularyEntry

def _w(word,pos,definition,example): return VocabularyEntry(word=word,pos=pos,definition=definition,example=example)

VOCABULARY_SETS=[
    VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="a1-unit-1",words=[_w("hallo","phrase","hello","Hallo!"),_w("goedemorgen","phrase","good morning","Goedemorgen!"),_w("tot ziens","phrase","goodbye","Tot ziens!"),_w("alsjeblieft","phrase","please / you're welcome","Alsjeblieft."),_w("dank je","phrase","thank you","Dank je wel.")]),
    VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="a1-unit-1",words=[_w("naam","noun","name","Mijn naam is Anna."),_w("student","noun","student","Ik ben student."),_w("leraar","noun","teacher","Zij is leraar."),_w("land","noun","country","Nederland is een land."),_w("taal","noun","language","Ik leer Nederlands.")]),
    VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="a1-unit-1",words=[_w("moeder","noun","mother","Mijn moeder is thuis."),_w("vader","noun","father","Mijn vader werkt."),_w("broer","noun","brother","Ik heb een broer."),_w("zus","noun","sister","Ik heb een zus.")]),
    VocabularySet(id="daily-life_a1",level="A1",topic="daily life",unit_ref="a1-unit-1",words=[_w("opstaan","verb","to get up","Ik sta om zeven uur op."),_w("werken","verb","to work","Ik werk thuis."),_w("leren","verb","to learn","Ik leer elke dag."),_w("slapen","verb","to sleep","Ik slaap 's nachts.")]),
    VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="a1-unit-1",words=[_w("water","noun","water","Ik wil water."),_w("brood","noun","bread","Ik koop brood."),_w("koffie","noun","coffee","Ik drink koffie."),_w("appel","noun","apple","Ik wil een appel.")]),
    VocabularySet(id="daily_a2",level="A2",topic="Daily life",unit_ref="a2-unit-1",words=[]),
    VocabularySet(id="work_b1",level="B1",topic="Work",unit_ref="b1-unit-1",words=[]),
    VocabularySet(id="formal_c1",level="C1",topic="Formal language",unit_ref="c1-unit-1",words=[]),
    VocabularySet(id="advanced_c2",level="C2",topic="Advanced communication",unit_ref="c2-unit-1",words=[]),
]
