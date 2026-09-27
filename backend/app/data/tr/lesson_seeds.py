"""Curated Turkish lesson seeds for deterministic, language-specific lesson generation.

These seeds are intentionally compact: they ground generated lessons in natural
Turkish examples and communicative goals while leaving exercise variation to
the lesson generator.
"""

LESSON_SEEDS = {
    ("A2", "a2-unit-1", "grammar"): {
        "title": "Geçmişten bugüne günlük hayat",
        "objective": "Geçmişte yaşanan olayları ve bugünkü durumları basitçe karşılaştırmak.",
        "grammar": ["past-tense", "locative", "comparatives"],
        "phrases": ["Dün evdeydim.", "Geçen hafta Ankara'ya gittim.", "Bugün daha iyiyim."],
        "examples": ["Dün çalıştım.", "Geçen yıl İstanbul'da yaşadım.", "Bu ev eskisinden daha büyük."],
    },
    ("A2", "a2-unit-1", "vocabulary"): {
        "title": "Ev ve şehir hayatı",
        "objective": "Ev, mahalle ve şehir hakkında günlük konuşmalar yapabilmek.",
        "words": [
            ("mahalle", "neighborhood", "Mahallemiz çok sakin."),
            ("apartman", "apartment building", "Apartmanımız merkezde."),
            ("taşınmak", "to move house", "Gelecek ay taşınıyoruz."),
            ("yakın", "near", "Market eve çok yakın."),
            ("uzak", "far", "İstasyon buradan uzak."),
            ("merkez", "city centre", "Şehir merkezi kalabalık."),
        ],
    },
    ("A2", "a2-unit-1", "reading"): {
        "title": "Yeni bir mahalle",
        "objective": "Kısa bir metinden ev, konum ve günlük hayat bilgilerini çıkarmak.",
        "text": "Elif yeni bir apartmana taşındı. Evi küçük ama aydınlık. Market ve otobüs durağı evine çok yakın. Hafta sonları parka gidiyor.",
        "questions": [
            ("Elif nereye taşındı?", ["Yeni bir apartmana", "Bir otele", "Bir okula"], "Yeni bir apartmana"),
            ("Market eve nasıl?", ["Çok yakın", "Çok uzak", "Kapalı"], "Çok yakın"),
        ],
    },
    ("A2", "a2-unit-1", "listening"): {
        "title": "Şehirde yön bulma",
        "objective": "Kısa bir günlük konuşmada yer ve mesafe bilgilerini anlamak.",
        "transcript": "Affedersiniz, istasyon nerede? Düz gidin ve ikinci sokaktan sola dönün. İstasyon bankanın yanında.",
        "questions": [
            ("İstasyona nasıl gidilir?", ["Düz gidip ikinci sokaktan sola dönerek", "Sağa dönerek", "Otobüsle"], "Düz gidip ikinci sokaktan sola dönerek"),
            ("İstasyonun yanında ne var?", ["Banka", "Market", "Okul"], "Banka"),
        ],
    },
    ("B1", "b1-unit-1", "grammar"): {
        "title": "Deneyim anlatmak",
        "objective": "Geçmiş deneyimleri nedenleri ve sonuçlarıyla anlatmak.",
        "grammar": ["past-tense", "aspect", "instrumental"],
        "phrases": ["Daha önce bu işi yaptım.", "Bu deneyim bana çok şey öğretti.", "Çünkü yeni bir şey öğrenmek istedim."],
        "examples": ["Geçen yıl bir kursa katıldım.", "Bu deneyim sayesinde daha rahat konuşuyorum.", "Arkadaşlarımla birlikte çalıştım."],
    },
    ("B1", "b1-unit-1", "vocabulary"): {
        "title": "Eğitim ve deneyim",
        "objective": "Eğitim geçmişi, beceriler ve deneyimler hakkında konuşabilmek.",
        "words": [
            ("deneyim", "experience", "Bu işte üç yıllık deneyimim var."),
            ("beceri", "skill", "İletişim becerilerimi geliştirmek istiyorum."),
            ("eğitim", "education/training", "Eğitim programı iki ay sürdü."),
            ("katılmak", "to participate/attend", "Geçen hafta seminere katıldım."),
            ("geliştirmek", "to improve", "Türkçemi geliştirmek istiyorum."),
            ("başarmak", "to succeed", "Hedefime ulaşmayı başardım."),
        ],
    },
    ("B1", "b1-unit-1", "reading"): {
        "title": "Bir öğrenme deneyimi",
        "objective": "Bir kişinin öğrenme deneyimini ve sonuçlarını özetlemek.",
        "text": "Mert geçen yıl akşamları Türkçe kursuna katıldı. Başlangıçta konuşmakta zorlandı, ancak düzenli olarak pratik yaptı. Üç ay sonra günlük konuşmaları daha rahat anlamaya başladı.",
        "questions": [
            ("Mert kursa ne zaman katıldı?", ["Geçen yıl", "Geçen ay", "İki yıl önce"], "Geçen yıl"),
            ("Üç ay sonra ne değişti?", ["Günlük konuşmaları daha rahat anlamaya başladı", "Kursu bıraktı", "Başka bir ülkeye taşındı"], "Günlük konuşmaları daha rahat anlamaya başladı"),
        ],
    },
    ("B2", "b2-unit-1", "grammar"): {
        "title": "Görüşleri gerekçelendirmek",
        "objective": "Bir görüşü koşul, neden ve karşı görüşlerle yapılandırmak.",
        "grammar": ["conditionals", "discourse-markers", "passive"],
        "phrases": ["Bence bu yaklaşım daha etkili.", "Bununla birlikte, başka bir seçenek de var.", "Eğer zamanımız varsa, yöntemi değiştirebiliriz."],
        "examples": ["Bu yöntem tercih ediliyor çünkü daha hızlı sonuç veriyor.", "Eğer kaynaklar artırılırsa, proje daha erken tamamlanabilir."],
    },
    ("B2", "b2-unit-1", "vocabulary"): {
        "title": "İş ve liderlik",
        "objective": "Profesyonel durumları, sorumlulukları ve önerileri daha kesin biçimde ifade etmek.",
        "words": [
            ("sorumluluk", "responsibility", "Bu görevin sorumluluğu bana ait."),
            ("hedef", "goal", "Ekibin temel hedefi kaliteyi artırmak."),
            ("verimlilik", "efficiency", "Yeni sistem verimliliği artırdı."),
            ("öneri", "proposal/suggestion", "Bir öneride bulunmak istiyorum."),
            ("müzakere", "negotiation", "Müzakere yarın devam edecek."),
            ("uygulanabilir", "feasible", "Bu plan kısa vadede uygulanabilir."),
        ],
    },
    ("B2", "b2-unit-1", "reading"): {
        "title": "Yeni çalışma yöntemi",
        "objective": "Profesyonel bir metindeki ana iddia, gerekçe ve sonucu ayırt etmek.",
        "text": "Şirket, çalışanların zamanını daha verimli kullanabilmesi için yeni bir çalışma yöntemi uygulamaya başladı. İlk sonuçlar olumlu olsa da bazı çalışanlar yüz yüze toplantıların azalmasının iletişimi zorlaştırdığını düşünüyor.",
        "questions": [
            ("Yeni yöntemin amacı nedir?", ["Zamanı daha verimli kullanmak", "Toplantıları artırmak", "Çalışan sayısını azaltmak"], "Zamanı daha verimli kullanmak"),
            ("Bazı çalışanların endişesi nedir?", ["İletişimin zorlaşması", "Maaşların düşmesi", "Ofisin taşınması"], "İletişimin zorlaşması"),
        ],
    },
    ("C1", "c1-unit-1", "grammar"): {
        "title": "Akademik ve resmî Türkçe",
        "objective": "Akademik bir iddiayı temkinli ve tutarlı biçimde ifade etmek.",
        "grammar": ["reported-speech", "academic-register", "nominalization"],
        "phrases": ["Araştırmanın sonuçları göstermektedir ki...", "Bu bulgu, ... ile ilişkilendirilebilir.", "Bununla birlikte, sonuçların dikkatle yorumlanması gerekir."],
        "examples": ["Araştırma, düzenli tekrarın öğrenmeyi desteklediğini göstermektedir.", "Bu sonuç farklı koşullarda yeniden değerlendirilmelidir."],
    },
    ("C1", "c1-unit-1", "vocabulary"): {
        "title": "Araştırma ve akademik iletişim",
        "objective": "Araştırma sonuçlarını ve sınırlılıklarını akademik bir dille tartışmak.",
        "words": [
            ("bulgu", "finding", "Araştırmanın temel bulgusu dikkat çekicidir."),
            ("varsayım", "assumption", "Bu varsayımın ayrıca test edilmesi gerekir."),
            ("yöntem", "method", "Kullanılan yöntem ayrıntılı olarak açıklanmıştır."),
            ("kapsam", "scope", "Çalışmanın kapsamı iki grupla sınırlıdır."),
            ("değerlendirmek", "to evaluate", "Sonuçları farklı açılardan değerlendirmek gerekir."),
            ("ilişkilendirmek", "to associate/relate", "Bu sonuç davranış değişikliğiyle ilişkilendirilebilir."),
        ],
    },
    ("C1", "c1-unit-1", "reading"): {
        "title": "Araştırma bulgularını yorumlamak",
        "objective": "Akademik bir paragrafta iddia, kanıt ve sınırlılığı ayırt etmek.",
        "text": "Çalışmanın sonuçları, düzenli kısa tekrarların uzun aralıklarla yapılan tek seferlik çalışmaya kıyasla daha kalıcı öğrenmeyle ilişkili olduğunu göstermektedir. Bununla birlikte, örneklemin sınırlı olması sonuçların tüm öğrencilere doğrudan genellenmesini güçleştirmektedir.",
        "questions": [
            ("Çalışmanın temel sonucu nedir?", ["Düzenli kısa tekrarlar daha kalıcı öğrenmeyle ilişkilidir", "Tek seferlik çalışma her zaman daha iyidir", "Öğrenciler çalışmamalıdır"], "Düzenli kısa tekrarlar daha kalıcı öğrenmeyle ilişkilidir"),
            ("Sonucun bir sınırlılığı nedir?", ["Örneklemin sınırlı olması", "Dilbilgisinin yanlış olması", "Çalışmanın çok uzun sürmesi"], "Örneklemin sınırlı olması"),
        ],
    },
    ("C2", "c2-unit-1", "grammar"): {
        "title": "Üslup ve anlam nüansı",
        "objective": "Aynı düşünceyi bağlama, vurguya ve resmiyet düzeyine göre yeniden ifade etmek.",
        "grammar": ["discourse", "style", "advanced-syntax"],
        "phrases": ["Bu ifade, bağlama bağlı olarak farklı biçimlerde yorumlanabilir.", "Daha temkinli bir ifadeyle...", "Burada asıl vurgulanması gereken nokta..."],
        "examples": ["Bu sonucun kesin olduğu söylenemez; ancak güçlü bir eğilim olduğu ileri sürülebilir.", "Asıl mesele sonucun kendisinden ziyade nasıl yorumlandığıdır."],
    },
    ("C2", "c2-unit-1", "vocabulary"): {
        "title": "İleri düzey üslup ve söylem",
        "objective": "Soyut, retorik ve eleştirel dili hassas biçimde kullanmak.",
        "words": [
            ("varsayım", "assumption", "Temel varsayım yeniden sorgulanmalıdır."),
            ("çıkarım", "inference", "Bu veriden böyle bir çıkarım yapmak mümkün değildir."),
            ("belirsizlik", "uncertainty", "Sonuçlarda belirli bir belirsizlik vardır."),
            ("nüans", "nuance", "İki ifade arasında önemli bir nüans bulunuyor."),
            ("bağlam", "context", "İfade bağlamından koparıldığında anlamı değişebilir."),
            ("yorumlamak", "to interpret", "Metni tarihsel bağlamı içinde yorumlamak gerekir."),
        ],
    },
    ("C2", "c2-unit-1", "reading"): {
        "title": "Bağlam ve yorum",
        "objective": "Yoğun bir metindeki açık iddia ile örtük anlam arasındaki farkı çözümlemek.",
        "text": "Bir ifadenin anlamı yalnızca sözcüklerin sözlük karşılıklarından oluşmaz; konuşma ortamı, muhatapların ortak bilgisi ve kullanılan üslup da anlamın oluşumuna katkıda bulunur. Bu nedenle aynı cümle, farklı bağlamlarda farklı bir pragmatik etki yaratabilir.",
        "questions": [
            ("Anlamı hangi unsurlar etkiler?", ["Bağlam, ortak bilgi ve üslup", "Yalnızca sözlük", "Yalnızca yazım"], "Bağlam, ortak bilgi ve üslup"),
            ("Aynı cümle neden farklı etki yaratabilir?", ["Bağlama göre pragmatik anlamı değişebilir", "Her zaman aynı anlamı taşır", "Çünkü kelimeler değişir"], "Bağlama göre pragmatik anlamı değişebilir"),
        ],
    },
    ("A2","a2-unit-1","speaking"): {
        "title":"Günlük hayatını anlat",
        "objective":"Günlük rutinini, yaşadığın yeri ve hafta sonu planlarını basitçe anlatmak.",
        "prompt":"Yaklaşık bir dakika konuş. Nerede yaşadığını, hafta içi neler yaptığını ve hafta sonu ne yaptığını anlat.",
        "phrases":["Genellikle ... yaparım.","Hafta sonları ... giderim.","Yaşadığım yerde ... var."],
        "examples":["Ankara'da yaşıyorum. Hafta içi çalışırım. Hafta sonları arkadaşlarımla parka giderim."]
    },
    ("A2","a2-unit-1","writing"): {
        "title":"Mahalleni tanıt",
        "objective":"Mahalle ve günlük hayat hakkında kısa, bağlantılı cümleler yazmak.",
        "prompt":"60–80 kelimeyle mahalleni tanıt. Nerede olduğunu, yakınındaki yerleri ve orada ne yaptığını yaz.",
        "guidance":["En az üç yer adı kullan.","yakın, uzak veya merkez gibi konum ifadeleri kullan.","Günlük bir etkinlik ekle."],
        "examples":["Mahallem şehir merkezine yakın. Evimizin yanında küçük bir market var. Otobüs durağı da çok yakın. Hafta sonları parka gidiyorum."]
    },
    ("A2","a2-unit-1","review"): {
        "title":"Ev ve şehir tekrarı",
        "objective":"Konum, geçmiş zaman ve günlük şehir kelimelerini tekrar etmek.",
        "questions":[
            ("Hangisi geçmişte yapılan bir işi anlatır?",["Dün çalıştım.","Yarın çalışacağım.","Şimdi çalışıyorum."],"Dün çalıştım."),
            ("“İstasyon evden uzak.” cümlesinde hangi bilgi veriliyor?",["Mesafe","Zaman","Hava durumu"],"Mesafe"),
            ("Hangisi doğru?",["Geçen hafta Ankara'ya gittim.","Geçen hafta Ankara'ya gidiyorum.","Geçen hafta Ankara'ya gideceğim."],"Geçen hafta Ankara'ya gittim.")
        ]
    },

    ("B1","b1-unit-1","listening"): {
        "title":"Bir kurs hakkında konuşma",
        "objective":"Bir konuşmada kursun zamanı, amacı ve konuşmacının motivasyonunu anlamak.",
        "transcript":"Ayşe: Yeni bir dil kursuna başladım. Dersler salı ve perşembe akşamları. Mehmet: Neden bu kursu seçtin? Ayşe: İşimde yabancı müşterilerle daha rahat konuşmak istiyorum.",
        "questions":[
            ("Dersler ne zaman?",["Salı ve perşembe akşamları","Pazartesi sabahları","Her gün"],"Salı ve perşembe akşamları"),
            ("Ayşe neden kursa başladı?",["İşinde daha rahat konuşmak için","Tatile gitmek için","Yeni bir eve taşınmak için"],"İşinde daha rahat konuşmak için"),
            ("Ayşe kiminle daha rahat konuşmak istiyor?",["Yabancı müşterilerle","Komşularıyla","Öğretmenleriyle"],"Yabancı müşterilerle")
        ]
    },
    ("B1","b1-unit-1","speaking"): {
        "title":"Bir kararını açıkla",
        "objective":"Bir kararın nedenlerini açıklamak ve farklı koşullarda ne yapacağını söylemek.",
        "prompt":"Önemli bir kararını anlat. Neden bu kararı verdiğini ve daha fazla zamanın olsaydı ne yapacağını açıkla.",
        "phrases":["... kararını verdim çünkü ...","Bunun en önemli nedeni ...","Daha fazla zamanım olsaydı ..."],
        "examples":["Akşam kursuna katılmaya karar verdim çünkü gündüz çalışıyorum. Daha fazla zamanım olsaydı konuşma pratiği de yapardım."]
    },
    ("B1","b1-unit-1","writing"): {
        "title":"Bir deneyimini anlat",
        "objective":"Bir deneyimi neden, sonuç ve kişisel değerlendirmeyle anlatmak.",
        "prompt":"100–120 kelimeyle öğrendiğin bir beceriyi veya yaşadığın önemli bir deneyimi anlat. Neden başladığını, ne öğrendiğini ve bugün nasıl değerlendirdiğini yaz.",
        "guidance":["Geçmiş zaman eklerini doğru kullan.","çünkü, bu yüzden ve ayrıca gibi bağlaçlar kullan.","Sonunda kişisel bir değerlendirme yap."],
        "examples":["Geçen yıl Türkçe konuşma kursuna başladım çünkü günlük hayatta daha rahat konuşmak istiyordum. İlk başta zorlandım, fakat düzenli çalıştım. Birkaç ay sonra insanlarla daha kolay iletişim kurmaya başladım."]
    },
    ("B1","b1-unit-1","review"): {
        "title":"Deneyim ve kararlar tekrarı",
        "objective":"Deneyim anlatımı, neden-sonuç bağlantıları ve varsayımsal ifadeleri tekrar etmek.",
        "questions":[
            ("Neden-sonuç ilişkisi kuran ifade hangisidir?",["çünkü","ama","ve"],"çünkü"),
            ("Hangisi varsayımsal bir durumdur?",["Daha fazla zamanım olsaydı daha çok okurdum.","Dün kitap okudum.","Şimdi kitap okuyorum."],"Daha fazla zamanım olsaydı daha çok okurdum."),
            ("Hangisi geçmiş bir deneyimi anlatır?",["Geçen yıl kursa başladım.","Gelecek yıl kursa başlayacağım.","Şimdi kursa gidiyorum."],"Geçen yıl kursa başladım.")
        ]
    },

    ("B2","b2-unit-1","listening"): {
        "title":"Geçmiş bir kararı değerlendirmek",
        "objective":"Bir konuşmada pişmanlık, alternatifler ve sonuçlar arasındaki ilişkiyi anlamak.",
        "transcript":"Selin: Geriye dönünce o işi kabul edebilirdim diye düşünüyorum. Yeni deneyimler kazanırdım. Ancak o dönemde taşınmak ailem için çok zordu. Bu yüzden bugün kararıma daha farklı bakıyorum.",
        "questions":[
            ("Selin neyi düşünüyor?",["İşi kabul edebileceğini","Şehri hemen terk ettiğini","Yeni bir kursa başladığını"],"İşi kabul edebileceğini"),
            ("Taşınmak neden zordu?",["Ailesi için zor olduğu için","İş olmadığı için","Kurs başladığı için"],"Ailesi için zor olduğu için"),
            ("Selin bugün kararına nasıl bakıyor?",["Daha farklı bakıyor","Hiç düşünmüyor","Kesinlikle pişman"],"Daha farklı bakıyor")
        ]
    },
    ("B2","b2-unit-1","speaking"): {
        "title":"Alternatifleri tartış",
        "objective":"Bir kararın avantaj ve dezavantajlarını tartışmak ve karşıt görüşü değerlendirmek.",
        "prompt":"İki farklı seçenek içeren bir karar seç. Her seçeneğin avantajlarını ve dezavantajlarını açıkla; sonunda hangi koşulda hangi seçeneği tercih edeceğini belirt.",
        "phrases":["Bir yandan ..., diğer yandan ...","Bunun avantajı ...","Öte yandan ...","Bu koşullarda ... daha mantıklı olurdu."],
        "examples":["Bir yandan yeni iş daha iyi fırsatlar sunuyor, diğer yandan taşınmak gerekiyor. Bu koşullarda aile durumuna göre karar vermek daha mantıklı olurdu."]
    },
    ("B2","b2-unit-1","writing"): {
        "title":"İki seçeneği karşılaştır",
        "objective":"İki seçeneği kanıt, karşılaştırma ve sonuç bölümleriyle dengeli biçimde değerlendirmek.",
        "prompt":"160–200 kelimeyle iki farklı seçenek içeren bir karar hakkında yaz. Her seçeneğin avantaj ve dezavantajlarını karşılaştır ve sonunda gerekçeli bir sonuç ver.",
        "guidance":["bir yandan ... diğer yandan yapısını kullan.","En az bir varsayımsal cümle yaz.","Sonuç bölümünde gerekçeni açıkça belirt."],
        "examples":["Bir yandan yeni iş daha iyi kariyer fırsatları sunuyor. Diğer yandan taşınma ve ek masraflar gerekiyor. Eğer aile koşullarım farklı olsaydı, yeni işi kabul edebilirdim."]
    },
    ("B2","b2-unit-1","review"): {
        "title":"Karşılaştırma ve varsayım tekrarı",
        "objective":"Geçmiş varsayımlarını, karşıtlık bağlaçlarını ve sonuç ifadelerini pekiştirmek.",
        "questions":[
            ("Karşıtlık bildiren ifade hangisidir?",["diğer yandan","bu yüzden","örneğin"],"diğer yandan"),
            ("Hangisi gerçekleşmemiş bir olasılığı anlatır?",["Kabul edebilirdim.","Kabul ediyorum.","Kabul edeceğim."],"Kabul edebilirdim."),
            ("Hangisi dengeli bir değerlendirmedir?",["Hem avantajları hem dezavantajları var.","Sadece avantajları var.","Hiçbir sonucu yok."],"Hem avantajları hem dezavantajları var.")
        ]
    },

    ("C1","c1-unit-1","listening"): {
        "title":"Veriler ne gösteriyor?",
        "objective":"Bir uzman açıklamasında bulgu, yorum ve belirsizlik arasındaki farkı anlamak.",
        "transcript":"Araştırma, düzenli kısa çalışma dönemleri ile daha iyi sonuçlar arasında belirgin bir ilişki olduğunu gösteriyor. Ancak bu sonuç, tek başına çalışma süresinin başarıya neden olduğunu kanıtlamıyor. Motivasyon ve önceki deneyim de etkili olabilir.",
        "questions":[
            ("Araştırma ne gösteriyor?",["Bir ilişki olduğunu","Kesin bir nedensellik olduğunu","Motivasyonun önemsiz olduğunu"],"Bir ilişki olduğunu"),
            ("Sonuç neyi kanıtlamıyor?",["Tek başına çalışma süresinin nedenselliğini","Verilerin varlığını","Katılımcıların çalıştığını"],"Tek başına çalışma süresinin nedenselliğini"),
            ("Hangi faktörler de etkili olabilir?",["Motivasyon ve önceki deneyim","Hava ve ulaşım","Yaş ve şehir"],"Motivasyon ve önceki deneyim")
        ]
    },
    ("C1","c1-unit-1","speaking"): {
        "title":"Bir tezi temkinli değerlendir",
        "objective":"Bir görüşü kanıtlarla değerlendirmek, belirsizliği işaretlemek ve dengeli sonuç çıkarmak.",
        "prompt":"Eğitim, çalışma veya teknoloji hakkında bir tez seç. İki gerekçe sun, en az bir noktayı sınırlandır ve sonunda ölçülü bir sonuç çıkar.",
        "phrases":["Eldeki veriler ... gösteriyor.","Bundan doğrudan ... sonucu çıkarılamaz.","Bununla birlikte ...","Dolayısıyla daha temkinli bir ifadeyle ..."],
        "examples":["Eldeki veriler yöntemin yararlı olabileceğini gösteriyor. Bundan herkes için aynı sonucu doğuracağı sonucu çıkarılamaz."]
    },
    ("C1","c1-unit-1","writing"): {
        "title":"Dengeli bir analiz yaz",
        "objective":"Kanıtları, karşı görüşü ve belirsizliği açıkça ayıran akademik bir metin yazmak.",
        "prompt":"220–280 kelimeyle tartışmalı bir tez hakkında analiz yaz. En az iki gerekçe, bir karşı görüş ve ölçülü bir sonuç kullan.",
        "guidance":["Bulgu ile yorumu birbirinden ayır.","muhtemelen, görünüşe göre veya ... düşünülebilir gibi ifadeler kullan.","Sonucun kapsamını açıkça sınırlandır."],
        "examples":["Sonuçlar düzenli çalışmanın yararlı olabileceğine işaret ediyor. Bununla birlikte, yöntemin tek başına başarıyı açıkladığı söylenemez."]
    },
    ("C1","c1-unit-1","review"): {
        "title":"Belirsizlik ve çıkarım tekrarı",
        "objective":"Kesinlik derecelerini, çıkarım ifadelerini ve temkinli akademik dili tekrar etmek.",
        "questions":[
            ("Güçlü bir çıkarım hangisidir?",["Mutlaka doğru olmalı.","Belki doğru olabilir.","Belki de yanlıştır."],"Mutlaka doğru olmalı."),
            ("Temkinli bir ifade hangisidir?",["... düşünülebilir.","Kesinlikle her zaman böyledir.","Hiçbir istisna yoktur."],"... düşünülebilir."),
            ("Akademik değerlendirmede ne ayrılmalıdır?",["Bulgu ve yorum","Başlık ve sayfa","Soru ve nokta"],"Bulgu ve yorum")
        ]
    },

    ("C2","c2-unit-1","listening"): {
        "title":"İlişki, nedensellik ve kapsam",
        "objective":"Yoğun bir akademik açıklamada nedensellik iddiasının koşullarını ve kapsam sınırlarını çözümlemek.",
        "transcript":"Gözlemlenen bir ilişki başlangıçta yalnızca betimleyici bir nitelik taşır. Nedensel bir yorum için alternatif açıklamaların ve olası karıştırıcı değişkenlerin sistematik biçimde incelenmesi gerekir. Bunun ardından bile bulgunun başka bağlamlara ne ölçüde aktarılabileceği ayrıca değerlendirilmelidir.",
        "questions":[
            ("Gözlemlenen ilişki başlangıçta hangi niteliği taşır?",["Betimleyici","Kesin nedensel","Normatif"],"Betimleyici"),
            ("Nedensel yorumdan önce ne incelenmelidir?",["Alternatif açıklamalar ve karıştırıcı değişkenler","Sadece ilk izlenim","Yalnızca başlık"],"Alternatif açıklamalar ve karıştırıcı değişkenler"),
            ("Başka hangi konu ayrıca değerlendirilmelidir?",["Bulgunun başka bağlamlara aktarılabilirliği","Konuşmacının yaşı","Metnin uzunluğu"],"Bulgunun başka bağlamlara aktarılabilirliği")
        ]
    },
    ("C2","c2-unit-1","speaking"): {
        "title":"İncelikli bir argüman kur",
        "objective":"Karmaşık bir tezi karşı görüşü hesaba katarak, kapsamını sınırlandırarak ve kesinlik derecesini kontrol ederek savunmak.",
        "prompt":"İleri düzey bir tez seç. Görüşünü açıkça kur, güçlü bir karşı görüşü ele al, kendi iddianı uygun yerde sınırlandır ve sonuçta hangi koşullarda geçerli olduğunu belirt.",
        "phrases":["Bu tez şu açıdan savunulabilir: ...","Ancak bu açıklama ... durumunda yetersiz kalır.","Buradan ... sonucunu çıkarmak erken olur.","Dolayısıyla daha isabetli ifade ... olacaktır."],
        "examples":["Bu tez verilerdeki ilişki açısından savunulabilir. Ancak alternatif nedenler dikkate alınmadığında bu açıklama yetersiz kalır."]
    },
    ("C2","c2-unit-1","writing"): {
        "title":"İleri düzey argümantasyon",
        "objective":"Karşı görüş, kip seçimi, kapsam sınırı ve sonuç arasında tutarlı bir akademik argüman kurmak.",
        "prompt":"300–400 kelimeyle ileri düzey bir tez hakkında bağımsız bir argüman yaz. Bir karşı görüşü ele al, bir varsayımsal değerlendirme ekle ve bulgu, yorum ve sonuç arasındaki farkı açıkça göster.",
        "guidance":["Dolaylı aktarımda uygun biçimde -miş veya aktarma yapılarını kullan.","Varsayımsal durumlarda koşul yapısını bilinçli seç.","Genellemelerin kapsamını sınırlandır."],
        "examples":["Araştırma, yöntemin etkili olduğunu düşündürüyor; ancak bunun her koşulda üstün olduğu sonucuna varmak erken olacaktır."]
    },
    ("C2","c2-unit-1","review"): {
        "title":"İncelikli dil kullanımı – Review",
        "objective":"Kapsam sınırlandırma, karşı görüş ve temkinli çıkarım yapılarını tekrar etmek.",
        "questions":[
            ("Temkinli bir sonuç hangisidir?",["Buradan kesin olarak şu sonucu çıkaramayız.","Bu her durumda böyledir.","Bunun hiçbir istisnası yoktur."],"Buradan kesin olarak şu sonucu çıkaramayız."),
            ("Karşı görüşü tanıtan ifade hangisidir?",["Bununla birlikte","Kesinlikle","Örneğin değil"],"Bununla birlikte"),
            ("İyi bir ileri düzey argüman ne yapar?",["İddianın kapsamını ve dayanaklarını açıklar","Her şeyi kesin kabul eder","Karşı görüşleri yok sayar"],"İddianın kapsamını ve dayanaklarını açıklar")
        ]
    },

}


def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict | None:
    return LESSON_SEEDS.get((level.upper(), unit_id, lesson_type))
