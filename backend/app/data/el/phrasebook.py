"""A1 phrasebook — practical el situations."""
from app.data._types import PhrasebookCategory, PhrasebookEntry

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Χαιρετισμοί",icon="👋",phrases=[PhrasebookEntry(phrase="Γεια σου.",translation="Hello."),PhrasebookEntry(phrase="Πώς σε λένε;",translation="What is your name?"),PhrasebookEntry(phrase="Με λένε Άννα.",translation="My name is Anna."),PhrasebookEntry(phrase="Αντίο.",translation="Goodbye.")]),
    PhrasebookCategory(id="daily_a1",level="A1",situation="Καθημερινή ζωή",icon="⏰",phrases=[PhrasebookEntry(phrase="Τι ώρα είναι;",translation="What time is it?"),PhrasebookEntry(phrase="Σηκώνομαι στις επτά.",translation="I get up at seven."),PhrasebookEntry(phrase="Πηγαίνω στη δουλειά.",translation="I go to work."),PhrasebookEntry(phrase="Το βράδυ είμαι στο σπίτι.",translation="I am at home in the evening.")]),
    PhrasebookCategory(id="shopping_a1",level="A1",situation="Αγορές",icon="🛒",phrases=[PhrasebookEntry(phrase="Πόσο κοστίζει αυτό;",translation="How much does this cost?"),PhrasebookEntry(phrase="Θέλω αυτό.",translation="I want this."),PhrasebookEntry(phrase="Έχετε άλλο μέγεθος;",translation="Do you have another size?"),PhrasebookEntry(phrase="Μπορώ να πληρώσω με κάρτα;",translation="Can I pay by card?")]),
    PhrasebookCategory(id="help_a1",level="A1",situation="Βοήθεια",icon="💬",phrases=[PhrasebookEntry(phrase="Δεν καταλαβαίνω.",translation="I don't understand."),PhrasebookEntry(phrase="Μπορείτε να το επαναλάβετε;",translation="Could you repeat that?"),PhrasebookEntry(phrase="Μιλάτε πιο αργά, παρακαλώ.",translation="Please speak more slowly."),PhrasebookEntry(phrase="Μπορείτε να με βοηθήσετε;",translation="Could you help me?")]),
    PhrasebookCategory(id="daily_a2",level="A2",situation="Daily life",icon="🏠",phrases=[]),
    PhrasebookCategory(id="work_b1",level="B1",situation="Work",icon="💼",phrases=[]),
    PhrasebookCategory(id="formal_b2",level="B2",situation="Formal communication",icon="📝",phrases=[]),
    PhrasebookCategory(id="academic_c1",level="C1",situation="Academic communication",icon="🎓",phrases=[]),
    PhrasebookCategory(id="advanced_c2",level="C2",situation="Advanced communication",icon="🧠",phrases=[]),
]
