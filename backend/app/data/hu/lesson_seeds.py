"""Curated Hungarian A2-C2 lesson seeds for JUBA LISAN."""
from __future__ import annotations
from typing import Any

UNITS = {
    "A2": {
        "hu-a2-unit-1": {
            "title": "Utazás és mindennapi tervek",
            "grammar": ["Múlt idő", "Jövő és tervek"],
            "words": [("jegy","ticket","Megvettem a vonatjegyet."),("pályaudvar","station","A pályaudvaron találkozunk."),("csomag","luggage","Hol van a csomagom?")],
            "text": "A múlt hétvégén Budapestre utaztam. Megvettem a jegyet, és időben elindultam a pályaudvarra. A jövő héten újra utazni fogok, de most már előre megtervezem az útvonalat.",
            "prompt": "Mesélj egy korábbi utazásodról, majd mondd el, mit fogsz csinálni a következő utazásodon.",
        },
        "hu-a2-unit-2": {
            "title": "Egészség és időpontok",
            "grammar": ["Esetragok"],
            "words": [("orvos","doctor","El kell mennem az orvoshoz."),("gyógyszer","medicine","Bevettem a gyógyszert."),("fájdalom","pain","Erős fájdalmat érzek.")],
            "text": "Ma reggel nem éreztem jól magam, ezért felhívtam az orvost. Délutánra kaptam időpontot. Az orvos megvizsgált, és azt mondta, hogy néhány napig pihennem kell.",
            "prompt": "Játssz el egy rövid párbeszédet az orvossal: mondd el, mi fáj, és kérj időpontot.",
        },
        "hu-a2-unit-3": {
            "title": "Munka és időbeosztás",
            "grammar": ["Fokozás"],
            "words": [("megbeszélés","meeting","A megbeszélés kilenckor kezdődik."),("kolléga","colleague","A kollégám otthonról dolgozik."),("határidő","deadline","A határidő péntek.")],
            "text": "Az új munkarend rugalmasabb, mint a régi. A reggeli megbeszélések rövidebbek, ezért több idő marad a fontos feladatokra. A pénteki határidő azonban szorosabb.",
            "prompt": "Hasonlíts össze két munkanapot vagy két időbeosztást, és indokold meg, melyik kényelmesebb.",
        },
    },
    "B1": {
        "hu-b1-unit-1": {
            "title": "Környezet és megoldások",
            "grammar": ["Határozott és határozatlan ragozás", "Feltételes mód"],
            "words": [("környezet","environment","Vigyáznunk kell a környezetre."),("hulladék","waste","Kevesebb hulladékot kell termelnünk."),("újrahasznosítás","recycling","Az újrahasznosítás fontos megoldás.")],
            "text": "A város egyre több hulladékot termel, ezért új megoldásokra van szükség. Ha többen használnák a tömegközlekedést, csökkenne a forgalom. A változás akkor lehet tartós, ha a lakók és az intézmények együttműködnek.",
            "prompt": "Mutass be egy környezeti problémát, és javasolj legalább két megoldást feltételes mondatokkal.",
        },
        "hu-b1-unit-2": {
            "title": "Oktatás és készségek",
            "grammar": ["Feltételes mód"],
            "words": [("készség","skill","Új készségeket szeretnék fejleszteni."),("tanfolyam","course","Jelentkeztem egy online tanfolyamra."),("tapasztalat","experience","A gyakorlat hasznos tapasztalatot adott.")],
            "text": "Az új készségek megszerzése időt és gyakorlást igényel. Ha lenne több szabadidőm, rendszeresen részt vennék egy tanfolyamon. A gyakorlati feladatok segítenek abban, hogy az elméleti tudást valódi helyzetekben is használjam.",
            "prompt": "Beszélj egy készségről, amelyet szeretnél fejleszteni, és mondd el, mit tennél, ha több időd lenne.",
        },
    },
    "B2": {
        "hu-b2-unit-1": {
            "title": "Társadalom és felelősség",
            "grammar": ["Vonatkozó mellékmondatok"],
            "words": [("felelősség","responsibility","A döntéshozóknak nagy a felelősségük."),("közösség","community","A közösség együtt keresett megoldást."),("egyenlőség","equality","Az egyenlőség fontos társadalmi érték.")],
            "text": "Egy közösség akkor működik jól, ha azok az emberek, akik részt vesznek benne, felelősséget vállalnak a közös ügyekért. Azok a döntések, amelyek hosszú távon hatnak a társadalomra, különösen körültekintő mérlegelést igényelnek.",
            "prompt": "Fejtsd ki, milyen felelőssége van az egyénnek a közösségben, és használj legalább három vonatkozó mellékmondatot.",
        },
        "hu-b2-unit-2": {
            "title": "Média és bizonyítékok",
            "grammar": ["Függő beszéd"],
            "words": [("forrás","source","Ellenőrizni kell a forrás megbízhatóságát."),("bizonyíték","evidence","A következtetést több bizonyíték támasztja alá."),("állítás","claim","Az állítást további adatokkal kell igazolni.")],
            "text": "A hírek értékelésekor nem elég egyetlen forrásra támaszkodni. Egy újságíró azt mondta, hogy további adatokat keres, mert az első jelentés több pontja még nem volt ellenőrizve. A megbízható elemzés különválasztja a tényeket, az állításokat és a véleményeket.",
            "prompt": "Foglalj össze egy hírt vagy nyilvános állítást függő beszéddel, és mondd el, milyen bizonyíték támasztja alá.",
        },
    },
    "C1": {
        "hu-c1-unit-1": {
            "title": "Akadémiai érvelés",
            "grammar": ["Ige előtti fókusz", "Hivatalos és akadémiai stílus"],
            "words": [("kutatás","research","A kutatás eredményei további kérdéseket vetnek fel."),("eredmény","result","Az eredmények alapján óvatos következtetés vonható le."),("korlátozás","limitation","A vizsgálat egyik korlátozása a kis minta.")],
            "text": "A kutatás eredményei alapján nem állítható egyértelműen, hogy az összes vizsgált tényező azonos hatással rendelkezik. Különösen fontos figyelembe venni a minta korlátozásait, amelyek befolyásolhatják az eredmények általánosíthatóságát.",
            "prompt": "Mutass be egy kutatási eredményt árnyaltan: különítsd el a bizonyítékot, a következtetést és a bizonytalanságot.",
        },
    },
    "C2": {
        "hu-c2-unit-1": {
            "title": "Kultúra és stiláris árnyalatok",
            "grammar": ["Összetett alárendelés", "Stilisztikai árnyalatok"],
            "words": [("árnyalat","nuance","A megfogalmazás finom árnyalatokat hordoz."),("célzás","allusion","A mondatban rejtett célzás található."),("hangnem","tone","A szöveg hangneme visszafogott és ironikus.")],
            "text": "Bár a mondat első pillantásra egyszerűnek tűnik, a hangnem és a szövegkörnyezet alapján többféleképpen is értelmezhető. Amennyiben az irónia szándékos, a szó szerinti jelentés nem feltétlenül egyezik a beszélő valódi szándékával.",
            "prompt": "Elemezd egy rövid magyar szöveg hangnemét és rejtett jelentését, majd magyarázd el, hogyan változna az értelmezés más kontextusban.",
        },
    },
}

def _seed(data: dict[str, Any], skill: str) -> dict[str, Any]:
    title, grammar, words, text, prompt = data["title"], data["grammar"], data["words"], data["text"], data["prompt"]
    base = {
        "title": title,
        "objective": f"Fejleszd a magyar nyelvtudásodat a következő témában: {title}.",
        "grammar": grammar,
        "words": words,
        "source": "curated_hungarian",
    }
    if skill == "grammar":
        base["objective"] = f"Használd pontosan a következő nyelvtani szerkezeteket: {', '.join(grammar)}."
        base["examples"] = [x[2] for x in words]
    elif skill == "vocabulary":
        base["objective"] = f"Tanuld meg és használd a {title} témakör legfontosabb szavait."
        base["examples"] = [x[2] for x in words]
    elif skill == "reading":
        base.update(objective="Érts meg egy összefüggő magyar szöveget, és azonosítsd a fő gondolatokat.", text=text,
                    questions=["Mi a szöveg fő témája?", "Melyik két részlet támasztja alá a fő gondolatot?", "Fogalmazd meg saját szavaiddal a szöveg egyik következtetését."])
    elif skill == "listening":
        base.update(objective="Értsd meg a fő információkat egy összefüggő magyar szövegben.", transcript=text,
                    questions=["Mi a fő üzenet?", "Milyen két fontos részletet hallottál?", "Milyen következtetést lehet levonni a hallott szövegből?"])
    elif skill == "speaking":
        base.update(objective="Beszélj önállóan a témáról pontos magyar nyelvhasználattal.", prompt=prompt,
                    phrases=[x[2] for x in words], examples=[x[2] for x in words[:2]])
    elif skill == "writing":
        base.update(objective="Írj összefüggő, a szintnek megfelelő magyar szöveget.", prompt=prompt,
                    guidance=[f"Használj legalább egy szerkezetet: {', '.join(grammar)}.", "Használj legalább három témához kapcsolódó szót.", "Kapcsold össze az ötleteidet világos mondatokkal."],
                    examples=[x[2] for x in words[:2]])
    elif skill == "review":
        base.update(objective="Ismételd át a nyelvtant és a szókincset a témakörben.",
                    questions=[f"Alkoss egy mondatot a következő szerkezet egyikével: {', '.join(grammar)}.", f"Használj két szót a témakörből: {', '.join(x[0] for x in words[:2])}.", "Magyarázd meg, hogyan változik a jelentés a szövegkörnyezettől függően."])
    else:
        return {}
    return base

S: dict[tuple[str, str, str], dict[str, Any]] = {}
for level, units in UNITS.items():
    for unit_id, data in units.items():
        for skill in ("grammar","vocabulary","reading","listening","speaking","writing","review"):
            S[(level, unit_id, skill)] = _seed(data, skill)

def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict[str, Any] | None:
    return S.get((str(level).upper(), str(unit_id), str(lesson_type).lower()))
