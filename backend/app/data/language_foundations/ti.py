"""Tigrinya (ትግርኛ) foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
_G=[
("pronouns","ናይ ሰብ ተውሳኽ ስማት","A1","grammar","ኣነ፣ ንስኻ፣ ንስኺ፣ ንሱን ንሳን ብቐሊሉ ተጠቐም።","ኣነ ተማሃራይ እየ።"),
("identity","ምልላይ ርእስኻ","A1","communication","ስምካን መንነትካን ግለጽ።","ስመይ ሚካኤል እዩ።"),
("family","ስድራን ዘርኢን","A1","grammar","ኣባላት ስድራ ንምግላጽ ቀለልቲ ሓረጋት ተጠቐም።","ሓፍተይ ኣብ ገዛ ኣላ።"),
("present","እዋናዊ ተግባር","A1","verbs","ኣብ ሕጂ ዝካየድ ተግባር ግለጽ።","ሕጂ ትግርኛ እምሃር ኣለኹ።"),
("questions","መሰረታዊ ሕቶታት","A1","communication","መን፣ እንታይ፣ ኣበይ፣ መዓስን ከመይን ተጠቐም።","ኣበይ ትነብር?"),
("negation","ምኽሓድ","A1","syntax","ቀለልቲ ኣሉታዊ ሓረጋት ስራሕ።","ኣነ ኣይፈልጥን።"),
("location","ቦታን ኣቕጣጫን","A1","grammar","ኣብ፣ ናብን ካብን ተጠቒምካ ቦታ ግለጽ።","ኣብ ገዛ ኣለኹ።"),
("time","ግዜን ዕለታትን","A1","time","ሎሚ፣ ጽባሕ፣ ትማሊን ሰዓትን ግለጽ።","ሎሚ ሰኑይ እዩ።"),
("past","ዝሓለፈ ግዜ","A2","verbs","ዝሓለፈ ተግባር ብቐሊሉ ግለጽ።","ትማሊ ናብ ዕዳጋ ከይደ።"),
("future","መጻኢ ግዜ","A2","verbs","መደብን መጻኢ ተግባርን ግለጽ።","ጽባሕ ክመጽእ እየ።"),
("possessives","ምልካውነት","A2","grammar","ናተይ፣ ናትካ፣ ናታን ካልኦትን ተጠቐም።","እዚ መጽሓፍ ናተይ እዩ።"),
("adjectives","መግለጺ ባህርያት","A2","adjectives","ሰብን ነገርን ብባህርያት ግለጽ።","እዚ ገዛ ዓቢ እዩ።"),
("comparatives","ምንጽጻር","A2","adjectives","ክልተ ነገራት ኣነጻጽር።","እዚ መጽሓፍ ካብቲ ይሓይሽ።"),
("imperatives","ትእዛዝን ሕቶን","A2","communication","ትእዛዝ ወይ ሕቶ ብኣኽብሮት ግለጽ።","በጃኻ ቁም።"),
("conjunctions","ምትእስሳር ሓሳባት","A2","syntax","ምኽንያትን ተቓራኒነትን ብምትእስሳር ግለጽ።","ስለ ዝደኸምኩ ኣይከድኩን።"),
("relative","ሓረግ ተዛማዲ","B1","syntax","ሰብ ወይ ነገር ብተዛማዲ ሓረግ ግለጽ።","እቲ መጽሓፍ ዝደለኽዎ እዩ።"),
("subordination","ተገዛኢ ሓረጋት","B1","syntax","ምኽንያት፣ ግዜን ኩነታትን ኣብ ዝተሓላለኸ ሓረግ ኣዋህድ።","እንተ ዘሎ ግዜ ክመጽእ እየ።"),
("conditional","ምስ ኩነታት","B1","verbs","ሓደ ኩነት ንኻልእ ውጽኢት ከመይ ከም ዝወልድ ግለጽ።","እንተ ዘንጊዕካ ክንጽበየካ ኢና።"),
("perfect","ዝተወድአ ተግባር","B1","verbs","ተግባር ከም ዝተወድአ ግለጽ።","ኣብ ገዛ በጺሐ እየ።"),
("habitual","ልምዲ","B1","verbs","ተደጋጋሚ ተግባር ግለጽ።","ኩሉ ንግሆ ስፖርት እገብር።"),
("passive","ተገብሮ ኣቀራርባ","B1","syntax","ትኩረት ኣብ ተግባር ወይ ውጽኢት ኣክብር።","እቲ ደብዳበ ተጻሒፉ እዩ።"),
("reported-speech","ተነጊሩ ዝቐረበ ሓሳብ","B1","discourse","ዝተዛረበ ሰብ ሓሳቡ ከመይ ከም ዝተሓበረ ግለጽ።","ንሱ ክመጽእ እዩ ኢሉ።"),
("connectors","መራኸቢ ቃላት","B1","discourse","ግን፣ ስለዚ፣ እንተኾነ ግንን ካልእን ተጠቐም።","ሓሚመ እየ፣ ስለዚ ኣይከድኩን።"),
("causative","ምኽንያት ተግባር","B2","verbs","ሓደ ሰብ ንኻልእ ተግባር ከም ዝገብር ግለጽ።","መምህር ንተማሃሮ ኣንቢቦም ከም ዝምሃሩ ይገብር።"),
("reciprocal","ሓድሕዳዊ ተግባር","B2","verbs","ሓድሕዳዊ ተግባር ግለጽ።","እቶም ኣዕሩኽ ሓድሕዶም ይሕግዙ።"),
("complex-relative","ዝተሓላለኸ ተዛማዲ","B2","syntax","ነዊሕ ተዛማዲ ሓረጋት ብግልጺ ኣዋህድ።","እቲ ትማሊ ዝኣነብክዎ መጽሓፍ ኣገዳሲ እዩ።"),
("indirect-question","ቀጥታዊ ዘይኮነ ሕቶ","B2","syntax","ሕቶ ኣብ ዓቢ ሓረግ ኣእቱ።","ኣበይ ከም ዝነብር ኣይፈልጥን።"),
("discourse-markers","መዋቕር ውይይት","B2","discourse","መጀመርታ፣ ብተወሳኺ፣ ብኣንጻሩን ኣብ መወዳእታን ተጠቐም።","መጀመርታ ጉዳዩ ንመርምሮ።"),
("subjunctive","ምኽሪን ድሌትን","C1","pragmatics","ምኽሪ፣ ድሌትን ግዴታን ብትክክል ግለጽ።","ክንጀምር ይግባእ።"),
("nominalization","ምፍጣር ስም","C1","word-formation","ተግባር ወይ ባህርይ ናብ ስም ቀይር ኣብ መዝገብ ስራሕ።","ምርምር ቋንቋ ይቕጽል ኣሎ።"),
("information-structure","መዋቕር ሓበሬታ","C1","discourse","ርእሰ ጉዳይ፣ ትኩረትን ሓድሽ ሓበሬታን ኣደራጅ።","እቲ ኣገዳሲ ነገር ውጽኢት እዩ።"),
("formal-register","ስርዓተ ቋንቋ ስራሕ","C1","register","ብዕላዊ ሰነዳት ትኽክለኛ ቃላት ምረጽ።","በጃኻ ሰነድካ ቅድሚ ዕለቱ ኣቕርብ።"),
("idioms","ምስላታትን ፈሊጣትን","C2","lexis","ምስላ ብመሰረት ኩነታት ተርጉም።","ቃላቱ ብኻልእ ትርጉም እዮም ዝጥቀሙ።"),
("rhetoric","ስነ-ክርክርን ርትዕን","C2","rhetoric","ሓሳብ ብምስክርን ተቓራኒ ርእይቶን ኣቕርብ።","እዚ ክርክር ሓያል እዩ፣ ግን ምስክሩ ውሱን እዩ።"),
]
GRAMMAR_TOPICS=[GrammarTopic(slug=s,title=t,level=l,category=c,summary=sm,explanation=sm,examples=[GrammarExample(text=e)]) for s,t,l,c,sm,e in _G]

_V=[
("A1","ሰላም","phrase","hello","ሰላም፣ ከመይ ኣለኻ?"),
("A1","ስም","noun","name","ስመይ ሚካኤል እዩ።"),
("A1","ስድራ","noun","family","ስድራይ ኣብዚ ኣሎ።"),
("A1","ገዛ","noun","house","ኣብ ገዛ ኣለኹ።"),
("A1","ቤት ትምህርቲ","noun","school","ናብ ቤት ትምህርቲ እኸይድ።"),
("A1","ማይ","noun","water","ማይ እደሊ።"),
("A1","ዕዳጋ","noun","market","ናብ ዕዳጋ ከይደ።"),
("A1","ሓገዝ","noun","help","ሓገዝ እደሊ።"),
("A2","ጉዕዞ","noun","journey","ጉዕዞና ጽባሕ እዩ።"),
("A2","ሕክምና","noun","healthcare","ንሕክምና ናብ ሓኪም ከይደ።"),
("A2","ዋጋ","noun","price","ዋጋ እዚ ክንደይ እዩ?"),
("A2","ዝናብ","noun","rain","ሎሚ ዝናብ ኣሎ።"),
("B1","ስራሕ","noun","work","ኣብ ስራሕ ኣለኹ።"),
("B1","ትምህርቲ","noun","education","ትምህርቲ ኣገዳሲ እዩ።"),
("B1","ማሕበረሰብ","noun","community","ማሕበረሰብና ብሓባር ይሰርሕ።"),
("B1","ርእይቶ","noun","opinion","ርእይቶኻ ክሰምዕ እደሊ።"),
("B2","ቴክኖሎጂ","noun","technology","ቴክኖሎጂ ንስራሕ ይቕይሮ።"),
("B2","ምርምር","noun","research","ምርምር ሓድሽ ውጽኢት ኣምጺኡ።"),
("C1","ማስረጃ","noun","evidence","ማስረጃ ነዚ ርእይቶ ይድግፍ።"),
("C2","ኣውድ","noun","context","ትርጉም ቃል ኣብ ኣውድ ይምርኮስ።"),
]
VOCABULARY_SETS=_VOCABULARY_SETS=[]
for i,(level,word,pos,definition,example) in enumerate(_V,1):
    idx=sum(1 for x in _V[:i] if x[0]==level)
    VOCABULARY_SETS.append(VocabularySet(id=f"ti-{level.lower()}-{idx}",level=level,topic=word,unit_ref=f"ti-{level.lower()}-unit-{min(idx,8)}",words=[VocabularyEntry(word=word,pos=pos,definition=definition,example=example)]))

_PH=[
("ሰላምታ",[("ሰላም፣ ከመይ ኣለኻ?","greeting","neutral"),("ከመይ ኣለኺ?","greeting","neutral"),("የቐንየለይ።","thanks","neutral")]),
("ምልላይ",[("ስመይ ሚካኤል እዩ።","introducing yourself","neutral"),("ካበይ ኢኻ?","asking origin","neutral"),("ኣነ ካብ ኣስመራ እየ።","stating origin","neutral")]),
("መዓልታዊ",[("ናብ ስራሕ እኸይድ።","daily routine","neutral"),("ሕጂ ክመጽእ እየ።","arrangement","neutral"),("ኣይተረድኣንን።","clarification","neutral")]),
("ዕዳጋ",[("ዋጋ እዚ ክንደይ እዩ?","asking price","neutral"),("እዚ እደሊ።","requesting item","neutral"),("ብካርድ ክኸፍል ይኽእልዶ?","payment","polite")]),
("ኣቕጣጫ",[("ጣብያ ኣበይ ኣሎ?","asking location","neutral"),("ቀጥታ ኪድ።","giving directions","neutral"),("ናብ የማን ግደ።","direction","neutral")]),
("ምግቢ",[("ማይ በጃኻ።","ordering drink","polite"),("እዚ ምግቢ እደሊ።","ordering food","neutral"),("እዚ ምግቢ ጥዑም እዩ።","commenting on food","neutral")]),
("ጥዕና",[("ርእሰይ ይሓምመኒ።","symptom","neutral"),("ሓኪም ክርኢ እደሊ።","seeking care","neutral"),("ሕጂ ይሓይሸኒ ኣሎ።","recovery","neutral")]),
("ስራሕ",[("ኣብዚ እሰርሕ።","work","neutral"),("እቲ ኣኼባ መዓስ እዩ?","meeting","neutral"),("ጽባሕ ኣብ ቤት ጽሕፈት ንራኸብ።","arrangement","neutral")]),
("ጉዕዞ",[("ቲኬት ኣለኒ።","travel","neutral"),("ባቡር መዓስ ይወጽእ?","departure","neutral"),("ፓስፖርተይ ጠፊኡኒ።","problem","neutral")]),
("ርእይቶ",[("ብርእይቶይ እዚ ሓሳብ ጽቡቕ እዩ።","opinion","neutral"),("ምሳኻ እሰማማዕ።","agreement","neutral"),("ብሓፂሩ ኣይሰማማዕን።","polite disagreement","polite")]),
("ዕላዊ",[("በጃኻ ማመልከቻይ ተቐበል።","formal request","formal"),("ተወሳኺ ሓበሬታ ክረኽብ እደሊ።","formal inquiry","formal"),("ንትሕብብርኩም የቐንየልና።","formal thanks","formal")]),
("ኣካዳሚ",[("እዚ ምርምር ሓድሽ ውጽኢት የርኢ።","research","formal"),("እዚ ምንጪ በጃኻ ተወከስ።","reference","formal"),("መደምደምታ ኣብ ማስረጃ ይምርኮስ።","academic discussion","formal")]),
("ክርክር",[("እዚ ርእይቶ ሓያል እዩ፣ ግን ...","qualified argument","formal"),("ኣብዚ ኣውድ ኣገዳሲ እዩ።","context","formal"),("ሓደ ተቓራኒ ርእይቶ ክንርኢ ኣለና።","counterargument","formal")]),
]
PHRASEBOOK_CATEGORIES=[PhrasebookCategory(id=f"ti-phrase-{i}",level="A1" if i<=5 else ("B1" if i<=9 else "C1"),situation=s,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in rows]) for i,(s,rows) in enumerate(_PH,1)]

_THEMES={
"A1":["ሰላምታን ምልላይን","ስድራ","ገዛ","መዓልታዊ ልምዲ","ግዜ","ምግቢ","ቦታታት","ሓበሬታ"],
"A2":["ጉዕዞ","ጥዕና","ዕዳጋ","ኩነታት ኣየር","መደባት","ኣገልግሎት","ምንጽጻር","ድግግሞሽ"],
"B1":["ስራሕ","ትምህርቲ","ማሕበረሰብ","ርእይቶ","ፍጻመታት","ርክብ","ዜና","ድግግሞሽ"],
"B2":["ቴክኖሎጂ","ምርምር","ሚድያ","ምምሕዳር","ከባቢ","ባህሊ","ክርክር","ድግግሞሽ"],
"C1":["ማስረጃ","ምርምር","ጽሑፍ","ምትንታን","ዕላዊ ሓበሬታ","ኣቀራርባ","ውይይት","ድግግሞሽ"],
"C2":["ምስላ","ኣውድ","ስነ-ክርክር","ስነ-ጽሑፍ","ትርጉም","ቅዲ","ሓሳብ ብዙሕ ደረጃ","ድግግሞሽ"]}
_GMAP={
"A1":["pronouns","identity","family","present","questions","negation","location","time"],
"A2":["past","future","possessives","adjectives","comparatives","imperatives","conjunctions","time"],
"B1":["relative","subordination","conditional","perfect","habitual","passive","reported-speech","connectors"],
"B2":["causative","reciprocal","complex-relative","indirect-question","discourse-markers","conditional","passive","relative"],
"C1":["subjunctive","nominalization","information-structure","formal-register","reported-speech","connectors","subordination","relative"],
"C2":["idioms","rhetoric","information-structure","formal-register","nominalization","discourse-markers","complex-relative","subordination"]}
CURRICULUM={}
for level in LEVELS:
    CURRICULUM[level]=[]
    for n,title in enumerate(_THEMES[level],1):
        # Reuse the closest level vocabulary set when an advanced unit has no dedicated single-item set.
        vid=f"ti-{level.lower()}-{min(n,8 if level=='A1' else 4)}"
        CURRICULUM[level].append(CurriculumUnit(id=f"ti-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=[_GMAP[level][n-1]],vocabulary_set_ids=[vid],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[f"Communicate in Tigrinya about {title.lower()}","Apply {level} grammar in context"],default_weeks=2))

ASSESSMENT_BANK=[
AssessmentQuestion(id="ti-a1-001",skill="vocabulary",difficulty="A1",question="Which phrase is a greeting?",options=["ሰላም፣ ከመይ ኣለኻ?","ማይ እደሊ።","ኣብ ገዛ ኣለኹ።","ሎሚ ሰኑይ እዩ።"],correct="ሰላም፣ ከመይ ኣለኻ?"),
AssessmentQuestion(id="ti-a1-002",skill="communication",difficulty="A1",question="Which sentence gives your name?",options=["ስመይ ሚካኤል እዩ።","ማይ እደሊ።","ኣብ ገዛ ኣለኹ።","ሎሚ ሰኑይ እዩ።"],correct="ስመይ ሚካኤል እዩ።"),
AssessmentQuestion(id="ti-a1-003",skill="grammar",difficulty="A1",question="Which sentence describes a daily routine?",options=["ኩሉ መዓልቲ ናብ ቤት ትምህርቲ እኸይድ።","ሎሚ ሰኑይ እዩ።","ሰላም።","ዋጋ እዚ ክንደይ እዩ?"],correct="ኩሉ መዓልቲ ናብ ቤት ትምህርቲ እኸይድ።"),
AssessmentQuestion(id="ti-a1-004",skill="vocabulary",difficulty="A1",question="Which word refers to water?",options=["ማይ","ገዛ","ስም","ስድራ"],correct="ማይ"),
AssessmentQuestion(id="ti-a1-005",skill="grammar",difficulty="A1",question="Which sentence gives a location?",options=["ኣብ ገዛ ኣለኹ።","ስመይ ሚካኤል እዩ።","ማይ እደሊ።","ሰላም።"],correct="ኣብ ገዛ ኣለኹ።"),
AssessmentQuestion(id="ti-a1-006",skill="communication",difficulty="A1",question="Which phrase asks where someone lives?",options=["ኣበይ ትነብር?","ከመይ ኣለኻ?","የቐንየለይ።","ማይ እደሊ።"],correct="ኣበይ ትነብር?"),
AssessmentQuestion(id="ti-a1-007",skill="vocabulary",difficulty="A1",question="Which word means family?",options=["ስድራ","ገዛ","ዕዳጋ","ማይ"],correct="ስድራ"),
AssessmentQuestion(id="ti-a1-008",skill="grammar",difficulty="A1",question="Which sentence is negative?",options=["ኣነ ኣይፈልጥን።","ኣነ እፈልጥ።","ኣብ ገዛ ኣለኹ።","ማይ እደሊ።"],correct="ኣነ ኣይፈልጥን።"),
AssessmentQuestion(id="ti-b1-009",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["እንተ ዘሎ ግዜ ክመጽእ እየ።","ኣብ ገዛ ኣለኹ።","ሕጂ እምሃር ኣለኹ።","ማይ እደሊ።"],correct="እንተ ዘሎ ግዜ ክመጽእ እየ።"),
AssessmentQuestion(id="ti-b1-010",skill="grammar",difficulty="B1",question="Which sentence reports another person's speech?",options=["ንሱ ክመጽእ እዩ ኢሉ።","ኣነ ክመጽእ እየ።","ኣብ ገዛ ኣለኹ።","ማይ እደሊ።"],correct="ንሱ ክመጽእ እዩ ኢሉ።"),
AssessmentQuestion(id="ti-b2-011",skill="grammar",difficulty="B2",question="Which sentence is an indirect question?",options=["ኣበይ ከም ዝነብር ኣይፈልጥን።","ኣበይ ትነብር?","ኣብ ገዛ ኣለኹ።","ናብ ገዛ እኸይድ።"],correct="ኣበይ ከም ዝነብር ኣይፈልጥን።"),
AssessmentQuestion(id="ti-b2-012",skill="grammar",difficulty="B2",question="Which phrase structures discourse?",options=["መጀመርታ ጉዳዩ ንመርምሮ።","ማይ እደሊ።","ሰላም።","ኣብ ገዛ ኣለኹ።"],correct="መጀመርታ ጉዳዩ ንመርምሮ።"),
AssessmentQuestion(id="ti-c1-013",skill="register",difficulty="C1",question="Which phrase suits a formal request?",options=["በጃኻ ሰነድካ ቅድሚ ዕለቱ ኣቕርብ።","ሰላም!","ማይ እደሊ።","ኣበይ ኢኻ?"],correct="በጃኻ ሰነድካ ቅድሚ ዕለቱ ኣቕርብ።"),
AssessmentQuestion(id="ti-c2-014",skill="rhetoric",difficulty="C2",question="Which statement introduces a qualified argument?",options=["እዚ ክርክር ሓያል እዩ፣ ግን ምስክሩ ውሱን እዩ።","እዚ ሓደ ቃል እዩ።","ማይ እደሊ።","ሰላም።"],correct="እዚ ክርክር ሓያል እዩ፣ ግን ምስክሩ ውሱን እዩ።"),
]
