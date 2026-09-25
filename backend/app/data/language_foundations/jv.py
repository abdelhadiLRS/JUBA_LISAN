"""Javanese A1-C2 foundation data for JUBA LISAN.

The foundation uses practical Javanese with explicit attention to speech levels
(ngoko and krama), common affixes, voice/focus, clause linking, and formal
register. Examples are intentionally native-language-first so lesson generation
can ground activities in Javanese rather than generic English templates.
"""
from app.data._types import (
    AssessmentQuestion,
    CurriculumUnit,
    GrammarExample,
    GrammarTopic,
    PhrasebookCategory,
    PhrasebookEntry,
    VocabularyEntry,
    VocabularySet,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def g(slug, title, level, summary, examples, category="grammar"):
    return GrammarTopic(
        slug=slug,
        title=title,
        level=level,
        category=category,
        summary=summary,
        explanation=summary,
        examples=[GrammarExample(text=x) for x in examples],
    )


GRAMMAR_TOPICS = [
    g("pronouns", "Personal reference", "A1", "Use aku, kowe, dheweke, kita and panjenengan appropriately.", ["Aku siswa.", "Panjenengan guru."]),
    g("nominal", "Nominal sentences", "A1", "Build identity and descriptive sentences without forcing an English-style copula.", ["Iki omahku.", "Dheweke guru."]),
    g("present", "Everyday actions", "A1", "Describe current and habitual actions in simple clauses.", ["Aku sinau basa Jawa.", "Dheweke saben dina kerja."]),
    g("questions", "Basic questions", "A1", "Ask identity, location, quantity and simple information questions.", ["Kepiye kabarmu?", "Pasar ana ing endi?"]),
    g("negation", "Negation", "A1", "Use ora, dudu and related negative patterns in everyday speech.", ["Aku ora ngerti.", "Iki dudu omahku."]),
    g("demonstratives", "Demonstratives", "A1", "Point to nearby and distant people or things.", ["Iki bukuku.", "Kuwi omahe."]),
    g("possessive", "Possession", "A1", "Express possession through noun phrases and possessive forms.", ["Iki omahku.", "Buku iki duweke Sari."]),
    g("location", "Location and prepositions", "A1", "Describe location with ing, saka, menyang and common spatial expressions.", ["Buku ana ing meja.", "Aku manggon ing Yogyakarta."]),
    g("plural_quantity", "Plurality and quantity", "A2", "Express groups, quantities and classifiers through context and numerals.", ["Ana telung siswa.", "Akeh wong teka."]),
    g("past", "Past and completed events", "A2", "Narrate completed events with temporal adverbs and appropriate verbal forms.", ["Wingi aku menyang pasar.", "Dheweke wis mangan."]),
    g("future_intention", "Future and intention", "A2", "Express plans, intention and expected events with arep and temporal context.", ["Aku arep kerja.", "Sesuk dheweke teka."]),
    g("progressive", "Ongoing actions", "A2", "Describe actions in progress using lagi and contextual aspect.", ["Aku lagi maca.", "Dheweke lagi sinau."]),
    g("imperative", "Imperatives and polite requests", "A2", "Give instructions and make requests while adjusting politeness.", ["Mangga lungguh.", "Tulung baleni maneh."]),
    g("comparison", "Comparison", "A2", "Compare people and things with luwih, kurang and paling.", ["Iki luwih gedhe.", "Dheweke paling cepet."]),
    g("time", "Time and sequence", "A2", "Talk about dates, schedules, frequency and sequence.", ["Aku teka jam wolu.", "Sawise mangan, aku kerja."]),
    g("speech_levels", "Ngoko and krama speech levels", "A2", "Choose everyday ngoko or respectful krama vocabulary according to relationship and setting.", ["Aku wis mangan.", "Panjenengan sampun dhahar."]),
    g("affix_ngoko", "Common verbal affixes", "B1", "Recognize and produce common N- and other verbal forms in everyday Javanese.", ["Aku maca buku.", "Dheweke nulis surat."]),
    g("affix_formal", "Verbal derivation and formal forms", "B1", "Use productive affixes and distinguish informal from more formal lexical choices.", ["Dheweke nyerat layang.", "Aku ngirim pesen."]),
    g("modality", "Ability, necessity and permission", "B1", "Express ability, obligation, permission and intention.", ["Aku bisa teka.", "Kowe kudu sinau."]),
    g("conditional", "Conditional clauses", "B1", "Build real and hypothetical conditions with yen and related connectors.", ["Yen udan, aku ora lunga.", "Yen duwe wektu, ayo ketemu."]),
    g("relative", "Relative clauses", "B1", "Modify nouns and identify people or things through relative clauses.", ["Buku sing tak waca apik.", "Wong sing teka kuwi guruku."]),
    g("cause_purpose", "Cause, purpose and result", "B1", "Connect reasons, goals and consequences clearly.", ["Aku ora lunga amarga udan.", "Aku sinau supaya lulus."]),
    g("serial_verbs", "Serial and chained actions", "B1", "Sequence actions naturally without overusing conjunctions.", ["Dheweke teka nggawa buku.", "Aku lunga tuku panganan."]),
    g("reported", "Reported speech", "B2", "Report statements, questions and requests while preserving speech level and meaning.", ["Dheweke kandha yen sesuk teka.", "Guru takon apa aku wis siap."]),
    g("passive", "Passive and voice patterns", "B2", "Use common di- and related passive constructions and distinguish actor prominence.", ["Buku kuwi diwaca Sari.", "Pintu dibukak dening petugas."]),
    g("aspect", "Aspect and event viewpoint", "B2", "Distinguish ongoing, completed and habitual interpretations through aspectual context.", ["Aku lagi maca.", "Aku wis maca buku kuwi."]),
    g("concession", "Contrast and concession", "B2", "Connect opposing ideas with nanging, sanajan and related structures.", ["Sanajan udan, dheweke tetep teka.", "Aku sibuk, nanging aku teka."]),
    g("discourse", "Discourse cohesion", "B2", "Organize longer explanations with temporal, causal and contrastive connectors.", ["Kaping pisan, masalah iki kudu ditliti. Banjur solusi digoleki."]),
    g("nominalization", "Nominalization", "C1", "Use nominal forms and abstract noun phrases in formal and analytical writing.", ["Pangembangan pendidikan mbutuhake wektu.", "Panganggone data kudu ati-ati."]),
    g("hedging", "Academic hedging and stance", "C1", "Qualify claims and separate evidence, interpretation and uncertainty.", ["Asil iki bisa uga nuduhake owah-owahan.", "Pratelan iki perlu ditliti maneh."]),
    g("subordination", "Complex subordination", "C1", "Build multi-clause sentences expressing logical and temporal relations.", ["Yen data wis diverifikasi, asil kasebut bisa diterbitake."]),
    g("embedded_questions", "Embedded questions", "C1", "Embed questions inside reports, requests and formal explanations.", ["Aku ora ngerti kapan dheweke teka.", "Dheweke takon apa rapat wis diwiwiti."]),
    g("information_structure", "Topic and focus", "C1", "Control emphasis through word order, context and discourse prominence.", ["Masalah iki sing arep kita rembug dina iki.", "Sing penting yaiku bukti kasebut."]),
    g("formal_register", "Formal and institutional Javanese", "C1", "Adapt vocabulary, krama choices and sentence structure for institutional communication.", ["Panyuwunan kasebut badhe dipunproses miturut aturan."]),
    g("argumentation", "Academic argumentation", "C1", "Present claims, evidence, counterarguments and conclusions coherently.", ["Adhedhasar data kasebut, bisa disimpulake yen kabijakan iki perlu dievaluasi."]),
    g("pragmatics", "Pragmatics and politeness", "C2", "Manage indirectness, respect, social distance and implied meaning.", ["Menawi kersa, saged dipunrembag malih."]),
    g("rhetoric", "Rhetorical and literary style", "C2", "Analyze metaphor, repetition, parallelism and stylistic variation.", ["Tembung-tembung kasebut mbangun gambaran sing kuwat."]),
    g("translation", "Translation precision", "C2", "Preserve meaning, speech level, register and discourse function across contexts.", ["Terjemahan kudu njaga makna lan unggah-ungguh basa."]),
    g("discourse_analysis", "Discourse analysis and register shifting", "C2", "Analyze genre, cohesion, stance and movement between ngoko, krama and written registers.", ["Gaya basa ing dokumen resmi beda karo basa pacelathon saben dina."]),
]


def v(i, level, topic, words):
    return VocabularySet(
        id=i,
        level=level,
        topic=topic,
        unit_ref=i,
        words=[
            VocabularyEntry(word=w, pos=p, definition=d, example=e)
            for w, p, d, e in words
        ],
    )


VOCABULARY_SETS = [
    v("greetings_a1", "A1", "Salam", [
        ("halo", "phrase", "hello", "Halo, apa kabar?"),
        ("matur nuwun", "phrase", "thank you", "Matur nuwun."),
        ("sugeng enjing", "phrase", "good morning", "Sugeng enjing, Pak."),
        ("jeneng", "noun", "name", "Jenengmu sapa?"),
    ]),
    v("identity_a1", "A1", "Identitas", [
        ("siswa", "noun", "student", "Aku siswa."),
        ("guru", "noun", "teacher", "Dheweke guru."),
        ("wong", "noun", "person", "Dheweke wong apik."),
        ("kanca", "noun", "friend", "Dheweke kancaku."),
    ]),
    v("family_a1", "A1", "Kulawarga", [
        ("ibu", "noun", "mother", "Ibuku ana ing omah."),
        ("bapak", "noun", "father", "Bapakku kerja."),
        ("kakang", "noun", "older sibling", "Kakangku wis mulih."),
        ("adik", "noun", "younger sibling", "Adikku sekolah."),
    ]),
    v("home_a1", "A1", "Omah", [
        ("omah", "noun", "house", "Iki omahku."),
        ("kamar", "noun", "room", "Kamar iki resik."),
        ("lawang", "noun", "door", "Lawange mbukak."),
        ("meja", "noun", "table", "Buku ana ing meja."),
    ]),
    v("daily_a1", "A1", "Urip saben dina", [
        ("esuk", "noun", "morning", "Esuk aku kerja."),
        ("dina", "noun", "day", "Dina iki panas."),
        ("kerja", "verb", "work", "Aku kerja saben dina."),
        ("banyu", "noun", "water", "Aku ngombe banyu."),
    ]),
    v("food_a1", "A1", "Panganan", [
        ("nasi", "noun", "rice", "Aku mangan nasi."),
        ("roti", "noun", "bread", "Aku tuku roti."),
        ("teh", "noun", "tea", "Aku ngombe teh."),
        ("panganan", "noun", "food", "Panganan iki enak."),
    ]),
    v("places_a1", "A1", "Panggonan", [
        ("pasar", "noun", "market", "Pasar ana ing kene."),
        ("sekolah", "noun", "school", "Sekolah cedhak omah."),
        ("rumah sakit", "noun", "hospital", "Rumah sakit ana ing kana."),
        ("dalan", "noun", "road", "Dalan iki dawa."),
    ]),
    v("communication_a1", "A1", "Komunikasi", [
        ("pitakon", "noun", "question", "Aku duwe pitakon."),
        ("pitulungan", "noun", "help", "Aku butuh pitulungan."),
        ("ngerti", "verb", "understand", "Aku ora ngerti."),
        ("ngomong", "verb", "speak", "Dheweke ngomong Jawa."),
    ]),
    v("people_a2", "A2", "Wong lan sesambungan", [
        ("tangga", "noun", "neighbor", "Tangga omahku apik."),
        ("tamu", "noun", "guest", "Ana tamu teka."),
        ("kelompok", "noun", "group", "Kelompok iki cilik."),
        ("masyarakat", "noun", "community", "Masyarakat kudu kerja bareng."),
    ]),
    v("travel_a2", "A2", "Lelungan", [
        ("pesawat", "noun", "airplane", "Pesawat mangkat esuk."),
        ("sepur", "noun", "train", "Aku numpak sepur."),
        ("tiket", "noun", "ticket", "Tiket iki larang."),
        ("hotel", "noun", "hotel", "Hotel iki cedhak stasiun."),
    ]),
    v("health_a2", "A2", "Kesehatan", [
        ("dokter", "noun", "doctor", "Aku arep menyang dokter."),
        ("lara", "adjective", "ill", "Sirahku lara."),
        ("obat", "noun", "medicine", "Obat iki kudu diombe."),
        ("rumah sakit", "noun", "hospital", "Dheweke ana ing rumah sakit."),
    ]),
    v("study_b1", "B1", "Sinau", [
        ("sinau", "verb", "study", "Aku sinau basa Jawa."),
        ("tugas", "noun", "assignment", "Tugasku wis rampung."),
        ("ujian", "noun", "exam", "Ujian diwiwiti sesuk."),
        ("panaliten", "noun", "research", "Panaliten iki penting."),
    ]),
    v("work_b1", "B1", "Pakaryan", [
        ("karyawan", "noun", "employee", "Karyawan teka jam wolu."),
        ("rapat", "noun", "meeting", "Rapat diwiwiti saiki."),
        ("pengalaman", "noun", "experience", "Dheweke duwe pengalaman akeh."),
        ("tanggung jawab", "noun", "responsibility", "Iki tanggung jawabku."),
    ]),
    v("society_b2", "B2", "Masyarakat", [
        ("masyarakat", "noun", "society", "Masyarakat terus owah."),
        ("pembangunan", "noun", "development", "Pembangunan kudu lestari."),
        ("kebijakan", "noun", "policy", "Kebijakan anyar lagi dibahas."),
        ("warga", "noun", "citizen", "Warga duwe hak lan kewajiban."),
    ]),
    v("economy_b2", "B2", "Ekonomi", [
        ("ekonomi", "noun", "economy", "Ekonomi daerah saya maju."),
        ("pasar", "noun", "market", "Pasar ngalami owah-owahan."),
        ("investasi", "noun", "investment", "Investasi tambah akeh."),
        ("penghasilan", "noun", "income", "Penghasilan kulawarga mundhak."),
    ]),
    v("media_c1", "C1", "Media", [
        ("informasi", "noun", "information", "Informasi kudu diverifikasi."),
        ("artikel", "noun", "article", "Artikel iki dawa."),
        ("sumber", "noun", "source", "Sumber data kudu cetha."),
        ("wawancara", "noun", "interview", "Wawancara kasebut direkam."),
    ]),
    v("academic_c1", "C1", "Basa akademik", [
        ("panaliten", "noun", "research", "Panaliten iki nggunakake data anyar."),
        ("bukti", "noun", "evidence", "Bukti kasebut durung cukup."),
        ("hipotesis", "noun", "hypothesis", "Hipotesis kudu diuji."),
        ("kesimpulan", "noun", "conclusion", "Kesimpulan adhedhasar data."),
    ]),
    v("institutional_c1", "C1", "Basa resmi", [
        ("aturan", "noun", "regulation", "Aturan kudu dituruti."),
        ("panyuwunan", "noun", "application/request", "Panyuwunan wis ditampa."),
        ("keputusan", "noun", "decision", "Keputusan wis diumumake."),
        ("pelaksanaan", "noun", "implementation", "Pelaksanaan program lagi diawasi."),
    ]),
    v("culture_c2", "C2", "Budaya lan sastra", [
        ("warisan", "noun", "heritage", "Warisan budaya kudu dijaga."),
        ("sastra", "noun", "literature", "Sastra Jawa sugih."),
        ("gambaran", "noun", "imagery", "Gambaran ing teks kasebut kuwat."),
        ("simbol", "noun", "symbol", "Simbol nduweni makna tartamtu."),
    ]),
    v("discourse_c2", "C2", "Wacana lan ragam basa", [
        ("ragam basa", "noun", "language variety", "Ragam basa kudu cocog karo konteks."),
        ("unggah-ungguh", "noun", "speech etiquette", "Unggah-ungguh penting ing basa Jawa."),
        ("makna tersirat", "noun", "implicit meaning", "Makna tersirat kudu diwaca saka konteks."),
        ("istilah", "noun", "term", "Istilah kudu konsisten."),
    ]),
]


def p(i, level, situation, items, register="neutral"):
    return PhrasebookCategory(
        id=i,
        level=level,
        situation=situation,
        icon="💬",
        phrases=[
            PhrasebookEntry(text=t, context=c, register=register)
            for t, c in items
        ],
    )


PHRASEBOOK_CATEGORIES = [
    p("greetings_a1", "A1", "Salam lan kenalan", [
        ("Halo!", "greeting"),
        ("Jenengmu sapa?", "asking a name"),
        ("Sugeng enjing.", "morning greeting"),
    ]),
    p("thanks_a1", "A1", "Matur nuwun lan nyuwun pangapunten", [
        ("Matur nuwun.", "thanks"),
        ("Tulung.", "please/help"),
        ("Nyuwun pangapunten.", "apology"),
    ]),
    p("shopping_a1", "A1", "Blanja", [
        ("Iki pira?", "asking price"),
        ("Aku pengin iki.", "requesting an item"),
        ("Ana warna liyane?", "asking for another option"),
    ]),
    p("directions_a1", "A1", "Arah", [
        ("Pasar ana ing endi?", "asking location"),
        ("Kepiye menyang stasiun?", "asking a route"),
        ("Lurus banjur ngiwa.", "giving directions"),
    ]),
    p("help_a1", "A1", "Pitulungan", [
        ("Tulung aku.", "asking for help"),
        ("Aku ora ngerti.", "saying you do not understand"),
        ("Tulung baleni maneh.", "asking for repetition"),
    ]),
    p("travel_a2", "A2", "Lelungan", [
        ("Tiket bisa tuku ing endi?", "buying a ticket"),
        ("Hotel iki ana ing endi?", "finding a hotel"),
        ("Aku arep konfirmasi pesenan.", "confirming a booking"),
    ]),
    p("health_a2", "A2", "Kesehatan", [
        ("Sirahku lara.", "describing a symptom"),
        ("Aku pengin ketemu dokter.", "requesting medical help"),
        ("Obat iki carane ngombe kepiye?", "asking about medicine"),
    ]),
    p("study_b1", "B1", "Sinau", [
        ("Tulung terangna maneh.", "asking for explanation"),
        ("Tugasku wis rampung.", "discussing an assignment"),
        ("Aku nggunakake sumber iki.", "citing a source"),
    ]),
    p("work_b1", "B1", "Pakaryan", [
        ("Ayo rapate diwiwiti.", "starting a meeting"),
        ("Ayo masalah iki dirembug.", "opening a discussion"),
        ("Laporan bakal tak kirim sesuk.", "work commitment"),
    ]),
    p("public_b2", "B2", "Diskusi umum", [
        ("Masalah iki nduweni sawetara sebab.", "explaining causes"),
        ("Nanging, ana sudut pandang liyane.", "introducing contrast"),
        ("Adhedhasar bukti kasebut...", "introducing evidence"),
    ], "formal"),
    p("academic_c1", "C1", "Diskusi akademik", [
        ("Panaliten iki nuduhake yen...", "stating a finding"),
        ("Asil iki kudu ditafsirake kanthi ati-ati.", "hedging"),
        ("Bab iki perlu ditliti luwih lanjut.", "proposing further research"),
    ], "academic"),
    p("institutional_c1", "C1", "Komunikasi resmi", [
        ("Panyuwunan wis ditampa.", "acknowledging an application"),
        ("Miturut aturan, perkara iki bakal diproses.", "formal procedure"),
        ("Mangga ngirim informasi sing dibutuhake.", "formal request"),
    ], "formal"),
    p("rhetoric_c2", "C2", "Ragam basa lan retorika", [
        ("Ana siji perkara penting sing kudu digatekake.", "foregrounding a point"),
        ("Ayo dipikirake apa panjelasan iki cukup kuwat.", "critical evaluation"),
        ("Bisa uga ana makna liyane ing mburi ukara iki.", "interpreting implicit meaning"),
    ], "formal"),
]


def u(level, number, title, grammar, vocab, a, b):
    return CurriculumUnit(
        id=f"jv-{level.lower()}-{number:02}",
        level=level,
        unit_number=number,
        title=title,
        grammar_points=grammar,
        vocabulary_set_ids=[vocab],
        lesson_types=["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"],
        competency_checklist=[a, b],
        default_weeks=2,
    )


CURRICULUM = {
    "A1": [
        u("A1", 1, "Salam lan kenalan", ["pronouns", "nominal"], "greetings_a1", "Ngucapake salam lan ngenalake awake dhewe", "Ngerti sapaan dhasar"),
        u("A1", 2, "Identitas", ["pronouns", "questions"], "identity_a1", "Nerangake identitas", "Takokake pitakon dhasar"),
        u("A1", 3, "Kulawarga", ["possessive", "demonstratives"], "family_a1", "Ngomong babagan kulawarga", "Nuduhake kepemilikan"),
        u("A1", 4, "Omah", ["location", "possessive"], "home_a1", "Nerangake omah", "Nerangake lokasi barang"),
        u("A1", 5, "Urip saben dina", ["present", "negation"], "daily_a1", "Nerangake rutinitas", "Nggawe ukara negatif"),
        u("A1", 6, "Panganan lan blanja", ["questions", "plural_quantity"], "food_a1", "Tuku panganan", "Takokake rega lan jumlah"),
        u("A1", 7, "Panggonan lan arah", ["location", "questions"], "places_a1", "Takokake lokasi", "Menehi arah sederhana"),
        u("A1", 8, "Komunikasi", ["negation", "questions"], "communication_a1", "Nyuwun pitulungan", "Njaluk klarifikasi"),
    ],
    "A2": [
        u("A2", 1, "Wong lan sesambungan", ["plural_quantity", "present"], "people_a2", "Nerangake wong lan kelompok", "Nerangake kabiasaan"),
        u("A2", 2, "Lelungan", ["past", "future_intention"], "travel_a2", "Nerangake perjalanan kepungkur", "Nggawe rencana"),
        u("A2", 3, "Kesehatan", ["progressive", "imperative"], "health_a2", "Nerangake gejala", "Nggawe panyuwunan sopan"),
        u("A2", 4, "Wektu lan jadwal", ["time", "future_intention"], "daily_a1", "Nerangake jadwal", "Ngomong babagan rencana"),
        u("A2", 5, "Perbandingan", ["comparison", "plural_quantity"], "home_a1", "Mbandhingake barang", "Nerangake ukuran lan kualitas"),
        u("A2", 6, "Unggah-ungguh basa", ["speech_levels", "imperative"], "communication_a1", "Milih tingkat tutur", "Nggawe panyuwunan miturut konteks"),
        u("A2", 7, "Layanan lan kutha", ["location", "questions"], "places_a1", "Takokake layanan", "Nerangake rute"),
        u("A2", 8, "Tinjauan A2", ["past", "future_intention"], "travel_a2", "Mbedakake kepungkur lan mbesuk", "Komunikasi nalika lelungan"),
    ],
    "B1": [
        u("B1", 1, "Sinau lan riset", ["affix_ngoko", "modality"], "study_b1", "Nerangake proses sinau", "Menehi saran"),
        u("B1", 2, "Pakaryan", ["affix_formal", "conditional"], "work_b1", "Nerangake tanggung jawab", "Nggawe usulan bersyarat"),
        u("B1", 3, "Sebab lan tujuan", ["cause_purpose", "serial_verbs"], "society_b2", "Nerangake sebab", "Nerangake tujuan"),
        u("B1", 4, "Kahanan lan rencana", ["conditional", "future_intention"], "travel_a2", "Nggawe rencana bersyarat", "Nerangake akibat sing bisa kedadeyan"),
        u("B1", 5, "Ukara relatif", ["relative", "affix_ngoko"], "study_b1", "Nerangake wong lan barang kanthi rinci", "Nggandhengake informasi"),
        u("B1", 6, "Urutan tumindak", ["serial_verbs", "past"], "daily_a1", "Nyritakake tumindak runtut", "Nerangake proses"),
        u("B1", 7, "Ngatasi masalah", ["cause_purpose", "modality"], "work_b1", "Nerangake sebab lan solusi", "Ngandharake kabutuhan"),
        u("B1", 8, "Tinjauan B1", ["relative", "conditional"], "study_b1", "Nggunakake ukara majemuk", "Ngrembug sinau lan kerja"),
    ],
    "B2": [
        u("B2", 1, "Warta lan ujaran ora langsung", ["reported", "subordination"], "media_c1", "Nglaporake ujaran wong liya", "Mbedakake sumber"),
        u("B2", 2, "Pasif lan sudut pandang", ["passive", "aspect"], "institutional_c1", "Ngganti fokus tumindak", "Mbedakake tumindak rampung lan proses"),
        u("B2", 3, "Bukti lan kemungkinan", ["aspect", "modality"], "academic_c1", "Nerangake tingkat kepastian", "Mbedakake bukti lan dugaan"),
        u("B2", 4, "Kontras lan konsesi", ["concession", "discourse"], "society_b2", "Nggandhengake gagasan sing bertentangan", "Ngakoni sudut pandang liyane"),
        u("B2", 5, "Ekonomi", ["reported", "cause_purpose"], "economy_b2", "Nerangake informasi ekonomi", "Nggandhengake sebab lan akibat"),
        u("B2", 6, "Masalah masyarakat", ["discourse", "concession"], "society_b2", "Ngrembug masalah saka pirang-pirang sisi", "Nerangake posisi sing beda"),
        u("B2", 7, "Media", ["reported", "aspect"], "media_c1", "Mbandhingake informasi", "Nerangake proses publikasi"),
        u("B2", 8, "Tinjauan B2", ["passive", "discourse"], "media_c1", "Ngringkes teks dawa", "Nyusun panjelasan runtut"),
    ],
    "C1": [
        u("C1", 1, "Basa resmi", ["nominalization", "formal_register"], "institutional_c1", "Nulis kanthi ragam resmi", "Nggunakake nominalisasi"),
        u("C1", 2, "Basa akademik", ["hedging", "aspect"], "academic_c1", "Mbedakake bukti lan interpretasi", "Nggawe kesimpulan sing ati-ati"),
        u("C1", 3, "Ukara majemuk", ["subordination", "embedded_questions"], "academic_c1", "Nggawe gagasan kompleks", "Nggunakake pitakon tersisip"),
        u("C1", 4, "Topik lan fokus", ["information_structure", "discourse"], "discourse_c2", "Ngatur informasi utama", "Milih struktur miturut konteks"),
        u("C1", 5, "Komunikasi institusi", ["formal_register", "nominalization"], "institutional_c1", "Nulis dokumen resmi", "Nerangake prosedur"),
        u("C1", 6, "Argumentasi akademik", ["argumentation", "hedging"], "academic_c1", "Nggawe argumen adhedhasar bukti", "Nanggepi argumen alternatif"),
        u("C1", 7, "Media lan wacana publik", ["information_structure", "formal_register"], "media_c1", "Nganalisis informasi publik", "Nyetel ragam basa"),
        u("C1", 8, "Tinjauan C1", ["subordination", "argumentation"], "academic_c1", "Nulis analisis dawa", "Nggandhengake gagasan kompleks"),
    ],
    "C2": [
        u("C2", 1, "Pragmatik lan makna tersirat", ["pragmatics", "information_structure"], "discourse_c2", "Mbedakake makna langsung lan tersirat", "Ngatur jarak sosial"),
        u("C2", 2, "Retorika lan sastra", ["rhetoric", "discourse_analysis"], "culture_c2", "Nggunakake teknik retorika", "Nganalisis gaya sastra"),
        u("C2", 3, "Terjemahan lan presisi", ["translation", "pragmatics"], "discourse_c2", "Njaga makna lan unggah-ungguh", "Milih istilah miturut konteks"),
        u("C2", 4, "Analisis wacana", ["discourse_analysis", "information_structure"], "discourse_c2", "Nganalisis genre lan register", "Nerangake kohesi wacana"),
        u("C2", 5, "Ragam sastra", ["rhetoric", "translation"], "culture_c2", "Ngenali basa sastra", "Nerangake pilihan stilistika"),
        u("C2", 6, "Basa profesional tingkat lanjut", ["formal_register", "pragmatics"], "institutional_c1", "Ngandharake gagasan profesional kanthi rinci", "Nyetel tingkat tutur"),
        u("C2", 7, "Sintesis sumber", ["argumentation", "discourse_analysis"], "media_c1", "Nggabungake pirang-pirang sumber", "Mbandhingake bukti sing beda"),
        u("C2", 8, "Evaluasi C2", ["translation", "rhetoric"], "academic_c1", "Nulis esai akademik sing rinci", "Nyetel gaya miturut tujuan"),
    ],
}


ASSESSMENT_BANK = [
    AssessmentQuestion(id=f"jv-{i:03}", skill=skill, difficulty=level, question=q, options=opts, correct=correct)
    for i, (level, skill, q, opts, correct) in enumerate([
        ("A1", "vocabulary", "What does matur nuwun mean?", ["thank you", "goodbye", "water", "school"], "thank you"),
        ("A1", "grammar", "Which phrase asks someone's name?", ["Jenengmu sapa?", "Aku ora ngerti.", "Matur nuwun.", "Iki omahku."], "Jenengmu sapa?"),
        ("A1", "vocabulary", "What does ibu mean?", ["mother", "father", "teacher", "friend"], "mother"),
        ("A2", "grammar", "Which sentence describes an ongoing action?", ["Aku lagi maca.", "Aku wis maca.", "Aku ora ngerti.", "Iki omahku."], "Aku lagi maca."),
        ("A2", "vocabulary", "What does tiket mean?", ["ticket", "medicine", "meeting", "source"], "ticket"),
        ("A2", "grammar", "Which expression is respectful krama?", ["Panjenengan sampun dhahar.", "Aku wis mangan.", "Aku ora ngerti.", "Iki bukuku."], "Panjenengan sampun dhahar."),
        ("B1", "grammar", "Which connector introduces a condition?", ["Yen...", "Amarga...", "Nanging...", "Banjur..."], "Yen..."),
        ("B1", "grammar", "Which expression introduces purpose?", ["supaya...", "nanging...", "wingi...", "ing endi..."], "supaya..."),
        ("B2", "grammar", "Which structure introduces reported speech?", ["Dheweke kandha yen...", "Iki pira?", "Halo!", "Ana ing endi?"], "Dheweke kandha yen..."),
        ("C1", "academic", "Which phrase is a hedge?", ["bisa uga...", "Halo!", "Iki pira?", "Sugeng enjing."], "bisa uga..."),
        ("C1", "formal", "Which phrase is formal institutional language?", ["Miturut aturan, perkara iki bakal diproses.", "Halo!", "Aku pengin iki.", "Kepiye kabarmu?"], "Miturut aturan, perkara iki bakal diproses."),
        ("C2", "discourse", "What should a Javanese translator preserve?", ["meaning, speech level and discourse function", "word count only", "literal word order only", "punctuation only"], "meaning, speech level and discourse function"),
    ], 1)
]
