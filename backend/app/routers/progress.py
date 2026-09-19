import random
from datetime import UTC, date, datetime, timedelta
from typing import cast
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, text, update
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
from app.schemas.progress import (GameSessionComplete, GameSessionResponse, GameSessionResultResponse, GameSessionStart, GameStatsResponse, ProgressHistoryResponse, ProgressResponse, ProgressSummary)
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



def _server_interactive_challenge(game_id: str, language: str, difficulty: int) -> tuple[dict, dict]:
    """Build a renderable challenge plus server-only solution state."""
    rng = random.SystemRandom()
    if game_id == "memory":
        symbols = {
            "ar": [("قمر", "moon"), ("كتاب", "book"), ("شمس", "sun"), ("بحر", "sea"), ("قلم", "pen"), ("باب", "door")],
            "fr": [("lune", "moon"), ("livre", "book"), ("soleil", "sun"), ("mer", "sea"), ("stylo", "pen"), ("porte", "door")],
            "en": [("moon", "lune"), ("book", "livre"), ("sun", "soleil"), ("sea", "mer"), ("pen", "stylo"), ("door", "porte")],
        }[language]
        count = {1: 3, 2: 4, 3: 5}[difficulty]
        selected = rng.sample(symbols, count)
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
        pairs_source = {
            "ar": [("كتاب", "book"), ("ماء", "water"), ("مدرسة", "school"), ("قلم", "pen")],
            "fr": [("livre", "book"), ("eau", "water"), ("école", "school"), ("stylo", "pen")],
            "en": [("book", "livre"), ("water", "eau"), ("school", "école"), ("pen", "stylo")],
        }[language]
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
    if game_id == "ordering":
        source = {
            "ar": ["الأول", "الثاني", "الثالث", "الرابع"],
            "fr": ["un", "deux", "trois", "quatre"],
            "en": ["one", "two", "three", "four"],
        }[language]
        items = [{"id": str(uuid4()), "label": label} for label in source]
        shuffled = list(items)
        rng.shuffle(shuffled)
        return {"type": "ordering", "items": shuffled}, {"target": [item["id"] for item in items]}
    raise ValueError("Unsupported interactive game")

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
        skills=await _get_game_skills(db, plan),
    )


def _server_game_questions(game_id: str, language: str, difficulty: int, target_language: str = "en-GB") -> list[dict]:
    rng = random.SystemRandom()
    hints = {
        "ar": "فكّر بهدوء قبل اختيار الإجابة.",
        "fr": "Réfléchis avant de choisir.",
        "en": "Think carefully before choosing.",
    }
    questions: list[dict] = []
    for index in range(5):
        question_id = str(uuid4())
        if game_id == "words":
            level = cast(CEFRLevel, {1: "A1", 2: "A2", 3: "B1"}[difficulty])
            vocab_sets = get_vocabulary_by_level(level, target_language)
            entries = [word for vocab_set in vocab_sets for word in vocab_set.words]
            rng.shuffle(entries)
            selected = entries[:4]
            if len(selected) < 4:
                fallback = [
                    ("hello", "a greeting"),
                    ("water", "a liquid people drink"),
                    ("school", "a place where people learn"),
                    ("book", "a written work"),
                ]
                selected = [type("VocabularyFallback", (), {"word": w, "definition": d})() for w, d in fallback]
            entry = selected[index % len(selected)]
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
    if data.game_id in {"memory", "matching", "ordering"}:
        interaction_public, interaction_solution = _server_interactive_challenge(
            data.game_id, data.language, data.difficulty
        )
        questions = [{
            "id": str(uuid4()),
            "prompt": interaction_public["type"],
            "choices": [],
            "answer": "",
            "hint": "",
            "skill": GAME_SKILL_MAP[data.game_id],
            "difficulty": data.difficulty,
            "interaction": {"public": interaction_public, "solution": interaction_solution},
        }]
    else:
        questions = _server_game_questions(data.game_id, data.language, data.difficulty, plan.target_language)
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
        interaction=questions[0].get("interaction", {}).get("public")
        if data.game_id in {"memory", "matching", "ordering"} else None,
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
    plan = await _get_active_plan_or_none(db, current_user.id)
    if plan is None:
        raise HTTPException(status_code=404, detail="No active study plan found")

    session = await db.get(GameSession, data.session_id)
    if session is None or session.user_id != user_id or session.study_plan_id != plan_id:
        raise HTTPException(status_code=404, detail="Game session not found")
    if session.completed:
        raise HTTPException(status_code=409, detail="Game session already completed")
    now = datetime.now(UTC).replace(tzinfo=None)
    if now > session.expires_at:
        raise HTTPException(status_code=410, detail="Game session expired")
    if data.daily_challenge and data.daily_challenge_date != date.today().isoformat():
        raise HTTPException(status_code=422, detail="daily_challenge_date must be today")

    if session.game_id in {"memory", "matching", "ordering"}:
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
            if submitted.choice not in question["choices"]:
                raise HTTPException(status_code=422, detail="Invalid choice for game question")
            if submitted.choice == question["answer"]:
                correct_answers += 1
        questions_answered = len(expected)
    # Capture scalar ownership keys before rollback. Async SQLAlchemy expires ORM
    # attributes on rollback, so reading current_user.id or plan.id afterwards
    # would trigger implicit async IO and raise MissingGreenlet.
    user_id = current_user.id
    plan_id = plan.id

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
    if session is None or session.user_id != current_user.id or session.study_plan_id != plan.id:
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
    skills = await _get_game_skills(db, plan)
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
        db, current_user.id, study_plan_id=plan.id,
        xp=base_xp + achievement_xp, skill=current_skill,
        skill_score=current_skill_score, commit=False,
    )
    if progress_entry is None:
        raise HTTPException(status_code=500, detail="Unable to persist game XP")

    db.add(GameProgressEvent(
        event_id=event_id, user_id=current_user.id, study_plan_id=plan.id,
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
