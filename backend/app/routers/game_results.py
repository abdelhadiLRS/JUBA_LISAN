"""Read-only recovery for committed game results after a lost HTTP response."""
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_learner
from app.core.limiter import limiter
from app.models.game_progress import GameProgress
from app.models.game_progress_event import GameProgressEvent
from app.models.game_session import GameSession
from app.models.progress import Progress
from app.models.user import User
from app.schemas.progress import GameSessionResultResponse

router = APIRouter(prefix='/api/progress/game-session', tags=['progress'])


@router.get('/{session_id}/result', response_model=GameSessionResultResponse)
@limiter.limit('30/minute')
async def get_saved_game_result(
    request: Request, session_id: str,
    user: User = Depends(require_learner), db: AsyncSession = Depends(get_db),
):
    # Do not expose another learner's existence or result. A completed session
    # remains recoverable after expiry or an active-language/plan switch.
    game = await db.scalar(select(GameSession).where(
        GameSession.id == session_id, GameSession.user_id == user.id,
    ))
    if game is None:
        raise HTTPException(404, 'Game session not found')
    if not game.completed:
        raise HTTPException(409, 'Game result not saved yet')
    event = await db.scalar(select(GameProgressEvent).where(
        GameProgressEvent.event_id == game.id,
        GameProgressEvent.user_id == user.id,
        GameProgressEvent.study_plan_id == game.study_plan_id,
    ))
    aggregate = await db.scalar(select(GameProgress).where(
        GameProgress.user_id == user.id,
        GameProgress.study_plan_id == game.study_plan_id,
    ))
    if event is None or aggregate is None:
        # Never infer a result or reconstruct rewards from the answer payload.
        raise HTTPException(409, 'Saved game result is unavailable')
    total_xp = int(await db.scalar(select(func.sum(Progress.xp_earned)).where(
        Progress.user_id == user.id,
        Progress.study_plan_id == game.study_plan_id,
    )) or 0)
    skills = await db.scalar(select(Progress.skills).where(
        Progress.user_id == user.id,
        Progress.study_plan_id == game.study_plan_id,
    ).order_by(Progress.date.desc()).limit(1))
    return GameSessionResultResponse(
        round_score=event.round_score,
        round_correct=event.correct_answers,
        round_questions=event.questions_answered,
        xp_earned=event.xp_earned,
        total_xp=total_xp,
        games_played=aggregate.games_played,
        questions_answered=aggregate.questions_answered,
        correct_answers=aggregate.correct_answers,
        best_round_score=aggregate.best_round_score,
        daily_challenges_completed=aggregate.daily_challenges_completed,
        last_daily_challenge_date=aggregate.last_daily_challenge_date,
        current_correct_streak=aggregate.current_correct_streak,
        best_correct_streak=aggregate.best_correct_streak,
        achievements=aggregate.achievements or [],
        skills=skills or {},
        # Old completion events do not persist the exact per-skill delta or the
        # response's newly-earned list. Do not invent either during recovery.
        skill_results={}, new_achievements=[],
    )
