"""Türkçe A1 phrasebook — practical situations."""
from app.data._types import PhrasebookCategory, PhrasebookEntry

def _c(i,situation,phrases,icon):
    return PhrasebookCategory(id=i,level="A1",situation=situation,icon=icon,phrases=[
        PhrasebookEntry(phrase=p,translation=t) for p,t in phrases
    ])

PHRASEBOOK_CATEGORIES = [
    _c("greetings_a1","Greetings and introductions",[
        ("Merhaba.","Hello."),("Nasılsın?","How are you?"),("Benim adım Ali.","My name is Ali."),
        ("Memnun oldum.","Nice to meet you."),("Görüşürüz.","See you.")
    ],"👋"),
    _c("family_a1","Family",[
        ("Ailen nasıl?","How is your family?"),("Bu benim annem.","This is my mother."),
        ("Bir kardeşim var.","I have one sibling."),("Ailem burada.","My family is here.")
    ],"👨‍👩‍👧"),
    _c("daily_a1","Daily routine",[
        ("Saat kaç?","What time is it?"),("Saat yedide kalkıyorum.","I get up at seven."),
        ("İşe gidiyorum.","I am going to work."),("Akşam evdeyim.","I am at home in the evening.")
    ],"⏰"),
    _c("shopping_a1","Shopping",[
        ("Bu ne kadar?","How much is this?"),("Bunu istiyorum.","I want this."),
        ("Başka bir şey var mı?","Is there anything else?"),("Kartla ödeyebilir miyim?","Can I pay by card?")
    ],"🛒"),
    _c("directions_a1","Places and directions",[
        ("Tuvalet nerede?","Where is the toilet?"),("Sağa dön.","Turn right."),
        ("Düz gidin.","Go straight."),("İstasyon yakın mı?","Is the station near?")
    ],"🧭"),
    _c("help_a1","Help and clarification",[
        ("Anlamıyorum.","I don't understand."),("Tekrar eder misiniz?","Could you repeat?"),
        ("Yavaş konuşur musunuz?","Could you speak slowly?"),("Yardım eder misiniz?","Could you help?")
    ],"💬"),
    _c("daily_a2","Daily life",[],"🏠"),
    _c("work_b1","Work",[],"💼"),
    _c("formal_b2","Formal communication",[],"📝"),
    _c("academic_c1","Academic communication",[],"🎓"),
    _c("advanced_c2","Advanced communication",[],"🧠"),
]
