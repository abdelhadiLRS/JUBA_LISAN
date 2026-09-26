"""Tongan A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

def _g(slug,title,level,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=f"Tongan {level} grammar.",explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

_topics=[
("pronouns","Personal pronouns","A1","Use basic personal references.","Ko au eni. Ko koe ia."),
("identification","Ko identification","A1","Introduce people and identify things.","Ko Sione hoku hingoa."),
("present","Present and ongoing actions","A1","Use ʻoku for present situations.","ʻOku ou ngāue ʻi he ʻaho ni."),
("questions","Basic questions","A1","Ask names, places and simple information.","Ko e hā ho hingoa?"),
("negation","Negation with ʻikai","A1","Make simple negative statements.","ʻOku ʻikai ke u ʻilo."),
("possessives","Possessive constructions","A1","Express ownership and relationships.","Ko hoku ʻapi ʻeni."),
("location","Location and existence","A1","Say where people and things are.","ʻOku ou nofo ʻi Nukuʻalofa."),
("requests","Requests and politeness","A1","Make simple polite requests.","Te ke lava ʻo tokoni mai?"),
("past","Past events","A2","Describe completed events.","Naʻa ku ʻalu ki he maketi."),
("future","Future and intention","A2","Express plans and intentions.","Te u ʻalu ʻapongipongi."),
("aspect","Aspect and event state","A2","Distinguish ongoing, completed and expected events.","ʻOku ou kei ako."),
("plural","Plural participants","A2","Talk about groups and plural participants.","ʻOku nau nofo ʻi heni."),
("comparatives","Comparison","A2","Compare people, places and things.","ʻOku lahi ange ʻa e fale ni."),
("modality","Ability, desire and obligation","A2","Express ability, wishes and necessity.","ʻOku ou fie ako."),
("prepositions","Prepositions and direction","B1","Express source, destination and relations.","ʻOku ou ʻalu ki he falekoloa."),
("conditionals","Conditional clauses","B1","Express conditions and consequences.","Kapau te ke lava, haʻu."),
("relative","Relative clauses","B1","Add information about a noun.","Ko e tangata ʻoku ngāue heni ia."),
("causal","Cause and purpose","B1","Explain reasons and purposes.","Naʻe nofo ʻi ʻapi koeʻuhi naʻe ʻasi ʻa e ʻuha."),
("reported","Reported speech","B1","Report another person's words or view.","Naʻe pehē ʻe Sione te ne haʻu."),
("reflexive","Reflexive and reciprocal meaning","B1","Express actions involving oneself or others mutually.","Naʻa nau fe tokoniʻaki."),
("passive","Passive and affected constructions","B2","Focus on the affected participant.","Naʻe tohi ʻa e tohi ʻe Sione."),
("causative","Causative constructions","B2","Express causing or making something happen.","Naʻe fakatupu ʻe he ʻea ʻa e liliu."),
("concessive","Concession and contrast","B2","Express contrast and concession.","Neongo ʻa e ʻuha, naʻa mau ʻalu."),
("discourse","Discourse connectors","B2","Organize longer explanations.","ʻUluaki, te tau sio ki he palopalema."),
("nominalization","Nominalization","C1","Turn processes into formal nouns.","Ko e fakalakalaka ʻo e ako ʻoku mahuʻinga."),
("hedging","Academic hedging and stance","C1","Qualify claims and express degrees of certainty.","ʻOku ngalingali ʻe liliu ʻa e tuʻunga."),
("embedded","Embedded questions","C1","Embed questions and propositions.","ʻOku ʻikai ke u ʻilo pe ko e fē ʻa e hala."),
("information_structure","Topic and focus","C1","Highlight information in formal discourse.","Ko e tefitoʻi meʻa eni ʻoku tau aleaʻi."),
("formal","Formal and institutional language","C1","Use professional and institutional language.","ʻOku kole atu ke fakafonu ʻa e foomu."),
("argumentation","Academic argumentation","C1","Build claims, evidence and counterclaims.","ʻOku poupouʻi ʻe he fakamoʻoni ʻa e fakakaukau."),
("pragmatics","Politeness and pragmatic nuance","C2","Interpret indirectness, respect and social meaning.","Kapau ʻoku ke loto, te tau toe vakai ki ai."),
("register","Register and style shifting","C2","Shift between conversational and formal styles.","ʻOku liliu ʻa e lea ʻo fakatatau ki he tuʻunga."),
("rhetoric","Rhetorical language","C2","Use emphasis, contrast and persuasive framing.","ʻOku ʻikai ngata pē ʻi he lelei, ka ʻoku mahuʻinga."),
("translation","Translation and paraphrase","C2","Preserve meaning and register across formulations.","ʻOku totonu ke tauhi ʻa e ʻuhinga mo e founga lea."),
("discourse_analysis","Discourse analysis","C2","Analyze cohesion, audience and genre.","ʻOku fakafalala ʻa e ʻuhinga ki he tuʻunga mo e koniteki.")
]
GRAMMAR_TOPICS=[_g(*x) for x in _topics]

def _v(id_,level,topic,ref,items):
    return VocabularySet(id=id_,level=level,topic=topic,unit_ref=ref,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS=[
_v("greetings_a1","A1","greetings","to-a1-unit-1",[("mālō e lelei","phrase","hello","Mālō e lelei!"),("mālō","phrase","thanks / well done","Mālō, kātaki."),("kātaki","phrase","please / excuse me","Kātaki, tokoni mai."),("moʻui","word","life / health","Moʻui lelei!")]),
_v("identity_a1","A1","identity","to-a1-unit-2",[("hingoa","noun","name","Ko e hā ho hingoa?"),("tangata","noun","person","Ko e tangata lelei ia."),("fefine","noun","woman","Ko e fefine ia."),("kaungāmeʻa","noun","friend","Ko hoku kaungāmeʻa ia.")]),
_v("family_a1","A1","family","to-a1-unit-3",[("faʻē","noun","mother","ʻOku nofo hoku faʻē ʻi Nukuʻalofa."),("tamai","noun","father","ʻOku ngāue hoku tamai."),("fānau","noun","children","ʻOku ʻi ʻapi ʻa e fānau."),("tuofefine","noun","sister","Ko hoku tuofefine ia.")]),
_v("home_a1","A1","home","to-a1-unit-4",[("ʻapi","noun","home","Ko hoku ʻapi ʻeni."),("fale","noun","house","Ko hoku fale ʻeni."),("lokí","noun","room","ʻOku ʻi he lokí ʻa Sione."),("matapā","noun","door","ʻOku ava ʻa e matapā.")]),
_v("routine_a1","A1","daily routine","to-a1-unit-5",[("ngāue","verb","work","ʻOku ou ngāue ʻi he ʻaho ni."),("ako","verb","study / learn","ʻOku ou ako ʻi he ʻapiako."),("mohe","verb","sleep","ʻOku ou mohe ʻi he poʻuli."),("pongipongi","noun","morning","ʻOku ou ako ʻi he pongipongi.")]),
_v("food_a1","A1","food and drink","to-a1-unit-6",[("vai","noun","water","ʻOku ou inu vai."),("meʻakai","noun","food","ʻOku ou kai meʻakai."),("inu","verb","drink","ʻOku ou inu vai."),("ika","noun","fish","ʻOku ou kai ika.")]),
_v("shopping_a1","A1","shopping","to-a1-unit-7",[("falekoloa","noun","shop","Ko e fē ʻa e falekoloa?"),("paʻanga","noun","money","ʻOku ʻikai haʻaku paʻanga."),("totongi","noun","price / payment","Ko e hā ʻa e totongi?"),("koloa","noun","goods / item","ʻOku lelei ʻa e koloa.")]),
_v("help_a1","A1","help and directions","to-a1-unit-8",[("tokoni","noun","help","Kātaki, tokoni mai."),("hala","noun","road / way","Ko e fē ʻa e hala?"),("ʻilo","verb","know","ʻOku ʻikai ke u ʻilo."),("mahino","verb","understand","ʻOku mahino kiate au.")]),
_v("travel_a2","A2","travel","to-a2-unit-1",[("ʻalu","verb","go","Te u ʻalu ki he kolo."),("fononga","verb","travel","ʻOku mau fononga ki Tongatapu."),("tikite","noun","ticket","ʻOku ou fakatau ʻa e tikite."),("vakalele","noun","airport","Ko e fē ʻa e vakalele?")]),
_v("health_a2","A2","health","to-a2-unit-2",[("mahaki","noun","illness","ʻOku ou mahaki."),("toketā","noun","doctor","ʻOku ou fie sio ki he toketā."),("sai","adjective","well / good","ʻOku ou sai pē."),("faitoʻo","noun","medicine / treatment","ʻOku ou maʻu ʻa e faitoʻo.")]),
_v("study_a2","A2","study","to-a2-unit-3",[("tohi","noun","book / writing","ʻOku ou lau ʻa e tohi."),("akoʻanga","noun","school / learning place","ʻOku ou ʻalu ki he akoʻanga."),("ako","verb","study","ʻOku ou ako he pō."),("fakamahino","verb","explain","Kātaki, fakamahino mai.")]),
_v("weather_a2","A2","weather","to-a2-unit-4",[("ʻuha","noun","rain","ʻOku ʻuha."),("laʻā","noun","sun","ʻOku māfana ʻa e laʻā."),("matangi","noun","wind","ʻOku mālohi ʻa e matangi."),("momoko","adjective","cold","ʻOku momoko he pō.")]),
_v("work_b1","B1","work and plans","to-b1-unit-1",[("ngaueʻanga","noun","workplace","ʻOku mamaʻo ʻa e ngaueʻanga."),("palani","noun","plan","ʻOku ʻi ai haʻaku palani."),("fatongia","noun","responsibility","Ko e fatongia ʻeni ʻoʻou."),("fakataha","noun","meeting","ʻOku kamata ʻa e fakataha.")]),
_v("community_b1","B1","community","to-b1-unit-2",[("kolo","noun","town / community","ʻOku lelei ʻa e kolo."),("fonua","noun","land / country","ʻOku tau ʻofa ki hotau fonua."),("fāmili","noun","family","ʻOku nofo ʻa e fāmili ʻi heni."),("tokotaha","noun","person / individual","Ko e tokotaha kotoa pē.")]),
_v("environment_b2","B2","environment","to-b2-unit-1",[("ʻātakai","noun","environment","ʻOku totonu ke maluʻi ʻa e ʻātakai."),("maluʻi","verb","protect","Ke tau maluʻi ʻa e ʻātakai."),("fakaʻauha","verb","destroy","ʻOku kovi ʻa e fakaʻauha ʻo e meʻa moʻui."),("moʻunga","noun","mountain","ʻOku māʻolunga ʻa e moʻunga.")]),
_v("economy_b2","B2","economy","to-b2-unit-2",[("pisinisi","noun","business","ʻOku tupu ʻa e pisinisi."),("meʻa fakapaʻanga","noun","financial matter","ʻOku mahuʻinga ʻa e meʻa fakapaʻanga."),("paʻanga hū mai","noun","income","ʻOku lahi ʻa e paʻanga hū mai."),("fakatau","verb","buy / sell","ʻOku ou fakatau ʻa e koloa.")]),
_v("media_c1","C1","media","to-c1-unit-1",[("ongoongo","noun","news","ʻOku tau lau ʻa e ongoongo."),("maʻuʻanga fakamatala","noun","source of information","Ko e maʻuʻanga fakamatala ʻoku totonu ke falalaʻanga."),("fakamatala","noun","information","ʻOku mahuʻinga ʻa e fakamatala."),("vakai","noun","view / perspective","ʻOku kehekehe ʻa e vakai.")]),
_v("academic_c1","C1","academic","to-c1-unit-2",[("fakamoʻoni","noun","evidence","ʻOku poupou ʻa e fakamoʻoni ki he fakakaukau."),("fakakaukau","noun","idea / argument","ʻOku mālohi ʻa e fakakaukau."),("fekumi","verb","research / investigate","ʻOku mau fekumi ki he tali."),("fakamatala fakaako","noun","academic explanation","ʻOku mahino ʻa e fakamatala fakaako.")]),
_v("institutional_c1","C1","institutional","to-c1-unit-3",[("tuʻutuʻuni","noun","decision / regulation","ʻOku fakahoko ʻa e tuʻutuʻuni."),("tohi kole","noun","application","ʻOku ou fakafonu ʻa e tohi kole."),("falealea","noun","council / assembly","ʻOku fakataha ʻa e falealea."),("taki","verb","lead / govern","ʻOku taki ʻe he pule ʻa e ngāue.")]),
_v("culture_c2","C2","culture","to-c2-unit-1",[("anga fakafonua","noun","culture / customs","ʻOku mahuʻinga ʻa e anga fakafonua."),("tukufakaholo","noun","tradition / heritage","ʻOku tauhi ʻa e tukufakaholo."),("fakaʻapaʻapa","noun","respect","ʻOku mahuʻinga ʻa e fakaʻapaʻapa."),("ʻulungaanga","noun","character / behavior","ʻOku liliu ʻa e ʻulungaanga ʻo e lea.")]),
_v("discourse_c2","C2","discourse","to-c2-unit-2",[("fetalanoaʻaki","noun","conversation / discourse","ʻOku lelei ʻa e fetalanoaʻaki."),("ʻuhinga","noun","meaning","ʻOku fakafalala ʻa e ʻuhinga ki he koniteki."),("founga lea","noun","style of expression","ʻOku kehekehe ʻa e founga lea."),("liliu lea","noun","translation","ʻOku tauhi ʻe he liliu lea ʻa e ʻuhinga.")])
]

def _p(id_,level,situation,items,register="neutral"):
    return PhrasebookCategory(id=id_,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=register) for t,c in items])

PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","A1","greetings",[("Mālō e lelei!","greeting"),("Ko hoku hingoa ko Sione.","introduction"),("Fiefia ke tau fetaulaki.","meeting someone")]),
_p("thanks_a1","A1","thanks and politeness",[("Mālō.","thanks"),("Mālō ʻaupito.","strong thanks"),("Kātaki.","please / excuse me")]),
_p("shopping_a1","A1","shopping",[("Ko e hā ʻa e totongi?","asking price"),("ʻOku ou fiemaʻu ʻeni.","requesting an item"),("ʻOku ʻi ai ha toe taha?","asking for another item")]),
_p("directions_a1","A1","directions",[("Ko e fē ʻa e falekoloa?","asking location"),("Ko e fē ʻa e hala?","asking the way"),("Kātaki, tokoni mai.","asking for help")]),
_p("daily_a1","A1","daily life",[("Fēfē hake?","asking how someone is"),("ʻOku ou ngāue ʻi he ʻaho ni.","daily routine"),("ʻOku ou nofo ʻi Nukuʻalofa.","personal information")]),
_p("travel_a2","A2","travel",[("Te u ʻalu ʻapongipongi.","future travel"),("Ko e fē ʻa e vakalele?","airport"),("ʻOku ou fie fakatau tikite.","ticket")]),
_p("health_a2","A2","health",[("ʻOku ou mahaki.","illness"),("ʻOku ou fie sio ki he toketā.","doctor"),("ʻOku ou fiemaʻu ʻa e faitoʻo.","medicine")]),
_p("study_b1","B1","study",[("Kātaki, fakamahino mai.","asking for explanation"),("ʻOku ʻikai ke u mahino.","clarification"),("Tali mai ʻa e fehuʻi.","answering a question")]),
_p("work_b1","B1","work",[("Te tau aleaʻi ʻa e palani.","discussing a plan"),("ʻOku ou fokotuʻu atu ...","making a suggestion"),("ʻOku ou loto ki ai.","agreement")]),
_p("formal_b2","B2","formal communication",[("ʻOku kole atu ke ...","formal request"),("ʻOku fakahaaʻi ʻe he fakamatala ...","formal statement"),("Mālō ʻaupito ʻi homou tokoni.","formal thanks")],"formal"),
_p("academic_c1","C1","academic discussion",[("ʻOku ngalingali ʻe ...","hedging"),("ʻOku fakahaaʻi ʻe he fakamoʻoni ...","evidence"),("Neongo ia, ʻoku totonu ke ...","qualification")],"academic"),
_p("presentation_c1","C1","presentation",[("ʻUluaki, te tau sio ki ...","opening"),("Ko e tefitoʻi meʻa ...","highlighting"),("ʻI he fakaʻosi ...","closing")],"formal"),
_p("pragmatics_c2","C2","pragmatic nuance",[("Kapau ʻoku ke loto, te tau ...","softening"),("ʻOku ou mahino ki heʻetau kehekehe, ka ...","polite disagreement"),("ʻOku malava ke tau toe vakai ki ai.","tentative suggestion")],"polite")
]

def _u(level,n,title,grammar,vocab):
    return CurriculumUnit(id=f"to-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=vocab,lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Communicate effectively at {level}",f"Understand level-appropriate Tongan"],default_weeks=2)

CURRICULUM={}
plans={
"A1":[("Ko e ngaahi talitali mo e ngaahi hingoa",["pronouns","identification"],["greetings_a1"]),("Ko hai koe?",["questions","possessives"],["identity_a1"]),("Ko e fāmili",["possessives","plural"],["family_a1"]),("ʻApi mo e ngaahi feituʻu",["location","questions"],["home_a1"]),("Ngaahi ngāue fakaʻaho",["present","negation"],["routine_a1"]),("Meʻakai mo e inu",["present","requests"],["food_a1"]),("Fakatau mo e paʻanga",["questions","negation"],["shopping_a1"]),("Tokoni mo e ngaahi hala",["requests","location"],["help_a1"])],
"A2":[("Fononga",["future","prepositions"],["travel_a2"]),("Moʻui mo e faitoʻo",["modality","aspect"],["health_a2"]),("Ako mo e ngaahi tohi",["past","aspect"],["study_a2"]),("ʻEa mo e taimi",["present","comparatives"],["weather_a2"]),("Ngaahi palani",["future","modality"],["work_b1"]),("Ngaahi faʻahinga",["comparatives","plural"],["community_b1"]),("Ngaahi meʻa kuo hoko",["past","aspect"],["travel_a2"]),("Toe fakamanatu A2",["past","future","aspect"],["study_a2","weather_a2"])],
"B1":[("Ngaue mo e fetalanoaʻaki",["prepositions","relative"],["work_b1"]),("Palani mo e ngaahi tuʻunga",["conditionals","future"],["work_b1"]),("Kolo mo e komiuniti",["relative","discourse"],["community_b1"]),("Koeʻuhi mo e taumuʻa",["causal","concessive"],["community_b1"]),("Lea kuo fakamatala",["reported","embedded"],["media_c1"]),("Fealeaʻaki mo e fetokoni",["reflexive","discourse"],["community_b1"]),("Fakamatala mo e fakakaukau",["reported","relative"],["media_c1"]),("Toe fakamanatu B1",["conditionals","causal","reported"],["work_b1","media_c1"])],
"B2":[("Ngaahi ngāue ʻoku fakahoko",["passive","causative"],["work_b1"]),("Meʻa ʻoku fakatupu",["causative","aspect"],["economy_b2"]),("Kehekehe mo e fetalanoaʻaki",["concessive","discourse"],["community_b1"]),("Paʻanga mo e pisinisi",["passive","discourse"],["economy_b2"]),("ʻAtakai mo e fonua",["concessive","causal"],["environment_b2"]),("Fakamatala fakalōloa",["discourse","relative"],["media_c1"]),("Sio fakaanga ki he fakamatala",["passive","reported"],["media_c1"]),("Toe fakamanatu B2",["passive","concessive","discourse"],["environment_b2","economy_b2"])],
"C1":[("Fakamoʻoni mo e fekumi",["nominalization","hedging"],["academic_c1"]),("Ngaahi kautaha mo e tuʻutuʻuni",["formal","argumentation"],["institutional_c1"]),("Ongoongo mo e maʻuʻanga fakamatala",["information_structure","reported"],["media_c1"]),("Ngaahi fehuʻi ʻoku fakafufū",["embedded","causal"],["academic_c1"]),("Fetalanoaʻaki fakaako",["argumentation","discourse"],["academic_c1"]),("Lea fakaʻofisiale",["formal","hedging"],["institutional_c1"]),("Tefitoʻi fakamatala mo e fakamamafa",["information_structure","nominalization"],["media_c1"]),("Toe fakamanatu C1",["argumentation","formal","embedded"],["academic_c1","institutional_c1"])],
"C2":[("Fakaʻapaʻapa mo e pragmatics",["pragmatics","register"],["discourse_c2"]),("Rhetoric mo e lea fakaako",["rhetoric","discourse_analysis"],["culture_c2"]),("Liliu ʻo e founga lea",["register","pragmatics"],["institutional_c1"]),("Sivi ʻo e fetalanoaʻaki",["discourse_analysis","information_structure"],["discourse_c2"]),("Liliu lea mo e paraphrase",["translation","register"],["culture_c2"]),("Fakamatala mo e fakalotoʻi",["argumentation","rhetoric"],["discourse_c2"]),("ʻUlungaanga mo e ongoongo",["rhetoric","register"],["culture_c2","media_c1"]),("Toe fakamanatu C2",["translation","pragmatics","discourse_analysis"],["discourse_c2","culture_c2"])]
}
for level,items in plans.items():
    CURRICULUM[level]=[_u(level,i+1,title,grammar,vocab) for i,(title,grammar,vocab) in enumerate(items)]

ASSESSMENT_BANK=[
AssessmentQuestion(id="to-a1-001",skill="communication",difficulty="A1",question="Which Tongan phrase is a greeting?",options=["Mālō e lelei!","Ko e hā ʻa e totongi?","Ko e fē ʻa e hala?","Kātaki, tokoni mai."],correct="Mālō e lelei!"),
AssessmentQuestion(id="to-a1-002",skill="communication",difficulty="A1",question="Which question asks someone's name?",options=["Ko e hā ho hingoa?","Ko e hā ʻa e totongi?","Ko e fē ʻa e falekoloa?","Mālō e lelei!"],correct="Ko e hā ho hingoa?"),
AssessmentQuestion(id="to-a1-003",skill="reading",difficulty="A1",question="Which sentence says “My mother lives in Nukuʻalofa”?",options=["ʻOku nofo hoku faʻē ʻi Nukuʻalofa.","ʻOku ngāue hoku tamai.","ʻOku ʻi ʻapi ʻa e fānau.","ʻOku ou inu vai."],correct="ʻOku nofo hoku faʻē ʻi Nukuʻalofa."),
AssessmentQuestion(id="to-a1-004",skill="grammar",difficulty="A1",question="Which sentence means “This is my home”?",options=["Ko hoku ʻapi ʻeni.","Ko hoku kaungāmeʻa ia.","ʻOku ou ako ʻi he ʻapiako.","ʻOku ou nofo ʻi Nukuʻalofa."],correct="Ko hoku ʻapi ʻeni."),
AssessmentQuestion(id="to-a1-005",skill="vocabulary",difficulty="A1",question="Which word means “work”?",options=["ngāue","vai","falekoloa","hingoa"],correct="ngāue"),
AssessmentQuestion(id="to-a2-001",skill="grammar",difficulty="A2",question="Which sentence expresses a future plan?",options=["Te u ʻalu ʻapongipongi.","ʻOku ou nofo ʻi heni.","ʻOku ʻikai ke u ʻilo.","Mālō e lelei!"],correct="Te u ʻalu ʻapongipongi."),
AssessmentQuestion(id="to-a2-002",skill="vocabulary",difficulty="A2",question="Which word means “doctor”?",options=["toketā","tikite","ʻuha","tohi"],correct="toketā"),
AssessmentQuestion(id="to-b1-001",skill="grammar",difficulty="B1",question="Which sentence introduces a condition?",options=["Kapau te ke lava, haʻu.","ʻOku ou ako.","Te u ʻalu ʻapongipongi.","Mālō e lelei!"],correct="Kapau te ke lava, haʻu."),
AssessmentQuestion(id="to-b1-002",skill="grammar",difficulty="B1",question="Which sentence reports another person's words?",options=["Naʻe pehē ʻe Sione te ne haʻu.","ʻOku ou inu vai.","Ko e fē ʻa e hala?","Kātaki."],correct="Naʻe pehē ʻe Sione te ne haʻu."),
AssessmentQuestion(id="to-b2-001",skill="grammar",difficulty="B2",question="Which sentence is a passive construction?",options=["Naʻe tohi ʻa e tohi ʻe Sione.","Te u ʻalu ʻapongipongi.","Ko e hā ho hingoa?","ʻOku ou ako."],correct="Naʻe tohi ʻa e tohi ʻe Sione."),
AssessmentQuestion(id="to-b2-002",skill="discourse",difficulty="B2",question="Which phrase introduces a sequence?",options=["ʻUluaki, te tau sio ki he palopalema.","Mālō e lelei!","Ko e hā ho hingoa?","ʻOku ou inu vai."],correct="ʻUluaki, te tau sio ki he palopalema."),
AssessmentQuestion(id="to-c1-001",skill="academic",difficulty="C1",question="Which word means “evidence”?",options=["fakamoʻoni","fakaʻapaʻapa","tikite","falekoloa"],correct="fakamoʻoni"),
AssessmentQuestion(id="to-c1-002",skill="academic",difficulty="C1",question="Which phrase expresses academic hedging?",options=["ʻOku ngalingali ʻe ...","Mālō e lelei!","Ko e hā ho hingoa?","Kātaki, tokoni mai."],correct="ʻOku ngalingali ʻe ..."),
AssessmentQuestion(id="to-c2-001",skill="discourse",difficulty="C2",question="Which concept concerns meaning, audience and context in advanced communication?",options=["pragmatics","greetings","shopping","family"],correct="pragmatics")
]
