"""Українська foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

CURRICULUM={level:[CurriculumUnit(id=f"uk-{level.lower()}-unit-1",level=level,unit_number=1,title="Українська {level} communication",grammar_points=["basic word order","present tense"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Introduce yourself","Handle basic everyday exchanges"],default_weeks=2)] for level in ["A1","A2","B1","B2","C1","C2"]}

GRAMMAR_TOPICS=[GrammarTopic(slug="basic-word-order",title="Basic word order",level="A1",category="syntax",summary="Build simple sentences.",explanation="Learn the normal sentence pattern and basic subject-verb relationships.",examples=[GrammarExample(text="Привіт.")]),GrammarTopic(slug="present-tense",title="Present tense",level="A1",category="verbs",summary="Talk about current actions and facts.",explanation="Use common present-tense forms in everyday statements.",examples=[GrammarExample(text="Привіт.")])]

VOCABULARY_SETS=[VocabularySet(id="identity_a1",level="A1",topic="Greetings and identity",unit_ref="uk-a1-unit-1",words=[VocabularyEntry(word="Привіт",pos="phrase",definition="greeting",example="Привіт"),VocabularyEntry(word="Дякую",pos="phrase",definition="thanks",example="Дякую"),VocabularyEntry(word="ім’я",pos="noun",definition="name",example="ім’я"),VocabularyEntry(word="студент",pos="noun",definition="student",example="студент")])]

PHRASEBOOK_CATEGORIES=[PhrasebookCategory(id="greetings_a1",level="A1",situation="Greetings and introductions",icon="👋",phrases=[PhrasebookEntry(text="Привіт",context="greeting",register="neutral"),PhrasebookEntry(text="Дякую",context="expressing thanks",register="neutral")])]

ASSESSMENT_BANK=[AssessmentQuestion(id="uk-a1-001",skill="vocabulary",difficulty="A1",question="Which word means 'thanks'?",options=["Дякую","A","B","C"],correct="Дякую")]