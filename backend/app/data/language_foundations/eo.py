"""Esperanto foundation data for JUBA LISAN, CEFR A1-C2."""
from app.data._types import (
    CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet,
    PhrasebookCategory, PhrasebookEntry, AssessmentQuestion,
)

LEVELS=["A1","A2","B1","B2","C1","C2"]

_GRAMMAR=[
("pronouns","Personal pronouns and accusative","A1","Mi vidas ŝin.","Use -n for direct objects."),
("present","Present tense -as","A1","Mi lernas Esperanton.","Present verbs use -as."),
("plural","Plural -j and accusative -n","A1","La libroj estas novaj.","Combine plural and object marking."),
("questions","Ĉu and question words","A1","Ĉu vi komprenas?","Use ĉu for yes/no questions."),
("negation","Negation with ne","A1","Mi ne scias.","Place ne before the negated predicate."),
("possessives","Possessive adjectives","A1","Tio estas mia libro.","Possessives agree with number and accusative."),
("past","Past tense -is","A2","Mi legis hieraŭ.","Use -is for completed past events."),
("future","Future tense -os","A2","Mi venos morgaŭ.","Use -os for future events."),
("imperative","Volitive -u","A2","Venu kun mi.","Use -u for commands, wishes and exhortations."),
("adjectives","Adjective agreement -a","A2","La domoj estas grandaj.","Adjectives agree in plural and accusative."),
("comparison","Comparatives and superlatives","A2","Ŝi estas pli alta.","Use pli, plej and ol."),
("correlatives","Correlative table words","A2","Kie vi loĝas?","Use ki-, ti-, i-, ĉi- and neni- forms."),
("perfect","Participles and compound tenses","B1","Mi jam estas fininta.","Use participles with esti for compound meaning."),
("conditional","Conditional -us","B1","Mi irus, se mi povus.","Use -us for hypothetical situations."),
("relative","Relative clauses with kiu/kio","B1","La libro, kiun mi legis...","Mark the role of the relative pronoun."),
("reported","Reported speech","B1","Li diris, ke li venos.","Use ke and embedded clauses."),
("passive","Passive voice","B1","La libro estas legata.","Use esti plus passive participle."),
("word-formation","Affixes and productive derivation","B1","malgranda, samideano","Use Esperanto affixes systematically."),
("aspect","Participles for ongoing and completed action","B2","Ŝi estis leganta.","Choose participles according to event phase."),
("subordination","Complex subordinate clauses","B2","Kvankam li venis, ...","Link clauses precisely with conjunctions."),
("nominalization","Derivation and nominal style","B2","La decido estis grava.","Use -o and derivational morphology accurately."),
("discourse","Connectors and discourse structure","B2","Tamen, la rezulto...","Organise contrast, cause and consequence."),
("modality","Modal and evidential nuance","B2","Ŝajne li pravis.","Express certainty, inference and obligation."),
("formal","Formal and institutional Esperanto","C1","La kunsido estas malfermita.","Adapt syntax and vocabulary to institutions."),
("academic","Academic hedging","C1","La rezultoj ŝajnas indiki...","Qualify claims and distinguish evidence from inference."),
("information","Topic, focus and emphasis","C1","Precipe ĉi tiu punkto...","Control information structure."),
("embedded","Embedded questions and complements","C1","Mi ne scias, ĉu...","Integrate questions into complex sentences."),
("pragmatics","Politeness and pragmatic meaning","C2","Ĉu vi bonvolus...","Choose forms according to social context."),
("rhetoric","Rhetorical argumentation","C2","Unuflanke... aliflanke...","Build balanced persuasive discourse."),
("literary","Literary and idiomatic style","C2","La urbo vekiĝis.","Interpret figurative language."),
("translation","Translation precision and paraphrase","C2","Alivorte, ...","Choose precise equivalents across registers."),
("subjunctive-style","Volaj kaj deziraj nuancoj","C1","Mi volus, ke la plano sukcesu.","Express wishes, preferences and hypothetical attitudes precisely."),
("register-shift","Registro kaj ĝenro","C1","La tono dependas de la publiko.","Adapt vocabulary and syntax to genre and audience."),
("cohesion","Kohero kaj referenco","C2","Tio ĉi rilatas al la antaŭa argumento.","Maintain cohesion and explicit reference across long texts."),
("discourse-analysis","Diskursa analizo","C2","La elekto de vortoj montras la pozicion de la aŭtoro.","Analyse stance, cohesion, rhetoric and discourse structure.")
]
GRAMMAR_TOPICS=[GrammarTopic(slug=s,title=t,level=l,category=c,summary=t,explanation=x,examples=[GrammarExample(text=e)]) for s,t,l,c,e,x in _GRAMMAR]

_VOCAB=[
("A1","Greetings",["saluton","dankon","bonvolu","ĝis"]),
("A1","Identity",["nomo","studento","amiko","lingvo"]),
("A1","Family",["patrino","patro","frato","fratino"]),
("A1","Home",["domo","ĉambro","pordo","tablo"]),
("A1","Routine",["mateno","labori","manĝi","dormi"]),
("A1","Food",["pano","lakto","pomo","akvo"]),
("A1","Places",["butiko","lernejo","stacidomo","strato"]),
("A1","Communication",["kompreni","demando","helpo","rapide"]),
("A2","Travel",["vojaĝo","bileto","aŭtobuso","hotelo"]),
("A2","Health",["sano","kuracisto","doloro","medikamento"]),
("A2","Plans",["plano","bezono","povi","devi"]),
("A2","Shopping",["prezo","pagi","mono","ricevo"]),
("B1","Education",["studado","ekzameno","esploro","scio"]),
("B1","Work",["kunveno","kolego","projekto","sperto"]),
("B1","Society",["komunumo","medio","leĝo","rajto"]),
("B1","Opinions",["opinio","kialo","pruvo","argumento"]),
("B2","Media",["novaĵo","fonto","datumaro","teknologio"]),
("B2","Economy",["ekonomio","investo","entrepreno","merkato"]),
("B2","Culture",["kulturo","heredaĵo","tradicio","literaturo"]),
("B2","Environment",["poluo","rimedo","energio","daŭripovo"]),
("C1","Academic",["hipotezo","metodologio","konkludo","interpreto"]),
("C1","Administration",["politiko","regularo","proceduro","aplikaĵo"]),
("C1","Professional",["raporto","propono","intertraktado","interkonsento"]),
("C1","Analysis",["kritiko","antaŭjuĝo","perspektivo","kontrasto"]),
("C2","Rhetoric",["retoriko","persvado","emfazo","koncedo"]),
("C2","Nuance",["nuanco","metaforo","ironio","idiomo"]),
("C2","Literature",["rakonto","simbolo","stilo","tono"]),
("C2","Translation",["signifo","ekvivalento","parafrazo","precizeco"]),
]
VOCABULARY_SETS=[]
for idx,(level,topic,words) in enumerate(_VOCAB,1):
    level_idx=["A1","A2","B1","B2","C1","C2"].index(level)
    unit=(idx-1)%4+1
    vid=f"eo-{level.lower()}-{unit}"
    entries=[VocabularyEntry(word=w,pos="noun" if w.endswith(("o","aĵo")) else "verb" if w.endswith("i") else "phrase",definition=w,example=f"Ekzemplo kun {w}.") for w in words]
    VOCABULARY_SETS.append(VocabularySet(id=vid,level=level,topic=topic,unit_ref=f"eo-{level.lower()}-unit-{unit}",words=entries))

_CURRICULUM_TOPICS={
"A1":["Salutoj kaj identeco","Familio kaj hejmo","Ĉiutaga vivo","Tempo kaj rendevuoj","Manĝaĵoj kaj aĉetado","Lokoj kaj direktoj","Distro kaj ŝatokupoj","Ĉiutaga komunikado"],
"A2":["Vojaĝado","Sano","Plano kaj devo","Servoj","Pasintaj eventoj","Komparoj","Laboro kaj studado","Problemoj kaj solvoj"],
"B1":["Eduko","Laboro","Socio","Opinioj","Informo kaj raportado","Kondiĉoj","Rilatoj kaj kunlaboro","Medio kaj komunumo"],
"B2":["Amaskomunikiloj","Ekonomio","Kulturo","Medio","Formala klarigo","Argumentado","Teknologio","Publika diskuto"],
"C1":["Akademia diskurso","Publika administrado","Profesia komunikado","Kritika analizo","Evidenco","Formala verkado","Deziroj kaj nuancoj","Registro kaj ĝenro"],
"C2":["Retoriko","Pragmatiko","Literatura stilo","Tradukado","Diskursa analizo","Altnivela stilo","Kohero kaj referenco","Altnivela diskursa analizo"],
}
CURRICULUM={}
for level,titles in _CURRICULUM_TOPICS.items():
    CURRICULUM[level]=[
        CurriculumUnit(id=f"eo-{level.lower()}-unit-{n}",level=level,unit_number=n,title=f"Esperanto {level} · {title}",
        grammar_points=[x[0] for x in _GRAMMAR if x[2]==level][:2],
        vocabulary_set_ids=[f"eo-{level.lower()}-{(n-1)%4+1}"],
        lesson_types=["grammar","vocabulary","reading","writing","listening","review"],
        competency_checklist=[f"Communicate in Esperanto about {title.lower()} at {level} level","Apply Esperanto morphology and syntax accurately"],default_weeks=2)
        for n,title in enumerate(titles,1)
    ]

_PHRASES=[
("A1","Greetings",["Saluton!","Kiel vi fartas?","Mia nomo estas Ana."]),
("A1","Help",["Ĉu vi povas helpi min?","Mi ne komprenas.","Bonvolu paroli pli malrapide."]),
("A2","Travel",["Kie estas la stacidomo?","Kiom kostas bileto?","Je kioma horo ni foriros?"]),
("A2","Shopping",["Kiom kostas ĉi tio?","Mi ŝatus aĉeti ĝin.","Ĉu mi povas pagi per karto?"]),
("B1","Work",["Ĉu ni povas komenci la kunvenon?","Kio estas via opinio?","Mi konsentas kun tiu punkto."]),
("B1","Clarification",["Ĉu vi povas klarigi?","Kion vi volas diri?","Lasu min precizigi."]),
("B2","Formal",["Laŭ la disponeblaj fontoj...","Aliflanke...","Tamen, restas problemo."]),
("B2","Professional",["Mi alkroĉas la dokumenton.","Mi atendas vian respondon.","Ni devas konsideri ĉi tiun faktoron."]),
("C1","Academic",["La evidenteco sugestas, ke...","Oni povus argumenti, ke...","Tiu konkludo postulas plian esploron."]),
("C1","Administration",["Laŭ la regularo...","La aplikaĵo estis ricevita.","Bonvolu sekvi la proceduron."]),
("C2","Debate",["Ĉi-rilate...","Tiu argumento preterlasas la fakton, ke...","Indas rimarki, ke..."]),
("C2","Nuance",["La signifo dependas de la kunteksto.","Estas subtila diferenco inter tiuj terminoj.","Ĝenerale, sed ne sen esceptoj."]),
]
PHRASEBOOK_CATEGORIES=[PhrasebookCategory(id=f"eo-{l.lower()}-phrase-{n}",level=l,situation=s,icon="💬",phrases=[PhrasebookEntry(text=p,context=s.lower(),register="formal" if l in ("C1","C2") else "neutral") for p in ps]) for n,(l,s,ps) in enumerate(_PHRASES,1)]

_ASSESS=[
("A1","grammar","Which suffix marks a direct object?","-n","pronouns"),
("A1","vocabulary","Which word means thank you?","dankon","identity"),
("A2","grammar","Which ending marks the future?","-os","future"),
("A2","vocabulary","Which word means ticket?","bileto","travel"),
("B1","grammar","Which ending marks the conditional?","-us","conditional"),
("B1","vocabulary","Which word means evidence?","pruvo","reported"),
("B2","grammar","Which form can express passive voice?","estas legata","passive"),
("B2","vocabulary","Which word means sustainability?","daŭripovo","discourse"),
("C1","grammar","Which expression hedges an academic claim?","ŝajnas indiki","academic"),
("C1","vocabulary","Which word means methodology?","metodologio","formal"),
("C2","grammar","Which area concerns social-context adaptation?","pragmatiko","pragmatics"),
("C2","vocabulary","Which word means nuance?","nuanco","literary"),
]
ASSESSMENT_BANK=[AssessmentQuestion(id=f"eo-{l.lower()}-{n:03}",skill="grammar" if skill=="grammar" else "vocabulary",difficulty=l,question=q,options=[correct,"A","B","C"],correct=correct,grammar_slug=slug) for n,(l,skill,q,correct,slug) in enumerate(_ASSESS,1)]
