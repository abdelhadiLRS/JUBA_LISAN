"""Czech A1-C2 foundation data for JUBA LISAN."""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry,
    VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

def _g(slug, title, level, category, explanation, examples):
    return GrammarTopic(
        slug=slug, title=title, level=level, category=category,
        summary=f"Čeština {level}: {title}.",
        explanation=explanation,
        examples=[GrammarExample(text=x) for x in examples],
    )

GRAMMAR_TOPICS = [
    _g("pronouns","Osobní zájmena","A1","syntax","Používej osobní zájmena pro představení a běžnou komunikaci.",["Já jsem Anna.","Ty jsi student."]),
    _g("identity","Sloveso být a identita","A1","verbs","Tvoř jednoduché věty o identitě, povolání a původu.",["Jsem z Prahy.","On je učitel."]),
    _g("present","Přítomný čas","A1","verbs","Používej přítomný čas pro děje a pravidelné činnosti.",["Pracuji každý den.","Učíme se česky."]),
    _g("word-order","Základní slovosled","A1","syntax","Tvoř jednoduché oznamovací věty a přirozeně umisťuj slova.",["Bydlím v Brně.","Dnes pracuji doma."]),
    _g("questions","Otázky a tázací slova","A1","communication","Ptej se pomocí kdo, co, kde, kdy, proč a jak.",["Kde bydlíš?","Co děláš?"]),
    _g("negation","Zápor","A1","syntax","Tvoř záporné věty pomocí ne a rozlišuj základní záporné výrazy.",["Nerozumím.","Dnes nejdu do práce."]),
    _g("gender","Rod podstatných jmen","A1","nouns","Rozpoznávej mužský, ženský a střední rod u běžných slov.",["Ten muž je doma.","Ta žena pracuje."]),
    _g("cases-intro","Pády v základních větách","A1","cases","Seznam se s funkcí pádů v jednoduchých větách a ustálených spojeních.",["Jdu do školy.","Mluvím s Janou."]),
    _g("past","Minulý čas","A2","verbs","Vyprávěj o minulých událostech pomocí minulého času.",["Včera jsem pracoval.","Byla doma."]),
    _g("future","Budoucí čas","A2","verbs","Mluv o plánech, záměrech a očekávaných událostech.",["Zítra budu pracovat.","Příští týden pojedeme do Brna."]),
    _g("modal","Modální slovesa","A2","verbs","Vyjadřuj možnost, povinnost, schopnost a přání pomocí muset, moci, umět a chtít.",["Musím odejít.","Můžu vám pomoci?"]),
    _g("aspect","Vid dokonavý a nedokonavý","A2","verbs","Rozlišuj průběh a dokončení děje pomocí slovesného vidu.",["Čtu knihu.","Přečetl jsem knihu."]),
    _g("accusative","Akuzativ","A2","cases","Používej čtvrtý pád pro přímý předmět a některé směrové výrazy.",["Vidím svého bratra.","Kupuji novou knihu."]),
    _g("locative","Lokál a předložkové vazby","A2","cases","Používej lokál po běžných předložkách při vyjádření místa a tématu.",["Bydlím v Praze.","Mluvíme o práci."]),
    _g("comparatives","Stupňování přídavných jmen","A2","adjectives","Porovnávej osoby, věci a situace pomocí druhého a třetího stupně.",["Tento dům je větší.","To je nejlepší možnost."]),
    _g("reflexive","Zvratná slovesa","A2","verbs","Používej se a si ve zvratných slovesech a běžných vazbách.",["Učím se česky.","Ráno se sprchuji."]),
    _g("conditional","Podmiňovací způsob","B1","verbs","Vyjadřuj hypotetické situace, přání a zdvořilé žádosti.",["Kdybych měl čas, přijel bych.","Chtěl bych se zeptat."]),
    _g("relative","Vztažné věty","B1","syntax","Rozšiřuj podstatná jména pomocí který, která, které a dalších vztažných zájmen.",["To je kniha, kterou čtu.","Znám člověka, který tu pracuje."]),
    _g("subordinate","Vedlejší věty","B1","syntax","Spojuj věty pomocí že, protože, když, aby, i když a dalších spojek.",["Vím, že přijde.","Zůstanu doma, protože prší."]),
    _g("reported","Nepřímá řeč","B1","discourse","Převáděj přímé výroky do nepřímé řeči a zachovej jejich význam.",["Řekl, že přijde zítra.","Zeptala se, jestli mám čas."]),
    _g("purpose","Účelové věty","B1","syntax","Vyjadřuj účel pomocí aby a dalších konstrukcí.",["Přišel jsem, abych vám pomohl.","Učí se, aby udělal zkoušku."]),
    _g("cause","Příčina a důsledek","B1","discourse","Vyjadřuj důvody a následky pomocí protože, proto, takže a dalších výrazů.",["Nešel ven, protože pršelo.","Byl unavený, takže odešel."]),
    _g("prepositions","Předložkové vazby","B1","cases","Ovládej běžné vazby předložek s různými pády.",["Zajímám se o historii.","Záleží na výsledku."]),
    _g("motion","Směr, pohyb a umístění","B1","cases","Rozlišuj kde, kam a odkud a vybírej odpovídající pád.",["Jdu do školy.","Jsem ve škole.","Jdu ze školy."]),
    _g("passive","Trpný rod","B2","syntax","Používej opisný i zvratný pasivní způsob v odborném a neutrálním textu.",["Dokument byl podepsán.","Dům se staví."]),
    _g("causative","Kauzativní význam","B2","verbs","Vyjadřuj způsobení nebo zajištění děje pomocí přirozených českých konstrukcí.",["Nechal jsem opravit auto.","Donutili ho odejít."]),
    _g("aspect-nuance","Nuance slovesného vidu","B2","verbs","Vol správný vid podle fáze, opakování a výsledku děje.",["Celé ráno jsem psal.","Dopis jsem napsal za hodinu."]),
    _g("nominalization","Nominalizace","B2","style","Převáděj dějové informace do formálních jmenných konstrukcí.",["Realizace projektu začala v lednu.","Hodnocení výsledků pokračuje."]),
    _g("concession","Kontrast a ústupek","B2","syntax","Vyjadřuj protiklad a ústupek pomocí ačkoli, přestože, přesto a přestože.",["Ačkoli pršelo, pokračovali jsme.","Byl unavený, přesto pracoval."]),
    _g("connectors","Diskurzní spojovací prostředky","B2","discourse","Organizuj delší text pomocí prostředků pro pořadí, příčinu, kontrast a závěr.",["Nejprve popíšeme problém, poté navrhneme řešení."]),
    _g("formal-register","Formální a institucionální styl","C1","register","Přizpůsobuj slovní zásobu a gramatiku úředním, pracovním a akademickým situacím.",["Žádost musí být podána do pátku.","Dovolujeme si vás požádat o potvrzení."]),
    _g("hedging","Akademická opatrnost","C1","academic","Vyjadřuj míru jistoty pomocí podle všeho, pravděpodobně, lze předpokládat a podobných prostředků.",["Výsledky pravděpodobně souvisejí s touto změnou.","Lze předpokládat, že trend bude pokračovat."]),
    _g("embedded","Vložené otázky","C1","syntax","Používej nepřímé a vložené otázky v běžné i formální komunikaci.",["Nevím, kdy přijde.","Můžete mi říct, kde je nádraží?"]),
    _g("information-structure","Informační struktura","C1","discourse","Pracuj s tématem, ohniskem, důrazem a pořadím nové informace.",["Právě tento problém je nejdůležitější.","Co se týče výsledků, ty jsou přesvědčivé."]),
    _g("argumentation","Akademická argumentace","C2","rhetoric","Buduj tvrzení, důkazy, omezení a protiargumenty v komplexním textu.",["Na základě dostupných údajů lze tento závěr obhájit.","Tento argument však přehlíží jinou možnost."]),
    _g("pragmatics","Pragmatika a zdvořilost","C2","pragmatics","Interpretuj nepřímé významy, zdvořilost, společenský kontext a komunikační záměr.",["Pokud by to bylo možné, mohl byste to ověřit?","Možná by bylo vhodnější návrh ještě upravit."]),
    _g("rhetoric","Rétorika a styl","C2","rhetoric","Používej a interpretuj kontrast, paralelismus, metaforu a další rétorické prostředky.",["Nejde jen o čísla; jde především o jejich význam."]),
    _g("idioms","Idiomy a frazeologie","C2","lexis","Rozuměj idiomatickým výrazům podle kontextu a nepřekládej je mechanicky.",["Držet někomu palce znamená přát mu úspěch.","To je jen špička ledovce."]),
    _g("translation","Přesnost překladu a parafráze","C2","translation","Přeformuluj význam bez ztráty registru, významových odstínů a komunikační funkce.",["Tuto myšlenku lze vyjádřit i jinak.","Je třeba zachovat význam i tón textu."]),
    _g("discourse-analysis","Analýza diskurzu","C2","discourse","Analyzuj soudržnost, postoje, žánr a změny registru v delších českých textech.",["Volba výrazů se mění podle publika a účelu textu.","Formální text vyžaduje přesnější styl."]),
]

def _v(id_, level, topic, ref, rows):
    return VocabularySet(
        id=id_, level=level, topic=topic, unit_ref=ref,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w,p,d,e in rows],
    )

VOCABULARY_SETS = [
    _v("cs-a1-1","A1","Pozdravy","cs-a1-unit-1",[("Dobrý den","phrase","good day / hello","Dobrý den!"),("Ahoj","phrase","hello / bye","Ahoj, jak se máš?"),("děkuji","verb","thank you","Děkuji vám."),("prosím","phrase","please / you're welcome","Prosím, posaďte se.")]),
    _v("cs-a1-2","A1","Představení","cs-a1-unit-2",[("jméno","noun","name","Jaké je vaše jméno?"),("země","noun","country","Česká republika je moje země."),("město","noun","city","Bydlím ve městě."),("student","noun","student","Jsem student.")]),
    _v("cs-a1-3","A1","Rodina","cs-a1-unit-3",[("matka","noun","mother","Moje matka pracuje."),("otec","noun","father","Můj otec je doma."),("sestra","noun","sister","Moje sestra studuje."),("bratr","noun","brother","Můj bratr bydlí v Praze.")]),
    _v("cs-a1-4","A1","Domov","cs-a1-unit-4",[("dům","noun","house","Náš dům je velký."),("pokoj","noun","room","Můj pokoj je nahoře."),("kuchyně","noun","kitchen","Kuchyně je vedle pokoje."),("stůl","noun","table","Kniha je na stole.")]),
    _v("cs-a1-5","A1","Denní rutina","cs-a1-unit-5",[("ráno","noun","morning","Ráno vstávám v sedm."),("práce","noun","work","Jdu do práce."),("škola","noun","school","Děti jsou ve škole."),("večer","noun","evening","Večer čtu.")]),
    _v("cs-a1-6","A1","Jídlo a pití","cs-a1-unit-6",[("voda","noun","water","Prosím sklenici vody."),("chléb","noun","bread","Kupuji čerstvý chléb."),("káva","noun","coffee","Dám si kávu."),("jablko","noun","apple","Jím jablko.")]),
    _v("cs-a1-7","A1","Místa a doprava","cs-a1-unit-7",[("nádraží","noun","station","Nádraží je blízko."),("ulice","noun","street","Bydlím v této ulici."),("autobus","noun","bus","Čekám na autobus."),("centrum","noun","centre","Jdu do centra.")]),
    _v("cs-a1-8","A1","Každodenní komunikace","cs-a1-unit-8",[("pomoc","noun","help","Potřebuji pomoc."),("rozumět","verb","understand","Nerozumím otázce."),("opakovat","verb","repeat","Můžete to zopakovat?"),("otázka","noun","question","Mám jednu otázku.")]),
    _v("cs-a2-1","A2","Minulost","cs-a2-unit-1",[("včera","adverb","yesterday","Včera jsem byl doma."),("minulý","adjective","last / previous","Minulý týden jsem pracoval."),("navštívit","verb","visit","Navštívil jsem Prahu."),("začít","verb","begin","Kurz začal v pondělí.")]),
    _v("cs-a2-2","A2","Plány a budoucnost","cs-a2-unit-2",[("zítra","adverb","tomorrow","Zítra budu doma."),("plán","noun","plan","Mám nový plán."),("budoucnost","noun","future","Myslíme na budoucnost."),("cestovat","verb","travel","Chci cestovat po Evropě.")]),
    _v("cs-a2-3","A2","Povinnost a možnost","cs-a2-unit-3",[("muset","verb","must / have to","Musím odejít."),("moci","verb","can / may","Můžete mi pomoci?"),("chtít","verb","want","Chci se učit."),("umět","verb","know how to","Umím trochu česky.")]),
    _v("cs-a2-4","A2","Město a služby","cs-a2-unit-4",[("úřad","noun","office / authority","Úřad je otevřený."),("lékárna","noun","pharmacy","Lékárna je za rohem."),("banka","noun","bank","Banka zavírá v pět."),("pošta","noun","post office","Jdu na poštu.")]),
    _v("cs-b1-1","B1","Podmínky","cs-b1-unit-1",[("kdyby","conjunction","if / were it that","Kdybych měl čas, přijel bych."),("možnost","noun","possibility","Je to zajímavá možnost."),("podmínka","noun","condition","To je důležitá podmínka."),("rozhodnutí","noun","decision","Musíme udělat rozhodnutí.")]),
    _v("cs-b1-2","B1","Popis a vztahy","cs-b1-unit-2",[("který","pronoun","which / who","Člověk, který tu pracuje, je můj kolega."),("souviset","verb","be related","Tyto problémy spolu souvisejí."),("vztah","noun","relationship","Jejich vztah se změnil."),("prostředí","noun","environment","Pracovní prostředí je důležité.")]),
    _v("cs-b1-3","B1","Důvody a účel","cs-b1-unit-3",[("důvod","noun","reason","Jaký je důvod změny?"),("účel","noun","purpose","Účelem projektu je pomoc studentům."),("protože","conjunction","because","Zůstanu doma, protože prší."),("aby","conjunction","so that / in order to","Učí se, aby uspěl.")]),
    _v("cs-b1-4","B1","Práce a studium","cs-b1-unit-4",[("zkušenost","noun","experience","Mám pracovní zkušenosti."),("dovednost","noun","skill","Tato dovednost je užitečná."),("projekt","noun","project","Pracuji na novém projektu."),("zkouška","noun","exam","Zítra mám zkoušku.")]),
    _v("cs-b2-1","B2","Procesy","cs-b2-unit-1",[("proces","noun","process","Proces trvá několik týdnů."),("výsledek","noun","result","Výsledek je pozitivní."),("provést","verb","carry out","Kontrola byla provedena včas."),("zpracovat","verb","process","Data byla zpracována.")]),
    _v("cs-b2-2","B2","Kontrast a ústupek","cs-b2-unit-2",[("ačkoli","conjunction","although","Ačkoli pršelo, šli jsme ven."),("přesto","adverb","nevertheless","Byl unavený, přesto pokračoval."),("zatímco","conjunction","while / whereas","Zatímco pracoval, poslouchal hudbu."),("naopak","adverb","on the contrary","Naopak, druhý návrh je jednodušší.")]),
    _v("cs-b2-3","B2","Formální komunikace","cs-b2-unit-3",[("žádost","noun","application / request","Žádost byla podána včas."),("potvrzení","noun","confirmation","Potřebuji písemné potvrzení."),("lhůta","noun","deadline / period","Lhůta končí v pátek."),("příloha","noun","attachment","Dokument je v příloze.")]),
    _v("cs-b2-4","B2","Média a společnost","cs-b2-unit-4",[("zpráva","noun","report / news","Četl jsem zajímavou zprávu."),("veřejnost","noun","public","Veřejnost potřebuje informace."),("vliv","noun","influence","Média mají velký vliv."),("diskuse","noun","discussion","Diskuse pokračovala hodinu.")]),
]

_UNIT_TITLES = {
"A1":["Pozdravy a představení","Rodina a vlastnictví","Domov a každodenní život","Čas a schůzky","Jídlo a nakupování","Místa a směry","Doprava a služby","Každodenní komunikace"],
"A2":["Minulé události","Budoucí plány","Možnost a povinnost","Město a služby","Porovnávání a preference","Zdraví a rutina","Cestování","Praktické vyprávění"],
"B1":["Podmínky a hypotézy","Vztažné věty","Důvody a účel","Nepřímá řeč","Příčiny a důsledky","Práce a studium","Směr a prostor","Spojování argumentů"],
"B2":["Trpný rod a procesy","Kontrast a ústupek","Formální komunikace","Profesní popis","Komplexní souvětí","Média a společnost","Nominalizace","Integrované dovednosti"],
"C1":["Institucionální jazyk","Akademická opatrnost","Vložené otázky","Informační struktura","Analýza důkazů","Odborné psaní","Prezentace a diskuse","Pokročilá syntéza"],
"C2":["Argumentace a protiargument","Pragmatika","Rétorika","Idiomy a nuance","Překlad a parafráze","Analýza diskurzu","Literární styl","Jazykové mistrovství"],
}
GRAMMAR_BY_LEVEL = {level:[g for g in GRAMMAR_TOPICS if g.level==level] for level in LEVELS}
VOCAB_BY_LEVEL = {level:[v for v in VOCABULARY_SETS if v.level==level] for level in LEVELS}
CURRICULUM = {}
for level in LEVELS:
    CURRICULUM[level] = []
    gs = GRAMMAR_BY_LEVEL[level]
    vs = VOCAB_BY_LEVEL[level]
    for i, title in enumerate(_UNIT_TITLES[level], 1):
        CURRICULUM[level].append(CurriculumUnit(
            id=f"cs-{level.lower()}-unit-{i}", level=level, unit_number=i,
            title=f"Čeština {level} · {title}",
            grammar_points=[gs[(i-1) % len(gs)].slug],
            vocabulary_set_ids=[vs[(i-1) % len(vs)].id] if vs else [],
            lesson_types=["grammar","vocabulary","reading","writing","listening","speaking","review"],
            competency_checklist=[f"Komunikovat česky na úrovni {level} v tématu: {title}.","Použít cílovou gramatiku v samostatném úkolu."],
            default_weeks=2,
        ))

_PHRASES = [
("Pozdravy","👋",["Dobrý den!","Ahoj, jak se máte?","Těší mě.","Na shledanou."]),
("Představení","🪪",["Jmenuji se ...","Odkud jste?","Bydlím v ...","Pracuji jako ..."]),
("Nakupování","🛒",["Kolik to stojí?","Mohu si to vyzkoušet?","Máte to v jiné velikosti?","Zaplatím kartou."]),
("Cestování","🧳",["Kde je nádraží?","Jeden lístek, prosím.","V kolik hodin odjíždí vlak?","Potřebuji najít hotel."]),
("Zdraví","🩺",["Necítím se dobře.","Potřebuji lékaře.","Mám objednaný termín.","Kde je lékárna?"]),
("Práce","💼",["Můžeme to projednat?","Pošlu vám dokument.","Kdy je schůzka?","Souhlasím s návrhem."]),
("Studium","🎓",["Nerozumím této části.","Můžete to vysvětlit?","Potřebuji více času.","Kdy bude zkouška?"]),
("Názory","💭",["Podle mého názoru ...","Souhlasím s vámi.","Rozumím vašemu argumentu.","Vidím to trochu jinak."]),
("Porady","📅",["Navrhuji, abychom ...","Vraťme se k hlavnímu bodu.","Můžeme pokračovat?","Shrňme dosavadní závěry."]),
("Úřady","🏛️",["Mohl byste to písemně potvrdit?","Žádost musí být podána do pátku.","Které dokumenty potřebuji?","Děkuji za vyřízení."]),
("Akademické prostředí","📚",["Výsledky naznačují, že ...","Na základě dostupných údajů ...","Tento závěr vyžaduje další ověření.","Je třeba rozlišovat mezi ..."]),
("Debata","⚖️",["Dovolte mi reagovat na tento argument.","Tento pohled má své limity.","Naopak lze tvrdit, že ...","Podstatný je především kontext."]),
("Pokročilý styl","✍️",["Jinými slovy ...","Z hlediska širšího kontextu ...","Tato formulace připouští několik výkladů.","Je vhodné zachovat původní význam i tón."]),
]
PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id=f"cs-phrases-{i}", level=("A1" if i<=3 else "A2" if i<=5 else "B1" if i<=8 else "B2" if i<=10 else "C1" if i<=12 else "C2"), situation=s, icon=icon,
        phrases=[PhrasebookEntry(text=p, context=s, register="neutral") for p in phrases])
    for i,(s,icon,phrases) in enumerate(_PHRASES,1)
]

ASSESSMENT_BANK = [
    AssessmentQuestion(id="cs-a1-001",skill="communication",difficulty="A1",question="Jak pozdravíte člověka formálně?",options=["Dobrý den!","Ahoj!","Dobrou chuť!","Na zdraví!"],correct="Dobrý den!"),
    AssessmentQuestion(id="cs-a1-002",skill="grammar",difficulty="A1",question="Která věta znamená „I am a student“?",options=["Jsem student.","Jsem doma.","Mám studenta.","Studuji včera."],correct="Jsem student."),
    AssessmentQuestion(id="cs-a1-003",skill="vocabulary",difficulty="A1",question="Co znamená slovo „nádraží“?",options=["station","pharmacy","school","office"],correct="station"),
    AssessmentQuestion(id="cs-a2-001",skill="grammar",difficulty="A2",question="Která věta správně vyjadřuje minulost?",options=["Včera jsem pracoval.","Včera budu pracovat.","Včera pracuji.","Včera pracuj."],correct="Včera jsem pracoval."),
    AssessmentQuestion(id="cs-a2-002",skill="communication",difficulty="A2",question="Jak požádáte o pomoc zdvořile?",options=["Můžete mi pomoci?","Pomoc ty!","Pomáhat včera.","Já pomoc."],correct="Můžete mi pomoci?"),
    AssessmentQuestion(id="cs-b1-001",skill="grammar",difficulty="B1",question="Která věta správně vyjadřuje podmínku?",options=["Kdybych měl čas, přijel bych.","Kdybych mám čas, přijdu.","Když bych měl čas, přijel.","Mám čas, kdyby přijel."],correct="Kdybych měl čas, přijel bych."),
    AssessmentQuestion(id="cs-b1-002",skill="reading",difficulty="B1",question="Vyberte vhodnou větu pro vyjádření účelu.",options=["Učí se, aby uspěl.","Učí se, protože uspěl.","Učí se, přesto uspěl.","Učí se, který uspěl."],correct="Učí se, aby uspěl."),
    AssessmentQuestion(id="cs-b2-001",skill="grammar",difficulty="B2",question="Která věta používá trpný rod?",options=["Dokument byl podepsán.","Podepsal jsem dokument.","Podepisuji dokument.","Dokument leží na stole."],correct="Dokument byl podepsán."),
    AssessmentQuestion(id="cs-b2-002",skill="writing",difficulty="B2",question="Která formulace je vhodná pro formální žádost?",options=["Dovolujeme si vás požádat o potvrzení.","Hej, potvrďte to.","Chci to hned.","Řekněte mi to, jo?"],correct="Dovolujeme si vás požádat o potvrzení."),
    AssessmentQuestion(id="cs-c1-001",skill="academic",difficulty="C1",question="Který výraz vhodně vyjadřuje akademickou opatrnost?",options=["Lze předpokládat, že ...","Je to určitě vždy tak.","Nikdy to není jinak.","Všichni to vědí."],correct="Lze předpokládat, že ..."),
    AssessmentQuestion(id="cs-c1-002",skill="discourse",difficulty="C1",question="Která věta obsahuje vloženou otázku?",options=["Nevím, kdy přijde.","Kdy přijde?","Přijde zítra.","Přišel včera."],correct="Nevím, kdy přijde."),
    AssessmentQuestion(id="cs-c2-001",skill="pragmatics",difficulty="C2",question="Která formulace je nepřímá a zdvořilá žádost?",options=["Mohl byste to prosím ověřit?","Ověř to!","Ty to ověříš.","Ověřil včera."],correct="Mohl byste to prosím ověřit?"),
    AssessmentQuestion(id="cs-c2-002",skill="rhetoric",difficulty="C2",question="Která věta obsahuje kontrastní argumentační rámování?",options=["Tento pohled má své limity, naopak lze tvrdit, že ...","Toto je stůl.","Bydlím v Praze.","Včera jsem pracoval."],correct="Tento pohled má své limity, naopak lze tvrdit, že ..."),
]
