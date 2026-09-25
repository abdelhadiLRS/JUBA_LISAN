import random
from datetime import UTC, date, datetime, timedelta
from typing import Literal, cast
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, text, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user, require_learner
from app.core.limiter import limiter
from app.data._types import CEFRLevel
from app.data.grammar import get_grammar_topics
from app.data.vocabulary import get_vocabulary_by_level
from app.models.flashcard import Flashcard
from app.models.lesson import Exercise, Lesson
from app.models.exercise_attempt import ExerciseAttempt
from app.models.game_progress import GameProgress
from app.models.game_progress_event import GameProgressEvent
from app.models.game_session import GameSession
from app.models.learning_goal import LearningGoal
from app.models.learning_goal_milestone import LearningGoalMilestone
from app.models.progress import Progress
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.schemas.progress import (GameSessionComplete, GameSessionResponse, GameSessionResultResponse, GameSessionStart, GameStatsResponse, LearningGoalMilestoneResponse, LearningGoalMilestoneSummary, LearningGoalResponse, LearningGoalUpdate, MasteryCenterResponse, MasteryCenterLessonResponse, ProgressHistoryResponse, ProgressRangeSummary, ProgressResponse, ProgressSummary)
from app.services.progress_service import get_unit_competencies, update_daily_progress
from app.services.lesson_mastery import _skill_mastery_state, select_next_skill_mastery, summarize_lesson_mastery, summarize_skill_mastery
from app.services.user_language_service import get_active_language

router = APIRouter(prefix="/api/progress", tags=["progress"], dependencies=[Depends(require_learner)])


GAME_SKILL_MAP = {
    "math": "math",
    "words": "vocabulary",
    "quick_choice": "vocabulary",
    "context_quest": "speaking",
    "listen_choose": "listening",
    "listening_detective": "listening",
    "word_categories": "vocabulary",
    "translation_sprint": "writing",
    "grammar_duel": "grammar",
    "spelling": "writing",
    "word_scramble": "vocabulary",
    "fill_blank": "grammar",
    "sequence": "logic",
    "memory": "memory",
    "matching": "vocabulary",
    "ordering": "ordering",
    "sentence_builder": "grammar",
}

DAILY_GAME_IDS = (
    "matching",
    "quick_choice",
    "sentence_builder",
    "listen_choose",
    "spelling",
    "word_scramble",
    "fill_blank",
    "memory",
    "context_quest",
    "listening_detective",
    "word_categories",
    "translation_sprint",
    "grammar_duel",
)


def _daily_game_id(day: date) -> str:
    """Return the same deterministic daily-game slot used by the web client."""
    # JavaScript Date#getDay() is Sunday=0..Saturday=6; Python weekday() is
    # Monday=0..Sunday=6. Keep the existing UI rotation stable without trusting
    # the client to choose which game qualifies for the daily reward.
    return DAILY_GAME_IDS[((day.weekday() + 1) % 7) % len(DAILY_GAME_IDS)]


def _normalize_game_text(value: str) -> str:
    """Normalize learner text without changing its linguistic meaning."""
    normalized = " ".join(value.strip().casefold().split())
    return normalized.strip(".,!?;:。！？；：،،"'«»“”()[]{}")


def _game_answer_matches(submitted: str, expected: object) -> bool:
    candidate = _normalize_game_text(submitted)
    if isinstance(expected, (list, tuple, set)):
        return any(candidate == _normalize_game_text(str(item)) for item in expected)
    return candidate == _normalize_game_text(str(expected))



def _server_interactive_challenge(
    game_id: str, language: str, difficulty: int, target_language: str = "en-GB", cefr_level: CEFRLevel = "A1"
) -> tuple[dict, dict]:
    """Build a renderable challenge plus server-only solution state."""
    rng = random.SystemRandom()
    if game_id == "memory":
        count = {1: 3, 2: 4, 3: 5}[difficulty]
        selected_entries = cefr_entries[:count]
        if len(selected_entries) < count:
            raise ValueError(f"No vocabulary content for {target_language} at {cefr_level}")
        selected = [(entry.word.strip(), entry.definition.strip()) for entry in selected_entries]
        cards = []
        pairs = {}
        for index, (left, right) in enumerate(selected):
            a, b = str(uuid4()), str(uuid4())
            cards.extend([{"id": a, "label": left, "pair_key": str(index)}, {"id": b, "label": right, "pair_key": str(index)}])
            pairs[a] = index
            pairs[b] = index
        rng.shuffle(cards)
        return {"type": "memory", "cards": cards}, {"pairs": pairs, "pair_count": count}
    if game_id == "matching":
        count = {1: 3, 2: 4, 3: 5}[difficulty]
        pairs_source = [(entry.word.strip(), entry.definition.strip()) for entry in cefr_entries[:count]]
        if len(pairs_source) < count:
            raise ValueError(f"No vocabulary content for {target_language} at {cefr_level}")
        rng.shuffle(pairs_source)
        left, right = [], []
        pairs = {}
        for left_label, right_label in pairs_source:
            left_id, right_id = str(uuid4()), str(uuid4())
            left.append({"id": left_id, "label": left_label, "pair_key": str(len(left))})
            right.append({"id": right_id, "label": right_label, "pair_key": str(len(right))})
            pairs[left_id] = right_id
        rng.shuffle(left)
        rng.shuffle(right)
        return {"type": "matching", "left": left, "right": right}, {"pairs": pairs, "pair_count": len(left)}
    if game_id in {"ordering", "sentence_builder"}:
        if game_id == "sentence_builder":
            sentence_entries = [entry for entry in cefr_entries if entry.example.strip()]
            if not sentence_entries:
                raise ValueError(f"No example sentences for {target_language} at {cefr_level}")
            source = sentence_entries[0].example.strip().split()

        else:\n            count = {1: 3, 2: 4, 3: 5}[difficulty]\n            ordered_entries = cefr_entries[:count]\n            if len(ordered_entries) < count:\n                raise ValueError(f"No vocabulary content for {target_language} at {cefr_level}")\n            source = [entry.word.strip() for entry in ordered_entries]
        items = [{"id": str(uuid4()), "label": label} for label in source]
        shuffled = list(items)
        rng.shuffle(shuffled)
        return {"type": "ordering", "items": shuffled}, {"target": [item["id"] for item in items]}
    raise ValueError("Unsupported interactive game")

async def _get_game_skills(
    db: AsyncSession, user_id: int, plan: StudyPlan
) -> dict[str, float]:
    result = await db.execute(
        select(Progress.skills)
        .where(
            Progress.user_id == user_id,
            Progress.study_plan_id == plan.id,
        )
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
        select(Progress)
        .where(
            Progress.user_id == current_user.id,
            Progress.study_plan_id == plan.id,
        )
        .order_by(Progress.date.desc())
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
            skills=await _get_game_skills(db, current_user.id, plan),
        )
    total_xp_result = await db.execute(
        select(Progress.xp_earned).where(
            Progress.user_id == current_user.id,
            Progress.study_plan_id == plan.id,
        )
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
        skills=await _get_game_skills(db, current_user.id, plan),
    )


async def _get_or_create_learning_goal(
    db: AsyncSession, user_id: int, plan: StudyPlan
) -> LearningGoal:
    result = await db.execute(
        select(LearningGoal).where(
            LearningGoal.user_id == user_id,
            LearningGoal.study_plan_id == plan.id,
        )
    )
    goal = result.scalar_one_or_none()
    if goal is not None:
        return goal

    goal = LearningGoal(
        user_id=user_id,
        study_plan_id=plan.id,
        daily_xp_target=50,
        weekly_xp_target=250,
    )
    try:
        async with db.begin_nested():
            db.add(goal)
            await db.flush()
    except IntegrityError:
        result = await db.execute(
            select(LearningGoal).where(
                LearningGoal.user_id == user_id,
                LearningGoal.study_plan_id == plan.id,
            )
        )
        goal = result.scalar_one()
    return goal


async def _learning_goal_response(
    db: AsyncSession, user_id: int, plan: StudyPlan, goal: LearningGoal
) -> LearningGoalResponse:
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    result = await db.execute(
        select(Progress).where(
            Progress.user_id == user_id,
            Progress.study_plan_id == plan.id,
            Progress.date >= week_start,
            Progress.date <= today,
        )
    )
    entries = result.scalars().all()
    daily_xp = sum(max(entry.xp_earned - entry.reward_xp, 0) for entry in entries if entry.date == today)
    weekly_xp = sum(max(entry.xp_earned - entry.reward_xp, 0) for entry in entries)

    return LearningGoalResponse(
        daily_xp_target=goal.daily_xp_target,
        weekly_xp_target=goal.weekly_xp_target,
        daily_xp=daily_xp,
        weekly_xp=weekly_xp,
        daily_progress=round(min(daily_xp / goal.daily_xp_target, 1.0), 3),
        weekly_progress=round(min(weekly_xp / goal.weekly_xp_target, 1.0), 3),
        daily_completed=daily_xp >= goal.daily_xp_target,
        weekly_completed=weekly_xp >= goal.weekly_xp_target,
        daily_reward_xp=25 if goal.daily_reward_date == today else 0,
        weekly_reward_xp=75 if goal.weekly_reward_start == week_start else 0,
        daily_reward_claimed=goal.daily_reward_date == today,
        weekly_reward_claimed=goal.weekly_reward_start == week_start,
        day=today,
        week_start=week_start,
        week_end=week_end,
    )


@router.get("/goals", response_model=LearningGoalResponse)
@limiter.limit("60/minute")
async def get_learning_goals(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No active study plan")
    goal = await _get_or_create_learning_goal(db, current_user.id, plan)
    await db.commit()
    await db.refresh(goal)
    return await _learning_goal_response(db, current_user.id, plan, goal)


@router.put("/goals", response_model=LearningGoalResponse)
@limiter.limit("30/minute")
async def update_learning_goals(
    request: Request,
    data: LearningGoalUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No active study plan")
    goal = await _get_or_create_learning_goal(db, current_user.id, plan)
    goal.daily_xp_target = data.daily_xp_target
    goal.weekly_xp_target = data.weekly_xp_target
    await db.commit()
    await db.refresh(goal)
    return await _learning_goal_response(db, current_user.id, plan, goal)


@router.get("/goals/milestones/summary", response_model=LearningGoalMilestoneSummary)
@limiter.limit("60/minute")
async def get_learning_goal_milestone_summary(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return LearningGoalMilestoneSummary()

    result = await db.execute(
        select(LearningGoalMilestone).where(
            LearningGoalMilestone.user_id == current_user.id,
            LearningGoalMilestone.study_plan_id == plan.id,
        )
    )
    rows = result.scalars().all()
    daily = [row for row in rows if row.goal_type == "daily"]
    weekly = [row for row in rows if row.goal_type == "weekly"]
    return LearningGoalMilestoneSummary(
        total_milestones=len(rows),
        daily_milestones=len(daily),
        weekly_milestones=len(weekly),
        total_reward_xp=sum(row.reward_xp for row in rows),
        daily_reward_xp=sum(row.reward_xp for row in daily),
        weekly_reward_xp=sum(row.reward_xp for row in weekly),
    )


@router.get("/goals/history", response_model=list[LearningGoalMilestoneResponse])
@limiter.limit("60/minute")
async def get_learning_goal_history(
    request: Request,
    limit: int = Query(default=30, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No active study plan")

    result = await db.execute(
        select(LearningGoalMilestone)
        .where(
            LearningGoalMilestone.user_id == current_user.id,
            LearningGoalMilestone.study_plan_id == plan.id,
        )
        .order_by(LearningGoalMilestone.period_start.desc(), LearningGoalMilestone.id.desc())
        .limit(limit)
    )
    return result.scalars().all()


def _server_game_questions(\n    game_id: str,\n    language: str,\n    difficulty: int,\n    target_language: str = "en-GB",\n    cefr_level: CEFRLevel = "A1",\n) -> list[dict]:
    rng = random.SystemRandom()
    hints = {
        "ar": "فكّر بهدوء قبل اختيار الإجابة.",
        "fr": "Réfléchis avant de choisir.",
        "en": "Think carefully before choosing.",
        "es": "Piensa con calma antes de elegir.",
        "de": "Denke in Ruhe nach, bevor du wählst.",
        "it": "Rifletti con calma prima di scegliere.",
        "pt": "Pensa com calma antes de escolher.",
        "ja": "落ち着いて答えを選びましょう。",
        "ko": "천천히 생각한 후 답을 선택하세요.",
        "zh": "请仔细思考后再选择答案。",
    }
    questions: list[dict] = []
    word_entries: list[object] | None = None
    if game_id == "words":
        level = cast(CEFRLevel, {1: "A1", 2: "A2", 3: "B1"}[difficulty])
        vocab_sets = get_vocabulary_by_level(level, target_language)
        entries = [word for vocab_set in vocab_sets for word in vocab_set.words]
        rng.shuffle(entries)
        word_entries = entries[:5]
        if len(word_entries) < 5:
            fallback = [
                ("hello", "a greeting"),
                ("water", "a liquid people drink"),
                ("school", "a place where people learn"),
                ("book", "a written work"),
                ("friend", "a person you know and like"),
            ]
            word_entries = [
                type("VocabularyFallback", (), {"word": w, "definition": d})()
                for w, d in fallback
            ]

    if game_id in {"quick_choice", "listen_choose", "listening_detective", "spelling", "word_scramble", "fill_blank"}:
        level = cast(CEFRLevel, {1: "A1", 2: "A2", 3: "B1"}[difficulty])
        vocab_sets = get_vocabulary_by_level(level, target_language)
        entries = [word for vocab_set in vocab_sets for word in vocab_set.words]
        rng.shuffle(entries)
        word_entries = entries[:5]
        if len(word_entries) < 5:
            raise HTTPException(status_code=503, detail="Not enough vocabulary content for this game")

    for index in range(5):
        question_id = str(uuid4())
        if game_id == "words":
            assert word_entries is not None
            selected = word_entries
            entry = selected[index]
            correct = entry.definition.strip()
            distractors = list(dict.fromkeys(
                item.definition.strip() for item in selected if item.definition.strip() != correct
            ))[:3]
            choices = [correct, *distractors]
            while len(choices) < 4:
                choices.append(f"{correct} ({len(choices) + 1})")
            rng.shuffle(choices)
            prompt = (
                f"What does '{entry.word}' mean?"
                if language == "en"
                else (f"Que signifie '{entry.word}' ?" if language == "fr"
                      else f"ماذا تعني كلمة «{entry.word}»؟")
            )
            questions.append({
                "id": str(uuid4()),
                "prompt": prompt,
                "choices": choices,
                "answer": correct,
                "hint": (
                    "Choose the definition that best matches the word."
                    if language == "en"
                    else ("Choisis la définition qui correspond au mot."
                          if language == "fr" else "اختر التعريف المطابق للكلمة.")
                ),
                "skill": "vocabulary",
                "difficulty": difficulty,
                "topic": "vocabulary",
                "input_mode": "choice",
            })
            continue
        if game_id == "word_categories":
            category_bank = {
                "en": [
                    ("apple", "Food", ["Food", "Transport", "Clothing", "Weather"]),
                    ("bus", "Transport", ["Food", "Transport", "Clothing", "Weather"]),
                    ("jacket", "Clothing", ["Food", "Transport", "Clothing", "Weather"]),
                    ("rain", "Weather", ["Food", "Transport", "Clothing", "Weather"]),
                    ("teacher", "People", ["People", "Places", "Objects", "Animals"]),
                ],
                "fr": [
                    ("pomme", "Nourriture", ["Nourriture", "Transport", "Vêtements", "Météo"]),
                    ("bus", "Transport", ["Nourriture", "Transport", "Vêtements", "Météo"]),
                    ("veste", "Vêtements", ["Nourriture", "Transport", "Vêtements", "Météo"]),
                    ("pluie", "Météo", ["Nourriture", "Transport", "Vêtements", "Météo"]),
                    ("professeur", "Personnes", ["Personnes", "Lieux", "Objets", "Animaux"]),
                ],
                "ar": [
                    ("تفاحة", "طعام", ["طعام", "مواصلات", "ملابس", "طقس"]),
                    ("حافلة", "مواصلات", ["طعام", "مواصلات", "ملابس", "طقس"]),
                    ("سترة", "ملابس", ["طعام", "مواصلات", "ملابس", "طقس"]),
                    ("مطر", "طقس", ["طعام", "مواصلات", "ملابس", "طقس"]),
                    ("معلّم", "أشخاص", ["أشخاص", "أماكن", "أشياء", "حيوانات"]),
                ],
                "es": [
                    ("manzana", "Comida", ["Comida", "Transporte", "Ropa", "Clima"]),
                    ("autobús", "Transporte", ["Comida", "Transporte", "Ropa", "Clima"]),
                    ("chaqueta", "Ropa", ["Comida", "Transporte", "Ropa", "Clima"]),
                    ("lluvia", "Clima", ["Comida", "Transporte", "Ropa", "Clima"]),
                    ("profesor", "Personas", ["Personas", "Lugares", "Objetos", "Animales"]),
                ],
                "de": [
                    ("Apfel", "Essen", ["Essen", "Transport", "Kleidung", "Wetter"]),
                    ("Bus", "Transport", ["Essen", "Transport", "Kleidung", "Wetter"]),
                    ("Jacke", "Kleidung", ["Essen", "Transport", "Kleidung", "Wetter"]),
                    ("Regen", "Wetter", ["Essen", "Transport", "Kleidung", "Wetter"]),
                    ("Lehrer", "Personen", ["Personen", "Orte", "Gegenstände", "Tiere"]),
                ],
                "it": [
                    ("mela", "Cibo", ["Cibo", "Trasporti", "Abbigliamento", "Meteo"]),
                    ("autobus", "Trasporti", ["Cibo", "Trasporti", "Abbigliamento", "Meteo"]),
                    ("giacca", "Abbigliamento", ["Cibo", "Trasporti", "Abbigliamento", "Meteo"]),
                    ("pioggia", "Meteo", ["Cibo", "Trasporti", "Abbigliamento", "Meteo"]),
                    ("insegnante", "Persone", ["Persone", "Luoghi", "Oggetti", "Animali"]),
                ],
                "pt": [
                    ("maçã", "Comida", ["Comida", "Transporte", "Roupa", "Clima"]),
                    ("autocarro", "Transporte", ["Comida", "Transporte", "Roupa", "Clima"]),
                    ("casaco", "Roupa", ["Comida", "Transporte", "Roupa", "Clima"]),
                    ("chuva", "Clima", ["Comida", "Transporte", "Roupa", "Clima"]),
                    ("professor", "Pessoas", ["Pessoas", "Lugares", "Objetos", "Animais"]),
                ],
                "ja": [
                    ("りんご", "食べ物", ["食べ物", "乗り物", "服", "天気"]),
                    ("バス", "乗り物", ["食べ物", "乗り物", "服", "天気"]),
                    ("ジャケット", "服", ["食べ物", "乗り物", "服", "天気"]),
                    ("雨", "天気", ["食べ物", "乗り物", "服", "天気"]),
                    ("先生", "人", ["人", "場所", "物", "動物"]),
                ],
                "ko": [
                    ("사과", "음식", ["음식", "교통", "옷", "날씨"]),
                    ("버스", "교통", ["음식", "교통", "옷", "날씨"]),
                    ("재킷", "옷", ["음식", "교통", "옷", "날씨"]),
                    ("비", "날씨", ["음식", "교통", "옷", "날씨"]),
                    ("선생님", "사람", ["사람", "장소", "물건", "동물"]),
                ],
                "zh": [
                    ("苹果", "食物", ["食物", "交通", "衣服", "天气"]),
                    ("公交车", "交通", ["食物", "交通", "衣服", "天气"]),
                    ("夹克", "衣服", ["食物", "交通", "衣服", "天气"]),
                    ("雨", "天气", ["食物", "交通", "衣服", "天气"]),
                    ("老师", "人物", ["人物", "地点", "物品", "动物"]),
                ],
            }[language]
            word, answer, choices = category_bank[index]
            rng.shuffle(choices)
            questions.append({
                "id": question_id,
                "prompt": (
                    f"Which category does '{word}' belong to?"
                    if language == "en"
                    else (f"À quelle catégorie appartient « {word} » ?"
                          if language == "fr" else f"إلى أي فئة تنتمي كلمة «{word}»؟")
                ),
                "choices": choices,
                "answer": answer,
                "hint": (
                    "Think about what the word represents."
                    if language == "en"
                    else ("Pense à ce que le mot représente."
                          if language == "fr" else "فكّر في الشيء الذي تعبّر عنه الكلمة.")
                ),
                "skill": "vocabulary",
                "difficulty": difficulty,
                "topic": "semantic-categories",
                "input_mode": "choice",
            })
            continue
        if game_id == "context_quest":
            scenarios = {
                "en": [
                    ("You are at a café. The waiter asks: 'What would you like?'", "I'd like a coffee, please.", ["I'd like a coffee, please.", "Yesterday was sunny.", "My brother is tall.", "I studied French."]),
                    ("You meet someone for the first time. What is a natural response to 'Nice to meet you?'", "Nice to meet you too.", ["Nice to meet you too.", "Turn left at the bank.", "I need a ticket.", "It is three o'clock."]),
                    ("You did not hear someone clearly. What should you say?", "Could you say that again, please?", ["Could you say that again, please?", "I am twenty years old.", "The train is blue.", "I bought two books."]),
                    ("You want to ask for directions politely. Which sentence fits?", "Could you tell me how to get to the station?", ["Could you tell me how to get to the station?", "I usually wake up at seven.", "This soup is delicious.", "She has two sisters."]),
                    ("A friend invites you to dinner, but you cannot go. What is a polite reply?", "Thanks for inviting me, but I can't make it.", ["Thanks for inviting me, but I can't make it.", "Where is the nearest pharmacy?", "I am reading a novel.", "The lesson starts tomorrow."]),
                ],
                "fr": [
                    ("Au café, le serveur demande : « Qu'est-ce que vous désirez ? »", "Je voudrais un café, s'il vous plaît.", ["Je voudrais un café, s'il vous plaît.", "Il fait beau hier.", "Mon frère est grand.", "J'étudie demain."]),
                    ("Vous rencontrez quelqu'un pour la première fois. Que répondez-vous à « Enchanté(e) » ?", "Enchanté(e), moi aussi.", ["Enchanté(e), moi aussi.", "Tournez à gauche.", "Il est trois heures.", "J'ai deux livres."]),
                    ("Vous n'avez pas bien entendu. Que dites-vous ?", "Pourriez-vous répéter, s'il vous plaît ?", ["Pourriez-vous répéter, s'il vous plaît ?", "Je me lève à sept heures.", "La gare est bleue.", "J'aime ce film."]),
                    ("Vous cherchez la gare. Quelle demande est polie ?", "Pourriez-vous me dire comment aller à la gare ?", ["Pourriez-vous me dire comment aller à la gare ?", "Je lis un roman.", "Il pleut souvent.", "Elle a deux sœurs."]),
                    ("Un ami vous invite à dîner, mais vous ne pouvez pas venir. Que dites-vous ?", "Merci pour l'invitation, mais je ne peux pas venir.", ["Merci pour l'invitation, mais je ne peux pas venir.", "Où est la pharmacie ?", "Je prends le bus.", "Le cours commence demain."]),
                ],
                "ar": [
                    ("أنت في مقهى. يسألك النادل: «ماذا تريد؟» ما الرد الطبيعي؟", "أريد قهوة من فضلك.", ["أريد قهوة من فضلك.", "كان الجو مشمسًا أمس.", "أخي طويل.", "درست الفرنسية."]),
                    ("تلتقي بشخص لأول مرة ويقول: «سعيد بلقائك». ماذا تقول؟", "وأنا سعيد بلقائك أيضًا.", ["وأنا سعيد بلقائك أيضًا.", "انعطف يسارًا.", "الساعة الثالثة.", "لدي كتابان."]),
                    ("لم تسمع الشخص جيدًا. ماذا تقول بأدب؟", "هل يمكنك أن تعيد ما قلت من فضلك؟", ["هل يمكنك أن تعيد ما قلت من فضلك؟", "أستيقظ في السابعة.", "القطار أزرق.", "اشتريت كتابين."]),
                    ("تريد السؤال عن الاتجاهات بأدب. ماذا تقول؟", "هل يمكنك أن تخبرني كيف أصل إلى المحطة؟", ["هل يمكنك أن تخبرني كيف أصل إلى المحطة؟", "أقرأ رواية.", "الجو بارد.", "لدي أختان."]),
                    ("دعاك صديق إلى العشاء ولا تستطيع الذهاب. ما الرد المناسب؟", "شكرًا على الدعوة، لكن لا أستطيع الحضور.", ["شكرًا على الدعوة، لكن لا أستطيع الحضور.", "أين أقرب صيدلية؟", "أركب الحافلة.", "يبدأ الدرس غدًا."]),
                ],
                "es": [
                    ("Estás en un café. El camarero pregunta: «¿Qué quieres?».", "Quisiera un café, por favor.", ["Quisiera un café, por favor.", "Ayer hizo sol.", "Mi hermano es alto.", "Estudié francés."]),
                    ("Conoces a alguien por primera vez. ¿Qué respondes a «Mucho gusto»?", "Mucho gusto también.", ["Mucho gusto también.", "Gira a la izquierda.", "Son las tres.", "Tengo dos libros."]),
                    ("No has oído bien. ¿Qué dices educadamente?", "¿Podrías repetirlo, por favor?", ["¿Podrías repetirlo, por favor?", "Me levanto a las siete.", "El tren es azul.", "Compré dos libros."]),
                    ("Quieres pedir indicaciones con educación. ¿Qué dices?", "¿Podrías decirme cómo llegar a la estación?", ["¿Podrías decirme cómo llegar a la estación?", "Leo una novela.", "Llueve a menudo.", "Tengo dos hermanas."]),
                    ("Un amigo te invita a cenar, pero no puedes ir. ¿Qué respondes?", "Gracias por la invitación, pero no puedo ir.", ["Gracias por la invitación, pero no puedo ir.", "¿Dónde está la farmacia?", "Tomo el autobús.", "La clase empieza mañana."]),
                ],
                "de": [
                    ("Du bist in einem Café. Der Kellner fragt: „Was möchten Sie?“", "Ich möchte bitte einen Kaffee.", ["Ich möchte bitte einen Kaffee.", "Gestern war es sonnig.", "Mein Bruder ist groß.", "Ich habe Französisch gelernt."]),
                    ("Du triffst jemanden zum ersten Mal. Was antwortest du auf „Freut mich“?", "Mich freut es auch.", ["Mich freut es auch.", "Biegen Sie links ab.", "Es ist drei Uhr.", "Ich habe zwei Bücher."]),
                    ("Du hast jemanden nicht gut verstanden. Was sagst du höflich?", "Könnten Sie das bitte wiederholen?", ["Könnten Sie das bitte wiederholen?", "Ich stehe um sieben auf.", "Der Zug ist blau.", "Ich habe zwei Bücher gekauft."]),
                    ("Du möchtest höflich nach dem Weg fragen. Was sagst du?", "Könnten Sie mir sagen, wie ich zum Bahnhof komme?", ["Könnten Sie mir sagen, wie ich zum Bahnhof komme?", "Ich lese einen Roman.", "Es regnet oft.", "Sie hat zwei Schwestern."]),
                    ("Ein Freund lädt dich zum Essen ein, aber du kannst nicht. Was sagst du?", "Danke für die Einladung, aber ich kann nicht kommen.", ["Danke für die Einladung, aber ich kann nicht kommen.", "Wo ist die nächste Apotheke?", "Ich nehme den Bus.", "Der Kurs beginnt morgen."]),
                ],
                "it": [
                    ("Sei al bar. Il cameriere chiede: «Cosa desidera?»", "Vorrei un caffè, per favore.", ["Vorrei un caffè, per favore.", "Ieri c'era il sole.", "Mio fratello è alto.", "Ho studiato francese."]),
                    ("Incontri qualcuno per la prima volta. Cosa rispondi a «Piacere»?", "Piacere anche a te.", ["Piacere anche a te.", "Gira a sinistra.", "Sono le tre.", "Ho due libri."]),
                    ("Non hai sentito bene. Cosa dici educatamente?", "Potresti ripetere, per favore?", ["Potresti ripetere, per favore?", "Mi alzo alle sette.", "Il treno è blu.", "Ho comprato due libri."]),
                    ("Vuoi chiedere indicazioni con educazione. Cosa dici?", "Potresti dirmi come arrivare alla stazione?", ["Potresti dirmi come arrivare alla stazione?", "Leggo un romanzo.", "Piove spesso.", "Ha due sorelle."]),
                    ("Un amico ti invita a cena, ma non puoi andare. Cosa rispondi?", "Grazie per l'invito, ma non posso venire.", ["Grazie per l'invito, ma non posso venire.", "Dov'è la farmacia più vicina?", "Prendo l'autobus.", "La lezione inizia domani."]),
                ],
                "pt": [
                    ("Estás num café. O empregado pergunta: «O que deseja?»", "Queria um café, por favor.", ["Queria um café, por favor.", "Ontem esteve sol.", "O meu irmão é alto.", "Estudei francês."]),
                    ("Conheces alguém pela primeira vez. O que respondes a «Muito prazer»?", "Muito prazer também.", ["Muito prazer também.", "Vire à esquerda.", "São três horas.", "Tenho dois livros."]),
                    ("Não ouviste bem. O que dizes educadamente?", "Pode repetir, por favor?", ["Pode repetir, por favor?", "Levanto-me às sete.", "O comboio é azul.", "Comprei dois livros."]),
                    ("Queres pedir indicações educadamente. O que dizes?", "Pode dizer-me como chegar à estação?", ["Pode dizer-me como chegar à estação?", "Leio um romance.", "Chove muitas vezes.", "Ela tem duas irmãs."]),
                    ("Um amigo convida-te para jantar, mas não podes ir. O que respondes?", "Obrigado pelo convite, mas não posso ir.", ["Obrigado pelo convite, mas não posso ir.", "Onde fica a farmácia?", "Apanho o autocarro.", "A aula começa amanhã."]),
                ],
                "ja": [
                    ("カフェで店員に「何になさいますか」と聞かれました。", "コーヒーをお願いします。", ["コーヒーをお願いします。", "昨日は晴れていました。", "兄は背が高いです。", "フランス語を勉強しました。"]),
                    ("初対面の人に「はじめまして」と言われました。", "こちらこそ、はじめまして。", ["こちらこそ、はじめまして。", "左に曲がってください。", "3時です。", "本が2冊あります。"]),
                    ("よく聞こえませんでした。丁寧に何と言いますか。", "もう一度言っていただけますか。", ["もう一度言っていただけますか。", "7時に起きます。", "電車は青いです。", "本を2冊買いました。"]),
                    ("駅への行き方を丁寧に尋ねたいです。", "駅へはどう行けばいいですか。", ["駅へはどう行けばいいですか。", "小説を読みます。", "よく雨が降ります。", "姉妹が2人います。"]),
                    ("友達に夕食に誘われましたが行けません。", "誘ってくれてありがとう。でも行けません。", ["誘ってくれてありがとう。でも行けません。", "一番近い薬局はどこですか。", "バスに乗ります。", "授業は明日始まります。"]),
                ],
                "ko": [
                    ("카페에서 직원이 “무엇을 드릴까요?”라고 물었습니다.", "커피 한 잔 주세요.", ["커피 한 잔 주세요.", "어제는 맑았습니다.", "제 형은 키가 큽니다.", "프랑스어를 공부했습니다."]),
                    ("처음 만난 사람이 “반갑습니다”라고 말했습니다. 어떻게 답할까요?", "저도 반갑습니다.", ["저도 반갑습니다.", "왼쪽으로 가세요.", "세 시입니다.", "책이 두 권 있습니다."]),
                    ("잘 듣지 못했습니다. 정중하게 무엇이라고 말할까요?", "다시 말씀해 주시겠어요?", ["다시 말씀해 주시겠어요?", "일곱 시에 일어납니다.", "기차는 파란색입니다.", "책 두 권을 샀습니다."]),
                    ("정중하게 길을 묻고 싶습니다. 무엇이라고 말할까요?", "역에 어떻게 가는지 알려 주시겠어요?", ["역에 어떻게 가는지 알려 주시겠어요?", "소설을 읽습니다.", "비가 자주 옵니다.", "자매가 두 명 있습니다."]),
                    ("친구가 저녁 식사에 초대했지만 갈 수 없습니다. 어떻게 답할까요?", "초대해 줘서 고마워. 하지만 갈 수 없어.", ["초대해 줘서 고마워. 하지만 갈 수 없어.", "가장 가까운 약국이 어디예요?", "버스를 탑니다.", "수업은 내일 시작합니다."]),
                ],
                "zh": [
                    ("你在咖啡馆，服务员问：“您想要什么？”", "请给我一杯咖啡。", ["请给我一杯咖啡。", "昨天天气晴朗。", "我哥哥很高。", "我学过法语。"]),
                    ("你第一次见到一个人，对方说“很高兴认识你”。你怎么回答？", "我也很高兴认识你。", ["我也很高兴认识你。", "向左转。", "现在三点。", "我有两本书。"]),
                    ("你没有听清楚。礼貌地怎么说？", "请您再说一遍，好吗？", ["请您再说一遍，好吗？", "我七点起床。", "火车是蓝色的。", "我买了两本书。"]),
                    ("你想礼貌地问路。你怎么说？", "请问怎么去车站？", ["请问怎么去车站？", "我正在读小说。", "这里经常下雨。", "她有两个姐妹。"]),
                    ("朋友邀请你吃晚饭，但你不能去。你怎么回答？", "谢谢你的邀请，但是我不能去。", ["谢谢你的邀请，但是我不能去。", "最近的药店在哪里？", "我坐公交车。", "课程明天开始。"]),
                ],
            }[language]
            prompt, answer, choices = scenarios[index]
            rng.shuffle(choices)
            questions.append({
                "id": question_id,
                "prompt": prompt,
                "choices": choices,
                "answer": answer,
                "hint": (
                    "Choose the response that fits the situation naturally."
                    if language == "en"
                    else ("Choisis la réponse qui convient naturellement à la situation."
                          if language == "fr" else "اختر الرد الذي يناسب الموقف بشكل طبيعي.")
                ),
                "skill": "speaking",
                "difficulty": difficulty,
                "topic": "context-and-pragmatics",
                "input_mode": "choice",
            })
            continue
        if game_id == "quick_choice":
            assert word_entries is not None
            entry = word_entries[index]
            correct = entry.word.strip()
            distractors = [item.word.strip() for item in word_entries if item.word.strip() != correct]
            rng.shuffle(distractors)
            choices = [correct, *distractors[:3]]
            rng.shuffle(choices)
            prompt = (
                f"Quick! Which word matches this definition?\n{entry.definition.strip()}"
                if language == "en"
                else (f"Vite ! Quel mot correspond à cette définition ?\n{entry.definition.strip()}"
                      if language == "fr"
                      else f"بسرعة! ما الكلمة التي تطابق هذا التعريف؟\n{entry.definition.strip()}")
            )
            questions.append({
                "id": question_id,
                "prompt": prompt,
                "choices": choices,
                "answer": correct,
                "hint": hints[language],
                "skill": "vocabulary",
                "difficulty": difficulty,
                "topic": "quick-choice",
                "input_mode": "choice",
            })
            continue
        if game_id == "listening_detective":
            assert word_entries is not None
            entry = word_entries[index]
            correct = entry.word.strip()
            distractors = [item.word.strip() for item in word_entries if item.word.strip() != correct]
            rng.shuffle(distractors)
            choices = [correct, *distractors[:3]]
            rng.shuffle(choices)
            audio_text = (
                f"I need to buy {correct} today."
                if language == "en"
                else (f"Je dois acheter {correct} aujourd'hui."
                      if language == "fr" else f"أحتاج إلى شراء {correct} اليوم.")
            )
            questions.append({
                "id": question_id,
                "prompt": (
                    "Listen carefully. Which word is the key detail you heard?"
                    if language == "en"
                    else ("Écoute attentivement. Quel mot est le détail clé que tu as entendu ?"
                          if language == "fr" else "استمع جيدًا. ما الكلمة التي تمثل المعلومة الأساسية التي سمعتها؟")
                ),
                "choices": choices,
                "answer": correct,
                "hint": (
                    "Focus on the key noun in the sentence."
                    if language == "en"
                    else ("Concentre-toi sur le nom important de la phrase."
                          if language == "fr" else "ركّز على الاسم الأساسي في الجملة.")
                ),
                "skill": "listening",
                "difficulty": difficulty,
                "topic": "listening-detail",
                "input_mode": "choice",
                "audio_text": audio_text,
                "audio_language": target_language,
            })
            continue
        if game_id == "listen_choose":
            assert word_entries is not None
            entry = word_entries[index]
            correct = entry.word.strip()
            distractors = [item.word.strip() for item in word_entries if item.word.strip() != correct]
            rng.shuffle(distractors)
            choices = [correct, *distractors[:3]]
            rng.shuffle(choices)
            prompt = (
                "Listen, then choose the word you heard."
                if language == "en"
                else ("Écoute, puis choisis le mot entendu."
                      if language == "fr" else "استمع ثم اختر الكلمة التي سمعتها.")
            )
            questions.append({
                "id": question_id,
                "prompt": prompt,
                "choices": choices,
                "answer": correct,
                "hint": (
                    "Play the audio again if needed."
                    if language == "en"
                    else ("Relance l'audio si nécessaire."
                          if language == "fr" else "أعد تشغيل الصوت إذا احتجت.")
                ),
                "skill": "listening",
                "difficulty": difficulty,
                "topic": "listen-choose",
                "input_mode": "choice",
                "audio_text": correct,
                "audio_language": target_language,
            })
            continue
        if game_id == "word_scramble":
            assert word_entries is not None
            entry = word_entries[index]
            word = entry.word.strip()
            letters = list(word)
            rng.shuffle(letters)
            scrambled = "".join(letters)
            prompt = (
                f"Unscramble the word:\\n{scrambled}"
                if language == "en" else (f"Remets les lettres dans le bon ordre :\\n{scrambled}"
                if language == "fr" else f"رتّب الحروف لتكوين الكلمة:\\n{scrambled}")
            )
            questions.append({
                "id": question_id, "prompt": prompt, "choices": [], "answer": word,
                "hint": entry.definition.strip(), "skill": "vocabulary",
                "difficulty": difficulty, "topic": "word-scramble", "input_mode": "text",
            })
            continue
        if game_id == "fill_blank":
            assert word_entries is not None
            vocab_sets = get_vocabulary_by_level(cefr_level, target_language)
            pool = [entry for vocab_set in vocab_sets for entry in vocab_set.words]
            rng.shuffle(pool)
            cloze_entries = [
                entry
                for entry in pool
                if entry.word.strip()
                and entry.example.strip()
                and entry.word.strip().casefold() in entry.example.casefold()
            ][:5]
            if len(cloze_entries) < 5:
                raise HTTPException(
                    status_code=503,
                    detail=f"Not enough CEFR cloze content for {target_language} at {cefr_level}",
                )
            entry = cloze_entries[index]
            example = entry.example.strip()
            word = entry.word.strip()
            marker_index = example.casefold().find(word.casefold())
            if marker_index < 0:
                raise HTTPException(status_code=503, detail="CEFR cloze item is malformed")
            sentence = example[:marker_index] + "___" + example[marker_index + len(word):]
            distractors = [
                item.word.strip()
                for item in word_entries
                if item.word.strip().casefold() != word.casefold()
            ]
            rng.shuffle(distractors)
            choices = list(dict.fromkeys([word, *distractors]))[:4]
            if len(choices) < 4:
                raise HTTPException(status_code=503, detail="Not enough cloze distractors")
            rng.shuffle(choices)
            questions.append({
                "id": question_id,
                "prompt": sentence,
                "choices": choices,
                "answer": word,
                "hint": entry.definition.strip() or hints[language],
                "skill": "grammar",
                "difficulty": difficulty,
                "topic": "cefr-cloze",
                "input_mode": "choice",
            })
            continue
        if game_id == "spelling":
            assert word_entries is not None
            entry = word_entries[index]
            prompt = (
                f"Type the word that means:\n{entry.definition.strip()}"
                if language == "en"
                else (f"Écris le mot qui signifie :\n{entry.definition.strip()}"
                      if language == "fr"
                      else f"اكتب الكلمة التي تعني:\n{entry.definition.strip()}")
            )
            questions.append({
                "id": question_id,
                "prompt": prompt,
                "choices": [],
                "answer": entry.word.strip(),
                "hint": (
                    f"Target word: {entry.word.strip()}"
                    if language == "en"
                    else (f"Mot cible : {entry.word.strip()}"
                          if language == "fr" else f"الكلمة المستهدفة: {entry.word.strip()}")
                ),
                "skill": "writing",
                "difficulty": difficulty,
                "topic": "spelling",
                "input_mode": "text",
            })
            continue
        if game_id == "translation_sprint":
            translation_bank = {
                "en": [
                    ("Translate: Hello, how are you?", "Hello, how are you?"),
                    ("Translate: I need some water.", "I need some water."),
                    ("Translate: Where is the train station?", "Where is the train station?"),
                    ("Translate: I studied yesterday.", "I studied yesterday."),
                    ("Translate: Could you help me, please?", "Could you help me, please?"),
                ],
                "ar": [
                    ("ترجم إلى العربية: Hello, how are you?", "مرحبًا، كيف حالك؟"),
                    ("ترجم إلى العربية: I need some water.", "أحتاج إلى بعض الماء."),
                    ("ترجم إلى العربية: Where is the train station?", "أين محطة القطار؟"),
                    ("ترجم إلى العربية: I studied yesterday.", "درست أمس."),
                    ("ترجم إلى العربية: Could you help me, please?", "هل يمكنك مساعدتي من فضلك؟"),
                ],
                "fr": [
                    ("Traduis en français : Hello, how are you?", "Bonjour, comment allez-vous ?"),
                    ("Traduis en français : I need some water.", "J'ai besoin d'eau."),
                    ("Traduis en français : Where is the train station?", "Où est la gare ?"),
                    ("Traduis en français : I studied yesterday.", "J'ai étudié hier."),
                    ("Traduis en français : Could you help me, please?", "Pourriez-vous m'aider, s'il vous plaît ?"),
                ],
                "es": [
                    ("Traduce al español: Hello, how are you?", "Hola, ¿cómo estás?"),
                    ("Traduce al español: I need some water.", "Necesito agua."),
                    ("Traduce al español: Where is the train station?", "¿Dónde está la estación de tren?"),
                    ("Traduce al español: I studied yesterday.", "Estudié ayer."),
                    ("Traduce al español: Could you help me, please?", "¿Podrías ayudarme, por favor?"),
                ],
                "de": [
                    ("Übersetze ins Deutsche: Hello, how are you?", "Hallo, wie geht es dir?"),
                    ("Übersetze ins Deutsche: I need some water.", "Ich brauche etwas Wasser."),
                    ("Übersetze ins Deutsche: Where is the train station?", "Wo ist der Bahnhof?"),
                    ("Übersetze ins Deutsche: I studied yesterday.", "Ich habe gestern gelernt."),
                    ("Übersetze ins Deutsche: Could you help me, please?", "Könnten Sie mir bitte helfen?"),
                ],
                "it": [
                    ("Traduci in italiano: Hello, how are you?", "Ciao, come stai?"),
                    ("Traduci in italiano: I need some water.", "Ho bisogno di acqua."),
                    ("Traduci in italiano: Where is the train station?", "Dov'è la stazione ferroviaria?"),
                    ("Traduci in italiano: I studied yesterday.", "Ho studiato ieri."),
                    ("Traduci in italiano: Could you help me, please?", "Potresti aiutarmi, per favore?"),
                ],
                "pt": [
                    ("Traduz para português: Hello, how are you?", "Olá, como estás?"),
                    ("Traduz para português: I need some water.", "Preciso de água."),
                    ("Traduz para português: Where is the train station?", "Onde fica a estação de comboios?"),
                    ("Traduz para português: I studied yesterday.", "Estudei ontem."),
                    ("Traduz para português: Could you help-me, please?", "Podes ajudar-me, por favor?"),
                ],
                "ja": [
                    ("日本語に訳してください: Hello, how are you?", "こんにちは、お元気ですか？"),
                    ("日本語に訳してください: I need some water.", "水が必要です。"),
                    ("日本語に訳してください: Where is the train station?", "駅はどこですか？"),
                    ("日本語に訳してください: I studied yesterday.", "昨日勉強しました。"),
                    ("日本語に訳してください: Could you help me, please?", "手伝っていただけますか？"),
                ],
                "ko": [
                    ("한국어로 번역하세요: Hello, how are you?", "안녕하세요, 어떻게 지내세요?"),
                    ("한국어로 번역하세요: I need some water.", "물이 좀 필요해요."),
                    ("한국어로 번역하세요: Where is the train station?", "기차역이 어디예요?"),
                    ("한국어로 번역하세요: I studied yesterday.", "어제 공부했어요."),
                    ("한국어로 번역하세요: Could you help me, please?", "도와주시겠어요?"),
                ],
                "zh": [
                    ("翻译成中文：Hello, how are you?", "你好，你怎么样？"),
                    ("翻译成中文：I need some water.", "我需要一些水。"),
                    ("翻译成中文：Where is the train station?", "火车站在哪里？"),
                    ("翻译成中文：I studied yesterday.", "我昨天学习了。"),
                    ("翻译成中文：Could you help me, please?", "你能帮我吗？"),
                ],
                "pl": [
                    ("Przetłumacz na polski: Hello, how are you?", "Cześć, jak się masz?"),
                    ("Przetłumacz na polski: I need some water.", "Potrzebuję trochę wody."),
                    ("Przetłumacz na polski: Where is the train station?", "Gdzie jest dworzec kolejowy?"),
                    ("Przetłumacz na polski: I studied yesterday.", "Uczyłem się wczoraj."),
                    ("Przetłumacz na polski: Could you help me, please?", "Czy możesz mi pomóc?"),
                ],
                "nl": [
                    ("Vertaal naar het Nederlands: Hello, how are you?", "Hallo, hoe gaat het met je?"),
                    ("Vertaal naar het Nederlands: I need some water.", "Ik heb wat water nodig."),
                    ("Vertaal naar het Nederlands: Where is the train station?", "Waar is het treinstation?"),
                    ("Vertaal naar het Nederlands: I studied yesterday.", "Ik heb gisteren gestudeerd."),
                    ("Vertaal naar het Nederlands: Could you help me, please?", "Kun je me alsjeblieft helpen?"),
                ],
                "ro": [
                    ("Tradu în română: Hello, how are you?", "Bună, ce mai faci?"),
                    ("Tradu în română: I need some water.", "Am nevoie de apă."),
                    ("Tradu în română: Where is the train station?", "Unde este gara?"),
                    ("Tradu în română: I studied yesterday.", "Am studiat ieri."),
                    ("Tradu în română: Could you help me, please?", "Mă poți ajuta, te rog?"),
                ],
                "ru": [
                    ("Переведи на русский: Hello, how are you?", "Привет, как ты?"),
                    ("Переведи на русский: I need some water.", "Мне нужна вода."),
                    ("Переведи на русский: Where is the train station?", "Где находится железнодорожный вокзал?"),
                    ("Переведи на русский: I studied yesterday.", "Я учился вчера."),
                    ("Переведи на русский: Could you help me, please?", "Не могли бы вы мне помочь?"),
                ],
            }
            prompt, answer = translation_bank.get(language, translation_bank["en"])[index]
            questions.append({
                "id": question_id,
                "prompt": prompt,
                "choices": [],
                "answer": answer,
                "hint": hints.get(language, hints["en"]),
                "skill": "writing",
                "difficulty": difficulty,
                "topic": "translation",
                "input_mode": "text",
            })
            continue
        if game_id == "grammar_duel":
            topics = [
                topic
                for topic in get_grammar_topics(target_language)
                if topic.level == cefr_level
            ]
            mistakes = [
                (mistake, topic)
                for topic in topics
                for mistake in topic.common_mistakes
                if mistake.correct.strip() and mistake.wrong.strip()
            ]
            rng.shuffle(mistakes)
            selected_mistakes = mistakes[:5]

            if len(selected_mistakes) >= 5:
                mistake, topic = selected_mistakes[index]
                correct = mistake.correct.strip()
                wrong = mistake.wrong.strip()
                alternatives = [
                    item.correct.strip()
                    for item, _ in mistakes
                    if item.correct.strip() not in {correct, wrong}
                ]
                rng.shuffle(alternatives)
                choices = list(dict.fromkeys([correct, wrong, *alternatives]))[:4]
                if len(choices) < 4:
                    raise HTTPException(status_code=503, detail="Not enough grammar distractors")
                rng.shuffle(choices)
                prompt = (
                    f"Choose the correct form:\n{wrong}"
                    if language == "en"
                    else f"{hints.get(language, hints['en'])}\n{wrong}"
                )
                hint = mistake.note.strip() or hints.get(language, hints["en"])
                topic_slug = topic.slug
            else:
                examples = [
                    example
                    for topic in topics
                    for example in topic.examples
                    if example.text.strip()
                ]
                rng.shuffle(examples)
                if len(examples) < 5:
                    raise HTTPException(
                        status_code=503,
                        detail=f"Not enough CEFR grammar content for {target_language} at {cefr_level}",
                    )
                example = examples[index]
                correct = example.text.strip()
                alternatives = [item.text.strip() for item in examples if item.text.strip() != correct]
                rng.shuffle(alternatives)
                choices = list(dict.fromkeys([correct, *alternatives]))[:4]
                if len(choices) < 4:
                    raise HTTPException(status_code=503, detail="Not enough grammar example distractors")
                rng.shuffle(choices)
                prompt = "Which sentence is correct?"
                hint = example.note.strip() if example.note else hints.get(language, hints["en"])
                topic_slug = "grammar-example"

            questions.append({
                "id": question_id,
                "prompt": prompt,
                "choices": choices,
                "answer": correct,
                "hint": hint,
                "skill": "grammar",
                "difficulty": difficulty,
                "topic": topic_slug,
                "input_mode": "choice",
            })
            continue
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
            choices, prompt = alternatives, f"Remember this order:\n{answer}"
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
                      else f"رتّب الأرقام من الأصغر إلى الأكبر: {' · '.join(map(str, scrambled))}"))
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
async def _get_adaptive_game_difficulty(
    db: AsyncSession,
    user_id: int,
    plan_id: int,
    game_id: str,
    requested_difficulty: int,
) -> tuple[int, str]:
    """Adjust game difficulty from recent server-recorded performance."""
    result = await db.execute(
        select(GameProgressEvent)
        .where(
            GameProgressEvent.user_id == user_id,
            GameProgressEvent.study_plan_id == plan_id,
            GameProgressEvent.game_id == game_id,
        )
        .order_by(GameProgressEvent.created_at.desc())
        .limit(5)
    )
    recent = result.scalars().all()
    if not recent:
        return requested_difficulty, "new"

    scores = [
        event.correct_answers / max(1, event.questions_answered)
        for event in recent
    ]
    average = sum(scores) / len(scores)
    if average < 0.5:
        return max(1, requested_difficulty - 1), "review"
    if average >= 0.85:
        return min(3, requested_difficulty + 1), "challenge"
    return requested_difficulty, "steady"


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
    effective_game_id = data.game_id
    if data.game_id == "word_match":
        effective_game_id = "matching"
    effective_difficulty, adaptive_mode = await _get_adaptive_game_difficulty(
        db, current_user.id, plan.id, effective_game_id, data.difficulty
    )
    if effective_game_id in {"memory", "matching", "ordering", "sentence_builder"}:
        interaction_public, interaction_solution = _server_interactive_challenge(
            effective_game_id, data.language, effective_difficulty
        )
        questions = [{
            "id": str(uuid4()),
            "prompt": interaction_public["type"],
            "choices": [],
            "answer": "",
            "hint": "",
            "skill": GAME_SKILL_MAP[data.game_id],
            "difficulty": effective_difficulty,
            "interaction": {"public": interaction_public, "solution": interaction_solution},
        }]
    else:
        questions = _server_game_questions(\n            effective_game_id,\n            data.language,\n            effective_difficulty,\n            plan.target_language,\n            cast(CEFRLevel, plan.cefr_level),\n        )
    daily_challenge_date = now.date().isoformat() if effective_game_id == _daily_game_id(now.date()) else ""
    session = GameSession(
        id=session_id,
        user_id=current_user.id,
        study_plan_id=plan.id,
        game_id=effective_game_id,
        language=data.language,
        difficulty=effective_difficulty,
        questions=questions,
        started_at=now,
        expires_at=expires_at,
        daily_challenge_date=daily_challenge_date,
        completed=False,
    )
    db.add(session)
    await db.commit()
    public_questions = [
        {
            key: item.get(key)
            for key in ("id", "prompt", "choices", "hint", "skill", "difficulty", "input_mode", "audio_text", "audio_language")
        }
        for item in questions
    ]
    return GameSessionResponse(
        session_id=session_id,
        game_id=data.game_id,
        questions=public_questions,
        expires_at=expires_at.isoformat(),
        daily_challenge=bool(daily_challenge_date),
        daily_challenge_date=daily_challenge_date,
        interaction=questions[0].get("interaction", {}).get("public")
        if effective_game_id in {"memory", "matching", "ordering", "sentence_builder"} else None,
        adaptive_mode=adaptive_mode,
        effective_difficulty=effective_difficulty,
    )


@router.post("/game-session/complete", response_model=GameSessionResultResponse)
@limiter.limit("30/minute")
async def complete_game_session(
    request: Request,
    data: GameSessionComplete,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Verify a server-issued round and persist only server-derived results."""
    # Resolve the opaque session and verify ownership before looking up the
    # caller's active plan. This keeps cross-user attempts deterministic even when
    # the attacker has no active study plan of their own.
    user_id = current_user.id
    session = await db.get(GameSession, data.session_id)
    if session is None or session.user_id != user_id:
        raise HTTPException(status_code=404, detail="Game session not found")

    plan = await _get_active_plan_or_none(db, user_id)
    if plan is None or session.study_plan_id != plan.id:
        raise HTTPException(status_code=404, detail="Game session not found")

    # Capture scalar ownership keys before any rollback. Async SQLAlchemy expires
    # ORM attributes on rollback, so these values must be retained as plain scalars.
    plan_id = plan.id
    if session.completed:
        raise HTTPException(status_code=409, detail="Game session already completed")
    now = datetime.now(UTC).replace(tzinfo=None)
    if now > session.expires_at:
        raise HTTPException(status_code=410, detail="Game session expired")
    if data.daily_challenge:
        today = date.today()
        if data.daily_challenge_date != today.isoformat():
            raise HTTPException(status_code=422, detail="daily_challenge_date must be today")
        if session.daily_challenge_date != today.isoformat():
            raise HTTPException(status_code=422, detail="session is not today's daily challenge")

    if session.game_id in {"memory", "matching", "ordering", "sentence_builder"}:
        if data.answers:
            raise HTTPException(
                status_code=422,
                detail="Interactive games accept interaction_trace instead of answers",
            )
        if len(data.interaction_trace) > 100:
            raise HTTPException(status_code=422, detail="Too many interaction attempts")
        stored = session.questions[0].get("interaction", {})
        solution = stored.get("solution", {})
        if session.game_id == "memory":
            pairs = solution.get("pairs", {})
            seen_pairs: set[int] = set()
            correct_answers = 0
            for attempt in data.interaction_trace:
                first, second = attempt.get("first"), attempt.get("second")
                if not isinstance(first, str) or not isinstance(second, str) or first == second:
                    raise HTTPException(status_code=422, detail="Invalid memory interaction")
                if first not in pairs or second not in pairs:
                    raise HTTPException(status_code=422, detail="Unknown memory card")
                if pairs[first] == pairs[second]:
                    pair_id = pairs[first]
                    if pair_id not in seen_pairs:
                        seen_pairs.add(pair_id)
                        correct_answers += 1
            # Attempts are interaction telemetry, not question count. Keep the
            # scored question total fixed to the server-issued challenge size so
            # clients cannot inflate XP by submitting many incorrect attempts.
            questions_answered = solution.get("pair_count", 0)
            if correct_answers != questions_answered or len(seen_pairs) != questions_answered:
                raise HTTPException(status_code=422, detail="Memory challenge is not complete")
        elif session.game_id == "matching":
            pairs = solution.get("pairs", {})
            matched: set[str] = set()
            correct_answers = 0
            for attempt in data.interaction_trace:
                left_id, right_id = attempt.get("left"), attempt.get("right")
                if not isinstance(left_id, str) or not isinstance(right_id, str):
                    raise HTTPException(status_code=422, detail="Invalid matching interaction")
                if left_id not in pairs or right_id not in pairs.values():
                    raise HTTPException(status_code=422, detail="Unknown matching item")
                if pairs.get(left_id) == right_id and left_id not in matched:
                    matched.add(left_id)
                    correct_answers += 1
            # Score the fixed server-issued pair count rather than the
            # number of client-submitted attempts, preventing XP inflation.
            questions_answered = solution.get("pair_count", 0)
            if correct_answers != questions_answered:
                raise HTTPException(status_code=422, detail="Matching challenge is not complete")
        else:
            items = {item["id"] for item in stored.get("public", {}).get("items", [])}
            target = solution.get("target", [])
            attempts = []
            for attempt in data.interaction_trace:
                sequence = attempt.get("order")
                if not isinstance(sequence, list) or not sequence or any(
                    not isinstance(item, str) or item not in items for item in sequence
                ) or len(sequence) != len(set(sequence)) or len(sequence) != len(items):
                    raise HTTPException(status_code=422, detail="Invalid ordering interaction")
                attempts.append(sequence)
            # Ordering is one scored question regardless of how many
            # intermediate reorder attempts the client submits.
            questions_answered = 1
            correct_answers = 1 if attempts and attempts[-1] == target else 0
            if correct_answers != 1:
                raise HTTPException(status_code=422, detail="Ordering challenge is not complete")
    else:
        expected = {item["id"]: item for item in session.questions}
        if len(data.answers) != len(expected) or set(item.question_id for item in data.answers) != set(expected):
            raise HTTPException(status_code=422, detail="Exactly one answer is required for every question")

        correct_answers = 0
        for submitted in data.answers:
            question = expected[submitted.question_id]
            if question.get("input_mode", "choice") == "text":
                if not submitted.choice.strip():
                    raise HTTPException(status_code=422, detail="Text answer cannot be empty")
                if _game_answer_matches(submitted.choice, question["answer"]):
                    correct_answers += 1
            else:
                if submitted.choice == "__timeout__":
                    continue
                if submitted.choice not in question["choices"]:
                    raise HTTPException(status_code=422, detail="Invalid choice for game question")
                if submitted.choice == question["answer"]:
                    correct_answers += 1
        questions_answered = len(expected)
    # Validation above is read-only. Start the write phase with a database lock
    # so the GameProgress counters, achievements, and XP thresholds are calculated
    # from one serialized state.
    await db.rollback()
    if db.bind is not None and db.bind.dialect.name == "sqlite":
        # SQLite has no row-level SELECT ... FOR UPDATE. BEGIN IMMEDIATE acquires
        # the single-writer reservation before we re-read the aggregate.
        await db.execute(text("BEGIN IMMEDIATE"))
    else:
        # PostgreSQL row locking is scoped to the stable row created at session start.
        locked_progress = await db.execute(
            select(GameProgress)
            .where(
                GameProgress.user_id == user_id,
                GameProgress.study_plan_id == plan_id,
            )
            .with_for_update()
        )
        locked_progress.scalar_one_or_none()

    # Re-read the session after acquiring the write lock. A competing completion
    # may have claimed it while the validation phase was running.
    session = await db.get(GameSession, data.session_id)
    if session is None or session.user_id != user_id or session.study_plan_id != plan_id:
        raise HTTPException(status_code=404, detail="Game session not found")
    if session.completed:
        raise HTTPException(status_code=409, detail="Game session already completed")
    # The first expiry check happens before the write lock. Re-check after
    # acquiring the lock because a request can wait long enough for the
    # server-issued session to expire while another transaction is finishing.
    now = datetime.now(UTC).replace(tzinfo=None)
    if now > session.expires_at:
        raise HTTPException(status_code=410, detail="Game session expired")

    claim = await db.execute(
        update(GameSession)
        .where(
            GameSession.id == session.id,
            GameSession.user_id == user_id,
            GameSession.study_plan_id == plan_id,
            GameSession.completed.is_(False),
        )
        .values(completed=True)
    )
    if claim.rowcount != 1:
        raise HTTPException(status_code=409, detail="Game session already completed")

    round_score = round((correct_answers / questions_answered) * 25)
    # The session ID is the durable idempotency key for this game result.
    # Reusing it prevents the aggregate and event ledger from ever representing
    # the same server-issued session as two different progress events.
    event_id = session.id
    base_xp = correct_answers * 5 + (questions_answered - correct_answers)
    total_before_result = await db.execute(
        select(Progress.xp_earned).where(
            Progress.user_id == user_id,
            Progress.study_plan_id == plan_id,
        )
    )
    total_xp_before = sum(total_before_result.scalars().all())

    existing = await db.execute(
        select(GameProgress).where(
            GameProgress.user_id == user_id,
            GameProgress.study_plan_id == plan_id,
        )
    )
    entry = existing.scalar_one_or_none()
    if entry is None:
        # Completion is the first point at which the aggregate is persisted.
        # A savepoint isolates a first-writer unique conflict on PostgreSQL;
        # SQLite is already serialized by BEGIN IMMEDIATE.
        try:
            async with db.begin_nested():
                entry = GameProgress(
                    user_id=user_id,
                    study_plan_id=plan_id,
                    achievements=[],
                )
                db.add(entry)
                await db.flush()
        except IntegrityError:
            refreshed = await db.execute(
                select(GameProgress).where(
                    GameProgress.user_id == user_id,
                    GameProgress.study_plan_id == plan_id,
                )
            )
            entry = refreshed.scalar_one_or_none()
        if entry is None:
            raise HTTPException(status_code=409, detail="Game progress row is missing")

    entry.games_played += 1
    entry.questions_answered += questions_answered
    entry.correct_answers += correct_answers
    entry.best_round_score = max(entry.best_round_score, round_score)
    if data.daily_challenge:
        if entry.last_daily_challenge_date != data.daily_challenge_date:
            entry.daily_challenges_completed += 1
            entry.last_daily_challenge_date = data.daily_challenge_date

    if correct_answers == questions_answered:
        entry.current_correct_streak += correct_answers
        entry.best_correct_streak = max(entry.best_correct_streak, entry.current_correct_streak)
    else:
        entry.current_correct_streak = 0

    candidates = []
    if entry.games_played == 1:
        candidates.append("first_game")
    if correct_answers == questions_answered:
        candidates.append("perfect_round")
    if entry.best_correct_streak >= 5:
        candidates.append("streak_5")
    if data.daily_challenge:
        candidates.append("daily_challenge")

    current_skill = GAME_SKILL_MAP[session.game_id]
    current_skill_score = correct_answers / questions_answered
    plan = await db.get(StudyPlan, plan_id)
    if plan is None:
        raise HTTPException(status_code=409, detail="Study plan no longer exists")
    skills = await _get_game_skills(db, user_id, plan)
    projected_skills = dict(skills)
    current_skill_before = float(projected_skills.get(current_skill, current_skill_score))
    projected_skills[current_skill] = round(
        current_skill_before * 0.7 + current_skill_score * 0.3, 3
    )
    if sum(1 for score in projected_skills.values() if float(score) > 0) >= 3:
        candidates.append("multi_skill")

    rewards = {
        "first_game": 25, "perfect_round": 50, "streak_5": 40,
        "xp_100": 25, "xp_500": 100, "daily_challenge": 60, "multi_skill": 75,
    }
    existing_achievements = set(entry.achievements or [])
    fresh = [item for item in dict.fromkeys(candidates) if item not in existing_achievements]
    achievement_xp = sum(rewards[item] for item in fresh)
    projected_xp = total_xp_before + base_xp + achievement_xp
    if projected_xp >= 100 and "xp_100" not in existing_achievements:
        fresh.append("xp_100")
        achievement_xp += rewards["xp_100"]
        projected_xp += rewards["xp_100"]
    if projected_xp >= 500 and "xp_500" not in existing_achievements:
        fresh.append("xp_500")
        achievement_xp += rewards["xp_500"]

    entry.achievements = list(dict.fromkeys([*(entry.achievements or []), *fresh]))
    progress_entry = await update_daily_progress(
        db, user_id, study_plan_id=plan_id,
        xp=base_xp + achievement_xp, skill=current_skill,
        skill_score=current_skill_score, commit=False,
    )
    if progress_entry is None:
        raise HTTPException(status_code=500, detail="Unable to persist game XP")

    db.add(GameProgressEvent(
        event_id=event_id, user_id=user_id, study_plan_id=plan_id,
        game_id=session.game_id, questions_answered=questions_answered,
        correct_answers=correct_answers, round_score=round_score,
        daily_challenge=data.daily_challenge, daily_challenge_date=data.daily_challenge_date,
        achievements=fresh, xp_earned=base_xp + achievement_xp,
    ))
    try:
        await db.commit()
    except IntegrityError as exc:
        # The unique event key is a final idempotency guard. If a duplicate
        # completion reaches this point, roll back every aggregate mutation
        # made above and expose a deterministic conflict instead of a 500.
        await db.rollback()
        raise HTTPException(status_code=409, detail="Game completion already recorded") from exc
    # Refresh the authenticated user after commit so this endpoint remains safe
    # with production async_sessionmaker(expire_on_commit=True).
    await db.refresh(current_user)
    summary = await get_game_summary(request=request, current_user=current_user, db=db)
    return GameSessionResultResponse(
        **summary.model_dump(),
        round_score=round_score,
        round_correct=correct_answers,
        round_questions=questions_answered,
        xp_earned=base_xp + achievement_xp,
        new_achievements=fresh,
    )


@router.post("/game-event", response_model=GameStatsResponse, status_code=410)
@limiter.limit("60/minute")
async def record_game_event(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Legacy endpoint retired; all game writes require a server-issued session."""
    raise HTTPException(
        status_code=410,
        detail="Legacy game events are retired; use /api/progress/game-session",
    )


@router.post("/game-summary", deprecated=True)
@limiter.limit("60/minute")
async def reject_legacy_game_summary(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    raise HTTPException(
        status_code=410,
        detail="Legacy absolute game-summary sync is retired; use /api/progress/game-session/complete instead",
    )


@router.get("/history/summary", response_model=ProgressRangeSummary)
@limiter.limit("60/minute")
async def get_history_summary(
    request: Request,
    range: str = "week",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if range not in {"week", "month", "all"}:
        raise HTTPException(status_code=422, detail="range must be week, month or all")

    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return ProgressRangeSummary(period=range)

    today = date.today()
    start_date = None
    if range == "week":
        start_date = today - timedelta(days=6)
    elif range == "month":
        start_date = today - timedelta(days=29)

    query = select(Progress).where(
        Progress.user_id == current_user.id,
        Progress.study_plan_id == plan.id,
    )
    if start_date is not None:
        query = query.where(Progress.date >= start_date)

    result = await db.execute(query.order_by(Progress.date.asc()))
    entries = result.scalars().all()
    if not entries:
        return ProgressRangeSummary(
            period=range,
            from_date=start_date,
            to_date=today if start_date is not None else None,
        )

    total_xp = sum(entry.xp_earned for entry in entries)
    total_lessons = sum(entry.lessons_completed for entry in entries)
    total_exercises = sum(entry.exercises_total for entry in entries)
    exercises_correct = sum(entry.exercises_correct for entry in entries)
    accuracy = exercises_correct / total_exercises if total_exercises else 0.0

    skill_totals: dict[str, list[float]] = {}
    for entry in entries:
        for skill, score in (entry.skills or {}).items():
            if isinstance(score, (int, float)) and not isinstance(score, bool):
                skill_totals.setdefault(str(skill), []).append(float(score))

    skills = {
        skill: round(sum(scores) / len(scores), 3)
        for skill, scores in sorted(skill_totals.items())
        if scores
    }

    first_date = entries[0].date
    last_date = entries[-1].date
    return ProgressRangeSummary(
        period=range,
        from_date=start_date or first_date,
        to_date=today if start_date is not None else last_date,
        total_xp=total_xp,
        total_lessons=total_lessons,
        total_exercises=total_exercises,
        exercises_correct=exercises_correct,
        accuracy=round(accuracy, 3),
        active_days=len({entry.date for entry in entries}),
        average_daily_xp=round(total_xp / len({entry.date for entry in entries}), 2),
        skills=skills,
    )


@router.get("/history", response_model=ProgressHistoryResponse)
@limiter.limit("60/minute")
async def get_history(
    request: Request,
    range: Literal["week", "month", "all"] = "week",
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return ProgressHistoryResponse(entries=[])

    query = (
        select(Progress)
        .where(
            Progress.user_id == current_user.id,
            Progress.study_plan_id == plan.id,
        )
        .order_by(Progress.date.desc())
    )
    if range == "week":
        query = query.limit(7)
    elif range == "month":
        query = query.limit(30)
    result = await db.execute(query)
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


@router.get("/mastery", response_model=MasteryCenterResponse)
@limiter.limit("60/minute")
async def get_mastery_center(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return a cross-lesson mastery snapshot for the active study plan."""
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return MasteryCenterResponse(mastery_state="unseen")

    lesson_result = await db.execute(
        select(Lesson).where(Lesson.study_plan_id == plan.id).order_by(Lesson.week_number, Lesson.day_number, Lesson.id)
    )
    lessons = lesson_result.scalars().all()
    if not lessons: