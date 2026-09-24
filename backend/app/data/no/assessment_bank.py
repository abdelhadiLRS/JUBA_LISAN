from app.data._types import AssessmentQuestion

ASSESSMENT_BANK = [
AssessmentQuestion(id="no-a1-001",skill="grammar",difficulty="A1",question="Velg riktig setning.",options=["Jeg er student.","Jeg student er.","Er jeg student er.","Student jeg er."],correct="Jeg er student."),
AssessmentQuestion(id="no-a1-002",skill="vocabulary",difficulty="A1",question="Hva betyr «takk»?",options=["thanks","tomorrow","school","family"],correct="thanks"),
AssessmentQuestion(id="no-a1-003",skill="grammar",difficulty="A1",question="Velg riktig negasjon.",options=["Jeg ikke snakker norsk.","Jeg snakker ikke norsk.","Ikke jeg snakker norsk.","Jeg snakker norsk ikke."],correct="Jeg snakker ikke norsk."),
AssessmentQuestion(id="no-a1-004",skill="reading",difficulty="A1",question="«Jeg bor i Oslo.» Hvor bor personen?",options=["Bergen","Oslo","Trondheim","Tromsø"],correct="Oslo"),

AssessmentQuestion(id="no-a2-001",skill="grammar",difficulty="A2",question="Velg riktig preteritum.",options=["I går går jeg hjem.","I går gikk jeg hjem.","I går gå jeg hjem.","I går har gikk jeg hjem."],correct="I går gikk jeg hjem."),
AssessmentQuestion(id="no-a2-002",skill="grammar",difficulty="A2",question="Velg riktig perfektum.",options=["Jeg har spist.","Jeg har spise.","Jeg spiste har.","Jeg spise har."],correct="Jeg har spist."),
AssessmentQuestion(id="no-a2-003",skill="vocabulary",difficulty="A2",question="Hva betyr «forsinket»?",options=["delayed","cheap","healthy","quiet"],correct="delayed"),
AssessmentQuestion(id="no-a2-004",skill="reading",difficulty="A2",question="«Toget går klokken åtte, men det er forsinket.» Når skulle toget gå?",options=["06:00","07:00","08:00","09:00"],correct="08:00"),

AssessmentQuestion(id="no-b1-001",skill="grammar",difficulty="B1",question="Velg riktig leddsetning.",options=["Jeg tror at han kommer.","Jeg tror han at kommer.","Jeg at tror han kommer.","Jeg tror kommer at han."],correct="Jeg tror at han kommer."),
AssessmentQuestion(id="no-b1-002",skill="grammar",difficulty="B1",question="Velg riktig passivform.",options=["Døren åpner klokken åtte.","Døren åpnes klokken åtte.","Døren åpned klokken åtte.","Døren blir åpne klokken åtte."],correct="Døren åpnes klokken åtte."),
AssessmentQuestion(id="no-b1-003",skill="vocabulary",difficulty="B1",question="Hva betyr «innvending»?",options=["objection","salary","journey","holiday"],correct="objection"),
AssessmentQuestion(id="no-b1-004",skill="reading",difficulty="B1",question="«Prosjektet ble forsinket fordi leveransen kom sent.» Hvorfor ble prosjektet forsinket?",options=["Fordi møtet ble avlyst.","Fordi leveransen kom sent.","Fordi planen var ny.","Fordi kontoret var stengt."],correct="Fordi leveransen kom sent."),

AssessmentQuestion(id="no-b2-001",skill="grammar",difficulty="B2",question="Velg riktig innrømmende konstruksjon.",options=["Selv om det regner, går vi ut.","Selv det regner om, går vi ut.","Om selv det regner, går vi ut.","Det regner selv om går vi ut."],correct="Selv om det regner, går vi ut."),
AssessmentQuestion(id="no-b2-002",skill="grammar",difficulty="B2",question="Velg riktig verbvalg.",options=["Vi må venter på svaret.","Vi må vente på svaret.","Vi må ventet på svaret.","Vi må å vente på svaret."],correct="Vi må vente på svaret."),
AssessmentQuestion(id="no-b2-003",skill="vocabulary",difficulty="B2",question="Hva betyr «bærekraftig»?",options=["sustainable","temporary","uncertain","private"],correct="sustainable"),
AssessmentQuestion(id="no-b2-004",skill="reading",difficulty="B2",question="«Tiltaket er kostbart, men det kan begrense risikoen.» Hva er fordelen?",options=["Det reduserer risikoen.","Det gjør tiltaket billigere.","Det fjerner alle kostnader.","Det øker usikkerheten."],correct="Det reduserer risikoen."),

AssessmentQuestion(id="no-c1-001",skill="grammar",difficulty="C1",question="Velg den mest akademiske formuleringen.",options=["Resultatet kan tyde på en effekt.","Resultatet viser sikkert alt.","Resultatet er bare bra.","Resultatet gjør en ting."],correct="Resultatet kan tyde på en effekt."),
AssessmentQuestion(id="no-c1-002",skill="grammar",difficulty="C1",question="Velg riktig refererende uttrykk.",options=["Studien viser at effekten er begrenset.","Studien viser effekten er begrenset at.","Studien at viser effekten er begrenset.","Studien viser at er effekten begrenset."],correct="Studien viser at effekten er begrenset."),
AssessmentQuestion(id="no-c1-003",skill="vocabulary",difficulty="C1",question="Hva betyr «etterprøvbar»?",options=["verifiable","emotional","expensive","informal"],correct="verifiable"),
AssessmentQuestion(id="no-c1-004",skill="reading",difficulty="C1",question="«Datagrunnlaget er begrenset, og funnene bør derfor tolkes med varsomhet.» Hva er anbefalingen?",options=["Ignorere funnene.","Tolke funnene forsiktig.","Øke kostnadene.","Avslutte studien."],correct="Tolke funnene forsiktig."),

AssessmentQuestion(id="no-c2-001",skill="grammar",difficulty="C2",question="Velg riktig kontrafaktisk konstruksjon.",options=["Hvis jeg hadde visst det, ville jeg sagt fra.","Hvis jeg hadde vite det, ville jeg sagt fra.","Hvis jeg visste det, hadde jeg sagt fra i går.","Hvis jeg har visst det, ville jeg sagt fra."],correct="Hvis jeg hadde visst det, ville jeg sagt fra."),
AssessmentQuestion(id="no-c2-002",skill="grammar",difficulty="C2",question="Velg formuleringen med tydelig evidensstyrke.",options=["Dataene antyder en sammenheng.","Dataene fastslår alle årsaker.","Dataene beviser nødvendigvis alt.","Dataene betyr ingenting."],correct="Dataene antyder en sammenheng."),
AssessmentQuestion(id="no-c2-003",skill="vocabulary",difficulty="C2",question="Hva betyr «forbehold» i akademisk språk?",options=["reservation or qualification","celebration","transport","salary"],correct="reservation or qualification"),
AssessmentQuestion(id="no-c2-004",skill="reading",difficulty="C2",question="«Samlet sett peker funnene i samme retning, men datagrunnlaget er for begrenset til en entydig konklusjon.» Hva er hovedpoenget?",options=["Funnene er lovende, men konklusjonen må være forsiktig.","Det finnes ingen funn.","Datagrunnlaget er perfekt.","Konklusjonen er helt sikker."],correct="Funnene er lovende, men konklusjonen må være forsiktig."),
]
