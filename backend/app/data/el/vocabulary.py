"""Ελληνικά A1 vocabulary — expanded thematic content."""
from app.data._types import VocabularySet, VocabularyEntry

def _w(word,pos,definition,example): return VocabularyEntry(word=word,pos=pos,definition=definition,example=example)

VOCABULARY_SETS=[
    VocabularySet(id="greetings_a1",level="A1",topic="greetings",unit_ref="a1-unit-1",words=[_w("γεια σου","phrase","hello","Γεια σου!"),_w("καλημέρα","phrase","good morning","Καλημέρα!"),_w("αντίο","phrase","goodbye","Αντίο!"),_w("παρακαλώ","phrase","please / you're welcome","Παρακαλώ."),_w("ευχαριστώ","phrase","thank you","Ευχαριστώ πολύ.")]),
    VocabularySet(id="identity_a1",level="A1",topic="identity",unit_ref="a1-unit-1",words=[_w("όνομα","noun","name","Με λένε Άννα."),_w("φοιτητής","noun","student","Είμαι φοιτητής."),_w("δάσκαλος","noun","teacher","Είναι δάσκαλος."),_w("χώρα","noun","country","Η Ελλάδα είναι χώρα."),_w("γλώσσα","noun","language","Μαθαίνω ελληνικά.")]),
    VocabularySet(id="family_a1",level="A1",topic="family",unit_ref="a1-unit-1",words=[_w("μητέρα","noun","mother","Η μητέρα μου είναι στο σπίτι."),_w("πατέρας","noun","father","Ο πατέρας μου δουλεύει."),_w("αδελφός","noun","brother","Έχω έναν αδελφό."),_w("αδελφή","noun","sister","Έχω μια αδελφή.")]),
    VocabularySet(id="daily-life_a1",level="A1",topic="daily life",unit_ref="a1-unit-1",words=[_w("σηκώνομαι","verb","to get up","Σηκώνομαι στις επτά."),_w("δουλεύω","verb","to work","Δουλεύω στο σπίτι."),_w("μαθαίνω","verb","to learn","Μαθαίνω κάθε μέρα."),_w("κοιμάμαι","verb","to sleep","Κοιμάμαι τη νύχτα.")]),
    VocabularySet(id="food_a1",level="A1",topic="food",unit_ref="a1-unit-1",words=[_w("νερό","noun","water","Θέλω νερό."),_w("ψωμί","noun","bread","Αγοράζω ψωμί."),_w("καφές","noun","coffee","Πίνω καφέ."),_w("μήλο","noun","apple","Θέλω ένα μήλο.")]),
    VocabularySet(id="daily_a2",level="A2",topic="Daily life",unit_ref="a2-unit-1",words=[]),
    VocabularySet(id="work_b1",level="B1",topic="Work",unit_ref="b1-unit-1",words=[]),
    VocabularySet(id="formal_c1",level="C1",topic="Formal language",unit_ref="c1-unit-1",words=[]),
    VocabularySet(id="advanced_c2",level="C2",topic="Advanced communication",unit_ref="c2-unit-1",words=[]),
]
