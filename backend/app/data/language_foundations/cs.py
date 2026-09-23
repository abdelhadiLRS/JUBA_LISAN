"""Čeština foundation data for JUBA LISAN."""
from app.data._types import CurriculumUnit, GrammarExample, GrammarTopic, VocabularyEntry, VocabularySet, PhrasebookCategory, PhrasebookEntry, AssessmentQuestion

CURRICULUM={level:[CurriculumUnit(id=f"cs-{level.lower()}-unit-1",level=level,unit_number=1,title="Čeština {level} communication",grammar_points=["basic word order","present tense"],vocabulary_set_ids=["identity_a1"],lesson_types=["grammar","vocabulary","reading","writing","review"],competency_checklist=["Introduce yourself","Handle basic everyday exchanges"],default_weeks=2)] for level in ["A1","A2","B1","B2","C1","C2"]}

GRAMMAR_TOPICS=[GrammarTopic(slug="basic-word-order",title="Basic word order",level="A1",category="syntax",summary="Build simple sentences.",explanation="Learn the normal sentence pattern and basic subject-verb relationships.",examples=[GrammarExample(text="Ahoj.")]),GrammarTopic(slug="present-tense",title="Present tense",level="A1",category="verbs",summary="Talk about current actions and facts.",explanation="Use common present-tense forms in everyday statements.",examples=[GrammarExample(text="Ahoj.")])]

VOCABULARY_SETS=[VocabularySet(id="identity_a1",level="A1",topic="Greetings and identity",unit_ref="cs-a1-unit-1",words=[VocabularyEntry(word="Ahoj",pos="phrase",definition="greeting",example="Ahoj"),VocabularyEntry(word="Děkuji",pos="phrase",definition="thanks",example="Děkuji"),VocabularyEntry(word="jméno",pos="noun",definition="name",example="jméno"),VocabularyEntry(word="student",pos="noun",definition="student",example="student")])]

PHRASEBOOK_CATEGORIES=[PhrasebookCategory(id="greetings_a1",level="A1",situation="Greetings and introductions",icon="👋",phrases=[PhrasebookEntry(text="Ahoj",context="greeting",register="neutral"),PhrasebookEntry(text="Děkuji",context="expressing thanks",register="neutral")])]

ASSESSMENT_BANK=[AssessmentQuestion(id="cs-a1-001",skill="vocabulary",difficulty="A1",question="Which word means 'thanks'?",options=["Děkuji","A","B","C"],correct="Děkuji")]