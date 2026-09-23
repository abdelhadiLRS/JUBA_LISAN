"""A1 phrasebook — practical nl situations."""
from app.data._types import PhrasebookCategory, PhrasebookEntry

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Begroetingen",icon="👋",phrases=[PhrasebookEntry(phrase="Hallo.",translation="Hello."),PhrasebookEntry(phrase="Hoe heet je?",translation="What is your name?"),PhrasebookEntry(phrase="Ik heet Anna.",translation="My name is Anna."),PhrasebookEntry(phrase="Tot ziens.",translation="Goodbye.")]),
    PhrasebookCategory(id="daily_a1",level="A1",situation="Dagelijks leven",icon="⏰",phrases=[PhrasebookEntry(phrase="Hoe laat is het?",translation="What time is it?"),PhrasebookEntry(phrase="Ik sta om zeven uur op.",translation="I get up at seven."),PhrasebookEntry(phrase="Ik ga naar mijn werk.",translation="I go to work."),PhrasebookEntry(phrase="Ik ben 's avonds thuis.",translation="I am home in the evening.")]),
    PhrasebookCategory(id="shopping_a1",level="A1",situation="Winkelen",icon="🛒",phrases=[PhrasebookEntry(phrase="Hoeveel kost dit?",translation="How much does this cost?"),PhrasebookEntry(phrase="Ik wil dit.",translation="I want this."),PhrasebookEntry(phrase="Heeft u een andere maat?",translation="Do you have another size?"),PhrasebookEntry(phrase="Kan ik met de kaart betalen?",translation="Can I pay by card?")]),
    PhrasebookCategory(id="help_a1",level="A1",situation="Hulp",icon="💬",phrases=[PhrasebookEntry(phrase="Ik begrijp het niet.",translation="I don't understand."),PhrasebookEntry(phrase="Kunt u dat herhalen?",translation="Could you repeat that?"),PhrasebookEntry(phrase="Kunt u langzamer praten?",translation="Could you speak more slowly?"),PhrasebookEntry(phrase="Kunt u mij helpen?",translation="Could you help me?")]),
    PhrasebookCategory(id="daily_a2",level="A2",situation="Daily life",icon="🏠",phrases=[]),
    PhrasebookCategory(id="work_b1",level="B1",situation="Work",icon="💼",phrases=[]),
    PhrasebookCategory(id="formal_b2",level="B2",situation="Formal communication",icon="📝",phrases=[]),
    PhrasebookCategory(id="academic_c1",level="C1",situation="Academic communication",icon="🎓",phrases=[]),
    PhrasebookCategory(id="advanced_c2",level="C2",situation="Advanced communication",icon="🧠",phrases=[]),
]
