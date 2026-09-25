"""Afrikaans foundation data for JUBA LISAN."""

from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

LEVELS=["A1","A2","B1","B2","C1","C2"]

_GRAMMAR=[
("pronouns","Persoonlike voornaamwoorde","A1","syntax","Gebruik ek, jy, hy, sy, ons, julle en hulle in eenvoudige sinne.","Ek is Anna."),
("word-order","Basiese woordorde","A1","syntax","Bou eenvoudige hoofsinne met die werkwoord in die tweede posisie.","Ek woon in Kaapstad."),
("present-tense","Teenwoordige tyd","A1","verbs","Gebruik die eenvoudige teenwoordige tyd vir feite en roetines.","Ek werk vandag."),
("articles","Lidwoorde en naamwoorde","A1","nouns","Gebruik 'n en die in eenvoudige naamwoordfrases.","Dit is 'n huis."),
("negation","Dubbele negasie","A1","syntax","Afrikaans gebruik dikwels nie ... nie om 'n sin te ontken.","Ek verstaan nie."),
("questions","Vrae","A1","communication","Vorm ja/nee-vrae en vrae met wat, waar, wie en hoe.","Waar woon jy?"),
("possessives","Besitlike vorme","A1","grammar","Gebruik my, jou, sy, haar, ons en hulle om besit uit te druk.","Dit is my boek."),
("plurals","Meervoude","A1","nouns","Herken algemene meervoudsvorme met -e en -s.","Die kinders speel."),
("past-tense","Verlede tyd","A2","verbs","Gebruik het ... ge- vir algemene voltooide handelinge.","Ek het gister gewerk."),
("future","Toekomende tyd","A2","verbs","Gebruik sal plus die werkwoord vir planne en verwagtings.","Ek sal môre kom."),
("modal-verbs","Modale werkwoorde","A2","verbs","Gebruik kan, moet, wil en mag vir vermoë, verpligting en toestemming.","Ek moet nou gaan."),
("prepositions","Voorsetsels","A2","grammar","Gebruik algemene voorsetsels vir plek, tyd en beweging.","Ek gaan na die winkel."),
("comparatives","Vergelyking","A2","adjectives","Vergelyk dinge met meer, minder en as.","Hierdie boek is beter as daardie een."),
("reflexive-verbs","Refleksiewe werkwoorde","A2","verbs","Gebruik my, jou, hom, haar en ander refleksiewe vorme in roetines.","Ek was my hande."),
("subordinate-clauses","Bysinne","B1","syntax","Verbind idees met omdat, dat, wanneer, as en hoewel.","Ek bly tuis omdat dit reën."),
("relative-clauses","Betreklike sinne","B1","syntax","Beskryf mense en dinge met wat en ander betreklike konstruksies.","Die boek wat ek lees is interessant."),
("conditional","Voorwaardelike sinne","B1","verbs","Druk moontlike of hipotetiese situasies uit met as en sou.","As ek tyd het, sal ek kom."),
("reported-speech","Indirekte rede","B1","discourse","Rapporteer wat iemand gesê het sonder direkte aanhaling.","Hy sê dat hy môre kom."),
("perfect-imperfect","Voltooide en deurlopende verlede","B1","verbs","Kies verlede konstruksies volgens gebeurtenis en vertelling.","Toe ek aankom, het dit gereën."),
("connectors","Diskurskakelaars","B1","discourse","Verbind argumente met maar, daarom, tog, want en dus.","Ek was moeg, maar ek het aangehou."),
("passive","Passiewe vorm","B2","syntax","Fokus op die handeling of resultaat eerder as die handelende persoon.","Die brug word gebou."),
("causal-concessive","Oorsaak en toegewing","B2","syntax","Druk rede, gevolg, kontras en toegewing presies uit.","Alhoewel dit reën, gaan ons uit."),
("complex-relative","Komplekse betreklike sinne","B2","syntax","Beheer langer naamwoordfrases en ingebedde beskrywings.","Die verslag wat ek gister ontvang het is belangrik."),
("nominalization","Nominalisering","B2","style","Gebruik formele naamwoordkonstruksies om inligting bondig te organiseer.","Die implementering van die plan is belangrik."),
("formal-register","Formele register","B2","register","Pas woordkeuse en sinstruktuur by professionele en institusionele kommunikasie aan.","Ons versoek u om die vorm in te vul."),
("academic-hedging","Akademiese versigtigheid","C1","academic","Beperk stellings met waarskynlikheid en bewyse eerder as absolute aansprake.","Die resultate kan daarop dui dat ..."),
("embedded-questions","Ingebedde vrae","C1","syntax","Plaas 'n vraag binne 'n groter sin of versoek.","Ek weet nie wanneer die kursus begin nie."),
("information-structure","Inligtingstruktuur","C1","discourse","Gebruik fokus en tema om nuwe en bekende inligting duidelik te rangskik.","Veral hierdie punt is belangrik."),
("complex-subordination","Komplekse ondergeskiktheid","C1","syntax","Kombineer verskeie bysinne sonder om helderheid te verloor.","Hoewel die projek kompleks is, kan ons dit uitvoer."),
("administrative-style","Administratiewe styl","C1","professional","Gebruik presiese taal vir vorms, kennisgewings en institusionele dokumente.","Die aansoek moet teen Vrydag ingedien word."),
("idioms","Idiomatiese taal","C2","lexis","Gebruik en interpreteer idiome volgens konteks eerder as woord-vir-woord.","Dit is 'n druppel in die emmer."),
("register-shifting","Registerwisseling","C2","pragmatics","Skakel doelbewus tussen informele, professionele, akademiese en openbare style.","Kan u dit asseblief bevestig?"),
("rhetoric","Retoriek en argumentasie","C2","rhetoric","Bou genuanseerde argumente, toegewings en teenargumente.","Die argument is oortuigend, maar die bewyse is beperk."),
("literary-style","Literêre styl","C2","style","Herken beeldspraak, ritme en doelbewuste stylvariasie.","Die stad word stadig wakker onder die reën."),
("translation","Vertaalpresisie","C2","translation","Kies konteksgepaste Afrikaanse ekwivalente eerder as letterlike kalke.","Die formulering moet by die konteks pas.")
]

GRAMMAR_TOPICS=[GrammarTopic(slug=s,title=t,level=l,category=c,summary=sm,explanation=sm,examples=[GrammarExample(text=e)]) for s,t,l,c,sm,e in _GRAMMAR]

_VOCAB={
"A1":[("Groete","Hallo","phrase","hello","Hallo! Hoe gaan dit?"),("Identiteit","naam","noun","name","Wat is jou naam?"),("Familie","familie","noun","family","My familie woon hier."),("Huis","huis","noun","house","Ons huis is klein."),("Roetine","werk","verb","work","Ek werk elke dag."),("Tyd","oggend","noun","morning","Ek werk elke oggend."),("Kos","brood","noun","bread","Ek koop brood."),("Plekke","winkel","noun","shop","Die winkel is naby.")],
"A2":[("Reis","stasie","noun","station","Waar is die stasie?"),("Gesondheid","dokter","noun","doctor","Ek gaan dokter toe."),("Inkopies","prys","noun","price","Wat is die prys?"),("Weer","weer","noun","weather","Die weer is mooi.")],
"B1":[("Werk","ervaring","noun","experience","Ek het baie ervaring."),("Onderwys","kursus","noun","course","Die kursus begin môre."),("Samelewing","buurt","noun","neighbourhood","Ons buurt is stil."),("Opinies","mening","noun","opinion","Na my mening is dit belangrik.")],
"B2":[("Professioneel","data","noun","data","Die data word beskerm."),("Administrasie","aansoek","noun","application","Die aansoek is ingedien."),("Media","nuus","noun","news","Ek het die nuus gelees."),("Omgewing","omgewing","noun","environment","Ons moet die omgewing beskerm.")],
"C1":[("Akademies","bewyse","noun","evidence","Die bewyse is relevant."),("Analise","ontwikkeling","noun","development","Die ontwikkeling is betekenisvol."),("Bestuur","vereiste","noun","requirement","Dit is 'n belangrike vereiste."),("Argumentasie","gevolgtrekking","noun","conclusion","Die gevolgtrekking moet versigtig wees.")],
"C2":[("Retoriek","nuanse","noun","nuance","Die nuanse is belangrik."),("Pragmatiek","omstandighede","noun","circumstances","Die omstandighede moet oorweeg word."),("Literatuur","metafoor","noun","metaphor","Die metafoor is doelbewus."),("Vertaling","betekenis","noun","meaning","Die betekenis hang van die konteks af.")]
}
VOCABULARY_SETS=[]
for level,rows of Object.entries(_VOCAB)){
  rows.forEach((r,i)=>VOCABULARY_SETS.push(VocabularySet(id=`af-${level.toLowerCase()}-${i+1}`,level,topic:r[0],unit_ref:`af-${level.toLowerCase()}-unit-${i+1}`,words:[VocabularyEntry(word:r[1],pos:r[2],definition:r[3],example:r[4])]))
}

_UNITS={
"A1":["Bekendstelling","Familie en mense","Huis en roetine","Tyd en afsprake","Kos en inkopies","Plekke en rigtings","Vervoer en dienste","Alledaagse kommunikasie"],
"A2":["Verlede ervarings","Toekomsplanne","Vermoë en verpligting","Reis en beweging","Keuses vergelyk","Gesondheid en roetines"],
"B1":["Redes en verduidelikings","Mense en dinge beskryf","Hipotetiese situasies","Inligting rapporteer","Gebeurtenisse vertel","Menings verbind"],
"B2":["Prosesse en passief","Kontras en toegewing","Komplekse beskrywings","Formele prosesse","Professionele kommunikasie","Geïntegreerde taalgebruik"],
"C1":["Bewyse en aansprake","Ingebedde kommunikasie","Fokus en aanbieding","Komplekse argumente","Openbare administrasie","Gevorderde professionele skryfwerk"],
"C2":["Idiome en nuanse","Registerbeheer","Retoriese argumentasie","Literêre interpretasie","Vertaalkeuses","Meesterschap en sintese"]
}
CURRICULUM={}
for (const [level,titles] of Object.entries(_UNITS)){
  CURRICULUM[level]=titles.map((title,i)=>new CurriculumUnit({
    id:`af-${level.toLowerCase()}-unit-${i+1}`,level,unit_number:i+1,title:`Afrikaans ${level} · ${title}`,
    grammar_points:[_GRAMMAR[["A1","A2","B1","B2","C1","C2"].indexOf(level)*6+i][0]],
    vocabulary_set_ids:[`af-${level.toLowerCase()}-${Math.min(i+1,_VOCAB[level].length)}`],
    lesson_types:["grammar","vocabulary","reading","writing","listening","review"],
    competency_checklist:[`Communicate in Afrikaans about ${title.toLowerCase()}`,`Complete guided ${level} tasks accurately`],default_weeks:2
  }))
}

const PHRASES={
"A1":[["Groete","👋",["Hallo! Hoe gaan dit?","Goeie môre!","My naam is ..."]],["Inkopies","🛒",["Hoeveel kos dit?","Ek wil dit hê.","Kan ek met 'n kaart betaal?"]]],
"A2":[["Reis","🧳",["Waar is die stasie?","Een kaartjie, asseblief.","Hoe laat vertrek die trein?"]],["Gesondheid","🩺",["Ek voel nie goed nie.","Ek het 'n afspraak nodig.","Waar is die apteek?"]]],
"B1":[["Opinies","💭",["Na my mening ...","Ek stem saam.","Ek verstaan jou punt."]],["Werk","💼",["Kan ons dit saam bespreek?","Ek stuur die dokument vandag.","Wanneer is die vergadering?"]]],
"B2":[["Vergaderings","📅",["Kan ons hierdie punt verder bespreek?","Ek stel voor dat ons ...","Laat ons die opsies vergelyk."]],["Administrasie","🏛️",["Die aansoek word verwerk.","Kan u dit skriftelik bevestig?","Die dokument moet ingedien word."]]],
"C1":[["Akademies","🎓",["Die resultate dui daarop dat ...","Dit is belangrik om die data te interpreteer.","Die bewyse ondersteun hierdie gevolgtrekking."]],["Aanbiedings","📊",["Laat my hierdie punt beklemtoon.","Eerstens moet ons ...","Ten slotte kan ons sê dat ..."]]],
"C2":[["Debat","⚖️",["Hierdie interpretasie is moontlik, maar ...","Dit hang grootliks van die konteks af.","Ek wil 'n onderskeid tref tussen ..."]],["Literatuur","📚",["Hierdie formulering het 'n dubbele betekenis.","Die beeldspraak versterk die tema.","Die passage kan op verskillende maniere gelees word."]]]
}
PHRASEBOOK_CATEGORIES=[]
for (const [level,cats] of Object.entries(PHRASES)){
  cats.forEach((cat,i)=>PHRASEBOOK_CATEGORIES.push(new PhrasebookCategory({id:`af-${level.toLowerCase()}-phrases-${i+1}`,level,situation:cat[0],icon:cat[1],phrases:cat[2].map(text=>new PhrasebookEntry({text,context:cat[0],register:level==="A1"||level==="A2"?"neutral":"formal",unit_ref:`af-${level.toLowerCase()}-unit-${i+1}`}))})))
}

ASSESSMENT_BANK=[
new AssessmentQuestion({id:"af-a1-001",skill:"grammar",difficulty:"A1",question:"Choose the correct sentence.",options:["Ek is 'n student.","Ek 'n student is.","Ek is student 'n.","Is ek student 'n."],correct:"Ek is 'n student.",grammar_slug:"word-order"}),
new AssessmentQuestion({id:"af-a1-002",skill:"grammar",difficulty:"A1",question:"Which sentence uses Afrikaans double negation?",options:["Ek verstaan nie.","Ek verstaan nie nie.","Ek nie verstaan nie.","Nie ek verstaan."],correct:"Ek verstaan nie nie.",grammar_slug:"negation"}),
new AssessmentQuestion({id:"af-a2-001",skill:"grammar",difficulty:"A2",question:"Which sentence refers to tomorrow?",options:["Ek sal môre kom.","Ek het gister gekom.","Ek kom gister.","Ek sou gister kom."],correct:"Ek sal môre kom.",grammar_slug:"future"}),
new AssessmentQuestion({id:"af-a2-002",skill:"vocabulary",difficulty:"A2",question:"Which word means doctor?",options:["dokter","stasie","prys","weer"],correct:"dokter"}),
new AssessmentQuestion({id:"af-b1-001",skill:"grammar",difficulty:"B1",question:"Which sentence gives a reason?",options:["Ek bly tuis omdat dit reën.","Ek bly tuis maar dit reën.","Ek bly tuis of dit reën.","Ek bly tuis daarom dit reën."],correct:"Ek bly tuis omdat dit reën.",grammar_slug:"subordinate-clauses"}),
new AssessmentQuestion({id:"af-b1-002",skill:"grammar",difficulty:"B1",question:"Which sentence is conditional?",options:["As ek tyd het, sal ek kom.","Ek kom elke dag.","Ek het gekom.","Ek sal nou gaan."],correct:"As ek tyd het, sal ek kom.",grammar_slug:"conditional"}),
new AssessmentQuestion({id:"af-b2-001",skill:"grammar",difficulty:"B2",question:"Which sentence is passive?",options:["Die brug word gebou.","Hulle bou die brug.","Hulle het die brug gebou.","Die brug is groot."],correct:"Die brug word gebou.",grammar_slug:"passive"}),
new AssessmentQuestion({id:"af-b2-002",skill:"communication",difficulty:"B2",question:"Which phrase is formal?",options:["Ons versoek u om die vorm in te vul.","Gee my die vorm.","Stuur dit nou.","Hey, stuur dit."],correct:"Ons versoek u om die vorm in te vul.",grammar_slug:"formal-register"}),
new AssessmentQuestion({id:"af-c1-001",skill:"grammar",difficulty:"C1",question:"Which sentence contains an embedded question?",options:["Ek weet nie wanneer die kursus begin nie.","Wanneer begin die kursus?","Die kursus begin môre.","Ek wil die kursus."],correct:"Ek weet nie wanneer die kursus begin nie.",grammar_slug:"embedded-questions"}),
new AssessmentQuestion({id:"af-c1-002",skill:"reading",difficulty:"C1",question:"Which expression appropriately qualifies an academic claim?",options:["Die resultate kan daarop dui dat ...","Die resultate is altyd reg.","Die resultate bewys alles.","Die resultate is seker vir almal."],correct:"Die resultate kan daarop dui dat ...",grammar_slug:"academic-hedging"}),
new AssessmentQuestion({id:"af-c2-001",skill:"grammar",difficulty:"C2",question:"Which phrase introduces a qualified counterargument?",options:["Hierdie interpretasie is moontlik, maar ...","Dit is net verkeerd.","Ek weet niks nie.","Dit maak nie saak nie."],correct:"Hierdie interpretasie is moontlik, maar ...",grammar_slug:"rhetoric"}),
new AssessmentQuestion({id:"af-c2-002",skill:"reading",difficulty:"C2",question:"What is central to advanced translation?",options:["Context-sensitive equivalents","Literal word-for-word translation","Ignoring context","One synonym everywhere"],correct:"Context-sensitive equivalents",grammar_slug:"translation"})
]
