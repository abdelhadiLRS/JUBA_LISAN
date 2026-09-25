"""Thai A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def g(slug,title,level,summary,examples,category="grammar"):
    return GrammarTopic(slug=slug,title=title,level=level,category=category,summary=summary,explanation=summary,examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS = [
    g("pronouns","Personal pronouns","A1","Choose Thai pronouns according to relationship and context.",["ผมเป็นนักเรียนครับ","คุณเป็นครูไหมครับ"],"core"),
    g("copula","Identity and nominal predicates","A1","Use เป็น and noun/adjective predicates naturally.",["เขาเป็นหมอ","วันนี้อากาศดี"],"core"),
    g("questions","Questions","A1","Use ไหม, หรือ and question words.",["คุณมาจากไหนครับ","คุณเป็นนักเรียนไหมครับ"],"core"),
    g("negation","Negation","A1","Place ไม่ before verbs and adjectives and ใช่ไหม patterns.",["ผมไม่กินกาแฟ","วันนี้ไม่ร้อน"],"core"),
    g("classifiers","Classifiers and counting","A1","Use classifiers with numbers and noun phrases.",["หนังสือสองเล่ม","นักเรียนสามคน"],"core"),
    g("location","Location and existence","A1","Use อยู่, ที่ and location expressions.",["ผมอยู่ที่บ้าน","หนังสืออยู่บนโต๊ะ"],"core"),
    g("politeness","Polite particles","A1","Use ครับ and ค่ะ/คะ appropriately.",["ขอบคุณครับ","ขอบคุณค่ะ"],"core"),
    g("requests","Requests and imperatives","A1","Make practical requests with ช่วย, กรุณา and ขอ.",["ช่วยพูดอีกครั้งครับ","ขอน้ำหนึ่งแก้วค่ะ"],"core"),
    g("word_order","Basic Thai word order","A2","Build common subject-verb-object sentences.",["ฉันเรียนภาษาไทย","เขาซื้อหนังสือ"],"core"),
    g("possessives","Possession with ของ","A2","Express ownership and relationships with ของ.",["นี่คือหนังสือของฉัน","บ้านของเขาอยู่ที่นี่"],"core"),
    g("time","Time expressions","A2","Place time expressions naturally in Thai sentences.",["พรุ่งนี้ฉันจะไปทำงาน","เมื่อวานเขามาที่นี่"],"core"),
    g("aspect","Aspect markers","A2","Use กำลัง, แล้ว and อยู่ to express ongoing and completed events.",["ฉันกำลังอ่านหนังสือ","เขากินข้าวแล้ว"],"core"),
    g("future","Future and intention","A2","Use จะ and contextual time expressions.",["พรุ่งนี้จะฝนตกไหม","ฉันจะไปกรุงเทพฯ"],"core"),
    g("past","Past reference","A2","Express completed events through context and aspect markers.",["เมื่อวานฉันไปตลาด","เขาเพิ่งกลับมา"],"core"),
    g("comparatives","Comparison","A2","Use กว่า and ที่สุด for comparison.",["รถคันนี้แพงกว่าคันนั้น","วันนี้ร้อนที่สุด"],"core"),
    g("modality","Ability, obligation and permission","A2","Use สามารถ, ต้อง, ควร, ได้ and ไม่ได้.",["คุณต้องพักผ่อน","ฉันสามารถช่วยได้"],"core"),
    g("serial_verbs","Serial verb constructions","B1","Combine verbs to express direction, purpose and sequence.",["ฉันไปซื้ออาหาร","เขาเดินมาหาฉัน"],"intermediate"),
    g("result","Result and degree","B1","Use แล้ว, จน, มาก and related constructions.",["เขาวิ่งจนเหนื่อย","งานนี้ยากมาก"],"intermediate"),
    g("relative","Relative clauses with ที่","B1","Modify nouns with ที่ and contextual clauses.",["หนังสือที่ฉันซื้อดีมาก","คนที่ยืนอยู่ตรงนั้นเป็นครู"],"intermediate"),
    g("conditional","Conditionals","B1","Use ถ้า...ก็ and related conditional patterns.",["ถ้าฝนตก เราก็จะอยู่บ้าน","ถ้ามีเวลา ฉันจะไป"],"intermediate"),
    g("cause_purpose","Cause and purpose","B1","Use เพราะ, ดังนั้น, เพื่อ and เพราะว่า.",["เพราะฝนตกจึงรถติด","ฉันเรียนเพื่อทำงาน"],"intermediate"),
    g("reported","Reported speech","B1","Report statements, questions and beliefs with ว่า.",["เขาบอกว่าจะมา","เธอถามว่าฉันอยู่ที่ไหน"],"intermediate"),
    g("passive","Passive constructions","B1","Use ถูก and ได้รับ according to event and register.",["เขาถูกเชิญไปประชุม","ผู้สมัครได้รับการอนุมัติ"],"intermediate"),
    g("causative","Causative and ให้ constructions","B1","Express causing, allowing and arranging actions.",["ครูให้เด็กอ่านหนังสือ","เขาให้ช่างซ่อมรถ"],"intermediate"),
    g("connectors","Discourse connectors","B2","Link clauses with แต่, อย่างไรก็ตาม, นอกจากนี้ and therefore patterns.",["ฉันอยากไป แต่ไม่มีเวลา","นอกจากนี้ยังมีอีกประเด็นหนึ่ง"],"intermediate"),
    g("concession","Concession and contrast","B2","Express แม้ว่า, ถึงแม้ and อย่างไรก็ตาม.",["แม้ว่าจะเหนื่อย แต่เขายังทำงาน","ถึงแม้ฝนตก เราก็ไป"],"intermediate"),
    g("subordination","Complex subordination","B2","Build multi-clause sentences with temporal and logical relations.",["หลังจากที่ประชุมเสร็จ เราจะกลับบ้าน","ก่อนที่จะตัดสินใจควรตรวจสอบข้อมูล"],"intermediate"),
    g("nominalization","Nominalization with การ and ความ","B2","Form abstract nouns for formal and analytical language.",["การศึกษาเป็นเรื่องสำคัญ","ความปลอดภัยต้องมาก่อน"],"intermediate"),
    g("hedging","Academic hedging","C1","Qualify claims with อาจ, น่าจะ, มีแนวโน้ม and อาจกล่าวได้ว่า.",["ผลลัพธ์อาจแตกต่างกัน","อาจกล่าวได้ว่าปัจจัยนี้มีความสำคัญ"],"advanced"),
    g("embedded_questions","Embedded questions","C1","Embed question content in formal clauses.",["ฉันไม่รู้ว่าเขาจะมาเมื่อไร","ยังไม่ชัดเจนว่าทำไมผลจึงเปลี่ยน"],"advanced"),
    g("formal_register","Formal and institutional Thai","C1","Handle official notices, procedures and formal requests.",["กรุณายื่นเอกสารภายในวันที่กำหนด","โปรดตรวจสอบข้อมูลก่อนส่งแบบฟอร์ม"],"advanced"),
    g("academic_argument","Academic argumentation","C1","Present claims, evidence, contrast and conclusions.",["หลักฐานดังกล่าวสนับสนุนข้อสรุปนี้","อย่างไรก็ตาม ข้อมูลยังมีข้อจำกัด"],"advanced"),
    g("information_structure","Topic and focus","C1","Manage topic-comment structure and emphasis in Thai discourse.",["สำหรับประเด็นนี้ เราจะอภิปรายภายหลัง","สิ่งที่สำคัญที่สุดคือคุณภาพ"],"advanced"),
    g("register_shift","Register shifting and politeness","C1","Shift between informal, neutral and formal Thai.",["กินข้าวหรือยัง","รับประทานอาหารแล้วหรือยังครับ"],"advanced"),
    g("pragmatics","Pragmatics and indirectness","C2","Interpret indirect requests, politeness and contextual meaning.",["พอจะช่วยดูให้หน่อยได้ไหมครับ","ถ้าไม่เป็นการรบกวน ขอถามอีกเรื่องได้ไหม"],"advanced"),
    g("rhetoric","Rhetorical Thai","C2","Use parallelism, contrast and emphasis in persuasive discourse.",["ในด้านหนึ่งมีข้อดี แต่อีกด้านหนึ่งก็มีความเสี่ยง","ประเด็นสำคัญไม่ได้อยู่ที่จำนวน แต่อยู่ที่คุณภาพ"],"advanced"),
    g("literary","Literary and idiomatic Thai","C2","Handle figurative language, idioms and literary register.",["เวลาเหมือนสายน้ำ","เขาเป็นเสาหลักของครอบครัว"],"advanced"),
    g("translation","Translation precision","C2","Preserve meaning, register, politeness and discourse function.",["คำนี้ต้องแปลตามบริบท","ระดับภาษาเป็นส่วนสำคัญของความหมาย"],"advanced"),
    g("discourse_analysis","Discourse analysis","C2","Analyze cohesion, reference, stance, genre and paragraph structure.",["ดังนั้น ข้อเสนอดังกล่าวควรพิจารณาในบริบทที่กว้างขึ้น","อย่างไรก็ตาม ข้อสรุปนี้อาศัยข้อมูลจำนวนจำกัด"],"advanced"),
]

def v(i,level,topic,words):
    return VocabularySet(id=i,level=level,topic=topic,unit_ref=f"th-{level.lower()}",words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS = [
    v("greetings_a1","A1","Greetings",[["สวัสดี","phrase","hello","สวัสดีครับ"],["ขอบคุณ","phrase","thank you","ขอบคุณค่ะ"],["ชื่อ","noun","name","ฉันชื่อมิน"],["เพื่อน","noun","friend","เขาเป็นเพื่อนของฉัน"]]),
    v("family_a1","A1","Family",[["แม่","noun","mother","แม่อยู่บ้าน"],["พ่อ","noun","father","พ่อทำงาน"],["พี่","noun","older sibling","พี่ของฉันเป็นครู"],["น้อง","noun","younger sibling","น้องเรียนอยู่"]]),
    v("home_a1","A1","Home",[["บ้าน","noun","home","บ้านของฉันอยู่ที่นี่"],["ห้อง","noun","room","ห้องสะอาด"],["โต๊ะ","noun","table","หนังสืออยู่บนโต๊ะ"],["ประตู","noun","door","ประตูเปิดอยู่"]]),
    v("daily_a1","A1","Daily life",[["เช้า","noun","morning","ตอนเช้าฉันทำงาน"],["กิน","verb","eat","ฉันกินข้าว"],["เรียน","verb","study","ฉันเรียนภาษาไทย"],["นอน","verb","sleep","ฉันนอนตอนกลางคืน"]]),
    v("food_a1","A1","Food",[["น้ำ","noun","water","ขอน้ำหนึ่งแก้ว"],["ข้าว","noun","rice/meal","ฉันกินข้าว"],["กาแฟ","noun","coffee","ฉันดื่มกาแฟ"],["ราคา","noun","price","ราคาเท่าไรครับ"]]),
    v("places_a1","A1","Places",[["ตลาด","noun","market","ตลาดอยู่ใกล้บ้าน"],["โรงเรียน","noun","school","โรงเรียนอยู่ตรงนั้น"],["ซ้าย","noun","left","เลี้ยวซ้าย"],["ขวา","noun","right","เลี้ยวขวา"]]),
    v("time_a2","A2","Time",[["วันนี้","adverb","today","วันนี้ฉันทำงาน"],["พรุ่งนี้","adverb","tomorrow","พรุ่งนี้ฉันจะไป"],["เมื่อวาน","adverb","yesterday","เมื่อวานฝนตก"],["เวลา","noun","time","ตอนนี้กี่โมง"]]),
    v("travel_a2","A2","Travel",[["ตั๋ว","noun","ticket","ขอตั๋วหนึ่งใบ"],["สนามบิน","noun","airport","สนามบินอยู่ไกล"],["รถไฟ","noun","train","รถไฟออกกี่โมง"],["จอง","verb","reserve","ฉันจองโรงแรมแล้ว"]]),
    v("health_a2","A2","Health",[["ปวด","verb","hurt","ฉันปวดหัว"],["ยา","noun","medicine","กินยาหลังอาหาร"],["โรงพยาบาล","noun","hospital","โรงพยาบาลอยู่ใกล้"],["พัก","verb","rest","คุณควรพักผ่อน"]]),
    v("education_b1","B1","Education",[["การศึกษา","noun","education","การศึกษามีความสำคัญ"],["การบ้าน","noun","homework","ฉันทำการบ้านแล้ว"],["วิชา","noun","subject","วิชานี้น่าสนใจ"],["วิจัย","noun","research","งานวิจัยกำลังดำเนินการ"]]),
    v("work_b1","B1","Work",[["สำนักงาน","noun","office","สำนักงานเปิดเก้าโมง"],["ประชุม","verb","meet","เราจะประชุมพรุ่งนี้"],["หน้าที่","noun","duty","นี่เป็นหน้าที่ของฉัน"],["ประสบการณ์","noun","experience","ฉันมีประสบการณ์ห้าปี"]]),
    v("society_b2","B2","Society",[["สังคม","noun","society","สังคมกำลังเปลี่ยนแปลง"],["ความเท่าเทียม","noun","equality","ความเท่าเทียมเป็นหลักสำคัญ"],["สิทธิ","noun","right","ทุกคนมีสิทธิ"],["นโยบาย","noun","policy","นโยบายใหม่มีผลแล้ว"]]),
    v("environment_b2","B2","Environment",[["สิ่งแวดล้อม","noun","environment","เราต้องรักษาสิ่งแวดล้อม"],["มลพิษ","noun","pollution","มลพิษลดลง"],["ทรัพยากร","noun","resource","ทรัพยากรมีจำกัด"],["สภาพภูมิอากาศ","noun","climate","สภาพภูมิอากาศเปลี่ยนแปลง"]]),
    v("technology_b2","B2","Technology",[["เทคโนโลยี","noun","technology","เทคโนโลยีพัฒนาเร็ว"],["ซอฟต์แวร์","noun","software","ซอฟต์แวร์ได้รับการอัปเดต"],["ข้อมูล","noun","data","เราวิเคราะห์ข้อมูล"],["ความปลอดภัย","noun","security","ความปลอดภัยของข้อมูลสำคัญ"]]),
    v("economy_c1","C1","Economy",[["เศรษฐกิจ","noun","economy","เศรษฐกิจฟื้นตัว"],["การลงทุน","noun","investment","การลงทุนเพิ่มขึ้น"],["ผลิตภาพ","noun","productivity","ผลิตภาพเพิ่มขึ้น"],["ตลาด","noun","market","ตลาดมีการแข่งขันสูง"]]),
    v("governance_c1","C1","Governance",[["การบริหาร","noun","administration","การบริหารมีประสิทธิภาพ"],["กระบวนการ","noun","process","กระบวนการชัดเจน"],["ระเบียบ","noun","regulation","ระเบียบใหม่มีผล"],["การปฏิบัติตาม","noun","compliance","การปฏิบัติตามเป็นสิ่งจำเป็น"]]),
    v("academic_c1","C1","Academic discourse",[["สมมติฐาน","noun","hypothesis","สมมติฐานได้รับการทดสอบ"],["การวิเคราะห์","noun","analysis","การวิเคราะห์พบประเด็นใหม่"],["หลักฐาน","noun","evidence","หลักฐานยังไม่เพียงพอ"],["ข้อสรุป","noun","conclusion","ข้อสรุปชัดเจน"]]),
    v("media_c2","C2","Public discourse",[["วาทกรรม","noun","discourse","วาทกรรมสาธารณะเปลี่ยนแปลง"],["มุมมอง","noun","perspective","นี่เป็นอีกมุมมองหนึ่ง"],["การตีความ","noun","interpretation","มีการตีความหลายแบบ"],["ความเกี่ยวข้อง","noun","relevance","ความเกี่ยวข้องของประเด็นนี้ชัดเจน"]]),
    v("literary_c2","C2","Literary language",[["อุปมา","noun","simile/metaphor","อุปมานี้สร้างภาพที่ชัดเจน"],["นัย","noun","implication/connotation","นัยของคำขึ้นอยู่กับบริบท"],["สำนวน","noun","idiom","สำนวนนี้ใช้ในภาษาพูด"],["ความละเอียดอ่อน","noun","nuance","การแปลต้องรักษาความละเอียดอ่อน"]]),
]

def p(i,level,situation,items):
    return PhrasebookCategory(id=i,level=level,situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in items])

PHRASEBOOK_CATEGORIES = [
    p("greetings_a1","A1","Greetings",[["สวัสดีครับ","greeting","polite"],["คุณชื่ออะไรครับ","introducing/asking name","polite"]]),
    p("shopping_a1","A1","Shopping",[["ราคาเท่าไรครับ","asking price","polite"],["ขออันนี้หนึ่งอันครับ","requesting an item","polite"]]),
    p("directions_a1","A1","Directions",[["สถานีอยู่ที่ไหนครับ","asking location","polite"],["เลี้ยวซ้ายแล้วตรงไปครับ","giving directions","neutral"]]),
    p("help_a1","A1","Help",[["ช่วยผมหน่อยได้ไหมครับ","asking for help","polite"],["พูดอีกครั้งได้ไหมครับ","asking for repetition","polite"]]),
    p("travel_a2","A2","Travel",[["ขอตั๋วไปเชียงใหม่หนึ่งใบครับ","buying a ticket","polite"],["รถไฟออกกี่โมงครับ","asking departure time","polite"]]),
    p("health_a2","A2","Health",[["ผมปวดหัวครับ","describing symptoms","polite"],["ขอพบหมอได้ไหมครับ","requesting medical help","polite"]]),
    p("study_b1","B1","Study",[["ช่วยอธิบายคำนี้หน่อยได้ไหมครับ","asking for explanation","polite"],["ผมส่งงานแล้วครับ","reporting submission","neutral"]]),
    p("work_b1","B1","Work",[["เราจะเริ่มประชุมกันไหมครับ","starting a meeting","formal"],["ขอเสนอความคิดเห็นครับ","offering an opinion","formal"]]),
    p("formal_c1","C1","Formal administration",[["กรุณายื่นเอกสารภายในวันที่กำหนด","official instruction","formal"],["โปรดตรวจสอบข้อมูลก่อนส่ง","formal instruction","formal"]]),
    p("academic_c1","C1","Academic discussion",[["หลักฐานดังกล่าวสนับสนุนข้อสรุปนี้","presenting evidence","academic"],["อย่างไรก็ตาม ข้อมูลยังมีข้อจำกัด","qualifying an argument","academic"]]),
    p("public_c2","C2","Public discourse",[["ประเด็นนี้มีหลายมุมมอง","framing a debate","formal"],["ข้อกล่าวอ้างนี้ยังไม่มีหลักฐานเพียงพอ","challenging a claim","formal"]]),
    p("literary_c2","C2","Literary analysis",[["นัยของข้อความนี้ขึ้นอยู่กับบริบท","interpreting nuance","literary"],["สำนวนนี้สะท้อนวัฒนธรรมของผู้พูด","interpreting idiom","literary"]]),
]

def u(level,n,title,grammar,vocab,c1,c2):
    return CurriculumUnit(id=f"th-{level.lower()}-{n}",level=level,unit_number=n,title=title,grammar_points=grammar,vocabulary_set_ids=[vocab],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[c1,c2],default_weeks=2)

CURRICULUM = {}
CURRICULUM["A1"] = [
    u("A1",1,"ทักทายและแนะนำตัว",["pronouns","copula"],"greetings_a1","Handle A1 Thai in this topic","Use connected Thai with appropriate register"),
    u("A1",2,"ครอบครัว",["copula","questions"],"family_a1","Handle A1 Thai in this topic","Use connected Thai with appropriate register"),
    u("A1",3,"บ้านและสถานที่",["questions","negation"],"home_a1","Handle A1 Thai in this topic","Use connected Thai with appropriate register"),
    u("A1",4,"ชีวิตประจำวัน",["negation","classifiers"],"daily_a1","Handle A1 Thai in this topic","Use connected Thai with appropriate register"),
    u("A1",5,"อาหารและการซื้อของ",["classifiers","location"],"food_a1","Handle A1 Thai in this topic","Use connected Thai with appropriate register"),
    u("A1",6,"สถานที่และทิศทาง",["location","politeness"],"places_a1","Handle A1 Thai in this topic","Use connected Thai with appropriate register"),
    u("A1",7,"การขอความช่วยเหลือ",["politeness","requests"],"greetings_a1","Handle A1 Thai in this topic","Use connected Thai with appropriate register"),
    u("A1",8,"ทบทวน A1",["requests","pronouns"],"family_a1","Handle A1 Thai in this topic","Use connected Thai with appropriate register"),
]
CURRICULUM["A2"] = [
    u("A2",1,"เวลาและแผนการ",["word_order","possessives"],"time_a2","Handle A2 Thai in this topic","Use connected Thai with appropriate register"),
    u("A2",2,"การเดินทาง",["possessives","time"],"travel_a2","Handle A2 Thai in this topic","Use connected Thai with appropriate register"),
    u("A2",3,"สุขภาพ",["time","aspect"],"health_a2","Handle A2 Thai in this topic","Use connected Thai with appropriate register"),
    u("A2",4,"บริการในชีวิตประจำวัน",["aspect","future"],"daily_a1","Handle A2 Thai in this topic","Use connected Thai with appropriate register"),
    u("A2",5,"การเปรียบเทียบ",["future","past"],"time_a2","Handle A2 Thai in this topic","Use connected Thai with appropriate register"),
    u("A2",6,"การสื่อสารอย่างสุภาพ",["past","comparatives"],"travel_a2","Handle A2 Thai in this topic","Use connected Thai with appropriate register"),
    u("A2",7,"เหตุการณ์ในอดีต",["comparatives","modality"],"health_a2","Handle A2 Thai in this topic","Use connected Thai with appropriate register"),
    u("A2",8,"ทบทวน A2",["modality","word_order"],"daily_a1","Handle A2 Thai in this topic","Use connected Thai with appropriate register"),
]
CURRICULUM["B1"] = [
    u("B1",1,"การศึกษา",["serial_verbs","result"],"education_b1","Handle B1 Thai in this topic","Use connected Thai with appropriate register"),
    u("B1",2,"การทำงาน",["result","relative"],"work_b1","Handle B1 Thai in this topic","Use connected Thai with appropriate register"),
    u("B1",3,"เหตุผลและจุดประสงค์",["relative","conditional"],"study_b1","Handle B1 Thai in this topic","Use connected Thai with appropriate register"),
    u("B1",4,"เงื่อนไขและแผนการ",["conditional","cause_purpose"],"education_b1","Handle B1 Thai in this topic","Use connected Thai with appropriate register"),
    u("B1",5,"ประโยคขยาย",["cause_purpose","reported"],"work_b1","Handle B1 Thai in this topic","Use connected Thai with appropriate register"),
    u("B1",6,"ลำดับเหตุการณ์",["reported","modality"],"study_b1","Handle B1 Thai in this topic","Use connected Thai with appropriate register"),
    u("B1",7,"การแก้ปัญหา",["modality","connectors"],"education_b1","Handle B1 Thai in this topic","Use connected Thai with appropriate register"),
    u("B1",8,"ทบทวน B1",["connectors","serial_verbs"],"work_b1","Handle B1 Thai in this topic","Use connected Thai with appropriate register"),
]
CURRICULUM["B2"] = [
    u("B2",1,"คำพูดรายงาน",["passive","causative"],"society_b2","Handle B2 Thai in this topic","Use connected Thai with appropriate register"),
    u("B2",2,"รูปประโยคถูกกระทำ",["causative","concession"],"environment_b2","Handle B2 Thai in this topic","Use connected Thai with appropriate register"),
    u("B2",3,"หลักฐานและการคาดคะเน",["concession","subordination"],"technology_b2","Handle B2 Thai in this topic","Use connected Thai with appropriate register"),
    u("B2",4,"ความขัดแย้งและการยอมรับ",["subordination","aspect"],"society_b2","Handle B2 Thai in this topic","Use connected Thai with appropriate register"),
    u("B2",5,"เศรษฐกิจ",["aspect","reported"],"environment_b2","Handle B2 Thai in this topic","Use connected Thai with appropriate register"),
    u("B2",6,"ประเด็นสังคม",["reported","connectors"],"technology_b2","Handle B2 Thai in this topic","Use connected Thai with appropriate register"),
    u("B2",7,"สื่อและแหล่งข้อมูล",["connectors","relative"],"society_b2","Handle B2 Thai in this topic","Use connected Thai with appropriate register"),
    u("B2",8,"ทบทวน B2",["relative","passive"],"environment_b2","Handle B2 Thai in this topic","Use connected Thai with appropriate register"),
]
CURRICULUM["C1"] = [
    u("C1",1,"ภาษาทางการ",["nominalization","hedging"],"economy_c1","Handle C1 Thai in this topic","Use connected Thai with appropriate register"),
    u("C1",2,"การเขียนเชิงวิชาการ",["hedging","embedded_questions"],"governance_c1","Handle C1 Thai in this topic","Use connected Thai with appropriate register"),
    u("C1",3,"ประโยคซับซ้อน",["embedded_questions","formal_register"],"academic_c1","Handle C1 Thai in this topic","Use connected Thai with appropriate register"),
    u("C1",4,"การจัดโครงสร้างข้อมูล",["formal_register","academic_argument"],"economy_c1","Handle C1 Thai in this topic","Use connected Thai with appropriate register"),
    u("C1",5,"การสื่อสารในองค์กร",["academic_argument","information_structure"],"governance_c1","Handle C1 Thai in this topic","Use connected Thai with appropriate register"),
    u("C1",6,"การโต้แย้งเชิงวิชาการ",["information_structure","register_shift"],"academic_c1","Handle C1 Thai in this topic","Use connected Thai with appropriate register"),
    u("C1",7,"ภาษานโยบายและสื่อ",["register_shift","pragmatics"],"economy_c1","Handle C1 Thai in this topic","Use connected Thai with appropriate register"),
    u("C1",8,"ทบทวน C1",["pragmatics","nominalization"],"governance_c1","Handle C1 Thai in this topic","Use connected Thai with appropriate register"),
]
CURRICULUM["C2"] = [
    u("C2",1,"ความหมายเชิงปริบท",["rhetoric","literary"],"media_c2","Handle C2 Thai in this topic","Use connected Thai with appropriate register"),
    u("C2",2,"วาทศิลป์",["literary","translation"],"literary_c2","Handle C2 Thai in this topic","Use connected Thai with appropriate register"),
    u("C2",3,"การแปล",["translation","discourse_analysis"],"academic_c1","Handle C2 Thai in this topic","Use connected Thai with appropriate register"),
    u("C2",4,"การวิเคราะห์วาทกรรม",["discourse_analysis","academic_argument"],"media_c2","Handle C2 Thai in this topic","Use connected Thai with appropriate register"),
    u("C2",5,"ภาษาวรรณกรรม",["academic_argument","information_structure"],"literary_c2","Handle C2 Thai in this topic","Use connected Thai with appropriate register"),
    u("C2",6,"ภาษาวิชาชีพ",["information_structure","pragmatics"],"academic_c1","Handle C2 Thai in this topic","Use connected Thai with appropriate register"),
    u("C2",7,"การสังเคราะห์หลายแหล่ง",["pragmatics","register_shift"],"media_c2","Handle C2 Thai in this topic","Use connected Thai with appropriate register"),
    u("C2",8,"ประเมินรวม C2",["register_shift","rhetoric"],"literary_c2","Handle C2 Thai in this topic","Use connected Thai with appropriate register"),
]

ASSESSMENT_BANK = [
    AssessmentQuestion(id="th-a1-001",skill="vocabulary",difficulty="A1",question="What does สวัสดี mean?",options=["hello","goodbye","water","ticket"],correct="hello"),
    AssessmentQuestion(id="th-a1-002",skill="grammar",difficulty="A1",question="Which sentence is negative?",options=["ผมไม่กินกาแฟ","ผมกินกาแฟ","ผมกำลังกินกาแฟ","ผมจะกินกาแฟ"],correct="ผมไม่กินกาแฟ"),
    AssessmentQuestion(id="th-a1-003",skill="grammar",difficulty="A1",question="Which classifier is used for books?",options=["เล่ม","คน","ใบ","ตัว"],correct="เล่ม"),
    AssessmentQuestion(id="th-a2-004",skill="grammar",difficulty="A2",question="Which marker commonly expresses ongoing action?",options=["กำลัง","จะ","แล้ว","ไม่"],correct="กำลัง"),
    AssessmentQuestion(id="th-a2-005",skill="vocabulary",difficulty="A2",question="What does ตั๋ว mean?",options=["ticket","medicine","office","evidence"],correct="ticket"),
    AssessmentQuestion(id="th-b1-006",skill="grammar",difficulty="B1",question="Which expresses purpose?",options=["เพื่อ","แต่","ไหม","แล้ว"],correct="เพื่อ"),
    AssessmentQuestion(id="th-b1-007",skill="grammar",difficulty="B1",question="Which introduces a relative clause?",options=["ที่","เพราะ","จะ","ไม่"],correct="ที่"),
    AssessmentQuestion(id="th-b2-008",skill="grammar",difficulty="B2",question="Which is passive?",options=["เขาถูกเชิญไปประชุม","เขาเชิญเพื่อนไปประชุม","เขาจะประชุม","เขาประชุมทุกวัน"],correct="เขาถูกเชิญไปประชุม"),
    AssessmentQuestion(id="th-b2-009",skill="vocabulary",difficulty="B2",question="What does หลักฐาน mean?",options=["evidence","ticket","family","market"],correct="evidence"),
    AssessmentQuestion(id="th-c1-010",skill="academic",difficulty="C1",question="Which sentence uses academic hedging?",options=["ผลลัพธ์อาจแตกต่างกัน","ผลลัพธ์แน่นอนเสมอ","สวัสดีครับ","ฉันไปตลาด"],correct="ผลลัพธ์อาจแตกต่างกัน"),
    AssessmentQuestion(id="th-c1-011",skill="formal",difficulty="C1",question="Which is formal administrative language?",options=["กรุณายื่นเอกสารภายในวันที่กำหนด","ไปไหนมา","กินข้าวหรือยัง","สวัสดี"],correct="กรุณายื่นเอกสารภายในวันที่กำหนด"),
    AssessmentQuestion(id="th-c2-012",skill="discourse",difficulty="C2",question="What should translation preserve?",options=["meaning, register and discourse function","word count only","literal order only","punctuation only"],correct="meaning, register and discourse function"),
]
