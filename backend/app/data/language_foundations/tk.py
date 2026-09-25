"""Turkmen A1-C2 foundation data for JUBA LISAN."""
from app.data._types import (
    AssessmentQuestion, CurriculumUnit, GrammarExample, GrammarTopic,
    PhrasebookCategory, PhrasebookEntry, VocabularyEntry, VocabularySet,
)

LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"]


def g(slug, title, level, summary, examples, category="grammar"):
    return GrammarTopic(
        slug=slug, title=title, level=level, category=category,
        summary=summary, explanation=summary,
        examples=[GrammarExample(text=x) for x in examples],
    )


GRAMMAR_TOPICS = [
    g("pronouns", "Personal pronouns", "A1", "Use personal pronouns in basic exchanges.", ["Men talyp.", "Siz mugallym." ]),
    g("nominal", "Nominal predicates", "A1", "Identify people and things with nominal sentences.", ["Bu kitap.", "Ol lukman." ]),
    g("possessive", "Possessive suffixes", "A1", "Express possession with possessive forms and genitive phrases.", ["Bu meniň kitabym.", "Onuň öýi uly." ]),
    g("present", "Present tense", "A1", "Describe current and habitual actions.", ["Men türkmençe öwrenýärin.", "Ol her gün işleýär." ]),
    g("questions", "Questions and interrogatives", "A1", "Ask yes-no and information questions.", ["Sen nirede ýaşaýarsyň?", "Bu näme?" ]),
    g("negation", "Negation", "A1", "Negate nominal and verbal statements.", ["Men mugallym däl.", "Men bilemok." ]),
    g("demonstratives", "Demonstratives and deixis", "A1", "Use bu, şol and related forms to identify things.", ["Bu meniň öýüm.", "Şol kitap gyzykly." ]),
    g("location", "Location and postpositions", "A1", "Describe location and simple spatial relations.", ["Kitap stoluň üstünde.", "Ol mekdepde." ]),
    g("plural", "Plural formation", "A2", "Form common plural nouns with Turkmen plural suffixes.", ["Okuwçylar geldiler.", "Kitaplar stoluň üstünde." ]),
    g("cases", "Core case system", "A2", "Use accusative, genitive, dative, locative and ablative cases.", ["Men kitaby okaýaryn.", "Men Aşgabatdan geldim." ]),
    g("past", "Past tense", "A2", "Describe completed past events.", ["Düýn işe bardym.", "Biz filmi gördük." ]),
    g("future", "Future and intention", "A2", "Express plans, predictions and intentions.", ["Ertir bararyn.", "Men täze kitap alaryn." ]),
    g("progressive", "Progressive aspect", "A2", "Describe actions currently in progress.", ["Men kitap okaýaryn.", "Olar gürrüň edýärler." ]),
    g("comparatives", "Comparison", "A2", "Compare people and things.", ["Bu kitap beýlekiden gyzykly.", "Ol iň beýik bina." ]),
    g("imperative", "Imperatives and politeness", "A2", "Give instructions and make polite requests.", ["Oturmagyňyzy haýyş edýärin.", "Gaýtadan aýdyň." ]),
    g("modality", "Ability, necessity and obligation", "B1", "Express ability, necessity, permission and intention.", ["Men muny edip bilýärin.", "Bu işi tamamlamaly." ]),
    g("conditional", "Conditional -sa/-se", "B1", "Express real and hypothetical conditions.", ["Wagtym bolsa, bararyn.", "Ýagyş ýagsa, öýde galarys." ]),
    g("relative", "Participial relative clauses", "B1", "Modify nouns with participial constructions.", ["Düýn gelen adam meniň dostum.", "Okaýan kitabym gyzykly." ]),
    g("converbs", "Converbs and sequencing", "B1", "Link events by showing sequence and manner.", ["Işimi gutaryp, öýe gaýtdym.", "Gülüp gürrüň etdi." ]),
    g("causal", "Cause, purpose and result", "B1", "Express reasons, purposes and consequences.", ["Howa sowuk bolany üçin, öýde galdyk.", "Öwrenmek üçin kitaphana bardym." ]),
    g("reflexive", "Reflexive and reciprocal meaning", "B1", "Express self-directed and reciprocal actions.", ["Ol özüni tanatdy.", "Olar biri-birine kömek etdiler." ]),
    g("reported", "Reported speech", "B2", "Report statements, questions and requests.", ["Ol ertir geljekdigini aýtdy.", "Mugallym synag boljakdygyny aýtdy." ]),
    g("passive", "Passive voice", "B2", "Shift focus to the affected participant.", ["Kitap neşir edildi.", "Karar kabul edildi." ]),
    g("causative", "Causative constructions", "B2", "Express causing or arranging an action.", ["Mugallym okuwçylara maşk etdirdi.", "Ol çagasyna kitap okatdy." ]),
    g("aspect", "Aspect and event viewpoint", "B2", "Distinguish ongoing, habitual and completed events.", ["Ol işleýärdi.", "Ol işi tamamlandy." ]),
    g("concession", "Contrast and concession", "B2", "Connect opposing ideas and concessions.", ["Ýadaw bolsak-da, işi dowam etdik.", "Ýönekeý bolsa-da, möhüm mesele." ]),
    g("discourse", "Discourse connectors", "B2", "Organize explanations with sequential, causal and contrastive markers.", ["Ilki bilen meseläni kesgitleýäris. Soň çözgüt gözleýäris." ]),
    g("nominalization", "Nominalization", "C1", "Turn actions and clauses into abstract nouns for formal discourse.", ["Taslamanyň durmuşa geçirilmegi möhümdir.", "Karar kabul etmek prosesi uzaga çekdi." ]),
    g("hedging", "Academic hedging and stance", "C1", "Qualify claims and indicate evidence or uncertainty.", ["Bu netije goşmaça barlagy talap edip biler.", "Maglumatlara görä, bu çemeleşme täsirli bolup görünýär." ]),
    g("subordination", "Complex subordination", "C1", "Build multi-clause sentences with logical relations.", ["Maglumat tassyklansa, taslama indiki tapgyra geçiriler." ]),
    g("embedded_questions", "Embedded questions", "C1", "Embed questions in reports and formal explanations.", ["Onuň haçan geljekdigini bilemok." ]),
    g("information_structure", "Topic and focus", "C1", "Manage emphasis and contrast through discourse structure.", ["Bu meseläni biz şu gün ara alyp maslahatlaşarys." ]),
    g("formal_register", "Formal and institutional Turkmen", "C1", "Adapt language to administrative and professional contexts.", ["Arza degişli tertibe laýyklykda serediler." ]),
    g("argumentation", "Academic argumentation", "C1", "Present claims, evidence, counterarguments and conclusions.", ["Şu maglumatlara esaslanyp, aşakdaky netijä gelmek bolýar." ]),
    g("pragmatics", "Pragmatics and politeness", "C2", "Manage indirectness, respect, stance and social meaning.", ["Mümkin bolsa, bu meselä täzeden seredip bilersiňizmi?" ]),
    g("rhetoric", "Rhetorical and literary style", "C2", "Use and interpret metaphor, emphasis and stylistic variation.", ["Bu pikir jemgyýetçilik ösüşiniň giň çägine degişlidir." ]),
    g("translation", "Translation precision", "C2", "Preserve meaning, register and discourse function in translation.", ["Terminleri degişli pudagyň ulanylyşyna laýyk terjime etmeli."]),
    g("discourse_analysis", "Discourse analysis and register shifting", "C2", "Analyze genre, cohesion, stance and register shifts.", ["Resmi ýazuw dili gündelik gepleşik dilinden tapawutlanýar."]),
]


def v(i, level, topic, words):
    return VocabularySet(
        id=i, level=level, topic=topic, unit_ref=i,
        words=[VocabularyEntry(word=w, pos=p, definition=d, example=e) for w, p, d, e in words],
    )


VOCABULARY_SETS = [
    v("greetings_a1", "A1", "Salamlaşmak", [("Salam", "phrase", "hello", "Salam!"), ("Sag bol", "phrase", "thanks/goodbye", "Sag bol!"), ("ady", "noun", "name", "Meniň adym Kerim."), ("dost", "noun", "friend", "Ol meniň dostum.")]),
    v("identity_a1", "A1", "Şahsyýet", [("talyp", "noun", "student", "Men talyp."), ("mugallym", "noun", "teacher", "Ol mugallym."), ("lukman", "noun", "doctor", "Ol lukman."), ("işçi", "noun", "worker", "Ol işçi.")]),
    v("family_a1", "A1", "Maşgala", [("eje", "noun", "mother", "Meniň ejem öýde."), ("kaka", "noun", "father", "Kakam işleýär."), ("aga", "noun", "older brother", "Agam geldi."), ("uýa", "noun", "sister", "Uýam mekdepde.")]),
    v("home_a1", "A1", "Öý", [("öý", "noun", "home", "Meniň öýüm uly."), ("otag", "noun", "room", "Otaga giriň."), ("gapy", "noun", "door", "Gapy açyk."), ("stol", "noun", "table", "Kitap stoluň üstünde.")]),
    v("daily_a1", "A1", "Gündelik durmuş", [("ertir", "noun", "tomorrow", "Ertir işe bararyn."), ("gün", "noun", "day", "Bu gün dynç güni."), ("işlemek", "verb", "to work", "Men her gün işleýärin."), ("gitmek", "verb", "to go", "Men mekdebe gidýärin.")]),
    v("food_a1", "A1", "Iýmit", [("çörek", "noun", "bread", "Çörek alyň."), ("çaý", "noun", "tea", "Men çaý içýärin."), ("tüwi", "noun", "rice", "Tüwi taýýar."), ("alma", "noun", "apple", "Bir alma isleýärin.")]),
    v("places_a1", "A1", "Ýerler", [("bazar", "noun", "market", "Bazar nirede?"), ("mekdep", "noun", "school", "Mekdep ýakyn."), ("hassahana", "noun", "hospital", "Hassahana bu ýerde."), ("ýol", "noun", "road", "Bu ýol şähere gidýär.")]),
    v("communication_a1", "A1", "Aragatnaşyk", [("sorag", "noun", "question", "Mende bir sorag bar."), ("kömek", "noun", "help", "Maňa kömek gerek."), ("dil", "noun", "language", "Türkmen dili gyzykly."), ("söhbet", "noun", "conversation", "Söhbet edýäris.")]),
    v("travel_a2", "A2", "Syýahat", [("uçara", "noun", "airplane", "Uçara sagat dokuzda gidýär."), ("otly", "noun", "train", "Otly geldi."), ("myhmanhana", "noun", "hotel", "Myhmanhanada otag bar."), ("bilet", "noun", "ticket", "Bilet nireden alynýar?")]),
    v("health_a2", "A2", "Saglyk", [("lukman", "noun", "doctor", "Lukmana bardym."), ("agyry", "noun", "pain", "Kellämiň agyrysy bar."), ("derman", "noun", "medicine", "Dermany wagtynda içiň."), ("keselhana", "noun", "hospital", "Keselhana şäherde ýerleşýär.")]),
    v("study_b1", "B1", "Bilim", [("öwrenmek", "verb", "learn", "Men dil öwrenýärin."), ("barlag", "noun", "research", "Barlag dowam edýär."), ("tabşyrma", "noun", "assignment", "Tabşyrmany tamamladym."), ("synag", "noun", "exam", "Synag ertir bolar.")]),
    v("work_b1", "B1", "Iş we kär", [("işgär", "noun", "employee", "Işgär hasabat taýýarlady."), ("ýygnak", "noun", "meeting", "Ýygnak üçde başlanýar."), ("tejribe", "noun", "experience", "Onuň köp tejribesi bar."), ("borç", "noun", "responsibility", "Bu meniň borjum.")]),
    v("society_b2", "B2", "Jemgyýet", [("jemgyýet", "noun", "society", "Jemgyýet çalt üýtgeýär."), ("ösüş", "noun", "development", "Durnukly ösüş möhümdir."), ("syýasat", "noun", "policy/politics", "Täze syýasat ara alnyp maslahatlaşyldy."), ("raýat", "noun", "citizen", "Raýat öz hukuklaryny bilmeli.")]),
    v("economy_b2", "B2", "Ykdysadyýet", [("ykdysadyýet", "noun", "economy", "Ykdysadyýet ösýär."), ("bazar", "noun", "market", "Bazar islegi artdy."), ("maýa goýum", "noun", "investment", "Maýa goýum köpeldi."), ("girdeji", "noun", "income", "Öý hojalygynyň girdejisi artdy.")]),
    v("media_c1", "C1", "Habar serişdeleri", [("habar", "noun", "news", "Habar barlanylmaly."), ("makala", "noun", "article", "Makalada täze maglumat bar."), ("çeşme", "noun", "source", "Çeşme görkezildi."), ("söhbetdeşlik", "noun", "interview", "Ol söhbetdeşlik berdi.")]),
    v("academic_c1", "C1", "Akademiki dil", [("barlag", "noun", "research", "Barlagyň netijesi möhümdir."), ("subutnama", "noun", "evidence", "Subutnama ýeterlikdir."), ("çaklama", "noun", "hypothesis", "Çaklama barlandy."), ("netije", "noun", "conclusion/result", "Netije aýdyň görkezildi.")]),
    v("institutional_c1", "C1", "Resmi dil", [("tertip", "noun", "regulation/procedure", "Tertibe laýyklykda hereket ediler."), ("arza", "noun", "application", "Arza kabul edildi."), ("karar", "noun", "decision", "Karar resmi taýdan çykaryldy."), ("ýerine ýetiriş", "noun", "implementation", "Ýerine ýetiriş gözegçilikde saklanýar.")]),
    v("culture_c2", "C2", "Medeniýet we edebiýat", [("miras", "noun", "heritage", "Medeni miras goralar."), ("edebiýat", "noun", "literature", "Türkmen edebiýaty baý."), ("şekillendiriş", "noun", "imagery", "Awtor güýçli şekillendiriş ulanýar."), ("simwol", "noun", "symbol", "Simwolyň manysy düşündirildi.")]),
]


def p(i, level, situation, items, register="neutral"):
    return PhrasebookCategory(
        id=i, level=level, situation=situation, icon="💬",
        phrases=[PhrasebookEntry(text=t, context=c, register=register) for t, c in items],
    )


PHRASEBOOK_CATEGORIES = [
    p("greetings_a1", "A1", "Salamlaşmak", [("Salam!", "greeting"), ("Adyň näme?", "asking a name"), ("Tanyşanyma şat.", "meeting someone")]),
    p("thanks_a1", "A1", "Minnetdarlyk we ötünç", [("Sag boluň.", "thanks"), ("Bagyşlaň.", "apology"), ("Hiç zat däl.", "polite response")]),
    p("shopping_a1", "A1", "Söwda", [("Bu näçe?", "asking price"), ("Muny isleýärin.", "requesting an item"), ("Başga reňkiňiz barmy?", "asking for an alternative")]),
    p("directions_a1", "A1", "Ýol soramak", [("Bazar nirede?", "asking location"), ("Mekdebe nädip barmaly?", "asking a route"), ("Şu tarapa gidiň.", "giving directions")]),
    p("help_a1", "A1", "Kömek we düşündiriş", [("Maňa kömek ediň.", "asking for help"), ("Men düşünmedim.", "clarification"), ("Gaýtadan aýdyň.", "asking for repetition")]),
    p("travel_a2", "A2", "Syýahat", [("Bilet nireden alynýar?", "buying a ticket"), ("Haçan gidýäris?", "asking departure time"), ("Sargydymy tassyklajak.", "confirming a booking")]),
    p("health_a2", "A2", "Saglyk", [("Başym agyrýar.", "describing a symptom"), ("Lukman bilen görüşmek isleýärin.", "requesting care"), ("Bu dermany nädip ulanmaly?", "asking about medicine")]),
    p("study_b1", "B1", "Bilim", [("Bu pikiri düşündirip bilersiňizmi?", "asking for explanation"), ("Tabşyrmany wagtynda bererin.", "assignment"), ("Bu çeşmä salgylanyldym.", "citing a source")]),
    p("work_b1", "B1", "Iş", [("Ýygnagy başlalyň.", "starting a meeting"), ("Bu meseläni ara alyp maslahatlaşalyň.", "opening discussion"), ("Hasabaty ertir ibererin.", "work commitment")]),
    p("public_b2", "B2", "Jemgyýetçilik pikir alyşmasy", [("Bu meselä birnäçe faktor täsir edýär.", "explaining causes"), ("Başga tarapdan seredeniňde...", "contrast"), ("Subutnamalara esaslanyp...", "introducing evidence")], "formal"),
    p("academic_c1", "C1", "Akademiki aragatnaşyk", [("Bu barlag ... görkezýär.", "stating a finding"), ("Bu netijäni seresaply düşündirmek gerek.", "hedging"), ("Muny geljekde goşmaça öwrenmek zerurdyr.", "further research")], "academic"),
    p("institutional_c1", "C1", "Resmi aragatnaşyk", [("Arzaňyz kabul edildi.", "acknowledgement"), ("Tertibe laýyklykda serediler.", "formal procedure"), ("Degişli maglumatlary ibermegiňizi haýyş edýäris.", "formal request")], "formal"),
]


def u(level, number, title, grammar, vocab, a, b):
    return CurriculumUnit(
        id=f"tk-{level.lower()}-{number:02}",
        level=level, unit_number=number, title=title,
        grammar_points=grammar, vocabulary_set_ids=[vocab],
        lesson_types=["grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review"],
        competency_checklist=[a, b], default_weeks=2,
    )


CURRICULUM = {
    "A1": [
        u("A1", 1, "Salamlaşmak we tanyşmak", ["pronouns", "nominal"], "greetings_a1", "Özüňi tanyşdyrmak", "Salamlaşmak"),
        u("A1", 2, "Şahsyýet we maşgala", ["possessive", "demonstratives"], "identity_a1", "Özüň barada maglumat bermek", "Ýakyn adamlary tanatmak"),
        u("A1", 3, "Maşgala", ["possessive", "plural"], "family_a1", "Maşgalany suratlandyrmak", "Eýeçiligi görkezmek"),
        u("A1", 4, "Öý we zatlar", ["location", "demonstratives"], "home_a1", "Öýi suratlandyrmak", "Zatlaryň ýerleşýän ýerini aýtmak"),
        u("A1", 5, "Gündelik durmuş", ["present", "negation"], "daily_a1", "Gündelik işleri gürrüň bermek", "Ýokluk bildirmek"),
        u("A1", 6, "Iýmit we söwda", ["questions", "negation"], "food_a1", "Haryt soramak", "Islegi bildirmek"),
        u("A1", 7, "Ýerler we ugurlar", ["location", "questions"], "places_a1", "Ýer soramak", "Ýol görkezmek"),
        u("A1", 8, "Aragatnaşyk", ["questions", "pronouns"], "communication_a1", "Düşünmedik zadyňy soramak", "Kömek soramak"),
    ],
    "A2": [
        u("A2", 1, "Syýahat", ["cases", "past"], "travel_a2", "Geçen syýahaty gürrüň bermek", "Ýol bilen baglanyşykly sorag bermek"),
        u("A2", 2, "Saglyk", ["progressive", "imperative"], "health_a2", "Alamatlary düşündirmek", "Politeli haýyş etmek"),
        u("A2", 3, "Geçmiş wakalar", ["past", "progressive"], "daily_a1", "Geçmiş wakany beýan etmek", "Dowam edýän işi aýtmak"),
        u("A2", 4, "Geljek meýilnamalar", ["future", "questions"], "travel_a2", "Meýilnama düzmek", "Wagt barada soramak"),
        u("A2", 5, "Deňeşdirmek", ["comparatives", "plural"], "home_a1", "Zatlary deňeşdirmek", "Hil we ölçeg barada aýtmak"),
        u("A2", 6, "Söwda we hyzmatlar", ["cases", "imperative"], "food_a1", "Hyzmat soramak", "Sargyt bermek"),
        u("A2", 7, "Şäherde", ["cases", "location"], "places_a1", "Ýol görkezmek", "Ýerleşişi düşündirmek"),
        u("A2", 8, "A2 gaýtalama", ["past", "future"], "daily_a1", "Geçmiş we geljegi tapawutlandyrmak", "Gündelik ýagdaýlarda aragatnaşyk"),
    ],
    "B1": [
        u("B1", 1, "Bilim we öwrenmek", ["modality", "cases"], "study_b1", "Öwreniş usulyny düşündirmek", "Maslahat bermek"),
        u("B1", 2, "Iş we kär", ["modality", "conditional"], "work_b1", "Iş borçlaryny beýan etmek", "Şertli teklip bermek"),
        u("B1", 3, "Sebäp we maksat", ["causal", "converbs"], "society_b2", "Sebäp düşündirmek", "Maksat bildirmek"),
        u("B1", 4, "Şert we netijeler", ["conditional", "future"], "work_b1", "Şertli meýilnama düzmek", "Netijäni çaklamak"),
        u("B1", 5, "Habar beriji gurluşlar", ["relative", "cases"], "study_b1", "Atlary giňişleýin düşündirmek", "Goşmaça maglumat bermek"),
        u("B1", 6, "Wakalaryň yzygiderliligi", ["converbs", "aspect"], "daily_a1", "Wakalary yzygiderli beýan etmek", "Hereketiň görnüşini görkezmek"),
        u("B1", 7, "Mesele çözmek", ["causal", "modality"], "work_b1", "Sebäp we çözgüt hödürlemek", "Gerekçiligi bildirmek"),
        u("B1", 8, "B1 gaýtalama", ["relative", "conditional"], "study_b1", "Çylşyrymly sözlemler ulanmak", "Bilim we iş barada pikir alyşmak"),
    ],
    "B2": [
        u("B2", 1, "Başga biriniň sözleri", ["reported", "subordination"], "media_c1", "Başga biriniň pikirini geçirmek", "Çeşmäni görkezmek"),
        u("B2", 2, "Işjeňlik we passiw", ["passive", "causative"], "institutional_c1", "Wakanyň merkezini üýtgetmek", "Hereketiň sebäbini düşündirmek"),
        u("B2", 3, "Subutnama we çaklama", ["aspect", "hedging"], "academic_c1", "Subutnamanyň derejesini görkezmek", "Çaklamany seresaply aýtmak"),
        u("B2", 4, "Garşylyk we boýun alma", ["concession", "discourse"], "society_b2", "Garşy pikirleri baglamak", "Boýun alma bilen düşündirmek"),
        u("B2", 5, "Ykdysadyýet", ["reported", "causal"], "economy_b2", "Ykdysady maglumatlary düşündirmek", "Sebäp-netijäni baglamak"),
        u("B2", 6, "Jemgyýetçilik meseleleri", ["discourse", "concession"], "society_b2", "Köp taraply meseläni ara alyp maslahatlaşmak", "Garşy pozisiýany beýan etmek"),
        u("B2", 7, "Habar serişdeleri", ["reported", "aspect"], "media_c1", "Habar çeşmesini seljermek", "Fakty we çaklamany tapawutlandyrmak"),
        u("B2", 8, "B2 gaýtalama", ["passive", "discourse"], "media_c1", "Çylşyrymly maglumatlary jemlemek", "Uzak düşündiriş ýazmak"),
    ],
    "C1": [
        u("C1", 1, "Resmi atlandyrma", ["nominalization", "formal_register"], "institutional_c1", "Resmi dilde ýazmak", "Hereketi abstrakt at bilen beýan etmek"),
        u("C1", 2, "Akademiki seresaplylyk", ["hedging", "aspect"], "academic_c1", "Ynam derejesini görkezmek", "Seresaply netije çykarmak"),
        u("C1", 3, "Çylşyrymly tabyn sözlemler", ["subordination", "embedded_questions"], "academic_c1", "Köp bölekli pikiri gurmak", "Gizlin soraglary ulanmak"),
        u("C1", 4, "Tema we ünsi jemlemek", ["information_structure", "discourse"], "media_c1", "Möhüm maglumaty öňe çykarmak", "Kontekste görä söz tertibini saýlamak"),
        u("C1", 5, "Edara aragatnaşygy", ["formal_register", "nominalization"], "institutional_c1", "Resmi hat ýazmak", "Amaly prosedurany düşündirmek"),
        u("C1", 6, "Akademiki argument", ["argumentation", "hedging"], "academic_c1", "Subutnama esasly argument ýazmak", "Garşy pikiri göz öňünde tutmak"),
        u("C1", 7, "Habar we syýasat dili", ["information_structure", "formal_register"], "media_c1", "Jemgyýetçilik tekstini seljermek", "Resmi äheňi sazlamak"),
        u("C1", 8, "C1 gaýtalama", ["subordination", "argumentation"], "academic_c1", "Uzyn akademiki düşündiriş ýazmak", "Çylşyrymly pikirleri baglamak"),
    ],
    "C2": [
        u("C2", 1, "Pragmatiki many", ["pragmatics", "information_structure"], "institutional_c1", "Göni we gizlin manyny tapawutlandyrmak", "Politeli däl äheňi azaltmak"),
        u("C2", 2, "Ritoriki dil", ["rhetoric", "discourse_analysis"], "culture_c2", "Ritoriki serişdeleri ulanmak", "Çeper şekillendirişi düşündirmek"),
        u("C2", 3, "Terjime takyklygy", ["translation", "pragmatics"], "media_c1", "Many we äheňi saklamak", "Terminleri kontekste görä saýlamak"),
        u("C2", 4, "Diskurs seljermesi", ["discourse_analysis", "information_structure"], "media_c1", "Žanr we registri seljermek", "Diskursyň sazlaşygyny düşündirmek"),
        u("C2", 5, "Edebi registr", ["rhetoric", "translation"], "culture_c2", "Edebi dili tanamak", "Çeper saýlawlary düşündirmek"),
        u("C2", 6, "Ýokary hünär dili", ["formal_register", "pragmatics"], "institutional_c1", "Hünär taýdan çylşyrymly pikir beýan etmek", "Sosial ýagdaýda sypaýylygy sazlamak"),
        u("C2", 7, "Birnäçe çeşmäni birleşdirmek", ["argumentation", "discourse_analysis"], "media_c1", "Birnäçe çeşmäni deňeşdirmek", "Garşy maglumatlary birleşdirmek"),
        u("C2", 8, "C2 jemleýji baha", ["translation", "rhetoric"], "academic_c1", "Çylşyrymly akademiki tekst ýazmak", "Registri maksada laýyk üýtgetmek"),
    ],
}


ASSESSMENT_BANK = [
    AssessmentQuestion(id="tk-001", skill="vocabulary", difficulty="A1", question="What does Salam mean?", options=["hello", "ticket", "school", "market"], correct="hello"),
    AssessmentQuestion(id="tk-002", skill="grammar", difficulty="A1", question="Which asks someone's name?", options=["Adyň näme?", "Bu näçe?", "Bazar nirede?", "Sag bol."], correct="Adyň näme?"),
    AssessmentQuestion(id="tk-003", skill="vocabulary", difficulty="A1", question="What does eje mean?", options=["mother", "father", "teacher", "friend"], correct="mother"),
    AssessmentQuestion(id="tk-004", skill="grammar", difficulty="A2", question="Which is a past-tense sentence?", options=["Düýn işe bardym.", "Ertir bararyn.", "Men işleýärin.", "Men bilemok."], correct="Düýn işe bardym."),
    AssessmentQuestion(id="tk-005", skill="vocabulary", difficulty="A2", question="What does bilet mean?", options=["ticket", "medicine", "meeting", "source"], correct="ticket"),
    AssessmentQuestion(id="tk-006", skill="grammar", difficulty="B1", question="Which introduces a condition?", options=["Wagtym bolsa...", "Men geldim.", "Bu kitap.", "Ol işleýär."], correct="Wagtym bolsa..."),
    AssessmentQuestion(id="tk-007", skill="grammar", difficulty="B1", question="What does -mek üçin express?", options=["purpose", "ownership", "comparison", "location"], correct="purpose"),
    AssessmentQuestion(id="tk-008", skill="grammar", difficulty="B2", question="Which reports another person's statement?", options=["geljekdigini aýtdy", "iň uly", "öýde", "Salam"], correct="geljekdigini aýtdy"),
    AssessmentQuestion(id="tk-009", skill="vocabulary", difficulty="B2", question="What does subutnama mean?", options=["evidence", "holiday", "neighbor", "ticket"], correct="evidence"),
    AssessmentQuestion(id="tk-010", skill="academic", difficulty="C1", question="Which is an academic hedge?", options=["talap edip biler", "Salam", "Sag bol.", "Şu ýerde"], correct="talap edip biler"),
    AssessmentQuestion(id="tk-011", skill="formal", difficulty="C1", question="Which is institutional language?", options=["Tertibe laýyklykda serediler.", "Salam!", "Muny isleýärin.", "Bu näçe?"], correct="Tertibe laýyklykda serediler."),
    AssessmentQuestion(id="tk-012", skill="discourse", difficulty="C2", question="What should translation preserve?", options=["meaning, register and discourse function", "word count only", "literal order only", "punctuation only"], correct="meaning, register and discourse function"),
]
