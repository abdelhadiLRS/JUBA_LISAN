"""Curated Czech A2-C2 lesson seeds aligned with all Czech curriculum units."""
from __future__ import annotations
from typing import Any

UNITS = {
"A2":[("cs-a2-1","Bydlení a okolí","Bydlím v klidné ulici. V okolí je park a obchod.",["byt","sousedství","náměstí"]),
("cs-a2-2","Cestování a doprava","Zítra pojedu vlakem do Prahy. Koupím si jízdenku.",["jízdenka","nádraží","vlak"]),
("cs-a2-3","Zdraví a volný čas","Včera mě bolela hlava, ale dnes už je mi lépe.",["lékař","bolest","výlet"]),
("cs-a2-4","Práce a služby","Potřebuji si objednat službu a domluvit termín.",["zaměstnání","zákazník","objednat"])],
"B1":[("cs-b1-1","Studium a cíle","Chtěl bych studovat, abych si zlepšil kvalifikaci.",["studium","zkouška","dovednost"]),
("cs-b1-2","Práce a zkušenosti","Řekl, že získal nové zkušenosti.",["kariéra","zkušenost","příležitost"]),
("cs-b1-3","Média a společnost","Zpráva vyvolala diskusi, protože téma bylo důležité.",["zpráva","společnost","názor"]),
("cs-b1-4","Problémy a řešení","Problém lze vyřešit několika způsoby.",["problém","řešení","opatření"])],
"B2":[("cs-b2-1","Argumentace a debata","Na jedné straně je změna užitečná, na druhé straně přináší rizika.",["argument","námitka","důkaz"]),
("cs-b2-2","Kultura a identita","Ačkoli se tradice mění, její význam zůstává.",["identita","tradice","hodnota"]),
("cs-b2-3","Ekonomika a profesní komunikace","Dovolte mi upozornit na změnu podmínek.",["rozpočet","investice","jednání"]),
("cs-b2-4","Analýza a prezentace řešení","Výsledky ukazují několik možností dalšího postupu.",["analýza","výsledek","návrh"])],
"C1":[("cs-c1-1","Akademický jazyk a výzkum","Výsledky naznačují, že tento trend souvisí s několika faktory.",["výzkum","hypotéza","evidence"]),
("cs-c1-2","Profesionální komunikace","Domnívám se, že by bylo vhodné návrh ještě upravit.",["schůzka","návrh","doporučení"]),
("cs-c1-3","Společnost a analýza","Tento jev nelze vysvětlit jedinou příčinou.",["jev","souvislost","důsledek"]),
("cs-c1-4","Rétorika a styl","Zvolená formulace zdůrazňuje hlavní problém.",["formulace","důraz","styl"])],
"C2":[("cs-c2-1","Sémantická nuance","Rozdíl mezi těmito výrazy je především pragmatický.",["nuance","význam","idiom"]),
("cs-c2-2","Pokročilá argumentace","Tvrzení působí přesvědčivě, avšak jeho předpoklad zůstává sporný.",["předpoklad","protiargument","implikace"]),
("cs-c2-3","Specializovaný a odborný jazyk","V odborném kontextu je třeba termín přesně vymezit.",["terminologie","kontext","vymezení"]),
("cs-c2-4","Syntéza a přesné vyjadřování","Z dostupných údajů lze vyvodit pouze omezený závěr.",["syntéza","závěr","omezení"])]
}

def _make(level:str, unit:str, title:str, example:str, words:list[str])->dict[tuple[str,str,str],dict[str,Any]]:
    vocab=[(w,f"klíčový výraz k tématu {title}",f"Používám výraz {w} v kontextu.") for w in words]
    return {
      (level,unit,"grammar"):{"title":f"{title}: gramatika","objective":f"Používej gramatiku vhodnou pro úroveň {level} při tématu {title}.","examples":[example]},
      (level,unit,"vocabulary"):{"title":f"{title}: slovní zásoba","objective":f"Osvoj si slovní zásobu k tématu {title}.","words":vocab},
      (level,unit,"reading"):{"title":f"{title}: čtení","objective":f"Porozuměj souvislému textu o tématu {title}.","text":f"{example} {title} je důležitou součástí běžné komunikace. Text uvádí hlavní myšlenku, několik detailů a konkrétní příklad.","questions":[f"Jaká je hlavní myšlenka textu o tématu {title}?","Najdi dva důležité detaily.","Shrň text vlastními slovy."]},
      (level,unit,"listening"):{"title":f"{title}: poslech","objective":f"Zachyť hlavní informace v mluveném projevu o tématu {title}.","transcript":f"{example} Mluvčí vysvětluje hlavní důvod a uvádí konkrétní příklad.","questions":["Jaká je hlavní myšlenka?","Jaký důvod mluvčí uvádí?","Jaký příklad zazní?"]},
      (level,unit,"speaking"):{"title":f"{title}: mluvení","objective":f"Mluv samostatně o tématu {title}.","prompt":f"Mluv 1–2 minuty o tématu {title}. Uveď názor, důvod a konkrétní příklad.","phrases":["Podle mého názoru","Například","Na druhé straně","Proto si myslím"],"examples":[example]},
      (level,unit,"writing"):{"title":f"{title}: psaní","objective":f"Napiš souvislý text o tématu {title}.","prompt":f"Napiš text o tématu {title}. Uveď hlavní myšlenku, detaily a závěr.","guidance":["Použij alespoň tři slova z tématu.","Propojuj věty vhodnými spojovacími výrazy.","Zkontroluj gramatickou přesnost."],"examples":[example]},
      (level,unit,"review"):{"title":f"{title}: opakování","objective":f"Zopakuj obsah tématu {title}.","questions":[f"Napiš jednu větu o tématu {title}.","Použij tři nová slova ve vlastních větách.","Shrň hlavní myšlenku ve dvou větách."]}
    }

S={}
for level,units in UNITS.items():
    for unit,title,example,words in units:
        S.update(_make(level,unit,title,example,words))

def get_lesson_seed(level:str, unit_id:str, lesson_type:str)->dict[str,Any]|None:
    return S.get((str(level).upper(),str(unit_id),str(lesson_type).lower()))
