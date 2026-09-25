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

_q(5,"A1","vocabulary","Mitä tarkoittaa sana «aamu»?",["päivän alku","päivän loppu","viikko","kuukausi"],"päivän alku"),
_q(6,"A1","reading","Lue: «Mikko asuu Turussa.» Missä Mikko asuu?",["Turussa","Helsingissä","Tampereella","Oulussa"],"Turussa"),
_q(7,"A1","grammar","Valitse oikea kysymys.",["Missä asut?","Missä asua?","Asut missä?","Missä asutko?"],"Missä asut?","questions"),
_q(8,"A1","vocabulary","Mikä on «kirja»?",["luettava teos","juoma","ajoneuvo","ammatti"],"luettava teos"),
_q(5,"A2","grammar","Valitse oikea menneen ajan muoto.",["Eilen menin töihin.","Eilen menen töihin.","Eilen mennä töihin.","Eilen mennyt töihin."],"Eilen menin töihin.","past-tense"),
_q(6,"A2","vocabulary","Mitä «viivästys» tarkoittaa?",["myöhästyminen aikataulusta","varaus","osoite","maksu"],"myöhästyminen aikataulusta"),
_q(7,"A2","reading","Lue: «Kauppa sulkeutuu kello kuusi.» Milloin kauppa sulkeutuu?",["Kello viisi.","Kello kuusi.","Kello seitsemän.","Kello kahdeksan."],"Kello kuusi."),
_q(8,"A2","grammar","Valitse oikea astevaihtelumuoto.",["Minä menen kauppaan.","Minä menee kauppaan.","Minä mennä kauppaan.","Minä menin kauppaan huomenna."],"Minä menen kauppaan.","present-tense"),
_q(5,"B1","grammar","Valitse oikea relatiivilause.",["Tämä on kirja, jonka ostin.","Tämä on kirja, jonka ostaa.","Tämä on kirja, joka ostin sen.","Tämä on kirja, missä ostin."],"Tämä on kirja, jonka ostin.","relative-clause"),
_q(6,"B1","vocabulary","Mitä «haaste» tarkoittaa?",["asia, joka vaatii ponnistelua","palkinto","loma","osoite"],"asia, joka vaatii ponnistelua"),
_q(7,"B1","reading","Lue: «Kokous siirrettiin, koska johtaja oli sairaana.» Miksi kokous siirrettiin?",["Koska johtaja oli sairaana.","Koska toimisto oli suljettu.","Koska juna myöhästyi.","Koska oli juhlapäivä."],"Koska johtaja oli sairaana."),
_q(8,"B1","grammar","Valitse oikea sanajärjestys.",["Eilen ostin uuden tietokoneen.","Eilen minä uuden tietokoneen ostin.","Eilen ostin uuden tietokoneen minä.","Eilen uuden tietokoneen minä ostin."],"Eilen ostin uuden tietokoneen.","word-order"),
_q(5,"B2","grammar","Valitse oikea myönnytysrakenne.",["Vaikka satoi, lähdimme kävelylle.","Vaikka satoi, me lähdimme kävelyllekin.","Vaikka satoi, lähdimme me kävelylle.","Vaikka satoi, me kävelylle lähteä."],"Vaikka satoi, lähdimme kävelylle.","concessive"),
_q(6,"B2","vocabulary","Mitä «ennustaa» tarkoittaa?",["arvioida, mitä tulevaisuudessa tapahtuu","selittää menneisyyttä","muuttaa sääntöä","perua tapaaminen"],"arvioida, mitä tulevaisuudessa tapahtuu"),
_q(7,"B2","reading","Lue: «Tulokset osoittavat selvän suuntauksen, mutta niitä on tulkittava varoen.» Mitä suositellaan?",["Tulosten varovaista tulkintaa.","Tulosten sivuuttamista.","Kaikkien tulosten muuttamista.","Tutkimuksen lopettamista."],"Tulosten varovaista tulkintaa."),
_q(8,"B2","grammar","Valitse oikea epäsuora kysymys.",["En tiedä, milloin kokous alkaa.","En tiedä, milloin alkaa kokous.","En tiedä, milloin kokous alkaa?","En tiedä kokous milloin alkaa."],"En tiedä, milloin kokous alkaa.","indirect-question"),
_q(5,"C1","grammar","Valitse akateemiseen tekstiin sopiva muoto.",["Tulokset viittaavat siihen, että vaikutus on rajallinen.","Tulokset viittaavat, että vaikutus on rajallinen.","Tulokset viittaavat vaikutus, että on rajallinen.","Tulokset viittaa siihen, että vaikutus rajallinen."],"Tulokset viittaavat siihen, että vaikutus on rajallinen.","academic-language"),
_q(6,"C1","vocabulary","Mitä «olennainen» tarkoittaa?",["merkittävä tai tärkeä","satunnainen","väliaikainen","epävirallinen"],"merkittävä tai tärkeä"),
_q(7,"C1","reading","Lue: «Korrelaatio ei yksinään osoita syy-yhteyttä.» Mitä korrelaatio ei osoita?",["Että toinen ilmiö aiheuttaa toisen.","Että aineistoa on olemassa.","Että muuttujat liittyvät toisiinsa.","Että analyysi on tehty."],"Että toinen ilmiö aiheuttaa toisen."),
_q(8,"C1","grammar","Valitse oikea passiivirakenne.",["Tutkimus toteutettiin kolmessa vaiheessa.","Tutkimus toteutettiin kolmessa vaiheessaa.","Tutkimus toteuttaa kolmessa vaiheessa.","Tutkimus toteutettiin kolme vaiheessa."],"Tutkimus toteutettiin kolmessa vaiheessa.","passive"),
_q(5,"C2","grammar","Mikä ilmaus osoittaa akateemista varovaisuutta?",["Ei voida sulkea pois muiden tekijöiden vaikutusta.","Muut tekijät eivät varmasti vaikuta.","Kaikki muut selitykset on todistettu vääriksi.","Muita tekijöitä ei tarvitse tutkia."],"Ei voida sulkea pois muiden tekijöiden vaikutusta.","epistemic-modality"),
_q(6,"C2","vocabulary","Mitä «monitulkintainen» tarkoittaa?",["asia, joka voidaan ymmärtää useammalla tavalla","asia, joka on täysin yksiselitteinen","asia, joka on hyvin lyhyt","asia, joka on helppo mitata"],"asia, joka voidaan ymmärtää useammalla tavalla"),
_q(7,"C2","reading","Lue: «Johtopäätös on vakuuttava, mikäli taustalla oleva oletus pitää paikkansa.» Mistä arvio riippuu?",["Siitä, pitääkö taustalla oleva oletus paikkansa.","Siitä, onko teksti lyhyt.","Siitä, onko tyyli epävirallinen.","Siitä, ovatko tiedot vanhoja."],"Siitä, pitääkö taustalla oleva oletus paikkansa."),
_q(8,"C2","grammar","Valitse täsmällisin akateeminen muoto.",["Tulokset eivät mahdollista varmaa yleistystä ilman lisäaineistoa.","Tulokset mahdollistavat aina varman yleistyksen.","Tulokset eivät mahdollista yleistää ilman lisäaineistoa.","Tulokset mahdollistavat varman yleistyksen ilman aineistoa."],"Tulokset eivät mahdollista varmaa yleistystä ilman lisäaineistoa.","academic-style")

_q(9,"A1","vocabulary","Mitä sana «kiitos» ilmaisee?",["kiitollisuutta","kysymystä","paikkaa","aikaa"],"kiitollisuutta"),
_q(10,"A1","grammar","Täydennä: «Juon ___.»",["vettä","vesi","vedessä","vedestä"],"vettä","partitive"),
_q(11,"A1","reading","Lue: «Liisa työskentelee sairaalassa.» Missä Liisa työskentelee?",["Sairaalassa.","Koulussa.","Kaupassa.","Kirjastossa."],"Sairaalassa."),
_q(12,"A1","vocabulary","Mikä on «juna»?",["kulkuneuvo, joka kulkee raiteilla","ruokailuväline","rakennus","vaatekappale"],"kulkuneuvo, joka kulkee raiteilla"),

_q(9,"A2","grammar","Valitse oikea paikallissija: «Menen ___.»",["kouluun","koulussa","koulusta","koululla"],"kouluun","local-cases"),
_q(10,"A2","vocabulary","Mitä «lähin» tarkoittaa?",["etäisyydeltään pienin","kaikkein kallein","viimeiseksi tullut","kauimpana oleva"],"etäisyydeltään pienin"),
_q(11,"A2","reading","Lue: «Bussi lähtee kello 14.30. Matka kestää 20 minuuttia.» Milloin bussi saapuu?",["Kello 14.40.","Kello 14.50.","Kello 15.00.","Kello 15.20."],"Kello 14.50."),
_q(12,"A2","grammar","Täydennä: «Minun täytyy ___ aikaisin.»",["lähteä","lähden","lähtee","lähtenyt"],"lähteä","necessity"),

_q(9,"B1","grammar","Täydennä: «En ollut koskaan ___ Lapissa ennen sitä matkaa.»",["käynyt","käyn","käydä","käynytkö"],"käynyt","perfect"),
_q(10,"B1","vocabulary","Mitä verbi «soveltaa» tarkoittaa?",["käyttää tietoa tai menetelmää käytännössä","unohtaa kokonaan","siirtää myöhemmäksi","kieltäytyä keskustelusta"],"käyttää tietoa tai menetelmää käytännössä"),
_q(11,"B1","reading","Lue: «Kaupunki lisäsi bussivuoroja, koska matkustajamäärät kasvoivat.» Miksi vuoroja lisättiin?",["Matkustajia oli enemmän.","Lippujen hinnat laskivat.","Tie suljettiin.","Kuljettajia oli liian paljon."],"Matkustajia oli enemmän."),
_q(12,"B1","grammar","Valitse oikea epäsuora kysymys.",["Hän kysyi, missä asema sijaitsee.","Hän kysyi, missä sijaitsee asema?","Hän kysyi, missä asema sijaitsemaan.","Hän kysyi, missä sijaitsi asema on."],"Hän kysyi, missä asema sijaitsee.","indirect-questions"),

_q(9,"B2","grammar","Valitse oikea ehtolauseen menneen ajan muoto.",["Jos olisin tiennyt asiasta, olisin tullut aikaisemmin.","Jos tiedän asiasta, olisin tullut aikaisemmin.","Jos olisin tietänyt asiasta, tulen aikaisemmin.","Jos tiesin asiasta, olisin tulemaan aikaisemmin."],"Jos olisin tiennyt asiasta, olisin tullut aikaisemmin.","conditionals"),
_q(10,"B2","vocabulary","Mitä «olennainen» tarkoittaa tässä yhteydessä?",["asian kannalta tärkeä","täysin satunnainen","vain väliaikainen","vaikeasti havaittava"],"asian kannalta tärkeä"),
_q(11,"B2","reading","Lue: «Uudistus nopeutti käsittelyä, mutta lisäsi henkilöstön koulutustarvetta.» Mikä oli uudistuksen seuraus?",["Käsittely nopeutui ja koulutustarve kasvoi.","Käsittely hidastui ja koulutustarve väheni.","Koulutusta ei enää tarvittu.","Henkilöstömäärä puolittui."],"Käsittely nopeutui ja koulutustarve kasvoi."),
_q(12,"B2","grammar","Valitse kieliopillisesti oikea lause.",["Siitä huolimatta, että satoi, jatkoimme matkaa.","Siitä huolimatta että satoi, me jatkaa matkaa.","Siitä huolimatta satoi, jatkoimme matkaa että.","Siitä huolimatta, että satoi, jatkamme matkaa eilen."],"Siitä huolimatta, että satoi, jatkoimme matkaa.","concessive-clauses"),

_q(9,"C1","grammar","Valitse akateemiseen tekstiin sopiva jatko: «Vaikka aineisto on laaja, ...»",["tuloksia on tulkittava varoen.","tulokset todistaa kaiken.","aineisto eivät ole hyödyllisiä.","tuloksia tulkita varovainen."],"tuloksia on tulkittava varoen.","academic-register"),
_q(10,"C1","vocabulary","Mitä «ristiriitainen» tarkoittaa?",["sisäisesti keskenään yhteensopimaton","täysin yksiselitteinen","helposti mitattava","aina myönteinen"],"sisäisesti keskenään yhteensopimaton"),
_q(11,"C1","reading","Lue: «Tutkimus tukee hypoteesia, mutta pieni otos rajoittaa tulosten yleistettävyyttä.» Mikä rajoittaa yleistettävyyttä?",["Pieni otos.","Hypoteesin nimi.","Tutkimuksen otsikko.","Tulosten esitystapa."],"Pieni otos."),
_q(12,"C1","grammar","Valitse oikein muodostettu rakenne.",["Tutkimus ei ainoastaan kuvaa ilmiötä vaan myös selittää sitä.","Tutkimus ei ainoastaan kuvaa ilmiötä vaan myös selittävät sitä.","Tutkimus ei ainoastaan kuvaa ilmiötä mutta myös selittää sitäkö.","Tutkimus ei ainoastaan kuvaa ilmiö vaan myös selittää."],"Tutkimus ei ainoastaan kuvaa ilmiötä vaan myös selittää sitä.","correlative-constructions"),

_q(9,"C2","vocabulary","Mitä «implisiittinen» tarkoittaa?",["epäsuorasti ilmaistu tai oletettu","täysin näkyvä ja suora","tilastollisesti mitattu","kielellisesti virheellinen"],"epäsuorasti ilmaistu tai oletettu"),
_q(10,"C2","grammar","Valitse täsmällinen rajaus.",["Sikäli kuin aineisto sallii, tuloksia voidaan yleistää.","Aineisto sallii, tuloksia yleistää aina.","Sikäli aineisto kuin sallii tulokset voidaan yleistää.","Tuloksia voidaan yleistää, koska aineisto ei ole."],"Sikäli kuin aineisto sallii, tuloksia voidaan yleistää.","semantic-precision"),
_q(11,"C2","reading","Lue: «Vaikka malli selittää havaitun vaihtelun, se ei sulje pois vaihtoehtoisia mekanismeja.» Mitä väitettä teksti rajaa?",["Malli ei sulje pois muita selityksiä.","Malli ei selitä havaittua vaihtelua.","Vaihtoehtoisia mekanismeja ei ole.","Havaintoja ei ole tehty."],"Malli ei sulje pois muita selityksiä."),
_q(12,"C2","grammar","Valitse akateemisesti täsmällisin muotoilu.",["Johtopäätös on perusteltu vain siinä määrin kuin käytettävissä oleva näyttö sen sallii.","Johtopäätös on aina perusteltu näytöstä riippumatta.","Näyttö sallii johtopäätöksen ilman rajoituksia.","Johtopäätös perustelee näyttöä kaikissa tapauksissa."],"Johtopäätös on perusteltu vain siinä määrin kuin käytettävissä oleva näyttö sen sallii.","academic-precision"),

]
