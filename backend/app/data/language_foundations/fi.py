"""Finnish (suomi) A1-C2 foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

def _g(slug, title, level, summary, explanation, examples):
    return GrammarTopic(slug=slug, title=title, level=level, category="grammar", summary=summary, explanation=explanation, examples=[GrammarExample(text=x) for x in examples])

GRAMMAR_TOPICS = [
_g("pronouns","Persoonapronominit","A1","Use personal pronouns.","Minä, sinä, hän, me, te and he; spoken Finnish often uses mä and sä.",["Minä olen Aino.","Hän opiskelee suomea."]),
_g("present","Preesens ja verbityypit","A1","Describe present actions.","Learn common verb types and person endings.",["Puhun suomea.","Me asumme Turussa."]),
_g("word-order","Peruslause ja sanajärjestys","A1","Build basic clauses.","Finnish word order is flexible, but neutral clauses commonly begin with the subject.",["Minä asun Helsingissä.","Tänään menen kouluun."]),
_g("vowel-harmony","Vokaaliharmonia","A1","Apply vowel harmony.","Suffix vowels usually harmonize with front or back vowels; e and i are neutral.",["talossa","kylässä"]),
_g("questions","Kysymykset","A1","Ask questions.","Use question words and the -ko/-kö clitic.",["Missä asut?","Puhutko suomea?"]),
_g("negation","Kieltoverbi","A1","Form negative clauses.","The negative auxiliary inflects for person and combines with a connegative verb form.",["En ymmärrä.","He eivät tule."]),
_g("partitive","Partitiivi","A1","Use the partitive in common contexts.","Partitive appears with quantities, many objects, and incomplete or ongoing situations.",["Juon vettä.","Ostan kahvia."]),
_g("local-cases","Paikallissijat","A1","Express location and movement.","Learn inessive, elative, illative, adessive, ablative and allative in everyday phrases.",["Olen talossa.","Menen asemalle."]),
_g("genitive","Genetiivi ja omistus","A2","Express possession and relationships.","The genitive commonly marks possession and appears in many object and modifier constructions.",["Tämä on ystäväni kirja.","Odotan bussin lähtöä."]),
_g("past","Imperfekti","A2","Talk about past events.","Use the imperfect for bounded past events and recognize common stem changes.",["Eilen kävin kirjastossa.","Teimme ruokaa."]),
_g("perfect","Perfekti ja pluskvamperfekti","A2","Connect past events to a reference point.","Use olla plus the past participle; plusquamperfect describes an earlier past event.",["Olen käynyt Suomessa.","Olin jo syönyt."]),
_g("future-time","Tulevaisuudesta puhuminen","A2","Talk about future plans.","Finnish generally uses present tense with a future time expression or a verb of intention.",["Huomenna menen töihin.","Aion opiskella lisää."]),
_g("comparatives","Vertailu","A2","Compare people and things.","Use comparative and superlative forms and the elative in comparisons.",["Tämä on halvempi.","Hän on meistä pisin."]),
_g("imperative","Käskyt ja kohteliaisuus","A2","Give instructions politely.","Use imperative forms and softening expressions such as voisitko.",["Avaa ikkuna, kiitos.","Voisitko auttaa minua?"]),
_g("verb-rection","Verbien rektiot","B1","Choose the case required by a verb.","Many Finnish verbs govern a particular case or a specific complement pattern.",["Pidän musiikista.","Odotan ystävääni."]),
_g("object-cases","Objektin sijamuodot","B1","Distinguish total and partial objects.","Object case depends on clause polarity, aspectual meaning, and sentence structure.",["Luin kirjan.","Luin kirjaa."]),
_g("passive","Passiivi","B1","Use the Finnish passive.","The passive is common in instructions and general statements and differs from personal voice.",["Täällä puhutaan suomea.","Kokous aloitetaan kello yhdeksän."]),
_g("conditional","Konditionaali","B1","Express hypothetical or polite meanings.","The -isi- conditional appears in wishes, possibilities and courteous requests.",["Haluaisin kahvia.","Jos olisi aikaa, tulisin mukaan."]),
_g("relative","Relatiivilauseet","B1","Link clauses with relative pronouns.","Use joka and mikä, paying attention to their case forms.",["Tässä on kirja, jonka ostin.","Hän kertoi asiasta, josta puhuimme."]),
_g("participles","Partisiipit","B1","Use participles in descriptions.","Present and past participles form compact modifiers and occur in passive constructions.",["Kadulla kävelevä mies hymyili.","Suljettu ovi on tuolla."]),
_g("necessity","Täytyy, pitää ja on tehtävä","B1","Express obligation and necessity.","Compare täytyy, pitää, kannattaa and the necessive construction.",["Minun täytyy lähteä.","Tehtävä on palautettava huomenna."]),
_g("reported-speech","Referointi","B2","Report statements and questions.","Use että-clauses and indirect questions; recognize the Finnish reportative -han/-hän and evidential nuances.",["Hän sanoi, että tulee myöhemmin.","En tiedä, missä hän asuu."]),
_g("concessive","Myönnytys ja vastakohta","B2","Express contrast and concession.","Use vaikka, kuitenkin, silti, siitä huolimatta and related clause patterns.",["Vaikka satoi, lähdimme ulos.","Hän oli väsynyt, mutta jatkoi."]),
_g("converbs","Infinitiivit ja lauseenvastikkeet","B2","Condense clauses where appropriate.","Learn common infinitive constructions and participial clause substitutes in formal Finnish.",["Lähtiessään hän sulki oven.","Asiaa tarkemmin tutkittaessa huomattiin virhe."]),
_g("passive-perfect","Passiivin aikamuodot","B2","Use passive across time frames.","Recognize passive imperfect, perfect and pluperfect in formal and institutional texts.",["Asia on käsitelty.","Päätös oli tehty ennen kokousta."]),
_g("focus","Teema ja informaatiorakenne","B2","Manage topic and focus.","Word order and particles such as -kin and -kaan/-kään shape emphasis and contrast.",["Minäkin tulen.","Juuri tätä tarkoitin."]),
_g("nominalization","Nominalisointi","B2","Turn actions into noun phrases.","Nominalized forms are frequent in administrative and academic Finnish; keep relationships clear.",["Päätöksen tekeminen kesti.","Tutkimuksen tulokset julkaistiin."]),
_g("register","Rekisteri ja puhekieli","B2","Adapt Finnish to context.","Distinguish standard written Finnish, colloquial forms and professional conventions.",["Mä tuun kohta. (puhekieli)","Tulen pian. (yleiskieli)"]),
_g("academic-hedging","Tieteellinen varovaisuus","C1","Qualify academic claims.","Use näyttää siltä, että; voidaan olettaa; todennäköisesti and evidential framing.",["Tulokset viittaavat siihen, että vaikutus on rajallinen.","Tätä tulkintaa voidaan pitää mahdollisena."]),
_g("complex-subordination","Monipolviset sivulauseet","C1","Build complex arguments.","Combine subordinate clauses while maintaining clear reference and case government.",["Vaikka aineisto on rajallinen, tulokset tukevat hypoteesia, jonka mukaan muutos on pitkäaikainen."]),
_g("argumentation","Argumentointi ja tekstin rakenne","C1","Structure evidence-based arguments.","Signal claims, evidence, counterarguments and conclusions with precise connective choices.",["Ensinnäkin aineisto osoittaa muutoksen; toisaalta vaihtoehtoinen tulkinta on mahdollinen."]),
_g("institutional","Hallinto- ja työelämän kieli","C1","Write formal institutional Finnish.","Use conventional impersonal and nominal structures without unnecessary bureaucratic complexity.",["Hakemus tulee toimittaa määräaikaan mennessä.","Asia käsitellään seuraavassa kokouksessa."]),
_g("pragmatics","Pragmatiikka ja kohteliaisuus","C1","Interpret implied meaning and stance.","Choose directness, mitigation and particles according to relationship and setting.",["Voisitko vielä täsmentää tätä kohtaa?","Ymmärtääkseni ehdotus koskee vain ensimmäistä vaihetta."]),
_g("rhetoric","Retoriikka ja vaikuttaminen","C2","Analyze persuasive language.","Examine framing, parallelism, metaphor and the relationship between evidence and evaluation.",["Kysymys ei ole vain kustannuksista vaan myös yhdenvertaisuudesta."]),
_g("translation","Käännöksen täsmällisyys","C2","Preserve meaning across languages.","Avoid word-for-word calques; preserve Finnish case relations, register, modality and information structure.",["Ilmaus valittiin, koska se säilyttää alkuperäisen tekstin varauksen."]),
_g("literary-style","Kirjallinen tyyli ja vivahteet","C2","Interpret stylistic and literary nuance.","Analyze rhythm, idiom, register shifts and culturally situated meanings.",["Hiljaisuus jäi huoneeseen kuin vastaamaton kysymys."]),
_g("discourse-analysis","Diskurssin analyysi","C2","Analyze cohesion and discourse strategies.","Track reference, presupposition, stance, argument structure and shifts in register.",["Teksti rakentaa vastakkainasettelun valitsemalla toistuvasti saman arvioivan sanaston."]),
]

def _v(i, level, topic, words):
    return VocabularySet(id=i, level=level, topic=topic, unit_ref=f"fi-{level.lower()}-unit-1", words=[VocabularyEntry(word=w,pos=p,definition=d,example=e) for w,p,d,e in words])

VOCABULARY_SETS = [
_v("greetings_a1","A1","Tervehdykset",[("Hei","phrase","hello","Hei!"),("Kiitos","phrase","thank you","Kiitos avusta."),("Anteeksi","phrase","excuse me / sorry","Anteeksi, missä asema on?"),("Näkemiin","phrase","goodbye","Näkemiin!")]),
_v("identity_a1","A1","Minä ja ihmiset",[("nimi","noun","name","Nimeni on Aino."),("ystävä","noun","friend","Hän on ystäväni."),("opiskelija","noun","student","Olen opiskelija."),("opettaja","noun","teacher","Opettaja puhuu suomea.")]),
_v("family_a1","A1","Perhe",[("äiti","noun","mother","Äitini asuu täällä."),("isä","noun","father","Isäni on töissä."),("sisko","noun","sister","Minulla on sisko."),("veli","noun","brother","Veljeni on nuori.")]),
_v("home_a1","A1","Koti",[("koti","noun","home","Olen kotona."),("huone","noun","room","Huone on valoisa."),("keittiö","noun","kitchen","Keittiö on pieni."),("ikkuna","noun","window","Avaa ikkuna.")]),
_v("food_a1","A1","Ruoka",[("leipä","noun","bread","Ostan leipää."),("vesi","noun","water","Juon vettä."),("kahvi","noun","coffee","Haluaisin kahvia."),("omena","noun","apple","Syön omenan.")]),
_v("places_a1","A1","Paikat",[("kauppa","noun","shop","Kauppa on lähellä."),("asema","noun","station","Missä asema on?"),("koulu","noun","school","Lapset menevät kouluun."),("kirjasto","noun","library","Luen kirjastossa.")]),
_v("daily_a2","A2","Arki ja aika",[("herätä","verb","wake up","Herään kello seitsemän."),("aamupala","noun","breakfast","Syön aamupalan."),("myöhässä","adverb","late","Bussi on myöhässä."),("yleensä","adverb","usually","Käyn yleensä kävelyllä.")]),
_v("travel_a2","A2","Matkustaminen",[("lippu","noun","ticket","Ostin junalipun."),("juna","noun","train","Juna lähtee pian."),("vaihtaa","verb","change/transfer","Vaihdan junaa Tampereella."),("matkatavara","noun","luggage","Matkatavarat ovat tässä.")]),
_v("health_a2","A2","Terveys",[("sairas","adjective","ill","Olen tänään sairas."),("lääkäri","noun","doctor","Varaan ajan lääkärille."),("kipu","noun","pain","Minulla on päänsärkyä."),("resepti","noun","prescription","Tarvitsen reseptin.")]),
_v("work_b1","B1","Työelämä",[("työhakemus","noun","job application","Lähetin työhakemuksen."),("kokous","noun","meeting","Kokous alkaa kymmeneltä."),("määräaika","noun","deadline","Määräaika on perjantaina."),("vastuu","noun","responsibility","Vastuu kuuluu tiimille.")]),
_v("education_b1","B1","Opiskelu",[("kurssi","noun","course","Kurssi alkaa syyskuussa."),("tutkinto","noun","degree","Hän suoritti tutkinnon."),("tehtävä","noun","assignment","Palautan tehtävän tänään."),("oppiaine","noun","school subject","Suomi on oppiaine.")]),
_v("society_b1","B1","Yhteiskunta",[("äänestää","verb","vote","Kansalaiset voivat äänestää."),("palvelu","noun","service","Palvelu on maksuton."),("päätös","noun","decision","Päätös julkaistiin."),("oikeus","noun","right/law","Jokaisella on oikeus osallistua.")]),
_v("media_b2","B2","Media ja viestintä",[("uutisointi","noun","news coverage","Uutisointi herätti keskustelua."),("lähdekritiikki","noun","source criticism","Lähdekritiikki on tärkeää."),("väite","noun","claim","Väite vaatii näyttöä."),("näkökulma","noun","perspective","Artikkeli esittää uuden näkökulman.")]),
_v("environment_b2","B2","Ympäristö",[("ilmastonmuutos","noun","climate change","Ilmastonmuutos vaikuttaa luontoon."),("kiertotalous","noun","circular economy","Kiertotalous vähentää jätettä."),("luonnon monimuotoisuus","noun","biodiversity","Luonnon monimuotoisuus on tärkeää."),("päästö","noun","emission","Päästöjä on vähennettävä.")]),
_v("academic_c1","C1","Akateeminen kieli",[("tutkimusasetelma","noun","research design","Tutkimusasetelma kuvataan luvussa kaksi."),("aineisto","noun","data/material","Aineisto kerättiin keväällä."),("johtopäätös","noun","conclusion","Johtopäätös perustuu aineistoon."),("rajoite","noun","limitation","Tutkimuksella on useita rajoitteita.")]),
_v("policy_c1","C1","Hallinto ja päätöksenteko",[("lausunto","noun","statement/opinion","Lausunto julkaistiin verkossa."),("toimeenpano","noun","implementation","Toimeenpano alkaa ensi vuonna."),("sidosryhmä","noun","stakeholder","Sidosryhmät osallistuvat valmisteluun."),("vaikutusarviointi","noun","impact assessment","Vaikutusarviointi täydentää ehdotusta.")]),
_v("rhetoric_c2","C2","Retoriikka ja analyysi",[("kehystys","noun","framing","Kehystys vaikuttaa tulkintaan."),("implisiittinen","adjective","implicit","Teksti sisältää implisiittisen oletuksen."),("ristiriitainen","adjective","contradictory","Aineisto antaa ristiriitaisen kuvan."),("vivahde","noun","nuance","Sanavalinta muuttaa merkityksen vivahdetta.")]),
_v("idioms_c2","C2","Ilmaukset ja vivahteet",[("ottaa huomioon","phrase","take into account","On tärkeää ottaa kaikki näkökulmat huomioon."),("vetää johtopäätös","phrase","draw a conclusion","Aineistosta ei voi vetää varmaa johtopäätöstä."),("olla samaa mieltä","phrase","agree","Olen tästä täysin samaa mieltä."),("puhua asian vierestä","phrase","talk beside the point","Vastaus puhuu asian vierestä.")]),
]

_UNIT_TITLES = {
"A1":["Tervehdykset ja esittely","Perhe ja ihmiset","Koti ja esineet","Arki ja aika","Ruoka ja ostokset","Paikat ja suunnat","Keskustelu ja apu","Kertaus ja A1-viestintä"],
"A2":["Päivittäiset rutiinit","Menetelmät ja asiointi","Matkustaminen","Terveys ja hyvinvointi","Menneet tapahtumat","Suunnitelmat ja vertailu","Kokemukset ja mielipiteet","Kertaus ja A2-viestintä"],
"B1":["Työ ja opiskelu","Kertominen menneestä","Objektin sijat käytössä","Palvelut ja yhteiskunta","Ehdot ja kohteliaisuus","Suhdelauseet ja kuvailu","Perustelut ja keskustelu","Kertaus ja B1-viestintä"],
"B2":["Media ja lähdekritiikki","Passiivi ja muodollinen kieli","Referointi ja näkökulmat","Ympäristö ja yhteiskunta","Lauseenvastikkeet","Tekstin koheesio","Rekisteri ja argumentointi","Kertaus ja B2-viestintä"],
"C1":["Akateeminen kirjoittaminen","Monipolviset rakenteet","Hallinto ja työelämä","Varovaisuus ja evidenssi","Argumentin rakentaminen","Pragmatiikka ja sävy","Tekstin muokkaus","Kertaus ja C1-viestintä"],
"C2":["Retoriikan analyysi","Tyylin ja rekisterin hallinta","Käännöksen täsmällisyys","Kirjalliset vivahteet","Diskurssin analyysi","Vaativa argumentointi","Kielellinen editointi","Kertaus ja C2-viestintä"]}
_LEVEL_GRAMMAR = {
"A1":["pronouns","present","word-order","vowel-harmony","questions","negation","partitive","local-cases"],
"A2":["genitive","past","perfect","future-time","comparatives","imperative","verb-rection","local-cases"],
"B1":["verb-rection","object-cases","passive","conditional","relative","participles","necessity","reported-speech"],
"B2":["reported-speech","concessive","converbs","passive-perfect","focus","nominalization","register","complex-subordination"],
"C1":["academic-hedging","complex-subordination","argumentation","institutional","pragmatics","nominalization","focus","reported-speech"],
"C2":["rhetoric","translation","literary-style","discourse-analysis","argumentation","pragmatics","register","complex-subordination"]}
_LEVEL_VOCAB = {"A1":["greetings_a1","identity_a1","family_a1","home_a1","food_a1","places_a1","daily_a2","greetings_a1"],"A2":["daily_a2","travel_a2","health_a2","food_a1","places_a1","identity_a1","family_a1","travel_a2"],"B1":["work_b1","education_b1","society_b1","daily_a2","travel_a2","health_a2","work_b1","education_b1"],"B2":["media_b2","environment_b2","society_b1","work_b1","education_b1","media_b2","environment_b2","media_b2"],"C1":["academic_c1","policy_c1","work_b1","society_b1","academic_c1","policy_c1","media_b2","academic_c1"],"C2":["rhetoric_c2","idioms_c2","academic_c1","policy_c1","rhetoric_c2","idioms_c2","media_b2","rhetoric_c2"]}
CURRICULUM = {}
for level, titles in _UNIT_TITLES.items():
    CURRICULUM[level] = []
    for n, title in enumerate(titles, 1):
        CURRICULUM[level].append(CurriculumUnit(
            id=f"fi-{level.lower()}-unit-{n}", level=level, unit_number=n, title=title,
            grammar_points=_LEVEL_GRAMMAR[level] if n == 8 else [_LEVEL_GRAMMAR[level][(n-1)%len(_LEVEL_GRAMMAR[level])], _LEVEL_GRAMMAR[level][n%len(_LEVEL_GRAMMAR[level])]],
            vocabulary_set_ids=[_LEVEL_VOCAB[level][n-1]],
            lesson_types=["grammar","vocabulary","reading","listening","speaking","writing","review"],
            competency_checklist=[f"Use Finnish in the context: {title.lower()}", "Apply the unit's grammar and vocabulary in a short communicative task"],
            default_weeks=2))

def _p(i, situation, phrases):
    return PhrasebookCategory(id=i, level="A1", situation=situation, icon="💬", phrases=[PhrasebookEntry(text=t,context=c,register=r) for t,c,r in phrases])
PHRASEBOOK_CATEGORIES = [
_p("greetings_a1","Tervehdykset ja esittely",[("Hei!","greeting","neutral"),("Minun nimeni on Aino.","introducing yourself","neutral"),("Hauska tavata.","meeting someone","neutral"),("Kiitos paljon.","thanking","neutral")]),
_p("daily_a1","Arki",[("Mitä kuuluu?","asking how someone is","neutral"),("Minulle kuuluu hyvää.","answering","neutral"),("Nähdään huomenna.","saying goodbye","neutral")]),
_p("shopping_a1","Ostokset",[("Paljonko tämä maksaa?","asking a price","neutral"),("Haluaisin ostaa tämän.","buying an item","polite"),("Voinko maksaa kortilla?","payment","neutral")]),
_p("directions_a1","Tien kysyminen",[("Missä asema on?","asking directions","neutral"),("Mene suoraan.","giving directions","neutral"),("Käänny oikealle.","giving directions","neutral")]),
_p("help_a1","Avun pyytäminen",[("Voitko auttaa minua?","asking for help","neutral"),("En ymmärrä.","asking for clarification","neutral"),("Voisitko puhua hitaammin?","asking someone to slow down","polite")]),
_p("work_b1","Työelämä",[("Voisimmeko sopia tapaamisajan?","arranging a meeting","polite"),("Lähetän yhteenvedon sähköpostitse.","follow-up","formal"),("Voisitko täsmentää määräaikaa?","clarifying a deadline","polite")]),
_p("academic_c1","Akateeminen keskustelu",[("Aineisto viittaa siihen, että…","introducing evidence","formal"),("Tätä tulkintaa on syytä tarkastella kriittisesti.","critical discussion","formal"),("Voidaanko tulosta yleistää?","asking about generalization","formal")]),
_p("formal_c1","Virallinen asiointi",[("Pyydän ystävällisesti lisätietoja.","formal inquiry","formal"),("Hakemus on toimitettu määräajassa.","administrative update","formal"),("Kiitän vastauksestanne.","formal thanks","formal")]),
]

ASSESSMENT_BANK = [
AssessmentQuestion(id="fi-a1-001",skill="grammar",difficulty="A1",question="Which sentence means “I do not understand”?",options=["En ymmärrä.","Ei ymmärrän.","Minä ei ymmärrä.","En ymmärtää."],correct="En ymmärrä."),
AssessmentQuestion(id="fi-a1-002",skill="grammar",difficulty="A1",question="Choose the natural Finnish question “Do you speak Finnish?”",options=["Puhutko suomea?","Puhut suomea-ko?","Sinä puhuu suomea?","Puhua suomea?"],correct="Puhutko suomea?"),
AssessmentQuestion(id="fi-a2-001",skill="grammar",difficulty="A2",question="Which form commonly expresses “I drank water”?",options=["Join vettä.","Juon vettä.","Juoda vettä.","Juo vettä."],correct="Join vettä."),
AssessmentQuestion(id="fi-b1-001",skill="grammar",difficulty="B1",question="Which sentence uses the conditional politely?",options=["Haluaisin kahvia.","Haluan kahvia eilen.","Haluaisi kahvia minä.","Haluamaan kahvia."],correct="Haluaisin kahvia."),
AssessmentQuestion(id="fi-b2-001",skill="grammar",difficulty="B2",question="Which sentence reports what someone said?",options=["Hän sanoi, että tulee myöhemmin.","Hän sanoi tulee myöhemmin?","Hän sanoi tule myöhemmin.","Hän sanoo eilen."],correct="Hän sanoi, että tulee myöhemmin."),
AssessmentQuestion(id="fi-c1-001",skill="reading",difficulty="C1",question="Which phrase most clearly signals a cautious academic claim?",options=["Tulokset viittaavat siihen, että…","Tämä todistaa kaiken.","On täysin mahdotonta, että…","Kaikki tietävät, että…"],correct="Tulokset viittaavat siihen, että…"),
AssessmentQuestion(id="fi-c2-001",skill="communication",difficulty="C2",question="Which editing priority best preserves meaning in a Finnish translation?",options=["Preserve case relations, modality and register.","Translate every word in the same order.","Remove all hedging.","Replace idioms with unrelated literal phrases."],correct="Preserve case relations, modality and register."),
]
