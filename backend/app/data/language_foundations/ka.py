"""ქართული (Georgian) foundation data for JUBA LISAN — CEFR A1-C2."""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet,
    PhrasebookCategory, PhrasebookEntry, AssessmentQuestion,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]

GRAMMAR_TOPICS = [
    GrammarTopic(slug="ka-a1-copula", title="Copula and identity", level="A1", category="grammar", summary="Use Georgian copula forms to identify people and things.", explanation="Use ვარ, ხარ, არის and related forms with nouns and adjectives.", examples=[GrammarExample(text="მე სტუდენტი ვარ."), GrammarExample(text="ის ექიმია.")]),
    GrammarTopic(slug="ka-a1-present", title="Present tense", level="A1", category="verbs", summary="Talk about current actions.", explanation="Learn common present-series verb forms and personal agreement.", examples=[GrammarExample(text="მე ვმუშაობ."), GrammarExample(text="ის სწავლობს.")]),
    GrammarTopic(slug="ka-a1-cases", title="Core noun cases", level="A1", category="morphology", summary="Recognise basic Georgian case forms.", explanation="Georgian marks grammatical roles with case endings; begin with nominative, dative and postpositions.", examples=[GrammarExample(text="სახლში ვარ."), GrammarExample(text="მეგობარს ველაპარაკები.")]),
    GrammarTopic(slug="ka-a1-possession", title="Possession and existential forms", level="A1", category="grammar", summary="Express ownership and existence.", explanation="Use მაქვს and related constructions to say what you have and where things are.", examples=[GrammarExample(text="მე წიგნი მაქვს."), GrammarExample(text="მაგიდაზე წიგნია.")]),
    GrammarTopic(slug="ka-a1-questions", title="Question words", level="A1", category="syntax", summary="Ask who, what, where and when.", explanation="Use ვინ, რა, სად, როდის, როგორ and რამდენი in simple questions.", examples=[GrammarExample(text="სად ცხოვრობ?"), GrammarExample(text="რა გქვია?")]),
    GrammarTopic(slug="ka-a1-negation", title="Negation", level="A1", category="syntax", summary="Negate simple statements.", explanation="Use არ with present forms and არ არის with copular clauses.", examples=[GrammarExample(text="მე არ ვმუშაობ."), GrammarExample(text="ის აქ არ არის.")]),
    GrammarTopic(slug="ka-a1-plurals", title="Plural nouns", level="A1", category="morphology", summary="Form and recognise common plurals.", explanation="Learn common plural formation and agreement in everyday phrases.", examples=[GrammarExample(text="მეგობრები აქ არიან."), GrammarExample(text="ბავშვები თამაშობენ.")]),
    GrammarTopic(slug="ka-a2-past", title="Past series and completed events", level="A2", category="verbs", summary="Talk about what happened.", explanation="Build common past-tense forms and distinguish habitual states from completed events.", examples=[GrammarExample(text="გუშინ წავედი."), GrammarExample(text="ფილმი ვნახე.")]),
    GrammarTopic(slug="ka-a2-future", title="Future and plans", level="A2", category="verbs", summary="Describe future events and intentions.", explanation="Use future-series forms and contextual time expressions for plans and predictions.", examples=[GrammarExample(text="ხვალ წავალ."), GrammarExample(text="საღამოს დავურეკავ.")]),
    GrammarTopic(slug="ka-a2-case-system", title="Case system in everyday use", level="A2", category="morphology", summary="Use cases for objects, recipients and locations.", explanation="Expand control of dative, genitive, instrumental and other common case functions.", examples=[GrammarExample(text="მეგობრის წიგნი მაქვს."), GrammarExample(text="ავტობუსით მივდივარ.")]),
    GrammarTopic(slug="ka-a2-comparison", title="Comparison and description", level="A2", category="adjectives", summary="Compare people, places and things.", explanation="Use comparative expressions and descriptive vocabulary in connected speech.", examples=[GrammarExample(text="ეს ქალაქი უფრო დიდია."), GrammarExample(text="ეს გზა უფრო მოკლეა.")]),
    GrammarTopic(slug="ka-a2-motion", title="Motion and direction", level="A2", category="verbs", summary="Describe movement and destinations.", explanation="Use common motion verbs with location expressions and case-marked destinations.", examples=[GrammarExample(text="სკოლაში მივდივარ."), GrammarExample(text="სახლიდან მოვედი.")]),
    GrammarTopic(slug="ka-b1-screeve-system", title="Georgian screeve system", level="B1", category="verbs", summary="Control present, future and past series.", explanation="Develop systematic control of Georgian screeves and the way aspect and series encode events.", examples=[GrammarExample(text="ვკითხულობ."), GrammarExample(text="წავიკითხე.")]),
    GrammarTopic(slug="ka-b1-relative", title="Relative clauses", level="B1", category="syntax", summary="Add information about people and things.", explanation="Build relative clauses with appropriate subordinating patterns.", examples=[GrammarExample(text="ადამიანი, რომელიც აქ ცხოვრობს, ჩემი მეგობარია."), GrammarExample(text="წიგნი, რომელიც წავიკითხე, საინტერესოა.")]),
    GrammarTopic(slug="ka-b1-conditionals", title="Conditionals and hypothetical situations", level="B1", category="syntax", summary="Discuss possible and unreal situations.", explanation="Use თუ clauses and conditional forms to express conditions, advice and hypotheses.", examples=[GrammarExample(text="თუ დრო მექნება, მოვალ."), GrammarExample(text="რომ მცოდნოდა, გეტყოდი.")]),
    GrammarTopic(slug="ka-b1-connectors", title="Connectors and argument flow", level="B1", category="discourse", summary="Link reasons, results and contrasts.", explanation="Use მაგრამ, ამიტომ, რადგან, თუმცა and related connectors to create coherent speech.", examples=[GrammarExample(text="დავრჩი, რადგან წვიმდა."), GrammarExample(text="დაღლილი ვიყავი, მაგრამ მაინც წავედი.")]),
    GrammarTopic(slug="ka-b2-indirect-speech", title="Reported speech", level="B2", category="syntax", summary="Report what people said or believed.", explanation="Embed statements and questions while maintaining correct Georgian tense and case patterns.", examples=[GrammarExample(text="მან თქვა, რომ ხვალ მოვა."), GrammarExample(text="ვკითხე, სად ცხოვრობდა.")]),
    GrammarTopic(slug="ka-b2-version-system", title="Verb version and argument structure", level="B2", category="verbs", summary="Interpret indirect objects and version marking.", explanation="Understand Georgian verb morphology and version markers as part of argument structure.", examples=[GrammarExample(text="მე მას წიგნი მივეცი."), GrammarExample(text="მას ეს ამბავი მოეწონა.")]),
    GrammarTopic(slug="ka-b2-subordination", title="Complex subordinate clauses", level="B2", category="syntax", summary="Build multi-clause explanations.", explanation="Combine temporal, causal, concessive and conditional clauses with precise reference.", examples=[GrammarExample(text="მიუხედავად იმისა, რომ გვიან იყო, შეხვედრა გაგრძელდა."), GrammarExample(text="როცა სახლში მივედი, უკვე ეძინა.")]),
    GrammarTopic(slug="ka-b2-formal", title="Formal and professional Georgian", level="B2", category="style", summary="Adapt language to workplace and institutional contexts.", explanation="Use precise vocabulary, impersonal constructions and appropriate formal register.", examples=[GrammarExample(text="გთხოვთ, გაითვალისწინოთ აღნიშნული საკითხი."), GrammarExample(text="ანგარიშის მიხედვით, საჭიროა დამატებითი კვლევა.")]),
    GrammarTopic(slug="ka-c1-nominalisation", title="Abstract and nominal style", level="C1", category="style", summary="Write dense analytical prose.", explanation="Use abstract nouns and compact structures common in academic, administrative and analytical Georgian.", examples=[GrammarExample(text="პოლიტიკის განხორციელების შეფასება აუცილებელია."), GrammarExample(text="მონაცემთა ანალიზმა მნიშვნელოვანი ცვლილება აჩვენა.")]),
    GrammarTopic(slug="ka-c1-hedging", title="Academic hedging and qualification", level="C1", category="pragmatics", summary="Calibrate certainty and interpretation.", explanation="Use expressions such as სავარაუდოდ, შესაძლოა and შეიძლება ითქვას to qualify claims.", examples=[GrammarExample(text="სავარაუდოდ, შედეგებზე სხვა ფაქტორებმაც იმოქმედა."), GrammarExample(text="შეიძლება ითქვას, რომ მიდგომა ეფექტიანია.")]),
    GrammarTopic(slug="ka-c1-pragmatics", title="Pragmatic nuance and register", level="C1", category="pragmatics", summary="Control politeness, implication and tone.", explanation="Choose forms according to social distance, institutional setting and communicative intent.", examples=[GrammarExample(text="თუ წინააღმდეგი არ ხართ, საკითხს მოგვიანებით დავუბრუნდეთ."), GrammarExample(text="ეს შესაძლოა სხვაგვარადაც განიმარტოს.")]),
    GrammarTopic(slug="ka-c2-advanced-syntax", title="Advanced information structure", level="C2", category="syntax", summary="Control embedded and rhetorically structured clauses.", explanation="Combine subordinate clauses, participial structures and discourse framing with high precision.", examples=[GrammarExample(text="ის, რაც თავდაპირველად უმნიშვნელოდ ჩანდა, საბოლოოდ გადამწყვეტი აღმოჩნდა."), GrammarExample(text="იმის მიუხედავად, რომ შედეგის ზუსტად პროგნოზირება შეუძლებელია, რისკების შეფასება შესაძლებელია.")]),
    GrammarTopic(slug="ka-c2-rhetoric", title="Rhetorical and literary register", level="C2", category="style", summary="Use sophisticated Georgian across genres.", explanation="Control lexical nuance, rhetorical contrast and stylistic variation in essays, commentary and formal speech.", examples=[GrammarExample(text="საკითხი მხოლოდ ეკონომიკური თვალსაზრისით კი არა, სოციალური კუთხითაც უნდა განვიხილოთ."), GrammarExample(text="საბოლოო ჯამში, გადაწყვეტილების მნიშვნელობა ცალკეულ ციფრებს სცდება.")]),
]

def _unit(level, n, title, grammar, vocab):
    return CurriculumUnit(
        id=f"ka-{level.lower()}-unit-{n}", level=level, unit_number=n, title=title,
        grammar_points=grammar, vocabulary_set_ids=[vocab],
        lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],
        competency_checklist=[f"Use {title} vocabulary", f"Apply {grammar[0]} in connected Georgian"],
        default_weeks=2,
    )

CURRICULUM = {
    "A1": [
        _unit("A1",1,"მისალმება და გაცნობა",["ka-a1-copula"],"ka_a1_social"),
        _unit("A1",2,"ოჯახი და იდენტობა",["ka-a1-possession"],"ka_a1_family"),
        _unit("A1",3,"სახლი და ადგილები",["ka-a1-cases"],"ka_a1_home"),
        _unit("A1",4,"კითხვები და უარყოფა",["ka-a1-questions","ka-a1-negation"],"ka_a1_questions"),
        _unit("A1",5,"ყოველდღიური ცხოვრება",["ka-a1-present"],"ka_a1_routine"),
        _unit("A1",6,"საკვები და საყიდლები",["ka-a1-plurals"],"ka_a1_food"),
    ],
    "A2": [
        _unit("A2",1,"წარსული მოვლენები",["ka-a2-past"],"ka_a2_past"),
        _unit("A2",2,"მომავალი და გეგმები",["ka-a2-future"],"ka_a2_future"),
        _unit("A2",3,"ბრუნვები და ურთიერთობები",["ka-a2-case-system"],"ka_a2_cases"),
        _unit("A2",4,"აღწერა და შედარება",["ka-a2-comparison"],"ka_a2_comparison"),
        _unit("A2",5,"მოძრაობა და მიმართულება",["ka-a2-motion"],"ka_a2_travel"),
        _unit("A2",6,"ყოველდღიური კომუნიკაცია",["ka-a2-past","ka-a2-future"],"ka_a2_review"),
    ],
    "B1": [
        _unit("B1",1,"ზმნის სისტემის გაღრმავება",["ka-b1-screeve-system"],"ka_b1_verbs"),
        _unit("B1",2,"ადამიანები და საგნები",["ka-b1-relative"],"ka_b1_relations"),
        _unit("B1",3,"პირობითი სიტუაციები",["ka-b1-conditionals"],"ka_b1_conditions"),
        _unit("B1",4,"მიზეზი და შედეგი",["ka-b1-connectors"],"ka_b1_argument"),
        _unit("B1",5,"სამუშაო და სწავლა",["ka-b1-screeve-system"],"ka_b1_work"),
        _unit("B1",6,"მოსაზრება და დისკუსია",["ka-b1-connectors","ka-b1-conditionals"],"ka_b1_discussion"),
    ],
    "B2": [
        _unit("B2",1,"ნათქვამი და გადმოცემა",["ka-b2-indirect-speech"],"ka_b2_reporting"),
        _unit("B2",2,"ზმნის არგუმენტული სტრუქტურა",["ka-b2-version-system"],"ka_b2_verbs"),
        _unit("B2",3,"რთული წინადადებები",["ka-b2-subordination"],"ka_b2_syntax"),
        _unit("B2",4,"ოფიციალური კომუნიკაცია",["ka-b2-formal"],"ka_b2_professional"),
        _unit("B2",5,"საზოგადოება და მედია",["ka-b2-subordination"],"ka_b2_society"),
        _unit("B2",6,"B2 მიმოხილვა",["ka-b2-indirect-speech","ka-b2-formal"],"ka_b2_review"),
    ],
    "C1": [
        _unit("C1",1,"აკადემიური და ოფიციალური წერა",["ka-c1-nominalisation"],"ka_c1_formal"),
        _unit("C1",2,"არგუმენტი და მტკიცებულება",["ka-c1-hedging"],"ka_c1_argument"),
        _unit("C1",3,"ტონი და პრაგმატიკა",["ka-c1-pragmatics"],"ka_c1_pragmatics"),
        _unit("C1",4,"კულტურა და საზოგადოება",["ka-c1-hedging"],"ka_c1_culture"),
        _unit("C1",5,"კვლევა და საჯარო სფერო",["ka-c1-nominalisation"],"ka_c1_public"),
        _unit("C1",6,"C1 მიმოხილვა",["ka-c1-nominalisation","ka-c1-hedging"],"ka_c1_review"),
    ],
    "C2": [
        _unit("C2",1,"რთული სინტაქსი",["ka-c2-advanced-syntax"],"ka_c2_syntax"),
        _unit("C2",2,"რიტორიკა და სტილი",["ka-c2-rhetoric"],"ka_c2_rhetoric"),
        _unit("C2",3,"კრიტიკული ანალიზი",["ka-c1-hedging"],"ka_c2_analysis"),
        _unit("C2",4,"ნიუანსი და კომუნიკაციური მიზანი",["ka-c1-pragmatics"],"ka_c2_nuance"),
        _unit("C2",5,"აკადემიური ოსტატობა",["ka-c2-advanced-syntax"],"ka_c2_academic"),
        _unit("C2",6,"ქართული ენის სრულყოფა",["ka-c2-advanced-syntax","ka-c2-rhetoric"],"ka_c2_mastery"),
    ],
}

def _vset(id_, level, topic, unit_ref, words):
    return VocabularySet(id=id_, level=level, topic=topic, unit_ref=unit_ref,
        words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS = [
    _vset("ka_a1_social","A1","მისალმება","ka-a1-unit-1",[
        ("გამარჯობა","phrase","hello","გამარჯობა! როგორ ხარ?"),("დილა მშვიდობისა","phrase","good morning","დილა მშვიდობისა!"),("მადლობა","phrase","thank you","დიდი მადლობა."),("გთხოვთ","phrase","please","ერთი ყავა, გთხოვთ."),("ნახვამდის","phrase","goodbye","ნახვამდის!"),("ბოდიში","phrase","sorry/excuse me","ბოდიში, სად არის სადგური?")]),
    _vset("ka_a1_family","A1","ოჯახი და იდენტობა","ka-a1-unit-2",[
        ("სახელი","noun","name","რა გქვია?"),("ოჯახი","noun","family","ჩემი ოჯახი დიდია."),("დედა","noun","mother","დედა სახლშია."),("მამა","noun","father","მამა მუშაობს."),("ძმა","noun","brother","ჩემი ძმა სტუდენტია."),("და","noun","sister","ჩემი და აქ არის.")]),
    _vset("ka_a1_home","A1","სახლი და ადგილები","ka-a1-unit-3",[
        ("სახლი","noun","house","სახლში ვარ."),("ოთახი","noun","room","ოთახი დიდია."),("კარი","noun","door","კარი ღიაა."),("მაგიდა","noun","table","წიგნი მაგიდაზეა."),("ქალაქი","noun","city","ქალაქში ვცხოვრობ."),("ქუჩა","noun","street","ეს ქუჩა მშვიდია.")]),
    _vset("ka_a1_questions","A1","კითხვები","ka-a1-unit-4",[
        ("ვინ","pronoun","who","ვინ არის ის?"),("რა","pronoun","what","რა გინდა?"),("სად","adverb","where","სად ცხოვრობ?"),("როდის","adverb","when","როდის მოხვალ?"),("როგორ","adverb","how","როგორ ხარ?"),("რამდენი","quantifier","how many","რამდენი წლის ხარ?")]),
    _vset("ka_a1_routine","A1","ყოველდღიურობა","ka-a1-unit-5",[
        ("დილა","noun","morning","დილით ვმუშაობ."),("სამუშაო","noun","work","სამუშაო მაქვს."),("სკოლა","noun","school","სკოლაში მივდივარ."),("სწავლა","noun","study","სწავლა მიყვარს."),("დღეს","adverb","today","დღეს სახლში ვარ."),("ახლა","adverb","now","ახლა ვკითხულობ.")]),
    _vset("ka_a1_food","A1","საკვები","ka-a1-unit-6",[
        ("პური","noun","bread","პური მინდა."),("წყალი","noun","water","წყალი მინდა."),("რძე","noun","milk","რძე ცივია."),("ყავა","noun","coffee","ყავას ვსვამ."),("ვაშლი","noun","apple","ვაშლი გემრიელია."),("ბოსტნეული","noun","vegetables","ბოსტნეული სასარგებლოა.")]),
    _vset("ka_a2_past","A2","წარსული","ka-a2-unit-1",[
        ("გუშინ","adverb","yesterday","გუშინ სახლში ვიყავი."),("წავედი","verb","I went","გუშინ სამსახურში წავედი."),("ვნახე","verb","I saw","ფილმი ვნახე."),("ვიყიდე","verb","I bought","წიგნი ვიყიდე."),("შევხვდი","verb","I met","მეგობარს შევხვდი."),("გამოცდილება","noun","experience","კარგი გამოცდილება იყო.")]),
    _vset("ka_a2_future","A2","მომავალი","ka-a2-unit-2",[
        ("ხვალ","adverb","tomorrow","ხვალ წავალ."),("მომავალი","noun","future","მომავალი მნიშვნელოვანია."),("გეგმა","noun","plan","გეგმა მაქვს."),("დავურეკავ","verb","I will call","საღამოს დაგირეკავ."),("მოგზაურობა","noun","trip","მომავალ კვირას მოგზაურობა მაქვს."),("იმედი","noun","hope","იმედი მაქვს.")]),
    _vset("ka_a2_cases","A2","ბრუნვები","ka-a2-unit-3",[
        ("მეგობრის","form","of a friend","ეს ჩემი მეგობრის წიგნია."),("მეგობარს","form","to a friend","მეგობარს ველაპარაკები."),("ავტობუსით","form","by bus","ავტობუსით მივდივარ."),("სახლიდან","form","from the house","სახლიდან მოვედი."),("ქალაქში","form","in the city","ქალაქში ვცხოვრობ."),("სკოლასთან","form","near the school","სკოლასთან შევხვდით.")]),
    _vset("ka_a2_comparison","A2","აღწერა და შედარება","ka-a2-unit-4",[
        ("დიდი","adjective","big","ეს სახლი დიდია."),("პატარა","adjective","small","ეს ოთახი პატარაა."),("უფრო კარგი","phrase","better","ეს ვარიანტი უფრო კარგია."),("საუკეთესო","adjective","best","ეს საუკეთესო არჩევანია."),("იაფი","adjective","cheap","ეს უფრო იაფია."),("ძვირი","adjective","expensive","ეს ძალიან ძვირია.")]),
    _vset("ka_a2_travel","A2","მოგზაურობა","ka-a2-unit-5",[
        ("სადგური","noun","station","სადგური სად არის?"),("ბილეთი","noun","ticket","ერთი ბილეთი მინდა."),("აეროპორტი","noun","airport","აეროპორტში მივდივარ."),("მატარებელი","noun","train","მატარებელი მალე მოვა."),("მიმართულება","noun","direction","სწორი მიმართულებაა."),("მანძილი","noun","distance","მანძილი დიდია.")]),
    _vset("ka_a2_review","A2","ყოველდღიური კომუნიკაცია","ka-a2-unit-6",[
        ("კითხვა","noun","question","ერთი კითხვა მაქვს."),("პასუხი","noun","answer","ეს პასუხია."),("განმარტება","noun","explanation","განმარტება მჭირდება."),("შესაძლებლობა","noun","opportunity","კარგი შესაძლებლობაა."),("გადაწყვეტილება","noun","decision","გადაწყვეტილება მივიღეთ."),("ბედნიერი","adjective","happy","ძალიან ბედნიერი ვარ.")]),
    _vset("ka_b1_verbs","B1","ზმნის სისტემა","ka-b1-unit-1",[
        ("ვკითხულობ","verb","I read/am reading","ყოველ საღამოს ვკითხულობ."),("წავიკითხე","verb","I read/have read","წიგნი წავიკითხე."),("ვწერ","verb","I write","სტატიას ვწერ."),("დავწერე","verb","I wrote","გუშინ დავწერე."),("ვაკეთებ","verb","I do","სამუშაოს ვაკეთებ."),("გავაკეთე","verb","I did","დავალება გავაკეთე.")]),
    _vset("ka_b1_relations","B1","ურთიერთობები","ka-b1-unit-2",[
        ("რომელიც","relative","which/who","ადამიანი, რომელიც აქ ცხოვრობს..."),("ურთიერთობა","noun","relationship","კარგი ურთიერთობა გვაქვს."),("კავშირი","noun","connection","ამ ორ საკითხს კავშირი აქვს."),("პასუხისმგებლობა","noun","responsibility","პასუხისმგებლობა ავიღე."),("თანამშრომლობა","noun","cooperation","თანამშრომლობა მნიშვნელოვანია."),("მიზანი","noun","goal","მიზანი ნათელია.")]),
    _vset("ka_b1_conditions","B1","პირობები","ka-b1-unit-3",[
        ("თუ","conjunction","if","თუ დრო მექნება, მოვალ."),("რომ მცოდნოდა","phrase","if I had known","რომ მცოდნოდა, გეტყოდი."),("პირობა","noun","condition","ეს მნიშვნელოვანი პირობაა."),("შესაძლოა","adverb","possibly","შესაძლოა ხვალ მოვიდეს."),("ალბათ","adverb","probably","ალბათ მართალია."),("შემთხვევა","noun","case/occasion","ასეთი შემთხვევა იშვიათია.")]),
    _vset("ka_b1_argument","B1","მოსაზრება და არგუმენტი","ka-b1-unit-4",[
        ("მაგრამ","conjunction","but","მინდა, მაგრამ დრო არ მაქვს."),("ამიტომ","connector","therefore","წვიმდა, ამიტომ დავრჩი."),("რადგან","conjunction","because","დავრჩი, რადგან წვიმდა."),("თუმცა","conjunction","although/however","თუმცა რთულია, შესაძლებელია."),("მოსაზრება","noun","opinion","ჩემი მოსაზრება ასეთია."),("მიზეზი","noun","reason","ამის მიზეზი უცნობია.")]),
    _vset("ka_b1_work","B1","სამუშაო და სწავლა","ka-b1-unit-5",[
        ("შეხვედრა","noun","meeting","შეხვედრა ათ საათზეა."),("პროექტი","noun","project","პროექტი მიმდინარეობს."),("კვლევა","noun","research","კვლევა გრძელდება."),("უნარი","noun","skill","ეს მნიშვნელოვანი უნარია."),("შედეგი","noun","result","შედეგი კარგია."),("გამოცდილება","noun","experience","მუშაობის გამოცდილება მაქვს.")]),
    _vset("ka_b1_discussion","B1","დისკუსია","ka-b1-unit-6",[
        ("არგუმენტი","noun","argument","არგუმენტი დამაჯერებელია."),("მტკიცებულება","noun","evidence","მტკიცებულება საჭიროა."),("მაგალითი","noun","example","ეს კარგი მაგალითია."),("თვალსაზრისი","noun","viewpoint","სხვა თვალსაზრისიც არსებობს."),("შეთანხმება","noun","agreement","შეთანხმებას მივაღწიეთ."),("კამათი","noun","debate/argument","კამათი გაგრძელდა.")]),
    _vset("ka_b2_reporting","B2","გადმოცემა","ka-b2-unit-1",[
        ("თქვა","verb","said","მან თქვა, რომ მოვა."),("ჰკითხა","verb","asked","მან ჰკითხა, სად ვიყავი."),("განცხადება","noun","statement","განცხადება გამოქვეყნდა."),("წყარო","noun","source","წყარო უნდა გადავამოწმოთ."),("ანგარიში","noun","report","ანგარიში წავიკითხე."),("ინფორმაცია","noun","information","დამატებითი ინფორმაცია გვჭირდება.")]),
    _vset("ka_b2_verbs","B2","ზმნის სტრუქტურა","ka-b2-unit-2",[
        ("მივეცი","verb","I gave","მას წიგნი მივეცი."),("მოეწონა","verb","liked","მას ფილმი მოეწონა."),("დავეხმარე","verb","I helped","მეგობარს დავეხმარე."),("ვაჩვენე","verb","I showed","მას ფოტო ვაჩვენე."),("მთხოვა","verb","asked me","მან დახმარება მთხოვა."),("გადაწყვეტა","noun","solution","პრობლემის გადაწყვეტა ვიპოვეთ.")]),
    _vset("ka_b2_syntax","B2","რთული სინტაქსი","ka-b2-unit-3",[
        ("მიუხედავად იმისა, რომ","conjunction","although","მიუხედავად იმისა, რომ გვიან იყო, დარჩა."),("როცა","conjunction","when","როცა მოვედი, ეძინა."),("სანამ","conjunction","until/before","სანამ მოხვალ, დაველოდები."),("იმიტომ რომ","conjunction","because","დავრჩი, იმიტომ რომ წვიმდა."),("მაშინაც კი თუ","conjunction","even if","მოვალ მაშინაც კი თუ გვიანი იქნება."),("შედეგად","connector","as a result","შედეგად, მდგომარეობა შეიცვალა.")]),
    _vset("ka_b2_professional","B2","ოფიციალური ენა","ka-b2-unit-4",[
        ("გთხოვთ გაითვალისწინოთ","phrase","please take into account","გთხოვთ გაითვალისწინოთ აღნიშნული საკითხი."),("ანგარიშის მიხედვით","phrase","according to the report","ანგარიშის მიხედვით, საჭიროა კვლევა."),("რეკომენდაცია","noun","recommendation","რეკომენდაცია წარმოდგენილია."),("პოლიტიკა","noun","policy","პოლიტიკა განახლდა."),("განხილვა","noun","consideration/discussion","საკითხის განხილვა დაიწყო."),("მოთხოვნა","noun","requirement/request","მოთხოვნა დაკმაყოფილდა.")]),
    _vset("ka_b2_society","B2","საზოგადოება და მედია","ka-b2-unit-5",[
        ("საზოგადოება","noun","society","საზოგადოება იცვლება."),("საზოგადოებრივი","adjective","public/social","საზოგადოებრივი ინტერესი მნიშვნელოვანია."),("გარემო","noun","environment","გარემოს დაცვა საჭიროა."),("განათლება","noun","education","განათლება მნიშვნელოვანია."),("მედია","noun","media","მედია ინფორმაციას ავრცელებს."),("რესურსი","noun","resource","რესურსები შეზღუდულია.")]),
    _vset("ka_b2_review","B2","B2 მიმოხილვა","ka-b2-unit-6",[
        ("რთული","adjective","complex","ეს რთული საკითხია."),("ზუსტი","adjective","accurate","ზუსტი ინფორმაცია საჭიროა."),("სანდო","adjective","reliable","სანდო წყაროა."),("შესაბამისი","adjective","relevant/appropriate","შესაბამისი ინფორმაცია ვიპოვეთ."),("თანმიმდევრული","adjective","consistent","ტექსტი თანმიმდევრულია."),("დეტალური","adjective","detailed","დეტალური ანგარიშია.")]),
    _vset("ka_c1_formal","C1","ფორმალური წერა","ka-c1-unit-1",[
        ("განხორციელება","noun","implementation","პოლიტიკის განხორციელება შეფასდა."),("შეფასება","noun","assessment","შეფასება დასრულდა."),("მნიშვნელოვანი","adjective","significant","მნიშვნელოვანი ცვლილება მოხდა."),("მიდგომა","noun","approach","ახალი მიდგომა შემუშავდა."),("პრინციპი","noun","principle","ეს ძირითადი პრინციპია."),("მოთხოვნა","noun","requirement","მოთხოვნების შესრულება აუცილებელია.")]),
    _vset("ka_c1_argument","C1","აკადემიური არგუმენტი","ka-c1-unit-2",[
        ("სავარაუდოდ","adverb","probably","სავარაუდოდ, სხვა ფაქტორებმაც იმოქმედა."),("შეიძლება ითქვას","expression","it can be said","შეიძლება ითქვას, რომ შედეგი დადებითია."),("დაფუძნებული","adjective","based","მონაცემებზე დაფუძნებული შეფასება."),("ინტერპრეტაცია","noun","interpretation","სხვა ინტერპრეტაციაც შესაძლებელია."),("ჰიპოთეზა","noun","hypothesis","ჰიპოთეზა უნდა შემოწმდეს."),("დასკვნა","noun","conclusion","დასკვნა მტკიცებულებებს ეყრდნობა.")]),
    _vset("ka_c1_pragmatics","C1","პრაგმატიკა და ნიუანსი","ka-c1-unit-3",[
        ("ქვეტექსტი","noun","subtext","ქვეტექსტი მნიშვნელოვანია."),("ტონი","noun","tone","ტონი ოფიციალურია."),("თავაზიანი","adjective","polite","თავაზიანი პასუხი გასცა."),("შესაბამისი","adjective","appropriate","ტონი შესაბამისია."),("ნიუანსი","noun","nuance","მნიშვნელოვანი ნიუანსია."),("განმარტება","noun","clarification","დამატებითი განმარტება საჭიროა.")]),
    _vset("ka_c1_culture","C1","კულტურა და საზოგადოება","ka-c1-unit-4",[
        ("მემკვიდრეობა","noun","heritage","კულტურული მემკვიდრეობა დაცულია."),("ტრადიცია","noun","tradition","ტრადიცია გრძელდება."),("იდენტობა","noun","identity","ენობრივი იდენტობა მნიშვნელოვანია."),("მრავალფეროვნება","noun","diversity","მრავალფეროვნება საზოგადოების ძალაა."),("კულტურული","adjective","cultural","კულტურული კონტექსტი მნიშვნელოვანია."),("თანამედროვეობა","noun","modernity","ტრადიცია და თანამედროვეობა ერთმანეთს ხვდება.")]),
    _vset("ka_c1_public","C1","საჯარო სფერო","ka-c1-unit-5",[
        ("მმართველობა","noun","governance","ეფექტიანი მმართველობა მნიშვნელოვანია."),("ანგარიშვალდებულება","noun","accountability","ანგარიშვალდებულება აუცილებელია."),("გამჭვირვალობა","noun","transparency","გამჭვირვალობა ნდობას ზრდის."),("მონაწილეობა","noun","participation","საზოგადოების მონაწილეობა საჭიროა."),("სტრატეგია","noun","strategy","გრძელვადიანი სტრატეგია შეიქმნა."),("რეფორმა","noun","reform","რეფორმა ეტაპობრივად მიმდინარეობს.")]),
    _vset("ka_c1_review","C1","C1 მიმოხილვა","ka-c1-unit-6",[
        ("ზუსტი","adjective","precise","ზუსტი ფორმულირება მნიშვნელოვანია."),("ორაზროვანი","adjective","ambiguous","განცხადება ორაზროვანია."),("კრიტიკული","adjective","critical","კრიტიკული ანალიზი საჭიროა."),("დამოუკიდებელი","adjective","independent","დამოუკიდებელი შეფასება ჩატარდა."),("სანდოობა","noun","reliability","მონაცემების სანდოობა შემოწმდა."),("სიზუსტე","noun","accuracy","სიზუსტე მნიშვნელოვანია.")]),
    _vset("ka_c2_syntax","C2","რთული სინტაქსი","ka-c2-unit-1",[
        ("ის, რაც","relative phrase","that which","ის, რაც მნიშვნელოვანია, უნდა განვიხილოთ."),("მიუხედავად ამისა","connector","nevertheless","მიუხედავად ამისა, შედეგი დადებითი იყო."),("იმის მიუხედავად, რომ","conjunction","despite the fact that","იმის მიუხედავად, რომ რთულია, შესაძლებელია."),("საბოლოო ჯამში","connector","ultimately","საბოლოო ჯამში, გადაწყვეტილება მიღებულია."),("ცალკეულად","adverb","individually","ფაქტორები ცალკეულად უნდა შეფასდეს."),("საჭიროების შემთხვევაში","phrase","if necessary","საჭიროების შემთხვევაში, დამატებითი კვლევა ჩატარდება.")]),
    _vset("ka_c2_rhetoric","C2","რიტორიკა","ka-c2-unit-2",[
        ("ერთი მხრივ","connector","on the one hand","ერთი მხრივ, ეს ეფექტიანია."),("მეორე მხრივ","connector","on the other hand","მეორე მხრივ, რისკებიც არსებობს."),("არა მხოლოდ","connector","not only","არა მხოლოდ შედეგი, არამედ პროცესიც მნიშვნელოვანია."),("საბოლოო ჯამში","connector","in the end","საბოლოო ჯამში, არჩევანი ღირებულებებს ეხება."),("ხაზგასმა","noun","emphasis","საჭიროა ერთი საკითხის ხაზგასმა."),("ფართო კონტექსტი","noun phrase","broader context","ფართო კონტექსტი უნდა გავითვალისწინოთ.")]),
    _vset("ka_c2_analysis","C2","კრიტიკული ანალიზი","ka-c2-unit-3",[
        ("კონტრპოზიცია","noun","counter-position","კონტრპოზიცია უნდა განვიხილოთ."),("ვარაუდი","noun","assumption","ეს ვარაუდი უნდა შემოწმდეს."),("მტკიცებულება","noun","evidence","მტკიცებულება საკმარისი არ არის."),("კონტექსტი","noun","context","კონტექსტის გარეშე დასკვნა სუსტია."),("მასშტაბი","noun","scope/scale","კვლევის მასშტაბი შეზღუდულია."),("მიზეზობრიობა","noun","causality","კორელაცია მიზეზობრიობას არ ნიშნავს.")]),
    _vset("ka_c2_nuance","C2","ნიუანსი","ka-c2-unit-4",[
        ("ქვეტექსტი","noun","subtext","ტექსტის ქვეტექსტი მნიშვნელოვანია."),("ირონია","noun","irony","ირონია კონტექსტზეა დამოკიდებული."),("დამოკიდებულება","noun","stance/attitude","ავტორის დამოკიდებულება მკაფიოა."),("შერბილება","noun","mitigation","შერბილება თავაზიანობას ზრდის."),("ფორმალურობა","noun","formality","ფორმალურობის დონე შეიცვალა."),("ადაპტირება","verb","adapt","სტილი აუდიტორიას უნდა მოერგოს.")]),
    _vset("ka_c2_academic","C2","აკადემიური ოსტატობა","ka-c2-unit-5",[
        ("მეთოდოლოგია","noun","methodology","მეთოდოლოგია დეტალურადაა აღწერილი."),("კორელაცია","noun","correlation","კორელაცია მაღალია."),("შეზღუდვა","noun","limitation","კვლევას რამდენიმე შეზღუდვა აქვს."),("რეპრეზენტატიული","adjective","representative","ნიმუში რეპრეზენტატიული უნდა იყოს."),("სინთეზი","noun","synthesis","წყაროების სინთეზი გაკეთდა."),("დასაბუთება","noun","justification","დასკვნის დასაბუთება საჭიროა.")]),
    _vset("ka_c2_mastery","C2","ენის სრულყოფა","ka-c2-unit-6",[
        ("სიზუსტე","noun","precision","ენის სიზუსტე მაღალია."),("მოქნილობა","noun","flexibility","სტილისტური მოქნილობა მნიშვნელოვანია."),("თავისუფლად","adverb","fluently/freely","ქართულად თავისუფლად საუბრობს."),("ლექსიკური სიმდიდრე","noun phrase","lexical richness","ტექსტს ლექსიკური სიმდიდრე აქვს."),("განასხვავება","verb","distinguish","მნიშვნელობები უნდა განვასხვავოთ."),("ოსტატობა","noun","mastery","ტექსტი ენობრივ ოსტატობას აჩვენებს.")]),
]

PHRASEBOOK_CATEGORIES = [
    PhrasebookCategory(id="ka-a1-social",level="A1",situation="მისალმება",icon="💬",phrases=[
        PhrasebookEntry(text="გამარჯობა! როგორ ხარ?",context="greeting",register="neutral"),
        PhrasebookEntry(text="კარგად ვარ, მადლობა.",context="reply",register="neutral"),
        PhrasebookEntry(text="დილა მშვიდობისა!",context="morning",register="neutral"),
        PhrasebookEntry(text="ნახვამდის!",context="farewell",register="neutral"),
    ]),
    PhrasebookCategory(id="ka-a1-survival",level="A1",situation="ყოველდღიური საჭიროებები",icon="🧭",phrases=[
        PhrasebookEntry(text="სად არის ტუალეტი?",context="location",register="neutral"),
        PhrasebookEntry(text="დამეხმარეთ, გთხოვთ.",context="help",register="neutral"),
        PhrasebookEntry(text="ვერ გავიგე.",context="comprehension",register="neutral"),
        PhrasebookEntry(text="გთხოვთ, გაიმეორეთ.",context="clarification",register="neutral"),
    ]),
    PhrasebookCategory(id="ka-a2-shopping",level="A2",situation="შოპინგი",icon="🛍️",phrases=[
        PhrasebookEntry(text="რა ღირს?",context="price",register="neutral"),
        PhrasebookEntry(text="ეს მინდა.",context="purchase",register="neutral"),
        PhrasebookEntry(text="უფრო იაფი გაქვთ?",context="comparison",register="neutral"),
        PhrasebookEntry(text="ბარათით გადახდა შეიძლება?",context="payment",register="neutral"),
    ]),
    PhrasebookCategory(id="ka-a2-travel",level="A2",situation="მოგზაურობა",icon="🚌",phrases=[
        PhrasebookEntry(text="სადგური სად არის?",context="directions",register="neutral"),
        PhrasebookEntry(text="ერთი ბილეთი მინდა.",context="ticket",register="neutral"),
        PhrasebookEntry(text="როდის გადის მატარებელი?",context="schedule",register="neutral"),
        PhrasebookEntry(text="რამდენ ხანს გრძელდება გზა?",context="duration",register="neutral"),
    ]),
    PhrasebookCategory(id="ka-b1-work",level="B1",situation="სამუშაო და სწავლა",icon="💼",phrases=[
        PhrasebookEntry(text="ჩემი აზრით, ეს მნიშვნელოვანია.",context="opinion",register="neutral"),
        PhrasebookEntry(text="შეგვიძლია ეს საკითხი მოგვიანებით განვიხილოთ?",context="meeting",register="neutral"),
        PhrasebookEntry(text="დამატებითი ინფორმაცია მჭირდება.",context="information",register="neutral"),
        PhrasebookEntry(text="ამ საკითხზე ვეთანხმები.",context="agreement",register="neutral"),
    ]),
    PhrasebookCategory(id="ka-b2-professional",level="B2",situation="ოფიციალური კომუნიკაცია",icon="📄",phrases=[
        PhrasebookEntry(text="გთხოვთ, გაითვალისწინოთ აღნიშნული საკითხი.",context="formal_request",register="formal"),
        PhrasebookEntry(text="ანგარიშის მიხედვით, საჭიროა დამატებითი კვლევა.",context="reporting",register="formal"),
        PhrasebookEntry(text="გთხოვთ, მოგვაწოდოთ დამატებითი ინფორმაცია.",context="correspondence",register="formal"),
        PhrasebookEntry(text="მოხარული ვიქნები თქვენი პასუხის მიღებით.",context="closing",register="formal"),
    ]),
    PhrasebookCategory(id="ka-c1-discussion",level="C1",situation="აკადემიური დისკუსია",icon="🧠",phrases=[
        PhrasebookEntry(text="შეიძლება ითქვას, რომ ეს მიდგომა ეფექტიანია.",context="qualification",register="formal"),
        PhrasebookEntry(text="საკითხი უფრო ფართო კონტექსტში უნდა განვიხილოთ.",context="analysis",register="formal"),
        PhrasebookEntry(text="ეს დასკვნა დამატებით მტკიცებულებას მოითხოვს.",context="evidence",register="formal"),
        PhrasebookEntry(text="სხვა ინტერპრეტაციაც შესაძლებელია.",context="alternative",register="formal"),
    ]),
    PhrasebookCategory(id="ka-c2-rhetoric",level="C2",situation="რიტორიკა და სტილი",icon="✍️",phrases=[
        PhrasebookEntry(text="ერთი მხრივ, ეს მიდგომა ეფექტიანია.",context="opening_argument",register="formal"),
        PhrasebookEntry(text="მეორე მხრივ, არსებობს მნიშვნელოვანი რისკები.",context="contrast",register="formal"),
        PhrasebookEntry(text="საკითხი მხოლოდ ეკონომიკური კუთხით არ უნდა შეფასდეს.",context="qualification",register="formal"),
        PhrasebookEntry(text="საბოლოო ჯამში, გადაწყვეტილება ღირებულებებსა და პრიორიტეტებს ეხება.",context="conclusion",register="formal"),
    ]),
]

ASSESSMENT_BANK = [
    AssessmentQuestion(id="ka-a1-001",skill="communication",difficulty="A1",question="Which phrase means “Hello” in Georgian?",options=["გამარჯობა","მადლობა","ნახვამდის","გთხოვთ"],correct="გამარჯობა"),
    AssessmentQuestion(id="ka-a1-002",skill="grammar",difficulty="A1",question="Which sentence means “I am a student”?",options=["მე სტუდენტი ვარ.","მე სახლში ვარ.","მე არ ვმუშაობ.","ეს ჩემი წიგნია."],correct="მე სტუდენტი ვარ."),
    AssessmentQuestion(id="ka-a1-003",skill="vocabulary",difficulty="A1",question="Which word means “mother”?",options=["დედა","მამა","ძმა","და"],correct="დედა"),
    AssessmentQuestion(id="ka-a1-004",skill="grammar",difficulty="A1",question="Which sentence expresses possession?",options=["მე წიგნი მაქვს.","მე სახლში ვარ.","ის ექიმია.","სად ცხოვრობ?"],correct="მე წიგნი მაქვს."),
    AssessmentQuestion(id="ka-a2-001",skill="grammar",difficulty="A2",question="Which sentence describes a completed past event?",options=["გუშინ წავედი.","ხვალ წავალ.","ახლა ვკითხულობ.","სკოლაში მივდივარ."],correct="გუშინ წავედი."),
    AssessmentQuestion(id="ka-a2-002",skill="grammar",difficulty="A2",question="Which form means “by bus”?",options=["ავტობუსით","სახლიდან","ქალაქში","მეგობრის"],correct="ავტობუსით"),
    AssessmentQuestion(id="ka-a2-003",skill="vocabulary",difficulty="A2",question="Which word means “ticket”?",options=["ბილეთი","სადგური","მიმართულება","მანძილი"],correct="ბილეთი"),
    AssessmentQuestion(id="ka-b1-001",skill="grammar",difficulty="B1",question="Which sentence is conditional?",options=["თუ დრო მექნება, მოვალ.","გუშინ წავედი.","ახლა ვმუშაობ.","ხვალ მივდივარ."],correct="თუ დრო მექნება, მოვალ."),
    AssessmentQuestion(id="ka-b1-002",skill="grammar",difficulty="B1",question="Which word introduces a relative clause?",options=["რომელიც","მაგრამ","ამიტომ","ხვალ"],correct="რომელიც"),
    AssessmentQuestion(id="ka-b1-003",skill="discourse",difficulty="B1",question="Which connector means “therefore”?",options=["ამიტომ","რადგან","მაგრამ","თუმცა"],correct="ამიტომ"),
    AssessmentQuestion(id="ka-b2-001",skill="grammar",difficulty="B2",question="Which sentence reports what someone said?",options=["მან თქვა, რომ ხვალ მოვა.","ის ხვალ მოვა.","ის გუშინ მოვიდა.","ის ახლა მუშაობს."],correct="მან თქვა, რომ ხვალ მოვა."),
    AssessmentQuestion(id="ka-b2-002",skill="formal",difficulty="B2",question="Which phrase suits formal communication?",options=["გთხოვთ, გაითვალისწინოთ აღნიშნული საკითხი.","გამარჯობა!","რა ღირს?","ნახვამდის!"],correct="გთხოვთ, გაითვალისწინოთ აღნიშნული საკითხი."),
    AssessmentQuestion(id="ka-b2-003",skill="vocabulary",difficulty="B2",question="What does მტკიცებულება mean?",options=["evidence","family","station","tomorrow"],correct="evidence"),
    AssessmentQuestion(id="ka-c1-001",skill="writing",difficulty="C1",question="Which phrase appropriately qualifies a claim?",options=["შეიძლება ითქვას, რომ...","ეს ყოველთვის ასეა.","გამარჯობა!","ნახვამდის!"],correct="შეიძლება ითქვას, რომ..."),
    AssessmentQuestion(id="ka-c1-002",skill="analysis",difficulty="C1",question="Which Georgian word means “hypothesis”?",options=["ჰიპოთეზა","მემკვიდრეობა","სადგური","სამუშაო"],correct="ჰიპოთეზა"),
    AssessmentQuestion(id="ka-c1-003",skill="pragmatics",difficulty="C1",question="What is the purpose of hedging?",options=["To calibrate the strength of a claim","To greet someone","To ask a price","To form a plural"],correct="To calibrate the strength of a claim"),
    AssessmentQuestion(id="ka-c2-001",skill="discourse",difficulty="C2",question="Which connector means “on the other hand”?",options=["მეორე მხრივ","ერთი მხრივ","მადლობა","ხვალ"],correct="მეორე მხრივ"),
    AssessmentQuestion(id="ka-c2-002",skill="analysis",difficulty="C2",question="Which term means “correlation”?",options=["კორელაცია","ქვეტექსტი","ფორმალურობა","მემკვიდრეობა"],correct="კორელაცია"),
    AssessmentQuestion(id="ka-c2-003",skill="formal",difficulty="C2",question="Which phrase works as a formal conclusion?",options=["საბოლოო ჯამში...","გამარჯობა!","სად არის ტუალეტი?","წყალი მინდა."],correct="საბოლოო ჯამში..."),
]
