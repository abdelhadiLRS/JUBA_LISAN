"""Curated Icelandic A2-C2 lesson seeds for JUBA LISAN."""
from __future__ import annotations
from typing import Any

LEVELS = ("A2", "B1", "B2", "C1", "C2")
SKILLS = ("grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review")

TOPICS = {
"A2": [
("1","Tími og áform","Þátíð og framtíð","Segðu frá því sem þú gerðir í gær og hvað þú ætlar að gera á morgun.",["í gær","á morgun","áætlun","seinna"]),
("2","Þjónusta og peningar","Föll í algengum setningum","Biddu um þjónustu, spurðu um verð og útskýrðu hvað þú þarft.",["reikningur","verð","pöntun","kort"]),
("3","Ferðalög","Þátíð og ferðasagnir","Segðu frá ferð og lýstu því hvernig þú komst á áfangastað.",["ferð","flugvöllur","hótel","miði"]),
("4","Heilsa og líðan","Mætti og nauðsyn","Lýstu einkennum og útskýrðu hvað þú ættir að gera.",["heilsa","einkenni","læknir","hvíla"]),
("5","Nám og vinna","Tímatengingar","Lýstu náms- eða vinnudegi og tengdu atburði í réttri röð.",["verkefni","fundur","nám","vinna"]),
("6","Frítími","Samanburður","Berðu saman tvær frístundir og segðu hvor hentar þér betur.",["frístund","áhugamál","betri","skemmtilegur"]),
("7","Reynsla og skoðanir","Reynslusetningar","Segðu frá einhverju sem þú hefur prófað og gefðu einfalda skoðun.",["reynsla","prófa","finnast","áhugaverður"]),
("8","A2 upprifjun","Samþætting","Notaðu orðaforða og málfræði A2 til að leysa raunhæft verkefni.",["fyrst","síðan","vegna þess","þess vegna"]),
],
"B1": [
("1","Vinna og ábyrgð","Skilyrði","Útskýrðu hvaða færni þú þarft í starfi og hvað gerist ef áætlun breytist.",["ábyrgð","færni","reynsla","skilyrði"]),
("2","Samfélag og borgaralíf","Orsök og afleiðing","Lýstu samfélagslegu vandamáli og tengdu orsök þess við mögulega lausn.",["samfélag","vandamál","lausn","afleiðing"]),
("3","Fréttir og upplýsingar","Óbein ræða","Endursegðu upplýsingar úr frétt og greindu á milli staðreyndar og skoðunar.",["heimild","frétt","staðreynd","skoðun"]),
("4","Sambönd og lausnir","Tilvísunarsetningar","Lýstu fólki og aðstæðum með nákvæmum viðbótarupplýsingum.",["samband","aðstæður","manneskja","lausn"]),
("5","Menning og sjálfsmynd","Ívilnun","Settu fram skoðun og viðurkenndu sjónarmið sem er ólíkt þínu.",["menning","sjálfsmynd","þótt","sjónarmið"]),
("6","Umhverfi og lífsstíll","Tilgangur","Útskýrðu hvaða breytingar fólk getur gert til að draga úr áhrifum á umhverfið.",["umhverfi","neysla","endurvinna","markmið"]),
("7","Röksemdafærsla","Tengiorð","Byggðu upp einfalt rök og studdu það með dæmi.",["rök","dæmi","þess vegna","hins vegar"]),
("8","B1 upprifjun","Samhangandi mál","Skrifaðu og ræddu málefni með skýrum tengingum milli hugmynda.",["í fyrsta lagi","auk þess","þó","að lokum"]),
],
"B2": [
("1","Rök og sönnunargögn","Skilyrðissetningar","Settu fram fullyrðingu, rökstuddu hana og fjallaðu um mótrök.",["forsenda","sönnunargagn","mótrök","niðurstaða"]),
("2","Fjölmiðlar og gagnrýnin hugsun","Óbein ræða","Berðu saman tvær heimildir og greindu hvernig orðaval þeirra mótar framsetninguna.",["heimild","hlutdrægni","framsetning","áreiðanlegur"]),
("3","Fagleg samskipti","Óbeinar spurningar","Settu fram kurteisar fyrirspurnir og skýr svör í faglegu samhengi.",["fyrirspurn","skýra","samskipti","viðtakandi"]),
("4","Samfélagsmál","Nafnorðagerð","Lýstu samfélagslegri þróun með nákvæmu og formlegu orðalagi.",["þróun","breyting","stefna","áhrif"]),
("5","Vísindi og tækni","Óvissa og líkur","Greindu niðurstöður og gerðu greinarmun á staðreynd, vísbendingu og túlkun.",["rannsókn","gögn","vísbending","óvissa"]),
("6","Umræður og sjónarhorn","Skrá og tónn","Aðlagaðu sama boðskap að ólíkum viðtakendum og samhengi.",["sjónarhorn","tónn","formlegt","óformlegt"]),
("7","Stíll og nákvæmni","Samsettar setningar","Tengdu flóknar hugmyndir án þess að missa skýrleika.",["nákvæmni","tenging","samhengi","áhersla"]),
("8","B2 upprifjun","Jafnvægi í röksemdum","Settu fram yfirvegað svar sem tekur bæði eigin rök og mótrök alvarlega.",["hins vegar","þrátt fyrir","samanlagt","mat"]),
],
"C1": [
("1","Akademísk orðræða","Hófsemi í fullyrðingum","Mótaðu niðurstöður þannig að greinilegt sé hvað gögn styðja og hvað er aðeins túlkun.",["benda til","virðist","niðurstaða","túlkun"]),
("2","Fagleg tjáskipti","Formlegt mál","Skrifaðu greinargerð með skýrum tilgangi, rökum og niðurstöðu.",["greinargerð","framkvæmd","ábyrgð","niðurstaða"]),
("3","Rannsóknir og aðferðafræði","Nafnorðagerð","Lýstu aðferð, gögnum og takmörkunum rannsóknar á nákvæmu máli.",["aðferðafræði","gagnasöfnun","takmörkun","greining"]),
("4","Flóknir textar","Upplýsingaskipan","Endurskrifaðu texta þannig að nýjar og þekktar upplýsingar komi skýrt fram.",["upplýsingar","uppbygging","samhengi","áhersla"]),
("5","Opinber framsetning","Stofnanamál","Mótaðu formlega tilkynningu þar sem ábyrgð, ferli og næstu skref eru skýr.",["tilkynning","ferli","ákvörðun","framkvæmd"]),
("6","Greining og samþætting","Heimildir og sönnun","Berðu saman heimildir og mettu styrk þeirra áður en þú dregur ályktun.",["heimild","sönnun","gagnagrunnur","ályktun"]),
("7","Stíll og málnotkun","Pragmatík","Greindu hvernig tónn, samband og samhengi breyta merkingu sömu setningar.",["undirtexti","tónn","samhengi","tillitssemi"]),
("8","C1 upprifjun","Nákvæm ritstjórn","Endurbættu faglegan texta með meiri nákvæmni, flæði og hófsemi.",["nákvæmni","flæði","fyrirvari","blæbrigði"]),
],
"C2": [
("1","Stílstjórn","Flókin röksemdafærsla","Greindu sýnilegar og undirliggjandi forsendur og mótaðu yfirvegað svar.",["forsenda","undirliggjandi","mótrök","ályktun"]),
("2","Merkingarblæbrigði","Pragmatísk nákvæmni","Útskýrðu hvernig óbein orðræða getur tjáð gagnrýni, kurteisi eða fjarlægð.",["óbeinn","kurteisi","gagnrýni","undirtexti"]),
("3","Akademísk röksemdafærsla","Mælskulist","Notaðu andstæður, endurtekningu og sjónarhorn til að byggja upp sannfærandi texta.",["andstæða","endurtekning","sjónarhorn","áhersla"]),
("4","Faglegt og stjórnsýslulegt mál","Orðaval og rammasetning","Greindu hvernig orðaval í opinberum texta mótar túlkun lesandans.",["stjórnsýsla","rammasetning","afstaða","túlkun"]),
("5","Mælskulist og orðræða","Upplýsingaskipan","Skipuleggðu flókna ræðu þannig að áherslur og undirtexti haldist skýrir.",["mælskulist","uppbygging","áhersla","undirtexti"]),
("6","Mat og gagnrýni","Gagnrýnin greining","Metaðu rök og takmarkanir texta án þess að einfalda óvissuna.",["mat","takmörkun","gagnrýni","óvissa"]),
("7","Orðtök og pragmatík","Stíll og merking","Greindu orðtök, kaldhæðni og menningarlega merkingu í samhengi.",["orðtak","kaldhæðni","menningarlegur","merking"]),
("8","C2 samþætting","Samanburður og nýmyndun","Sameinaðu mótsagnakenndar heimildir í nákvæma og blæbrigðaríka niðurstöðu.",["mótsögn","samþætting","jafnvægi","blæbrigði"]),
],
}

def _seed(level: str, number: str, skill: str) -> dict[str, Any]:
    _, title, grammar, prompt, words = next(x for x in TOPICS[level] if x[0] == number)
    unit_id = f"is-{level.lower()}-unit-{number}"
    base: dict[str, Any] = {
        "title": title,
        "objective": f"Þróaðu íslenskukunnáttu á {level}-stigi með þemað {title.lower()}.",
        "grammar": [grammar],
        "words": [(w, f"Orðaforði um {title.lower()}", f"Notaðu «{w}» í eðlilegri íslenskri setningu.") for w in words],
        "examples": [prompt],
        "source": "curated_icelandic",
        "unit_id": unit_id,
    }
    if skill == "grammar":
        base["objective"] = f"Notaðu {grammar.lower()} rétt í íslensku."
        base["grammar_examples"] = [prompt]
    elif skill == "vocabulary":
        base["objective"] = f"Notaðu lykilorðaforða um {title.lower()} í samhengi."
    elif skill == "reading":
        base["text"] = f"{prompt} Textinn leggur áherslu á hugtökin {', '.join(words)}."
        base["questions"] = ["Hver er meginhugmyndin?", "Hvaða tvö orð eru mikilvægust?", "Hvaða atriði styður meginhugmyndina?"]
    elif skill == "listening":
        base["transcript"] = f"{prompt} Í samtalinu koma meðal annars fyrir orðin {', '.join(words)}."
        base["questions"] = ["Hvert er meginatriðið?", "Hvaða upplýsingar heyrðir þú?", "Hvaða orð sýnir afstöðu talandans?"]
    elif skill == "speaking":
        base["prompt"] = prompt
        base["phrases"] = words
        base["examples"] = [f"Ég vil útskýra {title.lower()} og tengja það við eigin reynslu."]
    elif skill == "writing":
        base["prompt"] = prompt
        base["guidance"] = [f"Notaðu að minnsta kosti þrjú orð: {', '.join(words)}.", "Tengdu hugmyndir með skýrum tengiorðum.", "Aðlagaðu tón og smáatriði að viðtakanda."]
    elif skill == "review":
        base["questions"] = [f"Skrifaðu tvær setningar um {title.lower()}.", f"Notaðu að minnsta kosti tvö orð: {', '.join(words)}.", "Útskýrðu hvenær málfræðimynstrið hentar."]
    return base

S = {(level, f"is-{level.lower()}-unit-{number}", skill): _seed(level, number, skill)
     for level in LEVELS for number, *_ in TOPICS[level] for skill in SKILLS}

def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict[str, Any] | None:
    return S.get((str(level).upper(), str(unit_id), str(lesson_type).lower()))
