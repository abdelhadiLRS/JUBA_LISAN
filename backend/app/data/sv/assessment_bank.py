from app.data._types import AssessmentQuestion

ASSESSMENT_BANK = [
    AssessmentQuestion("sv-a1-001","grammar","A1","Välj rätt mening.",["Jag är student.","Jag student är.","Är jag student är.","Jag är en studentar."],"Jag är student."),
    AssessmentQuestion("sv-a1-002","grammar","A1","Vilken form är bestämd?",["bok","böcker","boken","bokar"],"boken"),
    AssessmentQuestion("sv-a1-003","vocabulary","A1","Vad betyder ”tack”? ",["en artig hälsning när man får något","en fråga om namn","ett sätt att säga god natt","en plats i staden"],"en artig hälsning när man får något"),
    AssessmentQuestion("sv-a1-004","reading","A1","Läs: ”Anna bor i Malmö.” Var bor Anna?",["Stockholm","Göteborg","Malmö","Uppsala"],"Malmö"),

    AssessmentQuestion("sv-a2-001","grammar","A2","Vilken ordföljd är korrekt?",["Idag jag arbetar hemma.","Idag arbetar jag hemma.","Idag hemma arbetar jag.","Arbetar idag hemma jag."],"Idag arbetar jag hemma."),
    AssessmentQuestion("sv-a2-002","grammar","A2","Välj rätt bisats.",["Jag vet att han kommer inte.","Jag vet att han inte kommer.","Jag vet inte att han kommer.","Jag vet att inte han kommer."],"Jag vet att han inte kommer."),
    AssessmentQuestion("sv-a2-003","vocabulary","A2","Vad är en ”bokning”? ",["en reservation som man har gjort","en försening av ett tåg","en biljettmaskin","en adress till en plats"],"en reservation som man har gjort"),
    AssessmentQuestion("sv-a2-004","reading","A2","Läs: ”Tåget avgår klockan åtta men är tio minuter försenat.” När skulle tåget avgå?",["07:50","08:00","08:10","08:20"],"08:00"),

    AssessmentQuestion("sv-b1-001","grammar","B1","Välj korrekt perfektform.",["Jag har läser boken.","Jag har läst boken.","Jag hade läser boken.","Jag är läst boken."],"Jag har läst boken."),
    AssessmentQuestion("sv-b1-002","grammar","B1","Vilken mening är passiv?",["De publicerar rapporten.","Rapporten publiceras idag.","De har en rapport.","Rapporten är intressant."],"Rapporten publiceras idag."),
    AssessmentQuestion("sv-b1-003","vocabulary","B1","Vad betyder ”belägg” i en argumenterande text?",["underlag som stöder ett påstående","en lön som betalas varje månad","en resa som planeras","ett schema för en arbetsdag"],"underlag som stöder ett påstående"),
    AssessmentQuestion("sv-b1-004","reading","B1","Läs: ”Rapporten visar ett samband mellan sömn och prestation.” Vad visar rapporten?",["En resa","Ett samband","En lag","En intervju"],"Ett samband"),

    AssessmentQuestion("sv-b2-001","grammar","B2","Välj den kontrafaktiska formuleringen.",["Om jag vet skulle jag komma.","Om jag visste skulle jag komma.","Om jag visste kommer jag.","Om jag vet kom jag."],"Om jag visste skulle jag komma."),
    AssessmentQuestion("sv-b2-002","grammar","B2","Vilken koncessiv konstruktion är korrekt?",["Även om det regnar går vi.","Även det regnar om går vi.","Om även regnar det går vi.","Det regnar även om går vi."],"Även om det regnar går vi."),
    AssessmentQuestion("sv-b2-003","vocabulary","B2","Vad betyder ”nyansera”? ",["göra ett påstående mer detaljerat och balanserat","avsluta en diskussion","översätta en text ord för ord","förkorta en mening"],"göra ett påstående mer detaljerat och balanserat"),
    AssessmentQuestion("sv-b2-004","reading","B2","Läs: ”Förslaget har fördelar, men det finns också en viktig invändning.” Vad nämns?",["Bara fördelar","En invändning","Ingen bedömning","En resa"],"En invändning"),

    AssessmentQuestion("sv-c1-001","grammar","C1","Vilket uttryck markerar försiktighet?",["Det är bevisat att","Resultaten tyder på att","Det är alltid så att","Det kan aldrig vara"],"Resultaten tyder på att"),
    AssessmentQuestion("sv-c1-002","grammar","C1","Vilket uttryck passar bäst i ett formellt brev?",["Tjena!","Skulle ni kunna återkomma?","Vad händer?","Ses!"],"Skulle ni kunna återkomma?"),
    AssessmentQuestion("sv-c1-003","vocabulary","C1","Vad är en ”tolkningsram”? ",["ett perspektiv eller en modell för att förstå material","en tågbiljett","en löneform","en möteslokal"],"ett perspektiv eller en modell för att förstå material"),
    AssessmentQuestion("sv-c1-004","reading","C1","Läs: ”Resultaten bör tolkas med försiktighet eftersom urvalet var begränsat.” Varför behövs försiktighet?",["Urvalet var begränsat.","Resultaten saknas.","Studien var lång.","Språket var enkelt."],"Urvalet var begränsat."),

    AssessmentQuestion("sv-c2-001","grammar","C2","Vilken mening uttrycker ett kontrafaktiskt dåtidsvillkor korrekt?",["Om vi hade vetat det skulle vi ha agerat.","Om vi vet det skulle vi agera igår.","Om vi visste det har vi agerat.","Om vi hade vetat det agerar vi."],"Om vi hade vetat det skulle vi ha agerat."),
    AssessmentQuestion("sv-c2-002","grammar","C2","Vilken formulering är mest semantiskt försiktig?",["Det bevisar orsaken.","Det kan tyda på ett samband.","Det bevisar alltid allt.","Det är utan tvekan orsaken."],"Det kan tyda på ett samband."),
    AssessmentQuestion("sv-c2-003","vocabulary","C2","Vad betyder ”generaliserbarhet”? ",["möjligheten att överföra resultat till andra sammanhang","antalet deltagare i en studie","längden på en vetenskaplig text","skillnader i uttal mellan språk"],"möjligheten att överföra resultat till andra sammanhang"),
    AssessmentQuestion("sv-c2-004","reading","C2","Läs: ”Korrelationen är tydlig, men kausaliteten kan inte fastställas.” Vad kan inte fastställas?",["Korrelationen","Kausaliteten","Terminologin","Urvalet"],"Kausaliteten"),

    AssessmentQuestion("sv-a1-005","grammar","A1","Välj rätt fråga.",["Var bor du?","Var du bor?","Bor var du?","Var bor?"],"Var bor du?"),
    AssessmentQuestion("sv-a1-006","vocabulary","A1","Vad betyder ”äpple”? ",["en frukt","ett fordon","en byggnad","ett möbel"],"en frukt"),
    AssessmentQuestion("sv-a1-007","reading","A1","Läs: ”Erik bor i Uppsala.” Var bor Erik?",["Uppsala","Malmö","Göteborg","Lund"],"Uppsala"),
    AssessmentQuestion("sv-a1-008","grammar","A1","Välj rätt form.",["Hon har en bil.","Hon har ett bil.","Hon ha en bil.","Hon har en bilar."],"Hon har en bil."),
    AssessmentQuestion("sv-a2-005","grammar","A2","Välj korrekt perfektform.",["Jag har ätit.","Jag har äta.","Jag har åt.","Jag äter har."],"Jag har ätit."),
    AssessmentQuestion("sv-a2-006","vocabulary","A2","Vad betyder ”försening”? ",["något som kommer senare än planerat","en bokning","en adress","en betalning"],"något som kommer senare än planerat"),
    AssessmentQuestion("sv-a2-007","reading","A2","Läs: ”Butiken stänger klockan sex.” När stänger butiken?",["Klockan fem.","Klockan sex.","Klockan sju.","Klockan åtta."],"Klockan sex."),
    AssessmentQuestion("sv-a2-008","grammar","A2","Välj rätt preposition.",["Jag bor i Sverige.","Jag bor på Sverige.","Jag bor till Sverige.","Jag bor vid Sverige."],"Jag bor i Sverige."),
    AssessmentQuestion("sv-b1-005","grammar","B1","Välj korrekt relativsats.",["Det är boken som jag köpte.","Det är boken som jag köpt.","Det är boken jag som köpte.","Det är boken som köpte jag."],"Det är boken som jag köpte."),
    AssessmentQuestion("sv-b1-006","vocabulary","B1","Vad betyder ”utmaning”? ",["något som kräver en insats","en belöning","en semester","en adress"],"något som kräver en insats"),
    AssessmentQuestion("sv-b1-007","reading","B1","Läs: ”Mötet flyttades eftersom chefen var sjuk.” Varför flyttades mötet?",["Eftersom chefen var sjuk.","Eftersom lokalen var stängd.","Eftersom tåget var försenat.","Eftersom deltagarna var lediga."],"Eftersom chefen var sjuk."),
    AssessmentQuestion("sv-b1-008","grammar","B1","Välj korrekt ordföljd.",["I går köpte jag en ny dator.","I går jag köpte en ny dator.","I går köpte en ny dator jag.","I går en ny dator köpte jag."],"I går köpte jag en ny dator."),
    AssessmentQuestion("sv-b2-005","grammar","B2","Välj korrekt koncessiv bisats.",["Trots att det regnade gick vi en promenad.","Trots att det regnade vi gick en promenad.","Trots regnade det gick vi en promenad.","Trots att det regnade vi en promenad gick."],"Trots att det regnade gick vi en promenad."),
    AssessmentQuestion("sv-b2-006","vocabulary","B2","Vad betyder ”förutsäga”? ",["att säga vad man tror kommer att hända","att förklara något från förr","att ändra en regel","att ställa in ett möte"],"att säga vad man tror kommer att hända"),
    AssessmentQuestion("sv-b2-007","reading","B2","Läs: ”Resultaten visar en tydlig tendens, men de bör tolkas med försiktighet.” Vad rekommenderas?",["Försiktig tolkning av resultaten.","Att ignorera resultaten.","Att ändra alla resultat.","Att avsluta undersökningen."],"Försiktig tolkning av resultaten."),
    AssessmentQuestion("sv-b2-008","grammar","B2","Välj korrekt indirekt fråga.",["Jag vet inte när mötet börjar.","Jag vet inte när börjar mötet.","Jag vet inte när mötet börjar?","Jag vet inte mötet när börjar."],"Jag vet inte när mötet börjar."),
    AssessmentQuestion("sv-c1-005","grammar","C1","Välj den mest precisa formuleringen.",["Resultaten tyder på att effekten är begränsad.","Resultaten tyder att effekten är begränsad.","Resultaten tyder på effekten att är begränsad.","Resultaten tyder att effekten på är begränsad."],"Resultaten tyder på att effekten är begränsad."),
    AssessmentQuestion("sv-c1-006","vocabulary","C1","Vad betyder ”väsentlig”? ",["betydelsefull eller viktig","slumpmässig","tillfällig","informell"],"betydelsefull eller viktig"),
    AssessmentQuestion("sv-c1-007","reading","C1","Läs: ”Sambandet bevisar inte i sig ett orsakssamband.” Vad bevisar sambandet inte?",["Att det ena fenomenet orsakar det andra.","Att det finns data.","Att variablerna har ett samband.","Att en analys har gjorts."],"Att det ena fenomenet orsakar det andra."),
    AssessmentQuestion("sv-c1-008","grammar","C1","Välj korrekt passiv konstruktion.",["Studien genomfördes i tre steg.","Studien genomförde i tre steg.","Studien genomförts i tre steg.","Studien genomföra i tre steg."],"Studien genomfördes i tre steg."),
    AssessmentQuestion("sv-c2-005","grammar","C2","Vilken formulering uttrycker akademisk försiktighet?",["Det kan inte uteslutas att andra faktorer spelar en roll.","Andra faktorer spelar säkert ingen roll.","Det är bevisat utan undantag att andra faktorer är irrelevanta.","Det finns ingen anledning att undersöka andra faktorer."],"Det kan inte uteslutas att andra faktorer spelar en roll."),
    AssessmentQuestion("sv-c2-006","vocabulary","C2","Vad betyder ”tvetydig”? ",["som kan förstås på mer än ett sätt","som är helt tydlig","som är mycket kort","som är lätt att mäta"],"som kan förstås på mer än ett sätt"),
    AssessmentQuestion("sv-c2-007","reading","C2","Läs: ”Argumentet är övertygande, förutsatt att det bakomliggande antagandet håller.” Vad beror bedömningen på?",["Att det bakomliggande antagandet håller.","Att argumentet är kort.","Att texten är informell.","Att uppgifterna är gamla."],"Att det bakomliggande antagandet håller."),
    AssessmentQuestion("sv-c2-008","grammar","C2","Välj den mest idiomatiska akademiska formuleringen.",["Trots begränsningarna bör resultaten inte avfärdas utan vidare.","Trots begränsningarna bör resultaten inte avfärda utan vidare.","Trots begränsningarna resultaten bör inte avfärdas.","Trots av begränsningarna bör resultaten inte avfärdas."],"Trots begränsningarna bör resultaten inte avfärdas utan vidare.")
]
