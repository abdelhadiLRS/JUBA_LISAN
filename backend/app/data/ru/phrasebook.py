"""Русский phrasebook A1-C2 — практические ситуации."""
from app.data._types import PhrasebookCategory, PhrasebookEntry

def _p(id,level,situation,phrases):
    return PhrasebookCategory(id=id,level=level,situation=situation,icon="",phrases=[PhrasebookEntry(phrase=a,translation=b) for a,b in phrases])

PHRASEBOOK_CATEGORIES=[
_p("greetings_a1","A1","Знакомство",[("Здравствуйте!","Hello!"),("Как вас зовут?","What is your name?"),("Меня зовут Анна.","My name is Anna.")]),
_p("daily_a1","A1","Повседневная жизнь",[("Который час?","What time is it?"),("Я сейчас занят.","I am busy right now."),("Увидимся вечером.","See you in the evening.")]),
_p("shopping_a1","A1","Покупки",[("Сколько это стоит?","How much does this cost?"),("Мне нужен этот размер.","I need this size."),("Можно оплатить картой?","Can I pay by card?")]),
_p("help_a1","A1","Помощь",[("Я не понимаю.","I don't understand."),("Повторите, пожалуйста.","Please repeat."),("Говорите медленнее, пожалуйста.","Please speak more slowly.")]),
_p("home_a2","A2","Дом и город",[("Где находится ближайшая аптека?","Where is the nearest pharmacy?"),("Я живу недалеко от центра.","I live not far from the centre."),("Как пройти к вокзалу?","How do I get to the station?")]),
_p("travel_a2","A2","Путешествия",[("Где можно купить билет?","Where can I buy a ticket?"),("Во сколько отправляется поезд?","What time does the train leave?"),("Мне нужно сделать пересадку.","I need to change trains.")]),
_p("health_a2","A2","Здоровье",[("Мне плохо.","I feel unwell."),("У меня болит голова.","I have a headache."),("Мне нужна запись к врачу.","I need a doctor's appointment.")]),
_p("work_a2","A2","Работа и досуг",[("Я работаю до пяти.","I work until five."),("Чем вы занимаетесь?","What do you do?"),("Давайте встретимся завтра.","Let's meet tomorrow.")]),
_p("education_b1","B1","Учёба",[("Я изучаю эту тему уже год.","I have been studying this topic for a year."),("Мне нужно подготовиться к экзамену.","I need to prepare for the exam."),("Можете объяснить этот термин?","Can you explain this term?")]),
_p("opinions_b1","B1","Мнения и отношения",[("Я считаю, что это важно.","I think this is important."),("С моей точки зрения, решение разумное.","From my point of view, the decision is reasonable."),("Я не совсем с вами согласен.","I don't entirely agree with you.")]),
_p("debate_b2","B2","Дискуссия",[("Позвольте уточнить этот аргумент.","Allow me to clarify this argument."),("Это утверждение требует доказательств.","This claim requires evidence."),("С другой стороны, есть иные данные.","On the other hand, there is other data.")]),
_p("professional_b2","B2","Профессиональное общение",[("Предлагаю обсудить это отдельно.","I suggest discussing this separately."),("Нам необходимо уточнить сроки.","We need to clarify the deadlines."),("Давайте зафиксируем договорённости.","Let's record the agreements.")]),
_p("academic_c1","C1","Академическое общение",[("Полученные данные позволяют предположить, что...","The data obtained suggest that..."),("Необходимо различать эти два понятия.","It is necessary to distinguish these two concepts."),("Этот вывод требует дополнительной проверки.","This conclusion requires further verification.")]),
_p("society_c1","C1","Общественный анализ",[("Этот вопрос имеет несколько измерений.","This issue has several dimensions."),("Нельзя игнорировать контекст.","The context cannot be ignored."),("Следует учитывать альтернативные объяснения.","Alternative explanations should be considered.")]),
_p("style_c2","C2","Стиль и регистр",[("Это формулировка звучит слишком категорично.","This wording sounds too categorical."),("Можно выразить ту же мысль точнее.","The same idea can be expressed more precisely."),("Здесь уместен нейтральный регистр.","A neutral register is appropriate here.")]),
_p("rhetoric_c2","C2","Риторика и аргументация",[("Главный вопрос заключается в следующем.","The central question is the following."),("Этот аргумент не учитывает ключевого различия.","This argument overlooks a key distinction."),("Важно отделить факт от интерпретации.","It is important to separate fact from interpretation.")]),
_p("critical_c2","C2","Критическое чтение",[("Какое предположение лежит в основе этого вывода?","What assumption underlies this conclusion?"),("Есть ли данные, подтверждающие это утверждение?","Is there evidence supporting this claim?"),("Этот вывод выходит за пределы представленных данных.","This conclusion goes beyond the presented data.")]),
_p("synthesis_c2","C2","Синтез",[("Если сопоставить эти результаты, видна общая тенденция.","If these results are compared, a general trend emerges."),("Источники сходятся в основном выводе, но расходятся в деталях.","The sources agree on the main conclusion but differ in details."),("Итоговая формулировка должна сохранить это различие.","The final wording should preserve this distinction.")])
]
