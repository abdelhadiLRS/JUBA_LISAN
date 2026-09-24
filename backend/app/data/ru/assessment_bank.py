"""Русский assessment foundation."""
from app.data._types import AssessmentQuestion

ASSESSMENT_BANK=[
AssessmentQuestion(id="ru-a1-001",skill="communication",difficulty="A1",question="Вы встречаете друга. Как поздороваться?",options=["Привет!","Спасибо!","До свидания!","Спокойной ночи!"],correct="Привет!"),
AssessmentQuestion(id="ru-a1-002",skill="grammar",difficulty="A1",question="Вы хотите сказать «I am a student». Как правильно?",options=["Я студент.","Я студента.","Я студенты.","Я студентом."],correct="Я студент."),
AssessmentQuestion(id="ru-a1-003",skill="communication",difficulty="A1",question="Вы хотите спросить имя человека. Какой вопрос подходит?",options=["Как тебя зовут?","Где магазин?","Сколько это стоит?","Который час?"],correct="Как тебя зовут?"),
AssessmentQuestion(id="ru-a1-004",skill="grammar",difficulty="A1",question="Вы хотите сказать «I don't understand». Как правильно?",options=["Я не понимаю.","Я не понимать.","Я понимаю не.","Я нет понимаю."],correct="Я не понимаю."),
AssessmentQuestion(id="ru-a1-005",skill="vocabulary",difficulty="A1",question="Какое слово означает «water»?",options=["вода","хлеб","дом","книга"],correct="вода"),
AssessmentQuestion(id="ru-a1-006",skill="vocabulary",difficulty="A1",question="Вы говорите о семье. Как по-русски «mother»?",options=["мать","отец","брат","друг"],correct="мать"),
AssessmentQuestion(id="ru-a1-007",skill="communication",difficulty="A1",question="Вы в магазине и хотите узнать цену. Что спросить?",options=["Сколько это стоит?","Как вас зовут?","Где вы живёте?","Что это?"],correct="Сколько это стоит?"),
AssessmentQuestion(id="ru-a1-008",skill="grammar",difficulty="A1",question="Вы хотите сказать «I live in Moscow». Какое предложение правильное?",options=["Я живу в Москве.","Я жить в Москве.","Я живу Москва.","Я живёт в Москве."],correct="Я живу в Москве."),
AssessmentQuestion(id="ru-a1-009",skill="reading",difficulty="A1",question="Вы читаете «Школа рядом». Что это значит?",options=["The school is nearby.","The school is closed.","The school is far away.","The school is new."],correct="The school is nearby."),
AssessmentQuestion(id="ru-a1-010",skill="communication",difficulty="A1",question="Кто-то помогает вам. Что вы скажете?",options=["Спасибо!","Привет!","До свидания!","Извините?"],correct="Спасибо!"),
AssessmentQuestion(id="ru-a2-001",skill="grammar",difficulty="A2",question="Choose the correct form.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="ru-b1-001",skill="grammar",difficulty="B1",question="Choose the correct structure.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="ru-b2-001",skill="grammar",difficulty="B2",question="Choose the formal structure.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="ru-c1-001",skill="grammar",difficulty="C1",question="Choose the academic expression.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="ru-c2-001",skill="reading",difficulty="C2",question="Choose the best interpretation.",options=["A","B","C","D"],correct="A"),
]
