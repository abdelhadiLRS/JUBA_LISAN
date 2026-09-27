"""Curated Romanian A2-C2 lesson seeds for JUBA LISAN."""
from __future__ import annotations

from typing import Any

from app.data.language_foundations.ro import CURRICULUM

_SKILLS = ("grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review")

_CONTENT: dict[str, dict[str, Any]] = {
"ro-a2-unit-1":{"text":"Sâmbătă am plecat cu trenul spre Brașov. Am cumpărat biletul din gară și am ajuns înainte de prânz.","words":[("călătorie","trip","Călătoria a fost plăcută."),("gară","station","Gara este aproape."),("bilet","ticket","Am cumpărat un bilet.")],"questions":["Unde a plecat persoana?","De unde a cumpărat biletul?","Când a ajuns?"],"prompt":"Povestește o călătorie recentă folosind verbe la perfectul compus."},
"ro-a2-unit-2":{"text":"Maria lucrează dimineața și urmează un curs seara. Poate să studieze după serviciu, iar în weekend vrea să exerseze mai mult.","words":[("curs","course","Urmez un curs de limbi străine."),("a putea","can","Pot să studiez seara."),("a exersa","to practise","Vreau să exersez mai mult.")],"questions":["Când lucrează Maria?","Când studiază?","Ce vrea să facă în weekend?"],"prompt":"Descrie ce poți, vrei și trebuie să faci într-o săptămână obișnuită."},
"ro-a2-unit-3":{"text":"După serviciu, Dan merge la farmacie pentru că îl doare gâtul. Farmacistul îi recomandă apă, odihnă și un consult dacă simptomele continuă.","words":[("gât","throat","Mă doare gâtul."),("farmacie","pharmacy","Farmacia este la colț."),("simptom","symptom","Simptomele continuă.")],"questions":["De ce merge Dan la farmacie?","Ce îi recomandă farmacistul?","Când trebuie să consulte un medic?"],"prompt":"Descrie o problemă de sănătate și pune întrebări potrivite într-o conversație la farmacie."},
"ro-a2-unit-4":{"text":"Îmi place apartamentul luminos, dar prefer cartierul liniștit. Pentru mine, o locuință bună trebuie să fie aproape de transportul public.","words":[("luminos","bright","Apartamentul este luminos."),("liniștit","quiet","Cartierul este liniștit."),("preferință","preference","Am o preferință clară.")],"questions":["Ce îi place vorbitorului?","Ce preferă?","Ce condiție consideră importantă?"],"prompt":"Compară două locuri și explică-ți preferințele folosind adjective."},
"ro-b1-unit-1":{"text":"Când eram copil, petreceam verile la bunici. Acum îmi amintesc acele zile și înțeleg cât de mult m-au influențat.","words":[("amintire","memory","Este o amintire importantă."),("copilărie","childhood","Copilăria mea a fost liniștită."),("a influența","to influence","Experiența m-a influențat.")],"questions":["Unde petrecea persoana verile?","Ce face acum cu amintirile?","Cum au influențat-o acele experiențe?"],"prompt":"Povestește o experiență din trecut și explică efectul ei asupra prezentului."},
"ro-b1-unit-2":{"text":"La birou, colegii folosesc un calendar comun pentru întâlniri. Dacă apare o problemă, discută direct și caută o soluție împreună.","words":[("calendar","calendar","Folosim un calendar comun."),("întâlnire","meeting","Avem o întâlnire luni."),("soluție","solution","Căutăm o soluție.")],"questions":["Ce folosesc colegii?","Ce fac atunci când apare o problemă?","Cum caută o soluție?"],"prompt":"Descrie o situație de comunicare la locul de muncă și propune o soluție."},
"ro-b1-unit-3":{"text":"Știrile despre transport au provocat reacții diferite. Unii locuitori consideră măsura utilă, în timp ce alții cer mai multe explicații.","words":[("știre","news item","Am citit o știre interesantă."),("locuitor","resident","Locuitorii au răspuns."),("măsură","measure","Măsura a provocat discuții.")],"questions":["Ce a provocat reacții?","Ce cred unii locuitori?","Ce cer ceilalți?"],"prompt":"Prezintă două opinii diferite despre o știre și explică-le."},
"ro-b1-unit-4":{"text":"Am decis să învăț mai serios limba română. Mai întâi îmi organizez timpul, apoi aleg materiale și stabilesc obiective săptămânale.","words":[("decizie","decision","Am luat o decizie."),("obiectiv","goal","Am un obiectiv săptămânal."),("a organiza","to organise","Îmi organizez timpul.")],"questions":["Ce a decis persoana?","Ce face mai întâi?","Cum își organizează învățarea?"],"prompt":"Explică o decizie importantă și pașii pe care îi vei urma."},
"ro-b2-unit-1":{"text":"O propunere poate părea eficientă la prima vedere, însă analiza datelor arată și câteva riscuri. De aceea, argumentele trebuie comparate înaintea deciziei.","words":[("propunere","proposal","Propunerea trebuie analizată."),("risc","risk","Există un risc important."),("argument","argument","Argumentul se bazează pe date.")],"questions":["Cum poate părea propunerea inițial?","Ce arată datele?","Ce trebuie făcut înaintea deciziei?"],"prompt":"Construiește un argument echilibrat cu o idee principală, un contraargument și o concluzie."},
"ro-b2-unit-2":{"text":"Într-o echipă profesionistă, mesajele trebuie să fie clare, iar responsabilitățile bine definite. Când apar neînțelegeri, reformularea poate evita conflictele inutile.","words":[("responsabilitate","responsibility","Responsabilitatea este clară."),("neînțelegere","misunderstanding","A apărut o neînțelegere."),("reformulare","rephrasing","Reformularea clarifică mesajul.")],"questions":["Cum trebuie să fie mesajele?","Ce se întâmplă când apar neînțelegeri?","De ce este utilă reformularea?"],"prompt":"Simulează o situație profesională în care clarifici politicos o neînțelegere."},
"ro-b2-unit-3":{"text":"Un festival local poate susține economia orașului, dar succesul său depinde și de protejarea spațiilor publice și de implicarea comunității.","words":[("festival","festival","Festivalul atrage vizitatori."),("comunitate","community","Comunitatea participă activ."),("patrimoniu","heritage","Patrimoniul trebuie protejat.")],"questions":["Cum poate ajuta festivalul orașul?","De ce trebuie protejate spațiile publice?","Ce rol are comunitatea?"],"prompt":"Discută avantajele și posibilele probleme ale unui eveniment cultural."},
"ro-b2-unit-4":{"text":"Când o poveste este relatată din perspective diferite, aceleași evenimente pot părea foarte diferite. Detaliile alese de narator influențează interpretarea cititorului.","words":[("narator","narrator","Naratorul descrie evenimentele."),("perspectivă","perspective","Perspectiva schimbă interpretarea."),("detaliu","detail","Un detaliu poate fi important.")],"questions":["De ce pot părea diferite aceleași evenimente?","Cine influențează selecția detaliilor?","Cum este afectat cititorul?"],"prompt":"Povestește aceeași situație din două perspective diferite."},
"ro-c1-unit-1":{"text":"În analiza academică, rezultatele trebuie separate de interpretări. Datele pot indica o asociere, fără să demonstreze automat o relație cauzală.","words":[("asociere","association","Datele indică o asociere."),("cauzalitate","causality","Cauzalitatea nu este demonstrată."),("interpretare","interpretation","Interpretarea trebuie justificată.")],"questions":["Ce trebuie separat?","Ce pot indica datele?","Ce nu demonstrează automat asocierea?"],"prompt":"Prezintă o concluzie academică și formuleaz-o cu gradul potrivit de prudență."},
"ro-c1-unit-2":{"text":"În comunicarea profesională, o recomandare eficientă trebuie să precizeze responsabilitățile, termenul și criteriile de verificare, fără ambiguități inutile.","words":[("responsabilitate","responsibility","Responsabilitatea trebuie precizată."),("termen","deadline","Termenul este vineri."),("criteriu","criterion","Criteriul de evaluare este clar.")],"questions":["Ce trebuie să precizeze recomandarea?","De ce trebuie evitată ambiguitatea?","Ce element de verificare este menționat?"],"prompt":"Redactează o recomandare profesională precisă, cu responsabilități și termene."},
"ro-c1-unit-3":{"text":"Analiza unui fenomen cultural cere atenție la contextul istoric, la limbaj și la publicul căruia i se adresează opera.","words":[("context","context","Contextul istoric este important."),("fenomen","phenomenon","Fenomenul merită analizat."),("public","audience","Opera se adresează unui public larg.")],"questions":["La ce trebuie să fie atentă analiza?","De ce contează contextul istoric?","Cui se poate adresa opera?"],"prompt":"Analizează un fenomen cultural și explică de ce contextul îi schimbă interpretarea."},
"ro-c1-unit-4":{"text":"O afirmație nu devine convingătoare doar prin formulare sigură. Forța ei depinde de dovezi, de limitele recunoscute și de felul în care sunt tratate obiecțiile.","words":[("dovadă","evidence","Afirmația are nevoie de dovezi."),("obiecție","objection","Autorul răspunde unei obiecții."),("limită","limitation","Studiul are o limită.")],"questions":["De ce nu este suficient un ton sigur?","Ce susține o afirmație?","Cum trebuie tratate obiecțiile?"],"prompt":"Construiește un argument nuanțat care recunoaște o obiecție și răspunde la ea."},
"ro-c2-unit-1":{"text":"Discursul public poate combina informația explicită cu sugestii indirecte. Interpretarea corectă depinde de context, de alegerea cuvintelor și de relația dintre vorbitor și public.","words":[("subtext","subtext","Subtextul schimbă interpretarea."),("discurs","discourse","Discursul are mai multe niveluri."),("sugestie","implication","Sugestia nu este formulată direct.")],"questions":["Ce poate combina discursul public?","De ce contează contextul?","Ce alte elemente influențează interpretarea?"],"prompt":"Analizează o afirmație publică și separă sensul explicit de subtext."},
"ro-c2-unit-2":{"text":"Într-un document formal, precizia nu înseamnă doar alegerea unor cuvinte dificile; ea presupune delimitarea clară a obligațiilor, excepțiilor și condițiilor.","words":[("delimitare","delimitation","Delimitarea responsabilităților este necesară."),("obligație","obligation","Obligația este clar formulată."),("excepție","exception","Documentul prevede o excepție.")],"questions":["Ce înseamnă precizia în document?","Ce trebuie delimitat?","De ce nu sunt suficiente cuvintele dificile?"],"prompt":"Redactează un paragraf formal în care precizezi obligații, condiții și o excepție."},
"ro-c2-unit-3":{"text":"Într-o operă literară, alegerea unui cuvânt poate produce efecte de ton, ritm și perspectivă. Sensul se construiește prin relația dintre detalii, nu prin elemente izolate.","words":[("ton","tone","Tonul textului este ambiguu."),("ritm","rhythm","Ritmul frazei este rapid."),("perspectivă","perspective","Perspectiva narativă este complexă.")],"questions":["Ce efecte poate produce alegerea unui cuvânt?","Cum se construiește sensul?","De ce nu trebuie analizate elementele izolat?"],"prompt":"Analizează stilul unui scurt text literar, concentrându-te pe ton, ritm și perspectivă."},
"ro-c2-unit-4":{"text":"O formulare precisă poate părea mai puțin spectaculoasă decât una categorică, dar reduce riscul de interpretare greșită și permite autorului să distingă certitudinea de probabilitate.","words":[("precizie","precision","Precizia este esențială."),("certitudine","certainty","Autorul exprimă certitudinea cu atenție."),("probabilitate","probability","Probabilitatea trebuie formulată clar.")],"questions":["De ce poate fi preferată formularea precisă?","Ce risc reduce?","Ce diferență trebuie păstrată?"],"prompt":"Rescrie trei afirmații categorice astfel încât să exprime corect certitudinea și probabilitatea."},
}

def _unit(unit_id: str, level: str):
    return next((unit for unit in CURRICULUM.get(level, []) if unit.id == unit_id), None)

def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict[str, Any] | None:
    level = str(level).upper()
    skill = str(lesson_type).lower()
    unit = _unit(unit_id, level)
    content = _CONTENT.get(unit_id)
    if unit is None or content is None or skill not in _SKILLS:
        return None
    words = content["words"]
    base = {
        "title": unit.title,
        "objective": f"Dezvoltă competența de limba română la nivelul {level} prin tema „{unit.title}”.",
        "unit_id": unit_id,
        "source": "curated_romanian",
        "grammar": list(unit.grammar_points),
        "words": words,
        "vocabulary_words": [word[0] for word in words],
        "examples": [content["text"]],
    }
    if skill == "grammar":
        base["objective"] = f"Folosește structurile „{', '.join(unit.grammar_points)}” în contextul temei „{unit.title}”."
    elif skill == "vocabulary":
        base["objective"] = f"Folosește vocabularul specific temei „{unit.title}” în propoziții naturale."
    elif skill == "reading":
        base["text"], base["questions"] = content["text"], content["questions"]
    elif skill == "listening":
        base["transcript"], base["questions"] = content["text"], content["questions"]
    elif skill == "speaking":
        base["prompt"] = content["prompt"]
        base["phrases"] = [word[2] for word in words]
    elif skill == "writing":
        base["prompt"] = content["prompt"]
        base["guidance"] = [
            f"Folosește cel puțin o structură din: {', '.join(unit.grammar_points)}.",
            "Folosește cel puțin trei cuvinte din vocabularul lecției.",
            "Leagă ideile prin propoziții clare și coerente.",
        ]
    else:
        base["questions"] = content["questions"] + [f"Explică legătura dintre tema „{unit.title}” și gramatica țintă."]
    return base
