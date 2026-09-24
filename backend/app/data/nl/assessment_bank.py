"""Nederlands assessment foundation."""
from app.data._types import AssessmentQuestion

ASSESSMENT_BANK=[
AssessmentQuestion(id="nl-a1-001",skill="communication",difficulty="A1",question="Je ontmoet iemand. Welke begroeting past?",options=["Hallo!","Dank je!","Tot ziens!","Goedenacht!"],correct="Hallo!"),
AssessmentQuestion(id="nl-a1-002",skill="grammar",difficulty="A1",question="Je wilt zeggen “I am a student”. Welke zin is correct?",options=["Ik ben student.","Ik is student.","Ik bent student.","Ik zijn student."],correct="Ik ben student."),
AssessmentQuestion(id="nl-a1-003",skill="communication",difficulty="A1",question="Je wilt naar iemands naam vragen. Welke vraag gebruik je?",options=["Hoe heet je?","Waar is de winkel?","Hoe laat is het?","Hoeveel kost dit?"],correct="Hoe heet je?"),
AssessmentQuestion(id="nl-a1-004",skill="grammar",difficulty="A1",question="Je begrijpt iets niet. Welke zin betekent “I don't understand”?",options=["Ik begrijp het niet.","Ik begrijp het.","Ik niet begrijpen.","Ik is niet begrijpen."],correct="Ik begrijp het niet."),
AssessmentQuestion(id="nl-a1-005",skill="vocabulary",difficulty="A1",question="Je hebt dorst. Welk woord betekent “water”?",options=["water","brood","huis","boek"],correct="water"),
AssessmentQuestion(id="nl-a1-006",skill="vocabulary",difficulty="A1",question="Je praat over je familie. Welk woord betekent “mother”?",options=["moeder","vader","broer","vriend"],correct="moeder"),
AssessmentQuestion(id="nl-a1-007",skill="communication",difficulty="A1",question="Je bent in een winkel en wilt de prijs vragen. Wat zeg je?",options=["Hoeveel kost dit?","Hoe heet je?","Waar woon je?","Goedemorgen."],correct="Hoeveel kost dit?"),
AssessmentQuestion(id="nl-a1-008",skill="grammar",difficulty="A1",question="Je wilt zeggen “I live in Amsterdam”. Welke zin is correct?",options=["Ik woon in Amsterdam.","Ik wonen in Amsterdam.","Ik woont in Amsterdam.","Ik woon Amsterdam."],correct="Ik woon in Amsterdam."),
AssessmentQuestion(id="nl-a1-009",skill="reading",difficulty="A1",question="Je leest “Het station is dichtbij.” Wat betekent dit?",options=["The station is nearby.","The station is closed.","The station is far away.","The station is open."],correct="The station is nearby."),
AssessmentQuestion(id="nl-a1-010",skill="communication",difficulty="A1",question="Iemand helpt je. Wat zeg je?",options=["Dank je!","Hallo!","Tot ziens!","Pardon?"],correct="Dank je!"),
AssessmentQuestion(id="nl-a2-001",skill="grammar",difficulty="A2",question="Choose the correct form.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="nl-b1-001",skill="grammar",difficulty="B1",question="Choose the correct structure.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="nl-b2-001",skill="grammar",difficulty="B2",question="Choose the formal structure.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="nl-c1-001",skill="grammar",difficulty="C1",question="Choose the academic expression.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="nl-c2-001",skill="reading",difficulty="C2",question="Choose the best interpretation.",options=["A","B","C","D"],correct="A"),
]
