"""Dzongkha A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS = ["A1","A2","B1","B2","C1","C2"]

def _g(slug,title,level,explanation,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=f"Dzongkha {level} grammar.",explanation=explanation,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS = [
_g("pronouns","Personal pronouns","A1","Use common personal reference forms.",["ང་སློབ་ཕྲུག་ཨིན།","ཁོ་དགེ་རྒན་ཨིན།"]),
_g("copula","Identity and copula","A1","Form affirmative and negative identity statements.",["འདི་དཔེ་ཆ་ཨིན།","ང་དགེ་རྒན་མེན།"]),
_g("questions","Question words","A1","Ask basic what, where, who and how questions.",["འདི་ག་ཅི་ཨིན།","ཁྱོད་རང་ག་ཏེ་ཨིན།"]),
_g("negation","Negation","A1","Negate identity and simple propositions.",["ང་དགེ་རྒན་མེན།","ང་ལུ་ཧ་མ་གོ།"]),
_g("demonstratives","Demonstratives","A1","Use འདི and དེ for reference.",["འདི་ཁྱིམ་ཨིན།","དེ་སློབ་གྲྭ་ཨིན།"]),
_g("numbers","Numbers and quantities","A1","Count familiar objects and people.",["དཔེ་ཆ་གཉིས་ཡོད།","མི་གསུམ་ཡོད།"]),
_g("location","Existence and location","A1","Express location and existence with local expressions.",["དཔེ་ཆ་ཅོག་ཙེའི་སྟེང་ལུ་ཡོད།","ང་ཁྱིམ་ནང་ལུ་ཨིན།"]),
_g("time","Time expressions","A1","Talk about today, tomorrow and basic time.",["ད་རེས་ང་ཁྱིམ་ནང་ལུ་ཨིན།","སང་ཉིན་ང་འགྱོ།"]),
_g("case_particles","Case particles and postpositions","A2","Use common particles and postpositional relations.",["ཁྱིམ་ནང་ལུ་ཡོད།","སློབ་གྲྭ་ལུ་འགྱོ།"]),
_g("present_habitual","Present and habitual actions","A2","Describe ongoing and habitual activities.",["ང་ཉིན་རེ་ལཱ་འབད།","ཁོ་སློབ་སྦྱོང་འབད་དོ།"]),
_g("past","Past events","A2","Describe completed and earlier events.",["ཁོ་ཁ་སང་འགྱོ་ནུག།","ང་གིས་དཔེ་ཆ་ལྷབ་ཅི།"]),
_g("future","Future and intention","A2","Express future plans and intentions.",["ང་སང་ཉིན་འགྱོ་ནི་ཨིན།","ང་ལཱ་འབད་ནི་ཨིན།"]),
_g("imperatives","Imperatives and polite requests","A2","Give instructions and polite requests.",["གནང་གནང།","འདི་ལྟ་གནང།"]),
_g("comparatives","Comparison","A2","Compare objects, people and qualities.",["འདི་དེ་ལས་ཆེ།","ཁོ་ལས་ང་ཆེ་བ་མེན།"]),
_g("modality","Ability, necessity and desire","A2","Express ability, need, obligation and desire.",["ང་ལུ་འདི་དགོ།","ང་འགྱོ་ཚུགས།"]),
_g("aspect","Aspect and event structure","B1","Distinguish completed, ongoing and experiential events.",["ལཱ་འབད་དོ།","ལཱ་འབད་ཚར་ཅི།"]),
_g("conditional","Conditionals","B1","Build real and hypothetical conditional clauses.",["གལ་སྲིད་ཆརཔ་རྐྱབ་ན། ང་ཁྱིམ་ནང་ལུ་སྡོད།","གལ་སྲིད་དུས་ཚོད་ཡོད་པ་ཅིན་ང་འགྱོ།"]),
_g("relative","Relative clauses","B1","Modify nouns with relative and participial constructions.",["ང་གིས་ལྷབ་མི་དཔེ་ཆ་འདི་ལེགས།","ང་གིས་མཐོང་མི་མི་འདི་ཨིན།"]),
_g("causal_purpose","Cause and purpose","B1","Express reasons, causes and purposes.",["ཁོ་ན་སྨན་ཁང་ལུ་འགྱོ་དགོ།","སློབ་སྦྱོང་འབད་ནི་གི་དོན་ལུ་འགྱོ།"]),
_g("converbs","Clause chaining and converbal relations","B1","Link sequential and dependent actions.",["ཟ་ཚར་ཞིནམ་ལས་འགྱོ་ནི་ཨིན།","འགྱོ་ཞིནམ་ལས་ཁོ་དང་མཇལ།"]),
_g("reported","Reported speech","B1","Report statements and information from another source.",["ཁོ་གིས་འགྱོ་ནི་ཨིན་ཟེར་སླབ་ཅི།","ཁོ་གིས་ག་ཏེ་ཨིན་ན་ཟེར་དྲིས་ཅི།"]),
_g("passive","Passive and affected constructions","B2","Interpret and produce passive or affected-event constructions.",["དཔེ་ཆ་འདི་ལྷབ་ཅི།","ཡིག་ཆ་འདི་བྲིས་ཚར་ཅི།"]),
_g("causative","Causative constructions","B2","Express causing, arranging or enabling an action.",["ཁོ་གིས་བྱི་ལོག་ལུ་སློབ་སྦྱོང་བྱིན་ནུག།","ཁོ་གིས་ཡིག་ཆ་འབྲི་བཅུག་ཅི།"]),
_g("concession","Concession and contrast","B2","Connect propositions with contrast and concession.",["ཆརཔ་རྐྱབ་རུང་ཁོ་འགྱོ་ནུག།","དེ་འབདཝ་ད་རུང་ཁོ་འགྱོ་ནུག།"]),
_g("discourse","Discourse connectors and cohesion","B2","Organize extended explanations and narratives.",["དང་པ་རང་འཆར་གཞི་བཟོ་དགོ། དེ་ལས་ལཱ་འགོ་བཙུགས།","དེ་འབདཝ་ལས་གྲུབ་འབྲས་འཐོན་ཡོད།"]),
_g("subordination","Complex subordinate clauses","B2","Combine clauses for time, condition, cause and complement relations.",["ཁོ་འོང་བའི་སྐབས་ལུ་ང་ཚོགས་འདུ་འགོ་བཙུགས།","ཁོ་གིས་ག་ཅི་འབད་ནི་ཨིན་ན་ང་ལུ་མི་ཤེས།"]),
_g("nominalization","Nominalization","C1","Use nominalized processes in formal and academic discourse.",["སློབ་སྦྱོང་གི་གོང་འཕེལ་གལ་ཆེ།","ལས་འགུལ་གྱི་འཛིན་སྐྱོང་དགོས།"]),
_g("evidentiality","Evidentiality and stance","C1","Distinguish witnessed information, inference and reported information.",["ང་གིས་མཐོང་ཡོད།","ཁོ་གིས་སླབ་ཡོད་ཟེར་བཤད།"]),
_g("hedging","Academic hedging","C1","Qualify claims and express degrees of certainty.",["འདི་འདྲ་བའི་བསམ་འཆར་འདུག་ཟེར་སླབ་ཚུགས།","གནད་དོན་འདི་ཡང་དག་ཡིན་སྲིད།"]),
_g("embedded_questions","Embedded questions","C1","Embed questions in formal statements and requests.",["ཁོ་ག་ཏེ་འགྱོ་ནི་ཨིན་ན་ང་ལུ་མི་ཤེས།","ག་ཅི་འབད་ནི་ཨིན་ན་བལྟ།"]),
_g("information_structure","Topic and focus","C1","Manage topic, focus and contrastive information.",["འདི་རང་གལ་ཆེ་བའི་གནད་དོན་ཨིན།","ཁོ་རང་གིས་ལཱ་འདི་འབད་ཅི།"]),
_g("formal_register","Formal and institutional register","C1","Adjust language for administration, education and professional settings.",["གསལ་བསྒྲགས་འདི་ལུ་དགོངས་འཇོག་གནང།","ཡིག་ཆ་འདི་དུས་ཚོད་ནང་འབུལ་གནང།"]),
_g("argumentation","Argumentation and counterargument","C1","Build claims, evidence, qualifications and counterarguments.",["གྲངས་ཐོ་ལ་གཞི་བཞག་སྟེ་འདི་ལུ་རྒྱབ་སྐྱོར་འབད་ཚུགས།","དེ་འབདཝ་ད་གཞན་གྱི་བསམ་འཆར་ཡང་བསམ་དགོ།"]),
_g("pragmatics","Politeness and pragmatic nuance","C2","Interpret indirectness, social stance and contextual meaning.",["ག་དེ་འབད་ཡང་འདི་ལུ་གཟིགས་གནང་ཟེར་ཞུ།","དེ་ལས་ལེགས་ཤོམ་འབད་ནི་ཨིན་ན་བསམ་གཞིག་འབད་གནང།"]),
_g("rhetoric","Rhetoric and literary style","C2","Use and interpret rhetorical framing and literary nuance.",["འདི་རྐྱངམ་གཅིག་གི་དཀའ་ངལ་མེན། གོ་ལོག་གི་འགན་ཁུར་ཨིན།","བསམ་འཆར་འདི་སྙན་ངག་གི་སྐད་ཆ་ནང་བཀོད་ཡོད།"]),
_g("translation","Translation and paraphrase","C2","Preserve meaning, register and discourse function across reformulations.",["གནད་དོན་འདི་གཞན་སྐད་ནང་བསྒྱུར་ན་ཡང་དོན་དག་ཉར་དགོ།","ཚིག་སྦྱོར་འདི་སྐད་ཆ་གཞན་གྱིས་བཤད་ཚུགས།"]),
_g("discourse_analysis","Discourse analysis and register shifting","C2","Analyze cohesion, stance, genre and audience across extended texts.",["རྩོམ་ཡིག་གི་སྐད་ཆ་དང་དམངས་སྐད་གཉིས་མ་འདྲཝ་ཨིན།","སྐད་ཆའི་གནས་སྟངས་དང་ལྟ་ཚུལ་གཞི་བཞག་སྟེ་བསྒྱུར་དགོ།"]),
]

def _v(id_,level,topic,ref,items):
    return VocabularySet(id=id_,level=level,topic=topic,unit_ref=ref,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in items])

VOCABULARY_SETS = [
_v("greetings_a1","A1","greetings","dz-a1-unit-1",[("ཀུ་ཟུ་བཏབ་ག་ལེར་ཕེབས","phrase","hello","ཀུ་ཟུ་བཏབ་ག་ལེར་ཕེབས།"),("ཐུགས་རྗེ་ཆེ","phrase","thank you","ཐུགས་རྗེ་ཆེ།"),("མིང","noun","name","ངའི་མིང་བཀྲ་ཤིས་ཨིན།"),("གྲོགས་པོ","noun","friend","ཁོ་ངའི་གྲོགས་པོ་ཨིན།")]),
_v("family_a1","A1","family","dz-a1-unit-2",[("ཨ་མ","noun","mother","ཨ་མ་ཁྱིམ་ནང་ལུ་ཨིན།"),("ཨ་པ","noun","father","ཨ་པ་ལཱ་འབད།"),("ནུ་གཅུང","noun","younger sibling","ནུ་གཅུང་སློབ་གྲྭར་འགྱོ།"),("ཨ་ཞང","noun","uncle / brother","ཨ་ཞང་འདིར་ཡོད།")]),
_v("home_a1","A1","home","dz-a1-unit-3",[("ཁྱིམ","noun","home","ངའི་ཁྱིམ་ཆེ།"),("ཁང་མིག","noun","room","ཁང་མིག་གཙང་མ་ཨིན།"),("ཅོག་ཙེ","noun","table","དཔེ་ཆ་ཅོག་ཙེའི་སྟེང་ལུ་ཡོད།"),("སྒོ","noun","door","སྒོ་ཕྱེ་ཡོད།")]),
_v("daily_a1","A1","daily life","dz-a1-unit-4",[("ཞོགས་པ","noun","morning","ཞོགས་པ་ང་ལཱ་འབད།"),("ལཱ","noun","work","ང་ལཱ་འབད།"),("འགྱོ","verb","go","ང་སློབ་གྲྭར་འགྱོ།"),("ཉལ","verb","sleep","མཚན་མོ་ང་ཉལ།")]),
_v("food_a1","A1","food and shopping","dz-a1-unit-5",[("ཆུ","noun","water","ང་ཆུ་དགོ།"),("ཇ","noun","tea","ང་ཇ་འཐུང་།"),("ཨེམ་སི","noun","rice","ང་ཨེམ་སི་ཟ།"),("གོང་ཚད","noun","price","གོང་ཚད་ག་དེ་ཅིག་ཨིན།")]),
_v("places_a1","A1","places","dz-a1-unit-6",[("སློབ་གྲྭ","noun","school","སློབ་གྲྭ་འདིར་ཡོད།"),("ཚོང་ཁང","noun","shop","ཚོང་ཁང་ཉེ་ས་ལུ་ཡོད།"),("གཡས","noun","right","གཡས་ཕྱོགས་ལུ་འགྱོ།"),("གཡོན","noun","left","གཡོན་ཕྱོགས་ལུ་འགྱོ།")]),
_v("communication_a1","A1","communication","dz-a1-unit-7",[("རོགས་རམ","noun","help","ང་ལུ་རོགས་རམ་གནང་གནང་།"),("ཧ་གོ","verb","understand","ང་ལུ་ཧ་མ་གོ།"),("གསུང་གནང","phrase","please say","ཡང་བསྐྱར་གསུང་གནང་།"),("ཡང་བསྐྱར","adverb","again","ཡང་བསྐྱར་གསུང་གནང་།")]),
_v("travel_a2","A2","travel","dz-a2-unit-1",[("འགྲུལ་བསྐྱོད","noun","travel","འགྲུལ་བསྐྱོད་ལེགས་པོ་བྱུང་།"),("གནམ་གྲུ","noun","airplane","གནམ་གྲུ་གིས་འགྲུལ་བསྐྱོད་འབད།"),("འགྲུལ་ཁང","noun","hotel","འགྲུལ་ཁང་ནང་ལུ་སྡོད།"),("ས་གནས","noun","place","ས་གནས་འདི་མཛེས།")]),
_v("health_a2","A2","health","dz-a2-unit-2",[("ན་ཚ","noun","illness","ང་ལུ་ན་ཚ་འདུག།"),("སྨན","noun","medicine","སྨན་དགོ།"),("སྨན་པ","noun","doctor","སྨན་པ་དང་མཇལ།"),("གཟུགས་ཁམས","noun","health","གཟུགས་ཁམས་ལེགས།")]),
_v("study_a2","A2","study","dz-a2-unit-3",[("སློབ་སྦྱོང","noun","study","སློབ་སྦྱོང་འབད།"),("དཔེ་ཆ","noun","book","དཔེ་ཆ་ལྷབ།"),("ཡིག་ཚད","noun","exam","ཡིག་ཚད་ཡོད།"),("རྩོམ་ཡིག","noun","essay","རྩོམ་ཡིག་འབྲི།")]),
_v("work_b1","B1","work","dz-b1-unit-1",[("ལས་འགུལ","noun","project","ལས་འགུལ་འགོ་བཙུགས།"),("ལས་འགན","noun","responsibility","ལས་འགན་གལ་ཆེ།"),("ཚོགས་འདུ","noun","meeting","ཚོགས་འདུ་ཡོད།"),("ཐག་གཅོད","noun","decision","ཐག་གཅོད་བྱེད་དགོ།")]),
_v("society_b1","B1","society","dz-b1-unit-2",[("མི་སྡེ","noun","community","མི་སྡེ་གཅིག་རུབ་འབད།"),("ཞབས་ཏོག","noun","service","ཞབས་ཏོག་ལེགས།"),("ཐོབ་ཐང","noun","right","ཐོབ་ཐང་སྲུང།"),("འགན་ཁུར","noun","responsibility","འགན་ཁུར་ཡོད།")]),
_v("environment_b2","B2","environment","dz-b2-unit-1",[("ཁོར་ཡུག","noun","environment","ཁོར་ཡུག་སྲུང་དགོ།"),("བཙོག་བཙོག","noun","pollution","བཙོག་བཙོག་ཉུང་བར་བྱེད།"),("གད་སྙིགས","noun","waste","གད་སྙིགས་བསྡུ།"),("ཐོན་ཁུངས","noun","resource","ཐོན་ཁུངས་དཀོན།")]),
_v("economy_b2","B2","economy","dz-b2-unit-2",[("དཔལ་འབྱོར","noun","economy","དཔལ་འབྱོར་འཕེལ།"),("ཚོང་ལས","noun","business","ཚོང་ལས་གསར་པ་འགོ་བཙུགས།"),("གོང་ཚད","noun","price","གོང་ཚད་འཕར།"),("ཡོང་འབབ","noun","income","ཡོང་འབབ་འཕེལ།")]),
_v("media_c1","C1","media","dz-c1-unit-1",[("གསར་འགྱུར","noun","news","གསར་འགྱུར་ལྟ།"),("ཁུངས","noun","source","ཁུངས་གསལ་དགོ།"),("རྩོམ་ཡིག","noun","article","རྩོམ་ཡིག་བཀླག།"),("བསམ་འཆར","noun","opinion","བསམ་འཆར་བརྗོད།")]),
_v("academic_c1","C1","academic","dz-c1-unit-2",[("ཞིབ་འཇུག","noun","research","ཞིབ་འཇུག་འབད།"),("དཔང་རྟགས","noun","evidence","དཔང་རྟགས་དགོ།"),("ཐབས་ལམ","noun","method","ཐབས་ལམ་གསལ།"),("མཇུག་བསྡུ","noun","conclusion","མཇུག་བསྡུ་འབད།")]),
_v("institutional_c1","C1","institutional","dz-c1-unit-3",[("སྲིད་བྱུས","noun","policy","སྲིད་བྱུས་གསར་པ།"),("ཡིག་ཆ","noun","document","ཡིག་ཆ་འབུལ།"),("གསལ་བསྒྲགས","noun","notice","གསལ་བསྒྲགས་བཏོན།"),("ཞུ་ཡིག","noun","application","ཞུ་ཡིག་འབུལ།")]),
_v("culture_c2","C2","culture","dz-c2-unit-1",[("རིག་གཞུང","noun","culture","རིག་གཞུང་སྲུང།"),("རྒྱུན་སྲོལ","noun","tradition","རྒྱུན་སྲོལ་རྒྱུན་འཛིན།"),("ཤུལ་བཞག","noun","heritage","ཤུལ་བཞག་གལ་ཆེ།"),("ལྟ་ཚུལ","noun","perspective","ལྟ་ཚུལ་མི་འདྲ།")]),
_v("discourse_c2","C2","discourse","dz-c2-unit-2",[("གྲོས་གླེང","noun","discourse / discussion","གྲོས་གླེང་འགོ་བཙུགས།"),("རྩོད་པ","noun","debate","རྩོད་པ་བྱུང་།"),("ལྟ་བ","noun","stance","ལྟ་བ་གསལ།"),("དོན་དག","noun","meaning","དོན་དག་གསལ་བཤད་བྱེད།")]),
]

def _p(id_,level,situation,items,register="neutral"):
    return PhrasebookCategory(id=id_,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=register) for t,c in items])

PHRASEBOOK_CATEGORIES = [
_p("greetings_a1","A1","greetings",[("ཀུ་ཟུ་བཏབ་ག་ལེར་ཕེབས།","greeting"),("ཁྱོད་རང་གི་མིང་ག་ཅི་ཨིན།","asking a name"),("ངའི་མིང་བཀྲ་ཤིས་ཨིན།","introducing yourself")]),
_p("thanks_a1","A1","thanks",[("ཐུགས་རྗེ་ཆེ།","saying thank you"),("ཐུགས་རྗེ་ཆེ་ལེགས།","polite thanks"),("དགའ་བསུ་ཡིན།","responding politely")]),
_p("shopping_a1","A1","shopping",[("གོང་ཚད་ག་དེ་ཅིག་ཨིན།","asking price"),("ང་འདི་དགོ།","requesting an item"),("འདི་ག་དེ་ཅིག་ཨིན།","asking cost")]),
_p("directions_a1","A1","directions",[("སློབ་གྲྭ་ག་ཏེ་ཡོད།","asking location"),("གཡས་ཕྱོགས་ལུ་འགྱོ།","giving directions"),("གཡོན་ཕྱོགས་ལུ་འགྱོ།","giving another direction")]),
_p("help_a1","A1","help",[("ང་ལུ་རོགས་རམ་གནང་གནང་།","asking for help"),("ང་ལུ་ཧ་མ་གོ།","saying you do not understand"),("ཡང་བསྐྱར་གསུང་གནང་།","asking to repeat")]),
_p("travel_a2","A2","travel",[("ག་ཏེ་སྡོད་སའི་ས་གནས་ཨིན།","asking accommodation"),("འགྲུལ་བསྐྱོད་འབད་ནི་ཨིན།","talking about travel"),("གནམ་གྲུ་གིས་འགྱོ་ནི་ཨིན།","talking about a flight")]),
_p("health_a2","A2","health",[("ང་ལུ་ན་ཚ་འདུག།","describing illness"),("སྨན་པ་དང་མཇལ་དགོ།","saying you need a doctor"),("སྨན་དགོ།","asking for medicine")]),
_p("study_a2","A2","study",[("འདི་སློབ་སྦྱོང་འབད་ནི་ཨིན།","talking about study"),("ག་དེ་སྦེ་འབད་ནི་ཨིན་ན།","asking how"),("ཡང་བསྐྱར་གསུང་གནང།","asking for repetition")]),
_p("work_b1","B1","work",[("ཚོགས་འདུ་འགོ་བཙུགས་གནང།","starting a meeting"),("ང་ལུ་བསམ་འཆར་ཅིག་ཡོད།","offering an idea"),("འདི་ལུ་ང་གིས་ཁས་ལེན་འབད།","agreeing")]),
_p("formal_b2","B2","formal communication",[("ཡིག་ཆ་འདི་དུས་ཚོད་ནང་འབུལ་གནང།","formal instruction"),("གསལ་བསྒྲགས་འདི་ལུ་དགོངས་འཇོག་གནང།","formal notice"),("ཁྱེད་ཀྱི་མཉམ་འབྲེལ་ལུ་བཀྲིན་ཆེ།","formal thanks")],"formal"),
_p("academic_c1","C1","academic discussion",[("དཔང་རྟགས་ལ་གཞི་བཞག་སྟེ།","introducing evidence"),("འདི་འདྲ་བའི་སྲིད་སྲིད།","hedging a claim"),("གཞན་ཕྱོགས་ལས་བལྟ་བ་ཅིན།","introducing a contrast")],"academic"),
_p("presentation_c1","C1","presentation",[("དང་པ་རང་ང་ཚོས་བལྟ་དགོ།","opening a point"),("གནད་དོན་གཙོ་བོ་འདི་ཨིན།","stating the main point"),("མཇུག་ལུ་སྡོམ་བསྡུ།","closing a presentation")],"formal"),
_p("pragmatics_c2","C2","pragmatic nuance",[("ག་དེ་འབད་ཡང་གཟིགས་གནང།","softening a request"),("འདི་ལས་ལེགས་ཤོམ་འབད་ནི་ཨིན་ན་བསམ་གཞིག་གནང།","tentative suggestion"),("ཁྱེད་ཀྱི་ལྟ་ཚུལ་ཧ་གོ་ཡོད། དེ་འབདཝ་ད་རུང...","polite disagreement")],"polite"),
]

def _u(level,n,title,grammar,vocab):
    return CurriculumUnit(id=f"dz-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=vocab,lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Communicate effectively at {level}",f"Understand level-appropriate Dzongkha"],default_weeks=2)

CURRICULUM = {
"A1":[_u("A1",1,"བསུ་བ་དང་ངོ་ཤེས",["pronouns","copula"],["greetings_a1","family_a1"]),_u("A1",2,"ནང་མི་དང་ཁྱིམ",["demonstratives","location"],["home_a1","family_a1"]),_u("A1",3,"ཉིན་རེའི་འཚོ་བ",["questions","negation"],["daily_a1"]),_u("A1",4,"ཟས་དང་ཉོ་ཚོང",["questions","numbers"],["food_a1"]),_u("A1",5,"ས་གནས་དང་ཁ་ཕྱོགས",["location","questions"],["places_a1"]),_u("A1",6,"འབྲེལ་བ",["negation","pronouns"],["communication_a1"]),_u("A1",7,"དུས་ཚོད",["time","numbers"],["daily_a1"]),_u("A1",8,"A1 བསྐྱར་སྦྱོང",["copula","location","questions"],["greetings_a1","communication_a1"])],
"A2":[_u("A2",1,"འགྲུལ་བསྐྱོད",["case_particles","future"],["travel_a2"]),_u("A2",2,"གཟུགས་ཁམས",["present_habitual","imperatives"],["health_a2"]),_u("A2",3,"སློབ་སྦྱོང",["past","aspect"],["study_a2"]),_u("A2",4,"འཆར་གཞི་དང་འདོད་པ",["future","modality"],["travel_a2","study_a2"]),_u("A2",5,"བསྡུར་བ",["comparatives","case_particles"],["home_a1","places_a1"]),_u("A2",6,"ཞུ་བ་དང་བཀོད་ཁྱབ",["imperatives","negation"],["communication_a1"]),_u("A2",7,"ལས་ཀྱི་རིམ་པ",["aspect","past"],["daily_a1","work_b1"]),_u("A2",8,"A2 བསྐྱར་སྦྱོང",["future","comparatives","modality"],["travel_a2","health_a2"])],
"B1":[_u("B1",1,"གནས་སྟངས་དང་གདམ་ཁ",["conditional","modality"],["work_b1"]),_u("B1",2,"འབྲེལ་བའི་ཚིག་སྒྲིག",["relative","converbs"],["society_b1"]),_u("B1",3,"རྒྱུ་མཚན་དང་དམིགས་ཡུལ",["causal_purpose","reported"],["work_b1"]),_u("B1",4,"གཞན་གྱི་སྐད་ཆ",["reported","converbs"],["media_c1"]),_u("B1",5,"ལཱ་བཅུག་དང་བྱ་བ",["causative","aspect"],["work_b1"]),_u("B1",6,"མི་སྡེ་དང་འགན་ཁུར",["discourse","causal_purpose"],["society_b1"]),_u("B1",7,"བསྒྲུབ་ཚུལ",["relative","discourse"],["environment_b2"]),_u("B1",8,"B1 བསྐྱར་སྦྱོང",["conditional","relative","reported"],["work_b1","society_b1"])],
"B2":[_u("B2",1,"བྱ་ཚུལ་དང་བྱེད་སྒོ",["passive","aspect"],["economy_b2"]),_u("B2",2,"རྒྱུ་འབྲས་དང་གནས་སྟངས",["causal_purpose","converbs"],["environment_b2"]),_u("B2",3,"ཁྱད་པར་དང་དཀའ་ངལ",["concession","discourse"],["society_b1"]),_u("B2",4,"ཚིག་སྒྲིག་རིང་པོ",["relative","subordination"],["economy_b2"]),_u("B2",5,"དཔལ་འབྱོར་དང་མི་སྡེ",["discourse","passive"],["economy_b2"]),_u("B2",6,"ཁོར་ཡུག",["causal_purpose","concession"],["environment_b2"]),_u("B2",7,"གསལ་བཤད་དང་བསྡུར་བ",["comparatives","aspect"],["media_c1"]),_u("B2",8,"B2 བསྐྱར་སྦྱོང",["passive","concession","discourse"],["economy_b2","environment_b2"])],
"C1":[_u("C1",1,"ཞིབ་འཇུག་དང་དཔང་རྟགས",["nominalization","evidentiality"],["academic_c1"]),_u("C1",2,"སྲིད་བྱུས་དང་ལས་ཁུངས",["formal_register","argumentation"],["institutional_c1"]),_u("C1",3,"གསར་འགྱུར་དང་ཁུངས",["information_structure","reported"],["media_c1"]),_u("C1",4,"གཏན་འཁེལ་མེད་པའི་དྲི་བ",["embedded_questions","subordination"],["academic_c1"]),_u("C1",5,"རྩོད་བསྒྲུབ",["argumentation","discourse"],["academic_c1"]),_u("C1",6,"ལས་ཁུངས་ཀྱི་འབྲེལ་བ",["formal_register","hedging"],["institutional_c1"]),_u("C1",7,"གནད་དོན་དང་ལྟ་ཚུལ",["information_structure","evidentiality"],["media_c1"]),_u("C1",8,"C1 བསྐྱར་སྦྱོང",["argumentation","formal_register","embedded_questions"],["academic_c1","institutional_c1"])],
"C2":[_u("C2",1,"མི་ཚུལ་དང་གོ་དོན་གསལ་བ",["pragmatics","rhetoric"],["discourse_c2"]),_u("C2",2,"རྩོམ་རིག་དང་སྒྱུ་རྩལ",["rhetoric","discourse_analysis"],["culture_c2"]),_u("C2",3,"སྐད་རིགས་གནས་སྟངས",["formal_register","pragmatics"],["institutional_c1"]),_u("C2",4,"བརྗོད་ཚུལ་དཔྱད་པ",["discourse_analysis","information_structure"],["discourse_c2"]),_u("C2",5,"སྒྱུར་བཅོས་དང་བསྒྲིགས་སྐད",["translation","pragmatics"],["culture_c2"]),_u("C2",6,"རྩོད་བསྒྲུབ་མཐོ་རིམ",["argumentation","rhetoric"],["discourse_c2"]),_u("C2",7,"གསར་འགྱུར་དང་རྩོམ་རིག",["rhetoric","discourse_analysis"],["culture_c2","media_c1"]),_u("C2",8,"C2 མཐོ་རིམ་བསྐྱར་སྦྱོང",["translation","pragmatics","discourse_analysis"],["discourse_c2","culture_c2"])],
}

ASSESSMENT_BANK = [
AssessmentQuestion(id="dz-a1-001",skill="vocabulary",difficulty="A1",question="Which phrase is a polite Dzongkha greeting?",options=["ཀུ་ཟུ་བཏབ་ག་ལེར་ཕེབས","ཐུགས་རྗེ་ཆེ","ཆུ","སློབ་གྲྭ"],correct="ཀུ་ཟུ་བཏབ་ག་ལེར་ཕེབས"),
AssessmentQuestion(id="dz-a2-001",skill="grammar",difficulty="A2",question="Which sentence expresses a future intention?",options=["ང་སང་ཉིན་འགྱོ་ནི་ཨིན།","ང་གིས་དཔེ་ཆ་ལྷབ་ཅི།","ང་ལུ་ཧ་མ་གོ།","འདི་དཔེ་ཆ་ཨིན།"],correct="ང་སང་ཉིན་འགྱོ་ནི་ཨིན།"),
AssessmentQuestion(id="dz-a2-002",skill="grammar",difficulty="A2",question="Which sentence expresses a comparison?",options=["འདི་དེ་ལས་ཆེ།","ང་ཁྱིམ་ནང་ལུ་ཨིན།","ཁོ་སློབ་སྦྱོང་འབད།","ཆུ་དགོ།"],correct="འདི་དེ་ལས་ཆེ།"),
AssessmentQuestion(id="dz-b1-001",skill="grammar",difficulty="B1",question="Which sentence is conditional?",options=["གལ་སྲིད་ཆརཔ་རྐྱབ་ན། ང་ཁྱིམ་ནང་ལུ་སྡོད།","ང་སློབ་ཕྲུག་ཨིན།","དཔེ་ཆ་ཡོད།","ཁོ་འགྱོ་ནུག།"],correct="གལ་སྲིད་ཆརཔ་རྐྱབ་ན། ང་ཁྱིམ་ནང་ལུ་སྡོད།"),
AssessmentQuestion(id="dz-b1-002",skill="grammar",difficulty="B1",question="Which sentence reports another person's statement?",options=["ཁོ་གིས་འགྱོ་ནི་ཨིན་ཟེར་སླབ་ཅི།","ང་འགྱོ་ནི་ཨིན།","ཁོ་ཁྱིམ་ནང་ལུ་ཨིན།","ཆུ་དགོ།"],correct="ཁོ་གིས་འགྱོ་ནི་ཨིན་ཟེར་སླབ་ཅི།"),
AssessmentQuestion(id="dz-b2-001",skill="discourse",difficulty="B2",question="Which sentence expresses concession?",options=["ཆརཔ་རྐྱབ་རུང་ཁོ་འགྱོ་ནུག།","ཁོ་འགྱོ་ནི་ཨིན།","ང་ལཱ་འབད།","དཔེ་ཆ་ལྷབ།"],correct="ཆརཔ་རྐྱབ་རུང་ཁོ་འགྱོ་ནུག།"),
AssessmentQuestion(id="dz-b2-002",skill="grammar",difficulty="B2",question="Which construction reports an event as completed?",options=["ལཱ་འབད་ཚར་ཅི།","ལཱ་འབད་ནི་ཨིན།","ལཱ་འབད་དོ།","ལཱ་མེན།"],correct="ལཱ་འབད་ཚར་ཅི།"),
AssessmentQuestion(id="dz-c1-001",skill="academic",difficulty="C1",question="Which phrase introduces evidence in a formal discussion?",options=["དཔང་རྟགས་ལ་གཞི་བཞག་སྟེ།","ཀུ་ཟུ་བཏབ་ག་ལེར་ཕེབས།","ཆུ་དགོ།","ག་ཏེ་ཨིན།"],correct="དཔང་རྟགས་ལ་གཞི་བཞག་སྟེ།"),
AssessmentQuestion(id="dz-c1-002",skill="formal",difficulty="C1",question="Which is a formal institutional instruction?",options=["ཡིག་ཆ་འདི་དུས་ཚོད་ནང་འབུལ་གནང།","ཀུ་ཟུ་བཏབ་ག་ལེར་ཕེབས།","ཆུ་དགོ།","ང་གྲོགས་པོ་ཨིན།"],correct="ཡིག་ཆ་འདི་དུས་ཚོད་ནང་འབུལ་གནང།"),
AssessmentQuestion(id="dz-c2-001",skill="pragmatics",difficulty="C2",question="Which phrase softens a request?",options=["ག་དེ་འབད་ཡང་གཟིགས་གནང།","ད་ལྟོ་འབད།","མི་འབད།","དགོ།"],correct="ག་དེ་འབད་ཡང་གཟིགས་གནང།"),
AssessmentQuestion(id="dz-c2-002",skill="translation",difficulty="C2",question="What should advanced translation preserve?",options=["Meaning, register and discourse function","Only word order","Only literal words","Only punctuation"],correct="Meaning, register and discourse function"),
]
