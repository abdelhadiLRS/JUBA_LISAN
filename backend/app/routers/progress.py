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
    "review_mix": "vocabulary",
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
    game_id: str,
    language: str,
    difficulty: int,
    target_language: str = "en-GB",
    cefr_level: CEFRLevel = "A1",
    preferred_topics: list[str] | None = None,
    preferred_items: list[dict] | None = None,
) -> tuple[dict, dict]:
    """Build a renderable challenge plus server-only solution state."""
    rng = random.SystemRandom()
    vocab_sets = get_vocabulary_by_level(cefr_level, target_language)
    all_cefr_entries = [entry for vocab_set in vocab_sets for entry in vocab_set.words]
    cefr_entries = list(all_cefr_entries)
    if preferred_topics:
        preferred = set(preferred_topics)
        weak = [entry for vocab_set in vocab_sets if vocab_set.topic in preferred for entry in vocab_set.words]
        broad = [entry for vocab_set in vocab_sets if vocab_set.topic not in preferred for entry in vocab_set.words]
        rng.shuffle(weak)
        rng.shuffle(broad)
        cefr_entries = weak[:3] + broad[:2]
        if len(cefr_entries) < 5:
            cefr_entries.extend(weak[3:5])
        if len(cefr_entries) < 5:
            cefr_entries.extend(broad[2:5])
    else:
        rng.shuffle(cefr_entries)
    if preferred_items:
        exact_entries = []
        by_word = {entry.word.strip().casefold(): entry for entry in all_cefr_entries}
        for item in preferred_items:
            word = str(item.get("word", "")).strip()
            definition = str(item.get("definition", "")).strip()
            sentence = str(item.get("sentence", "")).strip()
            entry = by_word.get(word.casefold()) if word else None
            if entry and definition and entry.word.strip().casefold() == word.casefold():
                exact_entries.append(entry)
                continue
            if sentence:
                exact_entries.extend(
                    entry for entry in all_cefr_entries
                    if entry.example.strip() == sentence
                )
        seen_words = set()
        unique_exact = []
        for entry in exact_entries:
            key = entry.word.strip().casefold()
            if key not in seen_words:
                seen_words.add(key)
                unique_exact.append(entry)
        exact_entries = unique_exact
        cefr_entries = exact_entries + [entry for entry in cefr_entries if entry.word.strip().casefold() not in seen_words]

    if game_id == "memory":
        count = {1: 3, 2: 4, 3: 5}[difficulty]
        selected_entries = cefr_entries[:count]
        if len(selected_entries) < count:
            raise ValueError(f"No vocabulary content for {target_language} at {cefr_level}")
        selected = [(entry.word.strip(), entry.definition.strip()) for entry in selected_entries]
        cards = []
        pairs = {}
        review_items = {}
        for index, (left, right) in enumerate(selected):
            a, b = str(uuid4()), str(uuid4())
            cards.extend([{"id": a, "label": left, "pair_key": str(index)}, {"id": b, "label": right, "pair_key": str(index)}])
            pairs[a] = index
            pairs[b] = index
            topic = next((v.topic for v in vocab_sets if any(w.word.strip() == left for w in v.words)), "vocabulary")
            review_items[str(index)] = {
                "word": left,
                "definition": right,
                "topic": topic,
                "review_key": _review_key({
                    "skill": "memory",
                    "topic": topic,
                    "prompt": left,
                    "answer": right,
                }),
            }
        rng.shuffle(cards)
        return {"type": "memory", "cards": cards}, {"pairs": pairs, "pair_count": count, "review_items": review_items}
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
        review_items = {
            str(index): {
                "word": left_item,
                "definition": right_item,
                "topic": next((v.topic for v in vocab_sets if any(w.word.strip() == left_item for w in v.words)), "vocabulary"),
                "review_key": _review_key({
                    "skill": "vocabulary",
                    "topic": next((v.topic for v in vocab_sets if any(w.word.strip() == left_item for w in v.words)), "vocabulary"),
                    "prompt": left_item,
                    "answer": right_item,
                }),
            }
            for index, (left_item, right_item) in enumerate(pairs_source)
        }
        return {"type": "matching", "left": left, "right": right}, {"pairs": pairs, "pair_count": len(left), "review_items": review_items}
    if game_id in {"ordering", "sentence_builder"}:
        if game_id == "sentence_builder":
            sentence_entries = [entry for entry in cefr_entries if entry.example.strip()]
            if not sentence_entries:
                raise ValueError(f"No example sentences for {target_language} at {cefr_level}")
            source_entry = sentence_entries[0]
            source = source_entry.example.strip().split()

        else:
            count = {1: 3, 2: 4, 3: 5}[difficulty]
            ordered_entries = cefr_entries[:count]
            if len(ordered_entries) < count:
                raise ValueError(f"No vocabulary content for {target_language} at {cefr_level}")
            source = [entry.word.strip() for entry in ordered_entries]
        items = [{"id": str(uuid4()), "label": label} for label in source]
        shuffled = list(items)
        rng.shuffle(shuffled)
        solution = {"target": [item["id"] for item in items]}
        if game_id == "sentence_builder":
            sentence_topic = next((v.topic for v in vocab_sets if source_entry in v.words), "grammar")
            sentence = " ".join(source)
            solution["review_items"] = {
                "sentence": {
                    "sentence": sentence,
                    "topic": sentence_topic,
                    "review_key": _review_key({
                        "skill": "grammar",
                        "topic": sentence_topic,
                        "prompt": sentence,
                        "answer": sentence,
                    }),
                }
            }
        return {"type": "ordering", "items": shuffled}, solution
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


def _prioritize_curriculum_entries(entries: list[tuple[object, str]], preferred_topics: list[str] | None, count: int = 5) -> list[object]:
    """Keep review-focused rounds diverse while prioritizing weak curriculum topics."""
    rng = random.SystemRandom()
    pairs = list(entries)
    rng.shuffle(pairs)
    if not preferred_topics:
        return [entry for entry, _topic in pairs[:count]]
    preferred = set(preferred_topics)
    weak = [(entry, topic) for entry, topic in pairs if topic in preferred]
    broad = [(entry, topic) for entry, topic in pairs if topic not in preferred]
    rng.shuffle(weak)
    rng.shuffle(broad)
    selected = [entry for entry, _topic in weak[:min(3, count)]]
    selected.extend(entry for entry, _topic in broad[:count-len(selected)])
    if len(selected) < count:
        selected.extend(entry for entry, _topic in weak[3:count])
    return selected[:count]


def _server_game_questions(
    game_id: str,
    language: str,
    difficulty: int,
    target_language: str = "en-GB",
    cefr_level: CEFRLevel = "A1",
    preferred_topics: list[str] | None = None,
) -> list[dict]:
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
        level = cefr_level
        vocab_sets = get_vocabulary_by_level(level, target_language)
        entries = [(word, vocab_set.topic) for vocab_set in vocab_sets for word in vocab_set.words]
        word_entries = _prioritize_curriculum_entries(entries, preferred_topics)
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
        level = cefr_level
        vocab_sets = get_vocabulary_by_level(level, target_language)
        entries = [(word, vocab_set.topic) for vocab_set in vocab_sets for word in vocab_set.words]
        word_entries = _prioritize_curriculum_entries(entries, preferred_topics)
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
                "topic": next(topic for candidate, topic in entries if candidate is entry),
                "input_mode": "choice",
            })
            continue
        if game_id == "listening_detective":
            assert word_entries is not None
            entry = word_entries[index]
            alternatives = [
                item.word.strip()
                for item in word_entries
                if item.word.strip().casefold() != entry.word.strip().casefold()
            ]
            rng.shuffle(alternatives)
            choices = list(dict.fromkeys([entry.word.strip(), *alternatives]))[:4]
            if len(choices) < 4:
                raise HTTPException(status_code=503, detail="Not enough listening distractors")
            rng.shuffle(choices)
            question = {
                "id": question_id,
                "prompt": (
                    "Listen and choose the word you hear."
                    if language == "en"
                    else hints.get(language, hints["en"])
                ),
                "choices": choices,
                "answer": entry.word.strip(),
                "hint": entry.definition.strip() or hints.get(language, hints["en"]),
                "skill": "listening",
                "difficulty": difficulty,
                "topic": next(topic for candidate, topic in entries if candidate is entry),
                "input_mode": "choice",
                "audio_text": entry.example.strip(),
                "audio_language": target_language,
                "target_language": target_language,
                "cefr_level": cefr_level,
            }
            questions.append(question)
            continue
        if game_id == "word_categories":
            # Derive categories from the active CEFR vocabulary curriculum.
            vocab_sets = get_vocabulary_by_level(cefr_level, target_language)
            category_entries = [
                (entry, vocab_set.topic)
                for vocab_set in vocab_sets
                for entry in vocab_set.words
                if entry.word.strip()
            ]
            selected_entries = _prioritize_curriculum_entries(category_entries, preferred_topics)
            selected = [(entry, next(topic for candidate, topic in category_entries if candidate is entry)) for entry in selected_entries]
            if len(selected) < 5:
                raise HTTPException(
                    status_code=503,
                    detail=f"Not enough CEFR category content for {target_language} at {cefr_level}",
                )

            topics = list(dict.fromkeys(topic for _, topic in category_entries))
            if len(topics) < 4:
                raise HTTPException(status_code=503, detail="Not enough vocabulary topics for categories")

            entry, answer = selected[index]
            distractors = [topic for topic in topics if topic != answer]
            rng.shuffle(distractors)
            choices = [answer, *distractors[:3]]
            rng.shuffle(choices)
            questions.append({
                "id": question_id,
                "prompt": (
                    f"Which topic does '{entry.word}' belong to?"
                    if language == "en"
                    else f"{hints.get(language, hints['en'])}\n{entry.word}"
                ),
                "choices": choices,
                "answer": answer,
                "hint": entry.definition.strip() or hints.get(language, hints["en"]),
                "skill": "vocabulary",
                "difficulty": difficulty,
                "topic": "cefr-semantic-categories",
                "input_mode": "choice",
            })
            continue
        if game_id == "context_quest":
            # Turn authored CEFR example sentences into situational choices.
            vocab_sets = get_vocabulary_by_level(cefr_level, target_language)
            context_pairs = [(entry, vocab_set.topic) for vocab_set in vocab_sets for entry in vocab_set.words if entry.example.strip()]
            context_entries = _prioritize_curriculum_entries(context_pairs, preferred_topics)
            if len(context_entries) < 5:
                raise HTTPException(
                    status_code=503,
                    detail=f"Not enough CEFR context content for {target_language} at {cefr_level}",
                )

            entry = context_entries[index]
            answer = entry.example.strip()
            alternatives = [
                item.example.strip()
                for item in context_entries
                if item.example.strip() != answer
            ]
            rng.shuffle(alternatives)
            choices = list(dict.fromkeys([answer, *alternatives]))[:4]
            if len(choices) < 4:
                raise HTTPException(status_code=503, detail="Not enough context distractors")
            rng.shuffle(choices)
            questions.append({
                "id": question_id,
                "prompt": (
                    f"Which sentence best uses '{entry.word}'?"
                    if language == "en"
                    else f"{hints.get(language, hints['en'])}\n{entry.word}"
                ),
                "choices": choices,
                "answer": answer,
                "hint": entry.definition.strip() or hints.get(language, hints["en"]),
                "skill": "speaking",
                "difficulty": difficulty,
                "topic": next(topic for candidate, topic in context_pairs if candidate is entry),
                "input_mode": "choice",
            })
            continue
        if game_id == "translation_sprint":
            # Prefer curriculum-authored bilingual grammar examples at the
            # active CEFR level. This keeps translation practice aligned with
            # the same sentences learners encounter in lessons.
            translation_pairs = [(example, topic.slug) for topic in get_grammar_topics(target_language) if topic.level == cefr_level for example in topic.examples if example.text.strip() and example.translation and example.translation.strip()]
            translation_examples = _prioritize_curriculum_entries(translation_pairs, preferred_topics)
            if len(translation_examples) >= 5:
                example = translation_examples[index]
                example_topic = next(topic for candidate, topic in translation_pairs if candidate is example)
                questions.append({
                    "id": question_id,
                    "prompt": f"Translate into the target language:\n{example.translation.strip()}",
                    "choices": [],
                    "answer": example.text.strip(),
                    "hint": hints.get(language, hints["en"]),
                    "skill": "writing",
                    "difficulty": difficulty,
                    "topic": example_topic,
                    "input_mode": "text",
                })
                continue
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
            if preferred_topics:
                preferred = set(preferred_topics)
                topics = sorted(topics, key=lambda topic: (0 if topic.slug in preferred or topic.category in preferred else 1, topic.slug))
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
                example_pairs = [(example, topic.slug) for topic in topics for example in topic.examples if example.text.strip()]
                examples = _prioritize_curriculum_entries(example_pairs, preferred_topics)
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
                topic_slug = next(topic for candidate, topic in example_pairs if candidate is example)

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


async def _get_adaptive_review_topics(db: AsyncSession, user_id: int, plan_id: int, skill: str | None, target_language: str, cefr_level: CEFRLevel) -> list[str]:
    """Rank recurring weak topics while preserving the active language and CEFR."""
    if not skill:
        return []
    mistakes = await _get_recent_game_mistakes(db, user_id, plan_id, limit=100, skill=skill)
    scores: dict[str, float] = {}
    for mistake in mistakes:
        if str(mistake.get("target_language") or target_language) != target_language:
            continue
        if str(mistake.get("cefr_level") or cefr_level) != cefr_level:
            continue
        topic = str(mistake.get("topic", "")).strip()
        if not topic:
            continue
        count = max(0, int(mistake.get("review_count", 0)))
        scores[topic] = scores.get(topic, 0.0) + 1.0 + min(count, 5) * 0.5
    return [topic for topic, _score in sorted(scores.items(), key=lambda item: (-item[1], item[0]))]


def _review_key(question: dict) -> str:
    """Build a stable identity for a missed learning item across game sessions."""
    raw = "|".join(
        str(question.get(key, "")).strip().casefold()
        for key in ("skill", "topic", "prompt", "answer")
    )
    return raw


def _review_interval(review_count: int) -> timedelta:
    """Return a conservative expanding interval for retrieval practice."""
    return (
        timedelta(minutes=10)
        if review_count <= 0
        else timedelta(hours=1)
        if review_count == 1
        else timedelta(days=1)
        if review_count == 2
        else timedelta(days=3)
        if review_count == 3
        else timedelta(days=7)
    )


def _item_mastery_from_events(
    events: list[GameProgressEvent],
    review_key: str,
    skill: str | None = None,
    target_language: str | None = None,
    cefr_level: str | None = None,
) -> dict[str, object]:
    """Derive per-item mastery from the append-only game event ledger."""
    misses = 0
    resolutions = 0
    last_miss_at: datetime | None = None
    last_resolution_at: datetime | None = None

    for event in sorted(events, key=lambda event: event.created_at):
        for item in event.mistakes or []:
            if not isinstance(item, dict) or str(item.get("review_key", "")) != review_key:
                continue
            question = item.get("question")
            if isinstance(question, dict):
                if skill and str(question.get("skill", "")) != skill:
                    continue
                if target_language and str(question.get("target_language", "")) != target_language:
                    continue
                if cefr_level and str(question.get("cefr_level", "")) != cefr_level:
                    continue
            if item.get("resolved"):
                resolutions += 1
                last_resolution_at = event.created_at
            elif isinstance(question, dict):
                misses += 1
                last_miss_at = event.created_at

    if misses == 0 and resolutions == 0:
        return {
            "score": 0.0,
            "state": "new",
            "misses": 0,
            "resolutions": 0,
        }

    # Resolutions raise mastery while repeated misses keep the item weak.
    score = max(
        0.0,
        min(1.0, 0.5 + (resolutions * 0.65 - misses * 0.35) / max(1.0, misses + resolutions)),
    )
    if misses >= 3 and misses > resolutions:
        state = "weak"
    elif resolutions >= 3 and resolutions >= misses:
        state = "mastered"
    elif resolutions > 0 and last_resolution_at and last_miss_at and last_resolution_at >= last_miss_at:
        state = "reviewing"
    elif misses <= 1:
        state = "learning"
    else:
        state = "weak"

    return {
        "score": round(score, 3),
        "state": state,
        "misses": misses,
        "resolutions": resolutions,
        "last_miss_at": last_miss_at.isoformat() if last_miss_at else None,
        "last_resolution_at": last_resolution_at.isoformat() if last_resolution_at else None,
    }


async def _get_recent_game_mistakes(
    db: AsyncSession,
    user_id: int,
    plan_id: int,
    game_id: str | None = None,
    limit: int = 3,
    skill: str | None = None,
) -> list[dict]:
    """Return due missed items, optionally scoped by game or learning skill."""
    query = select(GameProgressEvent).where(
        GameProgressEvent.user_id == user_id,
        GameProgressEvent.study_plan_id == plan_id,
    )
    if game_id:
        query = query.where(GameProgressEvent.game_id == game_id)
    result = await db.execute(
        query
        .order_by(GameProgressEvent.created_at.desc())
        .limit(200)
    )
    events = result.scalars().all()
    resolved: set[str] = set()
    candidates: list[tuple[datetime, dict]] = []
    seen: set[str] = set()
    now = datetime.now(UTC).replace(tzinfo=None)

    for event in events:
        for item in event.mistakes or []:
            if not isinstance(item, dict):
                continue
            key = str(item.get("review_key", ""))
            if not key:
                question = item.get("question")
                if isinstance(question, dict):
                    key = _review_key(question)
            if not key:
                continue
            if item.get("resolved"):
                resolved.add(key)
                continue
            question = item.get("question")
            if (
                not isinstance(question, dict)
                or key in resolved
                or key in seen
                or (skill and str(question.get("skill", "")) != skill)
            ):
                continue
            due_value = item.get("next_review_at")
            try:
                due_at = datetime.fromisoformat(str(due_value)) if due_value else (
                    event.created_at + _review_interval(0)
                )
            except ValueError:
                due_at = event.created_at + _review_interval(0)
            if due_at <= now:
                replay = dict(question)
                replay["review_key"] = key
                replay["review_count"] = int(item.get("review_count", 0))
                replay["review_due_at"] = due_at.isoformat()
                replay["source_game_id"] = event.game_id
                replay["target_language"] = str(
                    question.get("target_language") or item.get("target_language") or ""
                )
                replay["cefr_level"] = str(
                    question.get("cefr_level") or item.get("cefr_level") or ""
                )
                candidates.append((due_at, replay))
                seen.add(key)

    ranked_candidates: list[tuple[float, datetime, dict]] = []
    for due_at, question in candidates:
        mastery = _item_mastery_from_events(
            events,
            str(question.get("review_key", "")),
            skill=skill,
            target_language=str(question.get("target_language") or "") or None,
            cefr_level=str(question.get("cefr_level") or "") or None,
        )
        question["mastery_score"] = float(mastery["score"])
        question["mastery_state"] = str(mastery["state"])
        question["mastery_misses"] = int(mastery["misses"])
        question["mastery_resolutions"] = int(mastery["resolutions"])
        ranked_candidates.append((float(mastery["score"]), due_at, question))
    ranked_candidates.sort(key=lambda item: (item[0], item[1]))
    # Mastered items are intentionally suppressed from normal review when
    # weaker material exists. They can still return when the learner has no
    # other due items, preserving coverage without creating repetitive rounds.
    active = [
        item for item in ranked_candidates
        if str(item[2].get("mastery_state", "")) != "mastered"
    ]
    selected = active[:limit]
    if len(selected) < limit:
        selected.extend(
            item for item in ranked_candidates
            if item not in selected
        )
    return [question for _, _, question in selected[:limit]]


def _apply_smart_review(
    questions: list[dict],
    mistakes: list[dict],
    target_language: str,
    cefr_level: CEFRLevel,
) -> list[dict]:
    """Blend due retrieval items with fresh CEFR questions without exposing answers."""
    if not mistakes or not questions:
        return questions

    eligible: list[dict] = []
    for mistake in mistakes:
        if str(mistake.get("skill", "")) != str(questions[0].get("skill", "")):
            continue
        if str(mistake.get("target_language", target_language)) != target_language:
            continue
        if str(mistake.get("cefr_level", cefr_level)) != cefr_level:
            continue
        eligible.append(mistake)

    if not eligible:
        return questions

    result = list(questions)
    # Keep most of the round fresh while giving retrieval practice a meaningful
    # presence. The stored answer remains server-side in GameSession.questions.
    review_count = min(3, len(eligible), len(result))
    for index, mistake in enumerate(eligible[:review_count]):
        replay = dict(mistake)
        replay["id"] = str(uuid4())
        replay["review"] = True
        replay["target_language"] = target_language
        replay["cefr_level"] = cefr_level
        # Review metadata is server-only; the public projection below omits
        # the authoritative answer and review bookkeeping.
        replay.pop("review_key", None)
        replay.pop("review_count", None)
        replay.pop("review_due_at", None)
        replay.pop("source_game_id", None)
        if replay.get("input_mode", "choice") == "choice":
            # Rebuild distractors from fresh questions while preserving the
            # authoritative answer from the prior mistake.
            answer = str(replay.get("answer", ""))
            distractors = [
                str(question.get("answer", "")).strip()
                for question in result
                if str(question.get("answer", "")).strip()
                and str(question.get("answer", "")).strip() != answer
                and question.get("input_mode", "choice") == "choice"
            ]
            distractors = list(dict.fromkeys(distractors))
            rng = random.SystemRandom()
            rng.shuffle(distractors)
            choices = [answer, *distractors[:3]]
            if len(choices) >= 2:
                rng.shuffle(choices)
                replay["choices"] = choices
        result[index] = replay
    return result


async def _build_multi_skill_review_questions(
    db: AsyncSession,
    user_id: int,
    plan: StudyPlan,
    language: str,
    difficulty: int,
) -> list[dict]:
    """Build one server-owned review round spanning several weak skills."""
    game_for_skill = {
        "vocabulary": "quick_choice",
        "grammar": "grammar_duel",
        "listening": "listening_detective",
        "writing": "translation_sprint",
        "speaking": "context_quest",
    }
    due = await _get_recent_game_mistakes(db, user_id, plan.id, limit=100)
    eligible_due = [
        item
        for item in due
        if str(item.get("skill", "")) in game_for_skill
        and str(item.get("target_language", plan.target_language)) == plan.target_language
        and str(item.get("cefr_level", plan.cefr_level)) == plan.cefr_level
    ]

    # Rank skills by both mastery weakness and due-review pressure. This avoids
    # letting database order decide the composition of a mixed review round.
    skills = await _get_game_skills(db, user_id, plan)
    skill_order = {skill: index for index, skill in enumerate(game_for_skill)}
    due_counts: dict[str, int] = {}
    for item in eligible_due:
        skill = str(item.get("skill", ""))
        due_counts[skill] = due_counts.get(skill, 0) + 1

    ranked_skills = sorted(
        (
            skill
            for skill in game_for_skill
            if skill in due_counts or isinstance(skills.get(skill), (int, float))
        ),
        key=lambda skill: (
            -due_counts.get(skill, 0),
            float(skills.get(skill, 0.0)),
            skill_order[skill],
        ),
    )

    selected: list[dict] = []
    selected_keys: set[str] = set()

    # First pass: guarantee broad coverage of eligible weak skills, preferring
    # due mistakes over fresh questions.
    for skill in ranked_skills:
        if len(selected) >= 5:
            break
        candidates = [item for item in eligible_due if str(item.get("skill", "")) == skill]
        if not candidates:
            continue
        replay = dict(candidates[0])
        replay["id"] = str(uuid4())
        replay["review"] = True
        replay["target_language"] = plan.target_language
        replay["cefr_level"] = plan.cefr_level
        selected.append(replay)
        selected_keys.add(str(replay.get("review_key") or _review_key(replay)))

    # Second pass: use additional due mistakes to fill the remaining slots,
    # still weighted toward skills with the most outstanding review pressure.
    if len(selected) < 5:
        for skill in ranked_skills:
            if len(selected) >= 5:
                break
            candidates = [
                item for item in eligible_due
                if str(item.get("skill", "")) == skill
                and str(item.get("review_key") or _review_key(item)) not in selected_keys
            ]
            for item in candidates:
                if len(selected) >= 5:
                    break
                replay = dict(item)
                replay["id"] = str(uuid4())
                replay["review"] = True
                replay["target_language"] = plan.target_language
                replay["cefr_level"] = plan.cefr_level
                selected.append(replay)
                selected_keys.add(str(replay.get("review_key") or _review_key(replay)))

    # Third pass: fill from the weakest skill records when the due queue is short.
    if len(selected) < 5:
        for skill in ranked_skills:
            if len(selected) >= 5:
                break
            game_id = game_for_skill[skill]
            fresh = _server_game_questions(
                game_id,
                language,
                difficulty,
                plan.target_language,
                cast(CEFRLevel, plan.cefr_level),
            )
            for question in fresh:
                if len(selected) >= 5:
                    break
                if str(question.get("skill", "")) != skill:
                    continue
                selected.append(question)
    if len(selected) < 5:
        # Deterministic fallback for a learner with no stored skill history.
        fresh = _server_game_questions(
            "quick_choice",
            language,
            difficulty,
            plan.target_language,
            cast(CEFRLevel, plan.cefr_level),
        )
        selected.extend(fresh[: 5 - len(selected)])
    return selected[:5]


async def _get_adaptive_game_difficulty(
    db: AsyncSession,
    user_id: int,
    plan_id: int,
    game_id: str,
    requested_difficulty: int,
) -> tuple[int, str]:
    """Adapt difficulty from both game history and the learner's weak skill."""
    requested_difficulty = max(1, min(3, int(requested_difficulty)))
    current_skill = GAME_SKILL_MAP.get(game_id, "vocabulary")

    # Game-specific evidence keeps the adaptation responsive to the exact activity.
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

    recent_average = None
    if recent:
        scores = [
            event.correct_answers / max(1, event.questions_answered)
            for event in recent
        ]
        recent_average = sum(scores) / len(scores)

    # The latest persisted skill score captures cross-game performance for the
    # same competency. A weak skill should bias the next round toward review even
    # when this particular game has not been played recently.
    skill_result = await db.execute(
        select(Progress.skills)
        .where(
            Progress.user_id == user_id,
            Progress.study_plan_id == plan_id,
        )
        .order_by(Progress.date.desc())
        .limit(1)
    )
    skills = skill_result.scalar_one_or_none() or {}
    skill_score = skills.get(current_skill)
    if isinstance(skill_score, (int, float)) and not isinstance(skill_score, bool):
        skill_score = max(0.0, min(1.0, float(skill_score)))
    else:
        skill_score = None

    if recent_average is not None and recent_average < 0.5:
        return max(1, requested_difficulty - 1), "review"
    if skill_score is not None and skill_score < 0.5:
        return max(1, requested_difficulty - 1), "review"
    if recent_average is not None and recent_average >= 0.85:
        return min(3, requested_difficulty + 1), "challenge"
    if skill_score is not None and skill_score >= 0.85:
        return min(3, requested_difficulty + 1), "challenge"
    if recent_average is None and skill_score is None:
        return requested_difficulty, "new"
    return requested_difficulty, "steady"


async def _recommended_review_game(
    db: AsyncSession,
    user_id: int,
    plan: StudyPlan,
) -> tuple[str | None, str | None]:
    """Choose the next review game from due mistakes, then weakest skill."""
    game_for_skill = {
        "vocabulary": "quick_choice",
        "grammar": "grammar_duel",
        "listening": "listening_detective",
        "writing": "translation_sprint",
        "speaking": "context_quest",
    }
    priority = tuple(game_for_skill)
    due_items = await _get_recent_game_mistakes(db, user_id, plan.id, limit=100)
    due_counts: dict[str, int] = {}
    for item in due_items:
        skill = str(item.get("skill", ""))
        if skill in game_for_skill:
            due_counts[skill] = due_counts.get(skill, 0) + 1
    skill = next((name for name in priority if due_counts.get(name, 0)), None)
    if skill is None:
        skills = await _get_game_skills(db, user_id, plan)
        ranked = [
            (name, float(score))
            for name, score in skills.items()
            if name in game_for_skill and isinstance(score, (int, float))
        ]
        ranked.sort(key=lambda item: (item[1], priority.index(item[0])))
        skill = ranked[0][0] if ranked else None
    return (game_for_skill[skill], skill) if skill else (None, None)


@router.get("/smart-review", response_model=dict)
@limiter.limit("60/minute")
async def get_smart_review(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Return a safe overview of due cross-game review items."""
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        return {
            "due_count": 0,
            "skills": {},
            "recommended_game": None,
            "items": [],
        }

    due_items = await _get_recent_game_mistakes(
        db, current_user.id, plan.id, limit=100
    )
    current_skills = await _get_game_skills(db, current_user.id, plan)
    skill_counts: dict[str, int] = {}
    skill_details: dict[str, dict[str, object]] = {}
    for item in due_items:
        skill = str(item.get("skill", "vocabulary"))
        skill_counts[skill] = skill_counts.get(skill, 0) + 1
        mastery = current_skills.get(skill)
        mastery_score = round(max(0.0, min(1.0, float(mastery))), 3) if isinstance(mastery, (int, float)) and not isinstance(mastery, bool) else 0.0
        skill_details[skill] = {
            "mastery": mastery_score,
            "cefr_level": str(item.get("cefr_level") or plan.cefr_level),
            "due_count": skill_counts[skill],
        }

    recommended_game, recommended_skill = await _recommended_review_game(
        db, current_user.id, plan
    )
    # Priority is an explainable review signal: weaker mastery and repeated
    # misses raise priority, while preserving a bounded 1..100 score.
    items = []
    for item in due_items[:20]:
        skill = str(item.get("skill", "vocabulary"))
        mastery = skill_details.get(skill, {}).get("mastery", 0.0)
        review_count = max(0, int(item.get("review_count", 0)))
        priority_score = min(100, round((1.0 - float(mastery)) * 70 + min(review_count, 5) * 6 + 10))
        priority = "high" if priority_score >= 70 else "medium" if priority_score >= 45 else "low"
        items.append({
            "review_key": str(item.get("review_key", "")),
            "skill": skill,
            "topic": str(item.get("topic", "")),
            "prompt": str(item.get("prompt", "")),
            "review_count": review_count,
            "due_at": str(item.get("review_due_at", "")),
            "source_game_id": str(item.get("source_game_id", "")),
            "mastery": float(mastery),
            "mastery_state": "struggling" if float(mastery) < 0.5 else "learning" if float(mastery) < 0.75 else "strong",
            "cefr_level": str(item.get("cefr_level") or plan.cefr_level),
            "priority": priority,
            "priority_score": priority_score,
        })

    return {
        "due_count": len(due_items),
        "cefr_level": str(plan.cefr_level),
        "skills": skill_counts,
        "skill_details": skill_details,
        "recommended_game": recommended_game,
        "recommended_skill": recommended_skill,
        "items": items,
    }


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
    effective_game_id = data.game_id
    if data.game_id == "word_match":
        effective_game_id = "matching"
    if data.review and effective_game_id != "review_mix":
        recommended_game, _ = await _recommended_review_game(db, current_user.id, plan)
        if recommended_game:
            effective_game_id = recommended_game
    effective_difficulty, adaptive_mode = await _get_adaptive_game_difficulty(
        db, current_user.id, plan.id, effective_game_id, data.difficulty
    )
    if data.review:
        adaptive_mode = "review"
    if effective_game_id == "review_mix":
        questions = await _build_multi_skill_review_questions(
            db,
            current_user.id,
            plan,
            data.language,
            effective_difficulty,
        )
    elif effective_game_id in {"memory", "matching", "ordering", "sentence_builder"}:
        cefr_level = cast(CEFRLevel, plan.cefr_level)
        preferred_topics = await _get_adaptive_review_topics(
            db,
            current_user.id,
            plan.id,
            GAME_SKILL_MAP.get(effective_game_id),
            plan.target_language,
            cefr_level,
        )
        interactive_review_items = [
            item
            for item in await _get_recent_game_mistakes(
                db,
                current_user.id,
                plan.id,
                skill=GAME_SKILL_MAP.get(effective_game_id),
                limit=20,
            )
            if item.get("source_game_id") == effective_game_id
        ]
        # Weak/reviewing items are exact retrieval targets. Mastered items are
        # omitted from the preferred queue so the round can introduce fresh
        # curriculum content instead of repeatedly drilling already-stable items.
        interactive_review_items = [
            item for item in interactive_review_items
            if str(item.get("mastery_state", "")) != "mastered"
        ]
        interaction_public, interaction_solution = _server_interactive_challenge(
            effective_game_id,
            data.language,
            effective_difficulty,
            plan.target_language,
            cefr_level,
            preferred_topics,
            interactive_review_items,
        )
        questions = [{
            "id": str(uuid4()),
            "prompt": interaction_public["type"],
            "choices": [],
            "answer": "",
            "hint": "",
            "skill": GAME_SKILL_MAP[effective_game_id],
            "difficulty": effective_difficulty,
            "interaction": {"public": interaction_public, "solution": interaction_solution},
        }]
    else:
        cefr_level = cast(CEFRLevel, plan.cefr_level)
        preferred_topics = await _get_adaptive_review_topics(db, current_user.id, plan.id, GAME_SKILL_MAP.get(effective_game_id), plan.target_language, cefr_level)
        questions = _server_game_questions(effective_game_id, data.language, effective_difficulty, plan.target_language, cefr_level, preferred_topics)
    if (adaptive_mode == "review" or data.review) and effective_game_id not in {"memory", "matching", "ordering", "sentence_builder", "review_mix"}:
        mistakes = await _get_recent_game_mistakes(
            db,
            current_user.id,
            plan.id,
            skill=GAME_SKILL_MAP.get(effective_game_id),
        )
        questions = _apply_smart_review(
            questions,
            mistakes,
            plan.target_language,
            cast(CEFRLevel, plan.cefr_level),
        )
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
        game_id=effective_game_id,
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

    mistakes: list[dict] = []
    # Track per-skill results for every server-issued game, including
    # interactive games. Mixed review rounds use this map to update each
    # covered skill instead of collapsing the result into one skill.
    skill_results: dict[str, list[int]] = {}
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
            for pair_id, item in solution.get("review_items", {}).items():
                pair_attempts = [a for a in data.interaction_trace if str(solution.get("pairs", {}).get(str(a.get("first")), "")) == str(pair_id) or str(solution.get("pairs", {}).get(str(a.get("second")), "")) == str(pair_id)]
                if any(solution.get("pairs", {}).get(a.get("first")) != solution.get("pairs", {}).get(a.get("second")) for a in pair_attempts):
                    question = {"skill": "memory", "topic": item.get("topic", "vocabulary"), "prompt": item.get("word", ""), "answer": item.get("definition", ""), "input_mode": "choice", "target_language": plan.target_language, "cefr_level": plan.cefr_level}
                    mistakes.append({"review_key": str(item.get("review_key") or _review_key(question)), "review_count": 1, "next_review_at": (now + _review_interval(1)).isoformat(), "question": question})
            for item in solution.get("review_items", {}).values():
                if item.get("review_key"):
                    mistakes.append({"review_key": str(item["review_key"]), "resolved": True})
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
            for attempt in data.interaction_trace:
                left_id, right_id = attempt.get("left"), attempt.get("right")
                if pairs.get(left_id) != right_id:
                    pair_index = pairs.get(left_id)
                    item = solution.get("review_items", {}).get(str(pair_index))
                    if item:
                        question = {"skill": "vocabulary", "topic": item.get("topic", "vocabulary"), "prompt": item.get("word", ""), "answer": item.get("definition", ""), "input_mode": "choice", "target_language": plan.target_language, "cefr_level": plan.cefr_level}
                        mistakes.append({"review_key": str(item.get("review_key") or _review_key(question)), "review_count": 1, "next_review_at": (now + _review_interval(1)).isoformat(), "question": question})
                        break
            for item in solution.get("review_items", {}).values():
                if item.get("review_key"):
                    mistakes.append({"review_key": str(item["review_key"]), "resolved": True})
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
            review_item = solution.get("review_items", {}).get("sentence")
            if any(attempt != target for attempt in attempts[:-1]):
                item = solution.get("review_items", {}).get("sentence")
                if item:
                    question = {"skill": "grammar", "topic": item.get("topic", "grammar"), "prompt": item.get("sentence", ""), "answer": item.get("sentence", ""), "input_mode": "text", "target_language": plan.target_language, "cefr_level": plan.cefr_level}
                    mistakes.append({"review_key": str(item.get("review_key") or _review_key(question)), "review_count": 1, "next_review_at": (now + _review_interval(1)).isoformat(), "question": question})
            if review_item and review_item.get("review_key"):
                mistakes.append({"review_key": str(review_item["review_key"]), "resolved": True})
    else:
        expected = {item["id"]: item for item in session.questions}
        if len(data.answers) != len(expected) or set(item.question_id for item in data.answers) != set(expected):
            raise HTTPException(status_code=422, detail="Exactly one answer is required for every question")

        correct_answers = 0
        for submitted in data.answers:
            question = expected[submitted.question_id]
            question_skill = str(question.get("skill", GAME_SKILL_MAP.get(session.game_id, "vocabulary")))
            skill_results.setdefault(question_skill, [0, 0])
            skill_results[question_skill][1] += 1
            is_correct = False
            if question.get("input_mode", "choice") == "text":
                if not submitted.choice.strip():
                    raise HTTPException(status_code=422, detail="Text answer cannot be empty")
                is_correct = _game_answer_matches(submitted.choice, question["answer"])
            else:
                if submitted.choice == "__timeout__":
                    is_correct = False
                else:
                    if submitted.choice not in question["choices"]:
                        raise HTTPException(status_code=422, detail="Invalid choice for game question")
                    is_correct = submitted.choice == question["answer"]
            if is_correct:
                correct_answers += 1
                skill_results[question_skill][0] += 1
                if question.get("review"):
                    mistakes.append({
                        "review_key": str(question.get("review_key") or _review_key(question)),
                        "resolved": True,
                        "question_id": submitted.question_id,
                    })
            else:
                review_count = int(question.get("review_count", 0)) if question.get("review") else 0
                snapshot = {
                    key: question.get(key)
                    for key in (
                        "id", "prompt", "choices", "hint", "answer",
                        "skill", "difficulty", "input_mode", "audio_text",
                        "audio_language", "topic",
                    )
                }
                # Pin review content to the study plan that produced it so
                # later retrieval practice cannot cross language/CEFR boundaries.
                snapshot["target_language"] = plan.target_language
                snapshot["cefr_level"] = plan.cefr_level
                review_key = str(question.get("review_key") or _review_key(question))
                mistakes.append({
                    "review_key": review_key,
                    "review_count": review_count + 1,
                    "next_review_at": (
                        now + _review_interval(review_count + 1)
                    ).isoformat(),
                    "question_id": submitted.question_id,
                    "submitted": submitted.choice,
                    "question": snapshot,
                })
        questions_answered = len(expected)

    # Interactive rounds are scored as one skill; regular and mixed rounds
    # already populated the map question-by-question.
    if not skill_results:
        skill = GAME_SKILL_MAP.get(session.game_id, "vocabulary")
        skill_results[skill] = [correct_answers, questions_answered]

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
    raw_xp = correct_answers * 5 + (questions_answered - correct_answers)
    difficulty_multiplier = {1: 1.0, 2: 1.15, 3: 1.3}.get(int(session.difficulty), 1.0)
    base_xp = max(
        0,
        round(raw_xp * difficulty_multiplier),
    )
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
    if session.game_id == "review_mix" and skill_results:
        current_skill = max(
            skill_results,
            key=lambda skill: (skill_results[skill][1], skill),
        )
        current_skill_score = skill_results[current_skill][0] / max(1, skill_results[current_skill][1])
    projected_skills = dict(skills)
    for skill, (skill_correct, skill_questions) in skill_results.items():
        skill_score = skill_correct / max(1, skill_questions)
        before = float(projected_skills.get(skill, skill_score))
        projected_skills[skill] = round(before * 0.7 + skill_score * 0.3, 3)
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
    if session.game_id == "review_mix" and skill_results:
        progress_entry = None
        for skill, (skill_correct, skill_questions) in skill_results.items():
            progress_entry = await update_daily_progress(
                db, user_id, study_plan_id=plan_id,
                xp=0,
                skill=skill,
                skill_score=skill_correct / max(1, skill_questions),
                commit=False,
            )
        progress_entry = await update_daily_progress(
            db, user_id, study_plan_id=plan_id,
            xp=base_xp + achievement_xp,
            skill=current_skill,
            skill_score=current_skill_score,
            commit=False,
        )
    else:
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
        mistakes=mistakes,
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
        skill_results={
            skill: {
                "correct": skill_correct,
                "questions": skill_questions,
                "accuracy": round(skill_correct / max(1, skill_questions), 3),
                "mastery_before": round(float(skills.get(skill, 0.0)), 3),
                "mastery_after": round(float(projected_skills.get(skill, skills.get(skill, 0.0))), 3),
                "mastery_delta": round(
                    float(projected_skills.get(skill, skills.get(skill, 0.0)))
                    - float(skills.get(skill, 0.0)),
                    3,
                ),
            }
            for skill, (skill_correct, skill_questions) in skill_results.items()
        },
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