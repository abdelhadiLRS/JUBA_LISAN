"""Nederlands assessment foundation."""
from app.data._types import AssessmentQuestion
ASSESSMENT_BANK=[
AssessmentQuestion(id="nl-a1-001",skill="vocabulary",difficulty="A1",question="Choose the basic greeting.",options=["hallo","X","Y","Z"],correct="hallo"),
AssessmentQuestion(id="nl-a2-001",skill="grammar",difficulty="A2",question="Choose the correct form.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="nl-b1-001",skill="grammar",difficulty="B1",question="Choose the correct structure.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="nl-b2-001",skill="grammar",difficulty="B2",question="Choose the formal structure.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="nl-c1-001",skill="grammar",difficulty="C1",question="Choose the academic expression.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="nl-c2-001",skill="reading",difficulty="C2",question="Choose the best interpretation.",options=["A","B","C","D"],correct="A"),
]