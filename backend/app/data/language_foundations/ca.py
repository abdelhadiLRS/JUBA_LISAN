"""Catalan A1-C2 curriculum data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]
def _g(slug,title,level,summary,example):
    return GrammarTopic(slug=slug,title=title,level=level,category="grammar",summary=summary,explanation=f"Practice {title.lower()} in authentic Catalan contexts.",examples=[GrammarExample(text=example)])
GRAMMAR_TOPICS=[
_g("a1-pronouns","Personal pronouns","A1","Use subject pronouns in introductions.","Jo sóc estudiant."),
_g("a1-ser","Ser and identity","A1","Identify people, professions and origin.","Ella és professora."),
_g("a1-estar","Estar and location/state","A1","Describe location and temporary states.","Estic a casa."),
_g("a1-present","Present tense","A1","Talk about current and habitual actions.","Estudio català."),
_g("a1-questions","Question words","A1","Ask who, what, where and how.","On ets?"),
_g("a1-negation","Negation","A1","Form simple negative statements.","No treballo avui."),
_g("a1-gender","Gender and number","A1","Agree nouns and adjectives.","Una casa gran."),
_g("a1-articles","Articles and contractions","A1","Use definite and indefinite articles.","El llibre és a la taula."),
_g("a2-past","Periphrastic past","A2","Describe completed past events with anar + infinitive.","Ahir vaig estudiar."),
_g("a2-imperfect","Imperfect tense","A2","Describe habitual or background past actions.","Quan era petit, vivia aquí."),
_g("a2-future","Simple future and plans","A2","Talk about future events and intentions.","Demà estudiaré."),
_g("a2-pronouns-object","Weak object pronouns","A2","Use basic unstressed object pronouns.","El veig cada dia."),
_g("a2-prepositions","Prepositions and contractions","A2","Express place, time and relationships.","Vaig al mercat."),
_g("a2-comparison","Comparatives and superlatives","A2","Compare people and things.","Aquesta casa és més gran."),
_g("a2-reflexive","Reflexive verbs","A2","Describe routines and reflexive actions.","Em llevo a les set."),
_g("b1-subjunctive","Present subjunctive","B1","Express wishes, doubt and recommendations.","Espero que vinguis."),
_g("b1-conditional","Conditional mood","B1","Express hypotheses and polite requests.","Voldria parlar amb tu."),
_g("b1-relative","Relative clauses","B1","Identify people and things with subordinate clauses.","La noia que vaig veure és aquí."),
_g("b1-cause-purpose","Cause and purpose clauses","B1","Explain reasons and purposes.","Ho faig perquè t'ajudi."),
_g("b1-connectors","Discourse connectors","B1","Connect ideas coherently.","Per això, continuarem."),
_g("b1-reported","Reported speech","B1","Report statements and questions.","Va dir que vindria."),
_g("b1-imperative","Imperative and pronoun placement","B1","Give instructions and combine commands with pronouns.","Explica-m'ho, si us plau."),
_g("b1-periphrastic","Anar a + infinitive","B1","Express immediate future and plans.","Anem a començar."),
_g("b2-passive","Passive and se constructions","B2","Describe processes and impersonal events.","Es venen llibres."),
_g("b2-perfect","Perfect and pluperfect","B2","Relate prior events and experiences.","Ja havia acabat."),
_g("b2-concession","Concession and contrast","B2","Express opposition and concession.","Tot i que plou, sortirem."),
_g("b2-conditionals","Complex conditionals","B2","Handle real, hypothetical and counterfactual conditions.","Si tingués temps, hi aniria."),
_g("b2-nominalization","Nominalization","B2","Use abstract nouns in formal discourse.","La construcció del projecte continua."),
_g("b2-information","Topic, focus and clitic doubling","B2","Manage information structure and object reference.","A la Maria, li ho diré demà."),
_g("b2-modal","Periphrastic modality","B2","Express obligation, probability and necessity.","Cal que ho revisem."),
_g("c1-formal","Formal and institutional register","C1","Write appropriately for administration and institutions.","D'acord amb la resolució..."),
_g("c1-academic","Academic register and hedging","C1","Qualify claims and report evidence.","Es pot considerar que els resultats són significatius."),
_g("c1-argumentation","Argumentation and counterargument","C1","Build claims, evidence and rebuttals.","Tanmateix, les dades indiquen el contrari."),
_g("c1-embedded","Embedded questions","C1","Embed questions and propositions in complex syntax.","Cal determinar què ha passat."),
_g("c1-pragmatics","Pragmatics and politeness","C1","Adapt wording to audience and social context.","Si em permet, voldria precisar aquest punt."),
_g("c2-discourse","Discourse analysis and register shifting","C2","Analyse cohesion, stance and register.","El canvi de registre modifica la interpretació."),
_g("c2-rhetoric","Rhetorical and literary nuance","C2","Interpret irony, metaphor and persuasive structure.","La ironia transforma el sentit literal.")
]
_vocab=[
("greetings","A1",[("hola","greeting","Hola!"),("gràcies","thanks","Gràcies per l'ajuda.")]),
("identity","A1",[("nom","name","Em dic Anna."),("estudiant","student","Sóc estudiant.")]),
("family","A1",[("mare","mother","La meva mare és a casa."),("pare","father","El meu pare treballa.")]),
("home","A1",[("casa","house","La casa és gran."),("habitació","room","La meva habitació és aquí.")]),
("daily","A1",[("matí","morning","Al matí treballo."),("dormir","sleep","Vaig a dormir.")]),
("food","A1",[("aigua","water","Bec aigua."),("pa","bread","Compro pa.")]),
("places","A1",[("estació","station","On és l'estació?"),("botiga","shop","La botiga és aquí.")]),
("communication","A1",[("ajuda","help","Necessito ajuda."),("pregunta","question","Tinc una pregunta.")]),
("travel","A2",[("bitllet","ticket","Necessito un bitllet."),("tren","train","El tren surt ara.")]),
("health","A2",[("metge","doctor","Necessito un metge."),("medicament","medicine","Prenc el medicament.")]),
("study","B1",[("examen","exam","Demà tinc un examen."),("aprenentatge","learning","L'aprenentatge requereix pràctica.")]),
("work","B1",[("projecte","project","El projecte continua."),("reunió","meeting","La reunió comença a les deu.")]),
("society","B2",[("societat","society","La societat canvia."),("responsabilitat","responsibility","És una responsabilitat compartida.")]),
("economy","B2",[("economia","economy","L'economia creix."),("mercat","market","El mercat és competitiu.")]),
("media","C1",[("notícia","news","La notícia és important."),("font","source","La font és fiable.")]),
("academic","C1",[("recerca","research","La recerca continua."),("evidència","evidence","L'evidència dona suport a la hipòtesi.")]),
("culture","C2",[("patrimoni","heritage","El patrimoni cultural és valuós."),("tradició","tradition","La tradició es transmet.")]),
("discourse","C2",[("context","context","El significat depèn del context."),("matis","nuance","Aquest matís és important.")])
]
VOCABULARY_SETS=[VocabularySet(id=f"ca-vocab-{i+1}",level=l,topic=t,unit_ref=f"ca-{l.lower()}-unit-{(i%8)+1}",words=[VocabularyEntry(word=w,pos="word",definition=d,example=e) for w,d,e in ws]) for i,(t,l,ws) in enumerate(_vocab)]
_phr=[
("Greetings","A1","👋",[("Hola!","greeting"),("Bon dia!","morning greeting")]),
("Introductions","A1","👤",[("Em dic Anna.","introducing yourself"),("Com et dius?","asking a name")]),
("Courtesy","A1","🙏",[("Gràcies.","thanks"),("Si us plau.","please")]),
("Shopping","A1","🛒",[("Quant costa?","asking price"),("Vull això.","choosing an item")]),
("Directions","A1","🧭",[("On és l'estació?","asking location"),("Gira a la dreta.","giving directions")]),
("Daily life","A2","☀️",[("A quina hora?","asking time"),("Demà estudiaré.","future plan")]),
("Travel","A2","✈️",[("Necessito un bitllet.","buying a ticket"),("Quan surt el tren?","transport question")]),
("Health","A2","🩺",[("Necessito un metge.","asking for a doctor"),("No em trobo bé.","describing condition")]),
("Discussion","B1","💬",[("Jo crec que...","stating an opinion"),("Què en penses?","asking an opinion")]),
("Formal","B2","🏛️",[("D'acord amb la resolució...","formal reference"),("Cal tenir en compte...","formal consideration")]),
("Academic","C1","📚",[("Es pot considerar que...","academic hedging"),("Les dades indiquen...","reporting evidence")]),
("Rhetoric","C2","🎙️",[("Tanmateix, ...","contrast"),("En definitiva, ...","conclusion")])
]
PHRASEBOOK_CATEGORIES=[PhrasebookCategory(id=f"ca-phrase-{i+1}",level=l,situation=s,icon=ic,phrases=[PhrasebookEntry(text=t,context=c,register="formal" if l in ("C1","C2") else "neutral") for t,c in ps]) for i,(s,l,ic,ps) in enumerate(_phr)]
_titles={
"A1":["Salutacions i identitat","Família i casa","Vida quotidiana","Menjar i compres","Llocs i direccions","Comunicació","Descripcions","Repàs A1"],
"A2":["Passat perifràstic","Imperfet","Futur","Pronoms febles","Preposicions","Comparació","Verbs reflexius","Repàs A2"],
"B1":["Subjuntiu","Condicional","Relatives","Causa i finalitat","Connectors","Estil indirecte","Imperatiu i pronoms","Plans i perífrasis"],
"B2":["Passiva i se","Perfets","Concessió i contrast","Condicionals complexos","Nominalització","Informació i clítics","Modalitat","Argumentació"],
"C1":["Registre institucional","Llengua acadèmica","Argumentació i contraargument","Preguntes integrades","Pragmàtica i cortesia","Escriptura cohesionada","Anàlisi d'evidència","Síntesi C1"],
"C2":["Anàlisi del discurs","Retòrica","Canvi de registre","Estil literari","Ironia i implicatura","Precisió lèxica","Traducció","Síntesi C2"]
}
CURRICULUM={}
for level in LEVELS:
    gs=[g for g in GRAMMAR_TOPICS if g.level==level]
    vs=[v for v in VOCABULARY_SETS if v.level==level]
    CURRICULUM[level]=[CurriculumUnit(id=f"ca-{level.lower()}-unit-{i}",level=level,unit_number=i,title=title,grammar_points=[gs[i-1].title],vocabulary_set_ids=[vs[(i-1)%len(vs)].id],lesson_types=["grammar","vocabulary","listening","speaking","reading","writing","review"],competency_checklist=[f"Use Catalan for {title.lower()} at {level} level."],default_weeks=2 if level in ("A1","A2") else 3) for i,title in enumerate(_titles[level],1)]
_A=[
("vocabulary","A1","Which word means 'thanks'?","gràcies",["gràcies","hola","casa","aigua"]),
("grammar","A1","Which sentence uses ser correctly?","Jo sóc estudiant.",["Jo sóc estudiant.","Jo és estudiant.","Jo sóc estudiants.","Jo estudiant."]),
("grammar","A1","Which question asks where someone is?","On ets?",["On ets?","Què és això?","Com et dius?","Quant costa?"]),
("grammar","A1","Which sentence is negative?","No treballo avui.",["No treballo avui.","Treballo avui.","Treballava ahir.","Treballaré demà."]),
("vocabulary","A1","Which word means 'mother'?","mare",["mare","pare","amic","estació"]),
("communication","A1","Which phrase asks for help?","Em pots ajudar?",["Em pots ajudar?","Adéu!","Gràcies!","Bon dia!"]),
("grammar","A2","Which sentence describes a completed past event?","Ahir vaig estudiar.",["Ahir vaig estudiar.","Demà estudiaré.","Estudio ara.","Estic estudiant."]),
("grammar","B1","Which sentence uses the subjunctive?","Espero que vinguis.",["Espero que vinguis.","Vinc cada dia.","Vaig ahir.","Vindré demà."]),
("grammar","B1","Which sentence reports speech?","Va dir que vindria.",["Va dir que vindria.","Voldria venir.","Vine aquí.","He vingut."]),
("register","C1","Which phrase is formal?","D'acord amb la resolució...",["D'acord amb la resolució...","Hola!","Quant costa?","Em pots ajudar?"]),
("academic","C1","Which phrase hedges an academic claim?","Es pot considerar que els resultats són significatius.",["Es pot considerar que els resultats són significatius.","Hola!","Vull això.","Adéu!"]),
("translation","C2","Which word means 'nuance'?","matis",["matis","mercat","metge","tren"])
]
ASSESSMENT_BANK=[AssessmentQuestion(id=f"ca-{i+1:03}",skill=s,difficulty=l,question=q,options=o,correct=c) for i,(s,l,q,c,o) in enumerate(_A)]
