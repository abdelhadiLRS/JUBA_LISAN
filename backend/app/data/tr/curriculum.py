"""Türkçe CEFR curriculum — expanded A1 pathway."""
from app.data._types import CurriculumUnit

def _u(level,n,title,g,v,goals,pr=None):
    return CurriculumUnit(id=f"{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=g,vocabulary_set_ids=v,lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=goals,default_weeks=2,prerequisite_unit=pr)

CURRICULUM = {
    "A1": [
        _u("A1",1,"Tanışma ve kimlik",["pronouns","nominal-sentence"],["greetings_a1","identity_a1"],["Kendini tanıtmak","Basit kişisel bilgiler vermek"]),
        _u("A1",2,"Aile",["possessive"],["family_a1"],["Aile üyelerini tanıtmak","Sahiplik ifade etmek"],"a1-unit-1"),
        _u("A1",3,"Ev ve eşyalar",["plural","vowel-harmony"],["home_a1"],["Evi ve temel eşyaları anlatmak","Çoğul isimleri kullanmak"],"a1-unit-2"),
        _u("A1",4,"Günlük hayat",["present-progressive"],["daily-life_a1"],["Günlük rutin hakkında konuşmak","Şu anda yapılan eylemleri anlatmak"],"a1-unit-3"),
        _u("A1",5,"Yemek ve alışveriş",["question-particle","basic-cases"],["food_a1"],["Yiyecek ve içecek istemek","Basit alışveriş yapmak"],"a1-unit-4"),
        _u("A1",6,"Yerler ve yönler",["basic-cases","question-particle"],["places_a1"],["Yer sormak","Basit yön tarifleri vermek"],"a1-unit-5"),
        _u("A1",7,"İletişim ve yardım",["negation","pronouns"],["communication_a1"],["Anlamadığını belirtmek","Yardım ve tekrar istemek"],"a1-unit-6"),
        _u("A1",8,"Genel tekrar",["nominal-sentence","present-progressive","negation"],["greetings_a1","identity_a1","daily-life_a1"],["A1 temel yapılarını birleştirmek","Günlük bir konuşmayı sürdürebilmek"],"a1-unit-7"),
    ],
    "A2":[_u("A2",1,"Daily situations",["present-progressive","past-tense"],["daily_a2"],["Develop A2 communication skills"],"a1-unit-8")],
    "B1":[_u("B1",1,"Communication and work",["future-tense","cases"],["work_b1"],["Develop B1 communication skills"],"a2-unit-1")],
    "B2":[_u("B2",1,"Argumentation and formal language",["conditionals","passive"],["formal_c1"],["Develop B2 communication skills"],"b1-unit-1")],
    "C1":[_u("C1",1,"Academic and professional language",["reported-speech","academic-register"],["formal_c1"],["Develop C1 communication skills"],"b2-unit-1")],
    "C2":[_u("C2",1,"Advanced style and discourse",["discourse","style"],["advanced_c2"],["Develop C2 communication skills"],"c1-unit-1")],
}
