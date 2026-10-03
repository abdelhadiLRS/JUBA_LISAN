import re
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.deps import get_current_user, require_learner
from app.core.limiter import limiter
from app.models.flashcard import Flashcard
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.flashcards import (FlashcardBulkCreate, FlashcardBulkResponse, FlashcardCreate, FlashcardFromWordRequest,
    FlashcardGenerateRequest, FlashcardGenerateResponse, FlashcardListResponse, FlashcardResponse, FlashcardReview, VocabularyListResponse)
from app.services.flashcard_sm2 import generate_flashcards, lookup_word, sm2_update
from app.services.feature_quota_service import feature_quota
from app.services.subscription_catalog import MAX_FLASHCARDS_PER_REQUEST
from app.services.llm_adapter import LLMError, LLMTimeoutError, LLMUnavailableError
from app.services.progress_service import update_daily_progress
from app.services.user_language_service import get_active_language

router = APIRouter(prefix="/api/flashcards", tags=["flashcards"], dependencies=[Depends(require_learner)])


def _normalize_flashcard_word(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


async def _get_active_plan_or_404(db: AsyncSession, user_id: int) -> StudyPlan:
    language = await get_active_language(db, user_id)
    if not language:
        raise HTTPException(status_code=404, detail="No active language set")
    plan = (await db.execute(select(StudyPlan).where(StudyPlan.user_language_id == language.id, StudyPlan.is_active.is_(True)))).scalar_one_or_none()
    if not plan:
        raise HTTPException(status_code=404, detail="No active study plan found")
    return plan


@router.get("/due", response_model=FlashcardListResponse)
@limiter.limit("60/minute")
async def get_due_flashcards(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plan = await _get_active_plan_or_404(db, current_user.id)
    filters = [Flashcard.user_id == current_user.id, Flashcard.study_plan_id == plan.id]
    due = (await db.execute(select(Flashcard).where(*filters, Flashcard.next_review <= date.today()).order_by(Flashcard.next_review))).scalars().all()
    total = (await db.execute(select(func.count(Flashcard.id)).where(*filters))).scalar()
    return FlashcardListResponse(due=due, total=total)


@router.get("/all", response_model=list[FlashcardResponse])
@limiter.limit("60/minute")
async def get_all_flashcards(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plan = await _get_active_plan_or_404(db, current_user.id)
    return (await db.execute(select(Flashcard).where(Flashcard.user_id == current_user.id, Flashcard.study_plan_id == plan.id).order_by(Flashcard.created_at.desc()))).scalars().all()


@router.post("", response_model=FlashcardResponse)
@limiter.limit("60/minute")
async def create_flashcard(request: Request, data: FlashcardCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plan = await _get_active_plan_or_404(db, current_user.id)
    card = Flashcard(user_id=current_user.id, study_plan_id=plan.id, word=data.word, definition=data.definition, example_sentence=data.example_sentence, translation=data.translation, source=data.source)
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return card


@router.post("/bulk", response_model=FlashcardBulkResponse)
@limiter.limit("60/minute")
async def create_flashcards_bulk(request: Request, data: FlashcardBulkCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plan = await _get_active_plan_or_404(db, current_user.id)
    existing = (await db.execute(select(Flashcard.word).where(Flashcard.user_id == current_user.id, Flashcard.study_plan_id == plan.id))).scalars().all()
    words = {_normalize_flashcard_word(word) for word in existing}
    created = 0
    for item in data.flashcards:
        normalized = _normalize_flashcard_word(item.word)
        if not normalized or normalized in words:
            continue
        db.add(Flashcard(user_id=current_user.id, study_plan_id=plan.id, word=item.word.strip(), definition=item.definition,
            example_sentence=item.example_sentence, translation=item.translation, source=item.source))
        words.add(normalized)
        created += 1
    await db.commit()
    return FlashcardBulkResponse(created=created)


@router.post("/{card_id}/review", response_model=FlashcardResponse)
@limiter.limit("60/minute")
async def review_flashcard(request: Request, card_id: int, data: FlashcardReview, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plan = await _get_active_plan_or_404(db, current_user.id)
    card = (await db.execute(select(Flashcard).where(Flashcard.id == card_id, Flashcard.user_id == current_user.id, Flashcard.study_plan_id == plan.id).with_for_update())).scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    # XP is earned only for a review the schedule actually asked for. The due
    # state must be captured before SM-2 moves next_review into the future, so
    # re-submitting the same review cannot farm XP. Early reviews still update
    # the schedule and the vocabulary skill signal, but award no XP.
    was_due = card.next_review is None or card.next_review <= date.today()
    card = sm2_update(card, data.quality)
    await db.commit()
    await db.refresh(card)
    await update_daily_progress(db, current_user.id, flashcard_reviewed=was_due, skill="vocabulary", skill_score=min(data.quality / 5.0, 1.0), study_plan_id=plan.id)
    return card


def _generation_error(exc):
    if isinstance(exc, LLMTimeoutError):
        return HTTPException(status_code=504, detail="The AI model took too long.")
    if isinstance(exc, LLMUnavailableError):
        return HTTPException(status_code=503, detail="ai_service_unavailable")
    return HTTPException(status_code=502, detail="ai_service_error")


@router.post("/generate", response_model=FlashcardGenerateResponse)
@limiter.limit("20/minute")
async def generate_flashcards_endpoint(request: Request, data: FlashcardGenerateRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not 1 <= data.count <= MAX_FLASHCARDS_PER_REQUEST:
        raise HTTPException(status_code=422, detail="Generate at most 20 cards per request")
    plan = await _get_active_plan_or_404(db, current_user.id)
    existing = (await db.execute(select(Flashcard.word).where(Flashcard.user_id == current_user.id, Flashcard.study_plan_id == plan.id))).scalars().all()
    words = {_normalize_flashcard_word(word) for word in existing}
    async with feature_quota(current_user, "flashcards", data.count, db=db) as quota:
        try:
            result = await generate_flashcards(topic=data.topic, count=data.count, cefr_level=data.cefr_level,
                native_language=current_user.native_language, target_language=data.target_language or plan.target_language)
        except (LLMTimeoutError, LLMUnavailableError, LLMError) as exc:
            raise _generation_error(exc) from exc
        unique = []
        for item in result.flashcards[:data.count]:
            normalized = _normalize_flashcard_word(item.word)
            if not normalized or normalized in words:
                continue
            words.add(normalized)
            unique.append(item)
            db.add(Flashcard(user_id=current_user.id, study_plan_id=plan.id, word=item.word.strip(), definition=item.definition,
                example_sentence=item.example_sentence, translation=item.translation))
        result.flashcards = unique
        quota.charge(len(unique))
        await quota.commit(db)
    return result


@router.post("/from-word", response_model=FlashcardResponse)
@limiter.limit("30/minute")
async def create_flashcard_from_word(request: Request, data: FlashcardFromWordRequest, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    plan = await _get_active_plan_or_404(db, current_user.id)
    normalized = _normalize_flashcard_word(data.word)
    if not normalized:
        raise HTTPException(status_code=422, detail="Word must not be empty")
    existing = (await db.execute(select(Flashcard).where(Flashcard.user_id == current_user.id, Flashcard.study_plan_id == plan.id))).scalars().all()
    cached = next((card for card in existing if _normalize_flashcard_word(card.word) == normalized), None)
    if cached is not None:
        return cached
    async with feature_quota(current_user, "flashcards", db=db) as quota:
        try:
            item = await lookup_word(word=data.word.strip(), context=data.context, cefr_level=data.cefr_level,
                native_language=current_user.native_language, target_language=plan.target_language)
        except (LLMTimeoutError, LLMUnavailableError, LLMError) as exc:
            raise _generation_error(exc) from exc
        card = Flashcard(user_id=current_user.id, study_plan_id=plan.id, word=item.word, definition=item.definition,
            example_sentence=item.example_sentence, translation=item.translation, source="from_text")
        db.add(card)
        await quota.commit(db)
        await db.refresh(card)
    return card


@router.get("/vocabulary", response_model=VocabularyListResponse)
@limiter.limit("60/minute")
async def get_vocabulary_flashcards(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), search: str = Query("")):
    plan = await _get_active_plan_or_404(db, current_user.id)
    filters = [Flashcard.user_id == current_user.id, Flashcard.study_plan_id == plan.id, Flashcard.source == "from_text"]
    if search:
        filters.append(Flashcard.word.ilike(f"%{search}%"))
    total = (await db.execute(select(func.count(Flashcard.id)).where(*filters))).scalar() or 0
    items = (await db.execute(select(Flashcard).where(*filters).order_by(func.lower(Flashcard.word)).offset((page - 1) * limit).limit(limit))).scalars().all()
    return VocabularyListResponse(items=items, total=total, page=page, pages=max(1, (total + limit - 1) // limit))


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("60/minute")
async def delete_flashcard(request: Request, card_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    card = await db.get(Flashcard, card_id)
    if not card or card.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    await db.delete(card)
    await db.commit()
