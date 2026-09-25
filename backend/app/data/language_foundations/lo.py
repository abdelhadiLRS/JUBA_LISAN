"""Lao A1-C2 foundation data for JUBA LISAN."""
from app.data._types import AssessmentQuestion, CurriculumUnit, GrammarExample, GrammarTopic, PhrasebookCategory, PhrasebookEntry, VocabularyEntry, VocabularySet

LEVELS = ["A1","A2","B1","B2","C1","C2"]

def g(slug,title,level,summary,examples):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS = [
g("pronouns","Personal pronouns","A1","Use common Lao pronouns in everyday exchanges.",["ຂ້ອຍເປັນນັກຮຽນ.","ລາວເປັນຄູ."]),
g("copula","Identity and classification","A1","Use ເປັນ and noun phrases to identify people and things.",["ລາວເປັນຄູ.","ນີ້ແມ່ນປື້ມ."]),
g("negation","Negation with ບໍ່","A1","Negate verbal and adjectival predicates with ບໍ່.",["ຂ້ອຍບໍ່ເຂົ້າໃຈ.","ລາວບໍ່ໄປ."]),
g("questions","Questions and question words","A1","Ask yes-no and information questions with ບໍ, ຫຍັງ, ໃຜ, ໃສ and ເທົ່າໃດ.",["ນີ້ແມ່ນຫຍັງ?","ເຈົ້າຢູ່ໃສ?"]),
g("demonstratives","Demonstratives","A1","Use ນີ້ and ນັ້ນ to identify nearby and distant referents.",["ນີ້ແມ່ນປື້ມ.","ນັ້ນແມ່ນໂຮງຮຽນ."]),
g("classifiers","Classifiers and quantities","A1","Count common nouns with classifiers such as ຫົວ, ຄົນ and ເຫຼັ້ມ.",["ປື້ມສອງເຫຼັ້ມ.","ມີສາມຄົນ."]),
g("location","Location and movement","A1","Express location and movement with ຢູ່, ໄປ and ມາ.",["ຂ້ອຍຢູ່ບ້ານ.","ຂ້ອຍໄປຕະຫຼາດ."]),
g("time","Time and dates","A1","Talk about days, clock time and simple schedules.",["ມື້ນີ້ວັນຈັນ.","ພົບກັນຕອນແປດໂມງ."]),
g("aspect","Aspect markers","A2","Use ກຳລັງ, ແລ້ວ and ຈະ to distinguish ongoing, completed and prospective events.",["ຂ້ອຍກຳລັງອ່ານ.","ລາວກິນເຂົ້າແລ້ວ."]),
g("future","Future and intention","A2","Express plans and predictions with ຈະ and contextual time expressions.",["ມື້ອື່ນຂ້ອຍຈະໄປ.","ລາວຈະມາຕອນແລງ."]),
g("past","Past and completed events","A2","Describe completed events with ແລ້ວ and time context.",["ຂ້ອຍໄປຕະຫຼາດແລ້ວ.","ລາວຮຽນຈົບແລ້ວ."]),
g("comparatives","Comparison","A2","Compare qualities using ກວ່າ, ເທົ່າກັບ and ທີ່ສຸດ.",["ອັນນີ້ໃຫຍ່ກວ່າ.","ລາວເກັ່ງທີ່ສຸດ."]),
g("politeness","Politeness particles","A2","Adapt requests and statements with ແດ່, ແມ່ນບໍ, ກະລຸນາ and context.",["ຊ່ວຍຂ້ອຍແດ່.","ກະລຸນາເວົ້າຊ້າໆ."]),
g("serial_verbs","Serial verb constructions","B1","Chain verbs to express manner, direction, purpose and linked actions.",["ໄປຊື້ເຂົ້າ.","ຂ້ອຍມາພົບຄູ."]),
g("modality","Ability, obligation and possibility","B1","Express ability, necessity, permission and possibility with modal expressions.",["ຂ້ອຍສາມາດເຮັດໄດ້.","ຕ້ອງໄປດຽວນີ້."]),
g("conditional","Conditional ຖ້າ...ກໍ","B1","Build real and hypothetical conditions with ຖ້າ...ກໍ.",["ຖ້າຝົນຕົກ ກໍຈະຢູ່ບ້ານ.","ຖ້າມີເວລາ ກໍມາໄດ້."]),
g("relative","Relative clauses with ທີ່","B1","Modify nouns with ທີ່ and contextually clear relative structures.",["ປື້ມທີ່ຂ້ອຍອ່ານດີຫຼາຍ.","ຄົນທີ່ມາແມ່ນຄູ."]),
g("cause_purpose","Cause and purpose","B1","Express reasons and purposes with ເພາະ, ເພາະວ່າ and ເພື່ອ.",["ເພາະຝົນຕົກ ພວກເຮົາບໍ່ໄປ.","ຂ້ອຍຮຽນເພື່ອເຮັດວຽກ."]),
g("reported","Reported speech with ວ່າ","B2","Report statements, beliefs and information with ວ່າ.",["ລາວເວົ້າວ່າຈະມາ.","ຄູບອກວ່າສອບເສັງມື້ອື່ນ."]),
g("passive","Passive and affected constructions","B2","Use ຖືກ and ໄດ້ຮັບ where appropriate to foreground affected participants.",["ລາວຖືກເຊີນໄປປະຊຸມ.","ຜູ້ສະໝັກໄດ້ຮັບການແຈ້ງ."]),
g("result","Result and completion","B2","Express completed outcomes and resulting states precisely.",["ວຽກສຳເລັດແລ້ວ.","ລາວເຮັດວຽກຈົນເສັດ."]),
g("concession","Contrast and concession","B2","Connect contrasting propositions with ແຕ່, ເຖິງແມ່ນ and ແມ່ນວ່າ.",["ເຖິງແມ່ນຝົນຕົກ ແຕ່ພວກເຮົາໄປ.","ລາວເຫນື່ອຍ ແຕ່ຍັງເຮັດວຽກ."]),
g("discourse","Discourse connectors","B2","Organize explanations with sequence, cause, contrast and conclusion markers.",["ທຳອິດພວກເຮົາວິເຄາະບັນຫາ ແລ້ວຈຶ່ງຫາວິທີແກ້."]),
g("nominalization","Nominalization and formal noun phrases","C1","Build dense formal noun phrases for institutional and analytical writing.",["ການພັດທະນາຄວນດຳເນີນຕໍ່ໄປ.","ການຕັດສິນໃຈຕ້ອງອາໄສຂໍ້ມູນ."]),
g("hedging","Academic hedging and stance","C1","Qualify claims and separate evidence from interpretation.",["ຜົນນີ້ອາດຈະສະທ້ອນໃຫ້ເຫັນວ່າ...","ອາດຈະເປັນໄປໄດ້ວ່າ..."]),
g("subordination","Complex subordination","C1","Combine multiple propositions with temporal, causal and conditional relations.",["ເມື່ອຂໍ້ມູນຖືກກວດສອບແລ້ວ ຈຶ່ງສາມາດສະຫຼຸບໄດ້."]),
g("embedded_questions","Embedded questions","C1","Embed questions inside reports, requests and formal explanations.",["ພວກເຮົາບໍ່ຮູ້ວ່າເຂົາຈະມາເມື່ອໃດ."]),
g("information_structure","Topic and focus","C1","Control emphasis through discourse context and information packaging.",["ບັນຫານີ້ ພວກເຮົາຈະສົນທະນາໃນມື້ນີ້."]),
g("formal_register","Formal and institutional Lao","C1","Use appropriate terminology and constructions in administrative and professional writing.",["ກະລຸນາຍື່ນເອກະສານຕາມຂັ້ນຕອນທີ່ກຳນົດ."]),
g("argumentation","Academic argumentation","C1","Present claims, evidence, limitations and conclusions coherently.",["ຈາກຂໍ້ມູນດັ່ງກ່າວ ສາມາດສະຫຼຸບໄດ້ວ່າ..."]),
g("pragmatics","Pragmatics and politeness","C2","Manage indirectness, respect, stance and social meaning.",["ຖ້າບໍ່ເປັນການລົບກວນ ຂໍຮົບກວນເບິ່ງໃຫ້ໄດ້ບໍ?"]),
g("rhetoric","Rhetorical and literary style","C2","Recognize metaphor, parallelism and stylistic variation.",["ພາສາແຫ່ງວັນນະຄະດີສ້າງພາບທີ່ລະອຽດ."]),
g("translation","Translation precision","C2","Preserve meaning, register and discourse function across contexts.",["ຄຳສັບສະເພາະຄວນແປໃຫ້ສອດຄ່ອງກັບບໍລິບົດ."]),
g("discourse_analysis","Discourse analysis and register shifting","C2","Analyze genre, cohesion, stance and shifts between spoken and written Lao.",["ພາສາທາງການມີຮູບແບບຕ່າງຈາກພາສາເວົ້າ."]),
]

def v(i,level,topic,words):
    return VocabularySet(id=i,level=level,topic=topic,unit_ref=i,words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS = [
v("greetings_a1","A1","ການທັກທາຍ",[("ສະບາຍດີ","phrase","hello","ສະບາຍດີ!"),("ຂອບໃຈ","phrase","thank you","ຂອບໃຈ."),("ລາກ່ອນ","phrase","goodbye","ລາກ່ອນ!"),("ຊື່","noun","name","ຂ້ອຍຊື່ນ້ອຍ.")]),
v("family_a1","A1","ຄອບຄົວ",[("ແມ່","noun","mother","ແມ່ຂອງຂ້ອຍຢູ່ບ້ານ."),("ພໍ່","noun","father","ພໍ່ຂອງຂ້ອຍເຮັດວຽກ."),("ອ້າຍ","noun","older brother","ອ້າຍຂອງຂ້ອຍຢູ່ນີ້."),("ນ້ອງ","noun","younger sibling","ນ້ອງໄປໂຮງຮຽນ.")]),
v("home_a1","A1","ເຮືອນ",[("ເຮືອນ","noun","house","ເຮືອນຂອງຂ້ອຍໃຫຍ່."),("ຫ້ອງ","noun","room","ຫ້ອງນີ້ສະອາດ."),("ໂຕະ","noun","table","ປື້ມຢູ່ເທິງໂຕະ."),("ປະຕູ","noun","door","ປະຕູເປີດ.")]),
v("daily_a1","A1","ຊີວິດປະຈຳວັນ",[("ເຊົ້າ","noun","morning","ຕອນເຊົ້າຂ້ອຍເຮັດວຽກ."),("ໄປ","verb","go","ຂ້ອຍໄປໂຮງຮຽນ."),("ເຮັດວຽກ","verb","work","ຂ້ອຍເຮັດວຽກ."),("ນອນ","verb","sleep","ຂ້ອຍນອນຕອນກາງຄືນ.")]),
v("food_a1","A1","ອາຫານ ແລະ ການຊື້",[("ນ້ຳ","noun","water","ຂ້ອຍຕ້ອງການນ້ຳ."),("ເຂົ້າ","noun","rice","ຂ້ອຍກິນເຂົ້າ."),("ກາເຟ","noun","coffee","ຂ້ອຍດື່ມກາເຟ."),("ລາຄາ","noun","price","ລາຄາເທົ່າໃດ?")]),
v("places_a1","A1","ສະຖານທີ່",[("ຕະຫຼາດ","noun","market","ຕະຫຼາດຢູ່ໃກ້."),("ໂຮງຮຽນ","noun","school","ໂຮງຮຽນຢູ່ນີ້."),("ຂວາ","noun","right","ໄປທາງຂວາ."),("ຊ້າຍ","noun","left","ໄປທາງຊ້າຍ.")]),
v("communication_a1","A1","ການສື່ສານ",[("ຊ່ວຍ","verb","help","ຊ່ວຍຂ້ອຍແດ່."),("ກະລຸນາ","adverb","please","ກະລຸນາເວົ້າອີກ."),("ເຂົ້າໃຈ","verb","understand","ຂ້ອຍບໍ່ເຂົ້າໃຈ."),("ອີກ","adverb","again","ກະລຸນາເວົ້າອີກ.")]),
v("people_a2","A2","ຜູ້ຄົນ",[("ໝູ່","noun","friend","ລາວເປັນໝູ່ຂອງຂ້ອຍ."),("ເພື່ອນບ້ານ","noun","neighbor","ເພື່ອນບ້ານຂອງຂ້ອຍໃຈດີ."),("ແຂກ","noun","guest","ມື້ນີ້ມີແຂກ."),("ກຸ່ມ","noun","group","ກຸ່ມນີ້ໃຫຍ່.")]),
v("travel_a2","A2","ການເດີນທາງ",[("ເຮືອບິນ","noun","airplane","ເຮືອບິນອອກຕອນເຊົ້າ."),("ລົດໄຟ","noun","train","ລົດໄຟມາແລ້ວ."),("ປີ້","noun","ticket","ຂໍຊື້ປີ້ໜຶ່ງໃບ."),("ໂຮງແຮມ","noun","hotel","ພວກເຮົາພັກຢູ່ໂຮງແຮມ.")]),
v("health_a2","A2","ສຸຂະພາບ",[("ໝໍ","noun","doctor","ຂ້ອຍຢາກພົບໝໍ."),("ເຈັບ","verb","hurt/be ill","ຂ້ອຍເຈັບຫົວ."),("ຢາ","noun","medicine","ກິນຢາຕາມເວລາ."),("ໂຮງໝໍ","noun","hospital","ໂຮງໝໍຢູ່ໃກ້.")]),
v("study_b1","B1","ການຮຽນ",[("ຄົ້ນຄວ້າ","verb","research","ຂ້ອຍຄົ້ນຄວ້າພາສາ."),("ບົດຮຽນ","noun","lesson","ບົດຮຽນມື້ນີ້ຍາວ."),("ການສອບເສັງ","noun","exam","ການສອບເສັງຈະເລີ່ມພູ່ນີ້."),("ຄູ","noun","teacher","ຄູອະທິບາຍບົດຮຽນ.")]),
v("work_b1","B1","ວຽກ ແລະ ອາຊີບ",[("ພະນັກງານ","noun","employee","ພະນັກງານສົ່ງລາຍງານ."),("ການປະຊຸມ","noun","meeting","ການປະຊຸມເລີ່ມສາມໂມງ."),("ປະສົບການ","noun","experience","ລາວມີປະສົບການຫຼາຍ."),("ໜ້າທີ່","noun","responsibility","ນີ້ແມ່ນໜ້າທີ່ຂອງຂ້ອຍ.")]),
v("society_b2","B2","ສັງຄົມ",[("ສັງຄົມ","noun","society","ສັງຄົມກຳລັງປ່ຽນແປງ."),("ການພັດທະນາ","noun","development","ການພັດທະນາຍືນຍົງສຳຄັນ."),("ນະໂຍບາຍ","noun","policy","ນະໂຍບາຍໃໝ່ກຳລັງດຳເນີນ."),("ພົນລະເມືອງ","noun","citizen","ພົນລະເມືອງຄວນຮູ້ສິດຂອງຕົນ.")]),
v("economy_b2","B2","ເສດຖະກິດ",[("ເສດຖະກິດ","noun","economy","ເສດຖະກິດກຳລັງເຕີບໂຕ."),("ຕະຫຼາດ","noun","market","ຄວາມຕ້ອງການໃນຕະຫຼາດເພີ່ມຂຶ້ນ."),("ການລົງທຶນ","noun","investment","ການລົງທຶນເພີ່ມຂຶ້ນ."),("ລາຍໄດ້","noun","income","ລາຍໄດ້ຂອງຄອບຄົວເພີ່ມຂຶ້ນ.")]),
v("media_c1","C1","ສື່ມວນຊົນ",[("ຂ່າວ","noun","news","ຂ່າວນີ້ຕ້ອງກວດສອບ."),("ບົດຄວາມ","noun","article","ບົດຄວາມສະເໜີຂໍ້ມູນໃໝ່."),("ແຫຼ່ງຂໍ້ມູນ","noun","source","ລະບຸແຫຼ່ງຂໍ້ມູນແລ້ວ."),("ການສຳພາດ","noun","interview","ລາວໃຫ້ສຳພາດ.")]),
v("academic_c1","C1","ພາສາວິຊາການ",[("ການຄົ້ນຄວ້າ","noun","research","ຜົນການຄົ້ນຄວ້າສຳຄັນ."),("ຫຼັກຖານ","noun","evidence","ຫຼັກຖານພຽງພໍ."),("ສົມມຸດຕິຖານ","noun","hypothesis","ສົມມຸດຕິຖານຖືກທົດສອບ."),("ຂໍ້ສະຫຼຸບ","noun","conclusion","ຂໍ້ສະຫຼຸບອີງໃສ່ຂໍ້ມູນ.")]),
v("institutional_c1","C1","ພາສາທາງການ",[("ລະບຽບ","noun","regulation","ຕ້ອງປະຕິບັດຕາມລະບຽບ."),("ໃບສະໝັກ","noun","application","ໄດ້ຮັບໃບສະໝັກແລ້ວ."),("ການຕັດສິນ","noun","decision","ການຕັດສິນອອກແລ້ວ."),("ການດຳເນີນງານ","noun","implementation","ການດຳເນີນງານກຳລັງກວດສອບ.")]),
v("culture_c2","C2","ວັດທະນະທຳ",[("ມໍລະດົກ","noun","heritage","ມໍລະດົກທາງວັດທະນະທຳຄວນຮັກສາ."),("ວັນນະຄະດີ","noun","literature","ວັນນະຄະດີລາວອຸດົມສົມບູນ."),("ພາບພົດ","noun","imagery","ນັກຂຽນໃຊ້ພາບພົດຢ່າງຊັດເຈນ."),("ສັນຍາລັກ","noun","symbol","ສັນຍາລັກມີຄວາມໝາຍສຳຄັນ.")]),
v("discourse_c2","C2","ວາທະສິນ ແລະ ພາສາ",[("ຮູບແບບ","noun","style","ຮູບແບບການຂຽນເປັນທາງການ."),("ນ້ຳສຽງ","noun","tone","ນ້ຳສຽງຂອງບົດຄວາມສຸພາບ."),("ຄວາມໝາຍແຝງ","noun","implicit meaning","ຄວາມໝາຍແຝງຕ້ອງເຂົ້າໃຈຈາກບໍລິບົດ."),("ຄຳສັບສະເພາະ","noun","terminology","ຄຳສັບສະເພາະຕ້ອງໃຊ້ໃຫ້ສອດຄ່ອງ.")]),
]

def p(i,level,situation,items,register="neutral"):
    return PhrasebookCategory(id=i,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=register) for t,c in items])

PHRASEBOOK_CATEGORIES=[
p("greetings_a1","A1","ການທັກທາຍ",[("ສະບາຍດີ!","greeting"),("ຂ້ອຍຊື່ນ້ອຍ.","introducing yourself"),("ເຈົ້າຊື່ຫຍັງ?","asking a name")]),
p("thanks_a1","A1","ຂອບໃຈ ແລະ ຂໍໂທດ",[("ຂອບໃຈ.","thanks"),("ຂໍໂທດ.","apology"),("ບໍ່ເປັນຫຍັງ.","polite response")]),
p("shopping_a1","A1","ການຊື້",[("ລາຄາເທົ່າໃດ?","asking price"),("ຂໍອັນນີ້.","requesting an item"),("ມີອັນອື່ນບໍ?","asking for another option")]),
p("directions_a1","A1","ທິດທາງ",[("ຕະຫຼາດຢູ່ໃສ?","asking location"),("ໄປທາງຂວາ.","giving directions"),("ໄປທາງຊ້າຍແລ້ວຊື່ງຕົງ.","giving a route")]),
p("help_a1","A1","ການຂໍຄວາມຊ່ວຍ",[("ຊ່ວຍຂ້ອຍແດ່.","asking for help"),("ຂ້ອຍບໍ່ເຂົ້າໃຈ.","clarification"),("ກະລຸນາເວົ້າຊ້າໆ.","asking someone to speak slowly")]),
p("travel_a2","A2","ການເດີນທາງ",[("ຂໍຊື້ປີ້ໜຶ່ງໃບ.","buying a ticket"),("ໂຮງແຮມຢູ່ໃສ?","finding a hotel"),("ຂ້ອຍມີການຈອງແລ້ວ.","confirming a booking")]),
p("health_a2","A2","ສຸຂະພາບ",[("ຂ້ອຍເຈັບຫົວ.","describing a symptom"),("ຂ້ອຍຢາກພົບໝໍ.","requesting medical help"),("ຢານີ້ໃຊ້ແນວໃດ?","asking about medicine")]),
p("study_b1","B1","ການຮຽນ",[("ກະລຸນາອະທິບາຍອີກໄດ້ບໍ?","asking for explanation"),("ຂ້ອຍສົ່ງວຽກຕາມກຳນົດ.","discussing an assignment"),("ຂ້ອຍໃຊ້ແຫຼ່ງຂໍ້ມູນນີ້.","citing a source")]),
p("work_b1","B1","ວຽກ",[("ເລີ່ມການປະຊຸມກັນເທາະ.","starting a meeting"),("ມາສົນທະນາບັນຫານີ້.","opening discussion"),("ຂ້ອຍຈະສົ່ງລາຍງານມື້ອື່ນ.","work commitment")]),
p("public_b2","B2","ການສົນທະນາສາທາລະນະ",[("ບັນຫານີ້ມີຫຼາຍປັດໃຈ.","explaining causes"),("ໃນອີກດ້ານໜຶ່ງ...","introducing contrast"),("ອີງຕາມຫຼັກຖານ...","introducing evidence")],"formal"),
p("academic_c1","C1","ການສົນທະນາວິຊາການ",[("ການຄົ້ນຄວ້ານີ້ສະແດງໃຫ້ເຫັນວ່າ...","stating a finding"),("ຜົນນີ້ຄວນຕີຄວາມຢ່າງລະມັດລະວັງ.","hedging"),("ຄວນສຶກສາປະເດັນນີ້ຕໍ່ໄປ.","proposing further research")],"academic"),
p("institutional_c1","C1","ການສື່ສານທາງການ",[("ໄດ້ຮັບເອກະສານແລ້ວ.","acknowledging a document"),("ຈະດຳເນີນການຕາມລະບຽບ.","formal procedure"),("ກະລຸນາສົ່ງຂໍ້ມູນທີ່ກ່ຽວຂ້ອງ.","formal request")],"formal"),
p("rhetoric_c2","C2","ພາສາສະທ້ອນ ແລະ ລະອຽດ",[("ຈຸດສຳຄັນຫນຶ່ງຄື...","foregrounding a point"),("ຄຳອະທິບາຍນີ້ມີຫຼັກຖານພຽງພໍບໍ?","critical evaluation"),("ອາດຈະມີຄວາມໝາຍອື່ນຢູ່ເບື້ອງຫຼັງ.","interpreting implicit meaning")],"formal"),
]

def u(level,n,title,gp,vocab,a,b):
    return CurriculumUnit(id=f"lo-{level.lower()}-{n:02}",level=level,unit_number=n,title=title,grammar_points=gp,vocabulary_set_ids=[vocab],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[a,b],default_weeks=2)

CURRICULUM={
"A1":[u("A1",1,"ການທັກທາຍ ແລະ ແນະນຳຕົວ",["pronouns","copula"],"greetings_a1","ແນະນຳຕົວເອງ","ແລກປ່ຽນຄຳທັກທາຍ"),
u("A1",2,"ຄອບຄົວ",["pronouns","demonstratives"],"family_a1","ເວົ້າກ່ຽວກັບຄອບຄົວ","ຖາມກ່ຽວກັບຍາດ"),
u("A1",3,"ເຮືອນ",["demonstratives","location"],"home_a1","ບັນຍາຍເຮືອນ","ບອກບ່ອນຢູ່ຂອງສິ່ງຂອງ"),
u("A1",4,"ຊີວິດປະຈຳວັນ",["questions","negation"],"daily_a1","ເວົ້າເຖິງກິດຈະວັດ","ສ້າງປະໂຫຍກປະຕິເສດ"),
u("A1",5,"ອາຫານ ແລະ ການຊື້",["questions","classifiers"],"food_a1","ຊື້ອາຫານ","ຖາມລາຄາ"),
u("A1",6,"ສະຖານທີ່ ແລະ ທິດທາງ",["location","questions"],"places_a1","ຖາມບ່ອນຢູ່","ບອກທິດທາງ"),
u("A1",7,"ການສື່ສານ",["negation","questions"],"communication_a1","ຂໍຄວາມຊ່ວຍ","ຂໍໃຫ້ເວົ້າຊ້າ"),
u("A1",8,"ທົບທວນ A1",["time","classifiers"],"greetings_a1","ຈັດການການສົນທະນາພື້ນຖານ","ທົບທວນຫົວຂໍ້ຄຸ້ນເຄີຍ")],
"A2":[u("A2",1,"ຜູ້ຄົນ ແລະ ຄວາມສຳພັນ",["aspect","politeness"],"people_a2","ບັນຍາຍຜູ້ຄົນ","ເວົ້າເຖິງກິດຈະວັດ"),
u("A2",2,"ການເດີນທາງ",["past","future"],"travel_a2","ເລົ່າການເດີນທາງ","ວາງແຜນການເດີນທາງ"),
u("A2",3,"ສຸຂະພາບ",["aspect","politeness"],"health_a2","ບັນຍາຍອາການ","ຂໍຄວາມຊ່ວຍຢ່າງສຸພາບ"),
u("A2",4,"ເວລາ ແລະ ແຜນການ",["future","time"],"daily_a1","ວາງແຜນ","ສົນທະນາຕາຕະລາງ"),
u("A2",5,"ການປຽບທຽບ",["comparatives","classifiers"],"home_a1","ປຽບທຽບສິ່ງຂອງ","ອະທິບາຍລະດັບ"),
u("A2",6,"ການຂໍຮ້ອງຢ່າງສຸພາບ",["politeness","questions"],"communication_a1","ຂໍຮ້ອງຢ່າງສຸພາບ","ຂໍໃຫ້ຊີ້ແຈງ"),
u("A2",7,"ບໍລິການ ແລະ ເມືອງ",["location","questions"],"places_a1","ບອກທາງ","ອະທິບາຍບ່ອນຢູ່"),
u("A2",8,"ທົບທວນ A2",["past","future"],"travel_a2","ແຍກອະດີດ ແລະ ອະນາຄົດ","ສື່ສານໃນສະຖານະການເດີນທາງ")],
"B1":[u("B1",1,"ການຮຽນ",["serial_verbs","modality"],"study_b1","ອະທິບາຍການຮຽນ","ໃຫ້ຄຳແນະນຳ"),
u("B1",2,"ວຽກ ແລະ ອາຊີບ",["modality","conditional"],"work_b1","ອະທິບາຍໜ້າທີ່","ໃຫ້ຂໍ້ສະເໜີ"),
u("B1",3,"ເຫດຜົນ ແລະ ຈຸດປະສົງ",["cause_purpose","serial_verbs"],"society_b2","ອະທິບາຍເຫດຜົນ","ສະແດງຈຸດປະສົງ"),
u("B1",4,"ເງື່ອນໄຂ",["conditional","future"],"travel_a2","ວາງແຜນຕາມເງື່ອນໄຂ","ອະທິບາຍຜົນທີ່ອາດເກີດ"),
u("B1",5,"ປະໂຫຍກຂະຫຍາຍ",["relative","serial_verbs"],"study_b1","ຂະຫຍາຍນາມ","ໃຫ້ຂໍ້ມູນລະອຽດ"),
u("B1",6,"ລຳດັບເຫດການ",["serial_verbs","past"],"daily_a1","ເລົ່າເຫດການຕາມລຳດັບ","ອະທິບາຍຂະບວນການ"),
u("B1",7,"ການແກ້ບັນຫາ",["cause_purpose","modality"],"work_b1","ອະທິບາຍສາເຫດ","ໃຫ້ຄຳແນະນຳ"),
u("B1",8,"ທົບທວນ B1",["relative","conditional"],"study_b1","ໃຊ້ປະໂຫຍກສັບຊ້ອນ","ສົນທະນາການຮຽນແລະວຽກ")],
"B2":[u("B2",1,"ຄຳເວົ້າລາຍງານ",["reported","subordination"],"media_c1","ລາຍງານຄຳເວົ້າ","ແຍກແຫຼ່ງຂໍ້ມູນ"),
u("B2",2,"ຮູບແບບຜູ້ຖືກກະທຳ",["passive","result"],"institutional_c1","ປ່ຽນມຸມມອງຂອງເຫດການ","ອະທິບາຍຜົນລັບ"),
u("B2",3,"ຫຼັກຖານ ແລະ ການຄາດຄະເນ",["hedging","modality"],"academic_c1","ສະແດງລະດັບຫຼັກຖານ","ໃຊ້ພາສາຢ່າງລະມັດລະວັງ"),
u("B2",4,"ຄວາມຂັດແຍ້ງ",["concession","discourse"],"society_b2","ເຊື່ອມຄວາມຄິດທີ່ຕ່າງກັນ","ສະແດງການຍອມຮັບ"),
u("B2",5,"ເສດຖະກິດ",["reported","cause_purpose"],"economy_b2","ອະທິບາຍຂໍ້ມູນເສດຖະກິດ","ເຊື່ອມເຫດແລະຜົນ"),
u("B2",6,"ບັນຫາສັງຄົມ",["discourse","concession"],"society_b2","ອະພິປາຍບັນຫາຫຼາຍດ້ານ","ນຳສະເໜີມຸມມອງຕ່າງກັນ"),
u("B2",7,"ສື່ມວນຊົນ",["reported","hedging"],"media_c1","ວິເຄາະແຫຼ່ງຂ່າວ","ແຍກຂໍ້ເທັດຈິງແລະການຄາດຄະເນ"),
u("B2",8,"ທົບທວນ B2",["passive","discourse"],"media_c1","ສະຫຼຸບຂໍ້ມູນລະອຽດ","ຂຽນຄຳອະທິບາຍຍາວ")],
"C1":[u("C1",1,"ພາສາທາງການ",["nominalization","formal_register"],"institutional_c1","ຂຽນແບບທາງການ","ໃຊ້ນາມສຳລັບຂະບວນການ"),
u("C1",2,"ພາສາວິຊາການ",["hedging","argumentation"],"academic_c1","ສະແດງລະດັບຄວາມແນ່ນອນ","ສະຫຼຸບຢ່າງລະມັດລະວັງ"),
u("C1",3,"ປະໂຫຍກຊັບຊ້ອນ",["subordination","embedded_questions"],"academic_c1","ສ້າງຂໍ້ຄວາມຊັບຊ້ອນ","ໃຊ້ຄຳຖາມທີ່ຝັງຢູ່"),
u("C1",4,"ຫົວຂໍ້ ແລະ ຈຸດເນັ້ນ",["information_structure","discourse"],"discourse_c2","ຈັດຂໍ້ມູນຕາມຈຸດເນັ້ນ","ປັບຮູບປະໂຫຍກຕາມບໍລິບົດ"),
u("C1",5,"ການສື່ສານສະຖາບັນ",["formal_register","nominalization"],"institutional_c1","ຂຽນເອກະສານທາງການ","ອະທິບາຍຂັ້ນຕອນ"),
u("C1",6,"ການໂຕ້ຖຽງວິຊາການ",["argumentation","hedging"],"academic_c1","ສ້າງຂໍ້ໂຕ້ຖຽງຈາກຫຼັກຖານ","ພິຈາລະນາຄວາມຄິດຕ່າງ"),
u("C1",7,"ພາສາສື່ ແລະ ນະໂຍບາຍ",["information_structure","formal_register"],"media_c1","ວິເຄາະພາສາສາທາລະນະ","ປັບນ້ຳສຽງທາງການ"),
u("C1",8,"ທົບທວນ C1",["subordination","argumentation"],"academic_c1","ຂຽນຄຳອະທິບາຍວິຊາການ","ເຊື່ອມຄວາມຄິດລະອຽດ"),
],
"C2":[u("C2",1,"ພາສາໃນບໍລິບົດ",["pragmatics","information_structure"],"discourse_c2","ແຍກຄວາມໝາຍຕົງແລະແຝງ","ຈັດການຄວາມສຸພາບ"),
u("C2",2,"ວາທະສິນ ແລະ ວັນນະຄະດີ",["rhetoric","discourse_analysis"],"culture_c2","ໃຊ້ວິທີການວາທະສິນ","ວິເຄາະພາບພົດ"),
u("C2",3,"ການແປຢ່າງແມ່ນຍຳ",["translation","pragmatics"],"discourse_c2","ຮັກສາຄວາມໝາຍແລະນ້ຳສຽງ","ເລືອກຄຳສັບຕາມບໍລິບົດ"),
u("C2",4,"ການວິເຄາະວາທະສິນ",["discourse_analysis","information_structure"],"discourse_c2","ວິເຄາະປະເພດແລະຮູບແບບ","ອະທິບາຍຄວາມສອດຄ່ອງ"),
u("C2",5,"ຮູບແບບວັນນະຄະດີ",["rhetoric","translation"],"culture_c2","ຈຳແນກພາສາວັນນະຄະດີ","ອະທິບາຍການເລືອກຮູບພາບ"),
u("C2",6,"ພາສາວິຊາຊີບ",["formal_register","pragmatics"],"institutional_c1","ສື່ສານຄວາມຄິດຊັບຊ້ອນ","ປັບຄວາມສຸພາບຕາມບໍລິບົດ"),
u("C2",7,"ການສັງລວມແຫຼ່ງຂໍ້ມູນ",["argumentation","discourse_analysis"],"media_c1","ສັງລວມຫຼາຍແຫຼ່ງ","ປຽບທຽບຫຼັກຖານທີ່ຕ່າງກັນ"),
u("C2",8,"ການປະເມີນ C2",["translation","rhetoric"],"academic_c1","ຂຽນບົດຄວາມວິຊາການ","ປັບຮູບແບບຕາມເປົ້າໝາຍ")],
}

ASSESSMENT_BANK=[
AssessmentQuestion(id=f"lo-{i:03}",skill=skill,difficulty=level,question=q,options=opts,correct=correct)
for i,(level,skill,q,opts,correct) in enumerate([
("A1","vocabulary","What does ສະບາຍດີ mean?",["hello","goodbye","water","market"],"hello"),
("A1","grammar","Which sentence is negative?",["ຂ້ອຍບໍ່ເຂົ້າໃຈ.","ຂ້ອຍເຂົ້າໃຈ.","ນີ້ແມ່ນປື້ມ.","ຂ້ອຍໄປ."],"ຂ້ອຍບໍ່ເຂົ້າໃຈ."),
("A1","vocabulary","What does ແມ່ mean?",["mother","father","friend","school"],"mother"),
("A2","grammar","Which marks an ongoing action?",["ກຳລັງ","ແລ້ວ","ຈະ","ບໍ່"],"ກຳລັງ"),
("A2","vocabulary","What does ປີ້ mean?",["ticket","medicine","meeting","source"],"ticket"),
("B1","grammar","Which expression introduces a condition?",["ຖ້າ...ກໍ","ເພາະວ່າ","ແຕ່","ເພື່ອ"],"ຖ້າ...ກໍ"),
("B1","grammar","Which expression introduces purpose?",["ເພື່ອ","ເພາະວ່າ","ແຕ່","ຖ້າ"],"ເພື່ອ"),
("B2","grammar","Which introduces reported information?",["ວ່າ","ກຳລັງ","ແລ້ວ","ບໍ່"],"ວ່າ"),
("B2","vocabulary","What does ຫຼັກຖານ mean?",["evidence","holiday","neighbor","ticket"],"evidence"),
("C1","academic","Which phrase is an academic hedge?",["ອາດຈະ...","ສະບາຍດີ!","ຂອບໃຈ.","ລາກ່ອນ!"],"ອາດຈະ..."),
("C1","formal","Which is formal institutional language?",["ກະລຸນາຍື່ນເອກະສານຕາມຂັ້ນຕອນ.","ສະບາຍດີ!","ລາຄາເທົ່າໃດ?","ຂ້ອຍຢາກນ້ຳ."],"ກະລຸນາຍື່ນເອກະສານຕາມຂັ້ນຕອນ."),
("C2","discourse","What should translation preserve?",["meaning, register and discourse function","word count only","literal word order only","punctuation only"],"meaning, register and discourse function"),
],1)
]
