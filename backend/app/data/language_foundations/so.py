"""Somali foundation data for JUBA LISAN."""

from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic,
    VocabularyEntry, VocabularySet, PhrasebookCategory,
    PhrasebookEntry, AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

_GRAMMAR = [
("pronouns","Magac-u-yaallada qofka","A1","syntax","Use personal pronouns and simple identity statements.","Anigu waxaan ahay arday."),
("word-order","Qaabka jumladda","A1","syntax","Build simple Somali sentences with clear subject and predicate order.","Waxaan akhriyaa buug."),
("present","Waqtiga hadda","A1","verbs","Use present constructions for routines and current facts.","Waxaan bartaa Af-Soomaali."),
("negation","Diidmada","A1","syntax","Use negative constructions such as ma and ma aha.","Ma fahmin."),
("questions","Su'aalaha","A1","communication","Ask basic who, what, where, when and how questions.","Xaggee baad degan tahay?"),
("possession","Lahaanshaha","A1","grammar","Express possession with common Somali possessive patterns.","Kani waa buuggayga."),
("plurals","Jamac","A1","nouns","Recognise and use common plural noun patterns.","Carruurtu way ciyaarayaan."),
("locative","Goob iyo jihayn","A1","grammar","Describe location and simple movement.","Waxaan aadayaa suuqa."),
("past","Waqtiga tagay","A2","verbs","Talk about completed events and recent experiences.","Shalay ayaan suuqa aaday."),
("future","Waqtiga mustaqbalka","A2","verbs","Express plans, intentions and predictions.","Berri ayaan iman doonaa."),
("modality","Kartida iyo waajibka","A2","modality","Express ability, necessity, permission and intention.","Waa inaan shaqeeyaa."),
("prepositions","Xiriiriyeyaasha goobta","A2","grammar","Use common relational and locative constructions.","Waxaan joogaa guriga."),
("comparatives","Isbarbardhig","A2","adjectives","Compare people, objects and situations.","Kan ayaa ka weyn kan kale."),
("reflexive","Fal-celiska qofka","A2","verbs","Express actions directed toward the subject.","Waan is dhaqayaa."),
("subordination","Jumlado hoosaad","B1","syntax","Connect clauses with sabab, waqti and condition structures.","Waan joogayaa sababtoo ah roob baa da'aya."),
("relative","Jumlado tilmaamaya","B1","syntax","Describe nouns with relative clauses.","Buugga aan akhriyayo waa cusub."),
("conditional","Shuruud","B1","verbs","Express real and hypothetical conditions.","Haddii aan waqti helo, waan imanayaa."),
("reported-speech","Hadal la soo tebiyey","B1","discourse","Report another person's words or information.","Wuxuu yiri inuu iman doono."),
("aspect","Dhacdo iyo socod","B1","verbs","Distinguish completed, ongoing and habitual events through context and construction.","Waan akhrinayay markii uu yimid."),
("connectors","Xiriiriyeyaasha hadalka","B1","discourse","Link reasons, contrasts, results and conclusions.","Waan daalay, laakiin waan sii waday."),
("passive","Dhismaha aan falaha muujin","B2","syntax","Use constructions that foreground the action or result rather than the agent.","Warbixinta waa la diray."),
("causal-concessive","Sabab iyo inkastoo","B2","syntax","Express cause, consequence, contrast and concession precisely.","Inkastoo uu roob da'ayo, waan baxay."),
("complex-relative","Tilmaamid adag","B2","syntax","Handle longer noun phrases and embedded descriptions.","Mashruuca aan shalay ka hadlaynay wuu muhiim yahay."),
("nominalization","Magacayn rasmi ah","B2","style","Use noun-based formulations in formal contexts.","Hirgelinta qorshuhu waa muhiim."),
("formal-register","Luqad rasmi ah","B2","register","Adapt Somali to professional and institutional communication.","Waxaan kaa codsanaynaa inaad foomka buuxiso."),
("academic-hedging","Taxaddarka aqooneed","C1","academic","Qualify claims and distinguish evidence from interpretation.","Natiijooyinku waxay muujin karaan in ..."),
("embedded-questions","Su'aalo ku dhex jira","C1","syntax","Embed questions within statements and requests.","Ma garanayo goorta uu imanayo."),
("information-structure","Diiradda iyo mawduuca","C1","discourse","Control topic, focus and new information for clarity.","Qodobkan gaar ahaan waa muhiim."),
("complex-subordination","Hoos-u-xirnaan adag","C1","syntax","Combine multiple subordinate relations while maintaining clarity.","Inkasta oo xaaladdu adag tahay, waxaan sii wadi karnaa."),
("institutional-style","Qoraalka hay'adaha","C1","professional","Write precise notices, requests and administrative texts.","Codsiga waa in la gudbiyaa Jimcaha."),
("idioms","Maahmaah iyo weedho sarbeeb ah","C2","lexis","Interpret idiomatic meaning from context.","Waa dhibic biyo ah oo badda ku dhacday."),
("register-shifting","Beddelka heerka hadalka","C2","pragmatics","Shift between conversational, professional, academic and public registers.","Fadlan ma xaqiijin kartaa?"),
("rhetoric","Dood iyo qancin","C2","rhetoric","Build nuanced claims, concessions and rebuttals.","Dooddu waa qancin kartaa, laakiin caddayntu way xaddidan tahay."),
("literary-style","Qaab suugaaneed","C2","style","Interpret imagery, rhythm and deliberate stylistic variation.","Magaaladu si tartiib ah ayay u soo toostay."),
("translation","Saxnaanta tarjumaadda","C2","translation","Choose context-sensitive Somali equivalents rather than literal calques.","Macnuhu wuxuu ku xiran yahay xaaladda."),
]
GRAMMAR_TOPICS = [GrammarTopic(slug=s,title=t,level=l,category=c,summary=sm,explanation=sm,examples=[GrammarExample(text=e)]) for s,t,l,c,sm,e in _GRAMMAR]

_VOCAB = {
"A1":[("Salaan","salaan","noun","greeting","Salaan, sidee tahay?"),("Qof","qof","noun","person","Qofkani waa arday."),("Qoys","qoys","noun","family","Qoyskaygu halkan ayuu deggan yahay."),("Guri","guri","noun","house","Gurigu waa weyn yahay."),("Shaqo","shaqo","noun","work","Shaqo ayaan hayaa."),("Waqti","saacad","noun","hour","Hal saac ayaan sugayaa."),("Cunto","cunto","noun","food","Cuntadu waa fiican tahay."),("Suuq","suuq","noun","market","Waxaan aadayaa suuqa.")],
"A2":[("Safar","tigidh","noun","ticket","Waxaan haystaa tigidh."),("Caafimaad","dhakhtar","noun","doctor","Dhakhtarka ayaan u socdaa."),("Wax-iibsasho","qiime","noun","price","Qiimuhu waa imisa?"),("Cimilo","roob","noun","rain","Maanta roob baa da'aya.")],
"B1":[("Shaqo","khibrad","noun","experience","Waxaan leeyahay khibrad badan."),("Waxbarasho","koorso","noun","course","Koorso cusub ayaan bilaabay."),("Bulsho","bulsho","noun","society","Bulshadu way wada shaqaysaa."),("Fikir","aragti","noun","opinion","Aragtidayda waa muhiim.")],
"B2":[("Xirfad","xog","noun","data","Xogta waa la ilaaliyaa."),("Maamul","codsi","noun","application","Codsiga waa la gudbiyey."),("Warbaahin","war","noun","news","Warka waan akhriyey."),("Deegaan","deegaan","noun","environment","Waa inaan deegaanka ilaalinaa.")],
"C1":[("Aqoon","caddayn","noun","evidence","Caddayntu way khusaysaa."),("Falanqayn","horumar","noun","development","Horumarku waa muhiim."),("Maamul","shuruud","noun","requirement","Tani waa shuruud muhiim ah."),("Dood","gunaanad","noun","conclusion","Gunaanadku waa inuu taxaddar yeeshaa.")],
"C2":[("Dood","nuance","noun","nuance","Nuance-ku wuxuu muhiim u yahay tarjumaadda."),("Macne","xaalad","noun","context","Macnuhu wuxuu ku xiran yahay xaaladda."),("Suugaan","sarbeeb","noun","metaphor","Sarbeebtu waxay xoojisaa mawduuca."),("Tarjumaad","macne","noun","meaning","Macnaha saxda ahi wuxuu ku xiran yahay duruufaha.")],
}
VOCABULARY_SETS=[]
for level,rows in _VOCAB.items():
    for i,(topic,word,pos,definition,example) in enumerate(rows,1):
        VOCABULARY_SETS.append(VocabularySet(id=f"so-{level.lower()}-{i}",level=level,topic=topic,unit_ref=f"so-{level.lower()}-unit-{i}",words=[VocabularyEntry(word=word,pos=pos,definition=definition,example=example)]))

_TITLES={
"A1":["Isbarasho","Qoyska","Guriga","Nolol maalmeedka","Waqti iyo ballamo","Cunto iyo wax-iibsi","Goobo iyo jihooyin","Isgaarsiinta maalinlaha"],
"A2":["Khibradaha hore","Qorshayaasha mustaqbalka","Kartida iyo waajibaadka","Safar iyo dhaqdhaqaaq","Isbarbardhig iyo doorasho","Caafimaad iyo nolol"],
"B1":["Sabab iyo sharaxaad","Sharaxaadda dadka iyo waxyaabaha","Xaaladaha shuruudda","Warbixin iyo hadal la soo tebiyey","Sheeko iyo dhacdooyin","Fikrado iyo dood"],
"B2":["Habraacyo iyo natiijooyin","Is-diidid iyo tanaasul","Sharaxaad adag","Codsiyo iyo maamul","Isgaarsiin xirfadeed","Qoraal isku dhafan"],
"C1":["Caddayn iyo sheegasho","Isgaarsiin ku dhex jirta","Diirad iyo soo bandhigid","Dood adag","Qoraal hay'adeed","Qoraal xirfadeed sare"],
"C2":["Sarbeeb iyo nuance","Xakamaynta heerka hadalka","Dood qancin leh","Fasiraadda suugaanta","Doorashada tarjumaadda","Synthesis iyo aqoon buuxda"],
}
_OFF={"A1":0,"A2":8,"B1":14,"B2":20,"C1":26,"C2":32}
CURRICULUM={}
for level,titles in _TITLES.items():
    CURRICULUM[level]=[]
    for i,title in enumerate(titles,1):
        idx=_OFF[level]+i-1
        CURRICULUM[level].append(CurriculumUnit(id=f"so-{level.lower()}-unit-{i}",level=level,unit_number=i,title=f"Somali {level} · {title}",grammar_points=[_GRAMMAR[idx][0]],vocabulary_set_ids=[f"so-{level.lower()}-{min(i,len(_VOCAB[level]))}"],lesson_types=["grammar","vocabulary","reading","writing","listening","speaking","review"],competency_checklist=[f"Use Somali for {title.lower()}","Complete guided CEFR-level tasks"],default_weeks=2))

_PHRASES={
"A1":[("Salaan","👋",["Salaan, sidee tahay?","Magacaygu waa ...","Mahadsanid."]),("Caawimo","🆘",["Fadlan i caawi.","Ma fahmin.","Fadlan mar kale sheeg."])],
"A2":[("Safar","🧳",["Xaggee saldhiggu ku yaal?","Hal tigidh, fadlan.","Goorma ayuu tareenku baxayaa?"]),("Caafimaad","🩺",["Ma fiicni.","Waxaan u baahanahay dhakhtar.","Waxaan leeyahay ballan."])],
"B1":[("Fikrad","💭",["Aragtidayda ...","Waan kugu raacsanahay.","Waan fahmay fikraddaada."]),("Shaqo","💼",["Ma ka wada hadli karnaa?","Dukumentiga maanta ayaan dirayaa.","Goorma ayay kulanku dhacayaa?"])],
"B2":[("Kulammo","📅",["Qodobkan ma sii falanqayn karnaa?","Waxaan soo jeedinayaa in ...","Aan isbarbardhigno doorashooyinka."]),("Maamul","🏛️",["Codsiga waa la farsameynayaa.","Fadlan qoraal ku xaqiiji.","Dukumentiga waa in la gudbiyaa."])],
"C1":[("Aqoonta","🎓",["Natiijooyinku waxay muujin karaan in ...","Waa muhiim in xogta la fasirto.","Caddayntu waxay taageeraysaa gunaanadkan."]),("Soo-bandhigid","📊",["Aan xoogga saaro qodobkan.","Marka hore ...","Ugu dambayn waxaa la oran karaa ..."])],
"C2":[("Dood","⚖️",["Fasiraaddani waa suurtagal, laakiin ...","Waxay si weyn ugu xiran tahay xaaladda.","Waxaan rabaa inaan kala saaro ..."]),("Suugaan","📚",["Weedhani waxay leedahay macne laba-geesood ah.","Sarbeebtu waxay xoojisaa mawduuca.","Qoraalkan siyaabo kala duwan ayaa loo fasiri karaa."])],
}
PHRASEBOOK_CATEGORIES=[]
for level,cats in _PHRASES.items():
    for i,(situation,icon,phrases) in enumerate(cats,1):
        PHRASEBOOK_CATEGORIES.append(PhrasebookCategory(id=f"so-{level.lower()}-phrases-{i}",level=level,situation=situation,icon=icon,phrases=[PhrasebookEntry(text=p,context=situation,register="neutral" if level in ("A1","A2") else "formal",unit_ref=f"so-{level.lower()}-unit-{i}") for p in phrases]))

ASSESSMENT_BANK=[
AssessmentQuestion(id="so-a1-001",skill="communication",difficulty="A1",question="Which Somali phrase means Hello?",options=["Salaan","Mahadsanid","Ma fahmin","Fadlan i caawi."],correct="Salaan",grammar_slug="pronouns"),
AssessmentQuestion(id="so-a1-002",skill="grammar",difficulty="A1",question="Which sentence expresses a negative meaning?",options=["Ma fahmin.","Waan fahmay.","Waan imaanayaa.","Waan akhriyayaa."],correct="Ma fahmin.",grammar_slug="negation"),
AssessmentQuestion(id="so-a2-001",skill="grammar",difficulty="A2",question="Which sentence refers to tomorrow?",options=["Berri ayaan iman doonaa.","Shalay ayaan imid.","Maanta ayaan joogaa.","Shalay ayaan joogay."],correct="Berri ayaan iman doonaa.",grammar_slug="future"),
AssessmentQuestion(id="so-a2-002",skill="vocabulary",difficulty="A2",question="Which word means doctor?",options=["dhakhtar","tigidh","qiime","roob"],correct="dhakhtar"),
AssessmentQuestion(id="so-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["Haddii aan waqti helo, waan imanayaa.","Waan imanayaa maanta.","Shalay ayaan imid.","Waan shaqeeyaa."],correct="Haddii aan waqti helo, waan imanayaa.",grammar_slug="conditional"),
AssessmentQuestion(id="so-b1-002",skill="discourse",difficulty="B1",question="Which phrase introduces an opinion?",options=["Aragtidayda ...","Mahadsanid.","Salaan.","Xaggee baad degan tahay?"],correct="Aragtidayda ...",grammar_slug="connectors"),
AssessmentQuestion(id="so-b2-001",skill="grammar",difficulty="B2",question="Which sentence foregrounds the action rather than the agent?",options=["Warbixinta waa la diray.","Waxaan diray warbixinta.","Wuu diray warbixinta.","Warbixintu way dheer tahay."],correct="Warbixinta waa la diray.",grammar_slug="passive"),
AssessmentQuestion(id="so-b2-002",skill="communication",difficulty="B2",question="Which phrase is suitable for formal administration?",options=["Fadlan qoraal ku xaqiiji.","I sii hadda.","Maxay tani tahay?","Haye, soo dir."],correct="Fadlan qoraal ku xaqiiji.",grammar_slug="formal-register"),
AssessmentQuestion(id="so-c1-001",skill="grammar",difficulty="C1",question="Which sentence contains an embedded question?",options=["Ma garanayo goorta uu imanayo.","Goorma ayuu imaanayaa?","Wuu imanayaa berri.","Waan ogahay."],correct="Ma garanayo goorta uu imanayo.",grammar_slug="embedded-questions"),
AssessmentQuestion(id="so-c1-002",skill="reading",difficulty="C1",question="Which expression appropriately qualifies an academic claim?",options=["Natiijooyinku waxay muujin karaan in ...","Tani mar walba waa run.","Tani wax walba ayay caddaynaysaa.","Qof walba wuu ogyahay."],correct="Natiijooyinku waxay muujin karaan in ...",grammar_slug="academic-hedging"),
AssessmentQuestion(id="so-c2-001",skill="rhetoric",difficulty="C2",question="Which phrase introduces a qualified counterargument?",options=["Fasiraaddani waa suurtagal, laakiin ...","Taasi waa khalad.","Ma aqaan.","Waxba kama jiraan."],correct="Fasiraaddani waa suurtagal, laakiin ...",grammar_slug="rhetoric"),
AssessmentQuestion(id="so-c2-002",skill="translation",difficulty="C2",question="What is central to advanced translation?",options=["Context-sensitive equivalents","Literal word-for-word translation","Ignoring context","One synonym everywhere"],correct="Context-sensitive equivalents",grammar_slug="translation"),
]
