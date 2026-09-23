"""Dansk A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(s,t,summary,ex,examples): return GrammarTopic(slug=s,title=t,level="A1",category="core",summary=summary,explanation=ex,examples=[GrammarExample(text=x) for x in examples])
GRAMMAR_TOPICS=[
_g("pronouns","Personlige pronominer","Use basic subject pronouns.","Learn jeg, du, han, hun and vi for everyday statements.",["Jeg hedder Anna.","Hun er studerende."]),
_g("word-order","Grundlæggende ordstilling","Build simple Danish sentences.","Use subject and finite verb in a basic main-clause pattern.",["Jeg bor i København.","Vi lærer dansk."]),
_g("present-tense","Nutid","Talk about present actions and habits.","Use common present-tense verb forms for current and regular actions.",["Jeg arbejder i dag.","Du taler dansk."]),
_g("questions","Spørgsmål","Ask basic questions.","Use question words and verb-first yes/no questions.",["Hvor bor du?","Taler du dansk?"]),
_g("negation","Nægtelse med ikke","Make negative statements.","Use ikke to negate simple clauses.",["Jeg forstår ikke.","Hun arbejder ikke i dag."]),
_g("definite-nouns","Bestemt form","Refer to specific things.","Learn common indefinite/definite pairs such as en bog / bogen.",["Det er en bog.","Bogen er ny."]),
_g("adjectives","Adjektiver","Describe people and things.","Use common adjectives in simple descriptions.",["En stor bil.","Et lille hus."]),
_g("modal-verbs","Kan og vil","Express ability and wishes.","Use modal verbs with the infinitive.",["Jeg kan svømme.","Jeg vil lære dansk."])
]
def _v(i,t,ws): return VocabularySet(id=i,level="A1",topic=t,unit_ref="da-a1-unit-1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in ws])
VOCABULARY_SETS=[
_v("greetings_a1","Hilsner",[("Hej","phrase","hello","Hej!"),("Godmorgen","phrase","good morning","Godmorgen!"),("Tak","phrase","thanks","Tak for hjælpen.")]),
_v("identity_a1","Identitet",[("navn","noun","name","Hvad hedder du?"),("år","noun","year","Jeg er tyve år."),("studerende","noun","student","Jeg er studerende.")]),
_v("family_a1","Familie",[("mor","noun","mother","Min mor bor her."),("far","noun","father","Min far arbejder."),("søster","noun","sister","Jeg har en søster.")]),
_v("home_a1","Hjem",[("hjem","noun","home","Jeg er hjemme."),("værelse","noun","room","Mit værelse er lille."),("bord","noun","table","Bogen ligger på bordet.")]),
_v("daily_life_a1","Hverdag",[("spise","verb","eat","Jeg spiser morgenmad."),("drikke","verb","drink","Jeg drikker vand."),("arbejde","verb","work","Jeg arbejder mandag.")]),
_v("food_a1","Mad",[("brød","noun","bread","Jeg køber brød."),("kaffe","noun","coffee","Jeg drikker kaffe."),("æble","noun","apple","Jeg spiser et æble.")]),
_v("places_a1","Steder og retninger",[("butik","noun","shop","Butikken ligger her."),("station","noun","station","Hvor ligger stationen?"),("venstre","noun","left","Drej til venstre.")]),
_v("communication_a1","Kommunikation",[("forstå","verb","understand","Jeg forstår."),("spørge","verb","ask","Jeg vil spørge om noget."),("hjælp","noun","help","Kan du hjælpe mig?")])
]
def _p(i,s,ps): return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in ps])
PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","Hilsner og præsentation",[("Hej!","greeting","neutral"),("Jeg hedder Sara.","introducing yourself","neutral"),("Rart at møde dig.","meeting someone","neutral")]),
_p("daily_a1","Hverdag",[("Hvordan har du det?","asking how someone is","neutral"),("Jeg har det godt.","answering","neutral"),("Vi ses i morgen.","saying goodbye","neutral")]),
_p("shopping_a1","Indkøb",[("Hvad koster det?","asking a price","neutral"),("Jeg vil gerne købe den her.","buying an item","neutral"),("Kan jeg betale med kort?","payment","neutral")]),
_p("directions_a1","Vejvisning",[("Hvor ligger stationen?","asking directions","neutral"),("Gå ligeud.","giving directions","neutral"),("Drej til højre.","giving directions","neutral")]),
_p("help_a1","Hjælp",[("Kan du hjælpe mig?","asking for help","neutral"),("Jeg forstår ikke.","asking for clarification","neutral"),("Kan du tale langsommere?","asking someone to slow down","neutral")])
]
CURRICULUM={"A1":[CurriculumUnit(id=f"da-a1-unit-{n}",level="A1",unit_number=n,title=t,grammar_points=g,vocabulary_set_ids=v,lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=c,default_weeks=2) for n,t,g,v,c in [
(1,"Hilsner og identitet",["pronouns","word-order"],["greetings_a1","identity_a1"],["Greet people","Introduce yourself"]),
(2,"Familie og mennesker",["pronouns","definite-nouns"],["identity_a1","family_a1"],["Talk about family","Describe people"]),
(3,"Hjem og ting",["definite-nouns","adjectives"],["home_a1"],["Name common objects","Describe your home"]),
(4,"Hverdag og tid",["present-tense","negation"],["daily_life_a1"],["Describe routines","Say what you do not do"]),
(5,"Mad og indkøb",["questions","modal-verbs"],["food_a1"],["Buy simple food","Ask for prices"]),
(6,"Steder og retninger",["questions","word-order"],["places_a1"],["Ask where places are","Give directions"]),
(7,"Samtale og hjælp",["negation","modal-verbs"],["communication_a1"],["Ask for clarification","Ask for help"]),
(8,"Repetition og A1-kommunikation",["present-tense","questions","adjectives"],["greetings_a1","daily_life_a1","food_a1","places_a1","communication_a1"],["Hold a short everyday conversation","Combine A1 structures"]]]}
ASSESSMENT_BANK=[AssessmentQuestion(id=f"da-a1-{i:03}",skill=s,difficulty="A1",question=q,options=o,correct=c) for i,s,q,o,c in [
(1,"vocabulary","What does 'Tak' mean?",["hello","thanks","please","goodbye"],"thanks"),
(2,"grammar","Choose the correct sentence.",["Jeg er studerende.","Jeg studerende er.","Er jeg studerende er.","Studerende jeg er."],"Jeg er studerende."),
(3,"grammar","Choose the correct negative sentence.",["Jeg ikke forstår.","Jeg forstår ikke.","Ikke jeg forstår.","Jeg forstår er ikke."],"Jeg forstår ikke."),
(4,"grammar","Choose the correct question.",["Hvor du bor?","Bor du hvor?","Hvor bor du?","Du hvor bor?"],"Hvor bor du?"),
(5,"vocabulary","Which word means 'mother'?",["far","søster","mor","bror"],"mor"),
(6,"vocabulary","Which word means 'shop'?",["station","butik","værelse","hjem"],"butik"),
(7,"grammar","Complete: Jeg ___ dansk.",["taler","tale","talte","talt"],"taler"),
(8,"communication","What do you say to ask for help?",["Tak!","Kan du hjælpe mig?","Godnat.","Jeg hedder Ali."],"Kan du hjælpe mig?"),
(9,"vocabulary","Which word means 'water'?",["kaffe","brød","vand","æble"],"vand"),
(10,"grammar","Choose the correct modal sentence.",["Jeg kan svømme.","Jeg kan at svømme.","Jeg kan svømmer.","Jeg kan svømmede."],"Jeg kan svømme.")
]]