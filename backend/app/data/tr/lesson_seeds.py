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
}


def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict | None:
    return LESSON_SEEDS.get((level.upper(), unit_id, lesson_type))
