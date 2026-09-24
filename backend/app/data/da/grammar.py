"""Danish grammar topics with learner-facing content in Danish."""
from app.data._types import GrammarTopic, GrammarExample
_DATA={
"A1":[("personlige-pronominer","Personlige pronominer","Subjektspronominer bruges til at angive hvem der handler.","Jeg hedder Anna.","jeg, du, han, hun, vi, I, de"),
("at-vaere","Verbet at være","Verbet være bruges til identitet, tilstand og egenskaber.","Jeg er studerende.","subjekt + er + prædikativ"),
("bestemt-form","Bestemt og ubestemt form","Substantiver skelner mellem ubestemt og bestemt form.","Jeg har en bog. Bogen er ny.","en bog / bogen"),
("hovedsaetning","Ordstilling i hovedsætninger","Det finitte verbum står normalt på anden plads.","I dag arbejder jeg hjemme.","led 1 + verbum + subjekt")],
"A2":[("datid","Datid","Datid bruges om afsluttede handlinger i fortiden.","I går arbejdede jeg hjemme.","subjekt + datidsverbum"),
("modalverber","Modalverber","Modalverber udtrykker mulighed, nødvendighed eller vilje.","Jeg skal arbejde i morgen.","modalverbum + infinitiv"),
("refleksive-verber","Refleksive verber","Refleksive pronominer viser at handlingen vender tilbage til subjektet.","Hun glæder sig.","subjekt + verbum + refleksivt pronomen"),
("sammenligninger","Sammenligninger","Komparativ og superlativ bruges til at sammenligne.","Denne bog er bedre end den anden.","mere / bedre / bedst")],
"B1":[("foer nutid","Førnutid","Førnutid forbinder en tidligere handling med nutiden.","Jeg har læst bogen.","har + perfektum participium"),
("fremtid","Fremtid","Fremtid kan udtrykkes med vil, skal eller en tidsangivelse.","Jeg vil rejse i morgen.","vil/skal + infinitiv"),
("ledsaetninger","Ledsætninger","Ledsætninger har en anden ordstilling end hovedsætninger.","Jeg ved, at hun kommer.","konjunktion + subjekt + adverbial + verbum"),
("relative-pronominer","Relative pronominer","Relative pronominer forbinder en beskrivelse med et navneord.","Det er bogen, som jeg læser.","som / der")],
"B2":[("passiv","Passiv","Passiv fremhæver handlingen eller resultatet frem for aktøren.","Døren åbnes klokken otte.","blive + participium"),
("betingelsessaetninger","Betingelsessætninger","Betingelser beskriver mulige eller hypotetiske situationer.","Hvis jeg havde tid, ville jeg rejse.","hvis + ledsætning"),
("indirekte-tale","Indirekte tale","Indirekte tale gengiver en anden persons udsagn.","Hun sagde, at hun kom senere.","sige + at + ledsætning"),
("konjunktioner","Avancerede konjunktioner","Konjunktioner binder ideer sammen og viser logiske relationer.","Selvom det regner, går vi ud.","selvom / derfor / mens")],
"C1":[("nominalisering","Nominalisering","Nominalisering gør verbale handlinger til abstrakte substantiver.","Beslutningen blev offentliggjort.","verbum → substantiv"),
("participier","Participier","Participier kan fungere som adjektiver og indgå i komplekse konstruktioner.","De ankomne gæster ventede.","præsens/perfektum participium"),
("kompleks-ledsaetning","Kompleks ledsætningsstruktur","Flere ledsætninger kan kombineres for præcis argumentation.","Jeg ved, at hun tror, at han kommer.","indlejrede ledsætninger"),
("tekstkohæsion","Tekstlig kohæsion","Referencer og forbindelsesord skaber sammenhæng i en tekst.","Dette viser, at problemet er større.","reference + forbindelsesled")],
"C2":[("inversion-fokus","Inversion og fokus","Ændret ordstilling kan fremhæve bestemte informationer.","Kun senere forstod jeg problemet.","fokusled + verbum + subjekt"),
("registerskift","Registerskift","Ordvalg og syntaks ændres efter situation og modtager.","Vi må drøfte sagen nærmere.","formelt / neutralt / uformelt"),
("retoriske-konstruktioner","Retoriske konstruktioner","Retoriske spørgsmål og gentagelser styrer læserens opmærksomhed.","Hvem kan ignorere dette?","spørgsmål / parallelisme"),
("syntaktisk-variation","Syntaktisk variation","Variation i sætningslængde og struktur giver præcision og rytme.","På trods af kritikken fortsatte projektet.","varieret syntaks")]
]}
GRAMMAR_TOPICS=[]
for level,rows in _DATA.items():
    for slug,title,summary,example,structure in rows:
        GRAMMAR_TOPICS.append(GrammarTopic(slug=slug,title=title,level=level,category="dansk grammatik",summary=summary,explanation=summary,structure=structure,rules=[summary],examples=[GrammarExample(text=example)],common_mistakes=[],related=[]))
