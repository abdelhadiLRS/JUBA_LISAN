"""Nederlands CEFR curriculum A1-C2."""
from app.data._types import CurriculumUnit
def _u(level,n,title,g,goals,pr=None):
 return CurriculumUnit(id=f"{level.lower()}-unit-{n}",level=level,unit_number=n,title=title,grammar_points=g,vocabulary_set_ids=["greetings_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=goals,default_weeks=2,prerequisite_unit=pr)
CURRICULUM = {
"A1":[_u("A1",1,"Basics and identity",["pronouns","word-order"],["Develop A1 communication skills"])],
"A2":[_u("A2",1,"Daily situations",["present-tense","past-tense"],["Develop A2 communication skills"], "a1-unit-1")],
"B1":[_u("B1",1,"Communication and work",["perfect","separable-verbs"],["Develop B1 communication skills"], "a2-unit-1")],
"B2":[_u("B2",1,"Argumentation and formal language",["conditionals","passive"],["Develop B2 communication skills"], "b1-unit-1")],
"C1":[_u("C1",1,"Academic and professional language",["reported-speech","academic-register"],["Develop C1 communication skills"], "b2-unit-1")],
"C2":[_u("C2",1,"Advanced style and discourse",["discourse","style"],["Develop C2 communication skills"], "c1-unit-1")]
}