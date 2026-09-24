"""Finnish assessment bank with balanced CEFR coverage."""
from app.data._types import AssessmentQuestion
def _q(i,level,skill,q,options,correct,slug=None):
    return AssessmentQuestion(id=f"fi-{level.lower()}-{i:03}",skill=skill,difficulty=level,question=q,options=options,correct=correct,grammar_slug=slug)
ASSESSMENT_BANK=[
_q(1,"A1","grammar","Which sentence correctly says “I speak Finnish”?",["Puhun suomea.","Puhua suomea.","Puhuin suomea.","Puhut suomea."],"Puhun suomea.","present-tense"),
_q(2,"A1","grammar","Choose the correct negative sentence.",["En ymmärrä.","Ei ymmärrän.","En ymmärtää.","Minä ei ymmärrä."],"En ymmärrä.","negation"),
_q(3,"A1","vocabulary","Which word means “water”?",["vesi","leipä","asema","huone"],"vesi"),
_q(4,"A1","grammar","How do you ask “Where do you live?”",["Missä asut?","Missä asutko?","Asut missä?","Missä sinä asua?"],"Missä asut?","questions"),
_q(1,"A2","grammar","Which sentence correctly expresses a completed past action?",["Eilen kävin Helsingissä.","Eilen käyn Helsingissä.","Eilen käydä Helsingissä.","Eilen käynyt Helsingissä."],"Eilen kävin Helsingissä.","past-tense"),
_q(2,"A2","grammar","Choose the natural total-object sentence.",["Luen kirjan.","Luen kirjaa loppuun.","Luen kirja.","Luen kirjassa."],"Luen kirjan.","object-cases"),
_q(3,"A2","vocabulary","What does “matkalippu” mean?",["travel ticket","passport","hotel","appointment"],"travel ticket"),
_q(4,"A2","grammar","Choose the correct imperative.",["Tule tänne!","Tulla tänne!","Tulevat tänne!","Tulen tänne!"],"Tule tänne!","imperative"),
_q(1,"B1","grammar","Which sentence correctly uses a relative clause?",["Tämä on kirja, jonka ostin.","Tämä on kirja, jonka ostaa.","Tämä on kirja, joka ostin sen.","Tämä on kirja, missä ostin."],"Tämä on kirja, jonka ostin.","relative-clauses"),
_q(2,"B1","grammar","Choose the Finnish passive form for a general statement.",["Suomessa puhutaan suomea.","Suomessa puhuvat suomea.","Suomessa puhun suomea.","Suomessa puhua suomea."],"Suomessa puhutaan suomea.","passive"),
_q(3,"B1","vocabulary","Which word means “deadline”?",["määräaika","palaute","tausta","ystävyyys"],"määräaika"),
_q(4,"B1","reading","Read: “Vaikka satoi, menimme ulos.” What happened?",["They went outside despite the rain.","They stayed home because it rained.","They went outside before the rain.","They stopped the rain."],"They went outside despite the rain.","subordinate-clauses"),
_q(1,"B2","grammar","Which sentence expresses concession correctly?",["Vaikka tehtävä oli vaikea, hän onnistui.","Vaikka tehtävä oli vaikea, hän onnistua.","Vaikka tehtävä vaikea, hän onnistui.","Vaikka tehtävä on vaikea, hän onnistunut."],"Vaikka tehtävä oli vaikea, hän onnistui.","concessive-clauses"),
_q(2,"B2","grammar","Choose the natural verb-government construction for “I like music.”",["Pidän musiikista.","Pidän musiikin.","Pidän musiikkia.","Pidän musiikissa."],"Pidän musiikista.","verb-government"),
_q(3,"B2","vocabulary","Which word means “conclusion”?",["johtopäätös","vastaväite","kustannus","perinne"],"johtopäätös"),
_q(4,"B2","reading","Read: “Sateen vuoksi tapahtuma siirrettiin.” Why was the event postponed?",["Because of rain.","Because of traffic.","Because of cost.","Because of illness."],"Because of rain.","causality"),
_q(1,"C1","grammar","Which sentence appropriately hedges a research claim?",["Tulokset saattavat johtua mittausmenetelmästä.","Tulokset johtua mittausmenetelmästä.","Tulokset ovat johtuen mittausmenetelmästä.","Tulokset saattaa johtua mittausmenetelmästä."],"Tulokset saattavat johtua mittausmenetelmästä.","hedging"),
_q(2,"C1","grammar","Which is a formal request?",["Voisitteko tarkentaa tätä kohtaa?","Tarkenna tätä nyt!","Voit tarkentaa tätä?","Tarkentaa tätä kohtaa."],"Voisitteko tarkentaa tätä kohtaa?","politeness"),
_q(3,"C1","vocabulary","Which word means “stakeholder”?",["sidosryhmä","esityslista","otanta","painotus"],"sidosryhmä"),
_q(4,"C1","reading","Read: “Tulokset viittaavat siihen, että menetelmä toimii.” What is the writer's stance?",["The results suggest the method works.","The method is certainly impossible.","No results were collected.","The method was never tested."],"The results suggest the method works.","academic-register"),
_q(1,"C2","grammar","Which sentence most clearly qualifies a claim?",["Tämä ei välttämättä tarkoita, että tulos on väärä.","Tämä tarkoittaa aina, että tulos on väärä.","Tämä tarkoittamaan tulos väärä.","Tämä ei tarkoittaa tulosta väärä."],"Tämä ei välttämättä tarkoita, että tulos on väärä.","semantic-precision"),
_q(2,"C2","grammar","Choose the correct counterfactual.",["Jos olisin tiennyt, olisin toiminut toisin.","Jos tiesin, toiminut toisin.","Jos olisin tiedän, toimin toisin.","Jos tiesin, olisin toimia toisin."],"Jos olisin tiennyt, olisin toiminut toisin.","advanced-conditionals"),
_q(3,"C2","vocabulary","Which term means “causality”?",["kausaalisuus","korrelaatio","viitekehys","vivahde"],"kausaalisuus"),
_q(4,"C2","reading","Read: “Korrelaatio ei yksin osoita kausaalisuutta.” What does the sentence say?",["Correlation alone does not prove causality.","Correlation always proves causality.","Causality and correlation are identical.","There is no correlation."],"Correlation alone does not prove causality.","technical-register"),
]