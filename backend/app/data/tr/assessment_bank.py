"""Türkçe assessment foundation."""
from app.data._types import AssessmentQuestion
ASSESSMENT_BANK=[
AssessmentQuestion(id="tr-a1-001",skill="vocabulary",difficulty="A1",question="Choose the basic greeting.",options=["Merhaba","X","Y","Z"],correct="Merhaba"),
AssessmentQuestion(id="tr-a2-001",skill="grammar",difficulty="A2",question="Choose the correct form.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="tr-b1-001",skill="grammar",difficulty="B1",question="Choose the correct structure.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="tr-b2-001",skill="grammar",difficulty="B2",question="Choose the formal structure.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="tr-c1-001",skill="grammar",difficulty="C1",question="Choose the academic expression.",options=["A","B","C","D"],correct="A"),
AssessmentQuestion(id="tr-c2-001",skill="reading",difficulty="C2",question="Choose the best interpretation.",options=["A","B","C","D"],correct="A"),
]