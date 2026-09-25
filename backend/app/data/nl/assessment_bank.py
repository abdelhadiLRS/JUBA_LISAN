"""Nederlands assessment bank A1-C2."""
from app.data._types import AssessmentQuestion

ASSESSMENT_BANK = [
    AssessmentQuestion(id="nl-a1-001",skill="grammar",difficulty="A1",question="Welke zin is correct?",options=["Ik ben student.","Ik is student.","Ik bent student.","Ik zijn student."],correct="Ik ben student."),
    AssessmentQuestion(id="nl-a1-002",skill="grammar",difficulty="A1",question="Welke zin heeft de juiste woordvolgorde?",options=["Vandaag werk ik thuis.","Vandaag ik werk thuis.","Vandaag thuis werk ik.","Werk vandaag ik thuis."],correct="Vandaag werk ik thuis."),
    AssessmentQuestion(id="nl-a1-003",skill="vocabulary",difficulty="A1",question="Welk woord betekent 'moeder'?",options=["moeder","vader","broer","zus"],correct="moeder"),
    AssessmentQuestion(id="nl-a1-004",skill="reading",difficulty="A1",question="Je wilt naar de prijs vragen. Wat zeg je?",options=["Hoeveel kost dit?","Hoe heet je?","Waar woon je?","Tot ziens."],correct="Hoeveel kost dit?"),
    AssessmentQuestion(id="nl-a1-005",skill="grammar",difficulty="A1",question="Welke zin gebruikt 'geen' correct?",options=["Ik heb geen auto.","Ik geen heb auto.","Ik heb niet auto.","Ik heb auto geen."],correct="Ik heb geen auto."),
    AssessmentQuestion(id="nl-a1-006",skill="vocabulary",difficulty="A1",question="Wat betekent 'afspraak'?",options=["afgesproken moment","maaltijd","familielid","vervoer"],correct="afgesproken moment"),
    AssessmentQuestion(id="nl-a1-007",skill="reading",difficulty="A1",question="Wat betekent 'Het station is dichtbij'?",options=["Het station is niet ver weg.","Het station is gesloten.","Het station is ver weg.","Het station is duur."],correct="Het station is niet ver weg."),
    AssessmentQuestion(id="nl-a1-008",skill="grammar",difficulty="A1",question="Kies het juiste lidwoord: ___ huis.",options=["het","de","een de","een het"],correct="het"),
    AssessmentQuestion(id="nl-a2-001",skill="grammar",difficulty="A2",question="Welke zin staat in de voltooide tijd?",options=["Ik heb gewerkt.","Ik werk.","Ik werkte.","Ik zal werken."],correct="Ik heb gewerkt."),
    AssessmentQuestion(id="nl-a2-002",skill="grammar",difficulty="A2",question="Welke zin gebruikt een scheidbaar werkwoord correct?",options=["Ik sta om zeven uur op.","Ik opsta om zeven uur.","Ik sta op om zeven uur niet.","Ik sta zeven uur om op."],correct="Ik sta om zeven uur op."),
    AssessmentQuestion(id="nl-a2-003",skill="vocabulary",difficulty="A2",question="Wat betekent 'buurt'?",options=["gebied rond een woning","trein","dokter","formulier"],correct="gebied rond een woning"),
    AssessmentQuestion(id="nl-a2-004",skill="reading",difficulty="A2",question="Welke zin past in een hotel?",options=["Ik wil een kamer reserveren.","Ik wil mijn diploma halen.","Ik wil het debat winnen.","Ik wil de hypothese testen."],correct="Ik wil een kamer reserveren."),
    AssessmentQuestion(id="nl-b1-001",skill="grammar",difficulty="B1",question="Welke zin heeft een correcte bijzin?",options=["Ik blijf thuis omdat ik ziek ben.","Ik blijf thuis omdat ben ik ziek.","Ik blijf thuis omdat ik ben ziek.","Ik blijf thuis omdat ziek ik ben."],correct="Ik blijf thuis omdat ik ziek ben."),
    AssessmentQuestion(id="nl-b1-002",skill="grammar",difficulty="B1",question="Welke zin gebruikt een betrekkelijk voornaamwoord correct?",options=["Het boek dat ik lees is interessant.","Het boek die ik lees is interessant.","De vrouw dat daar woont is docent.","De vrouw wat daar woont is docent."],correct="Het boek dat ik lees is interessant."),
    AssessmentQuestion(id="nl-b1-003",skill="vocabulary",difficulty="B1",question="Wat betekent 'ondersteunen'?",options=["helpen of steunen","tegenwerken","verplaatsen","vergeten"],correct="helpen of steunen"),
    AssessmentQuestion(id="nl-b1-004",skill="reading",difficulty="B1",question="Welke formulering geeft een mening?",options=["Volgens mij is dit een goede oplossing.","Het station is dichtbij.","Ik heb een afspraak.","De les begint om negen uur."],correct="Volgens mij is dit een goede oplossing."),
    AssessmentQuestion(id="nl-b2-001",skill="grammar",difficulty="B2",question="Welke zin staat correct in de passieve vorm?",options=["De beslissing wordt morgen bekendgemaakt.","De beslissing morgen wordt bekend.","De beslissing maakt morgen bekend.","De beslissing wordt morgen bekendmaken."],correct="De beslissing wordt morgen bekendgemaakt."),
    AssessmentQuestion(id="nl-b2-002",skill="vocabulary",difficulty="B2",question="Wat betekent 'nuanceren'?",options=["een uitspraak minder absoluut maken","een document verwijderen","een afspraak annuleren","een woord vertalen"],correct="een uitspraak minder absoluut maken"),
    AssessmentQuestion(id="nl-b2-003",skill="reading",difficulty="B2",question="Welke zin introduceert een tegenargument?",options=["Daar staat tegenover dat...","Mijn naam is...","Hoe laat is het?","Tot morgen."],correct="Daar staat tegenover dat..."),
    AssessmentQuestion(id="nl-b2-004",skill="grammar",difficulty="B2",question="Welke nominalisering is correct?",options=["beslissen → beslissing","werken → werkt","analyseren → analyseer","argumenteren → argumenteert"],correct="beslissen → beslissing"),
    AssessmentQuestion(id="nl-c1-001",skill="reading",difficulty="C1",question="Welke formulering past het best bij academisch Nederlands?",options=["Op basis van deze gegevens kunnen we concluderen dat...","Dit is gewoon supergoed.","Ik vind dit echt leuk.","Hoi, wat denk je?"],correct="Op basis van deze gegevens kunnen we concluderen dat..."),
    AssessmentQuestion(id="nl-c1-002",skill="vocabulary",difficulty="C1",question="Wat betekent 'hypothese'?",options=["veronderstelling die onderzocht wordt","afgesproken tijd","persoonlijke begroeting","vervoermiddel"],correct="veronderstelling die onderzocht wordt"),
    AssessmentQuestion(id="nl-c1-003",skill="reading",difficulty="C1",question="Welke formulering is formeler?",options=["Zou u dit document kunnen toesturen?","Kun je dit sturen?","Stuur dit even.","Dit moet je sturen."],correct="Zou u dit document kunnen toesturen?"),
    AssessmentQuestion(id="nl-c1-004",skill="reading",difficulty="C1",question="Welke zin maakt een analytische nuance?",options=["Een mogelijke interpretatie is dat...","Dit is altijd zo.","Ik weet het niet.","Het is gewoon goed."],correct="Een mogelijke interpretatie is dat..."),
    AssessmentQuestion(id="nl-c2-001",skill="reading",difficulty="C2",question="Wat is een premisse?",options=["een uitgangspunt van een redenering","een begroeting","een reisbestemming","een medische klacht"],correct="een uitgangspunt van een redenering"),
    AssessmentQuestion(id="nl-c2-002",skill="vocabulary",difficulty="C2",question="Wat betekent 'connotatie'?",options=["bijbetekenis van een woord","grammaticale tijd","plaats waar een trein stopt","officieel diploma"],correct="bijbetekenis van een woord"),
    AssessmentQuestion(id="nl-c2-003",skill="reading",difficulty="C2",question="Welke zin vraagt om een preciezere formulering?",options=["Deze formulering is te absoluut.","Hallo, hoe gaat het?","Ik koop brood.","Waar is het station?"],correct="Deze formulering is te absoluut."),
    AssessmentQuestion(id="nl-c2-004",skill="reading",difficulty="C2",question="Welke uitspraak is methodologisch correct?",options=["Correlatie bewijst niet automatisch causaliteit.","Elke correlatie bewijst causaliteit.","Een conclusie heeft nooit bewijs nodig.","Een aanname is altijd een feit."],correct="Correlatie bewijst niet automatisch causaliteit."),

AssessmentQuestion(id="nl-a1-009",skill="grammar",difficulty="A1",question="Kies de juiste vraag.",options=["Waar woon je?","Waar je woont?","Waar woont?","Waar wonen je?"],correct="Waar woon je?",grammar_slug="questions"),
AssessmentQuestion(id="nl-a1-010",skill="vocabulary",difficulty="A1",question="Wat betekent 'appel'?",options=["een vrucht","een voertuig","een gebouw","een meubel"],correct="een vrucht"),
AssessmentQuestion(id="nl-a1-011",skill="reading",difficulty="A1",question="Lees: 'Sofie woont in Utrecht.' Waar woont Sofie?",options=["In Utrecht.","In Rotterdam.","In Groningen.","In Leiden."],correct="In Utrecht."),
AssessmentQuestion(id="nl-a1-012",skill="grammar",difficulty="A1",question="Kies de juiste zin.",options=["Ik heb een boek.","Ik heb een boeken.","Ik heeft een boek.","Ik hebben een boek."],correct="Ik heb een boek.",grammar_slug="present-tense"),
AssessmentQuestion(id="nl-a2-005",skill="grammar",difficulty="A2",question="Kies de juiste verleden tijd.",options=["Gisteren werkte ik thuis.","Gisteren werk ik thuis.","Gisteren werken ik thuis.","Gisteren gewerkt ik thuis."],correct="Gisteren werkte ik thuis.",grammar_slug="past-tense"),
AssessmentQuestion(id="nl-a2-006",skill="vocabulary",difficulty="A2",question="Wat betekent 'vertraging'?",options=["iets dat later komt dan gepland","een reservering","een adres","een betaling"],correct="iets dat later komt dan gepland"),
AssessmentQuestion(id="nl-a2-007",skill="reading",difficulty="A2",question="Lees: 'De winkel sluit om zes uur.' Wanneer sluit de winkel?",options=["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],correct="Om zes uur."),
AssessmentQuestion(id="nl-a2-008",skill="grammar",difficulty="A2",question="Kies de juiste zin met 'moeten'.",options=["Ik moet werken.","Ik moet werkt.","Ik moet gewerkt.","Ik moeten werken."],correct="Ik moet werken.",grammar_slug="modal-verbs"),
AssessmentQuestion(id="nl-b1-005",skill="grammar",difficulty="B1",question="Kies de juiste betrekkelijke bijzin.",options=["Dit is het boek dat ik heb gekocht.","Dit is het boek dat ik gekocht heb het.","Dit is het boek die ik heb gekocht.","Dit is het boek dat ik kopen."],correct="Dit is het boek dat ik heb gekocht.",grammar_slug="relative-clauses"),
AssessmentQuestion(id="nl-b1-006",skill="vocabulary",difficulty="B1",question="Wat betekent 'uitdaging'?",options=["iets waarvoor inspanning nodig is","een beloning","een vakantie","een adres"],correct="iets waarvoor inspanning nodig is"),
AssessmentQuestion(id="nl-b1-007",skill="reading",difficulty="B1",question="Lees: 'De vergadering werd verplaatst omdat de directeur ziek was.' Waarom werd de vergadering verplaatst?",options=["Omdat de directeur ziek was.","Omdat het kantoor gesloten was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],correct="Omdat de directeur ziek was."),
AssessmentQuestion(id="nl-b1-008",skill="grammar",difficulty="B1",question="Kies de juiste woordvolgorde.",options=["Gisteren kocht ik een nieuwe computer.","Gisteren ik kocht een nieuwe computer.","Gisteren kocht een nieuwe computer ik.","Gisteren een nieuwe computer kocht ik."],correct="Gisteren kocht ik een nieuwe computer.",grammar_slug="word-order"),
AssessmentQuestion(id="nl-b2-005",skill="grammar",difficulty="B2",question="Kies de juiste concessieve zin.",options=["Hoewel het regende, gingen we wandelen.","Hoewel het regende, we gingen wandelen.","Hoewel regende het, gingen we wandelen.","Hoewel het regende, we wandelen gingen."],correct="Hoewel het regende, gingen we wandelen.",grammar_slug="concessive-clauses"),
AssessmentQuestion(id="nl-b2-006",skill="vocabulary",difficulty="B2",question="Wat betekent 'voorspellen'?",options=["inschatten wat waarschijnlijk zal gebeuren","iets uit het verleden uitleggen","een regel veranderen","een afspraak annuleren"],correct="inschatten wat waarschijnlijk zal gebeuren"),
AssessmentQuestion(id="nl-b2-007",skill="reading",difficulty="B2",question="Lees: 'De resultaten tonen een duidelijke trend, maar moeten voorzichtig worden geïnterpreteerd.' Wat wordt aanbevolen?",options=["De resultaten voorzichtig interpreteren.","De resultaten negeren.","Alle resultaten veranderen.","Het onderzoek meteen beëindigen."],correct="De resultaten voorzichtig interpreteren."),
AssessmentQuestion(id="nl-b2-008",skill="grammar",difficulty="B2",question="Kies de juiste indirecte vraag.",options=["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],correct="Ik weet niet wanneer de vergadering begint.",grammar_slug="indirect-questions"),
AssessmentQuestion(id="nl-c1-005",skill="grammar",difficulty="C1",question="Kies de meest precieze academische formulering.",options=["De resultaten wijzen erop dat het effect beperkt is.","De resultaten wijzen erop het effect beperkt is.","De resultaten wijst erop dat het effect beperkt is.","De resultaten wijzen dat het effect op beperkt is."],correct="De resultaten wijzen erop dat het effect beperkt is.",grammar_slug="academic-language"),
AssessmentQuestion(id="nl-c1-006",skill="vocabulary",difficulty="C1",question="Wat betekent 'wezenlijk' in een academische tekst?",options=["belangrijk of fundamenteel","toevallig","tijdelijk","informeel"],correct="belangrijk of fundamenteel"),
AssessmentQuestion(id="nl-c1-007",skill="reading",difficulty="C1",question="Lees: 'Correlatie bewijst op zichzelf geen causaal verband.' Wat wordt niet bewezen?",options=["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens zijn.","Dat variabelen samenhangen.","Dat er een analyse is uitgevoerd."],correct="Dat het ene verschijnsel het andere veroorzaakt."),
AssessmentQuestion(id="nl-c1-008",skill="grammar",difficulty="C1",question="Kies de juiste passieve constructie.",options=["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek uitgevoerd werd in drie fasen.","Het onderzoek werd uitvoeren in drie fasen."],correct="Het onderzoek werd in drie fasen uitgevoerd.",grammar_slug="passive"),
AssessmentQuestion(id="nl-c2-005",skill="grammar",difficulty="C2",question="Welke formulering drukt epistemische voorzichtigheid uit?",options=["Het kan niet worden uitgesloten dat andere factoren een rol spelen.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],correct="Het kan niet worden uitgesloten dat andere factoren een rol spelen.",grammar_slug="epistemic-modality"),
AssessmentQuestion(id="nl-c2-006",skill="vocabulary",difficulty="C2",question="Wat betekent 'dubbelzinnig'?",options=["vatbaar voor meer dan één interpretatie","volkomen duidelijk","zeer kort","gemakkelijk meetbaar"],correct="vatbaar voor meer dan één interpretatie"),
AssessmentQuestion(id="nl-c2-007",skill="reading",difficulty="C2",question="Lees: 'Het argument is overtuigend, mits de onderliggende aanname klopt.' Waarvan hangt de beoordeling af?",options=["Of de onderliggende aanname klopt.","Of het argument kort is.","Of de tekst informeel is.","Of de gegevens oud zijn."],correct="Of de onderliggende aanname klopt."),
AssessmentQuestion(id="nl-c2-008",skill="grammar",difficulty="C2",question="Kies de meest precieze academische formulering.",options=["De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.","De resultaten laten altijd een generalisatie toe zonder gegevens.","De resultaten laten geen generaliseren toe zonder aanvullende.","De resultaten laten een zekere generalisatie toe zonder analyse."],correct="De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.",grammar_slug="academic-style")






































AssessmentQuestion(id="nl-a2-009",skill="grammar",difficulty="A2",question="Kies de juiste voltooide tijd.",options=["Ik heb gegeten.","Ik heb eten.","Ik heb at.","Ik eten heb."],correct="Ik heb gegeten.",grammar_slug="voltooide-tijd"),
AssessmentQuestion(id="nl-a2-010",skill="vocabulary",difficulty="A2",question="Wat betekent 'vertraging'?",options=["iets dat later komt dan gepland","een reservering","een adres","een betaling"],correct="iets dat later komt dan gepland"),
AssessmentQuestion(id="nl-a2-011",skill="reading",difficulty="A2",question="Lees: 'De winkel sluit om zes uur.' Wanneer sluit de winkel?",options=["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],correct="Om zes uur."),
AssessmentQuestion(id="nl-a2-012",skill="grammar",difficulty="A2",question="Kies de juiste zin.",options=["Ik woon in Nederland.","Ik woon op Nederland.","Ik woon naar Nederland.","Ik woon bij Nederland."],correct="Ik woon in Nederland.",grammar_slug="voorzetsels"),
AssessmentQuestion(id="nl-b1-009",skill="grammar",difficulty="B1",question="Kies de juiste betrekkelijke bijzin.",options=["Dit is het boek dat ik heb gekocht.","Dit is het boek dat ik gekocht.","Dit is het boek die ik heb gekocht.","Dit is het boek dat heb ik gekocht."],correct="Dit is het boek dat ik heb gekocht.",grammar_slug="betrekkelijke-bijzin"),
AssessmentQuestion(id="nl-b1-010",skill="vocabulary",difficulty="B1",question="Wat betekent 'uitdaging'?",options=["iets dat inspanning vraagt","een beloning","een vakantie","een adres"],correct="iets dat inspanning vraagt"),
AssessmentQuestion(id="nl-b1-011",skill="reading",difficulty="B1",question="Lees: 'De vergadering werd verplaatst omdat de directeur ziek was.' Waarom werd de vergadering verplaatst?",options=["Omdat de directeur ziek was.","Omdat het kantoor gesloten was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],correct="Omdat de directeur ziek was."),
AssessmentQuestion(id="nl-b1-012",skill="grammar",difficulty="B1",question="Kies de juiste woordvolgorde.",options=["Gisteren kocht ik een nieuwe computer.","Gisteren ik kocht een nieuwe computer.","Gisteren kocht een nieuwe computer ik.","Gisteren een nieuwe computer kocht ik."],correct="Gisteren kocht ik een nieuwe computer.",grammar_slug="woordvolgorde"),
AssessmentQuestion(id="nl-b2-009",skill="grammar",difficulty="B2",question="Kies de juiste toegevende bijzin.",options=["Hoewel het regende, gingen we wandelen.","Hoewel het regende, we gingen wandelen.","Hoewel regende het, gingen we wandelen.","Hoewel het regende, we wandelen gingen."],correct="Hoewel het regende, gingen we wandelen.",grammar_slug="toegevende-bijzin"),
AssessmentQuestion(id="nl-b2-010",skill="vocabulary",difficulty="B2",question="Wat betekent 'voorspellen'?",options=["inschatten wat er zal gebeuren","iets uit het verleden uitleggen","een regel veranderen","een afspraak annuleren"],correct="inschatten wat er zal gebeuren"),
AssessmentQuestion(id="nl-b2-011",skill="reading",difficulty="B2",question="Lees: 'De resultaten tonen een duidelijke tendens, maar moeten voorzichtig worden geïnterpreteerd.' Wat wordt aanbevolen?",options=["Een voorzichtige interpretatie.","De resultaten negeren.","Alle resultaten veranderen.","Het onderzoek onmiddellijk stoppen."],correct="Een voorzichtige interpretatie."),
AssessmentQuestion(id="nl-b2-012",skill="grammar",difficulty="B2",question="Kies de juiste indirecte vraag.",options=["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],correct="Ik weet niet wanneer de vergadering begint.",grammar_slug="indirecte-vraag"),












































































AssessmentQuestion(id="nl-c1-009",skill="grammar",difficulty="C1",question="Kies de meest precieze academische formulering.",options=["De resultaten wijzen erop dat het effect beperkt is.","De resultaten wijzen dat het effect beperkt is.","De resultaten wijzen erop het effect dat beperkt is.","De resultaten wijst erop dat het effect beperkt is."],correct="De resultaten wijzen erop dat het effect beperkt is.",grammar_slug="academische-taal"),
AssessmentQuestion(id="nl-c1-010",skill="vocabulary",difficulty="C1",question="Wat betekent 'wezenlijk' in een academische tekst?",options=["belangrijk of fundamenteel","toevallig","tijdelijk","informeel"],correct="belangrijk of fundamenteel"),
AssessmentQuestion(id="nl-c1-011",skill="reading",difficulty="C1",question="Lees: 'Correlatie bewijst op zichzelf geen oorzakelijk verband.' Wat bewijst correlatie niet?",options=["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens bestaan.","Dat variabelen samenhangen.","Dat er een analyse is uitgevoerd."],correct="Dat het ene verschijnsel het andere veroorzaakt."),
AssessmentQuestion(id="nl-c1-012",skill="grammar",difficulty="C1",question="Kies de correcte passieve constructie.",options=["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek uitgevoerd werd in drie fasen.","Het onderzoek werd drie fasen uitgevoerd."],correct="Het onderzoek werd in drie fasen uitgevoerd.",grammar_slug="passieve-constructie"),
AssessmentQuestion(id="nl-c2-009",skill="grammar",difficulty="C2",question="Welke formulering drukt epistemische voorzichtigheid uit?",options=["Het kan niet worden uitgesloten dat andere factoren een rol spelen.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],correct="Het kan niet worden uitgesloten dat andere factoren een rol spelen.",grammar_slug="epistemische-modaliteit"),
AssessmentQuestion(id="nl-c2-010",skill="vocabulary",difficulty="C2",question="Wat betekent 'dubbelzinnig'?",options=["voor meerdere interpretaties vatbaar","volkomen duidelijk","zeer kort","gemakkelijk meetbaar"],correct="voor meerdere interpretaties vatbaar"),
AssessmentQuestion(id="nl-c2-011",skill="reading",difficulty="C2",question="Lees: 'Het argument is overtuigend, mits de onderliggende aanname klopt.' Waarvan hangt de beoordeling af?",options=["Of de onderliggende aanname klopt.","Of het argument kort is.","Of de tekst informeel is.","Of de gegevens oud zijn."],correct="Of de onderliggende aanname klopt."),
AssessmentQuestion(id="nl-c2-012",skill="grammar",difficulty="C2",question="Kies de meest precieze academische formulering.",options=["De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.","De resultaten laten altijd generalisatie toe zonder gegevens.","De resultaten laten geen generalisatie zonder aanvullende.","De resultaten laten een zekere generalisatie toe zonder analyse."],correct="De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.",grammar_slug="academische-formulering")




















    AssessmentQuestion(id="nl-a1-026",skill="vocabulary",difficulty="A1",question="Wat betekent 'appel'?",options=["een fruitsoort","een voertuig","een gebouw","een meubel"],correct="een fruitsoort"),
    AssessmentQuestion(id="nl-a1-027",skill="reading",difficulty="A1",question="Lees: 'Sara woont in Utrecht.' Waar woont Sara?",options=["In Utrecht.","In Rotterdam.","In Groningen.","In Leiden."],correct="In Utrecht."),
    AssessmentQuestion(id="nl-a1-028",skill="grammar",difficulty="A1",question="Welke zin is correct?",options=["Hij heeft een fiets.","Hij heeft een fietsje zijn.","Hij hebben een fiets.","Hij heeft een fietsen."],correct="Hij heeft een fiets."),
    AssessmentQuestion(id="nl-a1-029",skill="vocabulary",difficulty="A1",question="Wat betekent 'avond'?",options=["het einde van de dag","het begin van de week","een voertuig","een beroep"],correct="het einde van de dag"),
    AssessmentQuestion(id="nl-a1-030",skill="grammar",difficulty="A1",question="Kies het juiste lidwoord: '___ huis is groot.'",options=["Het","De","Een","Die"],correct="Het"),
    AssessmentQuestion(id="nl-a1-031",skill="reading",difficulty="A1",question="Lees: 'Tom drinkt elke ochtend koffie.' Wat drinkt Tom?",options=["Koffie.","Thee.","Water.","Melk."],correct="Koffie."),
    AssessmentQuestion(id="nl-a1-032",skill="grammar",difficulty="A1",question="Welke zin is negatief?",options=["Ik begrijp het niet.","Ik begrijp het.","Ik begreep het gisteren.","Ik wil het begrijpen."],correct="Ik begrijp het niet."),
    AssessmentQuestion(id="nl-a1-033",skill="vocabulary",difficulty="A1",question="Wat is 'brood'?",options=["een voedingsmiddel","een gebouw","een kledingstuk","een vervoermiddel"],correct="een voedingsmiddel"),
    AssessmentQuestion(id="nl-a1-034",skill="grammar",difficulty="A1",question="Kies de juiste vorm: 'Wij ___ in Amsterdam.'",options=["wonen","woont","woon","won"],correct="wonen"),
    AssessmentQuestion(id="nl-a1-035",skill="reading",difficulty="A1",question="Lees: 'De les begint om negen uur.' Hoe laat begint de les?",options=["Om acht uur.","Om negen uur.","Om tien uur.","Om elf uur."],correct="Om negen uur."),
    AssessmentQuestion(id="nl-a1-036",skill="vocabulary",difficulty="A1",question="Wat betekent 'vriend'?",options=["iemand die je goed kent en aardig vindt","een gebouw","een voertuig","een afspraak"],correct="iemand die je goed kent en aardig vindt"),
    AssessmentQuestion(id="nl-a1-037",skill="grammar",difficulty="A1",question="Welke zin gebruikt 'zijn' correct?",options=["Zij zijn thuis.","Zij is thuis.","Zij ben thuis.","Zij bent thuis."],correct="Zij zijn thuis."),
    AssessmentQuestion(id="nl-a1-038",skill="vocabulary",difficulty="A1",question="Waar koop je brood?",options=["Bij de bakker.","Bij de dokter.","Op het station.","In de bibliotheek."],correct="Bij de bakker."),
    AssessmentQuestion(id="nl-a1-039",skill="reading",difficulty="A1",question="Lees: 'Jan werkt vandaag niet.' Wat doet Jan vandaag?",options=["Hij werkt niet.","Hij werkt thuis.","Hij studeert.","Hij reist."],correct="Hij werkt niet."),
    AssessmentQuestion(id="nl-a1-040",skill="grammar",difficulty="A1",question="Welke zin is correct?",options=["Ik spreek Nederlands.","Ik spreekt Nederlands.","Ik spreken Nederlands.","Ik Nederlands spreek."],correct="Ik spreek Nederlands."),
    AssessmentQuestion(id="nl-a1-041",skill="vocabulary",difficulty="A1",question="Wat betekent 'water'?",options=["een drank","een beroep","een plaats","een kledingstuk"],correct="een drank"),
    AssessmentQuestion(id="nl-a1-042",skill="grammar",difficulty="A1",question="Kies de juiste vorm: 'Jij ___ Nederlands.'",options=["spreekt","spreek","spreken","sprak"],correct="spreekt"),
    AssessmentQuestion(id="nl-a1-043",skill="reading",difficulty="A1",question="Lees: 'De winkel is naast de school.' Waar is de winkel?",options=["Naast de school.","Achter het station.","In het ziekenhuis.","Onder het huis."],correct="Naast de school."),
    AssessmentQuestion(id="nl-a1-044",skill="vocabulary",difficulty="A1",question="Wat betekent 'dank je'?",options=["een manier om iemand te bedanken","een vraag naar de tijd","een afscheid","een plaatsaanduiding"],correct="een manier om iemand te bedanken"),

    AssessmentQuestion(id="nl-a1-045",skill="grammar",difficulty="A1",question="Welke zin is correct?",options=["Wij gaan naar school.","Wij gaat naar school.","Wij gaan naar scholen gisteren.","Wij naar school gaan."],correct="Wij gaan naar school."),
    AssessmentQuestion(id="nl-a1-046",skill="vocabulary",difficulty="A1",question="Wat betekent 'stoel'?",options=["iets waarop je kunt zitten","iets waarmee je reist","een soort eten","een gebouw"],correct="iets waarop je kunt zitten"),
    AssessmentQuestion(id="nl-a1-047",skill="reading",difficulty="A1",question="Lees: 'Mila heeft twee zussen.' Hoeveel zussen heeft Mila?",options=["Eén.","Twee.","Drie.","Vier."],correct="Twee."),
    AssessmentQuestion(id="nl-a1-048",skill="grammar",difficulty="A1",question="Kies de juiste vorm: 'Hij ___ in Den Haag.'",options=["woont","woon","wonen","woonde morgen"],correct="woont"),
    AssessmentQuestion(id="nl-a2-029",skill="grammar",difficulty="A2",question="Welke zin staat in de verleden tijd?",options=["Gisteren werkte ik thuis.","Gisteren werk ik thuis.","Gisteren zal ik thuis werken.","Gisteren thuis werken."],correct="Gisteren werkte ik thuis."),
    AssessmentQuestion(id="nl-a2-030",skill="vocabulary",difficulty="A2",question="Wat betekent 'vertraging'?",options=["iets komt later dan gepland","een reservering","een adres","een betaling"],correct="iets komt later dan gepland"),
    AssessmentQuestion(id="nl-a2-031",skill="reading",difficulty="A2",question="Lees: 'De trein vertrekt om half acht.' Wanneer vertrekt de trein?",options=["Om 07:00.","Om 07:30.","Om 08:00.","Om 08:30."],correct="Om 07:30."),
    AssessmentQuestion(id="nl-a2-032",skill="grammar",difficulty="A2",question="Welke zin gebruikt 'moeten' correct?",options=["Ik moet morgen werken.","Ik moet morgen werk.","Ik moeten morgen werken.","Ik moet morgen werkte."],correct="Ik moet morgen werken."),
    AssessmentQuestion(id="nl-b1-029",skill="grammar",difficulty="B1",question="Welke voorwaardelijke zin is correct?",options=["Als ik tijd had, zou ik reizen.","Als ik tijd heb, zou ik gisteren reizen.","Als ik tijd had, reisde ik morgen.","Als ik tijd hebben, zou ik reizen."],correct="Als ik tijd had, zou ik reizen."),
    AssessmentQuestion(id="nl-b1-030",skill="vocabulary",difficulty="B1",question="Wat betekent 'ervaring'?",options=["kennis uit eerdere gebeurtenissen","een ticket","een gebouw","een afspraak"],correct="kennis uit eerdere gebeurtenissen"),
    AssessmentQuestion(id="nl-b1-031",skill="reading",difficulty="B1",question="Lees: 'De vergadering werd uitgesteld omdat de directeur ziek was.' Waarom werd de vergadering uitgesteld?",options=["Omdat de directeur ziek was.","Omdat de zaal gesloten was.","Omdat de trein vertraging had.","Omdat het vakantie was."],correct="Omdat de directeur ziek was."),
    AssessmentQuestion(id="nl-b1-032",skill="grammar",difficulty="B1",question="Welke relatieve zin is correct?",options=["Dit is het boek dat ik heb gekocht.","Dit is het boek dat ik gekocht heb het.","Dit is het boek die ik heb gekocht.","Dit is het boek dat heb ik gekocht."],correct="Dit is het boek dat ik heb gekocht."),
    AssessmentQuestion(id="nl-b2-029",skill="grammar",difficulty="B2",question="Welke zin drukt een tegenstelling uit?",options=["Hoewel het regende, gingen we wandelen.","Omdat het regende, gingen we wandelen.","Zodra het regende, gingen we wandelen.","Als het regende, gingen we gisteren wandelen."],correct="Hoewel het regende, gingen we wandelen."),
    AssessmentQuestion(id="nl-b2-030",skill="vocabulary",difficulty="B2",question="Wat betekent 'voorspellen'?",options=["zeggen wat waarschijnlijk zal gebeuren","iets uit het verleden verklaren","een regel veranderen","een afspraak annuleren"],correct="zeggen wat waarschijnlijk zal gebeuren"),
    AssessmentQuestion(id="nl-b2-031",skill="reading",difficulty="B2",question="Lees: 'De resultaten wijzen op verbetering, maar verdere analyse is nodig.' Wat is nodig?",options=["Verdere analyse.","Geen onderzoek meer.","Een nieuwe afspraak.","Een andere locatie."],correct="Verdere analyse."),
    AssessmentQuestion(id="nl-b2-032",skill="grammar",difficulty="B2",question="Welke indirecte vraag is correct?",options=["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],correct="Ik weet niet wanneer de vergadering begint."),
    AssessmentQuestion(id="nl-c1-029",skill="grammar",difficulty="C1",question="Welke formulering past het best in een academische tekst?",options=["De resultaten suggereren dat het effect beperkt is.","De resultaten suggereren het effect dat beperkt is.","De resultaten suggereert dat het effect beperkt zijn.","De resultaten suggereren dat effect beperkt."],correct="De resultaten suggereren dat het effect beperkt is."),
    AssessmentQuestion(id="nl-c1-030",skill="vocabulary",difficulty="C1",question="Wat betekent 'wezenlijk'?",options=["belangrijk of fundamenteel","toevallig","tijdelijk","informeel"],correct="belangrijk of fundamenteel"),
    AssessmentQuestion(id="nl-c1-031",skill="reading",difficulty="C1",question="Lees: 'Correlatie bewijst op zichzelf geen oorzakelijk verband.' Wat wordt niet bewezen?",options=["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens zijn.","Dat variabelen samenhangen.","Dat er analyse is uitgevoerd."],correct="Dat het ene verschijnsel het andere veroorzaakt."),
    AssessmentQuestion(id="nl-c1-032",skill="grammar",difficulty="C1",question="Welke passieve constructie is correct?",options=["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek uitgevoerd werd in drie fasen.","Het onderzoek werd uitvoeren in drie fasen."],correct="Het onderzoek werd in drie fasen uitgevoerd."),
    AssessmentQuestion(id="nl-c2-029",skill="grammar",difficulty="C2",question="Welke formulering toont epistemische voorzichtigheid?",options=["Het valt niet uit te sluiten dat andere factoren een rol spelen.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],correct="Het valt niet uit te sluiten dat andere factoren een rol spelen."),
    AssessmentQuestion(id="nl-c2-030",skill="vocabulary",difficulty="C2",question="Wat betekent 'dubbelzinnig'?",options=["vatbaar voor meer dan één interpretatie","volledig eenduidig","zeer kort","gemakkelijk meetbaar"],correct="vatbaar voor meer dan één interpretatie"),
    AssessmentQuestion(id="nl-c2-031",skill="reading",difficulty="C2",question="Lees: 'Het argument is overtuigend, mits de onderliggende aanname klopt.' Waarvan hangt de beoordeling af?",options=["Of de onderliggende aanname klopt.","Of het argument kort is.","Of de tekst informeel is.","Of de gegevens oud zijn."],correct="Of de onderliggende aanname klopt."),
    AssessmentQuestion(id="nl-c2-032",skill="grammar",difficulty="C2",question="Welke academische formulering is het meest precies?",options=["De resultaten laten geen eenduidige generalisatie toe zonder aanvullende gegevens.","De resultaten laten altijd generalisatie toe zonder gegevens.","De resultaten laten geen generaliseren zonder aanvullende toe.","De resultaten laten een zekere generalisatie toe zonder analyse."],correct="De resultaten laten geen eenduidige generalisatie toe zonder aanvullende gegevens.")
AssessmentQuestion("nl-a1-257","grammar","A1","Kies de juiste vraag.",["Waar woon je?","Waar je woont?","Woon waar je?","Waar wonen?"],"Waar woon je?"),
AssessmentQuestion("nl-a1-258","vocabulary","A1","Wat betekent 'appel'?",["een vrucht","een voertuig","een gebouw","een meubel"],"een vrucht"),
AssessmentQuestion("nl-a1-259","reading","A1","Lees: 'Sofie woont in Utrecht.' Waar woont Sofie?",["In Utrecht.","In Rotterdam.","In Groningen.","In Eindhoven."],"In Utrecht."),
AssessmentQuestion("nl-a1-260","grammar","A1","Kies de juiste vorm.",["Zij heeft een auto.","Zij heeft een auto's.","Zij hebben een auto.","Zij heeft een autoo."],"Zij heeft een auto."),
AssessmentQuestion("nl-a2-261","grammar","A2","Kies de juiste verleden tijd.",["Gisteren werkte ik thuis.","Gisteren werk ik thuis.","Gisteren werken ik thuis.","Gisteren zal ik thuis werken."],"Gisteren werkte ik thuis."),
AssessmentQuestion("nl-a2-262","vocabulary","A2","Wat betekent 'vertraging'?",["iets dat later komt dan gepland","een reservering","een adres","een betaling"],"iets dat later komt dan gepland"),
AssessmentQuestion("nl-a2-263","reading","A2","Lees: 'De winkel sluit om zes uur.' Wanneer sluit de winkel?",["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],"Om zes uur."),
AssessmentQuestion("nl-a2-264","grammar","A2","Kies de juiste voorzetselcombinatie.",["Ik woon in Nederland.","Ik woon op Nederland.","Ik woon naar Nederland.","Ik woon bij Nederland."],"Ik woon in Nederland."),
AssessmentQuestion("nl-b1-265","grammar","B1","Kies de juiste bijzin.",["Ik weet dat hij morgen komt.","Ik weet dat hij morgen komen.","Ik weet hij dat morgen komt.","Ik weet dat morgen hij komt."],"Ik weet dat hij morgen komt."),
AssessmentQuestion("nl-b1-266","vocabulary","B1","Wat betekent 'uitdaging'?",["iets dat inspanning vraagt","een beloning","een vakantie","een adres"],"iets dat inspanning vraagt"),
AssessmentQuestion("nl-b1-267","reading","B1","Lees: 'De vergadering werd verplaatst omdat de directeur ziek was.' Waarom werd de vergadering verplaatst?",["Omdat de directeur ziek was.","Omdat het kantoor gesloten was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],"Omdat de directeur ziek was."),
AssessmentQuestion("nl-b1-268","grammar","B1","Kies de juiste woordvolgorde.",["Gisteren kocht ik een nieuwe computer.","Gisteren ik kocht een nieuwe computer.","Gisteren kocht een nieuwe computer ik.","Gisteren een nieuwe computer kocht ik."],"Gisteren kocht ik een nieuwe computer."),
AssessmentQuestion("nl-b2-269","grammar","B2","Kies de juiste concessieve zin.",["Hoewel het regende, gingen we wandelen.","Hoewel het regende, we gingen wandelen.","Hoewel regende het, gingen we wandelen.","Hoewel het regende, we wandelen gingen."],"Hoewel het regende, gingen we wandelen."),
AssessmentQuestion("nl-b2-270","vocabulary","B2","Wat betekent 'voorspellen'?",["zeggen wat waarschijnlijk zal gebeuren","iets uit het verleden uitleggen","een regel veranderen","een afspraak annuleren"],"zeggen wat waarschijnlijk zal gebeuren"),
AssessmentQuestion("nl-b2-271","reading","B2","Lees: 'De resultaten tonen een duidelijke trend, maar moeten voorzichtig worden geïnterpreteerd.' Wat wordt aanbevolen?",["De resultaten voorzichtig interpreteren.","De resultaten negeren.","Alle resultaten veranderen.","Het onderzoek meteen stoppen."],"De resultaten voorzichtig interpreteren."),
AssessmentQuestion("nl-b2-272","grammar","B2","Kies de juiste indirecte vraag.",["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],"Ik weet niet wanneer de vergadering begint."),
AssessmentQuestion("nl-c1-273","grammar","C1","Kies de meest precieze academische formulering.",["De resultaten wijzen erop dat het effect beperkt is.","De resultaten wijzen dat het effect beperkt is.","De resultaten wijst erop dat het effect beperkt is.","De resultaten wijzen erop het effect dat beperkt is."],"De resultaten wijzen erop dat het effect beperkt is."),
AssessmentQuestion("nl-c1-274","vocabulary","C1","Wat betekent 'wezenlijk' in een academische tekst?",["belangrijk of significant","toevallig","tijdelijk","informeel"],"belangrijk of significant"),
AssessmentQuestion("nl-c1-275","reading","C1","Lees: 'Correlatie bewijst op zichzelf geen causaal verband.' Wat bewijst correlatie niet?",["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens zijn.","Dat variabelen samenhangen.","Dat er een analyse is uitgevoerd."],"Dat het ene verschijnsel het andere veroorzaakt."),
AssessmentQuestion("nl-c1-276","grammar","C1","Kies de juiste passieve constructie.",["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek uitgevoerd werd in drie fasen.","Het onderzoek werden in drie fasen uitgevoerd."],"Het onderzoek werd in drie fasen uitgevoerd."),
AssessmentQuestion("nl-c2-277","grammar","C2","Welke formulering drukt wetenschappelijke voorzichtigheid uit?",["Het kan niet worden uitgesloten dat andere factoren een rol spelen.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],"Het kan niet worden uitgesloten dat andere factoren een rol spelen."),
AssessmentQuestion("nl-c2-278","vocabulary","C2","Wat betekent 'dubbelzinnig'?",["op meer dan één manier te interpreteren","volledig eenduidig","zeer kort","gemakkelijk te meten"],"op meer dan één manier te interpreteren"),
AssessmentQuestion("nl-c2-279","reading","C2","Lees: 'Het argument is overtuigend, mits de onderliggende aanname klopt.' Waarvan hangt de beoordeling af?",["Van het feit dat de onderliggende aanname klopt.","Van de lengte van de tekst.","Van een informele stijl.","Van de ouderdom van de gegevens."],"Van het feit dat de onderliggende aanname klopt."),
AssessmentQuestion("nl-c2-280","grammar","C2","Kies de meest precieze academische formulering.",["De resultaten laten geen eenduidige generalisatie toe zonder aanvullende gegevens.","De resultaten laten altijd generalisatie toe zonder gegevens.","De resultaten laten geen generaliseren toe zonder aanvullende.","De resultaten laten een zekere generalisatie toe zonder analyse."],"De resultaten laten geen eenduidige generalisatie toe zonder aanvullende gegevens.")





















































































AssessmentQuestion(id="nl-a1-013",skill="vocabulary",difficulty="A1",question="Wat betekent 'avond'?",options=["het einde van de dag","het begin van de week","een vervoermiddel","een beroep"],correct="het einde van de dag"),








]


AssessmentQuestion(id="nl-a2-013",skill="grammar",difficulty="A2",question="Welke zin gebruikt 'omdat' correct?",options=["Ik blijf thuis omdat ik ziek ben.","Ik blijf thuis omdat ben ik ziek.","Ik blijf thuis omdat ik ben ziek.","Ik blijf thuis omdat ziek ik ben."],correct="Ik blijf thuis omdat ik ziek ben."),
AssessmentQuestion(id="nl-a2-014",skill="vocabulary",difficulty="A2",question="Waar koop je medicijnen?",options=["Bij de apotheek.","Op het station.","In de bibliotheek.","In het hotel."],correct="Bij de apotheek."),
AssessmentQuestion(id="nl-a2-015",skill="reading",difficulty="A2",question="Lees: 'Lisa neemt de bus naar school.' Waar gaat Lisa naartoe?",options=["Naar school.","Naar het ziekenhuis.","Naar het station.","Naar huis."],correct="Naar school."),
AssessmentQuestion(id="nl-a2-016",skill="grammar",difficulty="A2",question="Kies de juiste voorzetselgroep.",options=["Ik woon in Nederland.","Ik woon op Nederland.","Ik woon aan Nederland.","Ik woon naar Nederland."],correct="Ik woon in Nederland."),








    AssessmentQuestion(id="nl-a2-021",skill="grammar",difficulty="A2",question="Welke zin staat in de verleden tijd?",options=["Gisteren ging ik naar de markt.","Gisteren ga ik naar de markt.","Gisteren zal ik naar de markt gaan.","Gisteren gaan ik naar de markt."],correct="Gisteren ging ik naar de markt."),
    AssessmentQuestion(id="nl-a2-022",skill="vocabulary",difficulty="A2",question="Wat betekent 'vertraging'?",options=["iets komt later dan gepland","een gemaakte afspraak","een betaling","een adres"],correct="iets komt later dan gepland"),
    AssessmentQuestion(id="nl-a2-023",skill="reading",difficulty="A2",question="Lees: 'De winkel sluit om zes uur.' Wanneer sluit de winkel?",options=["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],correct="Om zes uur."),
    AssessmentQuestion(id="nl-a2-024",skill="grammar",difficulty="A2",question="Kies de juiste voorzetselcombinatie.",options=["Ik woon in Nederland.","Ik woon op Nederland.","Ik woon naar Nederland.","Ik woon bij Nederland."],correct="Ik woon in Nederland."),
    AssessmentQuestion(id="nl-a2-025",skill="grammar",difficulty="A2",question="Welke zin met 'moeten' is correct?",options=["Ik moet werken.","Ik moet werkt.","Ik moet gewerkt.","Ik moet werk."],correct="Ik moet werken."),
    AssessmentQuestion(id="nl-a2-026",skill="vocabulary",difficulty="A2",question="Wat is een 'afspraak'?",options=["een afgesproken moment","een vervoermiddel","een gebouw","een maaltijd"],correct="een afgesproken moment"),
    AssessmentQuestion(id="nl-a2-027",skill="reading",difficulty="A2",question="Lees: 'Sara gaat na haar werk naar de apotheek.' Waar gaat Sara na haar werk naartoe?",options=["Naar de apotheek.","Naar het station.","Naar school.","Naar het hotel."],correct="Naar de apotheek."),
    AssessmentQuestion(id="nl-a2-028",skill="grammar",difficulty="A2",question="Welke vraag is correct?",options=["Waar woon je?","Waar je woont?","Waar woon jij bent?","Waar wonen je?"],"correct="Waar woon je?"),
    AssessmentQuestion(id="nl-b1-017",skill="grammar",difficulty="B1",question="Welke voorwaardelijke zin is correct?",options=["Als ik tijd had, zou ik reizen.","Als ik tijd heb, zou ik gisteren reizen.","Als ik tijd had, ik reisde gisteren.","Als ik tijd heb, zou ik reisde."],correct="Als ik tijd had, zou ik reizen."),
    AssessmentQuestion(id="nl-b1-018",skill="vocabulary",difficulty="B1",question="Wat betekent 'uitdaging'?",options=["iets waarvoor inspanning nodig is","een beloning","een vakantie","een adres"],correct="iets waarvoor inspanning nodig is"),
    AssessmentQuestion(id="nl-b1-019",skill="reading",difficulty="B1",question="Lees: 'De vergadering werd uitgesteld omdat de directeur ziek was.' Waarom werd de vergadering uitgesteld?",options=["Omdat de directeur ziek was.","Omdat het kantoor gesloten was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],correct="Omdat de directeur ziek was."),
    AssessmentQuestion(id="nl-b1-020",skill="grammar",difficulty="B1",question="Welke betrekkelijke bijzin is correct?",options=["Dit is het boek dat ik gisteren kocht.","Dit is het boek die ik gisteren kocht.","Dit is het boek dat ik gisteren kopen.","Dit is het boek ik dat gisteren kocht."],correct="Dit is het boek dat ik gisteren kocht."),
    AssessmentQuestion(id="nl-b1-021",skill="grammar",difficulty="B1",question="Welke woordvolgorde is correct?",options=["Gisteren heb ik een nieuwe computer gekocht.","Gisteren ik heb een nieuwe computer gekocht.","Gisteren heb een nieuwe computer ik gekocht.","Gisteren een nieuwe computer heb ik gekocht."],correct="Gisteren heb ik een nieuwe computer gekocht."),
    AssessmentQuestion(id="nl-b1-022",skill="vocabulary",difficulty="B1",question="Wat betekent 'ervaring'?",options=["kennis uit eerdere gebeurtenissen","een reisbiljet","een gebouw","een afspraak"],correct="kennis uit eerdere gebeurtenissen"),
    AssessmentQuestion(id="nl-b1-023",skill="reading",difficulty="B1",question="Lees: 'Hoewel het regende, gingen we wandelen.' Wat deden we?",options=["We gingen wandelen.","We bleven thuis.","We gingen werken.","We gingen reizen."],correct="We gingen wandelen."),
    AssessmentQuestion(id="nl-b1-024",skill="grammar",difficulty="B1",question="Welke zin is correct?",options=["Ik weet dat hij morgen komt.","Ik weet dat morgen hij komt.","Ik weet hij dat morgen komt.","Ik weet dat hij morgen komen."],correct="Ik weet dat hij morgen komt."),
    AssessmentQuestion(id="nl-b2-017",skill="grammar",difficulty="B2",question="Welke zin drukt een tegenstelling uit?",options=["Hoewel het moeilijk was, gingen we door.","Omdat het moeilijk was, gingen we door.","Zodra het moeilijk was, gingen we door.","Als het moeilijk was, gingen we door."],correct="Hoewel het moeilijk was, gingen we door."),
    AssessmentQuestion(id="nl-b2-018",skill="vocabulary",difficulty="B2",question="Wat betekent 'voorspellen'?",options=["zeggen wat waarschijnlijk zal gebeuren","iets uit het verleden uitleggen","een regel veranderen","een afspraak annuleren"],correct="zeggen wat waarschijnlijk zal gebeuren"),
    AssessmentQuestion(id="nl-b2-019",skill="reading",difficulty="B2",question="Lees: 'De resultaten wijzen op een duidelijke trend, maar moeten voorzichtig worden geïnterpreteerd.' Wat wordt aanbevolen?",options=["De resultaten voorzichtig interpreteren.","De resultaten negeren.","Alle resultaten veranderen.","Het onderzoek stoppen."],correct="De resultaten voorzichtig interpreteren."),
    AssessmentQuestion(id="nl-b2-020",skill="grammar",difficulty="B2",question="Welke indirecte vraag is correct?",options=["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],correct="Ik weet niet wanneer de vergadering begint."),
    AssessmentQuestion(id="nl-b2-021",skill="grammar",difficulty="B2",question="Welke passieve zin is correct?",options=["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek werd uitgevoerd drie fasen.","Het onderzoek uitgevoerd werd in drie fasen."],correct="Het onderzoek werd in drie fasen uitgevoerd."),
    AssessmentQuestion(id="nl-b2-022",skill="vocabulary",difficulty="B2",question="Wat betekent 'invloed'?",options=["effect op iets","een reis","een woning","een begroting"],correct="effect op iets"),
    AssessmentQuestion(id="nl-b2-023",skill="reading",difficulty="B2",question="Lees: 'De gegevens zijn veelbelovend, maar aanvullend onderzoek is nodig.' Wat is nodig?",options=["Aanvullend onderzoek.","Minder gegevens.","Een nieuwe vergadering.","Een andere locatie."],correct="Aanvullend onderzoek."),
    AssessmentQuestion(id="nl-b2-024",skill="grammar",difficulty="B2",question="Welke formulering is correct?",options=["Ondanks de problemen werd het project voltooid.","Ondanks van de problemen werd het project voltooid.","Ondanks de problemen het project werd voltooid.","Ondanks de problemen werd voltooid het project."],correct="Ondanks de problemen werd het project voltooid."),
    AssessmentQuestion(id="nl-c1-017",skill="grammar",difficulty="C1",question="Welke formulering past bij academisch Nederlands?",options=["De resultaten suggereren dat het effect beperkt is.","De resultaten suggereren het effect dat beperkt is.","De resultaten suggereert dat het effect beperkt zijn.","De resultaten suggereren dat effect beperkt."],correct="De resultaten suggereren dat het effect beperkt is."),
    AssessmentQuestion(id="nl-c1-018",skill="vocabulary",difficulty="C1",question="Wat betekent 'wezenlijk'?",options=["belangrijk of fundamenteel","toevallig","tijdelijk","informeel"],correct="belangrijk of fundamenteel"),
    AssessmentQuestion(id="nl-c1-019",skill="reading",difficulty="C1",question="Lees: 'Correlatie impliceert op zichzelf geen causaal verband.' Wat wordt niet aangetoond?",options=["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens zijn.","Dat variabelen samenhangen.","Dat er een analyse is uitgevoerd."],correct="Dat het ene verschijnsel het andere veroorzaakt."),
    AssessmentQuestion(id="nl-c1-020",skill="grammar",difficulty="C1",question="Welke nominalisatie is correct?",options=["De evaluatie van de resultaten was uitgebreid.","De evalueren van de resultaten was uitgebreid.","De evaluatie de resultaten was uitgebreid.","De resultaten evaluatie was uitgebreid."],correct="De evaluatie van de resultaten was uitgebreid."),
    AssessmentQuestion(id="nl-c1-021",skill="grammar",difficulty="C1",question="Welke formulering is het meest genuanceerd?",options=["De bevindingen lijken erop te wijzen dat het effect beperkt is.","De bevindingen bewijzen absoluut alles.","De bevindingen tonen zonder twijfel elke oorzaak aan.","De bevindingen sluiten alle alternatieve verklaringen uit."],correct="De bevindingen lijken erop te wijzen dat het effect beperkt is."),
    AssessmentQuestion(id="nl-c1-022",skill="vocabulary",difficulty="C1",question="Wat betekent 'voorwaarde' in een argument?",options=["een vereiste waaraan moet worden voldaan","een conclusie","een emotie","een nieuwsbericht"],correct="een vereiste waaraan moet worden voldaan"),
    AssessmentQuestion(id="nl-c1-023",skill="reading",difficulty="C1",question="Lees: 'De methode is bruikbaar, mits de steekproef voldoende representatief is.' Waarvan hangt de bruikbaarheid af?",options=["Van een voldoende representatieve steekproef.","Van de lengte van het rapport.","Van de leeftijd van de onderzoekers.","Van de vormgeving."],correct="Van een voldoende representatieve steekproef."),
    AssessmentQuestion(id="nl-c1-024",skill="grammar",difficulty="C1",question="Welke passieve constructie is correct?",options=["Er werd een uitgebreide analyse uitgevoerd.","Er werd een uitgebreide analyse uitvoeren.","Er een uitgebreide analyse werd uitgevoerd.","Er werd uitgevoerd een uitgebreide analyse."],correct="Er werd een uitgebreide analyse uitgevoerd."),
    AssessmentQuestion(id="nl-c2-017",skill="grammar",difficulty="C2",question="Welke formulering drukt epistemische voorzichtigheid uit?",options=["Het valt niet uit te sluiten dat andere factoren een rol spelen.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],correct="Het valt niet uit te sluiten dat andere factoren een rol spelen."),
    AssessmentQuestion(id="nl-c2-018",skill="vocabulary",difficulty="C2",question="Wat betekent 'dubbelzinnig'?",options=["vatbaar voor meer dan één interpretatie","volledig eenduidig","zeer kort","gemakkelijk meetbaar"],correct="vatbaar voor meer dan één interpretatie"),
    AssessmentQuestion(id="nl-c2-019",skill="reading",difficulty="C2",question="Lees: 'De conclusie is overtuigend, mits de onderliggende aanname standhoudt.' Waarvan hangt de conclusie af?",options=["Van de geldigheid van de onderliggende aanname.","Van de lengte van de tekst.","Van een informele stijl.","Van de ouderdom van de gegevens."],correct="Van de geldigheid van de onderliggende aanname."),
    AssessmentQuestion(id="nl-c2-020",skill="grammar",difficulty="C2",question="Welke academische formulering is het meest precies?",options=["De resultaten laten geen eenduidige generalisatie toe zonder aanvullende gegevens.","De resultaten laten altijd generalisatie toe zonder gegevens.","De resultaten laten geen generaliseren toe zonder aanvullende.","De resultaten laten een zekere generalisatie toe zonder analyse."],correct="De resultaten laten geen eenduidige generalisatie toe zonder aanvullende gegevens."),
    AssessmentQuestion(id="nl-c2-021",skill="grammar",difficulty="C2",question="Welke formulering vermijdt een te sterke causale claim?",options=["De bevindingen wijzen op een verband, maar bewijzen geen causaliteit.","De bevindingen bewijzen altijd causaliteit.","De bevindingen bewijzen dat er geen andere factoren zijn.","De bevindingen maken verder onderzoek overbodig."],correct="De bevindingen wijzen op een verband, maar bewijzen geen causaliteit."),
    AssessmentQuestion(id="nl-c2-022",skill="vocabulary",difficulty="C2",question="Wat betekent 'nuanceren'?",options=["een bewering preciezer en minder absoluut maken","een tekst inkorten","een onderwerp veranderen","een conclusie herhalen"],correct="een bewering preciezer en minder absoluut maken"),
    AssessmentQuestion(id="nl-c2-023",skill="reading",difficulty="C2",question="Lees: 'De hypothese blijft houdbaar zolang de tegenvoorbeelden onvoldoende verklaringskracht hebben.' Wat betekent dit?",options=["De hypothese blijft voorlopig aannemelijk zolang tegenvoorbeelden haar niet overtuigend weerleggen.","De hypothese is definitief bewezen.","Tegenvoorbeelden zijn altijd irrelevant.","De hypothese hoeft niet meer onderzocht te worden."],"correct="De hypothese blijft voorlopig aannemelijk zolang tegenvoorbeelden haar niet overtuigend weerleggen."),
    AssessmentQuestion(id="nl-c2-024",skill="grammar",difficulty="C2",question="Welke zin is het meest idiomatisch en academisch?",options=["Ondanks de beperkingen kunnen de resultaten niet zonder meer worden verworpen.","Ondanks de beperkingen kunnen de resultaten niet zonder meer verwerpen.","Ondanks de beperkingen de resultaten kunnen niet worden verworpen.","Ondanks van de beperkingen kunnen de resultaten niet worden verworpen."],correct="Ondanks de beperkingen kunnen de resultaten niet zonder meer worden verworpen.")








AssessmentQuestion(id="nl-c1-013",skill="grammar",difficulty="C1",question="Kies de correcte formulering met een voorbehoud.",options=["Voor zover de gegevens reiken, lijkt de conclusie aannemelijk.","Voor zover de gegevens reikt, lijkt de conclusie aannemelijk.","Voor zover de gegevens reiken, de conclusie lijkt aannemelijk.","Voor zover de gegevens reiken, lijkt aannemelijk de conclusie."],correct="Voor zover de gegevens reiken, lijkt de conclusie aannemelijk."),
AssessmentQuestion(id="nl-c1-014",skill="vocabulary",difficulty="C1",question="Wat betekent 'aanzienlijk'?",options=["in belangrijke mate of vrij groot","zonder enige betekenis","slechts tijdelijk","op een informele manier"],correct="in belangrijke mate of vrij groot"),
AssessmentQuestion(id="nl-c1-015",skill="reading",difficulty="C1",question="Lees: 'De steekproef was niet representatief; de bevindingen moeten daarom terughoudend worden geïnterpreteerd.' Waarom is terughoudendheid nodig?",options=["Omdat de steekproef niet representatief was.","Omdat er geen bevindingen zijn.","Omdat het onderzoek nog niet begonnen is.","Omdat de resultaten volledig zeker zijn."],correct="Omdat de steekproef niet representatief was."),
AssessmentQuestion(id="nl-c1-016",skill="grammar",difficulty="C1",question="Kies de correcte samengestelde zin.",options=["Hoewel de methode beperkingen kent, levert zij bruikbare inzichten op.","Hoewel de methode beperkingen kent, zij levert bruikbare inzichten op.","Hoewel kent de methode beperkingen, levert zij bruikbare inzichten op.","Hoewel de methode beperkingen kent, levert bruikbare inzichten zij op."],correct="Hoewel de methode beperkingen kent, levert zij bruikbare inzichten op."),
AssessmentQuestion(id="nl-c1-017-r2",skill="vocabulary",difficulty="C1",question="Wat betekent 'onderbouwen'?",options=["met argumenten of bewijs ondersteunen","zonder uitleg afwijzen","een tekst inkorten","een afspraak verplaatsen"],correct="met argumenten of bewijs ondersteunen"),
AssessmentQuestion(id="nl-c1-018-r2",skill="reading",difficulty="C1",question="Welke conclusie is het meest voorzichtig?",options=["De resultaten lijken erop te wijzen dat er mogelijk een verband bestaat.","De resultaten bewijzen alle mogelijke verklaringen.","Er bestaat absoluut geen onzekerheid.","De gegevens zijn per definitie onjuist."],correct="De resultaten lijken erop te wijzen dat er mogelijk een verband bestaat."),
AssessmentQuestion(id="nl-c1-019-r2",skill="grammar",difficulty="C1",question="Kies de correcte vorm van de indirecte rede.",options=["De onderzoeker stelde dat de resultaten nader onderzoek vereisten.","De onderzoeker stelde dat de resultaten nader onderzoek vereist.","De onderzoeker stelde de resultaten dat nader onderzoek vereisten.","De onderzoeker stelde dat vereisten de resultaten nader onderzoek."],correct="De onderzoeker stelde dat de resultaten nader onderzoek vereisten."),
AssessmentQuestion(id="nl-c1-020-r2",skill="vocabulary",difficulty="C1",question="Wat betekent 'tegenstrijdig'?",options=["met elkaar in conflict of niet verenigbaar","volledig gelijk","tijdelijk beschikbaar","eenvoudig meetbaar"],correct="met elkaar in conflict of niet verenigbaar"),
AssessmentQuestion(id="nl-c1-021-r2",skill="reading",difficulty="C1",question="Lees: 'De analyse bevestigt de trend, maar verklaart niet waardoor deze is ontstaan.' Wat blijft onverklaard?",options=["De oorzaak van de trend.","Het bestaan van de trend.","De uitgevoerde analyse.","De gebruikte gegevens."],correct="De oorzaak van de trend."),
AssessmentQuestion(id="nl-c1-022-r2",skill="grammar",difficulty="C1",question="Kies de juiste betrekkelijke constructie.",options=["De theorie waarop het onderzoek is gebaseerd, wordt vaak toegepast.","De theorie waarop het onderzoek is gebaseerd wordt vaak toegepast?","De theorie waar het onderzoek op gebaseerd is, wordt vaak toegepast door het.","De theorie waarop is het onderzoek gebaseerd, wordt vaak toegepast."],correct="De theorie waarop het onderzoek is gebaseerd, wordt vaak toegepast."),
AssessmentQuestion(id="nl-c1-023-r2",skill="vocabulary",difficulty="C1",question="Wat betekent 'nuanceren'?",options=["een uitspraak verfijnen en minder absoluut maken","een uitspraak zonder bewijs herhalen","een onderwerp volledig vermijden","een tekst letterlijk vertalen"],correct="een uitspraak verfijnen en minder absoluut maken"),
AssessmentQuestion(id="nl-c1-024-r2",skill="reading",difficulty="C1",question="Welke formulering maakt onderscheid tussen samenhang en oorzaak?",options=["Er is een verband waargenomen, maar causaliteit is niet vastgesteld.","Het verband bewijst automatisch de oorzaak.","Elke samenhang is per definitie causaal.","De oorzaak staat los van alle waarnemingen."],correct="Er is een verband waargenomen, maar causaliteit is niet vastgesteld."),
AssessmentQuestion(id="nl-c2-009-r2",skill="grammar",difficulty="C2",question="Welke formulering drukt een noodzakelijke voorwaarde uit?",options=["Mits de uitgangspunten kloppen, is de gevolgtrekking verdedigbaar.","Omdat de uitgangspunten kloppen, is de gevolgtrekking onmogelijk.","Hoewel de uitgangspunten kloppen, mits de gevolgtrekking.","De uitgangspunten mits kloppen de gevolgtrekking is."],correct="Mits de uitgangspunten kloppen, is de gevolgtrekking verdedigbaar."),
AssessmentQuestion(id="nl-c2-010-r2",skill="vocabulary",difficulty="C2",question="Wat betekent 'weerlegbaar'?",options=["vatbaar voor weerlegging met argumenten of bewijs","onmogelijk om te onderzoeken","volledig onbetwist","zonder betekenis"],correct="vatbaar voor weerlegging met argumenten of bewijs"),
AssessmentQuestion(id="nl-c2-011-r2",skill="reading",difficulty="C2",question="Lees: 'De hypothese is consistent met de waarnemingen, maar alternatieve verklaringen blijven mogelijk.' Wat volgt hieruit?",options=["De waarnemingen sluiten alternatieve verklaringen niet uit.","De hypothese is definitief bewezen.","Alternatieve verklaringen zijn onmogelijk.","De waarnemingen zijn irrelevant."],correct="De waarnemingen sluiten alternatieve verklaringen niet uit."),
AssessmentQuestion(id="nl-c2-012-r2",skill="grammar",difficulty="C2",question="Kies de meest zorgvuldige formulering.",options=["Op grond van de beschikbare gegevens lijkt deze interpretatie het meest aannemelijk.","De gegevens bewijzen zonder enige twijfel elke interpretatie.","Deze interpretatie is waar ongeacht de gegevens.","Op grond de gegevens lijkt deze interpretatie meest aannemelijk."],correct="Op grond van de beschikbare gegevens lijkt deze interpretatie het meest aannemelijk."),
AssessmentQuestion(id="nl-c2-013",skill="vocabulary",difficulty="C2",question="Wat betekent 'vooronderstelling'?",options=["een impliciet uitgangspunt dat als gegeven wordt beschouwd","een conclusie die experimenteel bewezen is","een willekeurige woordkeuze","een formele begroeting"],correct="een impliciet uitgangspunt dat als gegeven wordt beschouwd"),
AssessmentQuestion(id="nl-c2-014",skill="reading",difficulty="C2",question="Welke uitspraak onderscheidt bewijs en aannemelijkheid?",options=["Een plausibele verklaring is niet noodzakelijk empirisch bewezen.","Alles wat plausibel is, is bewezen.","Bewijs en plausibiliteit zijn altijd identiek.","Een verklaring kan nooit aannemelijk zijn."],correct="Een plausibele verklaring is niet noodzakelijk empirisch bewezen."),
AssessmentQuestion(id="nl-c2-015",skill="grammar",difficulty="C2",question="Kies de correcte concessieve formulering.",options=["Hoe overtuigend het argument ook lijkt, de premissen moeten worden getoetst.","Hoe overtuigend het argument ook lijkt, de premissen moet worden getoetst.","Hoe overtuigend ook het argument lijkt, de premissen moeten getoetst worden?","Hoe overtuigend het argument ook lijkt, moeten de premissen getoetst."],correct="Hoe overtuigend het argument ook lijkt, de premissen moeten worden getoetst."),
AssessmentQuestion(id="nl-c2-016",skill="vocabulary",difficulty="C2",question="Wat betekent 'voorbehoud' in een betoog?",options=["een expliciete beperking of kanttekening","een definitieve bevestiging","een willekeurige herhaling","een informele begroeting"],correct="een expliciete beperking of kanttekening"),
AssessmentQuestion(id="nl-c2-017-r2",skill="reading",difficulty="C2",question="Lees: 'De redenering is geldig indien de premissen waar zijn; de waarheid van die premissen is echter afzonderlijk te beoordelen.' Wat wordt afzonderlijk beoordeeld?",options=["De waarheid van de premissen.","De grammatica van de tekst.","De lengte van de redenering.","De volgorde van de alinea's."],correct="De waarheid van de premissen."),
AssessmentQuestion(id="nl-c2-018-r2",skill="grammar",difficulty="C2",question="Kies de meest precieze formulering.",options=["De bevindingen rechtvaardigen geen verdergaande conclusie dan de gegevens toelaten.","De bevindingen rechtvaardigt geen verdergaande conclusie dan de gegevens toelaten.","De bevindingen rechtvaardigen een conclusie ongeacht de gegevens.","De bevindingen rechtvaardigen geen conclusie dan de gegevens toelaten."],correct="De bevindingen rechtvaardigen geen verdergaande conclusie dan de gegevens toelaten."),
AssessmentQuestion(id="nl-c2-019-r2",skill="vocabulary",difficulty="C2",question="Wat betekent 'impliceren'?",options=["indirect inhouden of met zich meebrengen","uitdrukkelijk ontkennen","letterlijk overschrijven","zonder verband herhalen"],correct="indirect inhouden of met zich meebrengen"),
AssessmentQuestion(id="nl-c2-020-r2",skill="reading",difficulty="C2",question="Lees: 'De bevindingen zijn robuust binnen deze steekproef, maar de externe validiteit is beperkt.' Wat is beperkt?",options=["De mogelijkheid om de bevindingen naar andere situaties te generaliseren.","De interne consistentie binnen de steekproef.","Het aantal waarnemingen in elk geval.","De nauwkeurigheid van de gebruikte termen."],correct="De mogelijkheid om de bevindingen naar andere situaties te generaliseren.")


    AssessmentQuestion(id="nl-a2-005-r2",skill="grammar",difficulty="A2",question="Kies de juiste voltooide tijd.",options=["Ik heb gisteren gewerkt.","Ik heb gisteren werken.","Ik gisteren heb gewerkt.","Ik heeft gisteren gewerkt."],correct="Ik heb gisteren gewerkt."),
    AssessmentQuestion(id="nl-a2-006-r2",skill="vocabulary",difficulty="A2",question="Wat betekent 'vertraging'?",options=["later aankomen dan gepland","een reservering","een adres","een betaling"],correct="later aankomen dan gepland"),
    AssessmentQuestion(id="nl-a2-007-r2",skill="reading",difficulty="A2",question="Lees: 'De winkel sluit om zes uur.' Hoe laat sluit de winkel?",options=["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],correct="Om zes uur."),
    AssessmentQuestion(id="nl-a2-008-r2",skill="grammar",difficulty="A2",question="Kies de juiste voorzetselcombinatie.",options=["Ik woon in Nederland.","Ik woon op Nederland.","Ik woon naar Nederland.","Ik woon aan Nederland."],correct="Ik woon in Nederland."),
    AssessmentQuestion(id="nl-b1-005-r2",skill="grammar",difficulty="B1",question="Kies de correcte betrekkelijke bijzin.",options=["Dit is het boek dat ik heb gekocht.","Dit is het boek die ik heb gekocht.","Dit is het boek dat ik gekocht.","Dit is het boek ik dat heb gekocht."],correct="Dit is het boek dat ik heb gekocht."),
    AssessmentQuestion(id="nl-b1-006-r2",skill="vocabulary",difficulty="B1",question="Wat betekent 'uitdaging'?",options=["iets waarvoor inspanning nodig is","een beloning","een vakantie","een adres"],correct="iets waarvoor inspanning nodig is"),
    AssessmentQuestion(id="nl-b1-007-r2",skill="reading",difficulty="B1",question="Lees: 'De vergadering werd verplaatst omdat de directeur ziek was.' Waarom werd de vergadering verplaatst?",options=["Omdat de directeur ziek was.","Omdat het kantoor dicht was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],correct="Omdat de directeur ziek was."),
    AssessmentQuestion(id="nl-b1-008-r2",skill="grammar",difficulty="B1",question="Kies de juiste woordvolgorde.",options=["Gisteren kocht ik een nieuwe computer.","Gisteren ik kocht een nieuwe computer.","Gisteren kocht een nieuwe computer ik.","Gisteren een nieuwe computer kocht ik."],correct="Gisteren kocht ik een nieuwe computer."),
    AssessmentQuestion(id="nl-b2-005-r2",skill="grammar",difficulty="B2",question="Kies de correcte concessieve zin.",options=["Hoewel het regende, gingen we wandelen.","Hoewel het regende, we gingen wandelen.","Hoewel regende het, gingen we wandelen.","Hoewel het regende, we wandelen gingen."],correct="Hoewel het regende, gingen we wandelen."),
    AssessmentQuestion(id="nl-b2-006-r2",skill="vocabulary",difficulty="B2",question="Wat betekent 'voorspellen'?",options=["inschatten wat er later zal gebeuren","iets uit het verleden verklaren","een regel veranderen","een afspraak annuleren"],correct="inschatten wat er later zal gebeuren"),
    AssessmentQuestion(id="nl-b2-007-r2",skill="reading",difficulty="B2",question="Lees: 'De resultaten wijzen op een duidelijke trend, maar moeten voorzichtig worden geïnterpreteerd.' Wat wordt aangeraden?",options=["De resultaten voorzichtig interpreteren.","De resultaten negeren.","Alle resultaten aanpassen.","Het onderzoek direct beëindigen."],correct="De resultaten voorzichtig interpreteren."),
    AssessmentQuestion(id="nl-b2-008-r2",skill="grammar",difficulty="B2",question="Kies de juiste indirecte vraag.",options=["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],correct="Ik weet niet wanneer de vergadering begint."),
    AssessmentQuestion(id="nl-c1-005-r2",skill="grammar",difficulty="C1",question="Kies de meest precieze academische formulering.",options=["De resultaten wijzen erop dat het effect beperkt is.","De resultaten wijzen dat het effect beperkt is.","De resultaten wijzen erop het effect beperkt is.","De resultaten wijst erop dat het effect beperkt is."],correct="De resultaten wijzen erop dat het effect beperkt is."),
    AssessmentQuestion(id="nl-c1-006-r2",skill="vocabulary",difficulty="C1",question="Wat betekent 'wezenlijk' in een academische tekst?",options=["belangrijk of fundamenteel","toevallig","tijdelijk","informeel"],correct="belangrijk of fundamenteel"),
    AssessmentQuestion(id="nl-c1-007-r2",skill="reading",difficulty="C1",question="Lees: 'Een correlatie bewijst op zichzelf geen causaal verband.' Wat bewijst de correlatie niet?",options=["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens bestaan.","Dat variabelen samenhangen.","Dat er een analyse is uitgevoerd."],correct="Dat het ene verschijnsel het andere veroorzaakt."),
    AssessmentQuestion(id="nl-c1-008-r2",skill="grammar",difficulty="C1",question="Kies de correcte passieve constructie.",options=["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werden in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek uitgevoerd werd in drie fasen."],correct="Het onderzoek werd in drie fasen uitgevoerd."),
    AssessmentQuestion(id="nl-c2-005-r2",skill="grammar",difficulty="C2",question="Welke formulering drukt academische voorzichtigheid uit?",options=["De invloed van andere factoren kan niet worden uitgesloten.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],correct="De invloed van andere factoren kan niet worden uitgesloten."),
    AssessmentQuestion(id="nl-c2-006-r2",skill="vocabulary",difficulty="C2",question="Wat betekent 'dubbelzinnig'?",options=["vatbaar voor meer dan één uitleg","volkomen duidelijk","zeer kort","gemakkelijk te meten"],correct="vatbaar voor meer dan één uitleg"),
    AssessmentQuestion(id="nl-c2-007-r2",skill="reading",difficulty="C2",question="Lees: 'De redenering is overtuigend, mits de onderliggende aanname klopt.' Waarvan hangt de beoordeling af?",options=["Of de onderliggende aanname klopt.","Of de tekst kort is.","Of de stijl informeel is.","Of de gegevens oud zijn."],correct="Of de onderliggende aanname klopt."),
    AssessmentQuestion(id="nl-c2-008-r2",skill="grammar",difficulty="C2",question="Kies de meest nauwkeurige academische formulering.",options=["De bevindingen rechtvaardigen geen stellige generalisatie zonder aanvullend bewijs.","De bevindingen rechtvaardigen altijd een generalisatie zonder bewijs.","De bevindingen rechtvaardigen geen generaliseren zonder aanvullend.","De bevindingen rechtvaardigen een stellige generalisatie ondanks ontbrekend bewijs."],correct="De bevindingen rechtvaardigen geen stellige generalisatie zonder aanvullend bewijs.")


    AssessmentQuestion(id="nl-a2-009x",skill="grammar",difficulty="A2",question="Kies de juiste voltooid tegenwoordige tijd.",options=["Ik heb gisteren gekookt.","Ik heb gisteren koken.","Ik gisteren heb gekookt.","Ik heb gisteren kook."],correct="Ik heb gisteren gekookt."),
    AssessmentQuestion(id="nl-a2-010x",skill="vocabulary",difficulty="A2",question="Wat betekent 'de afspraak verzetten'?",options=["een afspraak naar een ander moment verplaatsen","een afspraak bevestigen","een rekening betalen","een route beschrijven"],correct="een afspraak naar een ander moment verplaatsen"),
    AssessmentQuestion(id="nl-a2-011x",skill="reading",difficulty="A2",question="Lees: 'De apotheek sluit om zes uur.' Wanneer sluit de apotheek?",options=["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],correct="Om zes uur."),
    AssessmentQuestion(id="nl-a2-012x",skill="grammar",difficulty="A2",question="Kies de juiste bijzin.",options=["Ik blijf thuis omdat ik ziek ben.","Ik blijf thuis omdat ben ik ziek.","Ik blijf thuis omdat ik ben ziek.","Ik blijf thuis omdat ziek ik ben."],correct="Ik blijf thuis omdat ik ziek ben."),
    AssessmentQuestion(id="nl-a2-013x",skill="vocabulary",difficulty="A2",question="Wat betekent 'gezellig' in deze context?",options=["prettig en aangenaam","gevaarlijk","onmogelijk","haastig"],correct="prettig en aangenaam"),
    AssessmentQuestion(id="nl-a2-014x",skill="reading",difficulty="A2",question="Lees: 'Sofie neemt de bus omdat haar fiets kapot is.' Waarom neemt Sofie de bus?",options=["Omdat haar fiets kapot is.","Omdat de bus gratis is.","Omdat ze te vroeg is.","Omdat het regent."],correct="Omdat haar fiets kapot is."),
    AssessmentQuestion(id="nl-a2-015x",skill="grammar",difficulty="A2",question="Kies de correcte vergelijkende vorm.",options=["Deze tas is goedkoper dan die tas.","Deze tas is goedkoopst dan die tas.","Deze tas is goedkopere dan die tas.","Deze tas goedkoper is dan die tas."],correct="Deze tas is goedkoper dan die tas."),
    AssessmentQuestion(id="nl-a2-016x",skill="grammar",difficulty="A2",question="Kies de juiste scheidbare werkwoordsvorm.",options=["Ik sta om zeven uur op.","Ik opsta om zeven uur.","Ik sta op om zeven uur?","Ik op om zeven uur sta."],correct="Ik sta om zeven uur op."),
    AssessmentQuestion(id="nl-b1-009x",skill="grammar",difficulty="B1",question="Kies de correcte voorwaardelijke zin.",options=["Als ik meer tijd had, zou ik vaker lezen.","Als ik meer tijd heb, zou ik gisteren lezen.","Als ik had meer tijd, zou ik lezen.","Als ik meer tijd had, zal ik gisteren lezen."],correct="Als ik meer tijd had, zou ik vaker lezen."),
    AssessmentQuestion(id="nl-b1-010x",skill="vocabulary",difficulty="B1",question="Wat betekent 'de verantwoordelijkheid'?",options=["de plicht om ergens voor te zorgen","een vrije dag","een vervoersbewijs","een toevallige gebeurtenis"],correct="de plicht om ergens voor te zorgen"),
    AssessmentQuestion(id="nl-b1-011x",skill="reading",difficulty="B1",question="Lees: 'De vergadering werd uitgesteld omdat belangrijke stukken ontbraken.' Waarom werd de vergadering uitgesteld?",options=["Omdat belangrijke stukken ontbraken.","Omdat iedereen op tijd was.","Omdat de zaal te groot was.","Omdat de agenda kort was."],correct="Omdat belangrijke stukken ontbraken."),
    AssessmentQuestion(id="nl-b1-012x",skill="grammar",difficulty="B1",question="Kies de juiste betrekkelijke bijzin.",options=["De vrouw die naast mij woont, werkt hier.","De vrouw die naast mij woont werkt hier?","De vrouw naast mij die woont, werkt hier.","De vrouw die woont naast mij, werkt hier."],correct="De vrouw die naast mij woont, werkt hier."),
    AssessmentQuestion(id="nl-b1-013x",skill="vocabulary",difficulty="B1",question="Wat betekent 'de voorwaarde'?",options=["iets waaraan moet worden voldaan","een samenvatting","een uitnodiging","een hulpmiddel"],correct="iets waaraan moet worden voldaan"),
    AssessmentQuestion(id="nl-b1-014x",skill="reading",difficulty="B1",question="Lees: 'Hoewel het project vertraging opliep, werd het binnen het budget afgerond.' Wat bleef binnen het budget?",options=["Het project.","De vertraging.","De vergadering.","De planning."],correct="Het project."),
    AssessmentQuestion(id="nl-b1-015x",skill="grammar",difficulty="B1",question="Kies de correcte indirecte vraag.",options=["Weet je waar de halte is?","Weet je waar is de halte?","Weet je waar de halte zijn?","Weet je waar is halte de?"],correct="Weet je waar de halte is?"),
    AssessmentQuestion(id="nl-b1-016x",skill="vocabulary",difficulty="B1",question="Wat betekent 'toenemen'?",options=["groter of sterker worden","helemaal verdwijnen","iets uitstellen","een besluit intrekken"],correct="groter of sterker worden"),
    AssessmentQuestion(id="nl-b1-017x",skill="reading",difficulty="B1",question="Lees: 'Mila spaart geld zodat ze volgend jaar kan reizen.' Waarom spaart Mila geld?",options=["Om volgend jaar te kunnen reizen.","Om een auto te verkopen.","Om haar baan op te zeggen.","Om vandaag te verhuizen."],correct="Om volgend jaar te kunnen reizen."),
    AssessmentQuestion(id="nl-b1-018x",skill="grammar",difficulty="B1",question="Kies de juiste combinatie van tijden.",options=["Toen ik aankwam, was de film al begonnen.","Toen ik aankom, was de film al begonnen.","Toen ik aankwam, is de film al beginnen.","Toen ik aankwam, de film al begonnen was?"],correct="Toen ik aankwam, was de film al begonnen."),
    AssessmentQuestion(id="nl-b1-019x",skill="vocabulary",difficulty="B1",question="Wat betekent 'de aanpak'?",options=["de manier waarop iets wordt aangepakt","een betaalmiddel","een verblijfplaats","een feestdag"],correct="de manier waarop iets wordt aangepakt"),
    AssessmentQuestion(id="nl-b2-009x",skill="grammar",difficulty="B2",question="Kies de correcte concessieve constructie.",options=["Hoewel de kosten stegen, bleef het project haalbaar.","Hoewel de kosten stegen, het project bleef haalbaar.","Hoewel stegen de kosten, bleef het project haalbaar.","Hoewel de kosten stegen, bleef haalbaar het project."],correct="Hoewel de kosten stegen, bleef het project haalbaar."),
    AssessmentQuestion(id="nl-b2-010x",skill="vocabulary",difficulty="B2",question="Wat betekent 'nuanceren'?",options=["een uitspraak preciezer en minder absoluut maken","een tekst letterlijk herhalen","een afspraak annuleren","een probleem verbergen"],correct="een uitspraak preciezer en minder absoluut maken"),
    AssessmentQuestion(id="nl-b2-011x",skill="reading",difficulty="B2",question="Lees: 'De steekproef was klein; daarom moeten de conclusies voorzichtig worden geïnterpreteerd.' Wat is de reden voor voorzichtigheid?",options=["De steekproef was klein.","De conclusies waren al bewezen.","De gegevens waren openbaar.","De studie duurde te lang."],correct="De steekproef was klein."),
    AssessmentQuestion(id="nl-b2-012x",skill="grammar",difficulty="B2",question="Kies de juiste inversie na een bijwoordelijke bepaling.",options=["Na de presentatie beantwoordde de onderzoeker vragen.","Na de presentatie de onderzoeker beantwoordde vragen.","Na de presentatie beantwoordde vragen de onderzoeker.","Na de presentatie de vragen beantwoordde de onderzoeker."],correct="Na de presentatie beantwoordde de onderzoeker vragen."),
    AssessmentQuestion(id="nl-b2-013x",skill="vocabulary",difficulty="B2",question="Wat betekent 'aannemelijk'?",options=["geloofwaardig op basis van beschikbare aanwijzingen","volledig onmogelijk","onbelangrijk","onmiddellijk zichtbaar"],correct="geloofwaardig op basis van beschikbare aanwijzingen"),
    AssessmentQuestion(id="nl-b2-014x",skill="reading",difficulty="B2",question="Lees: 'De maatregel had effect, maar het effect was kleiner dan verwacht.' Wat wordt gezegd?",options=["Het effect was kleiner dan verwacht.","De maatregel had geen effect.","Het effect was groter dan verwacht.","De maatregel werd niet uitgevoerd."],correct="Het effect was kleiner dan verwacht."),
    AssessmentQuestion(id="nl-b2-015x",skill="grammar",difficulty="B2",question="Kies de correcte formulering met 'tenzij'.",options=["We gaan door, tenzij er nieuwe informatie komt.","We gaan door, tenzij komt er nieuwe informatie.","We gaan door, tenzij er komt nieuwe informatie.","We gaan door tenzij nieuwe informatie er komt."],correct="We gaan door, tenzij er nieuwe informatie komt."),
    AssessmentQuestion(id="nl-b2-016x",skill="vocabulary",difficulty="B2",question="Wat betekent 'weerleggen'?",options=["aantonen dat een bewering niet klopt","een bewering herhalen","een afspraak plannen","een tekst inkorten"],correct="aantonen dat een bewering niet klopt"),
    AssessmentQuestion(id="nl-b2-017x",skill="reading",difficulty="B2",question="Lees: 'De auteurs erkennen de beperkingen van het onderzoek en stellen vervolgonderzoek voor.' Wat stellen zij voor?",options=["Vervolgonderzoek.","Het onderzoek onmiddellijk stoppen.","De beperkingen verbergen.","Alle gegevens verwijderen."],correct="Vervolgonderzoek."),
    AssessmentQuestion(id="nl-b2-018x",skill="grammar",difficulty="B2",question="Kies de correcte indirecte vraag.",options=["De commissie vroeg waarom de planning was gewijzigd.","De commissie vroeg waarom was de planning gewijzigd.","De commissie vroeg waarom de planning gewijzigd was?","De commissie vroeg waarom gewijzigd de planning was."],correct="De commissie vroeg waarom de planning was gewijzigd.")


    AssessmentQuestion(id="nl-a1-009x",skill="grammar",difficulty="A1",question="Kies het juiste lidwoord: ___ huis.",options=["het","de","een het","die"],correct="het"),
    AssessmentQuestion(id="nl-a1-010x",skill="vocabulary",difficulty="A1",question="Wat betekent 'brood'?",options=["een voedingsmiddel","een vervoermiddel","een gebouw","een kledingstuk"],correct="een voedingsmiddel"),
    AssessmentQuestion(id="nl-a1-011x",skill="reading",difficulty="A1",question="Lees: 'Sara drinkt thee.' Wat drinkt Sara?",options=["Thee.","Koffie.","Water.","Melk."],correct="Thee."),
    AssessmentQuestion(id="nl-a1-012x",skill="grammar",difficulty="A1",question="Kies de juiste meervoudsvorm van 'stoel'.",options=["stoelen","stoels","stoelens","stoeler"],correct="stoelen"),
    AssessmentQuestion(id="nl-b1-020x",skill="grammar",difficulty="B1",question="Kies de correcte indirecte vraag in de verleden tijd.",options=["Hij vroeg waar ik woonde.","Hij vroeg waar woonde ik.","Hij vroeg waar ik woon.","Hij vroeg waar woon ik."],correct="Hij vroeg waar ik woonde."),
    AssessmentQuestion(id="nl-b2-019x",skill="grammar",difficulty="B2",question="Kies de correcte formulering met een voorwaardelijke bijzin.",options=["Als de gegevens beschikbaar waren, konden we de hypothese toetsen.","Als de gegevens waren beschikbaar, we konden de hypothese toetsen.","Als de gegevens beschikbaar zijn, konden we gisteren toetsen.","Als de gegevens beschikbaar waren, we de hypothese toetsen konden."],correct="Als de gegevens beschikbaar waren, konden we de hypothese toetsen."),
    AssessmentQuestion(id="nl-b2-020x",skill="reading",difficulty="B2",question="Lees: 'De resultaten zijn veelbelovend, hoewel de steekproef beperkt blijft.' Welke beperking wordt genoemd?",options=["De steekproef is beperkt.","De resultaten zijn negatief.","Er is geen onderzoek uitgevoerd.","De resultaten zijn definitief."],correct="De steekproef is beperkt.")
]
