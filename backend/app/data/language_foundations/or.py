"""Odia A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

def _g(slug,title,level,summary,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS=[
_g("pronouns","Personal pronouns","A1","Use personal pronouns in everyday identity statements.",["ମୁଁ ଛାତ୍ର।","ଆପଣ ଶିକ୍ଷକ।"]),
_g("identity","Nominal identity and copular patterns","A1","Identify people and things in simple clauses.",["ସେ ଶିକ୍ଷକ।","ଏହା ଏକ ବହି।"]),
_g("present","Present and habitual actions","A1","Describe current and habitual actions.",["ମୁଁ ଓଡ଼ିଆ ପଢ଼େ।","ସେ ପ୍ରତିଦିନ କାମ କରେ।"]),
_g("questions","Question words","A1","Ask who, what, where, when and how.",["ଆପଣଙ୍କ ନାମ କଣ?","ଆପଣ କେଉଁଠି ଅଛନ୍ତି?"]),
_g("negation","Negation","A1","Form basic negative clauses.",["ମୁଁ ଯାଏ ନାହିଁ।","ଏହା ବହି ନୁହେଁ।"]),
_g("demonstratives","Demonstratives","A1","Point to nearby and distant things.",["ଏହା ମୋ ବହି।","ସେହିଟା ତାଙ୍କ ଘର।"]),
_g("possession","Possession","A1","Express ownership and relationships.",["ଏହା ମୋ ଘର।","ଏହା ରୀନାଙ୍କ ବହି।"]),
_g("location","Location and existence","A1","Say where people and objects are.",["ମୁଁ ଘରେ ଅଛି।","ବହିଟି ଟେବୁଲ ଉପରେ ଅଛି।"]),
_g("plural","Plurality and classifiers","A1","Talk about groups and quantities.",["ଛାତ୍ରମାନେ ଆସିଲେ।","ଦୁଇଟି ବହି ଅଛି।"]),
_g("case","Case markers and postpositions","A1","Use common case and relational markers.",["ମୁଁ ବନ୍ଧୁଙ୍କ ସହିତ ଯାଏ।","ସେ ଘରକୁ ଗଲା।"]),
_g("past","Past tense","A2","Describe completed past events.",["ମୁଁ ଗତକାଲି ବଜାରକୁ ଗଲି।","ସେ ଖାଇଲା।"]),
_g("future","Future and intention","A2","Express plans and future events.",["ମୁଁ କାଲି ଯିବି।","ଆମେ ପଢ଼ିବୁ।"]),
_g("progressive","Progressive aspect","A2","Describe actions in progress.",["ମୁଁ ଏବେ ପଢ଼ୁଛି।","ସେ ରୋଷେଇ କରୁଛି।"]),
_g("imperatives","Imperatives and polite requests","A2","Give instructions and make requests.",["ଦୟାକରି ବସନ୍ତୁ।","ଏଠାକୁ ଆସନ୍ତୁ।"]),
_g("comparatives","Comparison and degree","A2","Compare people and things.",["ଏହା ସେହିଟାଠାରୁ ବଡ଼।","ଏହା ଅଧିକ ଭଲ।"]),
_g("modality","Ability, necessity and desire","A2","Express ability, obligation and desire.",["ମୁଁ ଯାଇପାରିବି।","ମୋତେ ଯିବାକୁ ପଡ଼ିବ।"]),
_g("adverbs","Time, frequency and manner adverbs","A2","Place actions in time and describe frequency.",["ମୁଁ ପ୍ରତିଦିନ ପଢ଼େ।","ସେ ଶୀଘ୍ର ଆସିଲା।"]),
_g("motion","Motion and direction","A2","Describe movement toward and from places.",["ମୁଁ ସ୍କୁଲକୁ ଯାଉଛି।","ସେ ଘରରୁ ଆସିଲା।"]),
_g("conditional","Conditional clauses","B1","Express conditions and consequences.",["ଯଦି ବର୍ଷା ହୁଏ, ଆମେ ଘରେ ରହିବୁ।"]),
_g("relative","Relative clauses","B1","Modify nouns with relative clauses.",["ଯେଉଁ ବହିଟି ମୁଁ ପଢ଼ିଲି, ସେଟି ଭଲ।"]),
_g("cause_purpose","Cause and purpose","B1","Express reasons, causes and purposes.",["ମୁଁ ପଢ଼ିବା ପାଇଁ ଲାଇବ୍ରେରୀକୁ ଗଲି।"]),
_g("reported","Reported speech","B1","Report statements and questions.",["ସେ କହିଲା ଯେ ସେ ଆସିବ।"]),
_g("reflexive","Reflexive and reciprocal meaning","B1","Express self-directed and reciprocal actions.",["ସେ ନିଜକୁ ଦେଖିଲା।","ସେମାନେ ପରସ୍ପରକୁ ସାହାଯ୍ୟ କଲେ।"]),
_g("causative","Causative constructions","B1","Express causing or arranging an action.",["ଶିକ୍ଷକ ଛାତ୍ରମାନଙ୍କୁ ପଢ଼ାଇଲେ।"]),
_g("passive","Passive voice","B2","Focus on the affected participant.",["ଚିଠିଟି ଲେଖାଯାଇଛି।","ଘରଟି ତିଆରି କରାଯାଇଛି।"]),
_g("aspect","Aspect and event structure","B2","Distinguish completed, ongoing and habitual events.",["ସେ କାମ ସାରିଛି।","ସେ ଦୀର୍ଘ ସମୟ ଧରି ପଢ଼ୁଛି।"]),
_g("concession","Concession and contrast","B2","Express although, despite and contrast.",["ଯଦିଓ ବର୍ଷା ହେଉଥିଲା, ଆମେ ଗଲୁ।"]),
_g("connectors","Discourse connectors","B2","Organize sequence, cause, contrast and conclusion.",["ପ୍ରଥମେ ଯୋଜନା କରିବା। ତାପରେ କାମ ଆରମ୍ଭ କରିବା।"]),
_g("subordination","Complex subordination","B2","Combine clauses for time, condition and complement relations.",["ସେ ଆସିବା ପରେ ଆମେ ଆଲୋଚନା କଲୁ।"]),
_g("nominalization","Nominalization and formal style","C1","Turn processes into formal noun phrases.",["ଶିକ୍ଷାର ବିକାଶ ଆବଶ୍ୟକ।"]),
_g("hedging","Academic hedging","C1","Qualify claims and express degrees of certainty.",["ସମ୍ଭବତଃ ଏହାର ଅନ୍ୟ ଏକ କାରଣ ଥାଇପାରେ।"]),
_g("embedded","Embedded questions","C1","Embed questions inside formal statements.",["ମୁଁ ଜାଣିବାକୁ ଚାହେଁ ସେ କେଉଁଠି ଅଛି।"]),
_g("information","Information structure and focus","C1","Manage topic, focus and emphasis in longer prose.",["ଏହି ସମସ୍ୟାଟି ହିଁ ଆମେ ଆଲୋଚନା କରିବୁ।"]),
_g("formal","Formal and institutional Odia","C1","Use professional and administrative language.",["ଦୟାକରି ଆବଶ୍ୟକ ଦଲିଲଗୁଡ଼ିକ ଦାଖଲ କରନ୍ତୁ।"]),
_g("argumentation","Academic argumentation","C1","Present claims, evidence and counterarguments.",["ତଥ୍ୟ ଆଧାରରେ ଏହି ନିଷ୍କର୍ଷ ଯୁକ୍ତିସଙ୍ଗତ।"]),
_g("pragmatics","Politeness and pragmatic nuance","C2","Interpret indirectness and social meaning.",["ସମ୍ଭବ ହେଲେ, ଦୟାକରି ଏହାକୁ ପୁଣି ଯାଞ୍ଚ କରନ୍ତୁ।"]),
_g("register","Register shifting","C2","Shift between conversational, professional and academic styles.",["ପରିସ୍ଥିତି ଅନୁସାରେ ଭାଷାର ଶୈଳୀ ବଦଳିଯାଏ।"]),
_g("rhetoric","Rhetorical and literary style","C2","Use emphasis, contrast and figurative framing.",["ଏହା କେବଳ ସମସ୍ୟା ନୁହେଁ, ଏକ ସୁଯୋଗ ମଧ୍ୟ।"]),
_g("translation","Translation and paraphrase","C2","Preserve meaning, register and pragmatic force.",["ଅନୁବାଦରେ ମୂଳ ଅର୍ଥ ଓ ଶୈଳୀ ରକ୍ଷା କରିବା ଆବଶ୍ୟକ।"]),
_g("discourse_analysis","Discourse analysis","C2","Analyze cohesion, genre, audience and stance.",["ପାଠ୍ୟର ଅର୍ଥ ପରିପ୍ରେକ୍ଷିତ ଅନୁସାରେ ବଦଳିପାରେ।"])
]

def _v(id_,level,topic,ref,items):
    return VocabularySet(id=id_,level=level,topic=topic,unit_ref=ref,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS=[
_v("greetings_a1","A1","greetings","or-a1-unit-1",[("ନମସ୍କାର","phrase","hello","ନମସ୍କାର।"),("ଧନ୍ୟବାଦ","phrase","thank you","ଧନ୍ୟବାଦ।"),("ଦୟାକରି","adverb","please","ଦୟାକରି ଆସନ୍ତୁ।"),("ବିଦାୟ","noun","goodbye","ବିଦାୟ।")]),
_v("identity_a1","A1","identity","or-a1-unit-2",[("ନାମ","noun","name","ମୋ ନାମ ରବି।"),("ଛାତ୍ର","noun","student","ମୁଁ ଛାତ୍ର।"),("ଶିକ୍ଷକ","noun","teacher","ସେ ଶିକ୍ଷକ।"),("ବନ୍ଧୁ","noun","friend","ସେ ମୋ ବନ୍ଧୁ।")]),
_v("family_a1","A1","family","or-a1-unit-3",[("ମା","noun","mother","ମୋ ମା ଘରେ ଅଛନ୍ତି।"),("ବାପା","noun","father","ମୋ ବାପା କାମ କରନ୍ତି।"),("ଭାଇ","noun","brother","ମୋ ଭାଇ ସ୍କୁଲରେ ଅଛି।"),("ଭଉଣୀ","noun","sister","ମୋ ଭଉଣୀ ପଢ଼ୁଛି।")]),
_v("home_a1","A1","home","or-a1-unit-4",[("ଘର","noun","house","ଏହା ମୋ ଘର।"),("କୋଠରୀ","noun","room","ମୋ କୋଠରୀ ପରିଷ୍କାର।"),("ଦୁଆର","noun","door","ଦୁଆର ଖୋଲନ୍ତୁ।"),("ଟେବୁଲ","noun","table","ବହିଟି ଟେବୁଲ ଉପରେ ଅଛି।")]),
_v("routine_a1","A1","daily routine","or-a1-unit-5",[("ସକାଳ","noun","morning","ସକାଳେ ମୁଁ ପଢ଼େ।"),("କାମ","noun","work","ମୁଁ କାମ କରେ।"),("ପଢ଼ିବା","verb","study/read","ମୁଁ ପ୍ରତିଦିନ ପଢ଼େ।"),("ଶୋଇବା","verb","sleep","ମୁଁ ରାତିରେ ଶୋଏ।")]),
_v("food_a1","A1","food and drink","or-a1-unit-6",[("ପାଣି","noun","water","ମୋତେ ପାଣି ଦରକାର।"),("ଭାତ","noun","rice","ମୁଁ ଭାତ ଖାଏ।"),("ଦୁଧ","noun","milk","ସେ ଦୁଧ ପିଏ।"),("ଫଳ","noun","fruit","ମୁଁ ଫଳ ଖାଏ।")]),
_v("places_a1","A1","places and directions","or-a1-unit-7",[("ସ୍କୁଲ","noun","school","ସ୍କୁଲ ଏଠାରେ ଅଛି।"),("ବଜାର","noun","market","ମୁଁ ବଜାରକୁ ଯାଏ।"),("ଡାକ୍ତରଖାନା","noun","hospital","ଡାକ୍ତରଖାନା କେଉଁଠି?"),("ରାସ୍ତା","noun","road","ରାସ୍ତାଟି ଲମ୍ବା।")]),
_v("communication_a1","A1","communication","or-a1-unit-8",[("ସାହାଯ୍ୟ","noun","help","ମୋତେ ସାହାଯ୍ୟ ଦରକାର।"),("ଭାଷା","noun","language","ଓଡ଼ିଆ ଏକ ଭାଷା।"),("ପ୍ରଶ୍ନ","noun","question","ମୋର ଏକ ପ୍ରଶ୍ନ ଅଛି।"),("ଉତ୍ତର","noun","answer","ଉତ୍ତରଟି ସଠିକ।")]),
_v("travel_a2","A2","travel","or-a2-unit-1",[("ଯାତ୍ରା","noun","journey","ଆମର ଯାତ୍ରା ଆଜି ଆରମ୍ଭ ହେଲା।"),("ଟିକେଟ","noun","ticket","ମୁଁ ଟିକେଟ କିଣିଲି।"),("ଷ୍ଟେସନ","noun","station","ଷ୍ଟେସନ କେଉଁଠି?"),("ବସ","noun","bus","ବସ ଆସିଲା।")]),
_v("health_a2","A2","health","or-a2-unit-2",[("ସ୍ୱାସ୍ଥ୍ୟ","noun","health","ସ୍ୱାସ୍ଥ୍ୟ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ।"),("ଡାକ୍ତର","noun","doctor","ମୁଁ ଡାକ୍ତରଙ୍କୁ ଦେଖିଲି।"),("ଔଷଧ","noun","medicine","ମୋତେ ଔଷଧ ଦରକାର।"),("ବେଦନା","noun","pain","ମୋର ବେଦନା ଅଛି।")]),
_v("study_a2","A2","study","or-a2-unit-3",[("ପାଠ","noun","lesson","ଆଜିର ପାଠ ସହଜ।"),("ପରୀକ୍ଷା","noun","exam","ଆସନ୍ତାକାଲି ପରୀକ୍ଷା ଅଛି।"),("ବହି","noun","book","ମୁଁ ବହି ପଢ଼ୁଛି।"),("ଲେଖିବା","verb","write","ସେ ଉତ୍ତର ଲେଖୁଛି।")]),
_v("society_b1","B1","society","or-b1-unit-1",[("ସମାଜ","noun","society","ସମାଜର ବିକାଶ ଆବଶ୍ୟକ।"),("ସମୁଦାୟ","noun","community","ସମୁଦାୟ ଏକାଠି କାମ କରେ।"),("ଅଧିକାର","noun","right","ସମସ୍ତଙ୍କର ଅଧିକାର ଅଛି।"),("ଦାୟିତ୍ୱ","noun","responsibility","ଏହା ଆମର ଦାୟିତ୍ୱ।")]),
_v("work_b1","B1","work and projects","or-b1-unit-2",[("ଚାକିରି","noun","job","ମୋର ନୂଆ ଚାକିରି ଅଛି।"),("ପ୍ରକଳ୍ପ","noun","project","ପ୍ରକଳ୍ପଟି ଶେଷ ହେଲା।"),("ବୈଠକ","noun","meeting","ଆଜି ବୈଠକ ଅଛି।"),("ଯୋଜନା","noun","plan","ଆମର ଏକ ଯୋଜନା ଅଛି।")]),
_v("environment_b1","B1","environment","or-b1-unit-3",[("ପରିବେଶ","noun","environment","ଆମେ ପରିବେଶର ସୁରକ୍ଷା କରିବା।"),("ଜଙ୍ଗଲ","noun","forest","ଜଙ୍ଗଲ ସୁରକ୍ଷିତ ହେବା ଦରକାର।"),("ନଦୀ","noun","river","ନଦୀର ପାଣି ପରିଷ୍କାର।"),("ପ୍ରକୃତି","noun","nature","ପ୍ରକୃତି ଆମ ପାଇଁ ମୂଲ୍ୟବାନ।")]),
_v("economy_b2","B2","economy","or-b2-unit-1",[("ଅର୍ଥନୀତି","noun","economy","ଅର୍ଥନୀତିରେ ପରିବର୍ତ୍ତନ ହେଉଛି।"),("ବ୍ୟବସାୟ","noun","business","ସେ ଏକ ବ୍ୟବସାୟ ଚଳାନ୍ତି।"),("ନିବେଶ","noun","investment","ନିବେଶ ବଢ଼ୁଛି।"),("ମୂଲ୍ୟ","noun","value/price","ବସ୍ତୁର ମୂଲ୍ୟ ବଢ଼ିଛି।")]),
_v("governance_b2","B2","governance","or-b2-unit-2",[("ପ୍ରଶାସନ","noun","administration","ପ୍ରଶାସନ ନୂଆ ନିୟମ ଜାରି କଲା।"),("ନୀତି","noun","policy","ନୂଆ ନୀତି ଘୋଷଣା ହେଲା।"),("ନିୟମ","noun","rule","ନିୟମ ପାଳନ କରିବା ଦରକାର।"),("ନିଷ୍ପତ୍ତି","noun","decision","ନିଷ୍ପତ୍ତି ନିଆଯାଇଛି।")]),
_v("media_b2","B2","media","or-b2-unit-3",[("ସମ୍ବାଦ","noun","news","ସମ୍ବାଦଟି ଆଜି ପ୍ରକାଶିତ ହେଲା।"),("ସମ୍ବାଦପତ୍ର","noun","newspaper","ମୁଁ ସମ୍ବାଦପତ୍ର ପଢ଼େ।"),("ସାକ୍ଷାତକାର","noun","interview","ସାକ୍ଷାତକାରଟି ଆଜି ପ୍ରସାରିତ ହେଲା।"),("ପ୍ରତିବେଦନ","noun","report","ପ୍ରତିବେଦନ ଦାଖଲ ହେଲା।")]),
_v("academic_c1","C1","academic language","or-c1-unit-1",[("ଗବେଷଣା","noun","research","ଗବେଷଣା ଚାଲିଛି।"),("ପ୍ରମାଣ","noun","evidence","ଏହି ପ୍ରମାଣ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ।"),("ବିଶ୍ଳେଷଣ","noun","analysis","ବିଶ୍ଳେଷଣରେ ନୂଆ ତଥ୍ୟ ମିଳିଲା।"),("ନିଷ୍କର୍ଷ","noun","conclusion","ନିଷ୍କର୍ଷଟି ତଥ୍ୟ ଉପରେ ଆଧାରିତ।")]),
_v("professional_c1","C1","professional language","or-c1-unit-2",[("ଦଲିଲ","noun","document","ଦଲିଲଗୁଡ଼ିକ ଦାଖଲ କରନ୍ତୁ।"),("ଆବେଦନ","noun","application","ଆବେଦନଟି ଗ୍ରହଣ କରାଯାଇଛି।"),("ନିର୍ଦ୍ଦେଶ","noun","instruction","ନିର୍ଦ୍ଦେଶ ଅନୁସରଣ କରନ୍ତୁ।"),("ସେବା","noun","service","ସେବାର ଗୁଣବତ୍ତା ଉନ୍ନତ ହେଲା।")]),
_v("abstract_c1","C1","abstract concepts","or-c1-unit-3",[("ପ୍ରଭାବ","noun","effect","ଏହାର ପ୍ରଭାବ ଦୀର୍ଘକାଳୀନ।"),("ଲକ୍ଷ୍ୟ","noun","objective","ଆମର ଲକ୍ଷ୍ୟ ସ୍ପଷ୍ଟ।"),("ସମାଧାନ","noun","solution","ଆମେ ଏକ ସମାଧାନ ଖୋଜୁଛୁ।"),("ପରିଣାମ","noun","result","ପରିଣାମ ଆଶାଜନକ।")]),
_v("culture_c2","C2","culture","or-c2-unit-1",[("ଐତିହ୍ୟ","noun","heritage","ଐତିହ୍ୟର ସୁରକ୍ଷା ଆବଶ୍ୟକ।"),("ପରମ୍ପରା","noun","tradition","ପରମ୍ପରା ପିଢ଼ିରୁ ପିଢ଼ିକୁ ଯାଏ।"),("ସଂସ୍କୃତି","noun","culture","ସଂସ୍କୃତି ଆମର ପରିଚୟ।"),("ଦୃଷ୍ଟିକୋଣ","noun","perspective","ତାଙ୍କ ଦୃଷ୍ଟିକୋଣ ଭିନ୍ନ।")]),
_v("discourse_c2","C2","discourse and translation","or-c2-unit-2",[("ବକ୍ତବ୍ୟ","noun","statement/discourse","ବକ୍ତବ୍ୟଟି ସ୍ପଷ୍ଟ।"),("ପ୍ରସଙ୍ଗ","noun","context","ପ୍ରସଙ୍ଗ ବୁଝିବା ଆବଶ୍ୟକ।"),("ଭାବାର୍ଥ","noun","meaning","ଭାବାର୍ଥ ଅନୁବାଦରେ ରକ୍ଷା କରାଯିବା ଦରକାର।"),("ଶୈଳୀ","noun","style","ଲେଖକଙ୍କ ଶୈଳୀ ବିଶିଷ୍ଟ।")])
]

def _p(id_,level,situation,items,register="neutral"):
    return PhrasebookCategory(id=id_,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=register) for t,c in items])

PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","A1","greetings",[("ନମସ୍କାର।","hello"),("ଆପଣ କେମିତି ଅଛନ୍ତି?","asking how someone is"),("ମୋ ନାମ ...","introducing yourself")]),
_p("thanks_a1","A1","thanks",[("ଧନ୍ୟବାଦ।","thank you"),("ବହୁତ ଧନ୍ୟବାଦ।","thank you very much"),("କିଛି ନାହିଁ।","you are welcome")]),
_p("shopping_a1","A1","shopping",[("ଏହା କେତେ?","asking price"),("ମୋତେ ଏହା ଦରକାର।","asking for an item"),("ଦାମ କମ କରିପାରିବେ କି?","asking for a lower price")]),
_p("directions_a1","A1","directions",[("ବଜାର କେଉଁଠି?","asking location"),("ସ୍କୁଲକୁ କିପରି ଯିବି?","asking how to get somewhere"),("ଡାହାଣ କି ବାମ?","checking direction")]),
_p("help_a1","A1","help",[("ଦୟାକରି ମୋତେ ସାହାଯ୍ୟ କରନ୍ତୁ।","asking for help"),("ମୁଁ ବୁଝିପାରୁନାହିଁ।","saying you do not understand"),("ଦୟାକରି ପୁଣି କୁହନ୍ତୁ।","asking for repetition")]),
_p("travel_a2","A2","travel",[("ଷ୍ଟେସନ କେଉଁଠି?","asking for station"),("ଟିକେଟ କେତେ?","asking ticket price"),("ମୁଁ କେଉଁଠି ଓହ୍ଲାଇବି?","asking where to get off")]),
_p("health_a2","A2","health",[("ମୋ ଦେହ ଭଲ ଲାଗୁନାହିଁ।","saying you feel unwell"),("ମୋତେ ଡାକ୍ତର ଦରକାର।","asking for a doctor"),("ମୋତେ ଔଷଧ ଦରକାର।","asking for medicine")]),
_p("study_b1","B1","study",[("ଏହାର ଅର୍ଥ କଣ?","asking meaning"),("ଦୟାକରି ବୁଝାନ୍ତୁ।","asking for explanation"),("ପୁଣି କହିପାରିବେ କି?","asking for repetition")]),
_p("work_b1","B1","work",[("ଆମେ ଏହି ବିଷୟ ଆଲୋଚନା କରିବା।","starting a discussion"),("ମୋର ଏକ ପ୍ରସ୍ତାବ ଅଛି।","making a suggestion"),("ମୁଁ ଏଥିରେ ସହମତ।","agreeing")]),
_p("formal_b2","B2","formal communication",[("ଦୟାକରି ଆବଶ୍ୟକ ଦଲିଲ ଦାଖଲ କରନ୍ତୁ।","formal instruction"),("ଏହି ବିଷୟରେ ସୂଚିତ କରାଯାଉଛି।","formal notice"),("ଆପଣଙ୍କ ସହଯୋଗ ପାଇଁ ଧନ୍ୟବାଦ।","formal thanks")],"formal"),
_p("academic_c1","C1","academic discussion",[("ତଥ୍ୟ ଅନୁସାରେ...","introducing evidence"),("ସମ୍ଭବତଃ...","hedging a claim"),("ଅନ୍ୟ ପକ୍ଷରେ...","introducing contrast")],"academic"),
_p("presentation_c1","C1","presentation",[("ପ୍ରଥମେ, ଆମେ ଦେଖିବା...","opening"),("ମୁଖ୍ୟ ବିଷୟ ହେଉଛି...","highlighting"),("ଶେଷରେ...","closing")],"formal"),
_p("pragmatics_c2","C2","pragmatic nuance",[("ସମ୍ଭବ ହେଲେ, ଦୟାକରି...","softening a request"),("ଆପଣଙ୍କ ମତ ବୁଝୁଛି, କିନ୍ତୁ...","polite disagreement"),("ଏହାକୁ ଅନ୍ୟ ଭାବରେ ଭାବିପାରିବା।","tentative suggestion")],"polite")
]

def _u(level,n,title,grammar,vocab):
    return CurriculumUnit(id=f"or-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=vocab,lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Communicate effectively at {level} in Odia",f"Understand level-appropriate Odia"],default_weeks=2)

plans={
"A1":[("ନମସ୍କାର ଓ ପରିଚୟ",["pronouns","identity"],["greetings_a1","identity_a1"]),("ବ୍ୟକ୍ତିଗତ ସୂଚନା",["questions","possession"],["identity_a1"]),("ପରିବାର",["plural","possession"],["family_a1"]),("ଘର ଓ ସ୍ଥାନ",["location","demonstratives"],["home_a1"]),("ଦୈନନ୍ଦିନ ଜୀବନ",["present","negation"],["routine_a1"]),("ଖାଦ୍ୟ ଓ ପାନୀୟ",["case","questions"],["food_a1"]),("ସ୍ଥାନ ଓ ଦିଗ",["location","case"],["places_a1"]),("ଯୋଗାଯୋଗ",["negation","questions"],["communication_a1"])],
"A2":[("ଯାତ୍ରା",["past","motion"],["travel_a2"]),("ସ୍ୱାସ୍ଥ୍ୟ",["present","imperatives"],["health_a2"]),("ପଢ଼ାଶୁଣା",["progressive","modality"],["study_a2"]),("ଭବିଷ୍ୟତ ଯୋଜନା",["future","modality"],["routine_a1","travel_a2"]),("ତୁଳନା",["comparatives","adverbs"],["identity_a1"]),("ଅନୁରୋଧ ଓ ନିର୍ଦ୍ଦେଶ",["imperatives","negation"],["communication_a1"]),("ସମୟ ଓ ଅଭ୍ୟାସ",["adverbs","progressive"],["routine_a1"]),("A2 ପୁନରାବୃତ୍ତି",["past","future","comparatives"],["travel_a2","study_a2"])],
"B1":[("ସମାଜ",["conditional","relative"],["society_b1"]),("କାମ ଓ ପ୍ରକଳ୍ପ",["cause_purpose","reported"],["work_b1"]),("ପରିବେଶ",["cause_purpose","relative"],["environment_b1"]),("ରିପୋର୍ଟ କରିବା",["reported","subordination"],["media_b2"]),("କାରଣ ଓ ଉଦ୍ଦେଶ୍ୟ",["cause_purpose","causative"],["work_b1"]),("ସମ୍ପର୍କ ଓ କାର୍ଯ୍ୟ",["reflexive","causative"],["society_b1"]),("ସଂଯୁକ୍ତ ବାକ୍ୟ",["relative","conditional"],["environment_b1"]),("B1 ପୁନରାବୃତ୍ତି",["reported","relative","conditional"],["society_b1","work_b1"])],
"B2":[("ନିଷ୍କ୍ରିୟ ବାକ୍ୟ",["passive","aspect"],["economy_b2"]),("ଅର୍ଥନୀତି",["connectors","subordination"],["economy_b2"]),("ପ୍ରଶାସନ",["concession","connectors"],["governance_b2"]),("ମିଡିଆ",["aspect","information"],["media_b2"]),("ପରିବେଶ ଓ ନୀତି",["cause_purpose","concession"],["environment_b1","governance_b2"]),("ଔପଚାରିକ ଭାଷା",["formal","passive"],["governance_b2"]),("ଜଟିଳ ଆଲୋଚନା",["subordination","connectors"],["media_b2"]),("B2 ପୁନରାବୃତ୍ତି",["passive","concession","subordination"],["economy_b2","media_b2"])],
"C1":[("ଗବେଷଣା ଓ ପ୍ରମାଣ",["nominalization","hedging"],["academic_c1"]),("ସଂସ୍ଥା ଓ ପ୍ରଶାସନ",["formal","argumentation"],["professional_c1"]),("ମିଡିଆ ବିଶ୍ଳେଷଣ",["information","reported"],["media_b2"]),("Embedded ପ୍ରଶ୍ନ",["embedded","subordination"],["academic_c1"]),("ଯୁକ୍ତି ଓ ପ୍ରତିଯୁକ୍ତି",["argumentation","connectors"],["academic_c1"]),("ପେଶାଗତ ଯୋଗାଯୋଗ",["formal","pragmatics"],["professional_c1"]),("ତଥ୍ୟର ବିନ୍ୟାସ",["information","hedging"],["abstract_c1"]),("C1 ପୁନରାବୃତ୍ତି",["argumentation","formal","embedded"],["academic_c1","professional_c1"])],
"C2":[("ପ୍ରାଗ୍ମାଟିକ୍ସ",["pragmatics","register"],["discourse_c2"]),("ରେଟରିକ୍ ଓ ଶୈଳୀ",["rhetoric","discourse_analysis"],["culture_c2"]),("ରେଜିଷ୍ଟର ପରିବର୍ତ୍ତନ",["register","pragmatics"],["professional_c1"]),("ଡିସକୋର୍ସ ବିଶ୍ଳେଷଣ",["discourse_analysis","information"],["discourse_c2"]),("ଅନୁବାଦ ଓ ପୁନର୍ଲେଖନ",["translation","register"],["culture_c2"]),("ଉନ୍ନତ ଯୁକ୍ତି",["argumentation","rhetoric"],["discourse_c2"]),("ସାହିତ୍ୟ ଓ ମିଡିଆ",["rhetoric","discourse_analysis"],["culture_c2","media_b2"]),("C2 ପୁନରାବୃତ୍ତି",["translation","pragmatics","discourse_analysis"],["discourse_c2","culture_c2"])]
}
CURRICULUM={level:[_u(level,i+1,title,grammar,vocab) for i,(title,grammar,vocab) in enumerate(items)] for level,items in plans.items()}

ASSESSMENT_BANK=[
AssessmentQuestion(id="or-a1-001",skill="communication",difficulty="A1",question="Which Odia phrase means Hello?",options=["ନମସ୍କାର।","ଧନ୍ୟବାଦ।","ବିଦାୟ।","ସାହାଯ୍ୟ।"],correct="ନମସ୍କାର।"),
AssessmentQuestion(id="or-a1-002",skill="communication",difficulty="A1",question="Which phrase asks How are you?",options=["ଆପଣ କେମିତି ଅଛନ୍ତି?","ଏହା କେତେ?","ବଜାର କେଉଁଠି?","ଦୟାକରି ବସନ୍ତୁ।"],correct="ଆପଣ କେମିତି ଅଛନ୍ତି?"),
AssessmentQuestion(id="or-a1-003",skill="vocabulary",difficulty="A1",question="Which word means water?",options=["ପାଣି","ଭାତ","ଫଳ","ବହି"],correct="ପାଣି"),
AssessmentQuestion(id="or-a1-004",skill="grammar",difficulty="A1",question="Which sentence is negative?",options=["ମୁଁ ଯାଏ ନାହିଁ।","ମୁଁ ଘରେ ଅଛି।","ମୁଁ ପଢ଼େ।","ସେ ଆସିଲା।"],correct="ମୁଁ ଯାଏ ନାହିଁ।"),
AssessmentQuestion(id="or-a2-001",skill="grammar",difficulty="A2",question="Which sentence describes a completed past action?",options=["ମୁଁ ଗତକାଲି ବଜାରକୁ ଗଲି।","ମୁଁ କାଲି ଯିବି।","ମୁଁ ଏବେ ପଢ଼ୁଛି।","ମୁଁ ପ୍ରତିଦିନ ପଢ଼େ।"],correct="ମୁଁ ଗତକାଲି ବଜାରକୁ ଗଲି।"),
AssessmentQuestion(id="or-a2-002",skill="grammar",difficulty="A2",question="Which sentence expresses a future plan?",options=["ମୁଁ କାଲି ଯିବି।","ସେ ଖାଇଲା।","ମୁଁ ଘରେ ଅଛି।","ସେ ପଢ଼ୁଛି।"],correct="ମୁଁ କାଲି ଯିବି।"),
AssessmentQuestion(id="or-b1-001",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["ଯଦି ବର୍ଷା ହୁଏ, ଆମେ ଘରେ ରହିବୁ।","ମୁଁ ଘରେ ଅଛି।","ସେ ବହି ପଢ଼ୁଛି।","ଧନ୍ୟବାଦ।"],correct="ଯଦି ବର୍ଷା ହୁଏ, ଆମେ ଘରେ ରହିବୁ।"),
AssessmentQuestion(id="or-b1-002",skill="grammar",difficulty="B1",question="Which sentence reports another person's statement?",options=["ସେ କହିଲା ଯେ ସେ ଆସିବ।","ମୁଁ ଆସିବି।","ମୁଁ ପଢ଼ୁଛି।","ସେ ଘରେ ଅଛି।"],correct="ସେ କହିଲା ଯେ ସେ ଆସିବ।"),
AssessmentQuestion(id="or-b2-001",skill="grammar",difficulty="B2",question="Which sentence expresses concession?",options=["ଯଦିଓ ବର୍ଷା ହେଉଥିଲା, ଆମେ ଗଲୁ।","ମୁଁ ବଜାରକୁ ଗଲି।","ସେ ପଢ଼ୁଛି।","ଏହା ମୋ ବହି।"],correct="ଯଦିଓ ବର୍ଷା ହେଉଥିଲା, ଆମେ ଗଲୁ।"),
AssessmentQuestion(id="or-b2-002",skill="discourse",difficulty="B2",question="Which phrase introduces a sequence?",options=["ପ୍ରଥମେ","କିନ୍ତୁ","ସମ୍ଭବତଃ","ଧନ୍ୟବାଦ"],correct="ପ୍ରଥମେ"),
AssessmentQuestion(id="or-c1-001",skill="academic",difficulty="C1",question="Which phrase appropriately hedges a claim?",options=["ସମ୍ଭବତଃ ଏହାର ଅନ୍ୟ ଏକ କାରଣ ଥାଇପାରେ।","ଏହା ନିଶ୍ଚିତ ଭାବରେ ସବୁବେଳେ ସତ୍ୟ।","ଏହା ଛଡ଼ା ଅନ୍ୟ କିଛି ନାହିଁ।","ନମସ୍କାର।"],correct="ସମ୍ଭବତଃ ଏହାର ଅନ୍ୟ ଏକ କାରଣ ଥାଇପାରେ।"),
AssessmentQuestion(id="or-c1-002",skill="formal",difficulty="C1",question="Which is a formal institutional instruction?",options=["ଦୟାକରି ଆବଶ୍ୟକ ଦଲିଲଗୁଡ଼ିକ ଦାଖଲ କରନ୍ତୁ।","ମୋତେ ପାଣି ଦରକାର।","ବଜାର କେଉଁଠି?","ନମସ୍କାର।"],correct="ଦୟାକରି ଆବଶ୍ୟକ ଦଲିଲଗୁଡ଼ିକ ଦାଖଲ କରନ୍ତୁ।"),
AssessmentQuestion(id="or-c2-001",skill="pragmatics",difficulty="C2",question="Which phrase softens a request?",options=["ସମ୍ଭବ ହେଲେ, ଦୟାକରି...","ଏବେ କରନ୍ତୁ!","ନା!","ମୁଁ ଏହା ଚାହେଁ।"],correct="ସମ୍ଭବ ହେଲେ, ଦୟାକରି..."),
AssessmentQuestion(id="or-c2-002",skill="translation",difficulty="C2",question="What should advanced translation preserve?",options=["Meaning, register and pragmatic force","Only literal words","Only word order","Only punctuation"],correct="Meaning, register and pragmatic force")
]
