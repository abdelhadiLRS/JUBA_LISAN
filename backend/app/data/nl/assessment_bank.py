"""Nederlands assessment bank A1-C2."""
from app.data._types import AssessmentQuestion

ASSESSMENT_BANK = [
    AssessmentQuestion(id="nl-a1-001",skill="grammar",difficulty="A1",question="Welke zin is correct?",options=["Ik ben student.","Ik is student.","Ik bent student.","Ik zijn student."],correct="Ik ben student."),
    AssessmentQuestion(id="nl-a1-002",skill="grammar",difficulty="A1",question="Welke zin heeft de juiste woordvolgorde?",options=["Vandaag werk ik thuis.","Vandaag ik werk thuis.","Vandaag thuis werk ik.","Werk vandaag ik thuis."],correct="Vandaag werk ik thuis."),
    AssessmentQuestion(id="nl-a1-003",skill="vocabulary",difficulty="A1",question="Welk woord betekent 'moeder'?",options=["moeder","vader","broer","zus"],correct="moeder"),
    AssessmentQuestion(id="nl-a1-004",skill="reading",difficulty="A1",question="Je wilt naar de prijs vragen. Wat zeg je?",options=["Hoeveel kost dit?","Hoe heet je?","Waar woon je?","Tot ziens."],correct="Hoeveel kost dit?"),
    AssessmentQuestion(id="nl-a1-005",skill="grammar",difficulty="A1",question="Welke zin gebruikt 'geen' correct?",options=["Ik heb geen auto.","Ik geen heb auto.","Ik heb niet auto.","Ik heb auto geen."],correct="Ik heb geen auto."),
    AssessmentQuestion(id="nl-a1-006",skill="vocabulary",difficulty="A1",question="Wat betekent 'afspraak'?",options=["afgesproken moment","maaltijd","familielid","vervoer"],correct="afgesproken moment"),
    AssessmentQuestion(id="nl-a1-007",skill="reading",difficulty="A1",question="Wat betekent 'Het station is dichtbij'?",options=["Het station is dichtbij.","Het station is gesloten.","Het station is ver weg.","Het station is duur."],correct="Het station is dichtbij."),
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


AssessmentQuestion(id="nl-a2-009",skill="grammar",difficulty="A2",question="Welke zin staat in de verleden tijd?",options=["Gisteren ging ik naar de markt.","Gisteren ga ik naar de markt.","Gisteren gaan ik naar de markt.","Gisteren zal ik naar de markt gaan."],correct="Gisteren ging ik naar de markt."),
AssessmentQuestion(id="nl-a2-010",skill="vocabulary",difficulty="A2",question="Wat betekent 'vertraging'?",options=["iets komt later dan gepland","een reservering","een adres","een betaling"],correct="iets komt later dan gepland"),
AssessmentQuestion(id="nl-a2-011",skill="reading",difficulty="A2",question="Lees: 'De winkel sluit om zes uur.' Wanneer sluit de winkel?",options=["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],correct="Om zes uur."),
AssessmentQuestion(id="nl-a2-012",skill="grammar",difficulty="A2",question="Kies de juiste vorm met 'moeten'.",options=["Ik moet werken.","Ik moet werkt.","Ik moet gewerkt.","Ik moet te werken."],correct="Ik moet werken."),
AssessmentQuestion(id="nl-a2-013",skill="grammar",difficulty="A2",question="Welke zin gebruikt 'omdat' correct?",options=["Ik blijf thuis omdat ik ziek ben.","Ik blijf thuis omdat ben ik ziek.","Ik blijf thuis omdat ik ben ziek.","Ik blijf thuis omdat ziek ik ben."],correct="Ik blijf thuis omdat ik ziek ben."),
AssessmentQuestion(id="nl-a2-014",skill="vocabulary",difficulty="A2",question="Waar koop je medicijnen?",options=["Bij de apotheek.","Op het station.","In de bibliotheek.","In het hotel."],correct="Bij de apotheek."),
AssessmentQuestion(id="nl-a2-015",skill="reading",difficulty="A2",question="Lees: 'Lisa neemt de bus naar school.' Waar gaat Lisa naartoe?",options=["Naar school.","Naar het ziekenhuis.","Naar het station.","Naar huis."],correct="Naar school."),
AssessmentQuestion(id="nl-a2-016",skill="grammar",difficulty="A2",question="Kies de juiste voorzetselgroep.",options=["Ik woon in Nederland.","Ik woon op Nederland.","Ik woon aan Nederland.","Ik woon naar Nederland."],correct="Ik woon in Nederland."),
AssessmentQuestion(id="nl-b1-005",skill="grammar",difficulty="B1",question="Welke voorwaardelijke zin is correct?",options=["Als ik tijd had, zou ik reizen.","Als ik tijd had, zal ik gisteren reizen.","Als ik tijd heb, zou ik gisteren reizen.","Als ik tijd had, reisde ik morgen."],correct="Als ik tijd had, zou ik reizen."),
AssessmentQuestion(id="nl-b1-006",skill="vocabulary",difficulty="B1",question="Wat betekent 'uitdaging'?",options=["iets waarvoor inspanning nodig is","een beloning","een vakantie","een adres"],correct="iets waarvoor inspanning nodig is"),
AssessmentQuestion(id="nl-b1-007",skill="reading",difficulty="B1",question="Lees: 'De vergadering werd uitgesteld omdat de directeur ziek was.' Waarom werd de vergadering uitgesteld?",options=["Omdat de directeur ziek was.","Omdat het kantoor dicht was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],correct="Omdat de directeur ziek was."),
AssessmentQuestion(id="nl-b1-008",skill="grammar",difficulty="B1",question="Welke zin heeft de juiste woordvolgorde?",options=["Gisteren kocht ik een nieuwe computer.","Gisteren ik kocht een nieuwe computer.","Gisteren kocht een nieuwe computer ik.","Gisteren een nieuwe computer kocht ik."],correct="Gisteren kocht ik een nieuwe computer."),
AssessmentQuestion(id="nl-b1-009",skill="grammar",difficulty="B1",question="Welke relatieve bijzin is correct?",options=["De vrouw die daar woont is arts.","De vrouw dat daar woont is arts.","De vrouw die daar wonen is arts.","De vrouw wat daar woont is arts."],correct="De vrouw die daar woont is arts."),
AssessmentQuestion(id="nl-b1-010",skill="vocabulary",difficulty="B1",question="Wat betekent 'ervaring'?",options=["kennis uit eerdere gebeurtenissen","een treinkaartje","een gebouw","een afspraak"],correct="kennis uit eerdere gebeurtenissen"),
AssessmentQuestion(id="nl-b1-011",skill="reading",difficulty="B1",question="Welke zin drukt een mening uit?",options=["Volgens mij is dit een goede oplossing.","De winkel opent om negen uur.","Ik woon in Rotterdam.","De trein vertrekt om acht uur."],correct="Volgens mij is dit een goede oplossing."),
AssessmentQuestion(id="nl-b1-012",skill="grammar",difficulty="B1",question="Welke zin gebruikt de verleden tijd correct?",options=["Toen ik klein was, woonde ik in Utrecht.","Toen ik klein ben, woonde ik in Utrecht.","Toen ik klein was, woon ik in Utrecht.","Toen ik klein was, gewoond ik in Utrecht."],correct="Toen ik klein was, woonde ik in Utrecht."),
AssessmentQuestion(id="nl-b2-005",skill="grammar",difficulty="B2",question="Welke zin drukt een tegenstelling uit?",options=["Hoewel het regende, gingen we wandelen.","Omdat het regende, gingen we wandelen.","Toen het regende, gingen we wandelen.","Als het regende, gingen we wandelen."],correct="Hoewel het regende, gingen we wandelen."),
AssessmentQuestion(id="nl-b2-006",skill="vocabulary",difficulty="B2",question="Wat betekent 'voorspellen'?",options=["inschatten wat er zal gebeuren","het verleden uitleggen","een regel wijzigen","een afspraak annuleren"],correct="inschatten wat er zal gebeuren"),
AssessmentQuestion(id="nl-b2-007",skill="reading",difficulty="B2",question="Lees: 'De resultaten wijzen op verbetering, maar verdere studie is nodig.' Wat is nodig?",options=["Verdere studie.","Minder gegevens.","Een nieuwe afspraak.","Een andere taal."],correct="Verdere studie."),
AssessmentQuestion(id="nl-b2-008",skill="grammar",difficulty="B2",question="Kies de correcte indirecte vraag.",options=["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],correct="Ik weet niet wanneer de vergadering begint."),
AssessmentQuestion(id="nl-b2-009",skill="grammar",difficulty="B2",question="Welke passieve zin is correct?",options=["Het rapport wordt morgen gepubliceerd.","Het rapport wordt morgen publiceren.","Het rapport morgen wordt gepubliceerd.","Het rapport publiceert morgen."],correct="Het rapport wordt morgen gepubliceerd."),
AssessmentQuestion(id="nl-b2-010",skill="vocabulary",difficulty="B2",question="Wat betekent 'onderbouwen'?",options=["een bewering met argumenten of bewijs ondersteunen","een tekst inkorten","een afspraak verplaatsen","een woord vertalen"],correct="een bewering met argumenten of bewijs ondersteunen"),
AssessmentQuestion(id="nl-b2-011",skill="reading",difficulty="B2",question="Welke formulering introduceert een voorbehoud?",options=["Dit geldt alleen als de gegevens betrouwbaar zijn.","Dit is absoluut zeker.","Dit heeft niets met de gegevens te maken.","Dit is altijd het geval."],correct="Dit geldt alleen als de gegevens betrouwbaar zijn."),
AssessmentQuestion(id="nl-b2-012",skill="grammar",difficulty="B2",question="Welke zin is grammaticaal correct?",options=["Ondanks de problemen ging het project door.","Ondanks de problemen het project ging door.","Ondanks de problemen ging door het project.","Ondanks aan de problemen ging het project door."],correct="Ondanks de problemen ging het project door."),
AssessmentQuestion(id="nl-c1-005",skill="grammar",difficulty="C1",question="Welke formulering past het best in een academische tekst?",options=["De resultaten suggereren dat het effect beperkt is.","De resultaten zeggen dat alles zeker is.","De resultaten suggereren het effect dat beperkt is.","De resultaten suggereert dat het effect beperkt zijn."],correct="De resultaten suggereren dat het effect beperkt is."),
AssessmentQuestion(id="nl-c1-006",skill="vocabulary",difficulty="C1",question="Wat betekent 'wezenlijk' in een academische context?",options=["belangrijk of fundamenteel","toevallig","tijdelijk","informeel"],correct="belangrijk of fundamenteel"),
AssessmentQuestion(id="nl-c1-007",skill="reading",difficulty="C1",question="Lees: 'Correlatie bewijst op zichzelf geen oorzakelijk verband.' Wat wordt niet bewezen?",options=["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens zijn.","Dat variabelen samenhangen.","Dat er een analyse is uitgevoerd."],correct="Dat het ene verschijnsel het andere veroorzaakt."),
AssessmentQuestion(id="nl-c1-008",skill="grammar",difficulty="C1",question="Kies de correcte passieve constructie.",options=["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek uitgevoerd werd in drie fasen.","Het onderzoek werden in drie fasen uitgevoerd."],correct="Het onderzoek werd in drie fasen uitgevoerd."),
AssessmentQuestion(id="nl-c1-009",skill="grammar",difficulty="C1",question="Welke formulering is het meest genuanceerd?",options=["De gegevens lijken erop te wijzen dat het effect beperkt is.","De gegevens bewijzen absoluut dat alles klopt.","De gegevens zeggen niets over het effect.","De gegevens maken elke andere verklaring onmogelijk."],correct="De gegevens lijken erop te wijzen dat het effect beperkt is."),
AssessmentQuestion(id="nl-c1-010",skill="vocabulary",difficulty="C1",question="Wat betekent 'veronderstelling'?",options=["een aangenomen uitgangspunt","een conclusie","een begroeting","een vertraging"],correct="een aangenomen uitgangspunt"),
AssessmentQuestion(id="nl-c1-011",skill="reading",difficulty="C1",question="Lees: 'De resultaten zijn veelbelovend, hoewel de steekproef beperkt is.' Welke beperking wordt genoemd?",options=["De steekproef is beperkt.","De resultaten ontbreken.","De studie is geannuleerd.","De gegevens zijn oud."],correct="De steekproef is beperkt."),
AssessmentQuestion(id="nl-c1-012",skill="grammar",difficulty="C1",question="Welke zin gebruikt een concessieve constructie correct?",options=["Hoewel de methode beperkingen heeft, blijft zij bruikbaar.","Hoewel de methode beperkingen heeft, zij blijft bruikbaar.","Hoewel de methode heeft beperkingen, blijft zij bruikbaar.","Hoewel de methode beperkingen heeft, blijft bruikbaar zij."],correct="Hoewel de methode beperkingen heeft, blijft zij bruikbaar."),
AssessmentQuestion(id="nl-c2-005",skill="grammar",difficulty="C2",question="Welke formulering drukt epistemische voorzichtigheid uit?",options=["Het valt niet uit te sluiten dat andere factoren een rol spelen.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],correct="Het valt niet uit te sluiten dat andere factoren een rol spelen."),
AssessmentQuestion(id="nl-c2-006",skill="vocabulary",difficulty="C2",question="Wat betekent 'dubbelzinnig'?",options=["vatbaar voor meer dan één interpretatie","volkomen eenduidig","zeer kort","gemakkelijk meetbaar"],correct="vatbaar voor meer dan één interpretatie"),
AssessmentQuestion(id="nl-c2-007",skill="reading",difficulty="C2",question="Lees: 'Het argument is overtuigend, mits de onderliggende aanname standhoudt.' Waarvan hangt de beoordeling af?",options=["Of de onderliggende aanname standhoudt.","Of het argument kort is.","Of de tekst informeel is.","Of de gegevens oud zijn."],correct="Of de onderliggende aanname standhoudt."),
AssessmentQuestion(id="nl-c2-008",skill="grammar",difficulty="C2",question="Kies de meest precieze academische formulering.",options=["De resultaten laten geen eenduidige generalisatie toe zonder aanvullende gegevens.","De resultaten laten altijd generalisatie toe zonder gegevens.","De resultaten laten geen generaliseren toe zonder aanvullende.","De resultaten laten een zekere generalisatie toe zonder analyse."],correct="De resultaten laten geen eenduidige generalisatie toe zonder aanvullende gegevens.")

AssessmentQuestion(id="nl-c2-009",skill="grammar",difficulty="C2",question="Welke formulering maakt een bewering het meest voorzichtig?",options=["De gegevens lijken erop te wijzen dat het effect beperkt is.","De gegevens bewijzen zonder twijfel dat het effect beperkt is.","De gegevens sluiten elke andere verklaring uit.","De gegevens maken verder onderzoek overbodig."],correct="De gegevens lijken erop te wijzen dat het effect beperkt is."),
AssessmentQuestion(id="nl-c2-010",skill="vocabulary",difficulty="C2",question="Wat betekent 'voorwaardelijk' in een redenering?",options=["afhankelijk van een bepaalde voorwaarde","volledig onafhankelijk","zonder enige beperking","puur toevallig"],correct="afhankelijk van een bepaalde voorwaarde"),
AssessmentQuestion(id="nl-c2-011",skill="reading",difficulty="C2",question="Lees: 'De conclusie is aannemelijk, maar blijft afhankelijk van de kwaliteit van de onderliggende gegevens.' Waarvan hangt de conclusie af?",options=["Van de kwaliteit van de gegevens.","Van de lengte van het rapport.","Van de vormgeving van de tekst.","Van de leeftijd van de auteur."],correct="Van de kwaliteit van de gegevens."),
AssessmentQuestion(id="nl-c2-012",skill="grammar",difficulty="C2",question="Kies de meest idiomatische formulering.",options=["Niettemin dienen de resultaten met enige terughoudendheid te worden geïnterpreteerd.","Niettemin de resultaten dienen met terughoudendheid worden geïnterpreteerd.","Niettemin dienen de resultaten met terughoudendheid te interpreteren.","Niettemin de resultaten te worden geïnterpreteerd dienen."],correct="Niettemin dienen de resultaten met enige terughoudendheid te worden geïnterpreteerd.")

    AssessmentQuestion(id="nl-a2-005",skill="grammar",difficulty="A2",question="Welke zin staat in de verleden tijd?",options=["Gisteren werkte ik thuis.","Gisteren werk ik thuis.","Gisteren zal ik thuis werken.","Gisteren werken ik thuis."],correct="Gisteren werkte ik thuis."),
    AssessmentQuestion(id="nl-a2-006",skill="vocabulary",difficulty="A2",question="Wat betekent 'vertraging'?",options=["iets dat later komt dan gepland","een reservering","een adres","een betaling"],correct="iets dat later komt dan gepland"),
    AssessmentQuestion(id="nl-a2-007",skill="reading",difficulty="A2",question="Lees: 'De winkel sluit om zes uur.' Hoe laat sluit de winkel?",options=["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],correct="Om zes uur."),
    AssessmentQuestion(id="nl-a2-008",skill="grammar",difficulty="A2",question="Kies de juiste zin met 'moeten'.",options=["Ik moet morgen werken.","Ik moet morgen werk.","Ik moet morgen gewerkt.","Ik moeten morgen werken."],correct="Ik moet morgen werken."),
    AssessmentQuestion(id="nl-b1-005",skill="grammar",difficulty="B1",question="Welke betrekkelijke bijzin is correct?",options=["Dit is het boek dat ik gisteren kocht.","Dit is het boek die ik gisteren kocht.","Dit is het boek dat ik het kocht.","Dit is het boek die gisteren ik kocht."],correct="Dit is het boek dat ik gisteren kocht."),
    AssessmentQuestion(id="nl-b1-006",skill="vocabulary",difficulty="B1",question="Wat betekent 'uitdaging'?",options=["iets dat inspanning vereist","een beloning","een vakantie","een adres"],correct="iets dat inspanning vereist"),
    AssessmentQuestion(id="nl-b1-007",skill="reading",difficulty="B1",question="Lees: 'De vergadering werd verplaatst omdat de directeur ziek was.' Waarom werd de vergadering verplaatst?",options=["Omdat de directeur ziek was.","Omdat het kantoor gesloten was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],correct="Omdat de directeur ziek was."),
    AssessmentQuestion(id="nl-b1-008",skill="grammar",difficulty="B1",question="Kies de juiste woordvolgorde.",options=["Gisteren kocht ik een nieuwe computer.","Gisteren ik kocht een nieuwe computer.","Gisteren kocht een nieuwe computer ik.","Gisteren een nieuwe computer kocht ik."],correct="Gisteren kocht ik een nieuwe computer."),
    AssessmentQuestion(id="nl-b2-005",skill="grammar",difficulty="B2",question="Welke zin drukt een tegenstelling uit?",options=["Hoewel het regende, gingen we wandelen.","Omdat het regende, gingen we wandelen.","Zodra het regende, gingen we wandelen.","Als het regende, gingen we niet wandelen."],correct="Hoewel het regende, gingen we wandelen."),
    AssessmentQuestion(id="nl-b2-006",skill="vocabulary",difficulty="B2",question="Wat betekent 'voorspellen'?",options=["zeggen wat waarschijnlijk zal gebeuren","iets uit het verleden uitleggen","een regel veranderen","een afspraak annuleren"],correct="zeggen wat waarschijnlijk zal gebeuren"),
    AssessmentQuestion(id="nl-b2-007",skill="reading",difficulty="B2",question="Lees: 'De resultaten tonen een duidelijke trend, maar moeten voorzichtig worden geïnterpreteerd.' Wat wordt aanbevolen?",options=["Een voorzichtige interpretatie van de resultaten.","De resultaten negeren.","Alle resultaten veranderen.","Het onderzoek onmiddellijk stoppen."],correct="Een voorzichtige interpretatie van de resultaten."),
    AssessmentQuestion(id="nl-b2-008",skill="grammar",difficulty="B2",question="Kies de correcte indirecte vraag.",options=["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],correct="Ik weet niet wanneer de vergadering begint."),
    AssessmentQuestion(id="nl-c1-005",skill="grammar",difficulty="C1",question="Welke formulering past het best in een academische tekst?",options=["De resultaten wijzen erop dat het effect beperkt is.","De resultaten wijzen dat het effect beperkt is.","De resultaten wijst erop dat het effect beperkt is.","De resultaten wijzen erop het effect dat beperkt is."],correct="De resultaten wijzen erop dat het effect beperkt is."),
    AssessmentQuestion(id="nl-c1-006",skill="vocabulary",difficulty="C1",question="Wat betekent 'wezenlijk' in een academische context?",options=["belangrijk of significant","toevallig","tijdelijk","informeel"],correct="belangrijk of significant"),
    AssessmentQuestion(id="nl-c1-007",skill="reading",difficulty="C1",question="Lees: 'Correlatie bewijst op zichzelf geen causaal verband.' Wat wordt niet bewezen?",options=["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens zijn.","Dat de variabelen samenhangen.","Dat er een analyse is uitgevoerd."],correct="Dat het ene verschijnsel het andere veroorzaakt."),
    AssessmentQuestion(id="nl-c1-008",skill="grammar",difficulty="C1",question="Kies de correcte passieve constructie.",options=["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek uitgevoerd werd in drie fasen.","Het onderzoek werd in drie fase uitgevoerd."],correct="Het onderzoek werd in drie fasen uitgevoerd."),
    AssessmentQuestion(id="nl-c2-005",skill="grammar",difficulty="C2",question="Welke formulering drukt epistemische voorzichtigheid uit?",options=["Het kan niet worden uitgesloten dat andere factoren een rol spelen.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],correct="Het kan niet worden uitgesloten dat andere factoren een rol spelen."),
    AssessmentQuestion(id="nl-c2-006",skill="vocabulary",difficulty="C2",question="Wat betekent 'dubbelzinnig'?",options=["vatbaar voor meer dan één interpretatie","volledig eenduidig","zeer kort","gemakkelijk te meten"],correct="vatbaar voor meer dan één interpretatie"),
    AssessmentQuestion(id="nl-c2-007",skill="reading",difficulty="C2",question="Lees: 'Het argument is overtuigend, mits de onderliggende aanname klopt.' Waarvan hangt de beoordeling af?",options=["Of de onderliggende aanname klopt.","Of het argument kort is.","Of de tekst informeel is.","Of de gegevens oud zijn."],correct="Of de onderliggende aanname klopt."),
    AssessmentQuestion(id="nl-c2-008",skill="grammar",difficulty="C2",question="Kies de meest precieze academische formulering.",options=["De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.","De resultaten laten altijd generalisatie toe zonder gegevens.","De resultaten laten geen generaliseren zonder aanvullende toe.","De resultaten laten een zekere generalisatie toe zonder analyse."],correct="De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.")

AssessmentQuestion(id="nl-a1-009",skill="grammar",difficulty="A1",question="Kies de juiste vraag.",options=["Waar woon je?","Waar je woont?","Woon waar je?","Waar wonen?"],correct="Waar woon je?",grammar_slug="vragen"),
AssessmentQuestion(id="nl-a1-010",skill="vocabulary",difficulty="A1",question="Wat betekent 'appel'?",options=["een vrucht","een voertuig","een gebouw","een meubel"],correct="een vrucht"),
AssessmentQuestion(id="nl-a1-011",skill="reading",difficulty="A1",question="Lees: 'Sofie woont in Utrecht.' Waar woont Sofie?",options=["In Utrecht.","In Amsterdam.","In Rotterdam.","In Leiden."],correct="In Utrecht."),
AssessmentQuestion(id="nl-a1-012",skill="grammar",difficulty="A1",question="Kies de juiste zin.",options=["Ik heb een boek.","Ik heb een boeken.","Ik hebben een boek.","Ik heb boek een."],correct="Ik heb een boek.",grammar_slug="hebben"),
AssessmentQuestion(id="nl-a2-005",skill="grammar",difficulty="A2",question="Kies de juiste voltooide tijd.",options=["Ik heb gegeten.","Ik heb eten.","Ik heb at.","Ik eet heb."],correct="Ik heb gegeten.",grammar_slug="voltooide-tijd"),
AssessmentQuestion(id="nl-a2-006",skill="vocabulary",difficulty="A2",question="Wat betekent 'vertraging'?",options=["iets dat later komt dan gepland","een reservering","een adres","een betaling"],correct="iets dat later komt dan gepland"),
AssessmentQuestion(id="nl-a2-007",skill="reading",difficulty="A2",question="Lees: 'De winkel sluit om zes uur.' Hoe laat sluit de winkel?",options=["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],correct="Om zes uur."),
AssessmentQuestion(id="nl-a2-008",skill="grammar",difficulty="A2",question="Kies het juiste voorzetsel.",options=["Ik woon in Nederland.","Ik woon op Nederland.","Ik woon naar Nederland.","Ik woon aan Nederland."],correct="Ik woon in Nederland.",grammar_slug="voorzetsels"),
AssessmentQuestion(id="nl-b1-005",skill="grammar",difficulty="B1",question="Kies de juiste betrekkelijke bijzin.",options=["Dit is het boek dat ik heb gekocht.","Dit is het boek die ik heb gekocht.","Dit is het boek dat ik gekocht.","Dit is het boek ik dat heb gekocht."],correct="Dit is het boek dat ik heb gekocht.",grammar_slug="betrekkelijke-bijzin"),
AssessmentQuestion(id="nl-b1-006",skill="vocabulary",difficulty="B1",question="Wat betekent 'uitdaging'?",options=["iets waarvoor inspanning nodig is","een beloning","een vakantie","een adres"],correct="iets waarvoor inspanning nodig is"),
AssessmentQuestion(id="nl-b1-007",skill="reading",difficulty="B1",question="Lees: 'De vergadering werd verplaatst omdat de directeur ziek was.' Waarom werd de vergadering verplaatst?",options=["Omdat de directeur ziek was.","Omdat het kantoor gesloten was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],correct="Omdat de directeur ziek was."),
AssessmentQuestion(id="nl-b1-008",skill="grammar",difficulty="B1",question="Kies de juiste woordvolgorde.",options=["Gisteren kocht ik een nieuwe computer.","Gisteren ik kocht een nieuwe computer.","Gisteren kocht een nieuwe computer ik.","Gisteren een nieuwe computer kocht ik."],correct="Gisteren kocht ik een nieuwe computer.",grammar_slug="woordvolgorde"),
AssessmentQuestion(id="nl-b2-005",skill="grammar",difficulty="B2",question="Kies de juiste concessieve bijzin.",options=["Hoewel het regende, gingen we wandelen.","Hoewel het regende, we gingen wandelen.","Hoewel regende het, gingen we wandelen.","Hoewel het regende, we wandelen gingen."],correct="Hoewel het regende, gingen we wandelen.",grammar_slug="concessieve-bijzin"),
AssessmentQuestion(id="nl-b2-006",skill="vocabulary",difficulty="B2",question="Wat betekent 'voorspellen'?",options=["zeggen wat waarschijnlijk zal gebeuren","iets uit het verleden uitleggen","een regel veranderen","een afspraak annuleren"],correct="zeggen wat waarschijnlijk zal gebeuren"),
AssessmentQuestion(id="nl-b2-007",skill="reading",difficulty="B2",question="Lees: 'De resultaten tonen een duidelijke trend, maar moeten voorzichtig worden geïnterpreteerd.' Wat wordt aanbevolen?",options=["De resultaten voorzichtig interpreteren.","De resultaten negeren.","Alle resultaten veranderen.","Het onderzoek meteen stoppen."],correct="De resultaten voorzichtig interpreteren."),
AssessmentQuestion(id="nl-b2-008",skill="grammar",difficulty="B2",question="Kies de juiste indirecte vraag.",options=["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],correct="Ik weet niet wanneer de vergadering begint.",grammar_slug="indirecte-vraag"),
AssessmentQuestion(id="nl-c1-005",skill="grammar",difficulty="C1",question="Kies de meest precieze academische formulering.",options=["De resultaten wijzen erop dat het effect beperkt is.","De resultaten wijzen dat het effect beperkt is.","De resultaten wijst erop dat het effect beperkt is.","De resultaten wijzen erop het effect dat beperkt is."],correct="De resultaten wijzen erop dat het effect beperkt is.",grammar_slug="academische-taal"),
AssessmentQuestion(id="nl-c1-006",skill="vocabulary",difficulty="C1",question="Wat betekent 'wezenlijk' in een academische context?",options=["belangrijk of significant","toevallig","tijdelijk","informeel"],correct="belangrijk of significant"),
AssessmentQuestion(id="nl-c1-007",skill="reading",difficulty="C1",question="Lees: 'Correlatie bewijst op zichzelf geen causaal verband.' Wat bewijst correlatie niet?",options=["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens zijn.","Dat variabelen samenhangen.","Dat er een analyse is uitgevoerd."],correct="Dat het ene verschijnsel het andere veroorzaakt."),
AssessmentQuestion(id="nl-c1-008",skill="grammar",difficulty="C1",question="Kies de juiste passieve constructie.",options=["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek voerde in drie fasen uit.","Het onderzoek werd uitgevoerd drie fasen."],correct="Het onderzoek werd in drie fasen uitgevoerd.",grammar_slug="passief"),
AssessmentQuestion(id="nl-c2-005",skill="grammar",difficulty="C2",question="Welke formulering drukt epistemische voorzichtigheid uit?",options=["Het kan niet worden uitgesloten dat andere factoren een rol spelen.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],correct="Het kan niet worden uitgesloten dat andere factoren een rol spelen.",grammar_slug="epistemische-modaliteit"),
AssessmentQuestion(id="nl-c2-006",skill="vocabulary",difficulty="C2",question="Wat betekent 'dubbelzinnig'?",options=["voor meer dan één interpretatie vatbaar","volledig eenduidig","zeer kort","gemakkelijk te meten"],correct="voor meer dan één interpretatie vatbaar"),
AssessmentQuestion(id="nl-c2-007",skill="reading",difficulty="C2",question="Lees: 'Het argument is overtuigend, mits de onderliggende aanname klopt.' Waarvan hangt de beoordeling af?",options=["Of de onderliggende aanname klopt.","Of het argument kort is.","Of de tekst informeel is.","Of de gegevens oud zijn."],correct="Of de onderliggende aanname klopt."),
AssessmentQuestion(id="nl-c2-008",skill="grammar",difficulty="C2",question="Kies de meest precieze academische formulering.",options=["De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.","De resultaten laten altijd generalisatie toe zonder gegevens.","De resultaten laten geen generaliseren toe zonder aanvullende.","De resultaten laten een zekere generalisatie toe zonder analyse."],correct="De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.",grammar_slug="academische-stijl")

AssessmentQuestion("nl-a1-009","grammar","A1","Kies de juiste vraag.",["Waar woon je?","Waar je woont?","Woon waar je?","Waar wonen?"],"Waar woon je?","questions"),
AssessmentQuestion("nl-a1-010","vocabulary","A1","Wat betekent 'appel'?",["een fruitsoort","een voertuig","een gebouw","een meubel"],"een fruitsoort"),
AssessmentQuestion("nl-a1-011","reading","A1","Lees: 'Sofie woont in Utrecht.' Waar woont Sofie?",["In Utrecht.","In Amsterdam.","In Rotterdam.","In Groningen."],"In Utrecht."),
AssessmentQuestion("nl-a1-012","grammar","A1","Kies de juiste vorm.",["Hij heeft een auto.","Hij heeft een auto's.","Hij hebben een auto.","Hij heeft een auto zijn."],"Hij heeft een auto.","hebben"),
AssessmentQuestion("nl-a2-005","grammar","A2","Kies de juiste verleden tijd.",["Gisteren werkte ik thuis.","Gisteren werk ik thuis.","Gisteren werken ik thuis.","Gisteren heb ik werk."],"Gisteren werkte ik thuis.","past-tense"),
AssessmentQuestion("nl-a2-006","vocabulary","A2","Wat betekent 'vertraging'?",["iets dat later komt dan gepland","een reservering","een adres","een betaling"],"iets dat later komt dan gepland"),
AssessmentQuestion("nl-a2-007","reading","A2","Lees: 'De winkel sluit om zes uur.' Hoe laat sluit de winkel?",["Om vijf uur.","Om zes uur.","Om zeven uur.","Om acht uur."],"Om zes uur."),
AssessmentQuestion("nl-a2-008","grammar","A2","Kies de juiste voorzetselcombinatie.",["Ik woon in Nederland.","Ik woon op Nederland.","Ik woon naar Nederland.","Ik woon bij Nederland."],"Ik woon in Nederland.","prepositions"),
AssessmentQuestion("nl-b1-005","grammar","B1","Kies de juiste betrekkelijke bijzin.",["Dit is het boek dat ik heb gekocht.","Dit is het boek dat ik gekocht.","Dit is het boek die ik heb gekocht.","Dit is het boek dat heb ik gekocht."],"Dit is het boek dat ik heb gekocht.","relative-clause"),
AssessmentQuestion("nl-b1-006","vocabulary","B1","Wat betekent 'uitdaging'?",["iets dat inspanning vereist","een beloning","een vakantie","een adres"],"iets dat inspanning vereist"),
AssessmentQuestion("nl-b1-007","reading","B1","Lees: 'De vergadering werd uitgesteld omdat de directeur ziek was.' Waarom werd de vergadering uitgesteld?",["Omdat de directeur ziek was.","Omdat het kantoor gesloten was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],"Omdat de directeur ziek was."),
AssessmentQuestion("nl-b1-008","grammar","B1","Kies de juiste woordvolgorde.",["Gisteren kocht ik een nieuwe computer.","Gisteren ik kocht een nieuwe computer.","Gisteren kocht een nieuwe computer ik.","Gisteren een nieuwe computer kocht ik was."],"Gisteren kocht ik een nieuwe computer.","word-order"),
AssessmentQuestion("nl-b2-005","grammar","B2","Kies de juiste concessieve constructie.",["Hoewel het regende, gingen we wandelen.","Hoewel het regende, we gingen wandelen.","Hoewel regende het, gingen we wandelen.","Hoewel het regende, we wandelen gingen."],"Hoewel het regende, gingen we wandelen.","concessive"),
AssessmentQuestion("nl-b2-006","vocabulary","B2","Wat betekent 'voorspellen'?",["inschatten wat er zal gebeuren","het verleden uitleggen","een regel veranderen","een afspraak annuleren"],"inschatten wat er zal gebeuren"),
AssessmentQuestion("nl-b2-007","reading","B2","Lees: 'De resultaten tonen een duidelijke tendens, maar moeten voorzichtig worden geïnterpreteerd.' Wat wordt aanbevolen?",["De resultaten voorzichtig interpreteren.","De resultaten negeren.","Alle resultaten veranderen.","Het onderzoek onmiddellijk beëindigen."],"De resultaten voorzichtig interpreteren."),
AssessmentQuestion("nl-b2-008","grammar","B2","Kies de juiste indirecte vraag.",["Ik weet niet wanneer de vergadering begint.","Ik weet niet wanneer begint de vergadering.","Ik weet niet wanneer de vergadering begint?","Ik weet niet de vergadering wanneer begint."],"Ik weet niet wanneer de vergadering begint.","indirect-question"),
AssessmentQuestion("nl-c1-005","grammar","C1","Kies de meest precieze academische formulering.",["De resultaten wijzen erop dat het effect beperkt is.","De resultaten wijzen dat het effect beperkt is.","De resultaten wijst erop dat het effect beperkt is.","De resultaten wijzen erop het effect dat beperkt is."],"De resultaten wijzen erop dat het effect beperkt is.","academic-language"),
AssessmentQuestion("nl-c1-006","vocabulary","C1","Wat betekent 'wezenlijk' in een academische tekst?",["belangrijk of fundamenteel","toevallig","tijdelijk","informeel"],"belangrijk of fundamenteel"),
AssessmentQuestion("nl-c1-007","reading","C1","Lees: 'Correlatie bewijst op zichzelf geen causaal verband.' Wat wordt niet bewezen?",["Dat het ene verschijnsel het andere veroorzaakt.","Dat er gegevens zijn.","Dat variabelen samenhangen.","Dat er een analyse is uitgevoerd."],"Dat het ene verschijnsel het andere veroorzaakt."),
AssessmentQuestion("nl-c1-008","grammar","C1","Kies de juiste passieve constructie.",["Het onderzoek werd in drie fasen uitgevoerd.","Het onderzoek werd in drie fasen uitvoeren.","Het onderzoek uitgevoerd werd in drie fasen.","Het onderzoek werd uitgevoerd drie fasen."],"Het onderzoek werd in drie fasen uitgevoerd.","passive"),
AssessmentQuestion("nl-c2-005","grammar","C2","Welke formulering drukt wetenschappelijke voorzichtigheid uit?",["Het kan niet worden uitgesloten dat andere factoren een rol spelen.","Andere factoren spelen zeker geen rol.","Het is zonder uitzondering bewezen dat andere factoren irrelevant zijn.","Andere factoren hoeven niet te worden onderzocht."],"Het kan niet worden uitgesloten dat andere factoren een rol spelen.","epistemic-modality"),
AssessmentQuestion("nl-c2-006","vocabulary","C2","Wat betekent 'dubbelzinnig'?",["voor meerdere interpretaties vatbaar","volledig eenduidig","zeer kort","gemakkelijk meetbaar"],"voor meerdere interpretaties vatbaar"),
AssessmentQuestion("nl-c2-007","reading","C2","Lees: 'Het argument is overtuigend, mits de onderliggende aanname standhoudt.' Waarvan hangt de beoordeling af?",["Of de onderliggende aanname standhoudt.","Of het argument kort is.","Of de tekst informeel is.","Of de gegevens oud zijn."],"Of de onderliggende aanname standhoudt."),
AssessmentQuestion("nl-c2-008","grammar","C2","Kies de meest precieze academische formulering.",["De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.","De resultaten laten altijd een generalisatie toe zonder gegevens.","De resultaten laten geen generaliseren toe zonder aanvullende.","De resultaten laten een zekere generalisatie toe zonder analyse."],"De resultaten laten zonder aanvullende gegevens geen eenduidige generalisatie toe.","academic-style")

AssessmentQuestion("nl-a1-009","grammar","A1","Kies de juiste vorm.",["Ik ben moe.","Ik ben moei.","Ik zijn moe.","Ik ben moeë."],"Ik ben moe.","zijn"),
AssessmentQuestion("nl-a1-010","reading","A1","Lees: 'Sara woont in Utrecht.' Waar woont Sara?",["In Utrecht.","In Rotterdam.","In Groningen.","In Leiden."],"In Utrecht."),
AssessmentQuestion("nl-a2-009","grammar","A2","Kies de juiste verleden tijd.",["Gisteren werkte ik thuis.","Gisteren werk ik thuis.","Gisteren werken ik thuis.","Gisteren gewerkt ik thuis."],"Gisteren werkte ik thuis.","past-tense"),
AssessmentQuestion("nl-a2-010","vocabulary","A2","Wat betekent 'afspraak'?",["een afgesproken moment","een vertraging","een gebouw","een voertuig"],"een afgesproken moment"),
AssessmentQuestion("nl-b1-009","grammar","B1","Kies de correcte voorwaardelijke zin.",["Als ik tijd had, zou ik reizen.","Als ik tijd heb, zou ik gisteren reizen.","Als ik tijd had, reisde ik morgen.","Als ik tijd hebben, zou ik reizen."],"Als ik tijd had, zou ik reizen.","conditional"),
AssessmentQuestion("nl-b1-010","reading","B1","Lees: 'De vergadering werd uitgesteld omdat de directeur ziek was.' Waarom werd de vergadering uitgesteld?",["Omdat de directeur ziek was.","Omdat het kantoor gesloten was.","Omdat de trein vertraging had.","Omdat het een feestdag was."],"Omdat de directeur ziek was."),
AssessmentQuestion("nl-b2-009","grammar","B2","Kies de correcte concessieve constructie.",["Hoewel het regende, gingen we wandelen.","Hoewel het regende, we gingen wandelen.","Hoewel regende het, gingen we wandelen.","Hoewel het regende, we wandelen gingen."],"Hoewel het regende, gingen we wandelen.","concessive"),
AssessmentQuestion("nl-b2-010","vocabulary","B2","Wat betekent 'nuanceren'?",["een uitspraak preciezer en minder absoluut maken","een afspraak annuleren","een tekst vertalen","een rekening betalen"],"een uitspraak preciezer en minder absoluut maken"),
AssessmentQuestion("nl-c1-009","grammar","C1","Kies de meest natuurlijke academische formulering.",["De bevindingen suggereren dat verdere analyse noodzakelijk is.","De bevindingen suggereren dat verdere analyse noodzakelijk zijn.","De bevindingen suggereert verdere analyse noodzakelijk is.","De bevindingen suggereren verdere analyse dat noodzakelijk."],"De bevindingen suggereren dat verdere analyse noodzakelijk is.","academic-language"),
AssessmentQuestion("nl-c1-010","reading","C1","Lees: 'De gegevens zijn consistent met de hypothese, maar leveren geen definitief bewijs.' Wat wordt niet geleverd?",["Definitief bewijs.","Gegevens.","Een hypothese.","Een vergelijking."],"Definitief bewijs."),
AssessmentQuestion("nl-c2-009","grammar","C2","Welke formulering markeert een voorbehoud het duidelijkst?",["Voor zover de beschikbare gegevens toelaten, lijkt deze conclusie gerechtvaardigd.","Deze conclusie is zonder enige twijfel altijd juist.","De conclusie kan onder geen enkele voorwaarde veranderen.","Er is geen reden om alternatieve verklaringen te onderzoeken."],"Voor zover de beschikbare gegevens toelaten, lijkt deze conclusie gerechtvaardigd.","epistemic-modality"),
AssessmentQuestion("nl-c2-010","vocabulary","C2","Wat betekent 'voorbehoud' in een argumentatie?",["een beperking of kanttekening bij een bewering","een definitief bewijs","een herhaling van dezelfde zin","een informele begroeting"],"een beperking of kanttekening bij een bewering")
]
