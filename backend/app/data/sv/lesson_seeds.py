"""Curated Swedish A2-C2 lesson seeds for JUBA LISAN."""
from __future__ import annotations
from typing import Any

_UNITS = {
"A2":[("sv-a2-unit-1","Resor","resa"),("sv-a2-unit-2","Hälsa","hälsa"),("sv-a2-unit-3","Arbete","arbete"),("sv-a2-unit-4","Studier","studier"),("sv-a2-unit-5","Possession och vardag","vardag"),("sv-a2-unit-6","Jämförelser","jämförelser"),("sv-a2-unit-7","Begäran","begäran"),("sv-a2-unit-8","A2-repetition","vardag")],
"B1":[("sv-b1-unit-1","Samhälle","samhälle"),("sv-b1-unit-2","Utbildning","utbildning"),("sv-b1-unit-3","Miljö","miljö"),("sv-b1-unit-4","Kommunikation","kommunikation"),("sv-b1-unit-5","Passiv och process","processer"),("sv-b1-unit-6","Villkor","villkor"),("sv-b1-unit-7","Referat","referat"),("sv-b1-unit-8","B1-repetition","diskussion")],
"B2":[("sv-b2-unit-1","Ekonomi","ekonomi"),("sv-b2-unit-2","Förvaltning","förvaltning"),("sv-b2-unit-3","Medier","medier"),("sv-b2-unit-4","Teknik","teknik"),("sv-b2-unit-5","Nominalisering","formellt språk"),("sv-b2-unit-6","Modalitet","modalitet"),("sv-b2-unit-7","Register","register"),("sv-b2-unit-8","B2-repetition","argumentation")],
"C1":[("sv-c1-unit-1","Institutionellt språk","institutionellt språk"),("sv-c1-unit-2","Akademisk argumentation","akademisk argumentation"),("sv-c1-unit-3","Hedging","försiktiga påståenden"),("sv-c1-unit-4","Inbäddade frågor","inbäddade frågor"),("sv-c1-unit-5","Informationsstruktur","informationsstruktur"),("sv-c1-unit-6","Mediespråk","mediespråk"),("sv-c1-unit-7","Pragmatik","pragmatik"),("sv-c1-unit-8","Professionell korrespondens","korrespondens")],
"C2":[("sv-c2-unit-1","Avancerad kohesion","kohesion"),("sv-c2-unit-2","Nyansierad modalitet","nyanser"),("sv-c2-unit-3","Tät nominalisering","nominalisering"),("sv-c2-unit-4","Retorisk organisation","retorik"),("sv-c2-unit-5","Juridiskt språk","juridiskt språk"),("sv-c2-unit-6","Översättningsprecision","översättningsprecision"),("sv-c2-unit-7","Litterär stil","litterär stil"),("sv-c2-unit-8","Diskursanalys","diskursanalys")],
}
_GRAMMAR={
"A2":["preteritum","perfekt","framtid med ska","reflexiva pronomen","possessiva pronomen","komparation","prepositioner och artiga uppmaningar"],
"B1":["bisatser","V2-ordföljd","adverbplacering","relativa satser","passiv","particip","villkor och skulle","refererat tal"],
"B2":["avancerade bisatser","koncession","kohesion","diskursmarkörer","informationsstruktur","nominalisering","modalitet","register"],
"C1":["institutionellt språk","akademisk argumentation","epistemisk hedging","inbäddade frågor","informationspaketering","mediediskurs","pragmatik","professionell korrespondens"],
"C2":["avancerad kohesion","modal nyans","tät nominalisering","retorisk progression","juridisk precision","översättningsprecision","litterär stil","diskursanalys"],
}
_WORDS={
"A2":[("resa","trip","Jag ska resa i sommar."),("läkare","doctor","Jag behöver en läkare."),("arbete","work","Jag trivs på mitt arbete."),("kurs","course","Jag går en svenskakurs."),("erfarenhet","experience","Det var en viktig erfarenhet.")],
"B1":[("samhälle","society","Samhället förändras snabbt."),("utbildning","education","Utbildning öppnar nya möjligheter."),("miljö","environment","Vi måste skydda miljön."),("påstående","statement","Påståendet behöver stöd."),("källa","source","Vi bör kontrollera källan.")],
"B2":[("förvaltning","administration","Förvaltningen ansvarar för processen."),("medier","media","Medierna påverkar den offentliga debatten."),("teknikutveckling","technological development","Teknikutvecklingen går snabbt."),("perspektiv","perspective","Det finns flera perspektiv."),("ställningstagande","position","Ett tydligt ställningstagande kräver argument.")],
"C1":[("evidens","evidence","Resultaten ger viss evidens för hypotesen."),("begränsning","limitation","Studien har flera begränsningar."),("slutsats","conclusion","Slutsatsen bör formuleras försiktigt."),("förvaltning","administration","Dokumentet följer institutionella krav."),("tolkning","interpretation","Tolkningen beror på sammanhanget.")],
"C2":[("nyans","nuance","En liten nyans förändrar betydelsen."),("förutsättning","presupposition","Argumentet bygger på en outtalad förutsättning."),("tonfall","tone","Tonfallet kan uppfattas olika."),("register","register","Textens register är konsekvent formellt."),("underförstådd","implicit","Den underförstådda betydelsen framgår av sammanhanget.")],
}
def get_lesson_seed(level:str, unit_id:str, lesson_type:str)->dict[str,Any]|None:
    level=str(level).upper(); skill=str(lesson_type).lower()
    units=dict((u,t) for u,t,_ in _UNITS.get(level,[]))
    title=units.get(str(unit_id))
    if not title or skill not in {"grammar","vocabulary","reading","listening","speaking","writing","review"}: return None
    idx=max(0,[u for u,t,_ in _UNITS[level]].index(unit_id))
    grammar=_GRAMMAR[level]
    words=_WORDS[level]
    examples=[x[2] for x in words]
    focus=grammar[idx % len(grammar)]
    seed={"title":title,"objective":f"Utveckla din svenska genom temat {title}.","grammar":grammar[:4],"words":words,"examples":examples,"source":"curated_swedish"}
    if skill=="grammar":
        seed["objective"]=f"Använd {focus} korrekt i sammanhängande svenska."
    elif skill=="vocabulary":
        seed["objective"]=f"Bygg ett aktivt ordförråd kring {title} och använd orden i egna meningar."
    elif skill=="reading":
        seed["objective"]=f"Läs och tolka en svensk text om {title}."
        seed["text"]=f"{title}. I den här texten behandlas {title.lower()} ur ett praktiskt perspektiv. {examples[0]} {examples[1]} {examples[2]}"
        seed["questions"]=["Vad är textens huvudbudskap?","Vilka två uttryck är särskilt användbara?","Vilken detalj stöder textens huvudidé?"]
    elif skill=="listening":
        seed["objective"]=f"Förstå huvudidé och detaljer i talad svenska om {title}."
        seed["transcript"]=f"Vi ska tala om {title.lower()}. Först beskriver vi situationen, sedan jämför vi olika perspektiv. {examples[0]} {examples[3]}"
        seed["questions"]=["Vad är samtalets huvudämne?","Vilka två detaljer hör du?","Vilket uttryck visar talarens perspektiv?"]
    elif skill=="speaking":
        seed["objective"]=f"Diskutera {title} på svenska och motivera dina synpunkter."
        seed["prompt"]=f"Berätta om {title}. Använd minst tre nya ord och strukturen {focus}."
        seed["phrases"]=examples
    elif skill=="writing":
        seed["objective"]=f"Skriv en sammanhängande text på svenska om {title}."
        seed["prompt"]=f"Skriv en text om {title}. Använd minst tre ämnesord och {focus}."
        seed["guidance"]=[f"Använd {focus} korrekt.","Ge minst ett konkret exempel.","Knyt ihop idéerna med tydliga samband."]
    elif skill=="review":
        seed["objective"]=f"Repetera centrala strukturer och uttryck från {title}."
        seed["questions"]=[f"Skapa en mening med {focus}.",f"Använd två ord som hör till {title}.","Formulera samma idé på ett mer precist sätt."]
    return seed
