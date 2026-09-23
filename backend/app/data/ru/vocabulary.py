"""Русский A1 vocabulary — expanded thematic content."""
from app.data._types import VocabularySet, VocabularyEntry

def _w(word,pos,definition,example): return VocabularyEntry(word=word,pos=pos,definition=definition,example=example)

VOCABULARY_SETS=[
    VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="a1-unit-1",words=[_w("привет","phrase","hello","Привет!"),_w("здравствуйте","phrase","hello (formal)","Здравствуйте!"),_w("до свидания","phrase","goodbye","До свидания!"),_w("пожалуйста","phrase","please / you're welcome","Пожалуйста."),_w("спасибо","phrase","thank you","Спасибо большое.")]),
    VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="a1-unit-1",words=[_w("имя","noun","name","Меня зовут Анна."),_w("студент","noun","student","Я студент."),_w("учитель","noun","teacher","Она учитель."),_w("страна","noun","country","Россия — моя страна."),_w("язык","noun","language","Я учу русский язык.")]),
    VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="a1-unit-1",words=[_w("мама","noun","mother","Моя мама дома."),_w("папа","noun","father","Мой папа работает."),_w("брат","noun","brother","У меня есть брат."),_w("сестра","noun","sister","У меня есть сестра.")]),
    VocabularySet(id="daily-life_a1",level="A1",topic="daily life",unit_ref="a1-unit-1",words=[_w("вставать","verb","to get up","Я встаю в семь."),_w("работать","verb","to work","Я работаю дома."),_w("учиться","verb","to study","Я учусь каждый день."),_w("спать","verb","to sleep","Я сплю ночью.")]),
    VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="a1-unit-1",words=[_w("вода","noun","water","Мне нужна вода."),_w("хлеб","noun","bread","Я покупаю хлеб."),_w("кофе","noun","coffee","Я пью кофе."),_w("яблоко","noun","apple","Я хочу яблоко.")]),
    VocabularySet(id="daily_a2",level="A2",topic="Daily life",unit_ref="a2-unit-1",words=[]),
    VocabularySet(id="work_b1",level="B1",topic="Work",unit_ref="b1-unit-1",words=[]),
    VocabularySet(id="formal_c1",level="C1",topic="Formal language",unit_ref="c1-unit-1",words=[]),
    VocabularySet(id="advanced_c2",level="C2",topic="Advanced communication",unit_ref="c2-unit-1",words=[]),
]
