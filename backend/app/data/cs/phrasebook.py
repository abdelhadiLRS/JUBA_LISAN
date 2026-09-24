"""Czech A1-C2 phrasebook for JUBA LISAN."""
from app.data._types import PhrasebookCategory, PhrasebookEntry

def _p(text, context, register, unit_ref):
    return PhrasebookEntry(text=text, context=context, register=register, unit_ref=unit_ref)

def _cat(id, level, situation, unit_ref, phrases):
    return PhrasebookCategory(id=id, level=level, situation=situation, icon="•", phrases=phrases)

PHRASEBOOK_CATEGORIES = [
_cat("greetings_a1","A1","Pozdravy","cs-a1-1",[_p("Dobrý den.","greeting","neutral","cs-a1-1"),_p("Ahoj, jak se máš?","informal greeting","informal","cs-a1-1"),_p("Nashledanou, mějte se hezky.","farewell","polite","cs-a1-1")]),
_cat("identity_a1","A1","Představování","cs-a1-1",[_p("Jmenuji se Petr.","introducing yourself","neutral","cs-a1-1"),_p("Těší mě.","meeting someone","polite","cs-a1-1"),_p("Odkud jste?","asking origin","polite","cs-a1-1")]),
_cat("family_a1","A1","Rodina","cs-a1-2",[_p("To je moje rodina.","talking about family","neutral","cs-a1-2"),_p("Mám jednoho bratra.","family information","neutral","cs-a1-2"),_p("Bydlím s rodiči.","living arrangement","neutral","cs-a1-2")]),
_cat("home_a2","A2","Bydlení","cs-a2-1",[_p("Bydlím v centru.","location","neutral","cs-a2-1"),_p("Hledám větší byt.","housing search","neutral","cs-a2-1"),_p("Je tu volný pokoj?","asking about availability","polite","cs-a2-1")]),
_cat("neighborhood_a2","A2","Okolí","cs-a2-1",[_p("Kde je nejbližší obchod?","asking directions","polite","cs-a2-1"),_p("Park je nedaleko.","describing location","neutral","cs-a2-1"),_p("Jak se dostanu na náměstí?","asking for directions","polite","cs-a2-1")]),
_cat("travel_a2","A2","Cestování","cs-a2-2",[_p("Mám rezervaci.","hotel or travel reservation","neutral","cs-a2-2"),_p("V kolik hodin odjíždí vlak?","asking departure time","polite","cs-a2-2"),_p("Kde si mohu koupit jízdenku?","buying a ticket","polite","cs-a2-2")]),
_cat("education_b1","B1","Vzdělávání","cs-b1-1",[_p("Studuji na vysoké škole.","talking about studies","neutral","cs-b1-1"),_p("Zkouška bude příští týden.","talking about an exam","neutral","cs-b1-1"),_p("Chci si rozšířit znalosti.","learning goal","neutral","cs-b1-1")]),
_cat("goals_b1","B1","Cíle","cs-b1-1",[_p("Mým cílem je mluvit plynně.","stating a goal","neutral","cs-b1-1"),_p("Chci se v tom zlepšit.","personal improvement","neutral","cs-b1-1"),_p("Postupně dělám pokroky.","describing progress","neutral","cs-b1-1")]),
_cat("career_b1","B1","Kariéra","cs-b1-2",[_p("Hledám novou pracovní pozici.","job search","neutral","cs-b1-2"),_p("Mám několik let zkušeností.","describing experience","neutral","cs-b1-2"),_p("Kdy bude pracovní pohovor?","asking about an interview","polite","cs-b1-2")]),
_cat("debate_b2","B2","Debata","cs-b2-1",[_p("Domnívám se, že...","stating an opinion","neutral","cs-b2-1"),_p("S tímto názorem nesouhlasím.","disagreeing","neutral","cs-b2-1"),_p("Můžete svůj argument upřesnit?","requesting clarification","polite","cs-b2-1")]),
_cat("argument_b2","B2","Argumentace","cs-b2-1",[_p("Toto tvrzení vyžaduje důkaz.","requesting evidence","neutral","cs-b2-1"),_p("Tento závěr z dat nevyplývá.","challenging a conclusion","formal","cs-b2-1"),_p("Je třeba zvážit také druhou možnost.","introducing an alternative","formal","cs-b2-1")]),
_cat("culture_b2","B2","Kultura","cs-b2-2",[_p("Tato tradice má dlouhou historii.","discussing tradition","neutral","cs-b2-2"),_p("Kulturní rozdíly mohou být přínosné.","discussing diversity","neutral","cs-b2-2"),_p("Výstava mě velmi zaujala.","reacting to an exhibition","neutral","cs-b2-2")]),
_cat("academic_c1","C1","Akademický jazyk","cs-c1-1",[_p("Výzkum se zaměřuje na...","introducing research","formal","cs-c1-1"),_p("Výsledky naznačují, že...","reporting findings","formal","cs-c1-1"),_p("Tento závěr je třeba interpretovat opatrně.","academic qualification","formal","cs-c1-1")]),
_cat("research_c1","C1","Výzkum","cs-c1-1",[_p("Hypotéza byla potvrzena.","reporting a result","formal","cs-c1-1"),_p("Data byla získána z několika zdrojů.","describing data","formal","cs-c1-1"),_p("Výsledky podporují původní předpoklad.","interpreting findings","formal","cs-c1-1")]),
_cat("professional_c1","C1","Profesní styl","cs-c1-2",[_p("Navrhuji tento postup.","making a proposal","formal","cs-c1-2"),_p("Rád bych zdůraznil hlavní prioritu.","emphasizing a priority","formal","cs-c1-2"),_p("Můžeme tento bod projednat později?","professional discussion","polite","cs-c1-2")]),
_cat("nuance_c2","C2","Nuance","cs-c2-1",[_p("Toto tvrzení je poněkud zavádějící.","qualifying a statement","formal","cs-c2-1"),_p("Rozdíl je jemnější, než se může zdát.","expressing nuance","formal","cs-c2-1"),_p("Výraz má v tomto kontextu specifický odstín významu.","semantic nuance","formal","cs-c2-1")]),
_cat("semantics_c2","C2","Sémantika","cs-c2-1",[_p("Význam závisí na kontextu.","semantic analysis","formal","cs-c2-1"),_p("Tento výraz může mít dvojí interpretaci.","ambiguity","formal","cs-c2-1"),_p("Je třeba rozlišit mezi těmito dvěma pojmy.","semantic distinction","formal","cs-c2-1")]),
_cat("argument_c2","C2","Pokročilá argumentace","cs-c2-2",[_p("Tento předpoklad není dostatečně podložen.","challenging an assumption","formal","cs-c2-2"),_p("Z toho nelze jednoznačně vyvodit závěr.","limiting an inference","formal","cs-c2-2"),_p("Protiargument stojí na jiné premise.","comparing arguments","formal","cs-c2-2")]),
]
