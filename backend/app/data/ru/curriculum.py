"""Русский CEFR curriculum A1-C2."""
from app.data._types import CurriculumUnit

def _u(level, n, title, grammar, vocab, goals, prereq=None):
    return CurriculumUnit(
        id=f"{level.lower()}-unit-{n}", level=level, unit_number=n, title=title,
        grammar_points=grammar, vocabulary_set_ids=vocab,
        lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
        competency_checklist=goals, default_weeks=2, prerequisite_unit=prereq,
    )

CURRICULUM = {
"A1":[
_u("A1",1,"Знакомство и базовые фразы",["pronouns","gender","present-tense"],["greetings_a1","identity_a1"],["Поздороваться и попрощаться","Представиться и сообщить базовые сведения"]),
_u("A1",2,"Семья и повседневная жизнь",["adjectives","negation"],["family_a1","daily-life_a1"],["Рассказать о семье","Описать простой распорядок дня"],"a1-unit-1"),
_u("A1",3,"Время, место и встречи",["questions","prepositions","basic-cases"],["time_a1","places_a1"],["Спросить время и место","Назначить простую встречу"],"a1-unit-2"),
_u("A1",4,"Еда и покупки",["accusative-basics","numbers"],["food_a1","shopping_a1"],["Купить продукты","Спросить цену и количество"],"a1-unit-3")],
"A2":[
_u("A2",1,"Дом и город",["past-tense","locative"],["home_a2","city_a2"],["Описать жильё","Ориентироваться в городе"],"a1-unit-4"),
_u("A2",2,"Путешествия и транспорт",["motion-verbs","future-tense"],["travel_a2","transport_a2"],["Спросить дорогу","Говорить о планах поездки"],"a2-unit-1"),
_u("A2",3,"Здоровье и услуги",["dative","reflexive-verbs"],["health_a2","services_a2"],["Объяснить простую проблему","Общаться в повседневных службах"],"a2-unit-2"),
_u("A2",4,"Работа и свободное время",["comparatives","imperative"],["work_a2","leisure_a2"],["Рассказать о работе","Предложить занятие и дать простую рекомендацию"],"a2-unit-3")],
"B1":[
_u("B1",1,"Учёба и опыт",["instrumental","aspect"],["education_b1","experience_b1"],["Рассказывать об опыте","Объяснять учебные цели"],"a2-unit-4"),
_u("B1",2,"Новости и общество",["subordinate-clauses","relative-pronouns"],["media_b1","society_b1"],["Понимать основную мысль новости","Связывать причины и последствия"],"b1-unit-1"),
_u("B1",3,"Отношения и чувства",["reported-speech","verb-government"],["relationships_b1","emotions_b1"],["Передавать слова другого человека","Выражать мнение и эмоции"],"b1-unit-2"),
_u("B1",4,"Проблемы и решения",["verbal-nouns","participles-intro"],["problems_b1","solutions_b1"],["Описать проблему","Предложить и обосновать решение"],"b1-unit-3")],
"B2":[
_u("B2",1,"Аргументация и дискуссия",["discourse-markers","conditionals"],["argumentation_b2","debate_b2"],["Строить аргумент","Соглашаться и возражать корректно"],"b1-unit-4"),
_u("B2",2,"Работа и лидерство",["passive","complex-objects"],["leadership_b2","workplace_b2"],["Участвовать в профессиональном обсуждении","Описывать процессы и ответственность"],"b2-unit-1"),
_u("B2",3,"Культура и идентичность",["concessive-clauses","aspectual-nuance"],["culture_b2","identity_b2"],["Сравнивать культурные явления","Выражать нюансированную позицию"],"b2-unit-2"),
_u("B2",4,"Сложные проблемы",["nominalization","advanced-conjunctions"],["policy_b2","solutions_b2"],["Анализировать сложную проблему","Формулировать несколько вариантов решения"],"b2-unit-3")],
"C1":[
_u("C1",1,"Нюанс и регистр",["register","hedging"],["nuance_c1","register_c1"],["Различать официальный и разговорный регистр","Смягчать категоричные утверждения"],"b2-unit-4"),
_u("C1",2,"Академический русский",["academic-syntax","cohesion"],["academic_c1","research_c1"],["Структурировать академический текст","Связывать аргументы и источники"],"c1-unit-1"),
_u("C1",3,"Профессиональная коммуникация",["complex-subordination","professional-style"],["professional_c1","meetings_c1"],["Вести профессиональную дискуссию","Писать точные деловые сообщения"],"c1-unit-2"),
_u("C1",4,"Общественный анализ",["nominal-style","discourse-organization"],["society_c1","analysis_c1"],["Анализировать общественные процессы","Формулировать выводы с оговорками"],"c1-unit-3")],
"C2":[
_u("C2",1,"Стиль и авторский голос",["stylistic-syntax","inversion-focus"],["style_c2","register_c2"],["Распознавать авторский стиль","Выбирать синтаксис под коммуникативную задачу"],"c1-unit-4"),
_u("C2",2,"Продвинутая аргументация",["rhetoric","ellipsis"],["rhetoric_c2","argumentation_c2"],["Строить сложную аргументацию","Управлять риторическим акцентом"],"c2-unit-1"),
_u("C2",3,"Критический анализ",["semantic-precision","cohesion-advanced"],["critical_c2","analysis_c2"],["Разбирать скрытые предпосылки","Точно интерпретировать сложный текст"],"c2-unit-2"),
_u("C2",4,"Точность и синтез",["stylistic-variation","synthesis"],["precision_c2","synthesis_c2"],["Синтезировать несколько позиций","Редактировать текст до высокого уровня точности"],"c2-unit-3")]
}
