"""Sundanese (Basa Sunda) foundation data for JUBA LISAN."""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic,
    VocabularyEntry, VocabularySet, PhrasebookCategory,
    PhrasebookEntry, AssessmentQuestion,
)

LEVELS=["A1","A2","B1","B2","C1","C2"]
_GRAMMAR=[
("pronouns","Kecap gaganti jalma","A1","grammar","Gunakeun abdi, anjeun, manéhna jeung urang dina paguneman dasar.","Abdi murid."),
("nominal","Kalimat nominal","A1","grammar","Nyusun kalimat idéntitas jeung katerangan basajan.","Ieu imah abdi."),
("present","Kagiatan sapopoé","A1","verbs","Ngajelaskeun kagiatan anu keur dilakukeun atawa biasa dilakukeun.","Abdi diajar basa Sunda."),
("questions","Patarosan dasar","A1","communication","Gunakeun saha, naon, dimana, iraha, kumaha pikeun naroskeun informasi.","Anjeun ti mana?"),
("negation","Panyangkalan","A1","grammar","Gunakeun henteu jeung teu pikeun nyangkal pernyataan.","Abdi henteu ngartos."),
("demonstratives","Kecap panuduh","A1","grammar","Gunakeun ieu jeung éta pikeun nuduhkeun jalma atawa barang.","Ieu buku abdi."),
("possessive","Kapamilikan","A1","grammar","Nyatakeun kapamilikan ku susunan kecap anu alami.","Ieu indung abdi."),
("location","Tempat jeung lokasi","A1","grammar","Ngajelaskeun tempat ku aya, di, ka jeung ti.","Buku aya dina méja."),
("past","Kajadian katukang","A2","verbs","Ngajelaskeun kajadian anu geus kaliwat ku katerangan waktu jeung konteks.","Kamari abdi indit ka pasar."),
("future","Rencana ka hareup","A2","verbs","Ngajelaskeun rencana jeung kajadian anu bakal datang.","Isukan abdi rék indit."),
("aspect","Aspék kagiatan","A2","verbs","Ngabédakeun kagiatan anu keur lumangsung, geus réngsé jeung biasa.","Abdi keur maca."),
("politeness","Undak-usuk basa","A2","register","Milih kecap anu merenah pikeun kaayaan jeung lawan nyarita.","Punten, tiasa ngabantosan abdi?"),
("comparatives","Babandingan","A2","adjectives","Ngabandingkeun jalma, barang jeung kaayaan.","Ieu leuwih gedé tibatan éta."),
("imperatives","Parentah jeung pamundut","A2","communication","Méré parentah atawa pamundut kalayan sopan.","Mangga calik."),
("conjunctions","Panyambung kalimat","A2","syntax","Nyambungkeun gagasan ku sabab, tapi, tuluy jeung lamun.","Abdi datang sabab aya rapat."),
("relative","Kalimat relatif","B1","syntax","Nerangkeun jalma atawa barang ku kalimat tambahan.","Buku anu ku abdi dibaca téh alus."),
("subordination","Kalimat majemuk","B1","syntax","Ngawangun hubungan sabab, waktu, kaayaan jeung tujuan.","Lamun hujan, urang cicing di bumi."),
("conditional","Kaayaan sarat","B1","syntax","Ngajelaskeun akibat tina hiji sarat.","Lamun aya waktos, abdi bakal datang."),
("reported-speech","Carita tina omongan","B1","discourse","Nyaritakeun deui informasi anu ditepikeun ku batur.","Anjeunna nyarios yén anjeunna badé datang."),
("habitual","Kabiasaan","B1","verbs","Ngajelaskeun kagiatan anu lumangsung sacara rutin.","Unggal isuk abdi biasa olahraga."),
("passive","Kalimat pasif","B1","syntax","Nempatkeun hasil atawa objék kagiatan salaku fokus.","Surat éta parantos dikirim."),
("connectors","Panyambung wacana","B1","discourse","Ngatur alur pamadegan ku ku kituna, sanajan, tapi jeung salian ti éta.","Sanajan capé, anjeunna tetep damel."),
("causative","Sabab-akibat","B2","verbs","Ngajelaskeun yén hiji pihak nyababkeun parobahan atawa tindakan.","Guru ngajarkeun murid maca."),
("applicative","Kauntungan tindakan","B2","verbs","Ngajelaskeun saha atawa naon anu meunang mangpaat tina tindakan.","Abdi mésérkeun ibu kembang."),
("reciprocal","Tindakan silih","B2","verbs","Ngajelaskeun tindakan anu dilakukeun ku dua pihak atawa leuwih ka silih.","Maranehna silih tulungan."),
("complex-relative","Relatif kompléks","B2","syntax","Ngagunakeun kalimat relatif dina struktur anu leuwih panjang.","Dokumén anu kamari ku anjeunna dikirim parantos ditampi."),
("indirect-question","Patarosan henteu langsung","B2","syntax","Nempatkeun patarosan dina kalimat anu leuwih gedé.","Abdi henteu terang anjeunna cicing dimana."),
("discourse","Struktur wacana","B2","discourse","Ngatur bubuka, bukti, kontras jeung kacindekan dina wacana.","Kahiji, urang bakal nalungtik masalahna."),
("subjunctive","Kahayang jeung saran","C1","pragmatics","Ngébréhkeun kahayang, saran, tujuan jeung kawajiban sacara merenah.","Hadé urang ngabahas éta ayeuna."),
("nominalization","Ngawangun nomina","C1","word-formation","Ngarobah tindakan atawa kualitas jadi konsép pikeun gaya resmi.","Panalungtikan ngeunaan basa terus dilakukeun."),
("information-structure","Struktur informasi","C1","discourse","Ngatur topik, fokus jeung informasi anyar sacara écés.","Nu paling penting nyaéta hasil panalungtikan."),
("formal-register","Gaya resmi","C1","register","Milih basa anu merenah pikeun dokumén jeung komunikasi institusional.","Mangga kirimkeun dokumén sateuacan tanggal anu ditangtukeun."),
("idioms","Babasan jeung paribasa","C2","lexis","Ngartos harti idiomatis dumasar kana kontéks budaya.","Ulah ngukur baju sasereg awak."),
("rhetoric","Rétorika jeung arguméntasi","C2","rhetoric","Ngawangun argumén anu saimbang kalayan bukti jeung bantahan.","Argumén éta kuat, tapi buktina masih kawates."),
]
GRAMMAR_TOPICS=[GrammarTopic(slug=s,title=t,level=l,category=c,summary=sm,explanation=sm,examples=[GrammarExample(text=e)]) for s,t,l,c,sm,e in _GRAMMAR]

_VOCAB={
"A1":[("Salam","wilujeng","phrase","greetings","Wilujeng enjing!"),("Identitas","ngaran","noun","name","Saha ngaran anjeun?"),("Kulawarga","indung","noun","mother","Indung abdi aya di bumi."),("Imah","imah","noun","house","Ieu imah abdi."),("Rutinitas","isuk","noun","morning","Unggal isuk abdi diajar."),("Kadaharan","dahareun","noun","food","Dahareun ieu ngeunah."),("Tempat","pasar","noun","market","Pasar aya di ditu."),("Pitulung","pitulung","noun","help","Abdi peryogi pitulung.")],
"A2":[("Lalampahan","lalampahan","noun","journey","Lalampahan urang dimimitian isukan."),("Kaséhatan","dokter","noun","doctor","Abdi badé ka dokter."),("Balanja","harga","noun","price","Sabaraha hargana?"),("Cuaca","hujan","noun","rain","Dinten ieu hujan.")],
"B1":[("Pagawean","pangalaman","noun","experience","Abdi gaduh pangalaman tilu taun."),("Atikan","atikan","noun","education","Atikan penting pikeun masarakat."),("Masarakat","lingkungan","noun","environment","Urang kudu ngajaga lingkungan."),("Pamadegan","pamadegan","noun","opinion","Kumaha pamadegan anjeun?")],
"B2":[("Bisnis","usaha","noun","business","Usahana ngembang gancang."),("Téknologi","téknologi","noun","technology","Téknologi ngarobah cara urang damel."),("Média","warta","noun","news","Warta éta geus sumebar."),("Administrasi","kabijakan","noun","policy","Kabijakan anyar geus diterbitkeun.")],
"C1":[("Panalungtikan","analisis","noun","analysis","Analisis data nunjukkeun pola anyar."),("Hukum","perjangjian","noun","agreement","Perjangjian éta geus ditandatanganan."),("Akademik","makalah","noun","paper","Makalah ieu ngabahas basa Sunda."),("Laporan","laporan","noun","report","Laporan resmi geus dikirim.")],
"C2":[("Rétorika","argumén","noun","argument","Arguménna dumasar kana bukti."),("Linguistik","kontéks","noun","context","Harti kecap gumantung kana kontéks."),("Sastra","gaya","noun","style","Pangarang ngagunakeun gaya anu has."),("Tarjamahan","padanan","noun","equivalent","Tarjamahan kudu néangan padanan anu merenah.")]
}
VOCABULARY_SETS=[]
for level,rows in _VOCAB.items():
    for i,(topic,word,pos,definition,example) in enumerate(rows,1):
        VOCABULARY_SETS.append(VocabularySet(id=f"su-{level.lower()}-{i}",level=level,topic=topic,unit_ref=f"su-{level.lower()}-unit-{i}",words=[VocabularyEntry(word=word,pos=pos,definition=definition,example=example)]))

_PHRASES=[
("Salam",("Wilujeng sumping!","welcoming","neutral"),("Kumaha damang?","asking how someone is","neutral"),("Hatur nuhun.","thanking","neutral")),
("Perkenalan",("Ngaran abdi Dadan.","introducing yourself","neutral"),("Abdi ti Bandung.","saying origin","neutral"),("Punten, saha ngaran anjeun?","asking a name","polite")),
("Sapopoé",("Abdi badé angkat heula.","daily routine","neutral"),("Abdi mulih sonten.","daily routine","neutral"),("Abdi henteu ngartos.","asking for clarification","neutral")),
("Balanja",("Sabaraha hargana?","asking the price","neutral"),("Mangga, abdi nyandak ieu.","buying an item","neutral"),("Tiasa mayar nganggo kartu?","asking about payment","polite")),
("Pitunjuk",("Dimana stasina?","asking a location","neutral"),("Mangga lempeng waé.","giving directions","neutral"),("Belok ka katuhu.","giving directions","neutral")),
("Dahareun",("Mangga pasihan cai.","ordering a drink","polite"),("Abdi hoyong ieu.","ordering food","neutral"),("Dahareun ieu ngeunah.","commenting on food","neutral")),
("Kaséhatan",("Sirah abdi nyeri.","describing a symptom","neutral"),("Abdi kedah ka dokter.","seeking care","neutral"),("Ayeuna abdi parantos langkung saé.","describing recovery","neutral")),
("Pagawean",("Abdi damel di dieu.","talking about work","neutral"),("Iraha rapatna?","asking about a meeting","neutral"),("Urang tepang énjing.","making an arrangement","neutral")),
("Lalampahan",("Abdi gaduh tikét.","travel information","neutral"),("Iraha karéta angkat?","asking departure time","neutral"),("Paspor abdi leungit.","reporting a problem","neutral")),
("Pamadegan",("Numutkeun pamadegan abdi...","giving an opinion","neutral"),("Abdi satuju.","agreeing","neutral"),("Abdi kirang satuju.","disagreeing politely","polite")),
("Resmi",("Mangga tampi pamundut abdi.","formal request","formal"),("Abdi hoyong naroskeun inpormasi langkung seueur.","formal inquiry","formal"),("Hatur nuhun kana gawé barengna.","formal thanks","formal")),
("Akademik",("Panalungtikan ieu nunjukkeun hasil anyar.","research discussion","formal"),("Mangga tingali sumber ieu.","academic reference","formal"),("Kacindekan gumantung kana data.","academic discussion","formal")),
("Babasan",("Wilujeng damel.","acknowledging work","neutral"),("Mugia lancar!","wishing success","neutral"),("Henteu kunanaon.","reassuring someone","neutral")),
]
PHRASEBOOK_CATEGORIES=[PhrasebookCategory(id=f"su-phrase-{i}",level="A1" if i<=6 else "B1",situation=situation,icon="💬",phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in entries]) for i,(situation,*entries) in enumerate(_PHRASES,1)]

_THEMES={
"A1":["Salam jeung perkenalan","Kulawarga","Imah","Rutinitas","Kadaharan","Tempat","Pitulung","Ulangan"],
"A2":["Lalampahan","Kaséhatan","Balanja","Cuaca","Rencana","Palayanan","Babandingan","Ulangan"],
"B1":["Pagawean","Atikan","Masarakat","Pamadegan","Kajadian","Hubungan","Warta","Ulangan"],
"B2":["Bisnis","Téknologi","Média","Administrasi","Lingkungan","Budaya","Arguméntasi","Ulangan"],
"C1":["Panalungtikan","Hukum","Akademik","Laporan","Analisis","Komunikasi resmi","Diskusi","Ulangan"],
"C2":["Rétorika","Linguistik","Sastra","Tarjamahan","Kontéks","Gaya basa","Arguméntasi kompléks","Ulangan"]}
_GRAM={
"A1":["pronouns","nominal","present","questions","negation","demonstratives","possessive","location"],
"A2":["past","future","aspect","politeness","comparatives","imperatives","conjunctions","politeness"],
"B1":["relative","subordination","conditional","reported-speech","habitual","passive","connectors","subordination"],
"B2":["causative","applicative","reciprocal","complex-relative","indirect-question","discourse","causative","reciprocal"],
"C1":["subjunctive","nominalization","information-structure","formal-register","subjunctive","nominalization","information-structure","formal-register"],
"C2":["idioms","rhetoric","idioms","rhetoric","idioms","rhetoric","idioms","rhetoric"]}
CURRICULUM={}
for level in LEVELS:
    CURRICULUM[level]=[]
    for n,title in enumerate(_THEMES[level],1):
        vid=f"su-{level.lower()}-{min(n,8 if level=='A1' else 4)}"
        CURRICULUM[level].append(CurriculumUnit(id=f"su-{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=[_GRAM[level][n-1]],vocabulary_set_ids=[vid],lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],competency_checklist=[f"Communicate in Sundanese about {title.lower()}",f"Apply {level} grammar in context"],default_weeks=2))

ASSESSMENT_BANK=[
AssessmentQuestion(id="su-a1-001",skill="vocabulary",difficulty="A1",question="Which word means “name”?",options=["ngaran","imah","pasar","pitulung"],correct="ngaran"),
AssessmentQuestion(id="su-a1-002",skill="grammar",difficulty="A1",question="Choose the natural sentence for “I am a student.”",options=["Abdi murid.","Murid abdi téh?","Abdi muridna.","Murid téh abdi."],correct="Abdi murid."),
AssessmentQuestion(id="su-a1-003",skill="grammar",difficulty="A1",question="Which sentence expresses a current activity?",options=["Abdi diajar basa Sunda.","Kamari abdi indit.","Isukan abdi badé indit.","Abdi henteu ngartos."],correct="Abdi diajar basa Sunda."),
AssessmentQuestion(id="su-a1-004",skill="communication",difficulty="A1",question="Which phrase asks where someone is from?",options=["Anjeun ti mana?","Kumaha damang?","Hatur nuhun.","Mangga calik."],correct="Anjeun ti mana?"),
AssessmentQuestion(id="su-a1-005",skill="vocabulary",difficulty="A1",question="Which word means “mother”?",options=["indung","bapa","lanceuk","murid"],correct="indung"),
AssessmentQuestion(id="su-a1-006",skill="grammar",difficulty="A1",question="Which sentence is negative?",options=["Abdi henteu ngartos.","Abdi ngartos.","Abdi diajar.","Abdi sumping."],correct="Abdi henteu ngartos."),
AssessmentQuestion(id="su-a1-007",skill="vocabulary",difficulty="A1",question="Which word means “house/home”?",options=["imah","pasar","hujan","harga"],correct="imah"),
AssessmentQuestion(id="su-a1-008",skill="communication",difficulty="A1",question="Which phrase thanks someone?",options=["Hatur nuhun.","Wilujeng enjing.","Saha ngaran anjeun?","Dimana pasarna?"],correct="Hatur nuhun."),
AssessmentQuestion(id="su-a1-009",skill="communication",difficulty="A1",question="Which phrase asks for help?",options=["Abdi peryogi pitulung.","Wilujeng sumping.","Abdi ti Bandung.","Kumaha damang?"],correct="Abdi peryogi pitulung."),
AssessmentQuestion(id="su-a1-010",skill="grammar",difficulty="A1",question="Which phrase uses a demonstrative?",options=["Ieu buku abdi.","Abdi murid.","Abdi diajar.","Hatur nuhun."],correct="Ieu buku abdi."),
AssessmentQuestion(id="su-b1-011",skill="grammar",difficulty="B1",question="Which sentence expresses a condition?",options=["Lamun aya waktos, abdi bakal datang.","Abdi parantos sumping.","Abdi biasa olahraga.","Ieu buku abdi."],correct="Lamun aya waktos, abdi bakal datang."),
AssessmentQuestion(id="su-b1-012",skill="grammar",difficulty="B1",question="Which sentence reports another person's speech?",options=["Anjeunna nyarios yén anjeunna badé datang.","Abdi badé datang.","Abdi keur maca.","Buku éta alus."],correct="Anjeunna nyarios yén anjeunna badé datang."),
AssessmentQuestion(id="su-b2-013",skill="grammar",difficulty="B2",question="Which sentence expresses a reciprocal action?",options=["Maranehna silih tulungan.","Abdi mésér buku.","Anjeunna datang.","Abdi keur maca."],correct="Maranehna silih tulungan."),
AssessmentQuestion(id="su-c1-014",skill="formal",difficulty="C1",question="Which expression is suitable for a formal request?",options=["Mangga tampi pamundut abdi.","Vérsi pondokna kumaha?","Saha?","Hayu urang indit!"],correct="Mangga tampi pamundut abdi."),
]
