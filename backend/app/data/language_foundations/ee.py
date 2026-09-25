"""Ewe A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

def _g(slug,title,level,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=f"Ewe {level} grammar.",explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[
_g("pronouns","Personal pronouns","A1","Use subject pronouns in simple clauses.",["nye Eʋeʋegbe meƒe ŋkɔ.","wò nye xɔlɔ̃."]),
_g("copula","Nominal predicates","A1","Identify people and things with simple nominal predicates.",["nye amedzro.","eɖevi la nye ŋutsu."]),
_g("greetings","Greetings and introductions","A1","Open conversations and introduce yourself.",["Woezɔ!","nye ŋkɔe Kofi."]),
_g("negation","Basic negation","A1","Negate simple statements with common Ewe negative patterns.",["nye menye dɔwɔla o.","meɖu nu o."]),
_g("questions","Question words","A1","Ask who, what, where and how questions.",["nukae nye esia?","afi kae nèyi?"]),
_g("possessives","Possession and noun phrases","A1","Express possession and identify familiar objects.",["nye agbalẽ.","xɔ̃a ƒe afɔ."]),
_g("location","Location and existential clauses","A1","Say where people and things are.",["ame la le afima.","agbalẽ la le xɔ me."]),
_g("time","Time and routine","A1","Talk about days, time and everyday routines.",["egbe nye ŋkeke nyui.","meɖu nu ŋdi."]),
_g("plural","Plural and noun reference","A2","Use plural reference and agreement in common noun phrases.",["ameawo va.","ɖeviwo le afima."]),
_g("aspect","Progressive and habitual aspect","A2","Distinguish ongoing and habitual actions.",["mele nu ŋlɔm.","meɖu nu ɣesiaɣi."]),
_g("past","Past events","A2","Describe completed and earlier events.",["meɖu nu etsɔ.","eɖo ŋkɔe."]),
_g("future","Future and intention","A2","Express plans and future events.",["maɖu nu.","meyi afi ma gbɔ."]),
_g("imperative","Commands and polite requests","A2","Give instructions and make everyday requests.",["va afima.","meɖe kuku, tsɔe na ŋunye."]),
_g("comparatives","Comparison","A2","Compare people, objects and qualities.",["ehe wu esia.","Kofi nye ŋutsu gã wu."]),
_g("prepositions","Prepositions and relations","A2","Express direction, source and spatial relations.",["le xɔ me.","yi agbeƒe."]),
_g("modality","Ability, obligation and desire","B1","Express possibility, ability, need and intention.",["mate ŋu awɔe.","ele be mayi."]),
_g("conditional","Conditional clauses","B1","Form real and hypothetical conditions.",["ne èva la, míayi.","ne mekpɔ ga la, maɖu nu."]),
_g("relative","Relative clauses","B1","Modify nouns with relative clauses.",["ame si va la nye xɔlɔ̃nye.","nu si mekpɔ la nyo."]),
_g("serial_verbs","Serial verb constructions","B1","Chain related actions in natural Ewe verbal constructions.",["yi ɖaɖa va.","tsɔe va na me."]),
_g("cause_purpose","Cause, reason and purpose","B1","Connect events by cause and purpose.",["eƒe ta la, meyi o.","meva be makpɔ wò."]),
_g("reported","Reported speech","B1","Report statements and questions.",["egblɔ be yeyi.","ebia be nukae nye esia."]),
_g("aspectual_nuance","Aspectual and temporal nuance","B2","Control event boundaries and temporal interpretation.",["etsɔ wɔe vɔ.","ele nu wɔm fifia."]),
_g("passive","Passive and affected constructions","B2","Interpret and use passive-like affected event descriptions.",["agbalẽ la woŋlɔe.","nu la wɔe ɖe asi."]),
_g("causative","Causative constructions","B2","Express causing or arranging an action.",["eɖevi la na wɔ dɔa.","eɖo ameawo be woava."]),
_g("concession","Concession and contrast","B2","Express although, however and contrastive relations.",["evɔ̃ ŋutɔ, eya ta meyi o.","ke boŋ, míagblɔe."]),
_g("discourse","Discourse connectors","B2","Organize longer explanations and narratives.",["gbã la, míayi; emegbe la, míava.","eya ta la, wòkpɔ nu."]),
_g("nominalization","Nominalization","C1","Use nominalized processes in formal and academic discourse.",["nuŋlɔla ƒe dɔwɔwɔ le eteƒe.","nunya ƒe dzidzedze hia ɖoɖo."]),
_g("evidentiality","Evidence and stance","C1","Distinguish observation, inference and reported information.",["mekpɔe ŋutɔ.","ame aɖe gblɔ nam be..."]),
_g("hedging","Academic hedging","C1","Qualify claims and express degrees of certainty.",["ate ŋu anye nenema.","wòɖe edzi abe ene."]),
_g("embedded_questions","Embedded questions","C1","Embed questions in formal statements.",["menya afi si wòyi o.","mebia nuka ta wòva."]),
_g("information_structure","Topic and focus","C1","Manage topic, focus and contrastive information.",["nyee wɔe.","Kofi hãe va."]),
_g("formal_register","Formal and institutional register","C1","Adjust language for administration and professional settings.",["míele be míawɔ ɖoɖo le nu sia ŋu.","míaƒe agbalẽ le asi."]),
_g("argumentation","Argumentation and counterargument","C1","Present claims, reasons, evidence and counterarguments.",["nusi meɖo ɖe ŋu nye...","ke hã, ate ŋu anye..."]),
_g("pragmatics","Politeness and pragmatic nuance","C2","Interpret indirectness, politeness and contextual meaning.",["meɖe kuku, woawɔe na mí.","ne ète ŋu la, tsɔe va."]),
_g("rhetoric","Rhetorical and literary style","C2","Use rhetorical framing and literary nuance.",["menye nu sia ko o; eƒe nya gã le eme.","nunya la ƒe ŋutinya nye..."]),
_g("translation","Translation and paraphrase","C2","Preserve meaning, register and discourse function across reformulation.",["gɔmeɖeɖe la ele be wòakpɔ nya ƒe nɔnɔme.","tsɔ nya bubuwo gblɔ nu sia ŋutɔ."]),
_g("discourse_analysis","Discourse analysis and register shifting","C2","Analyze genre, cohesion, stance and audience.",["nya siwo nɔa ƒuƒoƒo la doa asi ɖe teƒe.","register la trɔna ɖe ame siwo le eƒe ŋgɔ."]),
]

def _v(id_,level,topic,ref,items):
    return VocabularySet(id=id_,level=level,topic=topic,unit_ref=ref,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS=[
_v("greetings_a1","A1","greetings","ee-a1-unit-1",[("Woezɔ","phrase","hello/welcome","Woezɔ!"),("akpe","phrase","thank you","Akpe!"),("ŋkɔ","noun","name","nye ŋkɔe Kofi."),("xɔlɔ̃","noun","friend","eɖe xɔlɔ̃nye.")]),
_v("identity_a1","A1","identity","ee-a1-unit-2",[("nye","pronoun","I/me","nyee."),("wò","pronoun","you","wò nye xɔlɔ̃."),("ŋutsu","noun","man","ŋutsu la va."),("nyɔnu","noun","woman","nyɔnu la le afima.")]),
_v("family_a1","A1","family","ee-a1-unit-3",[("aƒe","noun","home/house","aƒe la gã."),("tɔ","noun","father","tɔnye le afima."),("dada","noun","mother","dada la va."),("vi","noun","child","vi la le xɔ me.")]),
_v("routine_a1","A1","daily routine","ee-a1-unit-4",[("ŋdi","noun","morning","ŋdi me meɖu nu."),("ɣe","noun","day/time","ɣe sia ɣe."),("ɖu","verb","eat","meɖu nu."),("yi","verb","go","meyi.")]),
_v("time_a1","A1","time","ee-a1-unit-5",[("egbe","adverb","today","egbe meva."),("etsɔ","adverb","yesterday/tomorrow by context","etsɔ meva."),("fifia","adverb","now","fifia mele afima."),("ŋkeke","noun","day","ŋkeke nyui.")]),
_v("food_a1","A1","food and drink","ee-a1-unit-6",[("tsi","noun","water","tsi hã meɖu."),("nuɖuɖu","noun","food","nuɖuɖu le afima."),("ŋkɔ","noun","name/term","ŋkɔ la nyo."),("ɖu","verb","eat","meɖu nu.")]),
_v("places_a1","A1","places","ee-a1-unit-7",[("afi","noun","place","afi kae nèyi?"),("xɔ","noun","room/house","xɔ la le afima."),("sukuu","noun","school","sukuu la gã."),("agbeƒe","noun","market/place of trade","meyi agbeƒe.")]),
_v("review_a1","A1","review","ee-a1-unit-8",[("akpe","phrase","thanks","akpe na wò."),("Woezɔ","phrase","hello","Woezɔ!"),("afima","adverb","there","le afima."),("ɖo","verb","put/place","ɖo agbalẽa ɖe te.")]),
_v("travel_a2","A2","travel","ee-a2-unit-1",[("afɔku","noun","journey","afɔku la yɔ."),("tsitre","verb","depart","míatsitre ŋdi."),("mɔ","noun","road","mɔ la nyo."),("xɔme","noun","inside","le xɔme.")]),
_v("health_a2","A2","health","ee-a2-unit-2",[("dɔléle","noun","illness","dɔléle le eŋu."),("atike","noun","medicine","atike la wɔ dɔ."),("dɔkita","noun","doctor","dɔkita la va."),("ŋutilã","noun","body","ŋutilãa le ŋusẽ.")]),
_v("study_b1","B1","study","ee-b1-unit-1",[("nunya","noun","knowledge","nunya nyo."),("srɔ̃","verb","learn","mesrɔ̃ Eʋegbe."),("agbalẽ","noun","book","agbalẽ la le asi."),("nunyaƒe","noun","academic/knowledge domain","nunyaƒe la gã.")]),
_v("work_b1","B1","work","ee-b1-unit-2",[("dɔwɔwɔ","noun","work/activity","dɔwɔwɔ la sesẽ."),("dɔwɔla","noun","worker","dɔwɔla la va."),("ƒomeɖoɖo","noun","organization","ƒomeɖoɖo la wɔ dɔ."),("ɖoɖo","noun","plan/arrangement","míawɔ ɖoɖo.")]),
_v("society_b2","B2","society","ee-b2-unit-1",[("ameɖekuku","noun","individual/person","ameɖekuku ɖe sia ɖe."),("dukɔ","noun","country/nation","dukɔ la le afima."),("ƒome","noun","community","ƒome la ƒo ƒu."),("nudzraɖo","noun","development","nudzraɖo le edzi.")]),
_v("environment_b2","B2","environment","ee-b2-unit-2",[("yama","noun","forest","yama la lolo."),("atsi","noun","water/sea","atsi la nyo."),("agbale","noun","land","agbale la ƒe nɔnɔme."),("xɔxɔ","noun","pollution/dirty state","xɔxɔ la gblẽ yama.")]),
_v("media_c1","C1","media","ee-c1-unit-1",[("nyagblɔɖi","noun","news report","nyagblɔɖi la va."),("ɖoɖo","noun","arrangement/policy","ɖoɖo la nye..."),("gɔmeɖeɖe","noun","interpretation","gɔmeɖeɖe la kɔ.") ,("ŋutinya","noun","story/history","ŋutinya la le agbalẽ me.")]),
_v("academic_c1","C1","academic discourse","ee-c1-unit-2",[("dɔmenyo","noun","benefit/value","dɔmenyo le eme."),("dzedze","noun","growth","dzedze le edzi."),("kpɔɖeŋu","noun","evidence/example","kpɔɖeŋu aɖe va."),("nuwɔna","noun","process/action","nuwɔna la hia ɖoɖo.")]),
_v("institutional_c1","C1","institutional","ee-c1-unit-3",[("amedzroƒe","noun","institution","amedzroƒe la wɔ dɔ."),("agbalẽ","noun","document/book","agbalẽ la le asi."),("ɖoɖo","noun","policy/plan","ɖoɖo la kɔ."),("kpekpeɖeŋu","noun","support","kpekpeɖeŋu hia.")]),
_v("culture_c2","C2","culture","ee-c2-unit-1",[("amɛgbɔgbɔ","noun","culture","amɛgbɔgbɔ ƒe ŋutinya."),("dzidzɔ","noun","custom/joy","dzidzɔ le ƒome me."),("ŋutinya","noun","history/story","ŋutinya la sesẽ."),("nɔnɔme","noun","condition/state","nɔnɔme la trɔ.")]),
_v("discourse_c2","C2","discourse","ee-c2-unit-2",[("nya","noun","word/language","nya la kɔ."),("gɔme","noun","meaning","gɔme la gã."),("tata","noun","argument/position","tata la le eme."),("ŋugbedodo","noun","rhetorical expression","ŋugbedodo la zɔ.")]),
]

def _p(id_,level,situation,items,register="neutral"):
    return PhrasebookCategory(id=id_,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=register) for t,c in items])

PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","A1","greetings",[("Woezɔ!","hello"),("Ŋkɔ kae wò?","asking a name"),("nye ŋkɔe...","introducing yourself")]),
_p("thanks_a1","A1","thanks",[("Akpe!","thank you"),("Akpe ŋutɔ","many thanks"),("Míawɔ dɔ kple wò","appreciation")]),
_p("help_a1","A1","help",[("Meɖe kuku, kpe ɖe ŋunye","asking for help"),("Mese egɔme o","saying you do not understand"),("Gblɔe ake","asking to repeat")]),
_p("shopping_a1","A1","shopping",[("Ga home nye?","asking the price"),("Medi nu sia","asking for an item"),("Tsɔe na ŋunye","requesting an item")]),
_p("directions_a1","A1","directions",[("Afi kae?","asking where"),("Yi afima","giving a direction"),("Le afima","saying it is there")]),
_p("travel_a2","A2","travel",[("Míayi afima","talking about travel"),("Mele mɔ dzi","saying you are on the road"),("Medi xɔ aɖe","asking for accommodation")]),
_p("health_a2","A2","health",[("Dɔ le ŋunye","describing illness"),("Medi dɔkita","asking for a doctor"),("Atike hia","saying medicine is needed")]),
_p("study_b1","B1","study",[("Mele Eʋegbe srɔ̃m","talking about learning Ewe"),("Medi agbalẽ sia","asking for a book"),("Nunya sia kɔ","commenting on a topic")]),
_p("work_b1","B1","work",[("Míawɔ ɖoɖo","making a plan"),("Medi be míakpe","proposing a meeting"),("Nye susu nye...","stating an idea")]),
_p("discussion_b2","B2","discussion",[("Nusi meɖo ɖe ŋu nye...","giving a reason"),("Ke boŋ...","introducing contrast"),("Eya ta...","drawing a conclusion")],"formal"),
_p("academic_c1","C1","academic discussion",[("Kpɔɖeŋu la fia be...","introducing evidence"),("Ate ŋu anye be...","hedging a claim"),("Le bubuɖoɖo nu...","organizing an argument")],"academic"),
_p("institutional_c1","C1","institutional communication",[("Míele be míawɔ ɖoɖo...","formal proposal"),("Agbalẽa le asi","document status"),("Meɖe kuku, kɔe ɖe eme","formal clarification")],"formal"),
_p("pragmatics_c2","C2","pragmatic nuance",[("Meɖe kuku, ate ŋu a...","softening a request"),("Ne ète ŋu la...","tentative suggestion"),("Mese wò gome, ke...","polite disagreement")],"polite"),
]

def _u(level,n,title,grammar,vocab):
    return CurriculumUnit(id=f"ee-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=vocab,lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Communicate effectively at {level}",f"Understand level-appropriate Ewe"],default_weeks=2)

CURRICULUM={
"A1":[_u("A1",1,"Greetings and identity",["greetings","pronouns","copula"],["greetings_a1","identity_a1"]),_u("A1",2,"Family and home",["possessives","location"],["family_a1"]),_u("A1",3,"Daily routine",["questions","negation"],["routine_a1"]),_u("A1",4,"Time and food",["time","pronouns"],["time_a1","food_a1"]),_u("A1",5,"Places and directions",["location","questions"],["places_a1"]),_u("A1",6,"Basic interaction",["negation","possessives"],["review_a1"]),_u("A1",7,"Everyday exchange",["pronouns","time"],["greetings_a1","routine_a1"]),_u("A1",8,"A1 review",["greetings","questions","negation"],["review_a1","identity_a1"])],
"A2":[_u("A2",1,"Plural people and things",["plural","possessives"],["family_a1"]),_u("A2",2,"Ongoing actions",["aspect","present_habitual"],["routine_a1"]),_u("A2",3,"Past events",["past","aspect"],["travel_a2"]),_u("A2",4,"Future plans",["future","modality"],["travel_a2"]),_u("A2",5,"Requests and instructions",["imperative","negation"],["health_a2"]),_u("A2",6,"Comparing things",["comparatives","prepositions"],["places_a1","food_a1"]),_u("A2",7,"Movement and location",["prepositions","future"],["travel_a2"]),_u("A2",8,"A2 review",["past","future","comparatives"],["travel_a2","health_a2"])],
"B1":[_u("B1",1,"Ability and obligation",["modality","conditional"],["study_b1"]),_u("B1",2,"Relative descriptions",["relative","serial_verbs"],["study_b1"]),_u("B1",3,"Cause and purpose",["cause_purpose","conditional"],["work_b1"]),_u("B1",4,"Reported information",["reported","relative"],["media_c1"]),_u("B1",5,"Linked actions",["serial_verbs","aspectual_nuance"],["work_b1"]),_u("B1",6,"Society and work",["cause_purpose","discourse"],["society_b2","work_b1"]),_u("B1",7,"Extended descriptions",["relative","reported"],["study_b1"]),_u("B1",8,"B1 review",["conditional","relative","reported"],["work_b1","study_b1"])],
"B2":[_u("B2",1,"Aspectual nuance",["aspectual_nuance","passive"],["society_b2"]),_u("B2",2,"Causation",["causative","cause_purpose"],["work_b1"]),_u("B2",3,"Contrast and concession",["concession","discourse"],["society_b2"]),_u("B2",4,"Extended clauses",["relative","reported"],["environment_b2"]),_u("B2",5,"Environment and society",["discourse","passive"],["environment_b2","society_b2"]),_u("B2",6,"Formal explanations",["concession","aspectual_nuance"],["media_c1"]),_u("B2",7,"Complex communication",["causative","discourse"],["work_b1","media_c1"]),_u("B2",8,"B2 review",["passive","concession","discourse"],["society_b2","environment_b2"])],
"C1":[_u("C1",1,"Academic knowledge",["nominalization","evidentiality"],["academic_c1"]),_u("C1",2,"Institutional communication",["formal_register","argumentation"],["institutional_c1"]),_u("C1",3,"Media and evidence",["evidentiality","reported"],["media_c1"]),_u("C1",4,"Embedded questions",["embedded_questions","information_structure"],["academic_c1"]),_u("C1",5,"Academic argument",["argumentation","hedging"],["academic_c1"]),_u("C1",6,"Formal register",["formal_register","nominalization"],["institutional_c1"]),_u("C1",7,"Topic and focus",["information_structure","evidentiality"],["media_c1"]),_u("C1",8,"C1 review",["argumentation","formal_register","hedging"],["academic_c1","institutional_c1"])],
"C2":[_u("C2",1,"Pragmatic nuance",["pragmatics","rhetoric"],["discourse_c2"]),_u("C2",2,"Literary language",["rhetoric","discourse_analysis"],["culture_c2"]),_u("C2",3,"Register shifting",["formal_register","pragmatics"],["institutional_c1"]),_u("C2",4,"Discourse analysis",["discourse_analysis","information_structure"],["discourse_c2"]),_u("C2",5,"Translation and paraphrase",["translation","pragmatics"],["culture_c2"]),_u("C2",6,"Advanced argumentation",["argumentation","rhetoric"],["discourse_c2"]),_u("C2",7,"Media and literary discourse",["rhetoric","discourse_analysis"],["culture_c2","media_c1"]),_u("C2",8,"C2 review",["translation","pragmatics","discourse_analysis"],["discourse_c2","culture_c2"])],
}

ASSESSMENT_BANK=[
AssessmentQuestion(id="ee-a1-001",skill="vocabulary",difficulty="A1",question="Which Ewe expression is a greeting?",options=["Woezɔ","akpe","tsi","afi"],correct="Woezɔ"),
AssessmentQuestion(id="ee-a1-002",skill="communication",difficulty="A1",question="Which expression introduces your name?",options=["nye ŋkɔe...","egbe","aƒe","tsi"],correct="nye ŋkɔe..."),
AssessmentQuestion(id="ee-a2-001",skill="grammar",difficulty="A2",question="Which pattern describes an ongoing action?",options=["mele nu ŋlɔm","meyi","akpe","Woezɔ"],correct="mele nu ŋlɔm"),
AssessmentQuestion(id="ee-a2-002",skill="grammar",difficulty="A2",question="Which form expresses a future plan?",options=["meyi","maɖu nu","mele afima","meɖu nu"],correct="maɖu nu"),
AssessmentQuestion(id="ee-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["ne èva la, míayi","meyi","akpe","egbe"],correct="ne èva la, míayi"),
AssessmentQuestion(id="ee-b1-002",skill="grammar",difficulty="B1",question="Which sentence reports another person's statement?",options=["egblɔ be yeyi","meɖu nu","meyi","Woezɔ"],correct="egblɔ be yeyi"),
AssessmentQuestion(id="ee-b2-001",skill="discourse",difficulty="B2",question="Which connector introduces a contrast?",options=["ke boŋ","egbe","akpe","tsi"],correct="ke boŋ"),
AssessmentQuestion(id="ee-b2-002",skill="grammar",difficulty="B2",question="Which pattern expresses causation?",options=["eɖo ameawo be woava","Woezɔ","afi kae?","akpe"],correct="eɖo ameawo be woava"),
AssessmentQuestion(id="ee-c1-001",skill="academic",difficulty="C1",question="Which phrase qualifies an academic claim?",options=["Ate ŋu anye be...","Woezɔ","tsi","aƒe"],correct="Ate ŋu anye be..."),
AssessmentQuestion(id="ee-c1-002",skill="formal",difficulty="C1",question="Which area requires formal institutional register?",options=["administrative communication","basic greetings","counting","food vocabulary"],correct="administrative communication"),
AssessmentQuestion(id="ee-c2-001",skill="pragmatics",difficulty="C2",question="What should advanced Ewe pragmatics preserve?",options=["Context, politeness and intended meaning","Only literal word order","Only isolated vocabulary","Only punctuation"],correct="Context, politeness and intended meaning"),
AssessmentQuestion(id="ee-c2-002",skill="translation",difficulty="C2",question="What should advanced translation preserve?",options=["Meaning, register and discourse function","Only individual words","Only sentence length","Only punctuation"],correct="Meaning, register and discourse function"),
]