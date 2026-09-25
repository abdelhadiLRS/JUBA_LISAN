"""Luxembourgish foundation data for JUBA LISAN."""

from app.data._types import (
    CurriculumUnit,
    GrammarExample,
    GrammarTopic,
    VocabularyEntry,
    VocabularySet,
    PhrasebookCategory,
    PhrasebookEntry,
    AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

_GRAMMAR = [
    ("identity-pronouns","Identitéit a Personalpronomen","A1","syntax","Ech sinn, du bass, hien ass a si sinn am Alldag.","Ech sinn Anna."),
    ("basic-word-order","Basiswuertstellung","A1","syntax","Luxembourgish uses a clear finite-verb position in main clauses.","Ech wunnen zu Lëtzebuerg."),
    ("present-tense","Presens","A1","verbs","Use common present-tense forms for routines and facts.","Ech schaffen haut."),
    ("definite-article","Bestëmmten Artikel","A1","nouns","Recognise the main masculine, feminine and neuter article forms.","D'Kand liest."),
    ("negation","Negatioun mat net","A1","syntax","Place net correctly to negate ordinary statements.","Ech schaffen net haut."),
    ("questions","Froen","A1","communication","Form yes/no and wh-questions for everyday needs.","Wou wunnt Dir?"),
    ("possessives","Besëtz a Possessivformen","A1","grammar","Use possessive forms for family and personal objects.","Dat ass mäi Buch."),
    ("plural-nouns","Pluralformen","A1","nouns","Recognise common plural patterns in everyday vocabulary.","D'Kanner spillen."),
    ("past-tense","Vergaangenheet","A2","verbs","Use common past forms to describe completed events.","Gëschter hunn ech geschafft."),
    ("future-with-wäerten","Zukunft mat wäerten","A2","verbs","Use wäerten plus infinitive for future statements.","Ech wäert muer kommen."),
    ("modal-verbs","Modalverben","A2","verbs","Use kënnen, mussen, wëllen and similar verbs for ability and obligation.","Ech muss elo goen."),
    ("prepositions","Präpositiounen","A2","grammar","Use frequent prepositions for place, time and movement.","Ech fueren op Esch."),
    ("comparatives","Verglach","A2","adjectives","Build basic comparisons with méi and wéi.","Dëse Bus ass méi séier."),
    ("reflexive-verbs","Reflexivverben","A2","verbs","Use reflexive forms for daily routines and personal actions.","Ech wäsche mech."),
    ("subordinate-clauses","Ënneruerdent Sätz","B1","syntax","Build subordinate clauses with common conjunctions.","Ech bleiwen doheem, well et reent."),
    ("relative-clauses","Relativsätz","B1","syntax","Connect people and things with relative clauses.","D'Fra, déi do schafft, ass meng Nopesch."),
    ("conditional","Konditional","B1","verbs","Express hypothetical situations and polite requests.","Ech géif gär kommen."),
    ("reported-speech","Indirekt Ried","B1","discourse","Report what another person said without quoting directly.","Hie sot, datt hien muer kënnt."),
    ("perfect-and-imperfect","Perfekt an Imperfekt","B1","verbs","Choose common past forms according to narrative function.","Wéi ech ukomm sinn, huet et gereent."),
    ("discourse-connectors","Diskursverknëppungen","B1","discourse","Link ideas with well, awer, dofir, trotzdem and similar connectors.","Ech war midd, awer ech sinn gaangen."),
    ("passive-voice","Passiv","B2","syntax","Describe processes while focusing on the action or result.","D'Bréck gëtt gebaut."),
    ("causal-concessive-clauses","Kausal a konzessiv Sätz","B2","syntax","Express cause, contrast and concession precisely.","Obwuel et reent, gi mir eraus."),
    ("relative-pronoun-control","Relativpronomen am Detail","B2","syntax","Control relative clauses across more complex noun phrases.","D'Dokument, dat ech krut, ass wichteg."),
    ("nominalization","Nominaliséierung","B2","style","Turn actions and qualities into compact formal noun phrases.","D'Ëmsetzung vum Projet ass wichteg."),
    ("formal-register","Formelle Sproochgebrauch","B2","register","Shift from conversational wording to professional Luxembourgish.","Mir bieden Iech, dëse Formulaire auszefëllen."),
    ("academic-hedging","Akademesch Nuancéierung","C1","academic","Qualify claims with cautious, evidence-aware language.","D'Resultater kéinten drop hiweisen."),
    ("embedded-questions","Agebett Froen","C1","syntax","Embed questions inside statements and requests.","Ech weess net, wéini de Cours ufänkt."),
    ("information-structure","Thema a Fokus","C1","discourse","Organise information to foreground contrast and new information.","Besonnesch dëse Punkt ass wichteg."),
    ("complex-subordination","Komplex Ënneruerdnung","C1","syntax","Combine multiple subordinate relationships without losing clarity.","Och wann de Projet komplex ass, kënne mir en ëmsetzen."),
    ("administrative-language","Administrativ Sprooch","C1","professional","Use precise structures common in institutions and public administration.","D'Demande muss bis e Freideg agereecht ginn."),
    ("idiomatic-language","Idiomatesch Ausdréck","C2","lexis","Interpret and produce idiomatic expressions according to context.","Dat ass net mäi Béier."),
    ("register-shifting","Registerwiessel","C2","pragmatics","Adapt wording to informal, professional, institutional and academic settings.","Kënnt Dir dat w.e.g. confirméieren?"),
    ("rhetoric","Rhetorik an Argumentatioun","C2","rhetoric","Structure nuanced arguments, concessions and rebuttals.","Dës Argumentatioun ass zwar plausibel, awer net genuch beleeën."),
    ("literary-style","Literareche Stil","C2","style","Recognise figurative language and controlled stylistic variation.","D'Stad erwächt lues ënnert dem Reen."),
    ("translation-precision","Iwwersetzungspräzisioun","C2","translation","Choose context-sensitive Luxembourgish equivalents rather than literal calques.","D'Formuléierung muss dem Kontext ugepasst ginn."),
]

GRAMMAR_TOPICS = [
    GrammarTopic(slug=s, title=t, level=l, category=c, summary=sm, explanation=ex,
                 examples=[GrammarExample(text=exm)])
    for s,t,l,c,sm,exm in _GRAMMAR
]

_VOCAB = {
"A1":[("Greetings","Moien","phrase","hello","Moien, wéi geet et?"),("Identity","Numm","noun","name","Mäi Numm ass Lea."),("Family","Famill","noun","family","Meng Famill wunnt hei."),("Home","Haus","noun","house","Ech sinn doheem."),("Routine","Aarbecht","noun","work","Ech ginn op d'Aarbecht."),("Time","Auer","noun","clock/time","Et ass dräi Auer."),("Food","Brout","noun","bread","Ech kafen Brout."),("Places","Gare","noun","station","D'Gare ass no.")],
"A2":[("Transport","Bus","noun","bus","Ech fuere mam Bus."),("Health","Dokter","noun","doctor","Ech ginn bei den Dokter."),("Shopping","Präis","noun","price","De Präis ass gutt."),("Weather","Wieder","noun","weather","D'Wieder ass schéin.")],
"B1":[("Work","Erfahrung","noun","experience","Ech hunn vill Erfahrung."),("Education","Cours","noun","course","De Cours fänkt um néng un."),("Society","Noperschaft","noun","neighbourhood","D'Noperschaft ass roueg."),("Communication","Meenung","noun","opinion","Ech soen meng Meenung.")],
"B2":[("Professional","Donnéeën","noun","data","D'Donnéeë musse geschützt ginn."),("Institutions","Demande","noun","application/request","D'Demande ass agereecht."),("Media","Noriicht","noun","news item","Ech hunn d'Noriicht gelies."),("Environment","Ëmwelt","noun","environment","Mir mussen d'Ëmwelt schützen.")],
"C1":[("Academic","Beweiser","noun","evidence","D'Beweiser sinn relevant."),("Analysis","Entwécklung","noun","development","D'Entwécklung ass bedeitend."),("Administration","Viraussetzung","noun","requirement","Dat ass eng wichteg Viraussetzung."),("Argumentation","Konsequenz","noun","consequence","Dës Konsequenz muss berücksichtegt ginn.")],
"C2":[("Rhetoric","Nuance","noun","nuance","Dës Nuance ass entscheedend."),("Pragmatics","Ëmstänn","noun","circumstances","D'Ëmstänn musse berécksiichtegt ginn."),("Literature","Metapher","noun","metaphor","D'Metapher ass bewosst gewielt."),("Translation","Bedeitung","noun","meaning","D'Bedeitung hänkt vum Kontext of.")],
}

VOCABULARY_SETS=[]
for level, rows in _VOCAB.items():
    for i,(topic,word,pos,definition,example) in enumerate(rows,1):
        uid=f"lb-{level.lower()}-{i}"
        unit=f"lb-{level.lower()}-unit-{i}"
        VOCABULARY_SETS.append(VocabularySet(
            id=uid, level=level, topic=topic, unit_ref=unit,
            words=[VocabularyEntry(word=word,pos=pos,definition=definition,example=example)]
        ))

_UNITS = {
"A1":[("Introductions","identity-pronouns","Greetings"),("People and family","basic-word-order","Family"),("Home and routine","present-tense","Home"),("Time and schedules","negation","Daily life"),("Food and shopping","questions","Shopping"),("Town and directions","possessives","Places"),("Transport and services","plural-nouns","Transport"),("Everyday review","location-direction","Everyday communication")],
"A2":[("Past experiences","past-tense","Experiences"),("Plans and future","future-with-wäerten","Plans"),("Ability and obligation","modal-verbs","Work and services"),("Movement and place","prepositions","Travel"),("Comparing choices","comparatives","Shopping and choices"),("Daily routines","reflexive-verbs","Health and routine")],
"B1":[("Reasons and explanations","subordinate-clauses","Reasons"),("People and things","relative-clauses","Descriptions"),("Hypotheses","conditional","Plans and problems"),("Reporting information","reported-speech","Communication"),("Narrating events","perfect-and-imperfect","Stories"),("Connecting arguments","discourse-connectors","Opinions")],
"B2":[("Processes","passive-voice","Work"),("Contrast and concession","causal-concessive-clauses","Debate"),("Complex descriptions","relative-pronoun-control","Documents"),("Formal processes","nominalization","Administration"),("Professional communication","formal-register","Workplace"),("Integrated review","academic-hedging","Professional reasoning")],
"C1":[("Evidence and claims","academic-hedging","Academic discussion"),("Embedded communication","embedded-questions","Meetings and interviews"),("Focus and emphasis","information-structure","Presentations"),("Complex arguments","complex-subordination","Analysis"),("Public administration","administrative-language","Institutions"),("Advanced production","formal-register","Professional writing")],
"C2":[("Idioms and nuance","idiomatic-language","Everyday nuance"),("Register control","register-shifting","Professional and social contexts"),("Rhetorical argument","rhetoric","Debate"),("Literary interpretation","literary-style","Literature"),("Translation choices","translation-precision","Translation"),("Mastery and synthesis","information-structure","Integrated communication")],
}

CURRICULUM={}
for level, rows in _UNITS.items():
    units=[]
    for i,(title,grammar,topic) in enumerate(rows,1):
        units.append(CurriculumUnit(
            id=f"lb-{level.lower()}-unit-{i}", level=level, unit_number=i,
            title=f"Luxembourgish {level} · {title}",
            grammar_points=[grammar],
            vocabulary_set_ids=[f"lb-{level.lower()}-{min(i, len(_VOCAB[level]))}"],
            lesson_types=["grammar","vocabulary","reading","writing","listening","review"],
            competency_checklist=[f"Understand and use Luxembourgish for {topic.lower()}",f"Produce accurate {level} communication in guided tasks"],
            default_weeks=2
        ))
    CURRICULUM[level]=units

_PHRASES={
"A1":[("Greetings","👋",[("Moien, wéi geet et?","greeting","neutral"),("Ech heeschen ...","introducing yourself","neutral")]),("Shopping","🛒",[("Wéi vill kascht dat?","asking the price","neutral"),("Ech hätt gär dëst.","requesting an item","neutral")])],
"A2":[("Travel","🧳",[("Wou ass d'Gare?","asking directions","neutral"),("Ech brauch en Ticket op Lëtzebuerg.","buying a ticket","neutral")]),("Health","🩺",[("Ech fille mech net gutt.","describing how you feel","neutral"),("Ech hätt gär e Rendez-vous.","requesting an appointment","formal")])],
"B1":[("Opinions","💭",[("Menger Meenung no ...","giving an opinion","neutral"),("Ech sinn domat averstanen.","agreeing","neutral")]),("Work","💼",[("Kënne mir dat zesumme kucken?","collaborating","neutral"),("Ech schécken Iech d'Dokument nach haut.","professional follow-up","formal")])],
"B2":[("Meetings","📅",[("Kënne mir dëse Punkt méi genee diskutéieren?","formal discussion","formal"),("Ech proposéieren, datt mir ...","making a proposal","formal")]),("Administration","🏛️",[("D'Demande ass nach am Traitement.","describing an administrative process","formal"),("Kënnt Dir dat schrëftlech confirméieren?","requesting confirmation","formal")])],
"C1":[("Academic","🎓",[("D'Resultater weisen drop hin, datt ...","qualifying an academic claim","formal"),("Et ass wichteg, dës Donnéeën am Kontext ze interpretéieren.","academic discussion","formal")]),("Presentation","📊",[("Loosst mech dëse Punkt ervirhiewen.","highlighting a point","formal"),("Zum Schluss kann ee festhalen, datt ...","concluding","formal")])],
"C2":[("Debate","⚖️",[("Dës Interpretatioun ass zwar méiglech, awer ...","qualified rebuttal","formal"),("Dat hänkt wesentlech vum Kontext of.","nuanced qualification","formal")]),("Literary discussion","📚",[("Dës Formuléierung huet eng duebel Bedeitung.","interpreting ambiguity","formal"),("De Passage léisst sech op verschidde Manéiere liesen.","literary interpretation","formal")])],
}
PHRASEBOOK_CATEGORIES=[]
for level, cats in _PHRASES.items():
    for i,(situation,icon,phrases) in enumerate(cats,1):
        PHRASEBOOK_CATEGORIES.append(PhrasebookCategory(
            id=f"lb-{level.lower()}-phrases-{i}", level=level, situation=situation, icon=icon,
            phrases=[PhrasebookEntry(text=t,context=c,register=r,unit_ref=f"lb-{level.lower()}-unit-{i}") for t,c,r in phrases]
        ))

ASSESSMENT_BANK=[
    AssessmentQuestion(id="lb-a1-001",skill="grammar",difficulty="A1",question="Which sentence introduces the speaker?",options=["Ech sinn Anna.","Hie sinn Anna.","Ech ass Anna.","Anna sinn ech."],correct="Ech sinn Anna.",grammar_slug="identity-pronouns"),
    AssessmentQuestion(id="lb-a1-002",skill="grammar",difficulty="A1",question="Which sentence is correctly negated?",options=["Ech schaffen net haut.","Ech net schaffen haut.","Ech schaffen haut net?","Net ech schaffen haut."],correct="Ech schaffen net haut.",grammar_slug="negation"),
    AssessmentQuestion(id="lb-a2-001",skill="grammar",difficulty="A2",question="Which sentence refers to tomorrow?",options=["Ech wäert muer kommen.","Ech sinn gëschter komm.","Ech komme gëschter.","Ech koum muer."],correct="Ech wäert muer kommen.",grammar_slug="future-with-wäerten"),
    AssessmentQuestion(id="lb-a2-002",skill="vocabulary",difficulty="A2",question="Which word means doctor?",options=["Dokter","Gare","Präis","Wieder"],correct="Dokter"),
    AssessmentQuestion(id="lb-b1-001",skill="grammar",difficulty="B1",question="Which sentence gives a reason?",options=["Ech bleiwen doheem, well et reent.","Ech bleiwen doheem, awer et reent.","Ech bleiwen doheem, wann et reent.","Ech bleiwen doheem, oder et reent."],correct="Ech bleiwen doheem, well et reent.",grammar_slug="subordinate-clauses"),
    AssessmentQuestion(id="lb-b1-002",skill="grammar",difficulty="B1",question="Which form expresses a hypothetical wish?",options=["Ech géif gär kommen.","Ech kommen all Dag.","Ech sinn komm.","Ech wäert kommen."],correct="Ech géif gär kommen.",grammar_slug="conditional"),
    AssessmentQuestion(id="lb-b2-001",skill="grammar",difficulty="B2",question="Which sentence uses the passive?",options=["D'Bréck gëtt gebaut.","Si bauen d'Bréck.","Si hunn d'Bréck gebaut.","D'Bréck ass grouss."],correct="D'Bréck gëtt gebaut.",grammar_slug="passive-voice"),
    AssessmentQuestion(id="lb-b2-002",skill="communication",difficulty="B2",question="Which phrase is appropriate in a formal request?",options=["Kënnt Dir dat schrëftlech confirméieren?","Gëff mir dat.","Hey, schéck et.","Maach séier."],correct="Kënnt Dir dat schrëftlech confirméieren.",grammar_slug="formal-register"),
    AssessmentQuestion(id="lb-c1-001",skill="grammar",difficulty="C1",question="Which sentence contains an embedded question?",options=["Ech weess net, wéini de Cours ufänkt.","Wéini fänkt de Cours un?","De Cours fänkt un.","Ech wëll de Cours."],correct="Ech weess net, wéini de Cours ufänkt.",grammar_slug="embedded-questions"),
    AssessmentQuestion(id="lb-c1-002",skill="reading",difficulty="C1",question="Which expression appropriately qualifies an academic claim?",options=["D'Resultater kéinten drop hiweisen.","D'Resultater sinn ëmmer richteg.","D'Resultater beweisen alles.","D'Resultater si sécher fir jiddereen."],correct="D'Resultater kéinten drop hiweisen.",grammar_slug="academic-hedging"),
    AssessmentQuestion(id="lb-c2-001",skill="grammar",difficulty="C2",question="Which sentence signals a qualified rebuttal?",options=["Dës Interpretatioun ass zwar méiglech, awer ...","Dëst ass einfach falsch.","Ech weess näischt.","Dat ass egal."],correct="Dës Interpretatioun ass zwar méiglech, awer ...",grammar_slug="rhetoric"),
    AssessmentQuestion(id="lb-c2-002",skill="reading",difficulty="C2",question="Which skill is central to advanced translation precision?",options=["Choosing context-sensitive equivalents","Translating every word literally","Avoiding context","Using one synonym everywhere"],correct="Choosing context-sensitive equivalents",grammar_slug="translation-precision"),
]
