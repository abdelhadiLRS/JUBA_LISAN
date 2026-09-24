"""Finnish assessment bank with balanced CEFR coverage."""
from app.data._types import AssessmentQuestion

def _q(i,level,skill,q,options,correct,slug=None):
    return AssessmentQuestion(id=f"fi-{level.lower()}-{i:03}",skill=skill,difficulty=level,question=q,options=options,correct=correct,grammar_slug=slug)

ASSESSMENT_BANK=[
_q(1,"A1","grammar","Mikä lause tarkoittaa, että puhun suomea?",["Puhun suomea.","Puhua suomea.","Puhuin suomea.","Puhut suomea."],"Puhun suomea.","present-tense"),
_q(2,"A1","grammar","Valitse oikea kielteinen lause.",["En ymmärrä.","Ei ymmärrän.","En ymmärtää.","Minä ei ymmärrä."],"En ymmärrä.","negation"),
_q(3,"A1","vocabulary","Mikä sana tarkoittaa juotavaa vettä?",["vesi","leipä","asema","huone"],"vesi"),
_q(4,"A1","grammar","Miten kysyt toiselta, missä hän asuu?",["Missä asut?","Missä asutko?","Asut missä?","Missä sinä asua?"],"Missä asut?","questions"),

_q(1,"A2","grammar","Mikä lause ilmaisee päättyneen menneen tapahtuman?",["Eilen kävin Helsingissä.","Eilen käyn Helsingissä.","Eilen käydä Helsingissä.","Eilen käynyt Helsingissä."],"Eilen kävin Helsingissä.","past-tense"),
_q(2,"A2","grammar","Valitse luonnollinen kokonaisobjektin käyttö.",["Luen kirjan.","Luen kirjaa loppuun.","Luen kirja.","Luen kirjassa."],"Luen kirjan.","object-cases"),
_q(3,"A2","vocabulary","Mikä on matkalippu?",["lippu, jolla voi matkustaa","henkilöllisyystodistus","hotellihuone","varattu tapaaminen"],"lippu, jolla voi matkustaa"),
_q(4,"A2","grammar","Valitse oikea käskymuoto.",["Tule tänne!","Tulla tänne!","Tulevat tänne!","Tulen tänne!"],"Tule tänne!","imperative"),

_q(1,"B1","grammar","Mikä lause käyttää relatiivilausetta oikein?",["Tämä on kirja, jonka ostin.","Tämä on kirja, jonka ostaa.","Tämä on kirja, joka ostin sen.","Tämä on kirja, missä ostin."],"Tämä on kirja, jonka ostin.","relative-clauses"),
_q(2,"B1","grammar","Valitse yleistä tapahtumaa ilmaiseva passiivilause.",["Suomessa puhutaan suomea.","Suomessa puhuvat suomea.","Suomessa puhun suomea.","Suomessa puhua suomea."],"Suomessa puhutaan suomea.","passive"),
_q(3,"B1","vocabulary","Mikä sana tarkoittaa aikaa, johon mennessä tehtävä pitää tehdä?",["määräaika","palaute","tausta","ystävällisyys"],"määräaika"),
_q(4,"B1","reading","Lue: ”Vaikka satoi, menimme ulos.” Mitä tapahtui?",["He menivät ulos sateesta huolimatta.","He jäivät kotiin sateen takia.","He menivät ulos ennen sadetta.","He lopettivat sateen."],"He menivät ulos sateesta huolimatta.","subordinate-clauses"),

_q(1,"B2","grammar","Mikä lause ilmaisee myönnytystä oikein?",["Vaikka tehtävä oli vaikea, hän onnistui.","Vaikka tehtävä oli vaikea, hän onnistua.","Vaikka tehtävä vaikea, hän onnistui.","Vaikka tehtävä on vaikea, hän onnistunut."],"Vaikka tehtävä oli vaikea, hän onnistui.","concessive-clauses"),
_q(2,"B2","grammar","Valitse oikea verbin rektiota noudattava lause.",["Pidän musiikista.","Pidän musiikin.","Pidän musiikkia.","Pidän musiikissa."],"Pidän musiikista.","verb-government"),
_q(3,"B2","vocabulary","Mikä tarkoittaa päätelmää, joka tehdään perustelujen jälkeen?",["johtopäätös","vastaväite","kustannus","perinne"],"johtopäätös"),
_q(4,"B2","reading","Lue: ”Sateen vuoksi tapahtuma siirrettiin.” Miksi tapahtuma siirrettiin?",["Sateen vuoksi.","Liikenteen vuoksi.","Kustannusten vuoksi.","Sairauden vuoksi."],"Sateen vuoksi.","causality"),

_q(1,"C1","grammar","Mikä lause ilmaisee tutkimustuloksen varovaisesti?",["Tulokset saattavat johtua mittausmenetelmästä.","Tulokset johtua mittausmenetelmästä.","Tulokset ovat johtuen mittausmenetelmästä.","Tulokset saattaa johtua mittausmenetelmästä."],"Tulokset saattavat johtua mittausmenetelmästä.","hedging"),
_q(2,"C1","grammar","Mikä on muodollinen pyyntö?",["Voisitteko tarkentaa tätä kohtaa?","Tarkenna tätä nyt!","Voit tarkentaa tätä?","Tarkentaa tätä kohtaa."],"Voisitteko tarkentaa tätä kohtaa?","politeness"),
_q(3,"C1","vocabulary","Mikä sana tarkoittaa tahoa tai ryhmää, johon päätös vaikuttaa?",["sidosryhmä","esityslista","otanta","painotus"],"sidosryhmä"),
_q(4,"C1","reading","Lue: ”Tulokset viittaavat siihen, että menetelmä toimii.” Mitä kirjoittaja sanoo?",["Tulokset viittaavat menetelmän toimivuuteen.","Menetelmä on varmasti mahdoton.","Tuloksia ei kerätty.","Menetelmää ei koskaan testattu."],"Tulokset viittaavat menetelmän toimivuuteen.","academic-register"),

_q(1,"C2","grammar","Mikä lause rajaa väitettä semanttisesti tarkasti?",["Tämä ei välttämättä tarkoita, että tulos on väärä.","Tämä tarkoittaa aina, että tulos on väärä.","Tämä tarkoittamaan tulos väärä.","Tämä ei tarkoittaa tulosta väärä."],"Tämä ei välttämättä tarkoita, että tulos on väärä.","semantic-precision"),
_q(2,"C2","grammar","Valitse oikea vastakonditionaali.",["Jos olisin tiennyt, olisin toiminut toisin.","Jos tiesin, toiminut toisin.","Jos olisin tiedän, toimin toisin.","Jos tiesin, olisin toimia toisin."],"Jos olisin tiennyt, olisin toiminut toisin.","advanced-conditionals"),
_q(3,"C2","vocabulary","Mikä termi tarkoittaa syy-yhteyttä?",["kausaalisuus","korrelaatio","viitekehys","vivahde"],"kausaalisuus"),
_q(4,"C2","reading","Lue: ”Korrelaatio ei yksin osoita kausaalisuutta.” Mitä lause tarkoittaa?",["Pelkkä korrelaatio ei osoita syy-yhteyttä.","Korrelaatio osoittaa aina syy-yhteyden.","Kausaalisuus ja korrelaatio ovat sama asia.","Korrelaatiota ei ole."],"Pelkkä korrelaatio ei osoita syy-yhteyttä.","technical-register"),
]