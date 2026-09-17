"""
Community and Professional pages router for JUBA LISAN
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.core.database import get_db
from app.models.user import User

router = APIRouter(prefix="/api", tags=["community", "professional"])


# ==================== Community Models ====================

class ChallengeCreate(BaseModel):
    title: str
    description: str
    language_code: str
    start_date: datetime
    end_date: datetime
    target_participants: int = 100
    reward_xp: int = 500
    reward_badge: str = "challenge_master"

class ChallengeResponse(BaseModel):
    id: str
    title: str
    description: str
    language_code: str
    start_date: datetime
    end_date: datetime
    participants_count: int
    target_participants: int
    reward_xp: int
    reward_badge: str
    user_joined: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class ClubCreate(BaseModel):
    name: str
    description: str
    language_code: str
    is_public: bool = True
    max_members: int = 50

class ClubResponse(BaseModel):
    id: str
    name: str
    description: str
    language_code: str
    members_count: int
    max_members: int
    is_public: bool
    created_by: str
    created_at: datetime

    class Config:
        from_attributes = True

class StudyPartnerRequest(BaseModel):
    user_id: str
    native_language: str
    target_language: str
    level: str = "intermediate"
    availability: List[str] = []  # e.g., ["weekends", "evenings"]
    interests: List[str] = []

class StudyPartnerResponse(BaseModel):
    id: str
    user_id: str
    user_name: str
    user_avatar: Optional[str]
    native_language: str
    target_language: str
    level: str
    availability: List[str]
    interests: List[str]
    match_score: float = 0.0
    created_at: datetime


# ==================== Professional Models ====================

class ProfessionalCourseCreate(BaseModel):
    title: str
    description: str
    language_code: str
    category: str  # business, academic, medical, legal, technical
    level: str  # beginner, intermediate, advanced
    duration_hours: int
    price: float = 0.0
    certificate_available: bool = True

class ProfessionalCourseResponse(BaseModel):
    id: str
    title: str
    description: str
    language_code: str
    category: str
    level: str
    duration_hours: int
    price: float
    enrolled_count: int
    certificate_available: bool
    rating: float = 0.0
    created_at: datetime

    class Config:
        from_attributes = True

class CertificationExamCreate(BaseModel):
    title: str
    language_code: str
    category: str
    duration_minutes: int = 120
    passing_score: float = 70.0
    price: float = 99.0
    validity_months: int = 24

class CertificationExamResponse(BaseModel):
    id: str
    title: str
    language_code: str
    category: str
    duration_minutes: int
    passing_score: float
    price: float
    validity_months: int
    attempts_count: int
    created_at: datetime

    class Config:
        from_attributes = True

class EnrollmentCreate(BaseModel):
    user_id: str
    course_id: str
    payment_method: str = "card"

class EnrollmentResponse(BaseModel):
    id: str
    user_id: str
    course_id: str
    course_title: str
    enrollment_date: datetime
    progress: float = 0.0
    completed: bool = False
    certificate_earned: bool = False

    class Config:
        from_attributes = True


# ==================== Community Routes ====================

@router.get("/community/challenges", response_model=List[ChallengeResponse])
async def get_active_challenges(
    language_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all active community challenges"""
    # Mock implementation - replace with actual DB query
    challenges = [
        {
            "id": "challenge-1",
            "title": "30-Day Arabic Speaking Challenge",
            "description": "Practice speaking Arabic every day for 30 days",
            "language_code": "ar",
            "start_date": datetime.now(),
            "end_date": datetime.now(),
            "participants_count": 245,
            "target_participants": 500,
            "reward_xp": 1000,
            "reward_badge": "arabic_speaker",
            "user_joined": False
        }
    ]
    return challenges


@router.post("/community/challenges", response_model=ChallengeResponse)
async def create_challenge(
    challenge: ChallengeCreate,
    db: Session = Depends(get_db)
):
    """Create a new community challenge"""
    # Mock implementation
    return ChallengeResponse(
        id=f"challenge-{datetime.now().timestamp()}",
        **challenge.model_dump(),
        participants_count=0,
        user_joined=False
    )


@router.get("/community/clubs", response_model=List[ClubResponse])
async def get_clubs(
    language_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all language clubs"""
    clubs = [
        {
            "id": "club-1",
            "name": "Arabic Conversation Club",
            "description": "Weekly conversation practice for Arabic learners",
            "language_code": "ar",
            "members_count": 45,
            "max_members": 50,
            "is_public": True,
            "created_by": "user-123",
            "created_at": datetime.now()
        }
    ]
    return clubs


@router.post("/community/partners/find", response_model=List[StudyPartnerResponse])
async def find_study_partners(
    request: StudyPartnerRequest,
    db: Session = Depends(get_db)
):
    """Find compatible study partners based on language exchange"""
    # Mock implementation - in real app, use matching algorithm
    partners = [
        {
            "id": "partner-1",
            "user_id": "user-456",
            "user_name": "Ahmed",
            "user_avatar": "/avatars/ahmed.png",
            "native_language": "ar",
            "target_language": "en",
            "level": "intermediate",
            "availability": ["weekends", "evenings"],
            "interests": ["culture", "business"],
            "match_score": 0.85,
            "created_at": datetime.now()
        }
    ]
    return partners


# ==================== Professional Routes ====================

@router.get("/professional/courses", response_model=List[ProfessionalCourseResponse])
async def get_professional_courses(
    category: Optional[str] = None,
    language_code: Optional[str] = None,
    level: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get professional development courses"""
    courses = [
        {
            "id": "course-1",
            "title": "Business Arabic for Professionals",
            "description": "Master Arabic for business communication",
            "language_code": "ar",
            "category": "business",
            "level": "intermediate",
            "duration_hours": 40,
            "price": 199.99,
            "enrolled_count": 156,
            "certificate_available": True,
            "rating": 4.8,
            "created_at": datetime.now()
        }
    ]
    return courses


@router.post("/professional/courses/{course_id}/enroll", response_model=EnrollmentResponse)
async def enroll_in_course(
    course_id: str,
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db)
):
    """Enroll in a professional course"""
    # Mock implementation
    return EnrollmentResponse(
        id=f"enrollment-{datetime.now().timestamp()}",
        user_id=enrollment.user_id,
        course_id=course_id,
        course_title="Business Arabic for Professionals",
        enrollment_date=datetime.now(),
        progress=0.0,
        completed=False,
        certificate_earned=False
    )


@router.get("/professional/certifications", response_model=List[CertificationExamResponse])
async def get_certifications(
    language_code: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get available certification exams"""
    certifications = [
        {
            "id": "cert-1",
            "title": "JUBA Arabic Proficiency Certificate - Business",
            "language_code": "ar",
            "category": "business",
            "duration_minutes": 120,
            "passing_score": 70.0,
            "price": 99.0,
            "validity_months": 24,
            "attempts_count": 0,
            "created_at": datetime.now()
        }
    ]
    return certifications


@router.post("/professional/certifications/{cert_id}/register")
async def register_for_certification(
    cert_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):
    """Register for a certification exam"""
    return {
        "success": True,
        "registration_id": f"reg-{datetime.now().timestamp()}",
        "exam_date": datetime.now(),
        "message": "Registration successful. Check your email for details."
    }
