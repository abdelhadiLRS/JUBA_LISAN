"""Swedish foundation data for JUBA LISAN.

Language-specific Swedish structures, native examples, vocabulary, phrasebook,
curriculum sequencing and assessments for A1-C2.
"""
from app.data._types import (
    AssessmentQuestion, CurriculumUnit, GrammarExample, GrammarTopic,
    PhrasebookCategory, PhrasebookEntry, VocabularyEntry, VocabularySet,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def _g(slug, title, level, summary, examples):
    return GrammarTopic(
        slug=slug, title=title, level=level, category="grammar",
        summary=summary, explanation=summary,
        examples=[GrammarExample(text=e) for e in examples],
    )


GRAMMAR_TOPICS = [
    _g("sv-a1-g1","Personal pronouns","A1","Use Swedish subject pronouns.","Jag heter Anna.","Vi studerar svenska."] if False else _g("sv-a1-g1","Personal pronouns","A1","Use Swedish subject pronouns.",["Jag heter Anna.","Vi studerar svenska."]),
    _g("sv-a1-g2","Basic word order","A1","Build simple main clauses with subject and finite verb.",["Jag bor i Stockholm.","Hon arbetar idag."]),
    _g("sv-a1-g3","Present tense","A1","Describe habits and current facts.",["Jag arbetar idag.","Du talar svenska."]),
    _g("sv-a1-g4","Definite nouns","A1","Use indefinite and definite noun forms.",["en bok / boken","ett hus / huset"]),
    _g("sv-a1-g5","Questions","A1","Ask yes-no and information questions.",["Bor du här?","Var bor du?"]),
    _g("sv-a1-g6","Negation with inte","A1","Negate basic clauses.",["Jag förstår inte.","Hon arbetar inte idag."]),
    _g("sv-a1-g7","Adjective agreement","A1","Agree adjectives with en/ett nouns and plurals.",["en stor bil","ett stort hus"]),
    _g("sv-a1-g8","Modal verbs","A1","Express ability, desire and necessity with modal verbs.",["Jag kan simma.","Jag vill lära mig svenska."]),
    _g("sv-a2-g1","Past tense","A2","Talk about completed events with preterite.",["Jag bodde där förra året.","Hon kom igår."]),
    _g("sv-a2-g2","Perfect tense","A2","Connect past events to the present with har + supine.",["Jag har läst boken.","Vi har redan ätit."]),
    _g("sv-a2-g3","Future and intention","A2","Express plans with ska and future expressions.",["Jag ska resa imorgon.","Vi ska studera senare."]),
    _g("sv-a2-g4","Reflexive pronouns","A2","Use reflexive forms for actions directed at the subject.",["Jag tvättar mig.","Hon sätter sig."]),
    _g("sv-a2-g5","Possessives","A2","Express ownership with possessive pronouns.",["min bok","vårt hus"]),
    _g("sv-a2-g6","Comparatives","A2","Compare qualities using -are, -ast and mer.",["Den här är större.","Hon är mer erfaren."]),
    _g("sv-a2-g7","Prepositions of place and time","A2","Use common Swedish prepositions accurately.",["på bordet","i Sverige","på måndag"]),
    _g("sv-a2-g8","Imperatives and polite requests","A2","Give instructions and make requests.",["Kom hit!","Kan du hjälpa mig?"]),
    _g("sv-b1-g1","Subordinate clauses","B1","Build clauses with att, eftersom, när and other subordinators.",["Jag stannar eftersom det regnar.","Hon vet att han kommer."]),
    _g("sv-b1-g2","V2 word order","B1","Maintain verb-second order after fronting.",["Idag arbetar jag hemma.","På kvällen läser hon."]),
    _g("sv-b1-g3","Adverb placement","B1","Place inte and sentence adverbs correctly.",["Jag har inte sett honom.","Hon kommer kanske senare."]),
    _g("sv-b1-g4","Relative clauses","B1","Modify nouns with som and related relative structures.",["Boken som jag läser är ny.","Mannen som bor här arbetar hemma."]),
    _g("sv-b1-g5","Passive voice","B1","Form passive constructions with -s and bli.",["Dörren öppnas klockan åtta.","Huset blev byggt 1990."]),
    _g("sv-b1-g6","Participles and adjectives","B1","Use participial forms to describe states and processes.",["en stängd dörr","ett växande problem"]),
    _g("sv-b1-g7","Conditional and hypothetical clauses","B1","Express conditions with om and skulle.",["Om jag hade tid skulle jag resa.","Om det regnar stannar vi hemma."]),
    _g("sv-b1-g8","Reported speech","B1","Report statements and questions in Swedish.",["Hon sa att hon var trött.","Han frågade om jag kunde komma."]),
    _g("sv-b2-g1","Advanced subordinate clauses","B2","Combine several subordinate relations in coherent prose.",["Även om det är svårt fortsätter vi eftersom målet är viktigt."]),
    _g("sv-b2-g2","Concession and contrast","B2","Express concession with trots att, även om and ändå.",["Trots att det regnade gick vi ut.","Det är svårt, men ändå möjligt."]),
    _g("sv-b2-g3","Cohesion and reference","B2","Maintain reference with pronouns, demonstratives and lexical repetition.",["Detta problem kräver en lösning.","Frågan diskuterades tidigare."]),
    _g("sv-b2-g4","Discourse connectors","B2","Organize arguments with därför, däremot, dessutom and följaktligen.",["Därför behöver vi agera.","Däremot finns en annan möjlighet."]),
    _g("sv-b2-g5","Information structure and focus","B2","Use fronting and cleft-like structures to manage focus.",["Det är den här frågan vi måste lösa.","Idag är det Anna som leder mötet."]),
    _g("sv-b2-g6","Nominalization","B2","Use abstract nouns for formal written discourse.",["Genomförandet av planen kräver resurser.","Utvecklingen har gått snabbt."]),
    _g("sv-b2-g7","Modality and stance","B2","Express probability, obligation, evaluation and epistemic stance.",["Det kan vara möjligt.","Det bör undersökas vidare."]),
    _g("sv-b2-g8","Register and politeness","B2","Adapt Swedish to informal, neutral and professional contexts.",["Skulle du kunna skicka dokumentet?","Kan du skicka filen?"]),
    _g("sv-c1-g1","Formal institutional Swedish","C1","Produce precise administrative and institutional prose.",["Ansökan ska lämnas in senast den 15 juni."]),
    _g("sv-c1-g2","Academic argumentation","C1","Present claims, evidence, limitations and conclusions.",["Resultaten tyder på att metoden kan förbättras."]),
    _g("sv-c1-g3","Academic hedging","C1","Qualify claims with epistemic precision.",["Det förefaller som om resultaten delvis stöder hypotesen."]),
    _g("sv-c1-g4","Embedded questions","C1","Integrate questions into complex sentences.",["Det är oklart om resultaten kan generaliseras."]),
    _g("sv-c1-g5","Information packaging","C1","Control topic, focus and given/new information in long texts.",["Det centrala problemet är hur resurserna ska fördelas."]),
    _g("sv-c1-g6","Media and public discourse","C1","Interpret and produce concise public-facing Swedish.",["Rapporten publicerades efter en omfattande granskning."]),
    _g("sv-c1-g7","Idiomatic and pragmatic meaning","C1","Interpret idioms, implication and context-sensitive wording.",["Det är ingen ko på isen.","Vi behöver ta frågan på allvar."]),
    _g("sv-c1-g8","Professional correspondence","C1","Write precise emails, requests and institutional responses.",["Vi ber er återkomma med de efterfrågade handlingarna."]),
    _g("sv-c2-g1","Advanced cohesion","C2","Control long-range cohesion and rhetorical progression.",["Även om rapporten visar framsteg kvarstår flera strukturella problem som kräver långsiktiga åtgärder."]),
    _g("sv-c2-g2","Nuanced modality","C2","Express subtle degrees of certainty and evaluation.",["Det skulle knappast vara rimligt att dra en sådan slutsats på nuvarande underlag."]),
    _g("sv-c2-g3","Dense nominalization","C2","Compress complex propositions into formal noun phrases.",["Analysen av resultatens tillförlitlighet förutsätter en noggrann bedömning av urvalet."]),
    _g("sv-c2-g4","Rhetorical organization","C2","Manage concession, counterargument and emphasis.",["Även om invändningen är relevant bör den vägas mot de empiriska resultaten."]),
    _g("sv-c2-g5","Legal and administrative formulation","C2","Interpret obligations, conditions and procedural language.",["Sökanden ska inkomma med fullständiga handlingar enligt gällande bestämmelser."]),
    _g("sv-c2-g6","Translation precision","C2","Preserve meaning, register and pragmatic force across languages.",["Översättningen måste bevara både betydelse och stilnivå."]),
    _g("sv-c2-g7","Literary and rhetorical style","C2","Interpret figurative language and deliberate stylistic choices.",["Författaren låter bilden av havet bära berättelsens centrala symbolik."]),
    _g("sv-c2-g8","Discourse analysis and register shifting","C2","Shift deliberately among conversational, professional and academic registers.",["Samma innehåll måste omformuleras beroende på mottagare och kommunikativ situation."]),
]


def _v(id_, level, topic, unit_ref, entries):
    return VocabularySet(
        id=id_, level=level, topic=topic, unit_ref=unit_ref,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w,p,d,e in entries],
    )


VOCABULARY_SETS = [
    _v("greetings_a1","A1","greetings","sv-a1-unit-1",[("hej","phrase","hello","Hej!"),("tack","phrase","thank you","Tack så mycket."),("hej då","phrase","goodbye","Hej då!")]),
    _v("identity_a1","A1","identity","sv-a1-unit-2",[("namn","noun","name","Vad heter du?"),("student","noun","student","Jag är student."),("lärare","noun","teacher","Hon är lärare.")]),
    _v("family_a1","A1","family","sv-a1-unit-3",[("mamma","noun","mother","Min mamma bor här."),("pappa","noun","father","Min pappa arbetar."),("syster","noun","sister","Jag har en syster.")]),
    _v("home_a1","A1","home","sv-a1-unit-4",[("hem","noun","home","Jag är hemma."),("rum","noun","room","Mitt rum är litet."),("dörr","noun","door","Dörren är öppen.")]),
    _v("routine_a1","A1","routine","sv-a1-unit-5",[("äta","verb","eat","Jag äter frukost."),("dricka","verb","drink","Jag dricker vatten."),("sova","verb","sleep","Jag ska sova.")]),
    _v("food_a1","A1","food","sv-a1-unit-6",[("bröd","noun","bread","Jag köper bröd."),("kaffe","noun","coffee","Jag dricker kaffe."),("vatten","noun","water","Jag dricker vatten.")]),
    _v("places_a1","A1","places","sv-a1-unit-7",[("butik","noun","shop","Butiken ligger här."),("station","noun","station","Var ligger stationen?"),("vänster","adverb","left","Sväng till vänster.")]),
    _v("communication_a1","A1","communication","sv-a1-unit-8",[("förstå","verb","understand","Jag förstår."),("fråga","verb","ask","Jag vill fråga något."),("hjälp","noun","help","Kan du hjälpa mig?")]),
    _v("travel_a2","A2","travel","sv-a2-unit-1",[("resa","verb","travel","Jag ska resa imorgon."),("biljett","noun","ticket","Jag behöver en biljett."),("tåg","noun","train","Tåget kommer snart.")]),
    _v("health_a2","A2","health","sv-a2-unit-2",[("sjuk","adjective","ill","Jag är sjuk idag."),("läkare","noun","doctor","Jag behöver en läkare."),("smärta","noun","pain","Jag har smärta i ryggen.")]),
    _v("work_a2","A2","work","sv-a2-unit-3",[("arbete","noun","work","Jag har mycket arbete."),("möte","noun","meeting","Mötet börjar klockan nio."),("kollega","noun","colleague","Min kollega kommer senare.")]),
    _v("study_a2","A2","study","sv-a2-unit-4",[("studera","verb","study","Jag studerar svenska."),("kurs","noun","course","Kursen börjar idag."),("prov","noun","test","Vi har ett prov imorgon.")]),
    _v("society_b1","B1","society","sv-b1-unit-1",[("samhälle","noun","society","Samhället förändras."),("medborgare","noun","citizen","Medborgarna har rättigheter."),("jämlikhet","noun","equality","Jämlikhet är ett viktigt mål.")]),
    _v("education_b1","B1","education","sv-b1-unit-2",[("utbildning","noun","education","Utbildning påverkar arbetslivet."),("forskning","noun","research","Forskningen fortsätter."),("kunskap","noun","knowledge","Kunskap är viktig.")]),
    _v("environment_b1","B1","environment","sv-b1-unit-3",[("miljö","noun","environment","Vi måste skydda miljön."),("klimat","noun","climate","Klimatet förändras."),("hållbarhet","noun","sustainability","Hållbarhet kräver långsiktiga lösningar.")]),
    _v("communication_b1","B1","communication","sv-b1-unit-4",[("budskap","noun","message","Budskapet är tydligt."),("samtal","noun","conversation","Samtalet fortsätter."),("förklara","verb","explain","Kan du förklara detta?")]),
    _v("economy_b2","B2","economy","sv-b2-unit-1",[("ekonomi","noun","economy","Ekonomin påverkas av flera faktorer."),("investering","noun","investment","Investeringen kräver planering."),("marknad","noun","market","Marknaden förändras snabbt.")]),
    _v("governance_b2","B2","governance","sv-b2-unit-2",[("myndighet","noun","authority","Myndigheten publicerade rapporten."),("lagstiftning","noun","legislation","Ny lagstiftning diskuteras."),("beslut","noun","decision","Beslutet fattades igår.")]),
    _v("media_b2","B2","media","sv-b2-unit-3",[("nyhet","noun","news item","Nyheten spreds snabbt."),("rapport","noun","report","Rapporten publicerades idag."),("debatt","noun","debate","Debatten fortsätter.")]),
    _v("technology_b2","B2","technology","sv-b2-unit-4",[("teknik","noun","technology","Ny teknik förändrar arbetet."),("data","noun","data","Data måste skyddas."),("säkerhet","noun","security","Säkerhet är avgörande.")]),
    _v("academic_c1","C1","academic language","sv-c1-unit-1",[("hypotes","noun","hypothesis","Hypotesen prövas i studien."),("resultat","noun","result","Resultaten stöder delvis hypotesen."),("metod","noun","method","Metoden beskrivs tydligt.")]),
    _v("professional_c1","C1","professional language","sv-c1-unit-2",[("handling","noun","document","Skicka in handlingarna."),("ansökan","noun","application","Ansökan behandlas snart."),("ärende","noun","case/matter","Ärendet är under behandling.")]),
    _v("abstract_c1","C1","abstract concepts","sv-c1-unit-3",[("konsekvens","noun","consequence","Beslutet får flera konsekvenser."),("förutsättning","noun","condition","Det är en viktig förutsättning."),("bedömning","noun","assessment","En ny bedömning behövs.")]),
    _v("rhetoric_c2","C2","rhetoric and discourse","sv-c2-unit-1",[("invändning","noun","objection","Invändningen är relevant."),("slutsats","noun","conclusion","Slutsatsen måste stödjas av data."),("perspektiv","noun","perspective","Frågan kan ses ur flera perspektiv.")]),
]


def _unit(level, n, title, grammar, vocab, checks):
    return CurriculumUnit(
        id=f"sv-{level.lower()}-unit-{n}", level=level, unit_number=n,
        title=title, grammar_points=grammar, vocabulary_set_ids=vocab,
        lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
        competency_checklist=checks, default_weeks=1 if level in ("A1","A2") else 2,
    )


_CURRICULUM = {
"A1":[("Hälsningar och identitet",["sv-a1-g1","sv-a1-g2"],["greetings_a1","identity_a1"],["Greet people","Introduce yourself"]),
("Familj",["sv-a1-g4","sv-a1-g7"],["family_a1"],["Talk about family","Describe people"]),
("Hem och saker",["sv-a1-g4","sv-a1-g7"],["home_a1"],["Describe your home","Locate objects"]),
("Vardag",["sv-a1-g3","sv-a1-g6"],["routine_a1"],["Describe routines","Negate simple actions"]),
("Mat",["sv-a1-g5","sv-a1-g8"],["food_a1"],["Order food","Ask simple questions"]),
("Platser",["sv-a1-g5","sv-a1-g7"],["places_a1"],["Ask directions","Describe locations"]),
("Kommunikation",["sv-a1-g6","sv-a1-g8"],["communication_a1"],["Ask for help","Clarify meaning"]),
("A1-repetition",["sv-a1-g2","sv-a1-g3","sv-a1-g5"],["greetings_a1","routine_a1","communication_a1"],["Hold a short everyday exchange","Combine A1 structures"])],
"A2":[("Resor",["sv-a2-g1","sv-a2-g3"],["travel_a2"],["Talk about past and future travel"]),
("Hälsa",["sv-a2-g1","sv-a2-g8"],["health_a2"],["Describe health needs"]),
("Arbete",["sv-a2-g2","sv-a2-g5"],["work_a2"],["Talk about work"]),
("Studier",["sv-a2-g2","sv-a2-g7"],["study_a2"],["Talk about courses and tests"]),
("Possession och vardag",["sv-a2-g5","sv-a2-g4"],["home_a1"],["Express ownership","Describe daily activities"]),
("Jämförelser",["sv-a2-g6","sv-a2-g7"],["people_a2"],["Compare people and things"]),
("Begäran",["sv-a2-g8","sv-a2-g5"],["communication_a1"],["Make polite requests"]),
("A2-repetition",["sv-a2-g1","sv-a2-g2","sv-a2-g3"],["travel_a2","work_a2","study_a2"],["Sustain an extended everyday exchange"])],
"B1":[("Samhälle",["sv-b1-g1","sv-b1-g4"],["society_b1"],["Discuss social topics"]),
("Utbildning",["sv-b1-g2","sv-b1-g3"],["education_b1"],["Explain academic topics"]),
("Miljö",["sv-b1-g1","sv-b1-g7"],["environment_b1"],["Explain causes and conditions"]),
("Kommunikation",["sv-b1-g4","sv-b1-g8"],["communication_b1"],["Report information"]),
("Passiv och process",["sv-b1-g5","sv-b1-g6"],["work_a2"],["Describe processes"]),
("Villkor",["sv-b1-g7","sv-b1-g1"],["society_b1"],["Discuss hypothetical situations"]),
("Referat",["sv-b1-g8","sv-b1-g3"],["media_b2"],["Report statements and questions"]),
("B1-repetition",["sv-b1-g1","sv-b1-g2","sv-b1-g4"],["education_b1","communication_b1"],["Build connected multi-clause discourse"])],
"B2":[("Ekonomi",["sv-b2-g1","sv-b2-g7"],["economy_b2"],["Explain economic relationships"]),
("Förvaltning",["sv-b2-g4","sv-b2-g8"],["governance_b2"],["Discuss institutional processes"]),
("Medier",["sv-b2-g4","sv-b2-g5"],["media_b2"],["Summarize and evaluate media discourse"]),
("Teknik",["sv-b2-g6","sv-b2-g7"],["technology_b2"],["Discuss technical change"]),
("Nominalisering",["sv-b2-g6","sv-b2-g3"],["academic_c1"],["Write more formal prose"]),
("Modalitet",["sv-b2-g7","sv-b2-g2"],["governance_b2"],["Express nuanced stance"]),
("Register",["sv-b2-g8","sv-b2-g4"],["professional_c1"],["Adapt language to context"]),
("B2-repetition",["sv-b2-g1","sv-b2-g2","sv-b2-g5"],["media_b2","communication_b1"],["Build a coherent extended argument"])],
"C1":[("Institutionellt språk",["sv-c1-g1","sv-c1-g8"],["professional_c1"],["Write formal institutional prose"]),
("Akademisk argumentation",["sv-c1-g2","sv-c1-g3"],["academic_c1"],["Present claims and evidence"]),
("Hedging",["sv-c1-g3","sv-c1-g7"],["abstract_c1"],["Qualify academic claims"]),
("Inbäddade frågor",["sv-c1-g4","sv-c1-g5"],["communication_b1"],["Integrate questions into complex prose"]),
("Informationsstruktur",["sv-c1-g5","sv-c1-g2"],["academic_c1"],["Manage information flow"]),
("Mediespråk",["sv-c1-g6","sv-c1-g7"],["media_b2"],["Produce precise public language"]),
("Pragmatik",["sv-c1-g7","sv-c1-g8"],["professional_c1"],["Interpret implied meaning"]),
("Professionell korrespondens",["sv-c1-g8","sv-c1-g1"],["professional_c1"],["Draft precise formal requests"])],
"C2":[("Avancerad kohesion",["sv-c2-g1","sv-c2-g2"],["rhetoric_c2"],["Control long-range cohesion"]),
("Nyansierad modalitet",["sv-c2-g2","sv-c2-g4"],["abstract_c1"],["Express subtle stance"]),
("Tät nominalisering",["sv-c2-g3","sv-c2-g5"],["academic_c1"],["Handle dense formal prose"]),
("Retorisk organisation",["sv-c2-g4","sv-c2-g1"],["rhetoric_c2"],["Build and rebut arguments"]),
("Juridiskt språk",["sv-c2-g5","sv-c2-g6"],["professional_c1"],["Interpret procedural wording"]),
("Översättningsprecision",["sv-c2-g6","sv-c2-g2"],["rhetoric_c2"],["Preserve register and pragmatic force"]),
("Litterär stil",["sv-c2-g7","sv-c2-g1"],["rhetoric_c2"],["Interpret figurative language"]),
("Diskursanalys",["sv-c2-g8","sv-c2-g4"],["rhetoric_c2"],["Shift deliberately among registers"])]
}


CURRICULUM = {
    level: [_unit(level, i+1, title, grammar, vocab, checks) for i,(title,grammar,vocab,checks) in enumerate(items)]
    for level,items in _CURRICULUM.items()
}


PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="sv-greetings-a1",level="A1",situation="greetings",icon="👋",phrases=[PhrasebookEntry(text="Hej!",context="Hello!",register="neutral"),PhrasebookEntry(text="Hur mår du?",context="How are you?",register="neutral"),PhrasebookEntry(text="Trevligt att träffas.",context="Nice to meet you.",register="neutral")]),
    PhrasebookCategory(id="sv-thanks-a1",level="A1",situation="thanks",icon="🙏",phrases=[PhrasebookEntry(text="Tack så mycket.",context="Thank you very much.",register="neutral"),PhrasebookEntry(text="Varsågod.",context="You're welcome.",register="neutral")]),
    PhrasebookCategory(id="sv-shopping-a1",level="A1",situation="shopping",icon="🛒",phrases=[PhrasebookEntry(text="Vad kostar det?",context="How much does it cost?",register="neutral"),PhrasebookEntry(text="Jag vill köpa den här.",context="I want to buy this.",register="neutral")]),
    PhrasebookCategory(id="sv-directions-a1",level="A1",situation="directions",icon="🧭",phrases=[PhrasebookEntry(text="Var ligger stationen?",context="Where is the station?",register="neutral"),PhrasebookEntry(text="Gå rakt fram.",context="Go straight ahead.",register="neutral")]),
    PhrasebookCategory(id="sv-help-a1",level="A1",situation="help",icon="🆘",phrases=[PhrasebookEntry(text="Kan du hjälpa mig?",context="Can you help me?",register="polite"),PhrasebookEntry(text="Jag förstår inte.",context="I don't understand.",register="neutral")]),
    PhrasebookCategory(id="sv-travel-a2",level="A2",situation="travel",icon="🚆",phrases=[PhrasebookEntry(text="Var köper jag en biljett?",context="Where do I buy a ticket?",register="neutral"),PhrasebookEntry(text="När går tåget?",context="When does the train leave?",register="neutral")]),
    PhrasebookCategory(id="sv-health-a2",level="A2",situation="health",icon="🩺",phrases=[PhrasebookEntry(text="Jag mår inte bra.",context="I don't feel well.",register="neutral"),PhrasebookEntry(text="Jag behöver en läkare.",context="I need a doctor.",register="neutral")]),
    PhrasebookCategory(id="sv-work-b1",level="B1",situation="work",icon="💼",phrases=[PhrasebookEntry(text="När börjar mötet?",context="When does the meeting start?",register="neutral"),PhrasebookEntry(text="Kan du skicka dokumentet?",context="Can you send the document?",register="polite")]),
    PhrasebookCategory(id="sv-study-b1",level="B1",situation="study",icon="📚",phrases=[PhrasebookEntry(text="Jag studerar svenska.",context="I study Swedish.",register="neutral"),PhrasebookEntry(text="Vad betyder det här?",context="What does this mean?",register="neutral")]),
    PhrasebookCategory(id="sv-professional-b2",level="B2",situation="professional",icon="🏢",phrases=[PhrasebookEntry(text="Skulle du kunna återkomma?",context="Could you get back to me?",register="formal"),PhrasebookEntry(text="Därför behöver vi mer tid.",context="Therefore we need more time.",register="formal")]),
    PhrasebookCategory(id="sv-academic-c1",level="C1",situation="academic",icon="🎓",phrases=[PhrasebookEntry(text="Resultaten tyder på att...",context="The results suggest that...",register="formal"),PhrasebookEntry(text="Det förefaller som om...",context="It appears that...",register="formal")]),
    PhrasebookCategory(id="sv-formal-c1",level="C1",situation="formal correspondence",icon="✉️",phrases=[PhrasebookEntry(text="Vi ber er återkomma med...",context="We ask you to respond with...",register="formal"),PhrasebookEntry(text="Tack för ert samarbete.",context="Thank you for your cooperation.",register="formal")]),
    PhrasebookCategory(id="sv-debate-c2",level="C2",situation="discussion and debate",icon="🗣️",phrases=[PhrasebookEntry(text="Även om detta är relevant bör vi också beakta...",context="Although this is relevant, we should also consider...",register="formal"),PhrasebookEntry(text="Å andra sidan...",context="On the other hand...",register="formal")]),
]


ASSESSMENT_BANK = [
    AssessmentQuestion(id="sv-a1-001",skill="vocabulary",difficulty="A1",question="What does 'Tack' mean?",options=["hello","thanks","please","goodbye"],correct="thanks"),
    AssessmentQuestion(id="sv-a1-002",skill="grammar",difficulty="A1",question="Choose the correct sentence.",options=["Jag är student.","Jag student är.","Är jag student är.","Student jag är."],correct="Jag är student."),
    AssessmentQuestion(id="sv-a1-003",skill="grammar",difficulty="A1",question="Choose the correct negative sentence.",options=["Jag inte förstår.","Jag förstår inte.","Inte jag förstår.","Jag förstår är inte."],correct="Jag förstår inte."),
    AssessmentQuestion(id="sv-a1-004",skill="grammar",difficulty="A1",question="Choose the correct question.",options=["Var du bor?","Bor du var?","Var bor du?","Du var bor?"],correct="Var bor du?"),
    AssessmentQuestion(id="sv-a2-001",skill="grammar",difficulty="A2",question="Which sentence uses the perfect tense?",options=["Jag har läst boken.","Jag läser boken.","Jag ska läsa boken.","Jag läste boken."],correct="Jag har läst boken."),
    AssessmentQuestion(id="sv-a2-002",skill="communication",difficulty="A2",question="Which is a polite request?",options=["Kan du hjälpa mig?","Hej!","Jag är sjuk.","Tåget kommer."],correct="Kan du hjälpa mig?"),
    AssessmentQuestion(id="sv-b1-001",skill="grammar",difficulty="B1",question="Which sentence preserves Swedish V2 order after fronting?",options=["Idag arbetar jag hemma.","Idag jag arbetar hemma.","Idag hemma arbetar jag.","Arbetar idag hemma jag."],correct="Idag arbetar jag hemma."),
    AssessmentQuestion(id="sv-b1-002",skill="grammar",difficulty="B1",question="Which sentence is passive?",options=["Dörren öppnas klockan åtta.","Jag öppnar dörren.","Jag har öppnat dörren.","Jag ska öppna dörren."],correct="Dörren öppnas klockan åtta."),
    AssessmentQuestion(id="sv-b2-001",skill="discourse",difficulty="B2",question="Which connector marks contrast?",options=["Däremot","Därför","Dessutom","Följaktligen"],correct="Däremot"),
    AssessmentQuestion(id="sv-b2-002",skill="register",difficulty="B2",question="Which request is more formally polite?",options=["Skulle du kunna skicka dokumentet?","Skicka dokumentet!","Ge mig dokumentet.","Skicka nu."],correct="Skulle du kunna skicka dokumentet?"),
    AssessmentQuestion(id="sv-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges an academic claim?",options=["Det förefaller som om...","Det är alltid så.","Det är definitivt sant.","Det måste vara så."],correct="Det förefaller som om..."),
    AssessmentQuestion(id="sv-c1-002",skill="professional",difficulty="C1",question="Which phrase fits formal correspondence?",options=["Vi ber er återkomma med...","Hej, vad händer?","Ge mig filen.","Skicka den nu."],correct="Vi ber er återkomma med..."),
    AssessmentQuestion(id="sv-c2-001",skill="discourse",difficulty="C2",question="Which phrase introduces a concession?",options=["Även om detta är relevant...","Därför...","För det första...","Till exempel..."],correct="Även om detta är relevant..."),
    AssessmentQuestion(id="sv-c2-002",skill="translation",difficulty="C2",question="Advanced translation should preserve what besides literal meaning?",options=["Register and pragmatic force","Only word order","Only punctuation","Only word length"],correct="Register and pragmatic force"),
]
