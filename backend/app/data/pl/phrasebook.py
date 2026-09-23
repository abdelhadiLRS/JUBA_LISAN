"""A1 phrasebook — practical pl situations."""
from app.data._types import PhrasebookCategory, PhrasebookEntry

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Powitania",icon="👋",phrases=[PhrasebookEntry(phrase="Cześć.",translation="Hello."),PhrasebookEntry(phrase="Jak masz na imię?",translation="What is your name?"),PhrasebookEntry(phrase="Mam na imię Anna.",translation="My name is Anna."),PhrasebookEntry(phrase="Do widzenia.",translation="Goodbye.")]),
    PhrasebookCategory(id="daily_a1",level="A1",situation="Codzienna rutyna",icon="⏰",phrases=[PhrasebookEntry(phrase="Która jest godzina?",translation="What time is it?"),PhrasebookEntry(phrase="Wstaję o siódmej.",translation="I get up at seven."),PhrasebookEntry(phrase="Idę do pracy.",translation="I am going to work."),PhrasebookEntry(phrase="Wieczorem jestem w domu.",translation="I am at home in the evening.")]),
    PhrasebookCategory(id="shopping_a1",level="A1",situation="Zakupy",icon="🛒",phrases=[PhrasebookEntry(phrase="Ile to kosztuje?",translation="How much does this cost?"),PhrasebookEntry(phrase="Chcę to.",translation="I want this."),PhrasebookEntry(phrase="Czy jest inny rozmiar?",translation="Is there another size?"),PhrasebookEntry(phrase="Czy mogę zapłacić kartą?",translation="Can I pay by card?")]),
    PhrasebookCategory(id="help_a1",level="A1",situation="Pomoc",icon="💬",phrases=[PhrasebookEntry(phrase="Nie rozumiem.",translation="I don't understand."),PhrasebookEntry(phrase="Czy może Pan/Pani powtórzyć?",translation="Could you repeat?"),PhrasebookEntry(phrase="Czy może Pan/Pani mówić wolniej?",translation="Could you speak more slowly?"),PhrasebookEntry(phrase="Czy może mi Pan/Pani pomóc?",translation="Could you help me?")]),
    PhrasebookCategory(id="daily_a2",level="A2",situation="Daily life",icon="🏠",phrases=[]),
    PhrasebookCategory(id="work_b1",level="B1",situation="Work",icon="💼",phrases=[]),
    PhrasebookCategory(id="formal_b2",level="B2",situation="Formal communication",icon="📝",phrases=[]),
    PhrasebookCategory(id="academic_c1",level="C1",situation="Academic communication",icon="🎓",phrases=[]),
    PhrasebookCategory(id="advanced_c2",level="C2",situation="Advanced communication",icon="🧠",phrases=[]),
]
