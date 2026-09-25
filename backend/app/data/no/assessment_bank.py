from app.data._types import AssessmentQuestion

ASSESSMENT_BANK = [
AssessmentQuestion(id="no-a1-001",skill="grammar",difficulty="A1",question="Velg riktig setning.",options=["Jeg er student.","Jeg student er.","Er jeg student er.","Student jeg er."],correct="Jeg er student."),
AssessmentQuestion(id="no-a1-002",skill="vocabulary",difficulty="A1",question="Hva betyr «takk»?",options=["et høflig ord når du får noe","en hilsen om morgenen","et spørsmål om navn","en beskjed om tid"],correct="et høflig ord når du får noe"),
AssessmentQuestion(id="no-a1-003",skill="grammar",difficulty="A1",question="Velg riktig negasjon.",options=["Jeg ikke snakker norsk.","Jeg snakker ikke norsk.","Ikke jeg snakker norsk.","Jeg snakker norsk ikke."],correct="Jeg snakker ikke norsk."),
AssessmentQuestion(id="no-a1-004",skill="reading",difficulty="A1",question="«Jeg bor i Oslo.» Hvor bor personen?",options=["Bergen","Oslo","Trondheim","Tromsø"],correct="Oslo"),

AssessmentQuestion(id="no-a2-001",skill="grammar",difficulty="A2",question="Velg riktig preteritum.",options=["I går går jeg hjem.","I går gikk jeg hjem.","I går gå jeg hjem.","I går har gikk jeg hjem."],correct="I går gikk jeg hjem."),
AssessmentQuestion(id="no-a2-002",skill="grammar",difficulty="A2",question="Velg riktig perfektum.",options=["Jeg har spist.","Jeg har spise.","Jeg spiste har.","Jeg spise har."],correct="Jeg har spist."),
AssessmentQuestion(id="no-a2-003",skill="vocabulary",difficulty="A2",question="Hva betyr «forsinket»?",options=["at noe kommer senere enn planlagt","at noe er billig","at noe er sunt","at noe er stille"],correct="at noe kommer senere enn planlagt"),
AssessmentQuestion(id="no-a2-004",skill="reading",difficulty="A2",question="«Toget går klokken åtte, men det er forsinket.» Når skulle toget gå?",options=["06:00","07:00","08:00","09:00"],correct="08:00"),

AssessmentQuestion(id="no-b1-001",skill="grammar",difficulty="B1",question="Velg riktig leddsetning.",options=["Jeg tror at han kommer.","Jeg tror han at kommer.","Jeg at tror han kommer.","Jeg tror kommer at han."],correct="Jeg tror at han kommer."),
AssessmentQuestion(id="no-b1-002",skill="grammar",difficulty="B1",question="Velg riktig passivform.",options=["Døren åpner klokken åtte.","Døren åpnes klokken åtte.","Døren åpned klokken åtte.","Døren blir åpne klokken åtte."],correct="Døren åpnes klokken åtte."),
AssessmentQuestion(id="no-b1-003",skill="vocabulary",difficulty="B1",question="Hva betyr «innvending»?",options=["en innsigelse mot et forslag eller argument","en månedslønn","en reise","en ferie"],correct="en innsigelse mot et forslag eller argument"),
AssessmentQuestion(id="no-b1-004",skill="reading",difficulty="B1",question="«Prosjektet ble forsinket fordi leveransen kom sent.» Hvorfor ble prosjektet forsinket?",options=["Fordi møtet ble avlyst.","Fordi leveransen kom sent.","Fordi planen var ny.","Fordi kontoret var stengt."],correct="Fordi leveransen kom sent."),

AssessmentQuestion(id="no-b2-001",skill="grammar",difficulty="B2",question="Velg riktig innrømmende konstruksjon.",options=["Selv om det regner, går vi ut.","Selv det regner om, går vi ut.","Om selv det regner, går vi ut.","Det regner selv om går vi ut."],correct="Selv om det regner, går vi ut."),
AssessmentQuestion(id="no-b2-002",skill="grammar",difficulty="B2",question="Velg riktig verbvalg.",options=["Vi må venter på svaret.","Vi må vente på svaret.","Vi må ventet på svaret.","Vi må å vente på svaret."],correct="Vi må vente på svaret."),
AssessmentQuestion(id="no-b2-003",skill="vocabulary",difficulty="B2",question="Hva betyr «bærekraftig»?",options=["som kan opprettholdes over tid uten å bruke opp ressursene","midlertidig og kortvarig","usikkert og vanskelig å måle","privat og personlig"],correct="som kan opprettholdes over tid uten å bruke opp ressursene"),
AssessmentQuestion(id="no-b2-004",skill="reading",difficulty="B2",question="«Tiltaket er kostbart, men det kan begrense risikoen.» Hva er fordelen?",options=["Det reduserer risikoen.","Det gjør tiltaket billigere.","Det fjerner alle kostnader.","Det øker usikkerheten."],correct="Det reduserer risikoen."),

AssessmentQuestion(id="no-c1-001",skill="grammar",difficulty="C1",question="Velg den mest akademiske formuleringen.",options=["Resultatet kan tyde på en effekt.","Resultatet viser sikkert alt.","Resultatet er bare bra.","Resultatet gjør en ting."],correct="Resultatet kan tyde på en effekt."),
AssessmentQuestion(id="no-c1-002",skill="grammar",difficulty="C1",question="Velg riktig refererende uttrykk.",options=["Studien viser at effekten er begrenset.","Studien viser effekten er begrenset at.","Studien at viser effekten er begrenset.","Studien viser at er effekten begrenset."],correct="Studien viser at effekten er begrenset."),
AssessmentQuestion(id="no-c1-003",skill="vocabulary",difficulty="C1",question="Hva betyr «etterprøvbar»?",options=["som kan kontrolleres eller undersøkes på nytt","følelsesladet og personlig","svært kostbar","uformell og muntlig"],correct="som kan kontrolleres eller undersøkes på nytt"),
AssessmentQuestion(id="no-c1-004",skill="reading",difficulty="C1",question="«Datagrunnlaget er begrenset, og funnene bør derfor tolkes med varsomhet.» Hva er anbefalingen?",options=["Ignorere funnene.","Tolke funnene forsiktig.","Øke kostnadene.","Avslutte studien."],correct="Tolke funnene forsiktig."),

AssessmentQuestion(id="no-c2-001",skill="grammar",difficulty="C2",question="Velg riktig kontrafaktisk konstruksjon.",options=["Hvis jeg hadde visst det, ville jeg sagt fra.","Hvis jeg hadde vite det, ville jeg sagt fra.","Hvis jeg visste det, hadde jeg sagt fra i går.","Hvis jeg har visst det, ville jeg sagt fra."],correct="Hvis jeg hadde visst det, ville jeg sagt fra."),
AssessmentQuestion(id="no-c2-002",skill="grammar",difficulty="C2",question="Velg formuleringen med tydelig evidensstyrke.",options=["Dataene antyder en sammenheng.","Dataene fastslår alle årsaker.","Dataene beviser nødvendigvis alt.","Dataene betyr ingenting."],correct="Dataene antyder en sammenheng."),
AssessmentQuestion(id="no-c2-003",skill="vocabulary",difficulty="C2",question="Hva betyr «forbehold» i akademisk språk?",options=["en begrensning eller reservasjon som må tas med i vurderingen","en feiring","transport","lønn"],correct="en begrensning eller reservasjon som må tas med i vurderingen"),
AssessmentQuestion(id="no-c2-004",skill="reading",difficulty="C2",question="«Samlet sett peker funnene i samme retning, men datagrunnlaget er for begrenset til en entydig konklusjon.» Hva er hovedpoenget?",options=["Funnene er lovende, men konklusjonen må være forsiktig.","Det finnes ingen funn.","Datagrunnlaget er perfekt.","Konklusjonen er helt sikker."],correct="Funnene er lovende, men konklusjonen må være forsiktig."),

AssessmentQuestion(id="no-a1-005",skill="grammar",difficulty="A1",question="Velg riktig spørsmål.",options=["Hvor bor du?","Hvor du bor?","Hvor bor?","Hvor bor du er?"],correct="Hvor bor du?",grammar_slug="questions"),
AssessmentQuestion(id="no-a1-006",skill="vocabulary",difficulty="A1",question="Hva betyr «eple»?",options=["en frukt","et kjøretøy","en bygning","et møbel"],correct="en frukt"),
AssessmentQuestion(id="no-a1-007",skill="reading",difficulty="A1",question="Les: «Maria bor i Bergen.» Hvor bor Maria?",options=["I Bergen.","I Oslo.","I Trondheim.","I Stavanger."],correct="I Bergen."),
AssessmentQuestion(id="no-a1-008",skill="grammar",difficulty="A1",question="Velg riktig setning.",options=["Jeg har en bok.","Jeg har et bok.","Jeg har en bøker.","Jeg har ha en bok."],correct="Jeg har en bok.",grammar_slug="en-et"),
AssessmentQuestion(id="no-a2-005",skill="grammar",difficulty="A2",question="Velg riktig fortidsform.",options=["I går jobbet jeg hjemme.","I går jobber jeg hjemme.","I går jobbe jeg hjemme.","I går jobbet hjemme jeg."],correct="I går jobbet jeg hjemme.",grammar_slug="preteritum"),
AssessmentQuestion(id="no-a2-006",skill="vocabulary",difficulty="A2",question="Hva betyr «forsinkelse»?",options=["at noe kommer senere enn planlagt","en reservasjon","en adresse","en betaling"],correct="at noe kommer senere enn planlagt"),
AssessmentQuestion(id="no-a2-007",skill="reading",difficulty="A2",question="Les: «Butikken stenger klokken seks.» Når stenger butikken?",options=["Klokken fem.","Klokken seks.","Klokken sju.","Klokken åtte."],correct="Klokken seks."),
AssessmentQuestion(id="no-a2-008",skill="grammar",difficulty="A2",question="Velg riktig modalverb.",options=["Jeg må arbeide.","Jeg må arbeider.","Jeg må arbeidet.","Jeg må å arbeide."],correct="Jeg må arbeide.",grammar_slug="modalverb"),
AssessmentQuestion(id="no-b1-005",skill="grammar",difficulty="B1",question="Velg riktig relativsetning.",options=["Dette er boken som jeg kjøpte.","Dette er boken som jeg kjøpt.","Dette er boken som kjøpte jeg.","Dette er boken som jeg kjøpe."],correct="Dette er boken som jeg kjøpte.",grammar_slug="relativsetninger"),
AssessmentQuestion(id="no-b1-006",skill="vocabulary",difficulty="B1",question="Hva betyr «utfordring»?",options=["noe som krever innsats","en belønning","en ferie","en adresse"],correct="noe som krever innsats"),
AssessmentQuestion(id="no-b1-007",skill="reading",difficulty="B1",question="Les: «Møtet ble flyttet fordi direktøren var syk.» Hvorfor ble møtet flyttet?",options=["Fordi direktøren var syk.","Fordi kontoret var stengt.","Fordi toget var forsinket.","Fordi det var ferie."],correct="Fordi direktøren var syk."),
AssessmentQuestion(id="no-b1-008",skill="grammar",difficulty="B1",question="Velg riktig ordstilling.",options=["I går kjøpte jeg en ny datamaskin.","I går jeg kjøpte en ny datamaskin.","I går kjøpte en ny datamaskin jeg.","I går en ny datamaskin kjøpte jeg."],correct="I går kjøpte jeg en ny datamaskin.",grammar_slug="ordstilling"),
AssessmentQuestion(id="no-b2-005",skill="grammar",difficulty="B2",question="Velg riktig innrømmende leddsetning.",options=["Selv om det regnet, gikk vi en tur.","Selv om det regnet, vi gikk en tur.","Selv om regnet det, gikk vi en tur.","Selv om det regnet, vi en tur gikk."],correct="Selv om det regnet, gikk vi en tur.",grammar_slug="leddsetninger"),
AssessmentQuestion(id="no-b2-006",skill="vocabulary",difficulty="B2",question="Hva betyr «forutsi»?",options=["å si hva man tror vil skje","å forklare fortiden","å endre en regel","å avlyse en avtale"],correct="å si hva man tror vil skje"),
AssessmentQuestion(id="no-b2-007",skill="reading",difficulty="B2",question="Les: «Resultatene viser en tydelig tendens, men bør tolkes med forsiktighet.» Hva anbefales?",options=["Forsiktig tolkning av resultatene.","Å ignorere resultatene.","Å endre alle resultatene.","Å avslutte undersøkelsen."],correct="Forsiktig tolkning av resultatene."),
AssessmentQuestion(id="no-b2-008",skill="grammar",difficulty="B2",question="Velg riktig indirekte spørsmål.",options=["Jeg vet ikke når møtet begynner.","Jeg vet ikke når begynner møtet.","Jeg vet ikke når møtet begynner?","Jeg vet ikke møtet når begynner."],correct="Jeg vet ikke når møtet begynner.",grammar_slug="indirekte-spørsmål"),
AssessmentQuestion(id="no-c1-005",skill="grammar",difficulty="C1",question="Velg den mest presise akademiske formuleringen.",options=["Resultatene tyder på at effekten er begrenset.","Resultatene tyder at effekten er begrenset.","Resultatene tyder på effekten at er begrenset.","Resultatene tyder på at effekten begrenset."],correct="Resultatene tyder på at effekten er begrenset.",grammar_slug="akademisk-språk"),
AssessmentQuestion(id="no-c1-006",skill="vocabulary",difficulty="C1",question="Hva betyr «vesentlig» i akademisk sammenheng?",options=["betydningsfull eller viktig","tilfeldig","midlertidig","uformell"],correct="betydningsfull eller viktig"),
AssessmentQuestion(id="no-c1-007",skill="reading",difficulty="C1",question="Les: «Korrelasjon beviser ikke i seg selv en årsakssammenheng.» Hva beviser den ikke?",options=["At det ene fenomenet forårsaker det andre.","At det finnes data.","At variablene henger sammen.","At en analyse er gjennomført."],"At det ene fenomenet forårsaker det andre."),
AssessmentQuestion(id="no-c1-008",skill="grammar",difficulty="C1",question="Velg riktig passiv konstruksjon.",options=["Studien ble gjennomført i tre trinn.","Studien ble gjennomføre i tre trinn.","Studien gjennomført ble i tre trinn.","Studien ble gjennomførte i tre trinn."],correct="Studien ble gjennomført i tre trinn.",grammar_slug="passiv"),
AssessmentQuestion(id="no-c2-005",skill="grammar",difficulty="C2",question="Hvilken formulering uttrykker akademisk forsiktighet?",options=["Det kan ikke utelukkes at andre faktorer spiller en rolle.","Andre faktorer spiller sikkert ingen rolle.","Det er bevist uten unntak at andre faktorer er irrelevante.","Det er ikke nødvendig å undersøke andre faktorer."],correct="Det kan ikke utelukkes at andre faktorer spiller en rolle.",grammar_slug="epistemisk-modalisering"),
AssessmentQuestion(id="no-c2-006",skill="vocabulary",difficulty="C2",question="Hva betyr «tvetydig»?",options=["som kan forstås på mer enn én måte","som er helt tydelig","som er svært kort","som er lett å måle"],correct="som kan forstås på mer enn én måte"),
AssessmentQuestion(id="no-c2-007",skill="reading",difficulty="C2",question="Les: «Argumentet er overbevisende, forutsatt at den underliggende antakelsen holder.» Hva avhenger vurderingen av?",options=["At den underliggende antakelsen holder.","At argumentet er kort.","At teksten er uformell.","At dataene er gamle."],"At den underliggende antakelsen holder."),
AssessmentQuestion(id="no-c2-008",skill="grammar",difficulty="C2",question="Velg den mest presise akademiske formuleringen.",options=["Resultatene gir ikke grunnlag for en entydig generalisering uten flere data.","Resultatene gir alltid grunnlag for generalisering uten data.","Resultatene gir ikke grunnlag generalisere uten flere.","Resultatene gir sikkert grunnlag for generalisering uten analyse."],"Resultatene gir ikke grunnlag for en entydig generalisering uten flere data.",grammar_slug="akademisk-formulering")



































































































































AssessmentQuestion(id="no-c1-010",skill="vocabulary",difficulty="C1",question="Hva betyr «vesentlig» i en akademisk tekst?",options=["betydningsfull eller viktig","tilfeldig","midlertidig","uformell"],correct="betydningsfull eller viktig"),
AssessmentQuestion(id="no-c1-011",skill="reading",difficulty="C1",question="Les: «Korrelasjon alene beviser ikke en årsakssammenheng.» Hva beviser korrelasjonen ikke?",options=["At det ene fenomenet forårsaker det andre.","At det finnes data.","At variablene henger sammen.","At en analyse er gjennomført."],correct="At det ene fenomenet forårsaker det andre."),
AssessmentQuestion(id="no-c1-012",skill="grammar",difficulty="C1",question="Velg korrekt passiv konstruksjon.",options=["Studien ble gjennomført i tre trinn.","Studien ble gjennomføre i tre trinn.","Studien gjennomført ble i tre trinn.","Studien ble gjennomført tre trinn."],correct="Studien ble gjennomført i tre trinn.",grammar_slug="passiv-konstruksjon"),
AssessmentQuestion(id="no-c2-009",skill="grammar",difficulty="C2",question="Hvilken formulering uttrykker akademisk forsiktighet?",options=["Det kan ikke utelukkes at andre faktorer spiller en rolle.","Andre faktorer spiller sikkert ingen rolle.","Det er bevist uten unntak at andre faktorer er irrelevante.","Det er ikke nødvendig å undersøke andre faktorer."],correct="Det kan ikke utelukkes at andre faktorer spiller en rolle.",grammar_slug="epistemisk-modalisering"),
AssessmentQuestion(id="no-c2-010",skill="vocabulary",difficulty="C2",question="Hva betyr «tvetydig»?",options=["som kan forstås på mer enn én måte","som er helt entydig","som er svært kort","som er lett å måle"],correct="som kan forstås på mer enn én måte"),
AssessmentQuestion(id="no-c2-011",skill="reading",difficulty="C2",question="Les: «Argumentet er overbevisende, forutsatt at den underliggende antakelsen holder.» Hva avhenger vurderingen av?",options=["At den underliggende antakelsen holder.","At argumentet er kort.","At teksten er uformell.","At dataene er gamle."],correct="At den underliggende antakelsen holder."),
AssessmentQuestion(id="no-c2-012",skill="grammar",difficulty="C2",question="Velg den mest presise akademiske formuleringen.",options=["Resultatene tillater ikke en sikker generalisering uten ytterligere data.","Resultatene tillater alltid generalisering uten data.","Resultatene tillater ikke å generalisere uten ytterligere.","Resultatene tillater en sikker generalisering uten analyse."],correct="Resultatene tillater ikke en sikker generalisering uten ytterligere data.",grammar_slug="akademisk-formulering")
























AssessmentQuestion("no-a1-030","vocabulary","A1","Hva betyr «eple»?",["en frukt","et kjøretøy","en bygning","et møbel"],"en frukt"),
AssessmentQuestion("no-a1-031","reading","A1","Les: «Sara bor i Bergen.» Hvor bor Sara?",["Bergen","Oslo","Trondheim","Stavanger"],"Bergen"),
AssessmentQuestion("no-a1-032","grammar","A1","Velg riktig form.",["Han har en bil.","Han har et bil.","Han ha en bil.","Han har en biler."],"Han har en bil."),
AssessmentQuestion("no-a1-033","vocabulary","A1","Hva betyr «morgen»?",["begynnelsen av dagen","slutten av dagen","en uke","en måned"],"begynnelsen av dagen"),
AssessmentQuestion("no-a1-034","grammar","A1","Velg riktig artikkel: «___ hus er stort.»",["Et","En","Ei","De"],"Et"),
AssessmentQuestion("no-a1-035","reading","A1","Les: «Maria drikker kaffe hver morgen.» Hva drikker Maria?",["Kaffe.","Te.","Vann.","Melk."],"Kaffe."),
AssessmentQuestion("no-a1-036","grammar","A1","Hvilken setning er korrekt?",["Jeg snakker norsk.","Jeg snakkerer norsk.","Jeg snakke norsk.","Jeg norsk snakker."],"Jeg snakker norsk."),
AssessmentQuestion("no-a1-037","vocabulary","A1","Hva betyr «venn»?",["en person du kjenner godt","en bygning","et kjøretøy","en avtale"],"en person du kjenner godt"),
AssessmentQuestion("no-a1-038","grammar","A1","Velg riktig form: «Vi ___ i Oslo.»",["bor","borer","bo","bodde i morgen"],"bor"),
AssessmentQuestion("no-a1-039","reading","A1","Les: «Butikken åpner klokken ni.» Når åpner butikken?",["Klokken åtte.","Klokken ni.","Klokken ti.","Klokken elleve."],"Klokken ni."),
AssessmentQuestion("no-a1-040","vocabulary","A1","Hva betyr «takk»?",["et høflig uttrykk","en adresse","et yrke","et transportmiddel"],"et høflig uttrykk"),
AssessmentQuestion("no-a1-041","grammar","A1","Hvilken setning bruker «være» riktig?",["De er hjemme.","De er hjem.","De være hjemme.","De værede hjemme."],"De er hjemme."),
AssessmentQuestion("no-a1-042","vocabulary","A1","Hvor kjøper du brød?",["På bakeriet.","På sykehuset.","På stasjonen.","På biblioteket."],"På bakeriet."),
AssessmentQuestion("no-a1-043","reading","A1","Les: «Jon jobber ikke i dag.» Hva gjør Jon i dag?",["Han jobber ikke.","Han jobber hjemme.","Han studerer.","Han reiser."],"Han jobber ikke."),
AssessmentQuestion("no-a1-044","grammar","A1","Velg riktig form: «Du ___ norsk.»",["snakker","snakke","snakkerer","snakket i morgen"],"snakker"),
AssessmentQuestion("no-a1-045","vocabulary","A1","Hva betyr «vann»?",["en drikk","et yrke","en bygning","et klesplagg"],"en drikk"),
AssessmentQuestion("no-a1-046","grammar","A1","Hvilken setning er negativ?",["Jeg forstår ikke.","Jeg forstår.","Jeg forsto i går.","Jeg vil forstå."],"Jeg forstår ikke."),
AssessmentQuestion("no-a1-047","reading","A1","Les: «Skolen ligger ved siden av parken.» Hvor ligger skolen?",["Ved siden av parken.","Bak stasjonen.","I sykehuset.","Under huset."],"Ved siden av parken."),
AssessmentQuestion("no-a1-048","vocabulary","A1","Hva betyr «unnskyld»?",["en høflig måte å be om unnskyldning på","en måte å takke på","en hilsen om morgenen","en avslutning på en bok"],"en høflig måte å be om unnskyldning på"),
AssessmentQuestion("no-a2-029","grammar","A2","Velg riktig fortidsform.",["I går jobbet jeg hjemme.","I går jobber jeg hjemme.","I går skal jeg jobbe hjemme.","I går jobbe jeg hjemme."],"I går jobbet jeg hjemme."),
AssessmentQuestion("no-a2-030","vocabulary","A2","Hva betyr «forsinkelse»?",["noe som skjer senere enn planlagt","en bestilling","en adresse","en betaling"],"noe som skjer senere enn planlagt"),
AssessmentQuestion("no-a2-031","reading","A2","Les: «Toget går klokken halv åtte.» Når går toget?",["Klokken sju.","Klokken halv åtte.","Klokken åtte.","Klokken halv ni."],"Klokken halv åtte."),
AssessmentQuestion("no-a2-032","grammar","A2","Velg riktig bruk av «må».",["Jeg må jobbe i morgen.","Jeg må jobber i morgen.","Jeg må jobbet i morgen.","Jeg må arbeid i morgen."],"Jeg må jobbe i morgen."),
AssessmentQuestion("no-a2-033","grammar","A2","Hvilken setning uttrykker fremtid?",["Jeg skal reise i morgen.","Jeg reiste i morgen.","Jeg reise i går.","Jeg skal reiste i morgen."],"Jeg skal reise i morgen."),
AssessmentQuestion("no-a2-034","vocabulary","A2","Hva betyr «avtale»?",["en planlagt tid for et møte eller en aktivitet","en billett","en bygning","en sykdom"],"en planlagt tid for et møte eller en aktivitet"),
AssessmentQuestion("no-a2-035","reading","A2","Les: «Hun går til apoteket etter jobb.» Hvor går hun?",["Til apoteket.","Til skolen.","Til stasjonen.","Til hotellet."],"Til apoteket."),
AssessmentQuestion("no-a2-036","grammar","A2","Velg riktig preposisjon.",["Jeg bor i Norge.","Jeg bor på Norge.","Jeg bor til Norge.","Jeg bor ved Norge."],"Jeg bor i Norge."),
AssessmentQuestion("no-a2-037","grammar","A2","Velg riktig perfektum.",["Jeg har spist.","Jeg har spise.","Jeg har spiste.","Jeg spiser har."],"Jeg har spist."),
AssessmentQuestion("no-a2-038","vocabulary","A2","Hva betyr «nabo»?",["en person som bor i nærheten","en lege","en billett","en butikk"],"en person som bor i nærheten"),
AssessmentQuestion("no-a2-039","reading","A2","Les: «Bussen kommer klokken fem, men den er ti minutter forsinket.» Når skulle bussen komme?",["Klokken 16:40.","Klokken 17:00.","Klokken 17:10.","Klokken 17:20."],"Klokken 17:00."),
AssessmentQuestion("no-a2-040","grammar","A2","Hvilken setning er korrekt?",["Jeg liker å lese.","Jeg liker lese.","Jeg liker å leser.","Jeg liker lest."],"Jeg liker å lese."),
AssessmentQuestion("no-a2-041","vocabulary","A2","Hva betyr «helse»?",["tilstanden til kroppen og sinnet","en reise","en bygning","en avtale"],"tilstanden til kroppen og sinnet"),
AssessmentQuestion("no-a2-042","grammar","A2","Velg riktig flertall.",["to bøker","to bok","to boken","to bøkerne"],"to bøker"),
AssessmentQuestion("no-a2-043","reading","A2","Les: «Restauranten stenger klokken ti.» Når stenger den?",["Klokken åtte.","Klokken ni.","Klokken ti.","Klokken elleve."],"Klokken ti."),
AssessmentQuestion("no-a2-044","vocabulary","A2","Hva betyr «reise»?",["å dra fra ett sted til et annet","å betale en regning","å lese en bok","å lage mat"],"å dra fra ett sted til et annet"),
AssessmentQuestion("no-a2-045","grammar","A2","Velg riktig pronomen.",["Jeg ser henne.","Jeg ser hun.","Jeg ser hennes.","Jeg ser hunne."],"Jeg ser henne."),
AssessmentQuestion("no-a2-046","vocabulary","A2","Hva betyr «butikk»?",["et sted der man kjøper varer","et sykehus","en skole","en flyplass"],"et sted der man kjøper varer"),
AssessmentQuestion("no-a2-047","reading","A2","Les: «Per har time hos legen på tirsdag.» Hvem skal Per besøke?",["Legen.","Læreren.","Tannlegen i går.","Sjåføren."],"Legen."),
AssessmentQuestion("no-a2-048","grammar","A2","Hvilken setning bruker modalverbet riktig?",["Du kan komme i morgen.","Du kan kommer i morgen.","Du kan kom i morgen.","Du kan kommet i morgen."],"Du kan komme i morgen."),

AssessmentQuestion("no-b1-029","grammar","B1","Velg riktig relativsetning.",["Dette er boka som jeg kjøpte.","Dette er boka som jeg kjøpt.","Dette er boka som kjøpte jeg.","Dette er boka som jeg kjøpte den."],"Dette er boka som jeg kjøpte."),
AssessmentQuestion("no-b1-030","vocabulary","B1","Hva betyr «utfordring»?",["noe som krever innsats","en belønning","en ferie","en adresse"],"noe som krever innsats"),
AssessmentQuestion("no-b1-031","reading","B1","Les: «Møtet ble utsatt fordi lederen var syk.» Hvorfor ble møtet utsatt?",["Fordi lederen var syk.","Fordi rommet var stengt.","Fordi toget var forsinket.","Fordi det var ferie."],"Fordi lederen var syk."),
AssessmentQuestion("no-b1-032","grammar","B1","Velg riktig ordstilling.",["I går kjøpte jeg en ny datamaskin.","I går jeg kjøpte en ny datamaskin.","I går kjøpte en ny datamaskin jeg.","I går en ny datamaskin kjøpte jeg."],"I går kjøpte jeg en ny datamaskin."),
AssessmentQuestion("no-b1-033","grammar","B1","Velg riktig betingelsessetning.",["Hvis jeg hadde tid, ville jeg reist.","Hvis jeg hadde tid, vil jeg reiste.","Hvis jeg har tid, ville jeg reist i går.","Hvis jeg hadde tid, jeg reiste i går."],"Hvis jeg hadde tid, ville jeg reist."),
AssessmentQuestion("no-b1-034","vocabulary","B1","Hva betyr «erfaring»?",["kunnskap fra tidligere opplevelser","en billett","en bygning","en avtale"],"kunnskap fra tidligere opplevelser"),
AssessmentQuestion("no-b1-035","reading","B1","Les: «Hun tok bussen fordi bilen var på verksted.» Hvorfor tok hun bussen?",["Fordi bilen var på verksted.","Fordi bussen var gratis.","Fordi hun skulle kjøpe bil.","Fordi toget var forsinket."],"Fordi bilen var på verksted."),
AssessmentQuestion("no-b1-036","grammar","B1","Hvilken setning er korrekt?",["Jeg har allerede lest rapporten.","Jeg har allerede lese rapporten.","Jeg allerede har lest rapporten.","Jeg har allerede leste rapporten."],"Jeg har allerede lest rapporten."),
AssessmentQuestion("no-b1-037","vocabulary","B1","Hva betyr «påvirke»?",["å ha innflytelse på noe","å reise","å betale","å hilse"],"å ha innflytelse på noe"),
AssessmentQuestion("no-b1-038","reading","B1","Les: «Prosjektet ble forsinket, men teamet fullførte arbeidet.» Hva skjedde til slutt?",["Teamet fullførte arbeidet.","Prosjektet ble avlyst.","Teamet sluttet å arbeide.","Arbeidet ble aldri startet."],"Teamet fullførte arbeidet."),
AssessmentQuestion("no-b1-039","grammar","B1","Velg riktig konjunksjon: «Jeg blir hjemme ___ jeg er syk.»",["fordi","men","eller","selv om"],"fordi"),
AssessmentQuestion("no-b1-040","vocabulary","B1","Hva betyr «mulighet»?",["noe som kan la seg gjøre","en følelse","en bygning","en forsinkelse"],"noe som kan la seg gjøre"),
AssessmentQuestion("no-b1-041","reading","B1","Les: «Maria begynte å studere norsk for tre år siden.» Når begynte hun?",["For tre år siden.","I går.","Neste år.","I morgen."],"For tre år siden."),
AssessmentQuestion("no-b1-042","grammar","B1","Velg riktig form.",["Jeg tror at han kommer.","Jeg tror at kommer han.","Jeg tror han at kommer.","Jeg tror at han komme."],"Jeg tror at han kommer."),
AssessmentQuestion("no-b1-043","vocabulary","B1","Hva betyr «beslutning»?",["et valg man har tatt","en reise","en bygning","en sykdom"],"et valg man har tatt"),
AssessmentQuestion("no-b1-044","reading","B1","Les: «Prisen økte, derfor kjøpte færre kunder produktet.» Hva skjedde etter prisøkningen?",["Færre kunder kjøpte produktet.","Flere kunder kjøpte produktet.","Prisen ble satt ned.","Butikken stengte."],"Færre kunder kjøpte produktet."),
AssessmentQuestion("no-b1-045","grammar","B1","Velg riktig sammenligning.",["Denne oppgaven er vanskeligere enn den forrige.","Denne oppgaven er vanskelig enn den forrige.","Denne oppgaven er mest vanskeligere enn den forrige.","Denne oppgaven vanskeligere den forrige."],"Denne oppgaven er vanskeligere enn den forrige."),
AssessmentQuestion("no-b1-046","vocabulary","B1","Hva betyr «sammenheng»?",["forbindelse mellom ting eller hendelser","en billett","en adresse","en ferie"],"forbindelse mellom ting eller hendelser"),
AssessmentQuestion("no-b1-047","reading","B1","Les: «Selv om han var trøtt, fortsatte han å lese.» Hva gjorde han?",["Han fortsatte å lese.","Han gikk og la seg.","Han sluttet å lese.","Han dro på jobb."],"Han fortsatte å lese."),
AssessmentQuestion("no-b1-048","grammar","B1","Velg riktig preposisjon.",["Hun er interessert i språk.","Hun er interessert på språk.","Hun er interessert til språk.","Hun er interessert for språk."],"Hun er interessert i språk."),
AssessmentQuestion("no-b2-029","grammar","B2","Velg riktig innrømmende leddsetning.",["Selv om det regnet, gikk vi en tur.","Selv om det regnet, vi gikk en tur.","Selv om regnet det, gikk vi en tur.","Selv om det regnet, vi en tur gikk."],"Selv om det regnet, gikk vi en tur."),
AssessmentQuestion("no-b2-030","vocabulary","B2","Hva betyr «forutsi»?",["å si hva man tror vil skje","å forklare fortiden","å endre en regel","å avlyse et møte"],"å si hva man tror vil skje"),
AssessmentQuestion("no-b2-031","reading","B2","Les: «Resultatene viser en tydelig tendens, men bør tolkes med forsiktighet.» Hva anbefales?",["Forsiktig tolkning av resultatene.","Å ignorere resultatene.","Å endre resultatene.","Å avslutte undersøkelsen."],"Forsiktig tolkning av resultatene."),
AssessmentQuestion("no-b2-032","grammar","B2","Velg riktig indirekte spørsmål.",["Jeg vet ikke når møtet begynner.","Jeg vet ikke når begynner møtet.","Jeg vet ikke når møtet begynner?","Jeg vet ikke møtet når begynner."],"Jeg vet ikke når møtet begynner."),
AssessmentQuestion("no-b2-033","grammar","B2","Velg riktig passiv.",["Rapporten ble skrevet i går.","Rapporten ble skrive i går.","Rapporten skrevet ble i går.","Rapporten var skrive i går."],"Rapporten ble skrevet i går."),
AssessmentQuestion("no-b2-034","vocabulary","B2","Hva betyr «antakelse»?",["noe man tar for gitt som utgangspunkt","en betaling","en bygning","en reise"],"noe man tar for gitt som utgangspunkt"),
AssessmentQuestion("no-b2-035","reading","B2","Les: «Undersøkelsen viser forbedring, men flere data er nødvendige.» Hva trengs?",["Flere data.","Mindre forskning.","En ny avtale.","Et annet språk."],"Flere data."),
AssessmentQuestion("no-b2-036","grammar","B2","Velg riktig uttrykk for årsak.",["På grunn av regnet ble kampen utsatt.","På grunn regnet ble kampen utsatt.","På grunn av regnet kampen utsatt.","På grunn av regnet ble kampen utsette."],"På grunn av regnet ble kampen utsatt."),
AssessmentQuestion("no-b2-037","vocabulary","B2","Hva betyr «vesentlig»?",["viktig eller betydningsfull","tilfeldig","midlertidig","uformell"],"viktig eller betydningsfull"),
AssessmentQuestion("no-b2-038","reading","B2","Les: «Tiltaket reduserte kostnadene uten å påvirke kvaliteten.» Hva skjedde med kvaliteten?",["Den ble ikke påvirket.","Den ble dårligere.","Den ble doblet.","Den ble fjernet."],"Den ble ikke påvirket."),
AssessmentQuestion("no-b2-039","grammar","B2","Velg riktig uttrykk.",["Det er mulig at resultatene endrer seg.","Det er mulig at resultatene endre seg.","Det er mulig at resultatene endret seg i morgen.","Det er mulig resultatene at endrer seg."],"Det er mulig at resultatene endrer seg."),
AssessmentQuestion("no-b2-040","vocabulary","B2","Hva betyr «påstand»?",["et utsagn som hevder noe","en billett","en ferie","en bygning"],"et utsagn som hevder noe"),
AssessmentQuestion("no-b2-041","reading","B2","Les: «Selv om metoden er enkel, gir den pålitelige resultater.» Hvordan beskrives resultatene?",["Som pålitelige.","Som tilfeldige.","Som ubrukelige.","Som ukjente."],"Som pålitelige."),
AssessmentQuestion("no-b2-042","grammar","B2","Velg riktig komparativ.",["Denne løsningen er mer effektiv enn den andre.","Denne løsningen er mest effektiv enn den andre.","Denne løsningen er mer effektivere enn den andre.","Denne løsningen er effektiv mer enn den andre."],"Denne løsningen er mer effektiv enn den andre."),
AssessmentQuestion("no-b2-043","vocabulary","B2","Hva betyr «tilnærming»?",["en måte å gå fram på","en forsinkelse","en adresse","en betaling"],"en måte å gå fram på"),
AssessmentQuestion("no-b2-044","reading","B2","Les: «Forslaget fikk støtte, men flere deltakere ba om endringer.» Hva ba flere om?",["Endringer i forslaget.","At møtet skulle avlyses.","At prosjektet skulle avsluttes.","At støtten skulle fjernes."],"Endringer i forslaget."),
AssessmentQuestion("no-b2-045","grammar","B2","Velg riktig relativsetning.",["Metoden som ble brukt, var enkel.","Metoden som ble bruke, var enkel.","Metoden som brukte, var enkel.","Metoden som var brukt ble enkel."],"Metoden som ble brukt, var enkel."),
AssessmentQuestion("no-b2-046","vocabulary","B2","Hva betyr «begrensning»?",["en faktor som setter en grense","en fordel","en belønning","en avtale"],"en faktor som setter en grense"),
AssessmentQuestion("no-b2-047","reading","B2","Les: «Dataene er interessante, men utvalget er lite.» Hva er svakheten?",["Utvalget er lite.","Dataene finnes ikke.","Studien er for lang.","Metoden er uforståelig."],"Utvalget er lite."),
AssessmentQuestion("no-b2-048","grammar","B2","Velg riktig nominalisering.",["Gjennomføringen av prosjektet tok seks måneder.","Gjennomføre prosjektet tok seks måneder.","Gjennomførte av prosjektet tok seks måneder.","Gjennomføring prosjektet tok seks måneder."],"Gjennomføringen av prosjektet tok seks måneder."),

AssessmentQuestion("no-c1-029","grammar","C1","Velg den mest presise akademiske formuleringen.",["Resultatene tyder på at effekten er begrenset.","Resultatene tyder at effekten er begrenset.","Resultatene tyder på effekten at er begrenset.","Resultatene tyder at effekten på er begrenset."],"Resultatene tyder på at effekten er begrenset."),
AssessmentQuestion("no-c1-030","vocabulary","C1","Hva betyr «avgjørende» i akademisk sammenheng?",["svært viktig for utfallet","tilfeldig","midlertidig","uformell"],"svært viktig for utfallet"),
AssessmentQuestion("no-c1-031","reading","C1","Les: «Korrelasjonen viser en sammenheng, men beviser ikke årsakssammenheng.» Hva bevises ikke?",["At det ene fenomenet forårsaker det andre.","At dataene finnes.","At variablene henger sammen.","At analysen er gjennomført."],"At det ene fenomenet forårsaker det andre."),
AssessmentQuestion("no-c1-032","grammar","C1","Velg riktig passivkonstruksjon.",["Studien ble gjennomført i tre faser.","Studien ble gjennomføre i tre faser.","Studien gjennomført ble i tre faser.","Studien ble gjennomførte i tre faser."],"Studien ble gjennomført i tre faser."),
AssessmentQuestion("no-c1-033","grammar","C1","Hvilken formulering uttrykker en forsiktig konklusjon?",["Resultatene kan tyde på en begrenset effekt.","Resultatene beviser alltid en begrenset effekt.","Resultatene må uten tvil vise en begrenset effekt.","Resultatene viser definitivt alle årsaker."],"Resultatene kan tyde på en begrenset effekt."),
AssessmentQuestion("no-c1-034","vocabulary","C1","Hva betyr «forutsetning»?",["en betingelse som må være oppfylt","en avslutning","en følelse","en nyhet"],"en betingelse som må være oppfylt"),
AssessmentQuestion("no-c1-035","reading","C1","Les: «Funnene er lovende, men kan ikke generaliseres til hele befolkningen.» Hva kan ikke gjøres?",["Resultatene kan ikke generaliseres til hele befolkningen.","Resultatene kan ikke beskrives.","Dataene kan ikke analyseres.","Studien kan ikke gjennomføres."],"Resultatene kan ikke generaliseres til hele befolkningen."),
AssessmentQuestion("no-c1-036","grammar","C1","Velg riktig årsaksformulering.",["Dette skyldes at datagrunnlaget er begrenset.","Dette skyldes at datagrunnlaget begrenset.","Dette skyldes datagrunnlaget er begrenset.","Dette skyldes at datagrunnlaget begrense."],"Dette skyldes at datagrunnlaget er begrenset."),
AssessmentQuestion("no-c1-037","vocabulary","C1","Hva betyr «nyansert»?",["som tar hensyn til fine forskjeller","som er helt enkelt","som er tilfeldig","som er uformelt"],"som tar hensyn til fine forskjeller"),
AssessmentQuestion("no-c1-038","reading","C1","Les: «Metoden er transparent, slik at andre forskere kan etterprøve resultatene.» Hvorfor er metoden transparent?",["For at andre forskere skal kunne etterprøve resultatene.","For å gjøre teksten kortere.","For å unngå data.","For å fjerne analysen."],"For at andre forskere skal kunne etterprøve resultatene."),
AssessmentQuestion("no-c1-039","grammar","C1","Velg riktig nominalisering.",["Implementeringen av tiltaket krevde betydelige ressurser.","Implementere av tiltaket krevde ressurser.","Implementeringen tiltaket krevde ressurser.","Implementert av tiltaket krevde ressurser."],"Implementeringen av tiltaket krevde betydelige ressurser."),
AssessmentQuestion("no-c1-040","vocabulary","C1","Hva betyr «motsetning»?",["noe som står i kontrast til noe annet","en bekreftelse","en avtale","en fordel"],"noe som står i kontrast til noe annet"),
AssessmentQuestion("no-c1-041","reading","C1","Les: «Forfatteren avviser ikke hypotesen, men etterlyser mer dokumentasjon.» Hva ønsker forfatteren?",["Mer dokumentasjon.","En ny hypotese.","Mindre analyse.","En annen metode uten data."],"Mer dokumentasjon."),
AssessmentQuestion("no-c1-042","grammar","C1","Velg riktig setning med «til tross for».",["Til tross for begrensningene er resultatene relevante.","Til tross begrensningene er resultatene relevante.","Til tross for begrensningene resultatene er relevante.","Til tross for begrensningene er resultatene relevant."],"Til tross for begrensningene er resultatene relevante."),
AssessmentQuestion("no-c1-043","vocabulary","C1","Hva betyr «pålitelig»?",["som gir stabile og troverdige resultater","som er tilfeldig","som endres hele tiden","som er uformell"],"som gir stabile og troverdige resultater"),
AssessmentQuestion("no-c1-044","reading","C1","Les: «Utvalget var representativt, men relativt lite.» Hva er begrensningen?",["Utvalget var relativt lite.","Utvalget var helt tilfeldig.","Resultatene var ikke relevante.","Metoden var ukjent."],"Utvalget var relativt lite."),
AssessmentQuestion("no-c1-045","grammar","C1","Velg riktig indirekte spørsmål.",["Forskerne undersøkte hvordan deltakerne oppfattet tiltaket.","Forskerne undersøkte hvordan oppfattet deltakerne tiltaket.","Forskerne undersøkte hvordan deltakerne tiltaket oppfattet?","Forskerne undersøkte hvordan tiltaket deltakerne oppfattet."],"Forskerne undersøkte hvordan deltakerne oppfattet tiltaket."),
AssessmentQuestion("no-c1-046","vocabulary","C1","Hva betyr «implisere»?",["å innebære eller antyde noe","å avvise noe","å måle noe","å gjenta noe"],"å innebære eller antyde noe"),
AssessmentQuestion("no-c1-047","reading","C1","Les: «Konklusjonen bør forstås i lys av studiens metodiske begrensninger.» Hvordan bør konklusjonen forstås?",["Med hensyn til studiens metodiske begrensninger.","Uavhengig av metoden.","Som et sikkert bevis.","Uten å lese studien."],"Med hensyn til studiens metodiske begrensninger."),
AssessmentQuestion("no-c1-048","grammar","C1","Velg den mest idiomatiske formuleringen.",["Det er grunn til å anta at effekten er begrenset.","Det er grunn til anta at effekten er begrenset.","Det er grunn at anta effekten begrenset.","Det er grunn til å antar at effekten er begrenset."],"Det er grunn til å anta at effekten er begrenset."),
AssessmentQuestion("no-c2-029","grammar","C2","Hvilken formulering uttrykker sterk epistemisk forsiktighet?",["Det kan ikke utelukkes at andre forklaringer er relevante.","Andre forklaringer er uten tvil irrelevante.","Det er bevist at ingen andre forklaringer finnes.","Andre forklaringer trenger ikke undersøkes."],"Det kan ikke utelukkes at andre forklaringer er relevante."),
AssessmentQuestion("no-c2-030","vocabulary","C2","Hva betyr «tvetydig»?",["som kan forstås på mer enn én måte","som er helt entydig","som er svært kort","som er lett å måle"],"som kan forstås på mer enn én måte"),
AssessmentQuestion("no-c2-031","reading","C2","Les: «Argumentet er overbevisende, forutsatt at den underliggende antakelsen holder.» Hva avhenger vurderingen av?",["Om den underliggende antakelsen holder.","Om argumentet er kort.","Om teksten er uformell.","Om dataene er gamle."],"Om den underliggende antakelsen holder."),
AssessmentQuestion("no-c2-032","grammar","C2","Velg den mest presise akademiske formuleringen.",["Funnene gir ikke grunnlag for en entydig konklusjon uten ytterligere data.","Funnene gir alltid grunnlag for en konklusjon uten data.","Funnene gir ikke grunnlag konklusjon uten ytterligere.","Funnene gir grunnlag for en entydig konklusjon uten analyse."],"Funnene gir ikke grunnlag for en entydig konklusjon uten ytterligere data."),
AssessmentQuestion("no-c2-033","grammar","C2","Hvilken formulering markerer et nødvendig forbehold?",["Dette gjelder under forutsetning av at datagrunnlaget er representativt.","Dette gjelder alltid uavhengig av datagrunnlaget.","Dette gjelder uten noen form for begrensning.","Dette gjelder fordi data ikke trenger vurdering."],"Dette gjelder under forutsetning av at datagrunnlaget er representativt."),
AssessmentQuestion("no-c2-034","vocabulary","C2","Hva betyr «forbehold»?",["en uttrykt begrensning eller reservasjon","en sikker konklusjon","en tidsplan","en belønning"],"en uttrykt begrensning eller reservasjon"),
AssessmentQuestion("no-c2-035","reading","C2","Les: «Selv om hypotesen er plausibel, mangler det tilstrekkelig evidens til å fastslå årsakssammenhengen.» Hva mangler?",["Tilstrekkelig evidens for årsakssammenhengen.","En plausibel hypotese.","En metodebeskrivelse.","En forskergruppe."],"Tilstrekkelig evidens for årsakssammenhengen."),
AssessmentQuestion("no-c2-036","grammar","C2","Velg korrekt formulering av kontrast.",["På den ene siden er tiltaket effektivt, på den andre siden er kostnadene høye.","På den ene side tiltaket er effektivt, på den andre kostnadene er høye.","På den ene siden er tiltaket effektivt, på den andre siden kostnadene høye.","På den ene siden tiltaket effektivt er, på den andre siden er kostnadene høye."],"På den ene siden er tiltaket effektivt, på den andre siden er kostnadene høye."),
AssessmentQuestion("no-c2-037","vocabulary","C2","Hva betyr «årsaksforhold»?",["forholdet mellom årsak og virkning","en språklig variasjon","en tidsplan","en økonomisk avtale"],"forholdet mellom årsak og virkning"),
AssessmentQuestion("no-c2-038","reading","C2","Les: «Den observerte effekten kan skyldes både tiltaket og forskjeller mellom gruppene.» Hva innebærer dette?",["Flere forklaringer er mulige.","Tiltaket er den eneste mulige årsaken.","Gruppene er identiske.","Effekten er ikke observert."],"Flere forklaringer er mulige."),
AssessmentQuestion("no-c2-039","grammar","C2","Velg riktig formulering med «med mindre».",["Resultatet kan ikke tolkes sikkert med mindre flere data samles inn.","Resultatet kan ikke tolkes sikkert med mindre flere data samler inn.","Resultatet kan ikke tolkes sikkert med mindre flere data samlet inn.","Resultatet kan ikke tolkes sikkert med mindre samle inn flere data."],"Resultatet kan ikke tolkes sikkert med mindre flere data samles inn."),
AssessmentQuestion("no-c2-040","vocabulary","C2","Hva betyr «uomtvistelig»?",["som det er vanskelig å bestride","som er tvetydig","som er midlertidig","som er ufullstendig"],"som det er vanskelig å bestride"),
AssessmentQuestion("no-c2-041","reading","C2","Les: «Forfatteren problematiserer antakelsen snarere enn å forkaste hele teorien.» Hva gjør forfatteren?",["Setter spørsmålstegn ved antakelsen uten å forkaste hele teorien.","Forkaster hele teorien.","Godtar alle antakelser uten spørsmål.","Avslutter undersøkelsen."],"Setter spørsmålstegn ved antakelsen uten å forkaste hele teorien."),
AssessmentQuestion("no-c2-042","grammar","C2","Velg riktig formulering.",["Det er ikke dermed sagt at resultatene er uten verdi.","Det er ikke dermed sagt at resultatene er uten verdier.","Det er ikke dermed sagt resultatene er uten verdi.","Det er ikke dermed sagt at resultatene være uten verdi."],"Det er ikke dermed sagt at resultatene er uten verdi."),
AssessmentQuestion("no-c2-043","vocabulary","C2","Hva betyr «nyansering»?",["presisering av fine forskjeller eller forbehold","forenkling av alle forskjeller","gjentakelse av samme påstand","utelatelse av data"],"presisering av fine forskjeller eller forbehold"),
AssessmentQuestion("no-c2-044","reading","C2","Les: «Konklusjonen er foreløpig og bør revideres dersom nye data foreligger.» Hva bør skje ved nye data?",["Konklusjonen bør revideres.","Konklusjonen må aldri endres.","Dataene bør ignoreres.","Studien bør slettes."],"Konklusjonen bør revideres."),
AssessmentQuestion("no-c2-045","grammar","C2","Velg mest presise formulering.",["Det er rimelig å anta at effekten varierer mellom gruppene.","Det er rimelig anta at effekten varierer mellom gruppene.","Det er rimelig å antar at effekten varierer mellom gruppene.","Det er rimelig at anta effekten varierer."],"Det er rimelig å anta at effekten varierer mellom gruppene."),
AssessmentQuestion("no-c2-046","vocabulary","C2","Hva betyr «forbeholden»?",["forsiktig og ikke fullt ut bekreftende","helt sikker","svært uformell","helt uavhengig"],"forsiktig og ikke fullt ut bekreftende"),
AssessmentQuestion("no-c2-047","reading","C2","Les: «Selv en sterk korrelasjon kan være forenlig med flere alternative forklaringer.» Hva betyr dette?",["Flere forklaringer kan passe med de samme dataene.","Korrelasjon beviser alltid årsak.","Dataene er uten verdi.","Det finnes bare én forklaring."],"Flere forklaringer kan passe med de samme dataene."),
AssessmentQuestion("no-c2-048","grammar","C2","Velg den mest akademisk presise avslutningen.",["På dette grunnlaget bør konklusjonen tolkes med en viss forsiktighet.","På dette grunnlaget må konklusjonen alltid være sikker.","På dette grunnlaget er alle alternative forklaringer utelukket.","På dette grunnlaget trengs ingen videre vurdering."],"På dette grunnlaget bør konklusjonen tolkes med en viss forsiktighet.")
AssessmentQuestion("no-a1-337","grammar","A1","Velg riktig spørsmål.",["Hvor bor du?","Hvor du bor?","Bor hvor du?","Hvor bor?"],"Hvor bor du?"),
AssessmentQuestion("no-a1-338","vocabulary","A1","Hva betyr «eple»?",["en frukt","et kjøretøy","en bygning","et møbel"],"en frukt"),
AssessmentQuestion("no-a1-339","reading","A1","Les: «Erik bor i Bergen.» Hvor bor Erik?",["I Bergen.","I Oslo.","I Trondheim.","I Stavanger."],"I Bergen."),
AssessmentQuestion("no-a1-340","grammar","A1","Velg riktig form.",["Hun har en bil.","Hun har et bil.","Hun ha en bil.","Hun har en biler."],"Hun har en bil."),
AssessmentQuestion("no-a2-341","grammar","A2","Velg riktig preteritum.",["I går jobbet jeg hjemme.","I går jobber jeg hjemme.","I går jobbe jeg hjemme.","I går skal jeg jobbe hjemme."],"I går jobbet jeg hjemme."),
AssessmentQuestion("no-a2-342","vocabulary","A2","Hva betyr «forsinkelse»?",["noe som kommer senere enn planlagt","en bestilling","en adresse","en betaling"],"noe som kommer senere enn planlagt"),
AssessmentQuestion("no-a2-343","reading","A2","Les: «Butikken stenger klokken seks.» Når stenger butikken?",["Klokken fem.","Klokken seks.","Klokken sju.","Klokken åtte."],"Klokken seks."),
AssessmentQuestion("no-a2-344","grammar","A2","Velg riktig preposisjon.",["Jeg bor i Norge.","Jeg bor på Norge.","Jeg bor til Norge.","Jeg bor ved Norge."],"Jeg bor i Norge."),
AssessmentQuestion("no-b1-345","grammar","B1","Velg riktig relativsetning.",["Dette er boken som jeg kjøpte.","Dette er boken som jeg kjøpt.","Dette er boken jeg som kjøpte.","Dette er boken som kjøpte jeg."],"Dette er boken som jeg kjøpte."),
AssessmentQuestion("no-b1-346","vocabulary","B1","Hva betyr «utfordring»?",["noe som krever innsats","en belønning","en ferie","en adresse"],"noe som krever innsats"),
AssessmentQuestion("no-b1-347","reading","B1","Les: «Møtet ble flyttet fordi direktøren var syk.» Hvorfor ble møtet flyttet?",["Fordi direktøren var syk.","Fordi kontoret var stengt.","Fordi toget var forsinket.","Fordi det var en helligdag."],"Fordi direktøren var syk."),
AssessmentQuestion("no-b1-348","grammar","B1","Velg riktig ordstilling.",["I går kjøpte jeg en ny datamaskin.","I går jeg kjøpte en ny datamaskin.","I går kjøpte en ny datamaskin jeg.","I går en ny datamaskin kjøpte jeg."],"I går kjøpte jeg en ny datamaskin."),
AssessmentQuestion("no-b2-349","grammar","B2","Velg riktig innrømmende leddsetning.",["Selv om det regnet, gikk vi en tur.","Selv om det regnet, vi gikk en tur.","Selv om regnet det, gikk vi en tur.","Selv om det regnet, vi en tur gikk."],"Selv om det regnet, gikk vi en tur."),
AssessmentQuestion("no-b2-350","vocabulary","B2","Hva betyr «forutsi»?",["å si hva man tror vil skje","å forklare fortiden","å endre en regel","å avlyse en avtale"],"å si hva man tror vil skje"),
AssessmentQuestion("no-b2-351","reading","B2","Les: «Resultatene viser en tydelig tendens, men de bør tolkes med forsiktighet.» Hva anbefales?",["Forsiktig tolkning av resultatene.","Å ignorere resultatene.","Å endre alle resultatene.","Å avslutte undersøkelsen."],"Forsiktig tolkning av resultatene."),
AssessmentQuestion("no-b2-352","grammar","B2","Velg riktig indirekte spørsmål.",["Jeg vet ikke når møtet begynner.","Jeg vet ikke når begynner møtet.","Jeg vet ikke når møtet begynner?","Jeg vet ikke møtet når begynner."],"Jeg vet ikke når møtet begynner."),
AssessmentQuestion("no-c1-353","grammar","C1","Velg den mest presise akademiske formuleringen.",["Resultatene tyder på at effekten er begrenset.","Resultatene tyder at effekten er begrenset.","Resultatene tyder på effekten at er begrenset.","Resultatene tyder på at effekten begrenset."],"Resultatene tyder på at effekten er begrenset."),
AssessmentQuestion("no-c1-354","vocabulary","C1","Hva betyr «vesentlig» i en akademisk tekst?",["betydningsfull eller viktig","tilfeldig","midlertidig","uformell"],"betydningsfull eller viktig"),
AssessmentQuestion("no-c1-355","reading","C1","Les: «Korrelasjon beviser ikke i seg selv en årsakssammenheng.» Hva beviser korrelasjonen ikke?",["At det ene fenomenet forårsaker det andre.","At det finnes data.","At variablene henger sammen.","At en analyse er gjennomført."],"At det ene fenomenet forårsaker det andre."),
AssessmentQuestion("no-c1-356","grammar","C1","Velg riktig passiv konstruksjon.",["Studien ble gjennomført i tre trinn.","Studien ble gjennomføre i tre trinn.","Studien gjennomført ble i tre trinn.","Studien ble gjennomført tre trinn."],"Studien ble gjennomført i tre trinn."),
AssessmentQuestion("no-c2-357","grammar","C2","Hvilken formulering uttrykker akademisk forsiktighet?",["Det kan ikke utelukkes at andre faktorer spiller en rolle.","Andre faktorer spiller helt sikkert ingen rolle.","Det er bevist uten unntak at andre faktorer er irrelevante.","Det er unødvendig å undersøke andre faktorer."],"Det kan ikke utelukkes at andre faktorer spiller en rolle."),
AssessmentQuestion("no-c2-358","vocabulary","C2","Hva betyr «tvetydig»?",["som kan forstås på mer enn én måte","som er helt entydig","som er svært kort","som er lett å måle"],"som kan forstås på mer enn én måte"),
AssessmentQuestion("no-c2-359","reading","C2","Les: «Argumentet er overbevisende, forutsatt at den underliggende antakelsen holder.» Hva avhenger vurderingen av?",["At den underliggende antakelsen holder.","At argumentet er kort.","At teksten er uformell.","At dataene er gamle."],"At den underliggende antakelsen holder."),
AssessmentQuestion("no-c2-360","grammar","C2","Velg den mest presise akademiske formuleringen.",["Resultatene gir ikke grunnlag for en entydig generalisering uten flere data.","Resultatene gir alltid grunnlag for generalisering uten data.","Resultatene gir ikke grunnlag for å generalisere uten flere.","Resultatene gir grunnlag for sikker generalisering uten analyse."],"Resultatene gir ikke grunnlag for en entydig generalisering uten flere data.")





























































































AssessmentQuestion("no-a1-009","vocabulary","A1","Hva betyr «morgen»?",["begynnelsen av dagen","slutten av uken","et kjøretøy","et yrke"],"begynnelsen av dagen"),
AssessmentQuestion("no-a2-009","grammar","A2","Velg riktig framtidsuttrykk.",["I morgen skal jeg reise.","I morgen reiste jeg.","I morgen reiser jeg i går.","I morgen skal jeg reiste."],"I morgen skal jeg reise.","framtid"),
AssessmentQuestion("no-b1-009","reading","B1","Les: «Kurset starter neste uke og varer i tre måneder.» Hvor lenge varer kurset?",["Tre måneder.","Én uke.","Ett år.","To dager."],"Tre måneder."),
AssessmentQuestion("no-b2-009","vocabulary","B2","Hva betyr «understreke» i en tekst?",["å gjøre noe ekstra tydelig eller viktig","å glemme noe","å avlyse et møte","å oversette et ord"],"å gjøre noe ekstra tydelig eller viktig"),
AssessmentQuestion("no-c1-009","reading","C1","Les: «Funnene støtter hypotesen bare delvis.» Hva betyr dette?",["Hypotesen støttes bare delvis.","Hypotesen er fullstendig bevist.","Hypotesen er fullstendig avvist.","Det finnes ingen funn."],"Hypotesen støttes bare delvis."),

AssessmentQuestion("no-a1-010","vocabulary","A1","Hva betyr «eple»?",["en frukt","et kjøretøy","en bygning","et møbel"],"en frukt"),
AssessmentQuestion("no-a1-011","grammar","A1","Velg riktig spørsmål.",["Hvor bor du?","Hvor du bor?","Bor hvor du?","Hvor bor?"],"Hvor bor du?"),
AssessmentQuestion("no-a1-012","reading","A1","Les: «Kari bor i Bergen.» Hvor bor Kari?",["Bergen","Oslo","Trondheim","Stavanger"],"Bergen"),
AssessmentQuestion("no-a2-010","grammar","A2","Velg riktig framtidsform.",["Jeg skal reise i morgen.","Jeg skal reiste i morgen.","Jeg skal reiser i morgen.","Jeg reise skal i morgen."],"Jeg skal reise i morgen."),
AssessmentQuestion("no-a2-011","vocabulary","A2","Hva betyr «forsinkelse»?",["at noe kommer senere enn planlagt","en reservasjon","en adresse","en betaling"],"at noe kommer senere enn planlagt"),
AssessmentQuestion("no-a2-012","reading","A2","Les: «Butikken stenger klokken seks.» Når stenger butikken?",["Klokken fem.","Klokken seks.","Klokken sju.","Klokken åtte."],"Klokken seks."),
AssessmentQuestion("no-b1-010","grammar","B1","Velg riktig relativsetning.",["Dette er boka som jeg kjøpte.","Dette er boka som jeg kjøpt.","Dette er boka som kjøpte jeg.","Dette er boka jeg som kjøpte."],"Dette er boka som jeg kjøpte."),
AssessmentQuestion("no-b1-011","vocabulary","B1","Hva betyr «utfordring»?",["noe som krever innsats","en belønning","en ferie","en adresse"],"noe som krever innsats"),
AssessmentQuestion("no-b1-012","reading","B1","Les: «Møtet ble flyttet fordi lederen var syk.» Hvorfor ble møtet flyttet?",["Fordi lederen var syk.","Fordi rommet var stengt.","Fordi toget var forsinket.","Fordi det var ferie."],"Fordi lederen var syk."),
AssessmentQuestion("no-b2-010","grammar","B2","Velg riktig indirekte spørsmål.",["Jeg vet ikke når møtet begynner.","Jeg vet ikke når begynner møtet.","Jeg vet ikke når møtet begynner?","Jeg vet ikke møtet når begynner."],"Jeg vet ikke når møtet begynner."),
AssessmentQuestion("no-b2-011","vocabulary","B2","Hva betyr «forutsi»?",["å si hva man forventer vil skje","å forklare fortiden","å endre en regel","å avlyse en avtale"],"å si hva man forventer vil skje"),
AssessmentQuestion("no-b2-012","reading","B2","Les: «Resultatene viser en tydelig tendens, men bør tolkes med forsiktighet.» Hva anbefales?",["Forsiktig tolkning av resultatene.","Å ignorere resultatene.","Å endre alle resultatene.","Å avslutte undersøkelsen."],"Forsiktig tolkning av resultatene."),


AssessmentQuestion(id="no-a1-005",skill="grammar",difficulty="A1",question="Velg riktig spørsmål.",options=["Hvor bor du?","Hvor du bor?","Bor hvor du?","Hvor bor?"],correct="Hvor bor du?"),
AssessmentQuestion(id="no-a1-006",skill="vocabulary",difficulty="A1",question="Hva betyr «eple»?",options=["en frukt","et kjøretøy","en bygning","et møbel"],correct="en frukt"),
AssessmentQuestion(id="no-a1-007",skill="reading",difficulty="A1",question="«Kari bor i Bergen.» Hvor bor Kari?",options=["Oslo","Bergen","Trondheim","Stavanger"],correct="Bergen"),
AssessmentQuestion(id="no-a1-008",skill="grammar",difficulty="A1",question="Velg riktig form.",options=["Hun har en bil.","Hun har et bil.","Hun ha en bil.","Hun har en biler."],correct="Hun har en bil."),
AssessmentQuestion(id="no-a2-005",skill="grammar",difficulty="A2",question="Velg riktig perfektum.",options=["Jeg har spist.","Jeg har spise.","Jeg har spiste.","Jeg spiser har."],correct="Jeg har spist."),
AssessmentQuestion(id="no-a2-006",skill="vocabulary",difficulty="A2",question="Hva betyr «forsinkelse»?",options=["at noe kommer senere enn planlagt","en reservasjon","en adresse","en betaling"],correct="at noe kommer senere enn planlagt"),
AssessmentQuestion(id="no-a2-007",skill="reading",difficulty="A2",question="«Butikken stenger klokken seks.» Når stenger butikken?",options=["Klokken fem.","Klokken seks.","Klokken sju.","Klokken åtte."],correct="Klokken seks."),
AssessmentQuestion(id="no-a2-008",skill="grammar",difficulty="A2",question="Velg riktig modalverb.",options=["Jeg må jobbe.","Jeg må jobber.","Jeg må jobbet.","Jeg må arbeidet."],correct="Jeg må jobbe."),
AssessmentQuestion(id="no-b1-005",skill="grammar",difficulty="B1",question="Velg riktig relativsetning.",options=["Dette er boka som jeg kjøpte.","Dette er boka som jeg kjøpt.","Dette er boka som kjøpte jeg.","Dette er boka som jeg kjøpte den."],correct="Dette er boka som jeg kjøpte."),
AssessmentQuestion(id="no-b1-006",skill="vocabulary",difficulty="B1",question="Hva betyr «utfordring»?",options=["noe som krever innsats","en belønning","en ferie","en adresse"],correct="noe som krever innsats"),
AssessmentQuestion(id="no-b1-007",skill="reading",difficulty="B1",question="«Møtet ble utsatt fordi direktøren var syk.» Hvorfor ble møtet utsatt?",options=["Fordi direktøren var syk.","Fordi kontoret var stengt.","Fordi toget var forsinket.","Fordi det var en helligdag."],correct="Fordi direktøren var syk."),
AssessmentQuestion(id="no-b1-008",skill="grammar",difficulty="B1",question="Velg riktig ordstilling.",options=["I går kjøpte jeg en ny datamaskin.","I går jeg kjøpte en ny datamaskin.","I går kjøpte en ny datamaskin jeg.","I går en ny datamaskin kjøpte jeg."],correct="I går kjøpte jeg en ny datamaskin."),
AssessmentQuestion(id="no-b2-005",skill="grammar",difficulty="B2",question="Velg riktig leddsetning som uttrykker innrømmelse.",options=["Selv om det regnet, gikk vi en tur.","Selv om det regnet, vi gikk en tur.","Selv om regnet det, gikk vi en tur.","Selv om det regnet, vi en tur gikk."],correct="Selv om det regnet, gikk vi en tur."),
AssessmentQuestion(id="no-b2-006",skill="vocabulary",difficulty="B2",question="Hva betyr «forutsi»?",options=["å si hva man tror vil skje","å forklare fortiden","å endre en regel","å avlyse en avtale"],correct="å si hva man tror vil skje"),
AssessmentQuestion(id="no-b2-007",skill="reading",difficulty="B2",question="«Resultatene viser en tydelig tendens, men bør tolkes med forsiktighet.» Hva anbefales?",options=["Forsiktig tolkning av resultatene.","Å ignorere resultatene.","Å endre alle resultatene.","Å avslutte undersøkelsen straks."],correct="Forsiktig tolkning av resultatene."),
AssessmentQuestion(id="no-b2-008",skill="grammar",difficulty="B2",question="Velg riktig indirekte spørsmål.",options=["Jeg vet ikke når møtet begynner.","Jeg vet ikke når begynner møtet.","Jeg vet ikke når møtet begynner?","Jeg vet ikke møtet når begynner."],correct="Jeg vet ikke når møtet begynner."),
AssessmentQuestion(id="no-c1-005",skill="grammar",difficulty="C1",question="Velg den mest presise akademiske formuleringen.",options=["Resultatene tyder på at effekten er begrenset.","Resultatene tyder at effekten er begrenset.","Resultatene tyder på effekten at er begrenset.","Resultatene tyder på at effekten begrenset."],correct="Resultatene tyder på at effekten er begrenset."),
AssessmentQuestion(id="no-c1-006",skill="vocabulary",difficulty="C1",question="Hva betyr «vesentlig» i akademisk sammenheng?",options=["betydningsfull eller viktig","tilfeldig","midlertidig","uformell"],correct="betydningsfull eller viktig"),
AssessmentQuestion(id="no-c1-007",skill="reading",difficulty="C1",question="«Korrelasjon beviser ikke i seg selv et årsaksforhold.» Hva beviser korrelasjon ikke?",options=["At det ene fenomenet forårsaker det andre.","At det finnes data.","At variablene henger sammen.","At det er gjort en analyse."],correct="At det ene fenomenet forårsaker det andre."),
AssessmentQuestion(id="no-c1-008",skill="grammar",difficulty="C1",question="Velg riktig passiv konstruksjon.",options=["Studien ble gjennomført i tre trinn.","Studien ble gjennomføre i tre trinn.","Studien gjennomført ble i tre trinn.","Studien ble gjennomførte i tre trinn."],correct="Studien ble gjennomført i tre trinn."),
AssessmentQuestion(id="no-c2-005",skill="grammar",difficulty="C2",question="Hvilken formulering uttrykker akademisk forsiktighet?",options=["Det kan ikke utelukkes at andre faktorer spiller en rolle.","Andre faktorer spiller helt sikkert ingen rolle.","Det er bevist uten unntak at andre faktorer er irrelevante.","Det er ikke nødvendig å undersøke andre faktorer."],correct="Det kan ikke utelukkes at andre faktorer spiller en rolle."),
AssessmentQuestion(id="no-c2-006",skill="vocabulary",difficulty="C2",question="Hva betyr «tvetydig»?",options=["som kan forstås på mer enn én måte","som er helt entydig","som er svært kort","som er lett å måle"],correct="som kan forstås på mer enn én måte"),
AssessmentQuestion(id="no-c2-007",skill="reading",difficulty="C2",question="«Argumentet er overbevisende, forutsatt at den underliggende antakelsen holder.» Hva avhenger vurderingen av?",options=["At den underliggende antakelsen holder.","At argumentet er kort.","At teksten er uformell.","At dataene er gamle."],correct="At den underliggende antakelsen holder."),
AssessmentQuestion(id="no-c2-008",skill="grammar",difficulty="C2",question="Velg den mest presise akademiske formuleringen.",options=["Resultatene tillater ikke en entydig generalisering uten ytterligere data.","Resultatene tillater alltid generalisering uten data.","Resultatene tillater ikke å generalisere uten ytterligere.","Resultatene tillater en sikker generalisering uten analyse."],correct="Resultatene tillater ikke en entydig generalisering uten ytterligere data.")
    
    AssessmentQuestion(id="no-a1-005",skill="grammar",difficulty="A1",question="Velg riktig spørsmål.",options=["Hvor bor du?","Hvor du bor?","Bor hvor du?","Hvor bor?"],correct="Hvor bor du?"),
    AssessmentQuestion(id="no-a1-006",skill="vocabulary",difficulty="A1",question="Hva betyr «eple»?",options=["en frukt","et kjøretøy","en bygning","et møbel"],correct="en frukt"),
    AssessmentQuestion(id="no-a1-007",skill="reading",difficulty="A1",question="«Kari bor i Bergen.» Hvor bor Kari?",options=["Oslo","Bergen","Trondheim","Stavanger"],correct="Bergen"),
    AssessmentQuestion(id="no-a1-008",skill="grammar",difficulty="A1",question="Velg riktig form.",options=["Hun har en bil.","Hun har et bil.","Hun ha en bil.","Hun har en biler."],"correct="Hun har en bil."),
    AssessmentQuestion(id="no-a2-005",skill="grammar",difficulty="A2",question="Velg riktig preteritum.",options=["I går jobbet jeg hjemme.","I går jobber jeg hjemme.","I går skal jeg jobbe hjemme.","I går jobbe jeg hjemme."],correct="I går jobbet jeg hjemme."),
    AssessmentQuestion(id="no-a2-006",skill="vocabulary",difficulty="A2",question="Hva betyr «forsinkelse»?",options=["at noe kommer senere enn planlagt","en reservasjon","en adresse","en betaling"],correct="at noe kommer senere enn planlagt"),
    AssessmentQuestion(id="no-a2-007",skill="reading",difficulty="A2",question="«Butikken stenger klokken seks.» Når stenger butikken?",options=["Klokken fem.","Klokken seks.","Klokken sju.","Klokken åtte."],correct="Klokken seks."),
    AssessmentQuestion(id="no-a2-008",skill="grammar",difficulty="A2",question="Velg riktig modalverb.",options=["Jeg må jobbe.","Jeg må jobber.","Jeg må jobbet.","Jeg må arbeid."],correct="Jeg må jobbe."),
    AssessmentQuestion(id="no-b1-005",skill="grammar",difficulty="B1",question="Velg riktig relativsetning.",options=["Dette er boken som jeg kjøpte.","Dette er boken som jeg kjøpt.","Dette er boken som kjøpte jeg.","Dette er boken som jeg kjøpte den."],correct="Dette er boken som jeg kjøpte."),
    AssessmentQuestion(id="no-b1-006",skill="vocabulary",difficulty="B1",question="Hva betyr «utfordring»?",options=["noe som krever innsats","en belønning","en ferie","en adresse"],correct="noe som krever innsats"),
    AssessmentQuestion(id="no-b1-007",skill="reading",difficulty="B1",question="«Møtet ble utsatt fordi direktøren var syk.» Hvorfor ble møtet utsatt?",options=["Fordi direktøren var syk.","Fordi kontoret var stengt.","Fordi toget var forsinket.","Fordi det var helligdag."],correct="Fordi direktøren var syk."),
    AssessmentQuestion(id="no-b1-008",skill="grammar",difficulty="B1",question="Velg riktig ordstilling.",options=["I går kjøpte jeg en ny datamaskin.","I går jeg kjøpte en ny datamaskin.","I går kjøpte en ny datamaskin jeg.","I går en ny datamaskin kjøpte jeg."],correct="I går kjøpte jeg en ny datamaskin."),
    AssessmentQuestion(id="no-b2-005",skill="grammar",difficulty="B2",question="Velg riktig setning med innrømmelse.",options=["Selv om det regnet, gikk vi en tur.","Selv om det regnet, vi gikk en tur.","Selv om regnet det, gikk vi en tur.","Selv om det regnet, vi en tur gikk."],correct="Selv om det regnet, gikk vi en tur."),
    AssessmentQuestion(id="no-b2-006",skill="vocabulary",difficulty="B2",question="Hva betyr «forutsi»?",options=["å si hva man tror vil skje","å forklare fortiden","å endre en regel","å avlyse en avtale"],correct="å si hva man tror vil skje"),
    AssessmentQuestion(id="no-b2-007",skill="reading",difficulty="B2",question="«Resultatene viser en tydelig tendens, men de bør tolkes med forsiktighet.» Hva anbefales?",options=["Forsiktig tolkning av resultatene.","Å ignorere resultatene.","Å endre alle resultatene.","Å avslutte undersøkelsen."],correct="Forsiktig tolkning av resultatene."),
    AssessmentQuestion(id="no-b2-008",skill="grammar",difficulty="B2",question="Velg riktig indirekte spørsmål.",options=["Jeg vet ikke når møtet begynner.","Jeg vet ikke når begynner møtet.","Jeg vet ikke når møtet begynner?","Jeg vet ikke møtet når begynner."],correct="Jeg vet ikke når møtet begynner."),
    AssessmentQuestion(id="no-c1-005",skill="grammar",difficulty="C1",question="Velg den mest presise akademiske formuleringen.",options=["Resultatene tyder på at effekten er begrenset.","Resultatene tyder at effekten er begrenset.","Resultatene tyder på effekten at er begrenset.","Resultatene tyder på at effekten begrenset."],correct="Resultatene tyder på at effekten er begrenset."),
    AssessmentQuestion(id="no-c1-006",skill="vocabulary",difficulty="C1",question="Hva betyr «vesentlig» i en akademisk tekst?",options=["betydningsfull eller viktig","tilfeldig","midlertidig","uformell"],correct="betydningsfull eller viktig"),
    AssessmentQuestion(id="no-c1-007",skill="reading",difficulty="C1",question="«Korrelasjon beviser ikke i seg selv en årsakssammenheng.» Hva beviser korrelasjon ikke?",options=["At det ene fenomenet forårsaker det andre.","At det finnes data.","At variablene henger sammen.","At en analyse er gjennomført."],correct="At det ene fenomenet forårsaker det andre."),
    AssessmentQuestion(id="no-c1-008",skill="grammar",difficulty="C1",question="Velg riktig passiv konstruksjon.",options=["Studien ble gjennomført i tre trinn.","Studien ble gjennomføre i tre trinn.","Studien gjennomført ble i tre trinn.","Studien ble gjennomførte i tre trinn."],correct="Studien ble gjennomført i tre trinn."),
    AssessmentQuestion(id="no-c2-005",skill="grammar",difficulty="C2",question="Hvilken formulering uttrykker akademisk forsiktighet?",options=["Det kan ikke utelukkes at andre faktorer spiller en rolle.","Andre faktorer spiller sikkert ingen rolle.","Det er bevist uten unntak at andre faktorer er irrelevante.","Det er ikke nødvendig å undersøke andre faktorer."],correct="Det kan ikke utelukkes at andre faktorer spiller en rolle."),
    AssessmentQuestion(id="no-c2-006",skill="vocabulary",difficulty="C2",question="Hva betyr «tvetydig»?",options=["som kan forstås på mer enn én måte","som er helt entydig","som er svært kort","som er lett å måle"],correct="som kan forstås på mer enn én måte"),
    AssessmentQuestion(id="no-c2-007",skill="reading",difficulty="C2",question="«Argumentet er overbevisende, forutsatt at den underliggende antakelsen holder.» Hva avhenger vurderingen av?",options=["At den underliggende antakelsen holder.","At argumentet er kort.","At teksten er uformell.","At dataene er gamle."],correct="At den underliggende antakelsen holder."),
    AssessmentQuestion(id="no-c2-008",skill="grammar",difficulty="C2",question="Velg den mest presise akademiske formuleringen.",options=["Resultatene gir ikke grunnlag for en entydig generalisering uten flere data.","Resultatene gir alltid grunnlag for generalisering uten data.","Resultatene gir ikke grunnlag for å generalisere uten flere.","Resultatene gir grunnlag for sikker generalisering uten analyse."],correct="Resultatene gir ikke grunnlag for en entydig generalisering uten flere data.")


AssessmentQuestion(id="no-a1-005",skill="grammar",difficulty="A1",question="Velg riktig spørsmål.",options=["Hvor bor du?","Hvor du bor?","Bor hvor du?","Hvor bor?"],correct="Hvor bor du?"),
AssessmentQuestion(id="no-a1-006",skill="vocabulary",difficulty="A1",question="Hva betyr «eple»?",options=["en frukt","et kjøretøy","en bygning","et møbel"],correct="en frukt"),
AssessmentQuestion(id="no-a1-007",skill="reading",difficulty="A1",question="«Kari bor i Bergen.» Hvor bor Kari?",options=["Bergen","Oslo","Trondheim","Stavanger"],correct="Bergen"),
AssessmentQuestion(id="no-a1-008",skill="grammar",difficulty="A1",question="Velg riktig form.",options=["Hun har en bil.","Hun har et bil.","Hun ha en bil.","Hun har en biler."],correct="Hun har en bil."),
AssessmentQuestion(id="no-a2-005",skill="grammar",difficulty="A2",question="Velg riktig perfektum.",options=["Jeg har spist.","Jeg har spise.","Jeg har spiste.","Jeg spiser har."],correct="Jeg har spist."),
AssessmentQuestion(id="no-a2-006",skill="vocabulary",difficulty="A2",question="Hva betyr «forsinkelse»?",options=["at noe kommer senere enn planlagt","en reservasjon","en adresse","en betaling"],correct="at noe kommer senere enn planlagt"),
AssessmentQuestion(id="no-a2-007",skill="reading",difficulty="A2",question="«Butikken stenger klokken seks.» Når stenger butikken?",options=["Klokken fem.","Klokken seks.","Klokken sju.","Klokken åtte."],correct="Klokken seks."),
AssessmentQuestion(id="no-a2-008",skill="grammar",difficulty="A2",question="Velg riktig preposisjon.",options=["Jeg bor i Norge.","Jeg bor på Norge.","Jeg bor til Norge.","Jeg bor ved Norge."],correct="Jeg bor i Norge."),
AssessmentQuestion(id="no-b1-005",skill="grammar",difficulty="B1",question="Velg riktig relativsetning.",options=["Dette er boken som jeg kjøpte.","Dette er boken som jeg kjøpt.","Dette er boken jeg som kjøpte.","Dette er boken som kjøpte jeg."],correct="Dette er boken som jeg kjøpte."),
AssessmentQuestion(id="no-b1-006",skill="vocabulary",difficulty="B1",question="Hva betyr «utfordring»?",options=["noe som krever innsats","en belønning","en ferie","en adresse"],correct="noe som krever innsats"),
AssessmentQuestion(id="no-b1-007",skill="reading",difficulty="B1",question="«Møtet ble flyttet fordi lederen var syk.» Hvorfor ble møtet flyttet?",options=["Fordi lederen var syk.","Fordi lokalet var stengt.","Fordi toget var forsinket.","Fordi deltakerne hadde ferie."],correct="Fordi lederen var syk."),
AssessmentQuestion(id="no-b1-008",skill="grammar",difficulty="B1",question="Velg riktig ordstilling.",options=["I går kjøpte jeg en ny datamaskin.","I går jeg kjøpte en ny datamaskin.","I går kjøpte en ny datamaskin jeg.","I går en ny datamaskin kjøpte jeg."],correct="I går kjøpte jeg en ny datamaskin."),
AssessmentQuestion(id="no-b2-005",skill="grammar",difficulty="B2",question="Velg riktig innrømmende konstruksjon.",options=["Selv om det regnet, gikk vi en tur.","Selv om det regnet, vi gikk en tur.","Selv om regnet det, gikk vi en tur.","Selv om det regnet, vi en tur gikk."],correct="Selv om det regnet, gikk vi en tur."),
AssessmentQuestion(id="no-b2-006",skill="vocabulary",difficulty="B2",question="Hva betyr «forutsi»?",options=["å si hva man tror vil skje","å forklare noe fra fortiden","å endre en regel","å avlyse en avtale"],correct="å si hva man tror vil skje"),
AssessmentQuestion(id="no-b2-007",skill="reading",difficulty="B2",question="«Resultatene viser en tydelig tendens, men de bør tolkes med forsiktighet.» Hva anbefales?",options=["Forsiktig tolkning av resultatene.","Å ignorere resultatene.","Å endre alle resultatene.","Å avslutte undersøkelsen."],correct="Forsiktig tolkning av resultatene."),
AssessmentQuestion(id="no-b2-008",skill="grammar",difficulty="B2",question="Velg riktig indirekte spørsmål.",options=["Jeg vet ikke når møtet begynner.","Jeg vet ikke når begynner møtet.","Jeg vet ikke når møtet begynner?","Jeg vet ikke møtet når begynner."],correct="Jeg vet ikke når møtet begynner."),
AssessmentQuestion(id="no-c1-005",skill="grammar",difficulty="C1",question="Velg den mest presise akademiske formuleringen.",options=["Resultatene tyder på at effekten er begrenset.","Resultatene tyder at effekten er begrenset.","Resultatene tyder på effekten at er begrenset.","Resultatene tyder på at effekten begrenset."],correct="Resultatene tyder på at effekten er begrenset."),
AssessmentQuestion(id="no-c1-006",skill="vocabulary",difficulty="C1",question="Hva betyr «vesentlig» i en akademisk tekst?",options=["betydningsfull eller viktig","tilfeldig","midlertidig","uformell"],correct="betydningsfull eller viktig"),
AssessmentQuestion(id="no-c1-007",skill="reading",difficulty="C1",question="«Korrelasjon beviser ikke i seg selv et årsaksforhold.» Hva bevises ikke?",options=["At det ene fenomenet forårsaker det andre.","At det finnes data.","At variablene henger sammen.","At det er gjort en analyse."],correct="At det ene fenomenet forårsaker det andre."),
AssessmentQuestion(id="no-c1-008",skill="grammar",difficulty="C1",question="Velg riktig passiv konstruksjon.",options=["Studien ble gjennomført i tre trinn.","Studien ble gjennomføre i tre trinn.","Studien gjennomført ble i tre trinn.","Studien ble gjennomførte i tre trinn."],correct="Studien ble gjennomført i tre trinn."),
AssessmentQuestion(id="no-c2-005",skill="grammar",difficulty="C2",question="Hvilken formulering uttrykker akademisk forsiktighet?",options=["Det kan ikke utelukkes at andre faktorer spiller en rolle.","Andre faktorer spiller sikkert ingen rolle.","Det er bevist uten unntak at andre faktorer er irrelevante.","Det er unødvendig å undersøke andre faktorer."],correct="Det kan ikke utelukkes at andre faktorer spiller en rolle."),
AssessmentQuestion(id="no-c2-006",skill="vocabulary",difficulty="C2",question="Hva betyr «tvetydig»?",options=["som kan forstås på mer enn én måte","som er helt entydig","som er svært kort","som er lett å måle"],correct="som kan forstås på mer enn én måte"),
AssessmentQuestion(id="no-c2-007",skill="reading",difficulty="C2",question="«Argumentet er overbevisende, forutsatt at den underliggende antakelsen holder.» Hva avhenger vurderingen av?",options=["At den underliggende antakelsen holder.","At argumentet er kort.","At teksten er uformell.","At dataene er gamle."],correct="At den underliggende antakelsen holder."),
AssessmentQuestion(id="no-c2-008",skill="grammar",difficulty="C2",question="Velg den mest presise akademiske formuleringen.",options=["Resultatene tillater ikke en entydig generalisering uten ytterligere data.","Resultatene tillater alltid generalisering uten data.","Resultatene tillater ikke å generalisere uten ytterligere.","Resultatene tillater en sikker generalisering uten analyse."],correct="Resultatene tillater ikke en entydig generalisering uten ytterligere data.")


AssessmentQuestion("no-a1-005", "grammar", "A1", "Velg riktig spørsmål.", ["Hvor bor du?", "Hvor du bor?", "Bor hvor du?", "Hvor bor?"], "Hvor bor du?", "spørsmål"),
AssessmentQuestion("no-a1-006", "vocabulary", "A1", "Hva betyr «eple»?", ["en frukt", "et kjøretøy", "en bygning", "et møbel"], "en frukt"),
AssessmentQuestion("no-a1-007", "reading", "A1", "Les: «Kari bor i Bergen.» Hvor bor Kari?", ["I Bergen.", "I Oslo.", "I Trondheim.", "I Stavanger."], "I Bergen."),
AssessmentQuestion("no-a1-008", "grammar", "A1", "Velg riktig form.", ["Hun har en bil.", "Hun har et bil.", "Hun ha en bil.", "Hun har en biler."], "Hun har en bil.", "substantiv"),
AssessmentQuestion("no-a2-005", "grammar", "A2", "Velg riktig preteritum.", ["Jeg jobbet i går.", "Jeg jobbe i går.", "Jeg jobbet i morgen.", "Jeg har jobbe i går."], "Jeg jobbet i går.", "preteritum"),
AssessmentQuestion("no-a2-006", "vocabulary", "A2", "Hva betyr «forsinkelse»?", ["noe som kommer senere enn planlagt", "en bestilling", "en adresse", "en betaling"], "noe som kommer senere enn planlagt"),
AssessmentQuestion("no-a2-007", "reading", "A2", "Les: «Butikken stenger klokken seks.» Når stenger butikken?", ["Klokken fem.", "Klokken seks.", "Klokken sju.", "Klokken åtte."], "Klokken seks."),
AssessmentQuestion("no-a2-008", "grammar", "A2", "Velg riktig modalverb.", ["Jeg må jobbe i morgen.", "Jeg må jobber i morgen.", "Jeg må jobbet i morgen.", "Jeg må jobber."], "Jeg må jobbe i morgen.", "modalverb"),
AssessmentQuestion("no-b1-005", "grammar", "B1", "Velg riktig relativsetning.", ["Dette er boken som jeg kjøpte.", "Dette er boken som jeg kjøpt.", "Dette er boken som kjøpte jeg.", "Dette er boken jeg som kjøpte."], "Dette er boken som jeg kjøpte.", "relativsetninger"),
AssessmentQuestion("no-b1-006", "vocabulary", "B1", "Hva betyr «utfordring»?", ["noe som krever innsats", "en belønning", "en ferie", "en adresse"], "noe som krever innsats"),
AssessmentQuestion("no-b1-007", "reading", "B1", "Les: «Møtet ble flyttet fordi direktøren var syk.» Hvorfor ble møtet flyttet?", ["Fordi direktøren var syk.", "Fordi kontoret var stengt.", "Fordi toget var forsinket.", "Fordi det var helligdag."], "Fordi direktøren var syk."),
AssessmentQuestion("no-b1-008", "grammar", "B1", "Velg riktig ordstilling.", ["I går kjøpte jeg en ny datamaskin.", "I går jeg kjøpte en ny datamaskin.", "I går kjøpte en ny datamaskin jeg.", "I går en ny datamaskin kjøpte jeg."], "I går kjøpte jeg en ny datamaskin.", "ordstilling"),
AssessmentQuestion("no-b2-005", "grammar", "B2", "Velg riktig innrømmende leddsetning.", ["Selv om det regnet, gikk vi en tur.", "Selv om det regnet, vi gikk en tur.", "Selv om regnet det, gikk vi en tur.", "Selv om det regnet, vi en tur gikk."], "Selv om det regnet, gikk vi en tur.", "innrømmende-leddsetninger"),
AssessmentQuestion("no-b2-006", "vocabulary", "B2", "Hva betyr «forutsi»?", ["å si hva man tror vil skje", "å forklare noe fra fortiden", "å endre en regel", "å avlyse en avtale"], "å si hva man tror vil skje"),
AssessmentQuestion("no-b2-007", "reading", "B2", "Les: «Resultatene viser en tydelig tendens, men de bør tolkes med forsiktighet.» Hva anbefales?", ["Forsiktig tolkning av resultatene.", "Å ignorere resultatene.", "Å endre alle resultatene.", "Å avslutte undersøkelsen straks."], "Forsiktig tolkning av resultatene."),
AssessmentQuestion("no-b2-008", "grammar", "B2", "Velg riktig indirekte spørsmål.", ["Jeg vet ikke når møtet begynner.", "Jeg vet ikke når begynner møtet.", "Jeg vet ikke når møtet begynner?", "Jeg vet ikke møtet når begynner."], "Jeg vet ikke når møtet begynner.", "indirekte-spørsmål"),
AssessmentQuestion("no-c1-005", "grammar", "C1", "Velg den mest presise akademiske formuleringen.", ["Resultatene tyder på at effekten er begrenset.", "Resultatene tyder at effekten er begrenset.", "Resultatene tyder på effekten at er begrenset.", "Resultatene tyder på at effekten begrenset er."], "Resultatene tyder på at effekten er begrenset.", "akademisk-språk"),
AssessmentQuestion("no-c1-006", "vocabulary", "C1", "Hva betyr «vesentlig» i en akademisk tekst?", ["betydningsfull eller viktig", "tilfeldig", "midlertidig", "uformell"], "betydningsfull eller viktig"),
AssessmentQuestion("no-c1-007", "reading", "C1", "Les: «Korrelasjon beviser ikke i seg selv en årsakssammenheng.» Hva beviser korrelasjon ikke?", ["At det ene fenomenet forårsaker det andre.", "At det finnes data.", "At variablene henger sammen.", "At det er gjort en analyse."], "At det ene fenomenet forårsaker det andre."),
AssessmentQuestion("no-c1-008", "grammar", "C1", "Velg riktig passiv konstruksjon.", ["Studien ble gjennomført i tre trinn.", "Studien ble gjennomføre i tre trinn.", "Studien gjennomført ble i tre trinn.", "Studien ble gjennomført tre trinn."], "Studien ble gjennomført i tre trinn.", "passiv"),
AssessmentQuestion("no-c2-005", "grammar", "C2", "Hvilken formulering uttrykker faglig forsiktighet?", ["Det kan ikke utelukkes at andre faktorer spiller en rolle.", "Andre faktorer spiller sikkert ingen rolle.", "Det er bevist uten unntak at andre faktorer er irrelevante.", "Det er ikke nødvendig å undersøke andre faktorer."], "Det kan ikke utelukkes at andre faktorer spiller en rolle.", "epistemisk-modalisering"),
AssessmentQuestion("no-c2-006", "vocabulary", "C2", "Hva betyr «tvetydig»?", ["som kan forstås på mer enn én måte", "som er helt entydig", "som er svært kort", "som er lett å måle"], "som kan forstås på mer enn én måte"),
AssessmentQuestion("no-c2-007", "reading", "C2", "Les: «Argumentet er overbevisende, forutsatt at den underliggende antakelsen holder.» Hva avhenger vurderingen av?", ["At den underliggende antakelsen holder.", "At argumentet er kort.", "At teksten er uformell.", "At dataene er gamle."], "At den underliggende antakelsen holder."),
AssessmentQuestion("no-c2-008", "grammar", "C2", "Velg den mest presise akademiske formuleringen.", ["Resultatene gir ikke grunnlag for en entydig generalisering uten flere data.", "Resultatene gir alltid grunnlag for generalisering uten data.", "Resultatene gir ikke grunnlag for å generalisere uten flere.", "Resultatene gir grunnlag for sikker generalisering uten analyse."], "Resultatene gir ikke grunnlag for en entydig generalisering uten flere data.", "akademisk-stil")
]
