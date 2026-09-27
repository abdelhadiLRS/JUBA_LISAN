"""Curated Serbian A2-C2 lesson seeds for JUBA LISAN."""
from __future__ import annotations
from app.data.language_foundations.sr import CURRICULUM

_SKILLS=("grammar","vocabulary","reading","listening","speaking","writing","review")
_LEVEL_EXAMPLES={
"A2":["Јуче сам посетио музеј и разговарао са пријатељем.","Сутра ћу путовати и понећу карту са собом."],
"B1":["Кад бих имао више времена, истражио бих и друге могућности.","Читао сам извештај, а затим сам прочитао закључак."],
"B2":["Иако је предлог занимљив, треба размотрити његове последице.","Рекао је да ће резултати бити објављени након провере."],
"C1":["На основу доступних података може се закључити да је потребна додатна анализа.","У складу са прописима, документација мора бити достављена у року."],
"C2":["Спровођење предложених мера захтева пажљиво тумачење међусобно повезаних фактора.","Израз треба разумети у контексту, јер његово значење није увек дословно."],
}
_LEVEL_WORDS={
"A2":[("искуство","experience","То је било корисно искуство."),("путовање","journey","Путовање је трајало три дана."),("планирати","to plan","Планирам путовање.")],
"B1":[("одговорност","responsibility","То је велика одговорност."),("могућност","possibility","Имамо још једну могућност."),("истраживање","research","Истраживање је завршено.")],
"B2":[("последица","consequence","Морамо проценити последице."),("тврдња","claim","Тврдња захтева доказе."),("аргумент","argument","Ово је снажан аргумент.")],
"C1":[("претпоставка","assumption","Претпоставка се мора проверити."),("налаз","finding","Главни налаз је значајан."),("методологија","methodology","Методологија је описана у раду.")],
"C2":[("недвосмислен","unambiguous","Доказ није недвосмислен."),("имплицитно","implicitly","То је имплицитно наведено."),("нијанса","nuance","Важна је семантичка нијанса.")],
}
def _unit(unit_id, level):
    for unit in CURRICULUM.get(level, []):
        if unit.id==unit_id: return unit
    return None
def get_lesson_seed(level:str, unit_id:str, lesson_type:str)->dict|None:
    level=str(level).upper(); skill=str(lesson_type).lower(); unit=_unit(unit_id,level)
    if unit is None or skill not in _SKILLS: return None
    examples=_LEVEL_EXAMPLES[level]; words=_LEVEL_WORDS[level]; title=unit.title
    base={"title":title,"objective":f"Развијте знање српског језика на нивоу {level} кроз тему „{title}“.","unit_id":unit_id,"source":"curated_serbian","words":words,"vocabulary_words":[w[0] for w in words],"grammar":list(unit.grammar_points),"examples":examples}
    if skill=="grammar": base["objective"]=f"Употребите граматичке структуре за тему „{title}“."; base["examples"]=examples
    elif skill=="vocabulary": base["objective"]="Усвојите кључни речник и употребите га у контексту."
    elif skill=="reading": base.update(text=" ".join(examples),questions=["Која је главна тема текста?","Које две информације подржавају главну идеју?","Објасните један израз својим речима."])
    elif skill=="listening": base.update(transcript=" ".join(examples),questions=["Која је главна порука?","Које кључне речи чујете?","Који детаљ потврђује главну идеју?"])
    elif skill=="speaking": base.update(prompt=f"Говорите о теми „{title}“ и употребите најмање три речи из лекције.",phrases=examples,examples=examples[:2])
    elif skill=="writing": base.update(prompt=f"Напишите повезан текст о теми „{title}“.","guidance":["Употребите најмање три речи из лекције.","Укључите најмање једну циљну граматичку структуру.","Повежите идеје јасним реченицама."],examples=examples[:2])
    else: base["questions"]=["Објасните једну циљну граматичку структуру.","Напишите две реченице са новим речима.","Сажмите тему лекције својим речима."]
    return base
