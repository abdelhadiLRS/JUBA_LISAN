"""Türkçe A1 grammar — expanded learner-ready foundation."""
from app.data._types import GrammarTopic, GrammarExample

def _g(slug,title,summary,explanation,examples,rules=None):
    return GrammarTopic(slug=slug,title=title,level="A1",category="core",summary=summary,explanation=explanation,structure=None,rules=rules or [],examples=[GrammarExample(text=x) for x in examples],common_mistakes=[],related=[])

GRAMMAR_TOPICS = [
    _g("pronouns","Kişi zamirleri","Ben, sen, o ve çoğul kişi zamirlerini kullanma.","Türkçede kişi zamirleri özneyi belirtir; günlük konuşmada fiil eki de kişiyi gösterebilir.",["Ben öğrenciyim.","Sen öğretmensin.","O Ankara'da."],[ "Ben / sen / o / biz / siz / onlar temel kişi zamirleridir."]),
    _g("nominal-sentence","İsim cümleleri","İsim ve sıfatlarla temel cümleler kurma.","Türkçede şimdiki zamanda isim cümlelerinde kişi ekleri kullanılır.",["Ben öğrenciyim.","Sen yorgunsun.","Biz hazırız."],[ "Ben öğrenciyim; sen öğrencisin; o öğrenci."]),
    _g("vowel-harmony","Ünlü uyumu","Ekleri kelimenin ses yapısına göre seçme.","Türkçedeki birçok ek, kelimedeki son ünlünün özelliklerine göre biçim değiştirir.",["evler","kitaplar","günler"],["Çoğul eki -ler/-lar, son ünlüye göre değişir."]),
    _g("plural","Çoğul eki","İsimleri çoğul yapma.","İsimlerin çoğulu temel olarak -ler veya -lar ekiyle yapılır.",["kitaplar","evler","öğrenciler"],["-lar ve -ler ekleri ünlü uyumuna göre seçilir."]),
    _g("present-progressive","Şimdiki zaman","Şu anda olan eylemleri anlatma.","-iyor yapısı devam eden eylemleri anlatmak için kullanılır ve kişi ekleri alır.",["Ben Türkçe öğreniyorum.","Sen ne yapıyorsun?","O çalışıyor."],["Fiil + -iyor + kişi eki temel kalıptır."]),
    _g("question-particle","Soru eki mi","Evet-hayır soruları kurma.","mi soru parçacığı ayrı yazılır ve sonraki kişi eki ona bağlanır.",["Öğrenci misin?","Hazır mısın?","Türk müsünüz?"],["mi/mı/mu/mü ayrı yazılır."]),
    _g("negation","Olumsuzluk","Temel cümleleri olumsuz yapma.","Fiillerde -me/-ma, isim cümlelerinde değil kullanılır.",["Türkçe bilmiyorum.","Meşgul değilim.","O burada değil."],["Fiil: gelmiyorum. İsim/sıfat: değilim."]),
    _g("basic-cases","Temel hâl ekleri","Yer, yönelme ve belirtme ilişkilerini ifade etme.","A1 düzeyinde -e/-a, -de/-da ve -i/-ı/-u/-ü ekleriyle temel ilişkiler kurulur.",["Okula gidiyorum.","Evdeyim.","Kahveyi içiyorum."],["Ek seçimi ünlü uyumu ve ses uyumlarına bağlıdır."]),
]
