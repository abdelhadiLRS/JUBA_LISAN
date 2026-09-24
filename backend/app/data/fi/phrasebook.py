"""Finnish phrasebook for practical communication from A1 to C2."""
from app.data._types import PhrasebookCategory, PhrasebookEntry

def _c(i,level,situation,phrases):
    return PhrasebookCategory(id=i,level=level,situation=situation,icon="•",phrases=[PhrasebookEntry(text=t,context=c,register=r,unit_ref=i) for t,c,r in phrases])

PHRASEBOOK_CATEGORIES=[
_c("fi-a1-greetings","Tervehdykset ja esittely","A1",[("Hei!","greeting","neutral"),("Minun nimeni on Anna.","introducing yourself","neutral"),("Hauska tavata.","meeting someone","neutral")]),
_c("fi-a1-help","Apua ja selvennystä","A1",[("Voitko auttaa minua?","asking for help","neutral"),("En ymmärrä.","asking for clarification","neutral"),("Voitko puhua hitaammin?","asking someone to slow down","neutral")]),
_c("fi-a1-shopping","Ostokset","A1",[("Paljonko tämä maksaa?","asking a price","neutral"),("Haluan ostaa tämän.","buying an item","neutral"),("Voinko maksaa kortilla?","asking about payment","neutral")]),
_c("fi-a2-travel","Matkustaminen","A2",[("Missä on seuraava pysäkki?","asking about transport","neutral"),("Minulla on varaus.","checking a reservation","neutral"),("Mihin aikaan juna lähtee?","asking a departure time","neutral")]),
_c("fi-a2-health","Terveys","A2",[("Minulla on kuumetta.","describing a symptom","neutral"),("Tarvitsen lääkärin.","asking for medical help","neutral"),("Milloin voin tulla vastaanotolle?","asking for an appointment","neutral")]),
_c("fi-a2-work","Työ ja palvelut","A2",[("Voimmeko sopia ajan?","arranging an appointment","neutral"),("Lähetän tiedot sähköpostilla.","workplace communication","neutral"),("Tarvitsen apua tämän lomakkeen kanssa.","asking for service help","neutral")]),
_c("fi-b1-opinions","Mielipiteet","B1",[("Mielestäni tämä on hyvä ratkaisu.","giving an opinion","neutral"),("Olen samaa mieltä.","agreeing","neutral"),("En ole täysin samaa mieltä.","disagreeing politely","neutral")]),
_c("fi-b1-experiences","Kokemuksista kertominen","B1",[("Olen kokenut jotain vastaavaa.","sharing an experience","neutral"),("Se yllätti minut.","describing a reaction","neutral"),("Opin siitä paljon.","reflecting on experience","neutral")]),
_c("fi-b1-work","Työelämä","B1",[("Voimmeko keskustella tästä myöhemmin?","workplace discussion","neutral"),("Määräaika on perjantaina.","mentioning a deadline","neutral"),("Tarvitsen lisätietoja.","requesting information","neutral")]),
_c("fi-b2-debate","Väittely","B2",[("Ymmärrän näkökulmasi, mutta...","introducing a counterpoint","neutral"),("Tätä väitettä on syytä tarkastella tarkemmin.","challenging a claim","formal"),("Toisaalta voidaan ajatella, että...","introducing another perspective","neutral")]),
_c("fi-b2-meetings","Kokoukset","B2",[("Palataan tähän kohtaan myöhemmin.","deferring a topic","formal"),("Voisitko täsmentää tätä?","asking for precision","neutral"),("Ehdotan, että päätämme tästä tänään.","making a proposal","formal")]),
_c("fi-b2-problems","Ongelmat ja ratkaisut","B2",[("Ensimmäinen ongelma liittyy kustannuksiin.","framing a problem","formal"),("Ratkaisuna voisi olla...","proposing a solution","neutral"),("Meidän on arvioitava riskit.","discussing risk","formal")]),
_c("fi-c1-academic","Akateeminen keskustelu","C1",[("Tulokset viittaavat siihen, että...","presenting evidence","formal"),("Tämän perusteella voidaan päätellä, että...","drawing a conclusion","formal"),("Aiemman tutkimuksen mukaan...","attributing a claim","formal")]),
_c("fi-c1-professional","Ammatillinen viestintä","C1",[("Pyydän tarkentamaan tätä kohtaa.","formal clarification","formal"),("Voisitteko toimittaa asiakirjan perjantaihin mennessä?","formal request","formal"),("Ehdotan seuraavaa toimintatapaa.","professional proposal","formal")]),
_c("fi-c1-rhetoric","Retoriikka ja sävy","C1",[("On tärkeää huomata, että...","highlighting a point","formal"),("Toisaalta on syytä huomioida...","balancing an argument","formal"),("Näin ollen voidaan perustellusti todeta, että...","drawing a formal conclusion","formal")]),
_c("fi-c2-nuance","Merkityksen täsmentäminen","C2",[("Tämä ei välttämättä tarkoita, että...","qualifying a claim","formal"),("Ilmaus on tässä yhteydessä monitulkintainen.","discussing ambiguity","formal"),("Tarkemmin sanottuna...","refining a statement","formal")]),
_c("fi-c2-synthesis","Synteesi ja johtopäätökset","C2",[("Yhdessä tarkasteltuna nämä havainnot viittaavat siihen, että...","synthesizing evidence","formal"),("Lähteet täydentävät toisiaan, vaikka painotukset eroavat.","comparing sources","formal"),("Johtopäätös riippuu siitä, miten aineisto rajataan.","qualifying a conclusion","formal")]),
]
