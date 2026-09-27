"""Curated Hebrew A2-C2 lesson seeds for JUBA LISAN."""
from __future__ import annotations

_SKILLS = ("grammar", "vocabulary", "reading", "listening", "speaking", "writing", "review")

_UNITS = {
    "he-a2-unit-1": ("A2", "אירועים בעבר", "אתמול נסעתי לתל אביב, פגשתי חבר ותיק וביקרנו יחד במוזיאון."),
    "he-a2-unit-2": ("A2", "תכניות ועתיד", "בשבוע הבא ניפגש עם המשפחה ונכין יחד ארוחה חגיגית."),
    "he-a2-unit-3": ("A2", "סמיכות ושייכות", "בית הספר נמצא ליד תחנת הרכבת, ומנהל בית הספר עובד שם שנים רבות."),
    "he-a2-unit-4": ("A2", "מילות יחס ותקשורת", "אני צריך לדבר איתך על הנסיעה ולשאול אותך כמה שאלות."),
    "he-b1-unit-1": ("B1", "חברה ועבודה", "בצוות שלנו לכל עובד יש אחריות, וההחלטות מתקבלות לאחר דיון משותף."),
    "he-b1-unit-2": ("B1", "חינוך ולמידה", "הקורס שעשיתי בשנה שעברה עזר לי לפתח מיומנויות חדשות ולחשוב באופן עצמאי."),
    "he-b1-unit-3": ("B1", "תנאים ובחירות", "אם יהיה לנו מספיק זמן, נבדוק את האפשרויות לפני שנקבל החלטה סופית."),
    "he-b2-unit-1": ("B2", "תקשורת מקצועית ודיבור עקיף", "המנהלת אמרה שהצוות יבדוק את הנתונים לפני שיציג את ההמלצות."),
    "he-b2-unit-2": ("B2", "שיח ציבורי וקישוריות", "למרות הקשיים, התכנית נמשכה; עם זאת, היה צורך לשנות כמה מהיעדים."),
    "he-c1-unit-1": ("C1", "טיעון אקדמי וסיוג", "ניתן לטעון כי הממצאים תומכים בהשערה, אף שהראיות עדיין אינן חד-משמעיות."),
    "he-c1-unit-2": ("C1", "עברית מקצועית רשמית", "בהתאם להנחיות, יש להגיש את המסמכים עד המועד שנקבע ולצרף את האישורים הנדרשים."),
    "he-c2-unit-1": ("C2", "פרוזה רשמית מורכבת", "יישום ההמלצות מחייב בחינה מחודשת של סדרי העדיפויות ושל הקשרים בין הגורמים השונים."),
    "he-c2-unit-2": ("C2", "אידיומטיקה וניואנסים", "הוא לקח את העניין לידיים, אבל הדברים אינם חד-משמעיים כפי שנראו בתחילה."),
}

_WORDS = {
    "he-a2-unit-1": [("אתמול","yesterday","אתמול עבדתי בבית."),("פגשתי","I met","פגשתי חבר ותיק."),("ביקרנו","we visited","ביקרנו במוזיאון.")],
    "he-a2-unit-2": [("שבוע הבא","next week","בשבוע הבא ניפגש."),("ניפגש","we will meet","ניפגש בערב."),("להכין","to prepare","נכין ארוחה.")],
    "he-a2-unit-3": [("בית הספר","school","בית הספר קרוב."),("תחנת הרכבת","train station","תחנת הרכבת נמצאת כאן."),("מנהל","manager/principal","מנהל בית הספר הגיע.")],
    "he-a2-unit-4": [("איתך","with you","אני רוצה לדבר איתך."),("לשאול","to ask","אני רוצה לשאול אותך."),("נסיעה","trip","הנסיעה ארוכה.")],
    "he-b1-unit-1": [("אחריות","responsibility","יש לי אחריות על הפרויקט."),("צוות","team","הצוות עובד יחד."),("החלטה","decision","קיבלנו החלטה משותפת.")],
    "he-b1-unit-2": [("קורס","course","הקורס מתחיל ביום ראשון."),("מיומנות","skill","קריאה היא מיומנות חשובה."),("עצמאי","independent","הוא לומד באופן עצמאי.")],
    "he-b1-unit-3": [("אפשרות","possibility","יש לנו אפשרות אחרת."),("תנאי","condition","זה תנאי חשוב."),("להחליט","to decide","צריך להחליט היום.")],
    "he-b2-unit-1": [("נתונים","data","בדקנו את הנתונים."),("המלצה","recommendation","הצוות הציג המלצה."),("לדווח","to report","היא דיווחה על התוצאות.")],
    "he-b2-unit-2": [("למרות","despite/although","למרות הקשיים המשכנו."),("עם זאת","however","עם זאת, יש בעיה."),("יעד","target","הגדרנו יעד ברור.")],
    "he-c1-unit-1": [("ממצא","finding","הממצא המרכזי חשוב."),("השערה","hypothesis","ההשערה נבדקת במחקר."),("חד-משמעי","unambiguous","ההסבר אינו חד-משמעי.")],
    "he-c1-unit-2": [("בהתאם","in accordance","בהתאם להנחיות, יש לפעול כך."),("אישור","approval","נדרש אישור מנהל."),("מסמך","document","המסמך נחתם היום.")],
    "he-c2-unit-1": [("יישום","implementation","יישום ההמלצות דורש זמן."),("סדרי עדיפויות","priorities","שינינו את סדרי העדיפויות."),("בחינה מחודשת","reassessment","נדרשת בחינה מחודשת.")],
    "he-c2-unit-2": [("לכאורה","apparently/allegedly","לכאורה, הפתרון פשוט."),("משתמע","is implied","מן הדברים משתמע אחרת."),("ניואנס","nuance","הניואנס משנה את המשמעות.")],
}

_GRAMMAR = {
    "he-a2-unit-1": ["past-tense"],
    "he-a2-unit-2": ["future-tense"],
    "he-a2-unit-3": ["construct-state"],
    "he-a2-unit-4": ["prepositions-pronouns"],
    "he-b1-unit-1": ["binyanim"],
    "he-b1-unit-2": ["relative-clauses"],
    "he-b1-unit-3": ["conditionals"],
    "he-b2-unit-1": ["reported-speech"],
    "he-b2-unit-2": ["discourse-connectors"],
    "he-c1-unit-1": ["academic-hedging"],
    "he-c1-unit-2": ["formal-register"],
    "he-c2-unit-1": ["advanced-nominalization"],
    "he-c2-unit-2": ["idiomatic-nuance"],
}

def get_lesson_seed(level: str, unit_id: str, lesson_type: str) -> dict | None:
    """Return curated Hebrew lesson content for A2-C2."""
    skill = str(lesson_type).lower()
    item = _UNITS.get(str(unit_id))
    if item is None or item[0] != str(level).upper() or skill not in _SKILLS:
        return None
    level, title, text = item
    words = _WORDS[unit_id]
    base = {
        "title": title,
        "objective": f"פתחו את העברית שלכם ברמה {level} בנושא «{title}» והשתמשו בשפה בהקשר טבעי.",
        "unit_id": unit_id,
        "source": "curated_hebrew",
        "words": words,
        "vocabulary_words": [word[0] for word in words],
        "grammar": _GRAMMAR[unit_id],
        "examples": [text],
    }
    if skill == "grammar":
        base["objective"] = f"תרגלו את הנושא הדקדוקי «{_GRAMMAR[unit_id][0]}» באמצעות עברית טבעית."
        base["examples"] = [text, "אם יהיה לנו זמן, נבדוק את האפשרויות לפני שנחליט."]
    elif skill == "vocabulary":
        base["objective"] = "למדו את אוצר המילים המרכזי והשתמשו בכל מילה במשפט."
    elif skill == "reading":
        base.update(
            text=text,
            questions=[
                "מהו הנושא המרכזי של הקטע?",
                "אילו שתי מילים חדשות מופיעות בקטע?",
                "איזה פרט מהקטע תומך ברעיון המרכזי?",
            ],
        )
    elif skill == "listening":
        base.update(
            transcript=text,
            questions=[
                "מהו הנושא המרכזי ששמעתם?",
                "איזה פרט חשוב הוזכר?",
                "איזו מילה חדשה זיהיתם?",
            ],
        )
    elif skill == "speaking":
        base.update(
            prompt=f"דברו במשך דקה עד שתי דקות על «{title}». השתמשו לפחות בשלוש מילים חדשות.",
            phrases=[text, "לדעתי, חשוב לבחון את האפשרויות לפני שמחליטים.", "אני רוצה להוסיף נקודה נוספת."],
        )
    elif skill == "writing":
        base.update(
            prompt=f"כתבו פסקה של 80–120 מילים על «{title}» והשתמשו לפחות בשלוש מילים חדשות.",
            guidance=["חברו בין הרעיונות באמצעות מילות קישור.", "השתמשו במבנה הדקדוקי של היחידה.", "בדקו התאמה, זמנים וכתיב."],
        )
    else:
        base.update(
            questions=[
                "הסבירו במילים שלכם את המבנה הדקדוקי המרכזי.",
                "כתבו שני משפטים עם מילים חדשות מהיחידה.",
                "סכמו את הרעיון המרכזי במשפט אחד.",
            ]
        )
    return base
