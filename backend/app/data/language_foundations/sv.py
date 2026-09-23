"""Svenska A1 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug,title,summary,ex,examples):
    return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=ex,examples=[GrammarExample(text=x) for x in examples])
GRAMMAR_TOPICS=[
_g("pronouns","Personliga pronomen","Use basic subject pronouns.","Jag, du, han, hon and vi identify the speaker or subject.",["Jag heter Anna.","Hon är student."]),
_g("word-order","Grundläggande ordföljd","Build simple Swedish statements.","A basic main clause normally places the subject before the finite verb.",["Jag bor i Stockholm.","Vi studerar svenska."]),
_g("present-tense","Presens","Talk about habits and current facts.","Common verbs use present forms to describe what happens now or regularly.",["Jag arbetar idag.","Du talar svenska."]),
_g("definite-nouns","Bestämd form","Talk about specific people and things.","Learn common indefinite and definite noun patterns such as en bok / boken.",["Det är en bok.","Boken är ny."]),
_g("questions","Frågor","Ask simple yes/no and information questions.","Yes/no questions commonly place the finite verb before the subject.",["Bor du här?","Var bor du?"]),
_g("negation","Negation med inte","Make simple negative sentences.","Place inte after the finite verb in a basic main clause.",["Jag förstår inte.","Hon arbetar inte idag."]),
_g("adjectives","Vanliga adjektiv","Describe people and things.","Basic adjectives agree with common noun gender and number.",["En stor bil.","Ett stort hus."]),
_g("modal-verbs","Kan och vill","Express ability and wishes.","Use common modal verbs with an infinitive without att.",["Jag kan simma.","Jag vill lära mig svenska."])
]
def _v(i,topic,words): return VocabularySet(id=i,level="A1",topic=topic,unit_ref="sv-a1-unit-1",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])
VOCABULARY_SETS=[
_v("greetings_a1","Hälsningar",[("Hej","phrase","hello","Hej!"),("God morgon","phrase","good morning","God morgon!"),("Tack","phrase","thanks","Tack så mycket.")]),
_v("identity_a1","Jag och du",[("namn","noun","name","Vad heter du?"),("år","noun","year","Jag är tjugo år."),("student","noun","student","Jag är student.")]),
_v("family_a1","Familj",[("mamma","noun","mother","Min mamma bor här."),("pappa","noun","father","Min pappa arbetar."),("syster","noun","sister","Jag har en syster.")]),
_v("home_a1","Hemmet",[("hem","noun","home","Jag är hemma."),("rum","noun","room","Mitt rum är litet."),("bord","noun","table","Boken ligger på bordet.")]),
_v("daily_life_a1","Vardag",[("äta","verb","eat","Jag äter frukost."),("dricka","verb","drink","Jag dricker vatten."),("arbeta","verb","work","Jag arbetar på måndag.")]),
_v("food_a1","Mat",[("bröd","noun","bread","Jag köper bröd."),("kaffe","noun","coffee","Jag dricker kaffe."),("äpple","noun","apple","Jag äter ett äpple.")]),
_v("places_a1","Platser och riktningar",[("butik","noun","shop","Butiken ligger här."),("station","noun","station","Var ligger stationen?"),("vänster","noun","left","Sväng till vänster.")]),
_v("communication_a1","Kommunikation",[("förstå","verb","understand","Jag förstår."),("fråga","verb","ask","Jag vill fråga något."),("hjälp","noun","help","Kan du hjälpa mig?")])
]
def _p(i,s,phrases): return PhrasebookCategory(id=i,level="A1",situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in phrases])
PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","Hälsa och presentera sig",[("Hej!","greeting","neutral"),("Jag heter Sara.","introducing yourself","neutral"),("Trevligt att träffas.","meeting someone","neutral")]),
_p("daily_a1","Vardag",[("Hur mår du?","asking how someone is","neutral"),("Jag mår bra.","answering","neutral"),("Vi ses imorgon.","saying goodbye","neutral")]),
_p("shopping_a1","Handla",[("Vad kostar det?","asking a price","neutral"),("Jag vill köpa den här.","buying an item","neutral"),("Kan jag betala med kort?","payment","neutral")]),
_p("directions_a1","Fråga efter vägen",[("Var ligger stationen?","asking directions","neutral"),("Gå rakt fram.","giving directions","neutral"),("Sväng till höger.","giving directions","neutral")]),
_p("help_a1","Be om hjälp",[("Kan du hjälpa mig?","asking for help","neutral"),("Jag förstår inte.","asking for clarification","neutral"),("Kan du tala långsamt?","asking someone to slow down","neutral")])
]
CURRICULUM={"A1":[
CurriculumUnit(id=f"sv-a1-unit-{n}",level="A1",unit_number=n,title=t,grammar_points=g,vocabulary_set_ids=v,lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=c,default_weeks=2)
for n,t,g,v,c in [
(1,"Hälsningar och identitet",["pronouns","word-order"],["greetings_a1","identity_a1"],["Greet people","Introduce yourself"]),
(2,"Familj och människor",["pronouns","definite-nouns"],["identity_a1","family_a1"],["Talk about family","Describe people"]),
(3,"Hem och saker",["definite-nouns","adjectives"],["home_a1"],["Name common objects","Describe your home"]),
(4,"Vardag och tid",["present-tense","negation"],["daily_life_a1"],["Describe routines","Say what you do not do"]),
(5,"Mat och inköp",["questions","modal-verbs"],["food_a1"],["Buy simple food","Ask for prices"]),
(6,"Platser och vägen",["questions","word-order"],["places_a1"],["Ask where places are","Give simple directions"]),
(7,"Samtal och hjälp",["negation","modal-verbs"],["communication_a1"],["Ask for clarification","Ask for help"]),
(8,"Repetition och A1-kommunikation",["present-tense","questions","adjectives"],["greetings_a1","daily_life_a1","food_a1","places_a1","communication_a1"],["Hold a short everyday conversation","Combine A1 structures"])
]]}
ASSESSMENT_BANK=[
AssessmentQuestion(id=f"sv-a1-{i:03}",skill=s,difficulty="A1",question=q,options=o,correct=c)
for i,s,q,o,c in [
(1,"vocabulary","What does 'Tack' mean?",["hello","thanks","please","goodbye"],"thanks"),
(2,"grammar","Choose the correct sentence.",["Jag är student.","Jag student är.","Är jag student är.","Student jag är."],"Jag är student."),
(3,"grammar","Choose the correct negative sentence.",["Jag inte förstår.","Jag förstår inte.","Inte jag förstår.","Jag förstår är inte."],"Jag förstår inte."),
(4,"grammar","Choose the correct question.",["Var du bor?","Bor du var?","Var bor du?","Du var bor?"],"Var bor du?"),
(5,"vocabulary","Which word means 'mother'?",["pappa","syster","mamma","bror"],"mamma"),
(6,"vocabulary","Which word means 'shop'?",["station","butik","rum","hem"],"butik"),
(7,"grammar","Complete: Jag ___ svenska.",["talar","tala","talade","tal"],"talar"),
(8,"communication","What do you say to ask for help?",["Tack!","Kan du hjälpa mig?","God natt.","Jag heter Ali."],"Kan du hjälpa mig?"),
(9,"vocabulary","Which word means 'water'?",["kaffe","bröd","vatten","äpple"],"vatten"),
(10,"grammar","Choose the correct modal sentence.",["Jag kan simma.","Jag kan att simma.","Jag kan simmar.","Jag kan simmade."],"Jag kan simma.")
]]
