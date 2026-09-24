from app.data._types import CurriculumUnit

CURRICULUM = {
    "A1": [
        CurriculumUnit("sv-a1-1","A1",1,"Hälsa och presentationer",["personliga pronomen","vara och ha"],["sv-a1-greetings","sv-a1-identity"],["grammar","vocabulary","reading","listening"],["Presentera dig själv och andra","Förstå enkla hälsningsfraser"],2),
        CurriculumUnit("sv-a1-2","A1",2,"Vardag och familj",["bestämdhet","plural"],["sv-a1-family","sv-a1-daily"],["grammar","vocabulary","reading","writing"],["Beskriva familj och vardag","Använda vanliga substantiv"],2),
        CurriculumUnit("sv-a1-3","A1",3,"Tid och plats",["presens","frågeord"],["sv-a1-time","sv-a1-city"],["grammar","vocabulary","reading","listening"],["Berätta om tid och plats","Ställa enkla frågor"],2),
        CurriculumUnit("sv-a1-4","A1",4,"Mat och inköp",["negation","adjektiv"],["sv-a1-food","sv-a1-shopping"],["grammar","vocabulary","speaking","review"],["Handla och beställa mat","Uttrycka enkla behov"],2),
    ],
    "A2": [
        CurriculumUnit("sv-a2-1","A2",1,"Hem och område",["preteritum","adverb"],["sv-a2-home","sv-a2-neighborhood"],["grammar","vocabulary","reading","writing"],["Beskriva hem och omgivning","Berätta om tidigare händelser"],2),
        CurriculumUnit("sv-a2-2","A2",2,"Resor och transport",["futurum","modalverb"],["sv-a2-travel","sv-a2-transport"],["grammar","vocabulary","listening","speaking"],["Planera resor","Uttrycka möjlighet och skyldighet"],2),
        CurriculumUnit("sv-a2-3","A2",3,"Hälsa och fritid",["komparation","reflexiva verb"],["sv-a2-health","sv-a2-leisure"],["grammar","vocabulary","reading","listening"],["Beskriva hälsa och vanor","Jämföra aktiviteter"],2),
        CurriculumUnit("sv-a2-4","A2",4,"Arbete och service",["ordföljd","bisatser"],["sv-a2-work","sv-a2-service"],["grammar","vocabulary","writing","review"],["Kommunicera på arbetsplatsen","Skriva enkla sammanhängande texter"],2),
    ],
    "B1": [
        CurriculumUnit("sv-b1-1","B1",1,"Studier och mål",["perfekt","pluskvamperfekt"],["sv-b1-education","sv-b1-goals"],["grammar","vocabulary","reading","writing"],["Tala om erfarenheter","Beskriva mål och planer"],3),
        CurriculumUnit("sv-b1-2","B1",2,"Arbetsliv",["relativa satser","satsadverbial"],["sv-b1-career","sv-b1-workplace"],["grammar","vocabulary","reading","speaking"],["Beskriva arbetsuppgifter","Förstå längre sakprosatexter"],3),
        CurriculumUnit("sv-b1-3","B1",3,"Samhälle och media",["passiv konstruktion","konnektorer"],["sv-b1-media","sv-b1-society"],["grammar","vocabulary","listening","writing"],["Sammanfatta information","Förklara orsak och konsekvens"],3),
        CurriculumUnit("sv-b1-4","B1",4,"Relationer och erfarenheter",["indirekt tal","konjunktioner"],["sv-b1-relationships","sv-b1-experiences"],["grammar","vocabulary","speaking","review"],["Berätta sammanhängande","Återge andras åsikter"],3),
    ],
    "B2": [
        CurriculumUnit("sv-b2-1","B2",1,"Argumentation",["konditionalis","koncessiva satser"],["sv-b2-argument","sv-b2-debate"],["grammar","vocabulary","reading","speaking"],["Argumentera nyanserat","Bemöta motargument"],3),
        CurriculumUnit("sv-b2-2","B2",2,"Kultur och identitet",["participfraser","nominalisering"],["sv-b2-culture","sv-b2-identity"],["grammar","vocabulary","reading","writing"],["Analysera kulturella texter","Variera stil och struktur"],3),
        CurriculumUnit("sv-b2-3","B2",3,"Ekonomi och arbetsliv",["verbfraser","verbstyrning"],["sv-b2-economy","sv-b2-professional"],["grammar","vocabulary","listening","speaking"],["Diskutera ekonomi","Hantera professionella samtal"],3),
        CurriculumUnit("sv-b2-4","B2",4,"Problem och lösningar",["komplex ordföljd","textbindning"],["sv-b2-problems","sv-b2-solutions"],["grammar","vocabulary","writing","review"],["Föreslå lösningar","Skriva välstrukturerade argument"],3),
    ],
    "C1": [
        CurriculumUnit("sv-c1-1","C1",1,"Akademiskt språk",["nominal stil","formella bisatser"],["sv-c1-academic","sv-c1-research"],["grammar","vocabulary","reading","writing"],["Förstå akademiska texter","Formulera precisa resonemang"],3),
        CurriculumUnit("sv-c1-2","C1",2,"Professionell kommunikation",["formellt register","hövlighetsstrategier"],["sv-c1-professional","sv-c1-meetings"],["grammar","vocabulary","speaking","listening"],["Leda professionella samtal","Anpassa språk efter mottagare"],3),
        CurriculumUnit("sv-c1-3","C1",3,"Samhällsanalys",["modalitet","refererande språk"],["sv-c1-society","sv-c1-analysis"],["grammar","vocabulary","reading","writing"],["Analysera samhällsfrågor","Markera grad av säkerhet"],3),
        CurriculumUnit("sv-c1-4","C1",4,"Retorik och stil",["retoriska strukturer","kohesion"],["sv-c1-rhetoric","sv-c1-style"],["grammar","vocabulary","speaking","review"],["Bygga övertygande resonemang","Kontrollera stil och textbindning"],3),
    ],
    "C2": [
        CurriculumUnit("sv-c2-1","C2",1,"Semantisk precision",["lexikal aspekt","betydelsenyans"],["sv-c2-nuance","sv-c2-semantics"],["grammar","vocabulary","reading","writing"],["Uttrycka mycket fina betydelseskillnader","Välja exakt terminologi"],3),
        CurriculumUnit("sv-c2-2","C2",2,"Avancerad argumentation",["villkorsnyanser","koncessiv nyans"],["sv-c2-argument","sv-c2-debate"],["grammar","vocabulary","speaking","reading"],["Hantera komplexa argument","Diskutera abstrakta frågor"],3),
        CurriculumUnit("sv-c2-3","C2",3,"Fackspråk och akademi",["specialiserade nominalfraser","tät syntax"],["sv-c2-specialized","sv-c2-academic"],["grammar","vocabulary","reading","writing"],["Arbeta med fackspråk","Skriva täta akademiska texter"],3),
        CurriculumUnit("sv-c2-4","C2",4,"Syntes och uttryck",["diskursmarkörer","stilistisk precision"],["sv-c2-synthesis","sv-c2-expression"],["grammar","vocabulary","speaking","writing","review"],["Syntetisera komplex information","Behärska stilistiska nyanser"],3),
    ],
}
