"""A1 phrasebook — practical ru situations."""
from app.data._types import PhrasebookCategory, PhrasebookEntry

PHRASEBOOK_CATEGORIES=[
    PhrasebookCategory(id="greetings_a1",level="A1",situation="Greetings",icon="👋",phrases=[PhrasebookEntry(phrase="Привет.",translation="Hello."),PhrasebookEntry(phrase="Как тебя зовут?",translation="What is your name?"),PhrasebookEntry(phrase="Меня зовут Анна.",translation="My name is Anna."),PhrasebookEntry(phrase="До свидания.",translation="Goodbye.")]),
    PhrasebookCategory(id="daily_a1",level="A1",situation="Daily routine",icon="⏰",phrases=[PhrasebookEntry(phrase="Который час?",translation="What time is it?"),PhrasebookEntry(phrase="Я встаю в семь.",translation="I get up at seven."),PhrasebookEntry(phrase="Я иду на работу.",translation="I am going to work."),PhrasebookEntry(phrase="Я дома вечером.",translation="I am at home in the evening.")]),
    PhrasebookCategory(id="shopping_a1",level="A1",situation="Shopping",icon="🛒",phrases=[PhrasebookEntry(phrase="Сколько это стоит?",translation="How much does this cost?"),PhrasebookEntry(phrase="Я хочу это.",translation="I want this."),PhrasebookEntry(phrase="Есть другой размер?",translation="Is there another size?"),PhrasebookEntry(phrase="Можно оплатить картой?",translation="Can I pay by card?")]),
    PhrasebookCategory(id="help_a1",level="A1",situation="Help",icon="💬",phrases=[PhrasebookEntry(phrase="Я не понимаю.",translation="I don't understand."),PhrasebookEntry(phrase="Повторите, пожалуйста.",translation="Please repeat."),PhrasebookEntry(phrase="Говорите медленнее, пожалуйста.",translation="Please speak more slowly."),PhrasebookEntry(phrase="Помогите, пожалуйста.",translation="Please help me.")]),
    PhrasebookCategory(id="daily_a2",level="A2",situation="Daily life",icon="🏠",phrases=[]),
    PhrasebookCategory(id="work_b1",level="B1",situation="Work",icon="💼",phrases=[]),
    PhrasebookCategory(id="formal_b2",level="B2",situation="Formal communication",icon="📝",phrases=[]),
    PhrasebookCategory(id="academic_c1",level="C1",situation="Academic communication",icon="🎓",phrases=[]),
    PhrasebookCategory(id="advanced_c2",level="C2",situation="Advanced communication",icon="🧠",phrases=[]),
]
