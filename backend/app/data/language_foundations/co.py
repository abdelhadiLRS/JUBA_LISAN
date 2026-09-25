"""Corsican (corsu) A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug,title,level,summary,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=summary,explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[
_g("pronouns","Prunomi persunali","A1","Introduce people and refer to participants.","Use eiu, tù, ellu/ella, noi, voi and elli/elle in simple clauses.",["Eiu sò Maria.","Ella parla corsu."]),
_g("present","Presente è cunghjucazione","A1","Describe current actions and states.","Learn common present-tense verb patterns and agreement.",["Travagliu in cità.","Noi campemu quì."]),
_g("articles","Articuli è genere","A1","Build basic noun phrases.","Use definite and indefinite articles and recognize masculine/feminine agreement.",["Una casa bianca.","U paese hè vicinu."]),
_g("word-order","Ordine di e parolle","A1","Build clear everyday sentences.","Use a neutral subject-verb-complement order while recognizing common fronting.",["Eiu abitu in Aiacciu.","Oghje andemu à scola."]),
_g("questions","Dumande","A1","Ask practical questions.","Use question words such as chì, quale, induve, quandu, cumu and perchè.",["Induve campi?","Chì faci oghje?"]),
_g("negation","Negazione","A1","Negate statements and answers.","Use micca and common negative patterns in present communication.",["Ùn capiscu micca.","Ùn travagliu oghje."]),
_g("possessives","Pussessivi","A1","Talk about family and belongings.","Use possessive forms with noun phrases and agreement.",["A mo casa hè quì.","U mo fratellu studia."]),
_g("prepositions","Prepusizioni è locu","A1","Express location and movement.","Use à, in, da, cù and related prepositional patterns in everyday contexts.",["Sò in casa.","Andemu à Bastia."]),
_g("past","Passatu","A2","Talk about completed events.","Use common past forms and time expressions for yesterday and earlier events.",["Aghju manghjatu à meziornu.","Semu andati in paese."]),
_g("future","Futuru è intenzione","A2","Talk about plans and predictions.","Use future forms and expressions of intention and scheduled events.",["Anderemu dumane.","Vogliu studià di più."]),
_g("comparatives","Cumpagrazione","A2","Compare people, places and things.","Form common comparative and superlative expressions.",["Bastia hè più grande.","Hè u più chjucu."]),
_g("imperative","Imperativu è pulitezza","A2","Give instructions and requests.","Use imperative forms and polite requests appropriate to everyday interaction.",["Aspetta un mumentu.","Per piacè, pudete aiutà mi?"]),
_g("pronoun-clitics","Prunomi cumplementi","B1","Manage object reference.","Use unstressed object pronouns with frequent verbs and avoid ambiguity.",["A vecu ogni ghjornu.","Ti chjamu sta sera."]),
_g("relative","Frasi relative","B1","Connect descriptions and clauses.","Use relative structures with qui/chi and appropriate clause order.",["A casa chì avemu vistu hè bella.","L'omu chì parla hè u mo prufessore."]),
_g("conditional","Cundiziunale","B1","Express hypotheses and polite possibilities.","Use conditional forms with si clauses and courteous requests.",["Se avessi tempu, vinerebbe.","Vuleria una infurmazione, per piacè."]),
_g("modal","Modalità","B1","Express ability, obligation and possibility.","Use pudè, duvere, vulè and related constructions to express stance.",["Puderemu principià dumane.","Devi studià."]),
_g("causal","Causa è scopu","B1","Explain reasons and purposes.","Connect clauses with perchè, dunque, per, affinchè and related expressions.",["Studiu perchè vogliu avanzà.","Vengu per amparà."]),
_g("reported","Discorsu riportatu","B2","Report statements and questions.","Use reported clauses while preserving tense, reference and register.",["Ellu hà dettu ch'ellu veneria dumane.","Ùn sò induve campa."]),
_g("passive","Passivu","B2","Describe processes and institutional actions.","Recognize passive constructions and impersonal alternatives in formal Corsican.",["A porta hè stata chjosa.","U documentu hè statu firmatu."]),
_g("aspect","Aspettu è durata","B2","Distinguish completed, ongoing and habitual events.","Combine tense, adverbs and periphrastic patterns to express event structure.",["Stava travagliendu quandu hè ghjuntu.","Avemu digià finitu."]),
_g("subordination","Suburdinazione cumplessa","B2","Build multi-clause arguments.","Combine subordinate clauses while maintaining clear reference and conjunction choice.",["Ancu s'ellu piove, continueremu à marchjà."]),
_g("concession","Cuncessione è cuntrastu","B2","Express contrast and concession.","Use ancu s'è, però, tuttavia, malgradu and related discourse patterns.",["Ancu s'è hè stancu, cuntinueghja.","Hè caru, però vale a pena."]),
_g("discourse","Cunnettori è cuesione","B2","Organize connected discourse.","Use connectors for sequence, cause, contrast, consequence and conclusion.",["Prima analizemu i dati; dopu ne discutemu."]),
_g("nominalization","Nominalizazione","C1","Use dense formal noun phrases.","Recognize nominalized actions in administrative and academic texts and unpack them when clarity requires.",["L'analisi di i risultati hà iniziatu.","A valutazione di u prughjettu hè necessaria."]),
_g("register","Registru è pulitezza","C1","Adapt language to context.","Distinguish familiar, neutral, professional and institutional formulations.",["Puderebbe precisà stu puntu?","Vi ringraziu per a vostra risposta."]),
_g("academic-hedging","Prudenza accademica","C1","Qualify claims responsibly.","Use expressions of evidence, probability and limitation instead of absolute assertions.",["I risultati parenu indicà una tendenza.","Si pò suppone chì l'effettu sia limitatu."]),
_g("argumentation","Argumentazione","C1","Structure evidence-based reasoning.","Signal claims, evidence, counterarguments and conclusions with precise connectors.",["Prima, l'evidenza sustene l'ipotesi; tuttavia, ci vole à cunsiderà un'altra interpretazione."]),
_g("institutional","Lingua amministrativa","C1","Read and write formal institutional Corsican.","Use conventional impersonal and procedural structures while keeping sentences readable.",["A dumanda deve esse mandata prima di a scadenza.","U dossier serà esaminatu da a cumissione."]),
_g("embedded-questions","Dumande incastrate","C1","Embed questions in formal discourse.","Use indirect questions after sapere, spiegà, dumandà and related verbs.",["Ùn sò micca induve si trova u documentu.","Ci hà spiegatu cumu funziona u sistema."]),
_g("information-structure","Tema è focu","C1","Manage emphasis and information flow.","Use fronting, repetition and lexical choice to distinguish topic from new information.",["Sta questione, a discuteremu dumane.","Hè precisamente stu puntu chì vulemu chiarisce."]),
_g("pragmatics","Pragmatica è significatu implicitu","C2","Interpret stance and implied meaning.","Adjust directness, mitigation and context-sensitive expressions.",["À parè meiu, ci sarebbe forse un'altra suluzione.","Capiscu u puntu, ma ùn ne sò micca cunvintu."]),
_g("rhetoric","Retorica","C2","Analyze persuasive Corsican discourse.","Study framing, parallelism, metaphor, contrast and rhetorical organization.",["Ùn si tratta micca solu di u costu, ma ancu di l'equità."]),
_g("translation","Traduzzione precisa","C2","Preserve meaning across languages.","Preserve tense, modality, register, idiom and discourse relations rather than translating mechanically.",["A traduzzione deve mantene a sfumatura di u testu originale."]),
_g("literary","Stile literariu","C2","Interpret literary and stylistic nuance.","Analyze imagery, rhythm, idiom and register shifts in Corsican prose.",["U paese dormia sottu à a luce calma di a luna."]),
_g("discourse-analysis","Analisi di u discorsu","C2","Analyze advanced cohesion and stance.","Track reference, presupposition, argument structure, evaluation and register shifts.",["U testu custruisce u cuntrastu ripetendu termini di valutazione opposti."]),
_g("lexical-precision","Precisione lessicale","C2","Choose exact vocabulary for demanding contexts.","Distinguish near-synonyms and select terms according to genre, audience and intended force.",["A scelta di u verbu cambia a forza di l'affirmazione."])
]

def _v(i,level,topic,words):
    return VocabularySet(id=i,level=level,topic=topic,unit_ref=f"co-{level.lower()}-unit-1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS=[
_v("greetings_a1","A1","Saluti è presentazione",[("salute","phrase","hello","Salute!"),("bonghjornu","phrase","good morning","Bonghjornu!"),("grazie","phrase","thank you","Grazie assai."),("à prestu","phrase","see you soon","À prestu!")]),
_v("identity_a1","A1","Identità",[("nome","noun","name","Mi chjamu Maria."),("amicu","noun","friend","Hè u mo amicu."),("studiente","noun","student","Sò studiente."),("prufessore","noun","teacher","U prufessore parla.")]),
_v("family_a1","A1","Famiglia",[("mamma","noun","mother","A mo mamma hè quì."),("babbu","noun","father","U mo babbu travaglia."),("fratellu","noun","brother","U mo fratellu studia."),("surella","noun","sister","A mo surella hè ghjovana.")]),
_v("home_a1","A1","Casa",[("casa","noun","house","A casa hè vicina."),("stanza","noun","room","A stanza hè grande."),("porta","noun","door","A porta hè aperta."),("finestra","noun","window","A finestra hè chjusa.")]),
_v("food_a1","A1","Alimentazione",[("pane","noun","bread","Vogliu pane, per piacè."),("acqua","noun","water","Bevu acqua."),("latte","noun","milk","U latte hè caldu."),("mela","noun","apple","Manghju una mela.")]),
_v("places_a1","A1","Lochi",[("scola","noun","school","A scola hè quì."),("paese","noun","village/town","U paese hè vicinu."),("cità","noun","city","A cità hè grande."),("stazione","noun","station","Induve hè a stazione?")]),
_v("daily_a2","A2","Vita cutidiana",[("svegliassi","verb","wake up","Mi svegliu à sette ore."),("travaglià","verb","work","Travagliu ogni ghjornu."),("dumane","adverb","tomorrow","Partemu dumane."),("spessu","adverb","often","Leghju spessu.")]),
_v("travel_a2","A2","Viaghju",[("bigliettu","noun","ticket","Aghju u bigliettu."),("trenu","noun","train","U trenu parte à ottu ore."),("strada","noun","road","Questa strada hè longa."),("valisgia","noun","suitcase","A valisgia hè pesante.")]),
_v("health_a2","A2","Salute",[("duttore","noun","doctor","Vò à u duttore."),("dolore","noun","pain","Aghju un dolore."),("medicina","noun","medicine","A medicina hè quì."),("appuntamentu","noun","appointment","Aghju un appuntamentu.")]),
_v("work_b1","B1","U travagliu",[("riunione","noun","meeting","A riunione principia à dece ore."),("prughjettu","noun","project","U prughjettu hè impurtante."),("scadenza","noun","deadline","A scadenza hè vennari."),("rispunsabilità","noun","responsibility","A rispunsabilità hè cumuna.")]),
_v("education_b1","B1","Educazione",[("corsu","noun","course","U corsu principia luni."),("esame","noun","exam","L'esame hè difficiule."),("ricerca","noun","research","A ricerca cuntinueghja."),("cunniscenza","noun","knowledge","A cunniscenza cresce cù a pratica.")]),
_v("society_b1","B1","Sucietà",[("cumunità","noun","community","A cumunità participa."),("serviziu","noun","service","U serviziu hè publicu."),("dirittu","noun","right/law","Ognunu hà un dirittu."),("decisione","noun","decision","A decisione hè impurtante.")]),
_v("media_b2","B2","Media è infurmazione",[("nutizia","noun","news item","A nutizia hè stata publicata."),("fonte","noun","source","A fonte deve esse verificata."),("articulu","noun","article","Aghju lettu l'articulu."),("opinione","noun","opinion","Hè una opinione persunale.")]),
_v("environment_b2","B2","Ambiente",[("ambiente","noun","environment","A prutezzione di l'ambiente hè necessaria."),("inquinamentu","noun","pollution","L'inquinamentu deve calà."),("risorsa","noun","resource","A risorsa hè limitata."),("sustenibilità","noun","sustainability","A sustenibilità hè un scopu.")]),
_v("academic_c1","C1","Lingua accademica",[("evidenza","noun","evidence","L'evidenza sustene l'ipotesi."),("risultatu","noun","result","U risultatu hè chjaru."),("ipotesi","noun","hypothesis","L'ipotesi serà verificata."),("limitazione","noun","limitation","U studiu hà parechje limitazioni.")]),
_v("institutional_c1","C1","Amministrazione",[("dumanda","noun","application/request","A dumanda hè stata ricevuta."),("cumissione","noun","commission","A cumissione esamina u dossier."),("procedura","noun","procedure","A procedura hè definita."),("dispusizione","noun","provision","A dispusizione s'applica à tutti.")]),
_v("rhetoric_c2","C2","Retorica è analisi",[("sfumatura","noun","nuance","A parolla hà una sfumatura particulare."),("cuntrastu","noun","contrast","U testu crea un cuntrastu forte."),("presuppusizione","noun","presupposition","A frase cuntene una presuppusizione."),("perspettiva","noun","perspective","U testu cambia di perspettiva.")]),
_v("idioms_c2","C2","Espressioni idiomatiche",[("avè in contu","phrase","take into account","Ci vole à avè in contu tutti i fattori."),("vale a pena","phrase","be worthwhile","Vale a pena di cuntinuà."),("à parè meiu","phrase","in my opinion","À parè meiu, hè pussibule."),("mette in risaltu","phrase","highlight","U raportu mette in risaltu stu puntu.")])
]

_TITLES={
"A1":["Saluti è presentazione","Famiglia è persone","Casa è oggetti","Vita cutidiana","Alimentazione è acquisti","Lochi è direzzioni","Aiutu è cumunicazione","Ripresa A1 è compitu cumunicativu"],
"A2":["Routine è tempu","Servizii è vita pratica","Viaghju è trasportu","Salute è benessere","Esperienze passate","Piani è paragoni","Mustrà opinioni","Ripresa A2 è compitu cumunicativu"],
"B1":["Travagliu è studii","Raccontà sperienze","Prunomi cumplementi","Sucietà è servizii","Ipotesi è cortesia","Descrizzione è relative","Cause, scopi è argumenti","Ripresa B1 è compitu cumunicativu"],
"B2":["Media è fonti","Passivu è lingua formale","Discorsu riportatu","Ambiente è sucietà","Suburdinazione cumplessa","Cuesione di u testu","Registru è cuntrastu","Ripresa B2 è compitu cumunicativu"],
"C1":["Scrittura accademica","Frasi suburdinate","Amministrazione è travagliu","Evidenza è prudenza","Custruisce un argumentu","Pragmatica è tonu","Dumande incastrate è infurmazione","Ripresa C1 è compitu cumunicativu"],
"C2":["Analisi retorica","Registru è stile","Traduzzione precisa","Stile literariu","Analisi di u discorsu","Argumentazione avanzata","Precisione lessicale","Ripresa C2 è compitu cumunicativu"]}

_G={"A1":["pronouns","present","articles","word-order","questions","negation","possessives","prepositions"],"A2":["past","future","comparatives","imperative","pronoun-clitics","modal","causal","past"],"B1":["pronoun-clitics","relative","conditional","modal","causal","past","reported","relative"],"B2":["reported","passive","aspect","subordination","concession","discourse","nominalization","register"],"C1":["academic-hedging","argumentation","institutional","embedded-questions","information-structure","register","nominalization","subordination"],"C2":["pragmatics","rhetoric","translation","literary","discourse-analysis","lexical-precision","argumentation","register"]}
_V={"A1":["greetings_a1","identity_a1","family_a1","home_a1","food_a1","places_a1","daily_a2","greetings_a1"],"A2":["daily_a2","travel_a2","health_a2","food_a1","places_a1","identity_a1","travel_a2","health_a2"],"B1":["work_b1","education_b1","society_b1","daily_a2","work_b1","education_b1","society_b1","work_b1"],"B2":["media_b2","environment_b2","society_b1","work_b1","media_b2","environment_b2","media_b2","environment_b2"],"C1":["academic_c1","institutional_c1","work_b1","society_b1","academic_c1","institutional_c1","media_b2","academic_c1"],"C2":["rhetoric_c2","idioms_c2","academic_c1","institutional_c1","rhetoric_c2","idioms_c2","media_b2","rhetoric_c2"]}

CURRICULUM={}
for level,titles in _TITLES.items():
    CURRICULUM[level]=[]
    for n,title in enumerate(titles,1):
        gs=_G[level]
        CURRICULUM[level].append(CurriculumUnit(id=f"co-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=[gs[(n-1)%len(gs)],gs[n%len(gs)]],vocabulary_set_ids=[_V[level][n-1]],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[f"Use Corsican in the context: {title.lower()}","Apply the unit grammar and vocabulary in a communicative task"],default_weeks=2))

def _p(i,level,situation,phrases):
    return PhrasebookCategory(id=i,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in phrases])

PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","A1","Saluti è presentazione",[("Bonghjornu!","greeting","neutral"),("Mi chjamu Maria.","introducing yourself","neutral"),("Felice di cunnosce vi.","meeting someone","neutral"),("Grazie assai.","thanking","neutral")]),
_p("daily_a1","A1","Vita cutidiana",[("Cumu sì?","asking how someone is","neutral"),("Stò bè, grazie.","answering","neutral"),("À dumane!","saying goodbye","neutral")]),
_p("shopping_a1","A1","Cumprà",[("Quantu costa?","asking a price","neutral"),("Vogliu questu, per piacè.","buying","polite"),("Possu pagà cù a carta?","payment","neutral")]),
_p("directions_a1","A1","Direzzioni",[("Induve hè a stazione?","asking directions","neutral"),("Induve si trova a scola?","asking location","neutral"),("Andate à diritta.","giving directions","neutral")]),
_p("help_a1","A1","Aiutu",[("Pudete aiutà mi?","asking for help","polite"),("Ùn capiscu micca.","asking for clarification","neutral"),("Pudete ripete, per piacè?","asking to repeat","polite")]),
_p("travel_a2","A2","Viaghju",[("Induve possu cumprà un bigliettu?","travel information","neutral"),("À chì ora parte u trenu?","asking departure time","neutral"),("Induve hè a fermata?","asking location","neutral")]),
_p("work_b1","B1","Travagliu",[("Pudemu fissà una riunione?","arranging a meeting","polite"),("Vi mandu u documentu oghje.","follow-up","neutral"),("Pudete precisà a scadenza?","clarifying deadline","polite")]),
_p("academic_c1","C1","Discussione accademica",[("L'evidenza pare indicà chì…","introducing evidence","formal"),("Sta interpretazione deve esse esaminata cun prudenza.","critical discussion","formal"),("Pudemu cuncludere chì…","drawing a conclusion","formal")]),
_p("formal_c1","C1","Amministrazione",[("Vi scrivu per dumandà infurmazione.","formal inquiry","formal"),("A dumanda hè stata ricevuta.","administrative update","formal"),("Vi ringraziu per a vostra risposta.","formal thanks","formal")]),
_p("discussion_c2","C2","Argumentazione avanzata",[("À parè meiu, sta distinzione hè essenziale.","stating a nuanced view","formal"),("Tuttavia, ci vole à cunsiderà un'altra ipotesi.","counterargument","formal"),("Stu puntu mette in risaltu una differenza impurtante.","emphasis","formal")])
]

ASSESSMENT_BANK=[
AssessmentQuestion(id="co-a1-001",skill="grammar",difficulty="A1",question="Which sentence is a natural Corsican self-introduction?",options=["Mi chjamu Maria.","Mi chjama Maria.","Chjamu Maria mi.","Maria chjamà."],correct="Mi chjamu Maria."),
AssessmentQuestion(id="co-a1-002",skill="grammar",difficulty="A1",question="Which phrase asks where someone lives?",options=["Induve campi?","Quantu costa?","Cumu sì?","Chì manghji?"],correct="Induve campi?"),
AssessmentQuestion(id="co-a2-001",skill="grammar",difficulty="A2",question="Which sentence refers to tomorrow?",options=["Anderemu dumane.","Andemu eri.","Andemu ieri.","Andemu mai."],correct="Anderemu dumane."),
AssessmentQuestion(id="co-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a hypothetical situation?",options=["Se avessi tempu, vinerebbe.","Sò venutu ieri.","Vengu avà.","Veneraghju dumane."],correct="Se avessi tempu, vinerebbe."),
AssessmentQuestion(id="co-b2-001",skill="grammar",difficulty="B2",question="Which sentence reports another person's statement?",options=["Ellu hà dettu ch'ellu veneria dumane.","Ellu vene dumane.","Ellu hè venutu.","Ellu vene spessu."],correct="Ellu hà dettu ch'ellu veneria dumane."),
AssessmentQuestion(id="co-c1-001",skill="communication",difficulty="C1",question="Which expression is most appropriate for cautious academic writing?",options=["I risultati parenu indicà una tendenza.","I risultati provanu tuttu.","Hè sicuramente sempre cusì.","Tuttu hè evidenti."],correct="I risultati parenu indicà una tendenza."),
AssessmentQuestion(id="co-c1-002",skill="communication",difficulty="C1",question="Which phrase is appropriate in a formal administrative exchange?",options=["Vi ringraziu per a vostra risposta.","Ehi, chì faci?","Dammi quellu.","Va bè, ciao."],correct="Vi ringraziu per a vostra risposta."),
AssessmentQuestion(id="co-c2-001",skill="communication",difficulty="C2",question="What should a high-quality Corsican translation preserve?",options=["Meaning, modality, register and discourse relations.","Only word order.","Only individual dictionary meanings.","No stylistic nuance."],correct="Meaning, modality, register and discourse relations.")
]
