"""Bahasa Indonesia curriculum foundation."""
from app.data._types import CurriculumUnit
CURRICULUM={level:[CurriculumUnit(id=f"id-{level.lower()}-unit-1",level=level,unit_number=1,title=f"Bahasa Indonesia {level} communication",grammar_points=["basic word order","present tense"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Introduce yourself","Handle basic everyday exchanges"],default_weeks=2)] for level in ["A1","A2","B1","B2","C1","C2"]}
