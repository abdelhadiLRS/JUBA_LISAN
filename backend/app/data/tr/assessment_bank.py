"""Türkçe assessments — A1 real-content checks plus CEFR placeholders."""
from app.data._types import AssessmentQuestion

ASSESSMENT_BANK = [
    AssessmentQuestion(id="tr-a1-001",skill="communication",difficulty="A1",question="Bir arkadaşınızla karşılaşıyorsunuz. Hangi ifade “Hello” anlamına gelir?",options=["Merhaba!","İyi geceler!","Teşekkürler!","Görüşürüz!"],correct="Merhaba!"),
    AssessmentQuestion(id="tr-a1-002",skill="grammar",difficulty="A1",question="Kendinizi öğrenci olarak tanıtmak istiyorsunuz. Doğru cümleyi seçin.",options=["Ben öğrenciyim.","Ben öğrencisin.","Ben öğrencidir.","Ben öğrenciyiz."],correct="Ben öğrenciyim."),
    AssessmentQuestion(id="tr-a1-003",skill="grammar",difficulty="A1",question="Birine “Are you ready?” diye sormak istiyorsunuz. Doğru soru hangisidir?",options=["Hazır mısın?","Hazır mısın.","Hazır misin?","Hazır sen mi?"],correct="Hazır mısın?"),
    AssessmentQuestion(id="tr-a1-004",skill="grammar",difficulty="A1",question="“I am at home.” demek istiyorsunuz. Hangi cümleyi kullanırsınız?",options=["Evdeyim.","Eveyim.","Eviyim.","Evdeyiz."],correct="Evdeyim."),
    AssessmentQuestion(id="tr-a1-005",skill="vocabulary",difficulty="A1",question="Ailenizden bahsediyorsunuz. “kardeş” kelimesinin İngilizce karşılığı hangisidir?",options=["sibling","school","door","water"],correct="sibling"),
    AssessmentQuestion(id="tr-a1-006",skill="grammar",difficulty="A1",question="Türkçe bilmediğinizi söylemek istiyorsunuz. Doğru olumsuz cümleyi seçin.",options=["Türkçe bilmiyorum.","Türkçe biliyorum.","Türkçe bilirsin.","Türkçe biliyor."],correct="Türkçe bilmiyorum."),
    AssessmentQuestion(id="tr-a1-007",skill="communication",difficulty="A1",question="Bir mağazada fiyat sormak istiyorsunuz. Hangi ifadeyi kullanırsınız?",options=["Bu ne kadar?","Nasılsın?","Nerede yaşıyorsun?","Günaydın."],correct="Bu ne kadar?"),
    AssessmentQuestion(id="tr-a1-008",skill="grammar",difficulty="A1",question="Şu anda Türkçe öğrendiğinizi söylemek istiyorsunuz. Doğru cümleyi seçin.",options=["Ben Türkçe öğreniyorum.","Ben Türkçe öğreniyorsun.","Ben Türkçe öğreniyor.","Ben Türkçe öğrendim."],correct="Ben Türkçe öğreniyorum."),
    AssessmentQuestion(id="tr-a1-009",skill="reading",difficulty="A1",question="“İstasyon yakın.” cümlesini okuyorsunuz. Anlamı hangisidir?",options=["The station is near.","The station is closed.","The station is far.","The station is open."],correct="The station is near."),
    AssessmentQuestion(id="tr-a1-010",skill="communication",difficulty="A1",question="Bir konuşmayı anlamadığınızda hangi ifadeyi kullanırsınız?",options=["Anlamıyorum.","Görüşürüz.","Teşekkürler.","Günaydın."],correct="Anlamıyorum."),
    AssessmentQuestion(id="tr-a2-001",skill="grammar",difficulty="A2",question="Choose the correct form.",options=["A","B","C","D"],correct="A"),
    AssessmentQuestion(id="tr-b1-001",skill="grammar",difficulty="B1",question="Choose the correct structure.",options=["A","B","C","D"],correct="A"),
    AssessmentQuestion(id="tr-b2-001",skill="grammar",difficulty="B2",question="Choose the formal structure.",options=["A","B","C","D"],correct="A"),
    AssessmentQuestion(id="tr-c1-001",skill="grammar",difficulty="C1",question="Choose the academic expression.",options=["A","B","C","D"],correct="A"),
    AssessmentQuestion(id="tr-c2-001",skill="reading",difficulty="C2",question="Choose the best interpretation.",options=["A","B","C","D"],correct="A"),
]
