from app.data._types import PhrasebookCategory, PhrasebookEntry

def _c(id: str, level: str, situation: str, phrases: list[tuple[str,str,str]]) -> PhrasebookCategory:
    return PhrasebookCategory(id=id, level=level, situation=situation, icon="•", phrases=[PhrasebookEntry(text=t, context=c, register=r, unit_ref=None) for t,c,r in phrases])

PHRASEBOOK_CATEGORIES = [
_c("no-a1-greetings","A1","Hilsener",[("Hei!","møte noen","neutral"),("Hyggelig å møte deg.","første møte","neutral"),("Hvordan går det?","uformell samtale","neutral"),("Det går bra, takk.","svare på hilsen","neutral")]),
_c("no-a1-introduction","A1","Presentasjon",[("Jeg heter …","si navnet ditt","neutral"),("Jeg kommer fra …","fortelle opprinnelse","neutral"),("Jeg bor i …","fortelle bosted","neutral"),("Jeg lærer norsk.","fortelle hva du lærer","neutral")]),
_c("no-a1-daily","A1","Hverdag",[("Hva gjør du i dag?","spørre om planer","neutral"),("Jeg skal på jobb.","fortelle plan","neutral"),("Jeg har ikke tid.","avslå en avtale","neutral"),("Vi sees i morgen.","avslutte en samtale","neutral")]),

_c("no-a2-travel","A2","Reise",[("Hvor er stasjonen?","finne transport","neutral"),("Når går toget?","spørre om avgang","neutral"),("Jeg vil gjerne kjøpe en billett.","kjøpe billett","polite"),("Er toget forsinket?","spørre om status","neutral")]),
_c("no-a2-health","A2","Helse",[("Jeg føler meg ikke bra.","beskrive helse","neutral"),("Jeg har vondt i …","beskrive smerte","neutral"),("Kan jeg få en time?","bestille time","polite"),("Hvor lenge har du vært syk?","helseundersøkelse","neutral")]),
_c("no-a2-service","A2","Service",[("Kan du hjelpe meg?","be om hjelp","polite"),("Jeg vil gjerne bestille.","bestille","polite"),("Kan jeg betale med kort?","betaling","neutral"),("Kan jeg få kvitteringen?","butikk eller service","neutral")]),

_c("no-b1-work","B1","Arbeid",[("Kan vi ta dette på møtet?","flytte diskusjon til møte","neutral"),("Jeg følger opp saken.","arbeidsoppfølging","professional"),("Jeg sender det i løpet av dagen.","love levering","professional"),("La oss finne en løsning.","problemløsning","neutral")]),
_c("no-b1-opinions","B1","Meninger",[("Etter min mening …","uttrykke mening","neutral"),("Jeg er enig i at …","vise enighet","neutral"),("Jeg er ikke helt enig.","vise uenighet høflig","neutral"),("Det kommer an på.","nyansere svar","neutral")]),
_c("no-b1-social","B1","Sosiale situasjoner",[("Hva synes du om det?","be om mening","neutral"),("Det høres interessant ut.","reagere positivt","neutral"),("Jeg skjønner hva du mener.","vise forståelse","neutral"),("Kan du forklare litt mer?","be om utdyping","neutral")]),

_c("no-b2-debate","B2","Debatt",[("Jeg vil gjerne nyansere dette.","presisere argument","professional"),("Et viktig motargument er …","presentere innvending","professional"),("Det er et godt poeng, men …","respondere høflig","neutral"),("Dette bygger på antakelsen om at …","analysere premiss","professional")]),
_c("no-b2-meetings","B2","Profesjonelle møter",[("Kan vi avklare dette først?","styre diskusjon","professional"),("Jeg foreslår at vi …","foreslå tiltak","professional"),("La oss oppsummere beslutningen.","avslutte punkt","professional"),("Hva er neste steg?","avklare oppfølging","professional")]),
_c("no-b2-formal","B2","Formell kommunikasjon",[("Vi ber om at saken vurderes.","formell forespørsel","formal"),("Vi viser til tidligere korrespondanse.","formelt brev","formal"),("Saken er fortsatt under behandling.","statusmelding","formal"),("Vi kommer tilbake med en avklaring.","formell oppfølging","formal")]),

_c("no-c1-academic","C1","Akademisk kommunikasjon",[("Funnene kan tyde på at …","presentere forsiktig tolkning","academic"),("Dette støttes av …","knytte påstand til evidens","academic"),("Det bør imidlertid bemerkes at …","presentere begrensning","academic"),("Samlet sett peker resultatene mot …","oppsummere funn","academic")]),
_c("no-c1-professional","C1","Ledelse og samarbeid",[("Kunne du utdype dette?","be om mer informasjon","professional"),("Jeg foreslår at vi vurderer alternativet.","forslag i møte","professional"),("Dette bør avklares før vi går videre.","risiko eller avhengighet","professional"),("Jeg vil gjerne understreke at …","fremheve poeng","professional")]),
_c("no-c1-rhetoric","C1","Retorikk",[("På den ene siden …, på den andre siden …","balansere perspektiver","formal"),("Det er likevel grunn til å spørre om …","introdusere innvending","formal"),("Dette perspektivet overser imidlertid …","kritisere et argument","formal"),("Det avgjørende spørsmålet er …","ramme inn diskusjon","formal")]),

_c("no-c2-nuance","C2","Semantisk presisjon",[("Jeg vil presisere hva jeg mener med …","definere begrep","academic"),("Dette antyder snarere enn fastslår at …","markere evidensstyrke","academic"),("Formuleringen kan tolkes på flere måter.","peke på tvetydighet","academic"),("I den grad dette er relevant …","avgrense påstand","formal")]),
_c("no-c2-argument","C2","Avansert argumentasjon",[("Dette følger ikke nødvendigvis av premisset.","vurdere slutning","academic"),("Argumentet forutsetter at …","identifisere premiss","academic"),("Innvendingen kan imidlertid besvares ved å …","svare på motargument","formal"),("Samlet sett er evidensen utilstrekkelig til å fastslå …","konkludere forsiktig","academic")]),
_c("no-c2-synthesis","C2","Syntese og formidling",[("Samlet sett peker funnene i samme retning.","syntetisere kilder","academic"),("På dette grunnlaget kan vi konkludere med at …","konklusjon","formal"),("Det er grunn til å anta at …","forsiktig slutning","academic"),("Like fullt bør følgende forbehold nevnes.","presentere begrensning","formal")]),
]
