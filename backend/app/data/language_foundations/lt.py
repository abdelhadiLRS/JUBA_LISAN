"""Lithuanian curriculum foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

def _g(slug, title, level, explanation, examples):
    return GrammarTopic(slug=slug, title=title, level=level, category="grammar", summary=f"Lithuanian {level} grammar for real communication.", explanation=explanation, examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS = [
    _g("pronouns", "Asmeniniai įvardžiai", "A1", "Use personal pronouns and the copula in basic introductions.", ["Aš esu studentas.", "Ji yra mano draugė."]),
    _g("present", "Esamasis laikas", "A1", "Form the present tense for routines and current actions.", ["Aš mokausi lietuvių kalbos.", "Mes gyvename Vilniuje."]),
    _g("questions", "Klausimai", "A1", "Use question words and yes/no questions in everyday exchanges.", ["Kur gyveni?", "Ar kalbi lietuviškai?"]),
    _g("cases", "Linksniai ir prielinksniai", "A2", "Use Lithuanian case endings with common prepositions and everyday meanings.", ["Gyvenu Vilniuje.", "Einu į mokyklą."]),
    _g("past", "Būtasis laikas", "A2", "Describe completed past events with appropriate person and number endings.", ["Vakar dirbau namuose.", "Ji vakar skaitė knygą."]),
    _g("future", "Būsimasis laikas", "A2", "Talk about plans, predictions and future actions.", ["Rytoj mokysiuosi.", "Mes keliausime į Kauną."]),
    _g("aspect", "Veiksmo trukmė ir rezultatas", "B1", "Distinguish ongoing, completed and iterative meanings through Lithuanian verbal forms and context.", ["Visą vakarą skaičiau.", "Perskaičiau straipsnį."]),
    _g("comparatives", "Laipsniavimas", "B1", "Compare people, objects and situations with comparative and superlative forms.", ["Šis kelias trumpesnis.", "Tai geriausias pasirinkimas."]),
    _g("conditional", "Tariamoji nuosaka", "B2", "Express conditions, wishes, advice and hypothetical outcomes.", ["Jei turėčiau laiko, keliaučiau.", "Norėčiau daugiau sužinoti."]),
    _g("relative", "Šalutiniai pažyminio sakiniai", "B2", "Connect information with relative structures and precise reference.", ["Knyga, kurią skaitau, yra įdomi.", "Žmogus, su kuriuo kalbėjau, yra mokytojas."]),
    _g("reported-speech", "Netiesioginė kalba", "C1", "Report statements while preserving tense, reference and discourse relationships.", ["Jis sakė, kad rytoj atvyks.", "Ji paaiškino, jog susitikimas atšauktas."]),
    _g("nominalization", "Nominalizacija ir formalus stilius", "C1", "Use nominal structures common in administrative, academic and professional Lithuanian.", ["Sprendimo priėmimas užtruko.", "Tyrimo rezultatų analizė tęsiama."]),
    _g("complex-syntax", "Sudėtinga sakinio struktūra", "C2", "Control coordination, subordination, information structure and nuanced connectors.", ["Nors rezultatai buvo netikėti, išvados patvirtino pradinę hipotezę."]),
    _g("register", "Registras ir pragmatika", "C2", "Choose precise forms for informal, professional, academic and diplomatic communication.", ["Norėčiau pasiteirauti dėl galimybės dalyvauti projekte.", "Būtume dėkingi, jei pateiktumėte papildomos informacijos."]),
]

def _v(id, level, topic, unit, entries):
    return VocabularySet(id=id, level=level, topic=topic, unit_ref=unit, words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w,p,d,e in entries])

VOCABULARY_SETS = [
    _v("lt_a1_greetings", "A1", "greetings", "lt-a1-unit-1", [("labas","expression","hello","Labas! Kaip sekasi?"),("laba diena","expression","good afternoon/hello","Laba diena, ponia."),("ačiū","word","thank you","Ačiū už pagalbą."),("prašau","word","please/you are welcome","Prašau, atsisėskite."),("viso gero","expression","goodbye","Viso gero, iki rytojaus.")]),
    _v("lt_a1_identity", "A1", "identity", "lt-a1-unit-2", [("vardas","noun","name","Koks tavo vardas?"),("pavardė","noun","surname","Mano pavardė yra Petrauskas."),("studentas","noun","student","Esu universiteto studentas."),("draugas","noun","friend","Tai mano draugas."),("gyventi","verb","to live","Gyvenu Lietuvoje.")]),
    _v("lt_a1_family", "A1", "family", "lt-a1-unit-3", [("mama","noun","mother","Mano mama dirba mokykloje."),("tėtis","noun","father","Mano tėtis yra namuose."),("brolis","noun","brother","Turiu vieną brolį."),("sesuo","noun","sister","Mano sesuo studijuoja."),("šeima","noun","family","Mano šeima gyvena mieste.")]),
    _v("lt_a1_home", "A1", "home", "lt-a1-unit-4", [("namas","noun","house","Mūsų namas yra didelis."),("butas","noun","apartment","Gyvenu mažame bute."),("kambarys","noun","room","Mano kambarys šviesus."),("virtuvė","noun","kitchen","Virtuvė yra šalia svetainės."),("stalas","noun","table","Knyga yra ant stalo.")]),
    _v("lt_a1_daily", "A1", "daily life", "lt-a1-unit-5", [("rytas","noun","morning","Ryte geriu kavą."),("darbas","noun","work","Einu į darbą aštuntą valandą."),("mokytis","verb","to study","Kasdien mokausi lietuvių kalbos."),("šiandien","adverb","today","Šiandien esu namuose."),("rytoj","adverb","tomorrow","Rytoj dirbsiu.")]),
    _v("lt_a1_food", "A1", "food", "lt-a1-unit-6", [("duona","noun","bread","Perku šviežią duoną."),("vanduo","noun","water","Gerkite daugiau vandens."),("obuolys","noun","apple","Valgau obuolį."),("arbata","noun","tea","Norėčiau arbatos."),("skanus","adjective","tasty","Maistas labai skanus.")]),
    _v("lt_a1_places", "A1", "places", "lt-a1-unit-7", [("mokykla","noun","school","Mokykla yra netoli."),("ligoninė","noun","hospital","Kur yra ligoninė?"),("parduotuvė","noun","shop","Parduotuvė uždaryta."),("gatvė","noun","street","Gyvenu šioje gatvėje."),("stotis","noun","station","Stotis yra miesto centre.")]),
    _v("lt_a1_communication", "A1", "communication", "lt-a1-unit-8", [("suprasti","verb","to understand","Aš suprantu klausimą."),("pakartoti","verb","to repeat","Prašau pakartoti."),("pagalba","noun","help","Man reikia pagalbos."),("klausimas","noun","question","Turiu klausimą."),("kalbėti","verb","to speak","Ar kalbate angliškai?")]),
    _v("lt_a2_time", "A2", "time and plans", "lt-a2-unit-1", [("praeitą savaitę","expression","last week","Praeitą savaitę buvau Kaune."),("kitą mėnesį","expression","next month","Kitą mėnesį keliausime."),("dažnai","adverb","often","Dažnai važiuoju autobusu."),("kartais","adverb","sometimes","Kartais dirbu iš namų."),("vėliau","adverb","later","Susitiksime vėliau.")]),
    _v("lt_a2_services", "A2", "services", "lt-a2-unit-2", [("sąskaita","noun","bill/account","Prašau sąskaitos."),("užsakymas","noun","order","Mano užsakymas paruoštas."),("bilietas","noun","ticket","Nusipirkau bilietą."),("registracija","noun","registration","Registracija prasideda ryte."),("kaina","noun","price","Kokia šios prekės kaina?")]),
    _v("lt_a2_travel", "A2", "travel", "lt-a2-unit-3", [("kelionė","noun","trip","Kelionė buvo ilga."),("oro uostas","noun","airport","Oro uostas yra už miesto."),("traukinys","noun","train","Traukinys išvyksta devintą."),("viešbutis","noun","hotel","Viešbutis yra centre."),("žemėlapis","noun","map","Kur galiu gauti žemėlapį?")]),
    _v("lt_b1_work", "B1", "work", "lt-b1-unit-1", [("susitikimas","noun","meeting","Rytoj turime svarbų susitikimą."),("terminas","noun","deadline","Projekto terminas artėja."),("užduotis","noun","task","Šią užduotį atliksiu šiandien."),("patirtis","noun","experience","Turiu penkerių metų patirtį."),("atsakomybė","noun","responsibility","Tai didelė atsakomybė.")]),
    _v("lt_b1_society", "B1", "society", "lt-b1-unit-2", [("bendruomenė","noun","community","Bendruomenė organizuoja renginį."),("aplinka","noun","environment","Turime saugoti aplinką."),("sprendimas","noun","decision/solution","Reikia rasti sprendimą."),("nuomonė","noun","opinion","Kokia jūsų nuomonė?"),("įstatymas","noun","law","Naujasis įstatymas įsigaliojo.")]),
    _v("lt_b2_argumentation", "B2", "argumentation", "lt-b2-unit-1", [("įrodymas","noun","evidence","Reikia pateikti įrodymų."),("prielaida","noun","assumption","Ši prielaida nėra pakankamai pagrįsta."),("išvada","noun","conclusion","Tyrimo išvada aiški."),("priežastis","noun","reason/cause","Svarbu nustatyti priežastį."),("pasekmė","noun","consequence","Sprendimas turės ilgalaikių pasekmių.")]),
    _v("lt_b2_media", "B2", "media", "lt-b2-unit-2", [("šaltinis","noun","source","Patikrinkite informacijos šaltinį."),("pranešimas","noun","report/announcement","Perskaičiau oficialų pranešimą."),("viešoji nuomonė","noun phrase","public opinion","Viešoji nuomonė pasikeitė."),("šališkumas","noun","bias","Straipsnyje pastebimas šališkumas."),("patikimas","adjective","reliable","Tai patikimas šaltinis.")]),
    _v("lt_c1_academic", "C1", "academic language", "lt-c1-unit-1", [("tyrimas","noun","research/study","Tyrimas atskleidė naujus rezultatus."),("metodologija","noun","methodology","Metodologija aprašyta ataskaitoje."),("hipotezė","noun","hypothesis","Hipotezė buvo patikrinta."),("duomenys","noun","data","Duomenys buvo analizuojami kelis mėnesius."),("iš esmės","expression","essentially","Iš esmės šie rezultatai sutampa.")]),
    _v("lt_c1_professional", "C1", "professional", "lt-c1-unit-2", [("įgyvendinti","verb","to implement","Planą reikia įgyvendinti etapais."),("bendradarbiauti","verb","to cooperate","Įmonės pradėjo bendradarbiauti."),("prioritetas","noun","priority","Saugumas yra pagrindinis prioritetas."),("veiksmingumas","noun","effectiveness","Vertinome priemonės veiksmingumą."),("atsižvelgti","verb","to take into account","Būtina atsižvelgti į aplinkybes.")]),
    _v("lt_c2_nuance", "C2", "nuance", "lt-c2-unit-1", [("niuansas","noun","nuance","Šis niuansas keičia sakinio prasmę."),("dviprasmiškas","adjective","ambiguous","Formuluotė gali būti dviprasmiška."),("konotacija","noun","connotation","Žodis turi neigiamą konotaciją."),("sąlygiškai","adverb","conditionally/relatively","Šį teiginį galima priimti tik sąlygiškai."),("subtilus","adjective","subtle","Tai subtilus stilistinis skirtumas.")]),
    _v("lt_c2_formal", "C2", "formal style", "lt-c2-unit-2", [("atsižvelgiant į","expression","in view of","Atsižvelgiant į aplinkybes, sprendimas atidedamas."),("pabrėžtina","expression","it should be emphasized","Pabrėžtina, kad duomenys nėra galutiniai."),("manytina","expression","it may be considered","Manytina, kad priemonė bus veiksminga."),("nepaisant","preposition","despite","Nepaisant sunkumų, projektas tęsiamas."),("atitinkamai","adverb","accordingly","Rezultatai atitinkamai buvo pakoreguoti.")]),
]

PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="lt_a1_greetings", level="A1", situation="greetings", icon="👋", phrases=[PhrasebookEntry(text="Laba diena!", context="polite greeting", register="formal"), PhrasebookEntry(text="Kaip sekasi?", context="asking how someone is", register="neutral"), PhrasebookEntry(text="Malonu susipažinti.", context="first meeting", register="neutral")]),
    PhrasebookCategory(id="lt_a1_daily", level="A1", situation="daily", icon="☀️", phrases=[PhrasebookEntry(text="Aš nesuprantu.", context="asking for clarification", register="neutral"), PhrasebookEntry(text="Prašau pakartoti.", context="asking someone to repeat", register="polite"), PhrasebookEntry(text="Kur yra tualetas?", context="finding a facility", register="neutral")]),
    PhrasebookCategory(id="lt_a2_shopping", level="A2", situation="shopping", icon="🛒", phrases=[PhrasebookEntry(text="Kiek tai kainuoja?", context="asking price", register="neutral"), PhrasebookEntry(text="Ar galima atsiskaityti kortele?", context="payment", register="polite"), PhrasebookEntry(text="Norėčiau tai grąžinti.", context="returning an item", register="polite")]),
    PhrasebookCategory(id="lt_a2_travel", level="A2", situation="travel", icon="🧭", phrases=[PhrasebookEntry(text="Kur yra geležinkelio stotis?", context="asking directions", register="neutral"), PhrasebookEntry(text="Kada išvyksta autobusas?", context="transport schedule", register="neutral"), PhrasebookEntry(text="Man reikia bilieto į Kauną.", context="buying a ticket", register="neutral")]),
    PhrasebookCategory(id="lt_b1_work", level="B1", situation="work", icon="💼", phrases=[PhrasebookEntry(text="Ar galime aptarti šį klausimą?", context="work discussion", register="professional"), PhrasebookEntry(text="Siūlau susitikti kitą savaitę.", context="making a proposal", register="professional"), PhrasebookEntry(text="Pateiksiu atsakymą iki penktadienio.", context="setting a deadline", register="professional")]),
    PhrasebookCategory(id="lt_b2_discussion", level="B2", situation="discussion", icon="💬", phrases=[PhrasebookEntry(text="Mano nuomone, svarbu atsižvelgti į kontekstą.", context="argumentation", register="formal"), PhrasebookEntry(text="Šį teiginį reikėtų pagrįsti duomenimis.", context="critical discussion", register="formal"), PhrasebookEntry(text="Vis dėlto yra ir kita perspektyva.", context="introducing contrast", register="neutral")]),
    PhrasebookCategory(id="lt_c1_academic", level="C1", situation="academic", icon="🎓", phrases=[PhrasebookEntry(text="Tyrimo rezultatai rodo, kad...", context="presenting findings", register="academic"), PhrasebookEntry(text="Ši prielaida reikalauja papildomo pagrindimo.", context="academic critique", register="academic"), PhrasebookEntry(text="Apibendrinant galima teigti, kad...", context="conclusion", register="academic")]),
    PhrasebookCategory(id="lt_c2_formal", level="C2", situation="formal", icon="🏛️", phrases=[PhrasebookEntry(text="Atsižvelgiant į pirmiau išdėstytas aplinkybes...", context="formal writing", register="formal"), PhrasebookEntry(text="Pabrėžtina, kad šis vertinimas nėra galutinis.", context="qualified statement", register="formal"), PhrasebookEntry(text="Būtume dėkingi, jei pateiktumėte papildomos informacijos.", context="formal request", register="formal")]),
]

UNIT_TITLES = {
    "A1": ["Pasisveikinimas ir pažintis","Šeima ir žmonės","Namai ir daiktai","Kasdienė rutina","Maistas ir apsipirkimas","Miestas ir kryptys","Bendravimas ir pagalba","A1 kartojimas"],
    "A2": ["Laikas ir planai","Paslaugos ir pinigai","Kelionės","Sveikata ir savijauta","Mokslas ir darbas","Laisvalaikis","Patirtys ir nuomonės","A2 kartojimas"],
    "B1": ["Darbas ir atsakomybė","Bendruomenė ir visuomenė","Naujienos ir informacija","Santykiai ir problemų sprendimas","Kultūra ir tapatybė","Aplinka ir gyvenimo būdas","Argumentavimas","B1 kartojimas"],
    "B2": ["Argumentai ir įrodymai","Žiniasklaida ir kritinis mąstymas","Profesinis bendravimas","Politikos ir visuomenės temos","Mokslas ir technologijos","Debatai ir perspektyvos","Stilius ir tikslumas","B2 kartojimas"],
    "C1": ["Akademinis diskursas","Profesinė komunikacija","Tyrimai ir metodologija","Sudėtingi tekstai","Viešasis kalbėjimas","Analizė ir sintezė","Registras ir stilius","C1 kartojimas"],
    "C2": ["Stilistinė kontrolė","Subtili reikšmė","Akademinė argumentacija","Profesinis ir administracinis stilius","Retorika ir diskursas","Vertinimas ir kritika","Idiomatika ir pragmatika","C2 integracija"],
}
GRAMMAR_BY_LEVEL = {
    "A1": ["pronouns","present","questions"], "A2": ["cases","past","future"],
    "B1": ["aspect","comparatives"], "B2": ["conditional","relative"],
    "C1": ["reported-speech","nominalization"], "C2": ["complex-syntax","register"],
}
VOCAB_BY_LEVEL = {
    "A1": ["lt_a1_greetings","lt_a1_identity","lt_a1_family","lt_a1_home","lt_a1_daily","lt_a1_food","lt_a1_places","lt_a1_communication"],
    "A2": ["lt_a2_time","lt_a2_services","lt_a2_travel"], "B1": ["lt_b1_work","lt_b1_society"],
    "B2": ["lt_b2_argumentation","lt_b2_media"], "C1": ["lt_c1_academic","lt_c1_professional"], "C2": ["lt_c2_nuance","lt_c2_formal"],
}

CURRICULUM = {}
for level in LEVELS:
    units = []
    for i, title in enumerate(UNIT_TITLES[level], 1):
        units.append(CurriculumUnit(
            id=f"lt-{level.lower()}-unit-{i}", level=level, unit_number=i, title=title,
            grammar_points=GRAMMAR_BY_LEVEL[level] if i == 1 else [GRAMMAR_BY_LEVEL[level][(i-1) % len(GRAMMAR_BY_LEVEL[level])]],
            vocabulary_set_ids=VOCAB_BY_LEVEL[level] if i == 1 else [VOCAB_BY_LEVEL[level][(i-1) % len(VOCAB_BY_LEVEL[level])]],
            lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
            competency_checklist=["Understand and produce Lithuanian appropriate to the level.", "Use target vocabulary in a realistic communicative task.", "Demonstrate control of the unit grammar."],
            default_weeks=2 if level in {"A1","A2"} else 3,
        ))
    CURRICULUM[level] = units

ASSESSMENT_BANK = [
    AssessmentQuestion(id="lt-a1-001", skill="communication", difficulty="A1", question="How do you greet someone politely during the day?", options=["Laba diena!","Viso gero!","Ačiū.","Labas rytas."], correct="Laba diena!"),
    AssessmentQuestion(id="lt-a1-002", skill="identity", difficulty="A1", question="Which sentence means 'I am a student'?", options=["Aš esu studentas.","Aš gyvenu Vilniuje.","Aš turiu brolį.","Aš dirbu namuose."], correct="Aš esu studentas."),
    AssessmentQuestion(id="lt-a2-001", skill="grammar", difficulty="A2", question="Which sentence correctly describes yesterday?", options=["Vakar dirbau namuose.","Rytoj dirbsiu namuose.","Dabar dirbu namuose.","Dažnai dirbsiu namuose."], correct="Vakar dirbau namuose."),
    AssessmentQuestion(id="lt-a2-002", skill="travel", difficulty="A2", question="How do you ask when the bus leaves?", options=["Kada išvyksta autobusas?","Kur gyveni?","Kiek tai kainuoja?","Kaip sekasi?"], correct="Kada išvyksta autobusas?"),
    AssessmentQuestion(id="lt-b1-001", skill="grammar", difficulty="B1", question="Which sentence expresses a completed reading action?", options=["Perskaičiau straipsnį.","Skaičiau visą vakarą.","Skaitysiu rytoj.","Skaitau dabar."], correct="Perskaičiau straipsnį."),
    AssessmentQuestion(id="lt-b1-002", skill="argumentation", difficulty="B1", question="Which word means 'conclusion'?", options=["išvada","prielaida","pasekmė","atsakomybė"], correct="išvada"),
    AssessmentQuestion(id="lt-b2-001", skill="grammar", difficulty="B2", question="Which sentence expresses a hypothetical condition?", options=["Jei turėčiau laiko, keliaučiau.","Vakar keliavau.","Rytoj keliausiu.","Dabar keliauju."], correct="Jei turėčiau laiko, keliaučiau."),
    AssessmentQuestion(id="lt-b2-002", skill="reading", difficulty="B2", question="Which term refers to evidence supporting an argument?", options=["įrodymas","niuansas","pavardė","kelionė"], correct="įrodymas"),
    AssessmentQuestion(id="lt-c1-001", skill="academic", difficulty="C1", question="Which phrase appropriately introduces research findings?", options=["Tyrimo rezultatai rodo, kad...","Labas!","Kiek tai kainuoja?","Kur yra stotis?"], correct="Tyrimo rezultatai rodo, kad..."),
    AssessmentQuestion(id="lt-c1-002", skill="formal", difficulty="C1", question="Which expression is appropriate for a formal qualified statement?", options=["Manytina, kad priemonė bus veiksminga.","Labas, kas naujo?","Noriu šito.","Kur yra turgus?"], correct="Manytina, kad priemonė bus veiksminga."),
    AssessmentQuestion(id="lt-c2-001", skill="pragmatics", difficulty="C2", question="Which expression signals a formal consideration of preceding circumstances?", options=["Atsižvelgiant į pirmiau išdėstytas aplinkybes...","Labas rytas!","Kiek tai kainuoja?","Noriu vandens."], correct="Atsižvelgiant į pirmiau išdėstytas aplinkybes..."),
    AssessmentQuestion(id="lt-c2-002", skill="style", difficulty="C2", question="Which word describes a subtle stylistic difference?", options=["subtilus","garsus","kasdienis","greitas"], correct="subtilus"),
]
