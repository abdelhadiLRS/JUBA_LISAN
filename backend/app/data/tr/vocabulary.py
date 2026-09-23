"""Türkçe A1 vocabulary — expanded thematic sets."""
from app.data._types import VocabularySet, VocabularyEntry

def _w(word,pos,definition,example):
    return VocabularyEntry(word=word,pos=pos,definition=definition,example=example)

VOCABULARY_SETS = [
    VocabularySet(id="greetings_a1",level="A1",topic="Greetings and introductions",unit_ref="a1-unit-1",words=[
        _w("merhaba","phrase","hello","Merhaba, nasılsın?"), _w("günaydın","phrase","good morning","Günaydın!"),
        _w("hoşça kal","phrase","goodbye when leaving","Hoşça kal!"), _w("teşekkürler","phrase","thanks","Teşekkürler."),
        _w("lütfen","phrase","please","Lütfen tekrar eder misin?")
    ]),
    VocabularySet(id="identity_a1",level="A1",topic="Identity",unit_ref="a1-unit-1",words=[
        _w("ad","noun","name","Adım Ayşe."), _w("öğrenci","noun","student","Ben öğrenciyim."),
        _w("öğretmen","noun","teacher","O öğretmen."), _w("ülke","noun","country","Türkiye güzel bir ülke."),
        _w("dil","noun","language","Türkçe bir dil.")
    ]),
    VocabularySet(id="family_a1",level="A1",topic="Family",unit_ref="a1-unit-2",words=[
        _w("anne","noun","mother","Annem evde."), _w("baba","noun","father","Babam çalışıyor."),
        _w("kardeş","noun","sibling","Bir kardeşim var."), _w("aile","noun","family","Ailem Ankara'da.")
    ]),
    VocabularySet(id="home_a1",level="A1",topic="Home",unit_ref="a1-unit-3",words=[
        _w("ev","noun","house","Evimiz küçük."), _w("oda","noun","room","Odam üst katta."),
        _w("masa","noun","table","Kitap masada."), _w("kapı","noun","door","Kapı açık.")
    ]),
    VocabularySet(id="daily-life_a1",level="A1",topic="Daily routine",unit_ref="a1-unit-4",words=[
        _w("uyanmak","verb","to wake up","Saat yedide uyanıyorum."), _w("gitmek","verb","to go","Okula gidiyorum."),
        _w("çalışmak","verb","to work/study","Her gün çalışıyorum."), _w("uyumak","verb","to sleep","Gece erken uyuyorum.")
    ]),
    VocabularySet(id="food_a1",level="A1",topic="Food and drinks",unit_ref="a1-unit-5",words=[
        _w("su","noun","water","Bir su, lütfen."), _w("ekmek","noun","bread","Ekmek alıyorum."),
        _w("kahve","noun","coffee","Kahve içiyorum."), _w("elma","noun","apple","Bir elma istiyorum.")
    ]),
    VocabularySet(id="places_a1",level="A1",topic="Places and directions",unit_ref="a1-unit-6",words=[
        _w("okul","noun","school","Okul nerede?"), _w("market","noun","market","Markete gidiyorum."),
        _w("istasyon","noun","station","İstasyon yakın."), _w("sağ","noun","right","Sağa dön.")
    ]),
    VocabularySet(id="communication_a1",level="A1",topic="Everyday communication",unit_ref="a1-unit-7",words=[
        _w("anlamak","verb","to understand","Seni anlıyorum."), _w("tekrar","noun","again","Tekrar eder misin?"),
        _w("yardım","noun","help","Yardıma ihtiyacım var."), _w("sormak","verb","to ask","Bir şey sorabilir miyim?")
    ]),
    VocabularySet(id="daily_a2",level="A2",topic="Daily life",unit_ref="a2-unit-1",words=[]),
    VocabularySet(id="work_b1",level="B1",topic="Work",unit_ref="b1-unit-1",words=[]),
    VocabularySet(id="formal_c1",level="C1",topic="Formal language",unit_ref="c1-unit-1",words=[]),
    VocabularySet(id="advanced_c2",level="C2",topic="Advanced communication",unit_ref="c2-unit-1",words=[]),
]
