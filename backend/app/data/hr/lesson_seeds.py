"""Curated Croatian A2-C2 lesson seeds for JUBA LISAN."""
from __future__ import annotations
from app.data.language_foundations.hr import CURRICULUM
_SKILLS=("grammar","vocabulary","reading","listening","speaking","writing","review")
_EX={
"A2":["Jučer sam posjetio muzej i razgovarao s prijateljem.","Sutra ću putovati i unaprijed provjeriti raspored."],
"B1":["Kad bih imao više vremena, istražio bih i druge mogućnosti.","Pročitao sam izvještaj i zatim sažeo njegove glavne ideje."],
"B2":["Iako je prijedlog zanimljiv, treba razmotriti njegove moguće posljedice.","Rekao je da će rezultati biti objavljeni nakon provjere."],
"C1":["Na temelju dostupnih podataka može se zaključiti da je potrebna dodatna analiza.","U skladu s propisima, dokumentaciju treba dostaviti u predviđenom roku."],
"C2":["Provedba predloženih mjera zahtijeva pažljivo tumačenje međusobno povezanih čimbenika.","Izraz treba razumjeti u kontekstu jer njegovo značenje nije uvijek doslovno."],
}
_WORDS={
"A2":[("iskustvo","experience","To je bilo korisno iskustvo."),("putovanje","journey","Putovanje je trajalo tri dana."),("planirati","to plan","Planiram putovanje.")],
"B1":[("odgovornost","responsibility","To je velika odgovornost."),("mogućnost","possibility","Imamo još jednu mogućnost."),("istraživanje","research","Istraživanje je završeno.")],
"B2":[("posljedica","consequence","Moramo procijeniti posljedice."),("tvrdnja","claim","Tvrdnja zahtijeva dokaz."),("argument","argument","Ovo je snažan argument.")],
"C1":[("pretpostavka","assumption","Pretpostavku treba provjeriti."),("nalaz","finding","Glavni nalaz je važan."),("metodologija","methodology","Metodologija je jasno opisana.")],
"C2":[("dvosmislen","ambiguous","Izraz može biti dvosmislen."),("nijansa","nuance","Važna je semantička nijansa."),("ublažiti","to soften","Autor nastoji ublažiti tvrdnju.")],
}
def _unit(unit_id,level):
    for unit in CURRICULUM.get(level,[]):
        if unit.id==unit_id:return unit
    return None
def get_lesson_seed(level:str,unit_id:str,lesson_type:str)->dict|None:
    level=str(level).upper();skill=str(lesson_type).lower();unit=_unit(unit_id,level)
    if unit is None or skill not in _SKILLS:return None
    examples=_EX[level];words=_WORDS[level]
    base={"title":unit.title,"objective":f"Razvijajte hrvatski jezik na razini {level} kroz temu „{unit.title}“.","unit_id":unit_id,"source":"curated_croatian","words":words,"vocabulary_words":[w[0] for w in words],"grammar":list(unit.grammar_points),"examples":examples}
    if skill=="grammar":base["objective"]=f"Upotrijebite ciljane gramatičke strukture za temu „{unit.title}“."
    elif skill=="vocabulary":base["objective"]="Usvojite ključni rječnik i koristite ga u kontekstu."
    elif skill=="reading":base.update(text=" ".join(examples),questions=["Koja je glavna tema teksta?","Koje dvije informacije podupiru glavnu ideju?","Objasnite jedan izraz svojim riječima."])
    elif skill=="listening":base.update(transcript=" ".join(examples),questions=["Koja je glavna poruka?","Koje ključne riječi čujete?","Koji detalj potvrđuje glavnu ideju?"])
    elif skill=="speaking":base.update(prompt=f"Govorite o temi „{unit.title}“ i upotrijebite barem tri riječi iz lekcije.",phrases=examples,examples=examples[:2])
    elif skill=="writing":base.update(prompt=f"Napišite povezan tekst o temi „{unit.title}“.","guidance":["Upotrijebite barem tri riječi iz lekcije.","Uključite barem jednu ciljanu gramatičku strukturu.","Povežite ideje jasnim rečenicama."],examples=examples[:2])
    else:base["questions"]=["Objasnite jednu ciljanu gramatičku strukturu.","Napišite dvije rečenice s novim riječima.","Sažmite temu lekcije svojim riječima."]
    return base
