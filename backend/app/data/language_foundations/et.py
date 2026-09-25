"""Estonian A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

def _g(slug,title,level,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=f"Estonian {level} grammar.",explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[
_g("pronouns","Personal pronouns","A1","Use personal pronouns in basic reference.",["Mina olen õpilane.","Tema on õpetaja."]),
_g("copula","Olema and nominal predicates","A1","Form identity and classification sentences.",["See on maja.","Ma olen õpilane."]),
_g("questions","Question words and yes-no questions","A1","Ask basic who, what, where and how questions.",["Mis see on?","Kus sa oled?"]),
_g("present","Present tense","A1","Describe current and habitual actions.",["Ma õpin eesti keelt.","Ta töötab siin."]),
_g("negation","Negation with ei","A1","Negate finite present-tense clauses.",["Ma ei tööta täna.","See ei ole raamat."]),
_g("partitive","Basic partitive case","A1","Use partitive forms for quantities and objects.",["Ma joon vett.","Ma söön leiba."]),
_g("plural","Plural nouns","A1","Form and use plural noun phrases.",["Need on raamatud.","Minu sõbrad tulevad."]),
_g("location","Inessive and adessive location","A1","Express where people and objects are.",["Ma olen kodus.","Raamat on laual."]),
_g("past","Simple past","A2","Describe completed past events.",["Ma käisin poes.","Ta tuli eile."]),
_g("future","Future meaning with present and expressions","A2","Express future plans and expectations.",["Homme lähen tööle.","Järgmisel nädalal õpin."]),
_g("illative","Illative, inessive and elative","A2","Express movement into, being in and movement out of places.",["Lähen kooli.","Olen koolis."]),
_g("elative","Elative and source relations","A2","Express movement or information from a source.",["Tulime Tallinnast.","Sain kirja sõbralt."]),
_g("genitive","Genitive and possession","A2","Build possessive and dependent noun phrases.",["See on minu venna auto.","Õpilase raamat on laual."]),
_g("comparatives","Comparative and superlative","A2","Compare qualities and quantities.",["See on suurem.","Ta on kõige kiirem."]),
_g("imperative","Imperative and polite requests","A2","Give instructions and requests.",["Tule siia!","Palun istu."]),
_g("modality","Modal verbs and necessity","A2","Express ability, possibility and obligation.",["Ma saan tulla.","Pean õppima."]),
_g("object_cases","Object case choice","B1","Distinguish total and partial object meanings.",["Ma loen raamatut.","Ma lugesin raamatu läbi."]),
_g("perfect","Perfect and pluperfect","B1","Connect past events with present relevance and anteriority.",["Ma olen seda näinud.","Ta oli juba läinud."]),
_g("conditional","Conditional mood","B1","Express hypothetical situations and polite wishes.",["Ma läheksin hea meelega.","Kui oleks aega, tuleksin."]),
_g("subjunctive_impersonal","Impersonal and necessity constructions","B1","Use impersonal forms for general statements and necessity.",["Tuleb rohkem õppida.","On vaja otsustada."]),
_g("relative","Relative clauses","B1","Modify nouns with kes, mis and related forms.",["See on raamat, mida ma loen.","Inimene, kes tuli, on õpetaja."]),
_g("conjunctions","Subordination and conjunctions","B1","Link clauses for time, cause, condition and contrast.",["Kui sajab, jään koju.","Ma läksin, sest mul oli aega."]),
_g("reported","Reported speech","B1","Report statements and questions.",["Ta ütles, et tuleb homme.","Ma ei tea, kus ta on."]),
_g("reflexive","Reflexive and reciprocal meaning","B1","Express self-directed and reciprocal actions.",["Ta peseb ennast.","Nad aitasid üksteist."]),
_g("passive","Passive voice","B2","Use impersonal and passive constructions.",["Raamat loetakse läbi.","Maja ehitati eelmisel aastal."]),
_g("participles","Participles and participial phrases","B2","Use participles to compress clauses and describe events.",["Lugenud raamatu läbi, läks ta koju.","Kirjutatud tekst oli selge."]),
_g("infinitives","Infinitive constructions","B2","Use ma- and da-infinitive patterns with verbs and complements.",["Ma tahan õppida.","Ta hakkas tööle."]),
_g("concessive","Concession and contrast","B2","Express although, despite and contrast relations.",["Kuigi vihma sadas, läksime välja.","Sellest hoolimata jätkas ta."]),
_g("discourse","Discourse connectors and cohesion","B2","Organize extended speech with logical connectors.",["Esiteks selgitame probleemi. Seejärel vaatame lahendust."]),
_g("nominalization","Nominalization and formal syntax","C1","Build dense formal noun phrases from processes.",["Hariduse arendamine on oluline.","Otsuse tegemine võttis aega."]),
_g("hedging","Academic hedging and stance","C1","Qualify claims and express degrees of certainty.",["Võib oletada, et tulemus muutub.","Tõenäoliselt on põhjus teine."]),
_g("embedded","Embedded questions and complements","C1","Embed questions and propositions in formal syntax.",["Küsimus on selles, kuidas seda teha.","Ma ei tea, mida ta mõtleb."]),
_g("information_structure","Word order, topic and focus","C1","Use flexible Estonian word order to manage information structure.",["Selle raamatu ostsin ma eile.","Just tema tegi otsuse."]),
_g("formal","Formal and institutional Estonian","C1","Adapt syntax and vocabulary for administration and professional writing.",["Palume dokumendi esitada tähtajaks.","Taotlus vaadatakse läbi."]),
_g("argumentation","Academic argumentation and counterargument","C1","Build claims, evidence, qualifications and rebuttals.",["Andmed toetavad seda järeldust.","Samas tuleb arvestada teise võimalusega."]),
_g("pragmatics","Politeness and pragmatic nuance","C2","Interpret indirectness, stance and context.",["Kui võimalik, palun vaadake see üle.","Võib-olla oleks parem seda veel arutada."]),
_g("rhetoric","Rhetorical and literary style","C2","Use contrast, repetition, metaphor and rhetorical framing.",["See ei ole ainult probleem, vaid ka võimalus."]),
_g("register","Register shifting and genre","C2","Shift between colloquial, professional, academic and literary Estonian.",["Ametlikus tekstis on sõnavalik täpsem.","Kõnekeelne väljend sobib teistsugusesse olukorda."]),
_g("translation","Translation precision and paraphrase","C2","Preserve meaning, register and discourse function across reformulation.",["Mõtet saab väljendada teisel viisil.","Tõlge peab säilitama teksti tooni."]),
_g("discourse_analysis","Discourse analysis","C2","Analyze cohesion, stance, genre, audience and rhetorical structure.",["Teksti toon sõltub adressaadist.","Argumentatsiooni struktuur mõjutab tõlgendust."])
]

def _v(id_,level,topic,ref,items):
    return VocabularySet(id=id_,level=level,topic=topic,unit_ref=ref,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS=[
_v("greetings_a1","A1","greetings","et-a1-unit-1",[("tere","phrase","hello","Tere!"),("aitäh","phrase","thank you","Aitäh!"),("palun","phrase","please / you are welcome","Palun istu."),("hüvasti","phrase","goodbye","Hüvasti!")]),
_v("family_a1","A1","family","et-a1-unit-2",[("ema","noun","mother","Minu ema on kodus."),("isa","noun","father","Minu isa töötab."),("õde","noun","sister","Mul on õde."),("vend","noun","brother","Mul on vend.")]),
_v("home_a1","A1","home","et-a1-unit-3",[("kodu","noun","home","Ma olen kodus."),("tuba","noun","room","Minu tuba on väike."),("laud","noun","table","Raamat on laual."),("uks","noun","door","Uks on lahti.")]),
_v("daily_a1","A1","daily life","et-a1-unit-4",[("hommik","noun","morning","Hommikul ma töötan."),("sööma","verb","eat","Ma söön."),("jooma","verb","drink","Ma joon vett."),("magama","verb","sleep","Ma lähen magama.")]),
_v("food_a1","A1","food and shopping","et-a1-unit-5",[("vesi","noun","water","Ma joon vett."),("leib","noun","bread","Ma ostan leiba."),("piim","noun","milk","Palun piima."),("hind","noun","price","Mis on hind?")]),
_v("places_a1","A1","places and directions","et-a1-unit-6",[("pood","noun","shop","Pood on lähedal."),("jaam","noun","station","Kus on jaam?"),("parem","adverb","right","Pööra paremale."),("vasak","adverb","left","Pööra vasakule.")]),
_v("communication_a1","A1","communication","et-a1-unit-7",[("abi","noun","help","Vajan abi."),("aitama","verb","help","Kas sa saad mind aidata?"),("aru saama","verb","understand","Ma saan aru."),("aeglaselt","adverb","slowly","Palun räägi aeglaselt.")]),
_v("review_a1","A1","A1 review","et-a1-unit-8",[("sõber","noun","friend","Ta on minu sõber."),("täna","adverb","today","Täna ma töötan."),("homme","adverb","tomorrow","Homme ma õpin."),("aeg","noun","time","Mul on aega.")]),
_v("travel_a2","A2","travel","et-a2-unit-1",[("reis","noun","trip","Meie reis oli huvitav."),("lennujaam","noun","airport","Lennujaam on kaugel."),("hotell","noun","hotel","Broneerisime hotelli."),("pilet","noun","ticket","Mul on pilet.")]),
_v("health_a2","A2","health","et-a2-unit-2",[("haigus","noun","illness","See haigus vajab ravi."),("ravim","noun","medicine","Võtan ravimit."),("arst","noun","doctor","Arst tuleb varsti."),("tervis","noun","health","Tervis on oluline.")]),
_v("study_a2","A2","study","et-a2-unit-3",[("õppetund","noun","lesson","Õppetund algab kell üheksa."),("eksam","noun","exam","Eksam on homme."),("lugema","verb","read","Ma loen artiklit."),("kirjutama","verb","write","Ta kirjutab vastust.")]),
_v("work_b1","B1","work","et-b1-unit-1",[("ülesanne","noun","task","See on minu ülesanne."),("koosolek","noun","meeting","Koosolek algab varsti."),("projekt","noun","project","Projekt on tähtis."),("otsus","noun","decision","Otsus sündis eile.")]),
_v("society_b1","B1","society","et-b1-unit-2",[("kogukond","noun","community","Kogukond teeb koostööd."),("teenus","noun","service","Teenuse kvaliteet on hea."),("õigus","noun","right","Igaühel on see õigus."),("vastutus","noun","responsibility","Vastutus on suur.")]),
_v("environment_b2","B2","environment","et-b2-unit-1",[("keskkond","noun","environment","Keskkonda tuleb kaitsta."),("reostus","noun","pollution","Reostus vähendab elukvaliteeti."),("jäätmed","noun","waste","Jäätmed tuleb sorteerida."),("ressurss","noun","resource","Ressursid on piiratud.")]),
_v("economy_b2","B2","economy","et-b2-unit-2",[("majandus","noun","economy","Majandus kasvab."),("ettevõte","noun","company","Ettevõte laieneb."),("hind","noun","price","Hind muutus."),("sissetulek","noun","income","Sissetulek suurenes.")]),
_v("media_c1","C1","media","et-c1-unit-1",[("uudis","noun","news item","Uudis levis kiiresti."),("allikas","noun","source","Allikas peab olema usaldusväärne."),("artikkel","noun","article","Lugesin artiklit."),("arvamus","noun","opinion","See on tema arvamus.")]),
_v("academic_c1","C1","academic","et-c1-unit-2",[("uurimus","noun","study / research","Uurimus käsitleb keelt."),("tõend","noun","evidence","Tõend toetab väidet."),("meetod","noun","method","Meetod on läbipaistev."),("järeldus","noun","conclusion","Järeldus põhineb andmetel.")]),
_v("institutional_c1","C1","institutional","et-c1-unit-3",[("poliitika","noun","policy","Uus poliitika jõustus."),("dokument","noun","document","Dokument tuleb esitada."),("taotlus","noun","application","Taotlus on menetluses."),("tähtaeg","noun","deadline","Tähtaeg on homme.")]),
_v("culture_c2","C2","culture","et-c2-unit-1",[("kultuuripärand","noun","cultural heritage","Kultuuripärand vajab kaitset."),("traditsioon","noun","tradition","Traditsioon on vana."),("väärtus","noun","value","See väärtus on oluline."),("vaatenurk","noun","perspective","Tema vaatenurk erineb.")]),
_v("discourse_c2","C2","discourse","et-c2-unit-2",[("diskursus","noun","discourse","Diskursus muutub ajas."),("väide","noun","claim","Väide vajab tõendeid."),("seisukoht","noun","stance","Seisukoht on selge."),("tõlgendus","noun","interpretation","Tõlgendus sõltub kontekstist.")])
]

def _p(id_,level,situation,items,register="neutral"):
    return PhrasebookCategory(id=id_,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=register) for t,c in items])

PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","A1","greetings",[("Tere!","greeting"),("Minu nimi on ...","introducing yourself"),("Meeldiv tutvuda.","meeting someone")]),
_p("thanks_a1","A1","thanks",[("Aitäh.","saying thank you"),("Suur aitäh.","emphasizing thanks"),("Pole tänu väärt.","responding to thanks")]),
_p("shopping_a1","A1","shopping",[("Kui palju see maksab?","asking price"),("Ma soovin seda.","requesting an item"),("Kas saan kaardiga maksta?","payment")]),
_p("directions_a1","A1","directions",[("Kus jaam on?","asking location"),("Mine otse.","giving directions"),("Pööra paremale.","giving directions")]),
_p("help_a1","A1","help",[("Kas sa saad mind aidata?","asking for help"),("Ma ei saa aru.","clarification"),("Palun räägi aeglasemalt.","asking someone to slow down")]),
_p("travel_a2","A2","travel",[("Kus on lennujaam?","asking location"),("Kus hotell asub?","asking accommodation"),("Mul on pilet.","showing a ticket")]),
_p("health_a2","A2","health",[("Mul on halb enesetunne.","describing illness"),("Mul on vaja arsti.","asking for a doctor"),("Kas see ravim sobib?","asking about medicine")]),
_p("study_a2","A2","study",[("Palun selgita uuesti.","asking for explanation"),("Kuidas seda teha?","asking how"),("Ma ei saanud aru.","clarification")]),
_p("work_b1","B1","work",[("Arutame projekti.","starting a work discussion"),("Mul on üks ettepanek.","offering a suggestion"),("Olen sellega nõus.","agreeing")]),
_p("formal_b2","B2","formal communication",[("Palume dokumendi esitada tähtajaks.","formal instruction"),("Teatame, et ...","formal notice"),("Täname koostöö eest.","formal closing")],"formal"),
_p("academic_c1","C1","academic discussion",[("Andmete põhjal ...","introducing evidence"),("Võib oletada, et ...","hedging a claim"),("Teisest küljest ...","introducing contrast")],"academic"),
_p("presentation_c1","C1","presentation",[("Esiteks vaatleme ...","opening a point"),("Peamine küsimus on ...","stating the main point"),("Kokkuvõtteks ...","closing an argument")],"formal"),
_p("pragmatics_c2","C2","pragmatic nuance",[("Kui võimalik, palun ...","softening a request"),("Võib-olla oleks parem ...","tentative suggestion"),("Mõistan teie seisukohta, kuid ...","polite disagreement")],"polite")
]

def _u(level,n,title,grammar,vocab):
    return CurriculumUnit(id=f"et-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=vocab,lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Communicate effectively at {level}",f"Understand level-appropriate Estonian"],default_weeks=2)

CURRICULUM={
"A1":[_u("A1",1,"Tervitused ja tutvumine",["pronouns","copula"],["greetings_a1"]),_u("A1",2,"Perekond",["plural","genitive"],["family_a1"]),_u("A1",3,"Kodu ja asukoht",["location","questions"],["home_a1"]),_u("A1",4,"Igapäevaelu",["present","negation"],["daily_a1"]),_u("A1",5,"Toit ja ostlemine",["partitive","questions"],["food_a1"]),_u("A1",6,"Kohad ja suunad",["location","plural"],["places_a1"]),_u("A1",7,"Suhtlus",["negation","pronouns"],["communication_a1"]),_u("A1",8,"A1 kordamine",["copula","present","partitive"],["review_a1"])],
"A2":[_u("A2",1,"Reisimine",["illative","elative"],["travel_a2"]),_u("A2",2,"Tervis",["imperative","modality"],["health_a2"]),_u("A2",3,"Õppimine",["past","future"],["study_a2"]),_u("A2",4,"Plaanid",["future","comparatives"],["daily_a1","travel_a2"]),_u("A2",5,"Omamine",["genitive","location"],["family_a1","home_a1"]),_u("A2",6,"Võrdlemine",["comparatives","object_cases"],["food_a1","places_a1"]),_u("A2",7,"Kohustused",["modality","imperative"],["work_b1"]),_u("A2",8,"A2 kordamine",["past","illative","modality"],["travel_a2","health_a2"])],
"B1":[_u("B1",1,"Objekti käänded",["object_cases","partitive"],["study_a2"]),_u("B1",2,"Täisminevik",["perfect","past"],["travel_a2"]),_u("B1",3,"Tingimus",["conditional","modality"],["work_b1"]),_u("B1",4,"Suhtelause",["relative","conjunctions"],["society_b1"]),_u("B1",5,"Kaudne kõne",["reported","embedded"],["media_c1"]),_u("B1",6,"Enesele suunatud tegevus",["reflexive","perfect"],["health_a2"]),_u("B1",7,"Põhjus ja tingimus",["conjunctions","conditional"],["environment_b2"]),_u("B1",8,"B1 kordamine",["relative","reported","conditional"],["work_b1","society_b1"])],
"B2":[_u("B2",1,"Passiiv",["passive","participles"],["economy_b2"]),_u("B2",2,"Infinitiivid",["infinitives","modality"],["work_b1"]),_u("B2",3,"Konsessioon",["concessive","discourse"],["society_b1"]),_u("B2",4,"Pikad laused",["conjunctions","relative"],["environment_b2"]),_u("B2",5,"Majandus ja ühiskond",["passive","discourse"],["economy_b2"]),_u("B2",6,"Keskkond",["concessive","conjunctions"],["environment_b2"]),_u("B2",7,"Meedia",["reported","participles"],["media_c1"]),_u("B2",8,"B2 kordamine",["passive","concessive","discourse"],["economy_b2","environment_b2"])],
"C1":[_u("C1",1,"Uurimus ja tõendid",["nominalization","hedging"],["academic_c1"]),_u("C1",2,"Institutsioonid",["formal","argumentation"],["institutional_c1"]),_u("C1",3,"Meedia ja allikad",["information_structure","reported"],["media_c1"]),_u("C1",4,"Varjatud küsimused",["embedded","conjunctions"],["academic_c1"]),_u("C1",5,"Argumentatsioon",["argumentation","discourse"],["academic_c1"]),_u("C1",6,"Ametlik suhtlus",["formal","hedging"],["institutional_c1"]),_u("C1",7,"Teema ja fookus",["information_structure","nominalization"],["media_c1"]),_u("C1",8,"C1 kordamine",["argumentation","formal","embedded"],["academic_c1","institutional_c1"])],
"C2":[_u("C2",1,"Pragmaatika",["pragmatics","register"],["discourse_c2"]),_u("C2",2,"Retoorika",["rhetoric","discourse_analysis"],["culture_c2"]),_u("C2",3,"Registrivahetus",["register","pragmatics"],["institutional_c1"]),_u("C2",4,"Diskursuse analüüs",["discourse_analysis","information_structure"],["discourse_c2"]),_u("C2",5,"Tõlkimine ja ümberütlemine",["translation","register"],["culture_c2"]),_u("C2",6,"Kõrgtasemel argumentatsioon",["argumentation","rhetoric"],["discourse_c2"]),_u("C2",7,"Kirjandus ja meedia",["rhetoric","register"],["culture_c2","media_c1"]),_u("C2",8,"C2 meisterlikkuse kordamine",["translation","pragmatics","discourse_analysis"],["discourse_c2","culture_c2"])]
}

ASSESSMENT_BANK=[
AssessmentQuestion(id="et-a1-001",skill="vocabulary",difficulty="A1",question="What does “aitäh” mean?",options=["hello","thank you","goodbye","help"],correct="thank you"),
AssessmentQuestion(id="et-a1-002",skill="grammar",difficulty="A1",question="Choose the correct sentence.",options=["Mina olen õpilane.","Mina on õpilane.","Mina õpilane olen.","Õpilane mina on."],correct="Mina olen õpilane."),
AssessmentQuestion(id="et-a1-003",skill="grammar",difficulty="A1",question="Which sentence is negative?",options=["Ma ei tööta täna.","Ma töötan täna.","Ma olen kodus.","See on raamat."],correct="Ma ei tööta täna."),
AssessmentQuestion(id="et-a1-004",skill="grammar",difficulty="A2",question="Which sentence shows movement into a place?",options=["Lähen kooli.","Olen koolis.","Tulime Tallinnast.","Raamat on laual."],correct="Lähen kooli."),
AssessmentQuestion(id="et-b1-001",skill="grammar",difficulty="B1",question="Which sentence uses a conditional?",options=["Kui oleks aega, tuleksin.","Ma tulen homme.","Ma olen kodus.","Ta loeb raamatut."],correct="Kui oleks aega, tuleksin."),
AssessmentQuestion(id="et-b1-002",skill="grammar",difficulty="B1",question="Which sentence contains a relative clause?",options=["Inimene, kes tuli, on õpetaja.","Ma tulen homme.","Ta töötab siin.","See on maja."],correct="Inimene, kes tuli, on õpetaja."),
AssessmentQuestion(id="et-b2-001",skill="grammar",difficulty="B2",question="Which sentence is passive?",options=["Maja ehitati eelmisel aastal.","Ma ehitan maja.","Ta läheb koju.","Me loeme raamatut."],correct="Maja ehitati eelmisel aastal."),
AssessmentQuestion(id="et-b2-002",skill="discourse",difficulty="B2",question="Which phrase signals a contrast?",options=["Sellest hoolimata","Esiteks","Seetõttu","Näiteks"],correct="Sellest hoolimata"),
AssessmentQuestion(id="et-c1-001",skill="academic",difficulty="C1",question="Which phrase hedges an academic claim?",options=["Võib oletada, et tulemus muutub.","See on alati nii.","Kindlasti pole muud võimalust.","See tõestab kõike."],correct="Võib oletada, et tulemus muutub."),
AssessmentQuestion(id="et-c1-002",skill="formal",difficulty="C1",question="Which is formal institutional language?",options=["Palume dokumendi esitada tähtajaks.","Tere!","Mis toimub?","Ma tahan seda."],correct="Palume dokumendi esitada tähtajaks."),
AssessmentQuestion(id="et-c2-001",skill="pragmatics",difficulty="C2",question="Which phrase softens a request?",options=["Kui võimalik, palun ...","Tee seda kohe!","Ära tee seda.","Ma tahan seda."],correct="Kui võimalik, palun ..."),
AssessmentQuestion(id="et-c2-002",skill="translation",difficulty="C2",question="What should advanced translation preserve?",options=["Meaning, register and discourse function","Only literal words","Only word order","Only punctuation"],correct="Meaning, register and discourse function")
]
