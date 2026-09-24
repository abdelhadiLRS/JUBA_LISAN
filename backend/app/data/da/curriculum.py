"""Danish CEFR curriculum foundation, expanded for staged integration."""
from app.data._types import CurriculumUnit

CEFR_LEVELS=["A1","A2","B1","B2","C1","C2"]
_TITLES={
"A1":["Hilsner og præsentation","Familie og hverdag","Tal, tid og aftaler","Mad og indkøb"],
"A2":["Bolig og omgivelser","Transport og rejser","Sundhed og velvære","Arbejde og fritid"],
"B1":["Uddannelse og arbejde","Medier og samfund","Relationer og følelser","Rejseoplevelser"],
"B2":["Argumentation og debat","Arbejdsliv og ledelse","Kultur og identitet","Problemer og løsninger"],
"C1":["Nuanceret kommunikation","Akademisk dansk","Professionel formidling","Samfundsanalyse"],
"C2":["Stil og register","Avanceret argumentation","Retorik og præcision","Kritisk analyse"],
}
_GRAMMAR={
"A1":["personlige pronominer","verbet at være","bestemt og ubestemt form","ordstilling i hovedsætninger"],
"A2":["datid","modalverber","refleksive verber","sammenligninger"],
"B1":["førnutid","fremtid","ledsætninger","relative pronominer"],
"B2":["passiv","betingelsessætninger","indirekte tale","konjunktioner"],
"C1":["nominalisering","participier","kompleks ledsætningsstruktur","tekstkohæsion"],
"C2":["inversion og fokus","registerskift","retoriske konstruktioner","syntaktisk variation"],
}
_GOALS=["Kan præsentere sig klart","Kan forstå og bruge centrale udtryk","Kan deltage i en naturlig samtale","Kan forklare egne synspunkter"]
CURRICULUM={}
for level in CEFR_LEVELS:
    units=[]
    for n,title in enumerate(_TITLES[level],1):
        gid=f"{level.lower()}-{n}"
        units.append(CurriculumUnit(
            id=f"{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,
            grammar_points=[_GRAMMAR[level][n-1],_GRAMMAR[level][(n)%4]],
            vocabulary_set_ids=[f"da-{level.lower()}-{n}"],
            lesson_types=["grammar","vocabulary","reading","writing","listening","review"],
            competency_checklist=[_GOALS[(n-1)%4],_GOALS[n%4]],
            default_weeks=2,
            prerequisite_unit=f"{level.lower()}-unit-{n-1}" if n>1 else None))
    CURRICULUM[level]=units
