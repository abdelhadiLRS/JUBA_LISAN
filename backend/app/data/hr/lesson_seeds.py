"""Curated Croatian A2-C2 lesson seeds for JUBA LISAN."""
from __future__ import annotations

from app.data.language_foundations.hr import CURRICULUM

_SKILLS = ("grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review")

_CONTENT = {
    "hr-a2-unit-1": {"text":"Idem u školu ujutro, a poslije nastave razgovaram s prijateljem u gradu.","words":[("škola","school","Idem u školu."),("prijatelj","friend","Razgovaram s prijateljem."),("grad","city","Živim u gradu.")],"questions":["Kamo osoba ide ujutro?","S kim razgovara poslije nastave?","Koji oblik pokazuje mjesto?"],"prompt":"Opišite kako se krećete svojim gradom i upotrijebite najmanje tri padežna oblika."},
    "hr-a2-unit-2": {"text":"Jučer sam posjetio baku. Ona je pripremila ručak, a poslije smo dugo razgovarali.","words":[("jučer","yesterday","Jučer sam čitao."),("posjetiti","to visit","Posjetio sam baku."),("pripremiti","to prepare","Ona je pripremila ručak.")],"questions":["Koga je osoba posjetila?","Što je baka pripremila?","Što su radili poslije ručka?"],"prompt":"Ispričajte što ste radili jučer i upotrijebite najmanje tri glagola u prošlom vremenu."},
    "hr-a2-unit-3": {"text":"Sljedeći tjedan putovat ću u Rijeku. Kupit ću kartu i posjetiti nekoliko muzeja.","words":[("sljedeći tjedan","next week","Sljedeći tjedan putovat ću."),("karta","ticket","Kupit ću kartu."),("posjetiti","to visit","Posjetit ću muzej.")],"questions":["Kada će osoba putovati?","Što će kupiti?","Što planira posjetiti?"],"prompt":"Opišite svoje planove za sljedeći tjedan koristeći buduće vrijeme."},
    "hr-b1-unit-1": {"text":"Dok sam čitao izvještaj, bilježio sam važne podatke. Kad sam ga pročitao, napisao sam kratak zaključak.","words":[("izvještaj","report","Čitam izvještaj."),("bilježiti","to note","Bilježio sam podatke."),("zaključak","conclusion","Napisao sam zaključak.")],"questions":["Što je osoba radila dok je čitala?","Što je učinila nakon čitanja izvještaja?","Koji glagol označava završenu radnju?"],"prompt":"Objasnite razliku između radnje koja traje i radnje koja je završena."},
    "hr-b1-unit-2": {"text":"Kad bih imao više vremena, upisao bih tečaj i učio novu vještinu. Tako bih mogao promijeniti posao.","words":[("tečaj","course","Upisao bih tečaj."),("vještina","skill","Učim novu vještinu."),("promijeniti","to change","Promijenio bih posao.")],"questions":["Što bi osoba učinila da ima više vremena?","Zašto bi upisala tečaj?","Koja rečenica izražava uvjet?"],"prompt":"Zamislite da imate više slobodnog vremena i opišite što biste učinili."},
    "hr-b1-unit-3": {"text":"Ovo je knjiga koju sam dobio od nastavnika. Čovjek koji ju je napisao bavi se obrazovanjem.","words":[("knjiga","book","Ovo je zanimljiva knjiga."),("nastavnik","teacher","Nastavnik je preporučio knjigu."),("obrazovanje","education","Obrazovanje je važno.")],"questions":["Tko je dao knjigu?","Tko je napisao knjigu?","Koja riječ povezuje imenicu s opisnom rečenicom?"],"prompt":"Opišite osobu, mjesto ili predmet koristeći najmanje dvije odnosne rečenice."},
    "hr-b2-unit-1": {"text":"Direktor je rekao da će sastanak početi u devet. Kolegica je pitala gdje će se održati.","words":[("sastanak","meeting","Sastanak počinje u devet."),("direktor","director","Direktor je dao obavijest."),("održati","to hold","Sastanak će se održati sutra.")],"questions":["Što je direktor rekao?","Što je kolegica pitala?","Kako su informacije prenesene neizravnim govorom?"],"prompt":"Prenesite tri rečenice druge osobe u neizravnom govoru."},
    "hr-b2-unit-2": {"text":"Projekt je skup, međutim donosi dugoročne koristi. Iako postoje rizici, tim smatra da treba nastaviti.","words":[("korist","benefit","Projekt donosi koristi."),("rizik","risk","Postoje određeni rizici."),("međutim","however","Projekt je skup, međutim koristan.")],"questions":["Koji je glavni kontrast?","Koji veznik uvodi suprotnost?","Zašto tim želi nastaviti projekt?"],"prompt":"Napišite argument u kojem ćete upotrijebiti iako, međutim i stoga."},
    "hr-c1-unit-1": {"text":"Na temelju rezultata istraživanja može se zaključiti da obrazovne navike utječu na dugoročni uspjeh. Ipak, nalaze treba tumačiti uzimajući u obzir ograničenja metodologije.","words":[("nalaz","finding","Glavni nalaz je važan."),("metodologija","methodology","Metodologija je opisana u radu."),("ograničenje","limitation","Istraživanje ima određena ograničenja.")],"questions":["Do kojeg zaključka dolazi tekst?","Što treba uzeti u obzir pri tumačenju?","Koja formulacija ublažava akademsku tvrdnju?"],"prompt":"Napišite kratak akademski odlomak koji iznosi tvrdnju, dokaz i ograničenje."},
    "hr-c1-unit-2": {"text":"U skladu s propisima, dokumentaciju treba dostaviti do petka. Nakon provjere, nadležna služba obavijestit će podnositelje o ishodu postupka.","words":[("propis","regulation","Dokumentacija je u skladu s propisima."),("nadležna služba","competent authority","Nadležna služba provjerava zahtjev."),("ishod","outcome","Očekujemo ishod postupka.")],"questions":["Do kada dokumentaciju treba dostaviti?","Tko će obavijestiti podnositelje?","Koji izraz pripada formalnom registru?"],"prompt":"Napišite formalnu obavijest o roku, postupku i obvezi korisnika."},
    "hr-c2-unit-1": {"text":"Provedba predloženih mjera zahtijeva sustavno vrednovanje raspoloživih podataka, uz istodobno razmatranje ograničenja primijenjenog analitičkog okvira.","words":[("provedba","implementation","Provedba mjera zahtijeva vrijeme."),("vrednovanje","evaluation","Vrednovanje rezultata je nužno."),("analitički okvir","analytical framework","Okvir mora biti jasno definiran.")],"questions":["Što zahtijeva provedba mjera?","Što se mora istodobno razmatrati?","Kako nominalizacije zgušnjavaju informacije?"],"prompt":"Preoblikujte jednostavne rečenice u jedan precizan formalni odlomak s nominalizacijama."},
    "hr-c2-unit-2": {"text":"Iako je naizgled riječ o jednostavnom zahtjevu, njegovo značenje ovisi o kontekstu. Kad je rekao da će uzeti stvar u svoje ruke, nije mislio na doslovnu radnju.","words":[("naizgled","seemingly","Naizgled je rješenje jednostavno."),("nijansa","nuance","Važna je pragmatička nijansa."),("doslovno","literally","Izraz ne treba razumjeti doslovno.")],"questions":["Zašto značenje zahtjeva ovisi o kontekstu?","Što znači izraz „uzeti stvar u svoje ruke“?","Kako se razlikuje doslovno i idiomatsko značenje?"],"prompt":"Objasnite jedan hrvatski idiom, njegovo doslovno značenje i pragmatičku uporabu."},
}

def _unit(unit_id: str, level: str):
    return next((u for u in CURRICULUM.get(level, []) if u.id == unit_id), None)

def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict | None:
    level = str(level).upper()
    skill = str(lesson_type).lower()
    unit = _unit(unit_id, level)
    content = _CONTENT.get(unit_id)
    if unit is None or content is None or skill not in _SKILLS:
        return None
    words = content["words"]
    base = {
        "title": unit.title,
        "objective": f"Razvijajte hrvatski jezik na razini {level} kroz temu „{unit.title}“.",
        "unit_id": unit_id,
        "source": "curated_croatian",
        "grammar": list(unit.grammar_points),
        "words": words,
        "vocabulary_words": [word[0] for word in words],
        "examples": [content["text"]],
    }
    if skill == "grammar":
        base["objective"] = f"Upotrijebite gramatičke strukture „{', '.join(unit.grammar_points)}“ u kontekstu teme „{unit.title}“."
    elif skill == "vocabulary":
        base["objective"] = f"Usvojite ključni rječnik za temu „{unit.title}“ i upotrijebite ga u kontekstu."
    elif skill == "reading":
        base["text"], base["questions"] = content["text"], content["questions"]
    elif skill == "listening":
        base["transcript"], base["questions"] = content["text"], content["questions"]
    elif skill == "speaking":
        base["prompt"] = content["prompt"]
        base["phrases"] = [word[2] for word in words]
    elif skill == "writing":
        base["prompt"] = content["prompt"]
        base["guidance"] = [f"Upotrijebite strukturu: {', '.join(unit.grammar_points)}.", "Upotrijebite najmanje tri riječi iz ciljnog rječnika.", "Povežite ideje jasnim i logičnim rečenicama."]
    else:
        base["questions"] = content["questions"] + [f"Objasnite kako tema „{unit.title}“ koristi ciljnu gramatiku."]
    return base
