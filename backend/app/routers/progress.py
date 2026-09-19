from datetime import UTC, date, datetime, timedelta
from uuid import uuid4
import random
from typing import cast

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.limiter import limiter
from app.data._types import CEFRLevel
from app.data.vocabulary import get_vocabulary_by_level
from app.models.flashcard import Flashcard
from app.models.game_progress import GameProgress
from app.models.game_progress_event import GameProgressEvent
from app.models.game_session import GameSession
from app.models.progress import Progress
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.progress import (GameProgressEventCreate, GameSessionResponse, GameSessionStart, GameStatsResponse, ProgressHistoryResponse, ProgressResponse, ProgressSummary)
from app.services.progress_service import get_unit_competencies, update_daily_progress
from app.services.user_language_service import get_active_language

router = APIRouter(prefix="/api/progress", tags=["progress"])


GAME_SKILL_MAP = {
    "math": "math",
    "words": "vocabulary",
    "sequence": "logic",
    "memory": "memory",
    "matching": "vocabulary",
    "ordering": "ordering",
}


async def _get_game_skills(db: AsyncSession, plan: StudyPlan) -> dict[str, float]:
    result = await db.execute(
        select(Progress.skills)
        .where(Progress.study_plan_id == plan.id)
        .order_by(Progress.date.desc())
        .limit(1)
    )
    skills = result.scalar_one_or_none()
    return skills or {}


async def _get_active_plan_or_none(db: AsyncSession, user_id: int) -> StudyPlan | None:
    """Return the active study plan for the user's active language, or None if not set up yet."""
    active_lang = await get_active_language(db, user_id)
    if not active_lang:
        return None
    result = await db.execute(
        select(StudyPlan).where(
            StudyPlan.user_language_id == active_lang.id,
            StudyPlan.is_active.is_(True),
        )
    )
    return result.scalar_one_or_none()


async def _get_vocabulary_level_progress(
    db: AsyncSession, user_id: int, plan: StudyPlan
) -> tuple[int, int, float]:
    vocab_sets = get_vocabulary_by_level(cast(CEFRLevel, plan.cefr_level), plan.target_language)
    total_words = sum(len(vocab_set.words) for vocab_set in vocab_sets)
    if total_words == 0:
        return 0, 0, 0.0

    result = await db.execute(
        select(Flashcard.word).where(
            Flashcard.user_id == user_id,
            Flashcard.study_plan_id == plan.id,
            Flashcard.repetitions > 0,
        )
    )
    mastered_words = {word.strip().lower() for word in result.scalars().all()}
    mastered_count = sum(
        1
        for vocab_set in vocab_sets
        for word in vocab_set.words
        if word.word.strip().lower() in mastered_words
    )
    return mastered_count, total_words, mastered_count / total_words


@router.get("/summary", response_model=ProgressSummary)
@limiter.limit("60/minute")
async def get_summary(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return ProgressSummary(
            total_xp=0,
            current_streak=0,
            total_lessons=0,
            total_exercises=0,
            exercises_correct=0,
            accuracy=0.0,
            skills={},
        )

    vocabulary_mastered, vocabulary_total, vocabulary_progress = (
        await _get_vocabulary_level_progress(db, current_user.id, plan)
    )

    result = await db.execute(
        select(Progress).where(Progress.study_plan_id == plan.id).order_by(Progress.date.desc())
    )
    all_entries = result.scalars().all()

    if not all_entries:
        return ProgressSummary(
            total_xp=0,
            current_streak=0,
            total_lessons=0,
            total_exercises=0,
            exercises_correct=0,
            accuracy=0.0,
            skills={},
            vocabulary_level=plan.cefr_level,
            vocabulary_mastered=vocabulary_mastered,
            vocabulary_total=vocabulary_total,
            vocabulary_progress=round(vocabulary_progress, 2),
        )

    total_xp = sum(e.xp_earned for e in all_entries)
    total_lessons = sum(e.lessons_completed for e in all_entries)
    total_exercises = sum(e.exercises_total for e in all_entries)
    exercises_correct = sum(e.exercises_correct for e in all_entries)
    accuracy = exercises_correct / total_exercises if total_exercises > 0 else 0.0

    latest_skills = all_entries[0].skills if all_entries else {}
    latest_date = all_entries[0].date
    current_streak = (
        all_entries[0].streak_day
        if latest_date >= date.today() - timedelta(days=1)
        else 0
    )

    return ProgressSummary(
        total_xp=total_xp,
        current_streak=current_streak,
        total_lessons=total_lessons,
        total_exercises=total_exercises,
        exercises_correct=exercises_correct,
        accuracy=round(accuracy, 2),
        skills=latest_skills,
        vocabulary_level=plan.cefr_level,
        vocabulary_mastered=vocabulary_mastered,
        vocabulary_total=vocabulary_total,
        vocabulary_progress=round(vocabulary_progress, 2),
    )


@router.get("/game-summary", response_model=GameStatsResponse)
@limiter.limit("60/minute")
async def get_game_summary(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return GameStatsResponse(
            total_xp=0,
            games_played=0,
            questions_answered=0,
            correct_answers=0,
            best_round_score=0,
            daily_challenges_completed=0,
            last_daily_challenge_date="",
            current_correct_streak=0,
            best_correct_streak=0,
            achievements=[],
            skills={},
        )

    result = await db.execute(
        select(GameProgress).where(
            GameProgress.user_id == current_user.id,
            GameProgress.study_plan_id == plan.id,
        )
    )
    entry = result.scalar_one_or_none()
    if entry is None:
        return GameStatsResponse(
            total_xp=0,
            games_played=0,
            questions_answered=0,
            correct_answers=0,
            best_round_score=0,
            daily_challenges_completed=0,
            last_daily_challenge_date="",
            current_correct_streak=0,
            best_correct_streak=0,
            achievements=[],
            skills=await _get_game_skills(db, plan),
        )
    total_xp_result = await db.execute(
        select(Progress.xp_earned).where(Progress.study_plan_id == plan.id)
    )
    return GameStatsResponse(
        total_xp=sum(total_xp_result.scalars().all()),
        games_played=entry.games_played,
        questions_answered=entry.questions_answered,
        correct_answers=entry.correct_answers,
        best_round_score=entry.best_round_score,
        daily_challenges_completed=entry.daily_challenges_completed,
        last_daily_challenge_date=entry.last_daily_challenge_date,
        current_correct_streak=entry.current_correct_streak,
        best_correct_streak=entry.best_correct_streak,
        achievements=entry.achievements or [],
        skills=await _get_game_skills(db, plan),
    )


def _server_game_questions(game_id: str, language: str, difficulty: int) -> list[dict]:
    rng = random.SystemRandom()
    hints = {
        "ar": "فكّر بهدوء قبل اختيار الإجابة.",
        "fr": "Réfléchis avant de choisir.",
        "en": "Think carefully before choosing.",
    }
    questions: list[dict] = []
    for index in range(5):
        question_id = str(uuid4())
        if game_id == "math":
            maximum = {1: 18, 2: 60, 3: 150}[difficulty]
            a, b = 2 + rng.randrange(maximum), 2 + rng.randrange(maximum)
            subtraction = rng.random() > 0.5
            left, right = (max(a, b), min(a, b)) if subtraction else (a, b)
            answer = left - right if subtraction else left + right
            spread = {1: 2, 2: 5, 3: 10}[difficulty]
            choices = [str(answer), str(answer + 1), str(answer - 1), str(answer + spread)]
            rng.shuffle(choices)
            prompt = f"{left} {'-' if subtraction else '+'} {right} = ?"
            skill, topic = "math", "arithmetic"
        elif game_id == "sequence":
            start = 2 + rng.randrange(difficulty * 4)
            step = 2 + rng.randrange(difficulty * 4)
            answer = start + step * 4
            values = [start + step * n for n in range(4)]
            choices = [str(answer), str(answer + step), str(answer - step), str(answer + 2 * step)]
            rng.shuffle(choices)
            prompt = "  →  ".join(map(str, values)) + "  →  ?"
            skill, topic = "logic", "sequences"
        elif game_id == "memory":
            symbols = {
                "ar": ["قمر", "كتاب", "بحر", "شمس", "قلم", "باب"],
                "fr": ["lune", "livre", "mer", "soleil", "stylo", "porte"],
                "en": ["moon", "book", "sea", "sun", "pen", "door"],
            }[language]
            size = {1: 3, 2: 4, 3: 5}[difficulty]
            shown = rng.sample(symbols, size)
            answer = " • ".join(shown)
            alternatives = [answer]
            while len(alternatives) < 4:
                candidate = " • ".join(rng.sample(shown, len(shown)))
                if candidate not in alternatives:
                    alternatives.append(candidate)
            rng.shuffle(alternatives)
            choices, prompt = alternatives, f"Remember this order:\n\n{answer}"
            skill, topic = "memory", "memory-sequence"
        elif game_id == "matching":
            pairs = {
                "ar": [("كتاب", "book"), ("ماء", "water"), ("مدرسة", "school"), ("قلم", "pen")],
                "fr": [("livre", "book"), ("eau", "water"), ("école", "school"), ("stylo", "pen")],
                "en": [("book", "livre"), ("water", "eau"), ("school", "école"), ("pen", "stylo")],
            }[language]
            left, answer = rng.choice(pairs)
            wrong = [value for key, value in pairs if key != left]
            rng.shuffle(wrong)
            choices = [answer, *wrong[:3]]
            rng.shuffle(choices)
            prompt = f"Match: {left}" if language == "en" else (f"Associe : {left}" if language == "fr" else f"طابق: {left}")
            skill, topic = "vocabulary", "matching"
        else:
            base = {1: [1, 2, 3, 4], 2: [2, 4, 6, 8], 3: [3, 6, 9, 12]}[difficulty]
            scrambled = base[:]
            rng.shuffle(scrambled)
            answer = " → ".join(map(str, base))
            alternatives = [answer, " → ".join(map(str, reversed(base))), " → ".join(map(str, base[1:] + base[:1]))]
            if " → ".join(map(str, scrambled)) not in alternatives:
                alternatives.append(" → ".join(map(str, scrambled)))
            choices = list(dict.fromkeys(alternatives))[:4]
            rng.shuffle(choices)
            prompt = (
                f"Order from smallest to largest: {' · '.join(map(str, scrambled))}"
                if language == "en"
                else (f"Ordonne du plus petit au plus grand : {' · '.join(map(str, scrambled))}"
                      if language == "fr"
                      else f"رتّب الأرقام من الأصغر إلى الأكبر: {' · '.join(map(str, scrambled))}")
            skill, topic = "ordering", "ordering"
        questions.append({
            "id": question_id,
            "prompt": prompt,
            "choices": choices,
            "answer": str(answer),
            "hint": hints[language],
            "skill": skill,
            "difficulty": difficulty,
            "topic": topic,
        })
    return questions


@router.post("/game-session", response_model=GameSessionResponse)
@limiter.limit("30/minute")
async def start_game_session(
    request: Request,
    data: GameSessionStart,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Issue an opaque server-owned question set for a verifiable game round."""
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No active study plan found")

    session_id = str(uuid4())
    now = datetime.now(UTC).replace(tzinfo=None)
    expires_at = now + timedelta(minutes=15)
    questions = _server_game_questions(data.game_id, data.language, data.difficulty)
    session = GameSession(
        id=session_id,
        user_id=current_user.id,
        study_plan_id=plan.id,
        game_id=data.game_id,
        language=data.language,
        difficulty=data.difficulty,
        questions=questions,
        started_at=now,
        expires_at=expires_at,
        completed=False,
    )
    db.add(session)
    await db.commit()
    public_questions = [
        {key: item[key] for key in ("id", "prompt", "choices", "hint", "skill", "difficulty")}
        for item in questions
    ]
    return GameSessionResponse(
        session_id=session_id,
        game_id=data.game_id,
        questions=public_questions,
        expires_at=expires_at.isoformat(),
    )


@router.post("/game-event", response_model=GameStatsResponse)
@limiter.limit("60/minute")
async def record_game_event(
    request: Request,
    data: GameProgressEventCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Record one completed game exactly once and update the server aggregate."""
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No active study plan found")
    if data.daily_challenge and data.daily_challenge_date != date.today().isoformat():
        raise HTTPException(status_code=422, detail="daily_challenge_date must be today")

    existing_result = await db.execute(
        select(GameProgressEvent).where(
            GameProgressEvent.user_id == current_user.id,
            GameProgressEvent.study_plan_id == plan.id,
            GameProgressEvent.event_id == data.event_id,
        )
    )
    if existing_result.scalar_one_or_none() is not None:
        aggregate_result = await db.execute(
            select(GameProgress).where(
                GameProgress.user_id == current_user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
        aggregate = aggregate_result.scalar_one_or_none()
        if aggregate is None:
            raise HTTPException(status_code=409, detail="Game event already exists without an aggregate")
        total_xp_result = await db.execute(
            select(Progress.xp_earned).where(Progress.study_plan_id == plan.id)
        )
        return GameStatsResponse(
            total_xp=sum(total_xp_result.scalars().all()),
            games_played=aggregate.games_played,
            questions_answered=aggregate.questions_answered,
            correct_answers=aggregate.correct_answers,
            best_round_score=aggregate.best_round_score,
            daily_challenges_completed=aggregate.daily_challenges_completed,
            last_daily_challenge_date=aggregate.last_daily_challenge_date,
            current_correct_streak=aggregate.current_correct_streak,
            best_correct_streak=aggregate.best_correct_streak,
            achievements=aggregate.achievements or [],
            skills=await _get_game_skills(db, plan),
        )

    try:
        # Game XP is derived from the validated result; client-supplied XP/achievement rewards are ignored.
        base_xp = (data.correct_answers * 5) + max(0, data.questions_answered - data.correct_answers)
        current_total_xp_result = await db.execute(
            select(Progress.xp_earned).where(Progress.study_plan_id == plan.id)
        )
        total_xp_before = sum(current_total_xp_result.scalars().all())
        event = GameProgressEvent(
            event_id=data.event_id,
            user_id=current_user.id,
            study_plan_id=plan.id,
            game_id=data.game_id,
            questions_answered=data.questions_answered,
            correct_answers=data.correct_answers,
            round_score=data.round_score,
            daily_challenge=data.daily_challenge,
            daily_challenge_date=data.daily_challenge_date,
            achievements=[],
            xp_earned=base_xp,
        )
        db.add(event)
        await db.flush()

        result = await db.execute(
            select(GameProgress).where(
                GameProgress.user_id == current_user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
        entry = result.scalar_one_or_none()
        if entry is None:
            entry = GameProgress(
                user_id=current_user.id,
                study_plan_id=plan.id,
                achievements=[],
            )
            db.add(entry)
            await db.flush()

        entry.games_played += 1
        entry.questions_answered += data.questions_answered
        entry.correct_answers += data.correct_answers
        entry.best_round_score = max(entry.best_round_score, data.round_score)

        if (
            data.daily_challenge
            and data.daily_challenge_date
            and entry.last_daily_challenge_date != data.daily_challenge_date
        ):
            entry.daily_challenges_completed += 1
            entry.last_daily_challenge_date = data.daily_challenge_date

        if data.questions_answered > 0 and data.correct_answers == data.questions_answered:
            entry.current_correct_streak += data.correct_answers
            entry.best_correct_streak = max(
                entry.best_correct_streak, entry.current_correct_streak
            )
        else:
            entry.current_correct_streak = 0

        candidate_achievements: list[str] = []
        if entry.games_played == 1:
            candidate_achievements.append("first_game")
        if data.questions_answered > 0 and data.correct_answers == data.questions_answered:
            candidate_achievements.append("perfect_round")
        if entry.best_correct_streak >= 5:
            candidate_achievements.append("streak_5")
        if data.daily_challenge:
            candidate_achievements.append("daily_challenge")

        # Evaluate multi-skill progress from server-owned daily skills. The
        # current game's mapped skill counts as active only when the event has
        # at least one question, so the client cannot unlock this reward by
        # claiming an arbitrary achievement.
        current_skill = GAME_SKILL_MAP.get(data.game_id)
        current_skill_score = (
            data.correct_answers / data.questions_answered
            if data.questions_answered > 0
            else None
        )
        latest_progress_result = await db.execute(
            select(Progress.skills)
            .where(Progress.study_plan_id == plan.id)
            .order_by(Progress.date.desc())
            .limit(1)
        )
        existing_skills = latest_progress_result.scalar_one_or_none() or {}
        projected_skills = dict(existing_skills)
        if (
            current_skill
            and current_skill_score is not None
            and current_skill_score > 0
        ):
            projected_skills[current_skill] = current_skill_score
        active_skill_count = sum(
            1 for skill, score in projected_skills.items() if skill and float(score) > 0
        )
        if active_skill_count >= 3:
            candidate_achievements.append("multi_skill")

        reward_by_achievement = {
            "first_game": 25,
            "perfect_round": 50,
            "streak_5": 40,
            "xp_100": 25,
            "xp_500": 100,
            "daily_challenge": 60,
            "multi_skill": 75,
        }
        existing_achievements = set(entry.achievements or [])
        fresh_achievements = [
            achievement
            for achievement in dict.fromkeys(candidate_achievements)
            if achievement not in existing_achievements
        ]

        # Apply ordinary achievement rewards first, then evaluate XP thresholds
        # against the projected total so crossing 100/500 XP is rewarded in
        # the same event that crosses the threshold.
        achievement_xp = sum(reward_by_achievement[item] for item in fresh_achievements)
        projected_xp = total_xp_before + base_xp + achievement_xp
        if projected_xp >= 100 and "xp_100" not in existing_achievements:
            fresh_achievements.append("xp_100")
            achievement_xp += reward_by_achievement["xp_100"]
            projected_xp += reward_by_achievement["xp_100"]
        if projected_xp >= 500 and "xp_500" not in existing_achievements:
            fresh_achievements.append("xp_500")
            achievement_xp += reward_by_achievement["xp_500"]

        entry.achievements = list(
            dict.fromkeys([*(entry.achievements or []), *fresh_achievements])
        )

        progress_entry = await update_daily_progress(
            db,
            current_user.id,
            study_plan_id=plan.id,
            xp=base_xp + achievement_xp,
            skill=GAME_SKILL_MAP.get(data.game_id),
            skill_score=(data.correct_answers / data.questions_answered) if data.questions_answered > 0 else None,
            commit=False,
        )
        if progress_entry is None:
            raise HTTPException(status_code=500, detail="Unable to persist game XP")

        event.xp_earned = base_xp + achievement_xp
        entry.updated_at = datetime.now(UTC).replace(tzinfo=None)
        await db.commit()
        await db.refresh(entry)
        return GameStatsResponse(
            total_xp=sum((await db.execute(select(Progress.xp_earned).where(Progress.study_plan_id == plan.id))).scalars().all()),
            games_played=entry.games_played,
            questions_answered=entry.questions_answered,
            correct_answers=entry.correct_answers,
            best_round_score=entry.best_round_score,
            daily_challenges_completed=entry.daily_challenges_completed,
            last_daily_challenge_date=entry.last_daily_challenge_date,
            current_correct_streak=entry.current_correct_streak,
            best_correct_streak=entry.best_correct_streak,
            achievements=entry.achievements or [],
            skills=await _get_game_skills(db, plan),
        )
    except IntegrityError:
        await db.rollback()
        existing_result = await db.execute(
            select(GameProgressEvent).where(
                GameProgressEvent.user_id == current_user.id,
                GameProgressEvent.study_plan_id == plan.id,
                GameProgressEvent.event_id == data.event_id,
            )
        )
        if existing_result.scalar_one_or_none() is None:
            raise
        aggregate_result = await db.execute(
            select(GameProgress).where(
                GameProgress.user_id == current_user.id,
                GameProgress.study_plan_id == plan.id,
            )
        )
        aggregate = aggregate_result.scalar_one_or_none()
        if aggregate is None:
            raise HTTPException(status_code=409, detail="Game event exists without an aggregate")
        total_xp_result = await db.execute(
            select(Progress.xp_earned).where(Progress.study_plan_id == plan.id)
        )
        return GameStatsResponse(
            total_xp=sum(total_xp_result.scalars().all()),
            games_played=aggregate.games_played,
            questions_answered=aggregate.questions_answered,
            correct_answers=aggregate.correct_answers,
            best_round_score=aggregate.best_round_score,
            daily_challenges_completed=aggregate.daily_challenges_completed,
            last_daily_challenge_date=aggregate.last_daily_challenge_date,
            current_correct_streak=aggregate.current_correct_streak,
            best_correct_streak=aggregate.best_correct_streak,
            achievements=aggregate.achievements or [],
            skills=await _get_game_skills(db, plan),
        )


@router.post("/game-summary", deprecated=True)
@limiter.limit("60/minute")
async def reject_legacy_game_summary(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    raise HTTPException(
        status_code=410,
        detail="Legacy absolute game-summary sync is retired; submit /api/progress/game-event instead",
    )


@router.get("/history", response_model=ProgressHistoryResponse)
@limiter.limit("60/minute")
async def get_history(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return ProgressHistoryResponse(entries=[])

    result = await db.execute(
        select(Progress)
        .where(Progress.study_plan_id == plan.id)
        .order_by(Progress.date.desc())
        .limit(90)
    )
    entries = result.scalars().all()
    return ProgressHistoryResponse(entries=entries)


@router.get("/competencies", response_model=list)
@limiter.limit("60/minute")
async def get_competencies(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return []
    return await get_unit_competencies(db, current_user.id, study_plan_id=plan.id)
