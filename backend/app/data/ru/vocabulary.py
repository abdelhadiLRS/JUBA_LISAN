"""Русский vocabulary — initial CEFR foundation."""
from app.data._types import VocabularySet, VocabularyEntry
def _w(word,pos,definition,example): return VocabularyEntry(word=word,pos=pos,definition=definition,example=example)
VOCABULARY_SETS=[
VocabularySet(id="greetings_a1",level="A1",topic="Greetings",unit_ref="a1-unit-1",words=[_w("привет","phrase","basic greeting","привет"),_w("спасибо","phrase","thanks","спасибо")]),
VocabularySet(id="identity_a1",level="A1",topic="Identity",unit_ref="a1-unit-1",words=[_w("имя","noun","name","имя"),_w("студент","noun","student","студент")]),
VocabularySet(id="daily_a2",level="A2",topic="Daily life",unit_ref="a2-unit-1",words=[]),
VocabularySet(id="work_b1",level="B1",topic="Work",unit_ref="b1-unit-1",words=[]),
VocabularySet(id="formal_c1",level="C1",topic="Formal language",unit_ref="c1-unit-1",words=[]),
VocabularySet(id="advanced_c2",level="C2",topic="Advanced communication",unit_ref="c2-unit-1",words=[]),
]