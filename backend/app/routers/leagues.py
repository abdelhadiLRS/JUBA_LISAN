"""Authenticated, opt-in competitions backed only by persisted learning XP."""
from datetime import UTC, date, datetime, timedelta
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from pydantic import BaseModel, ConfigDict
from sqlalchemy import case, func, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import require_learner
from app.core.limiter import limiter
from app.models.league import LeagueMembership, LeagueSeason
from app.models.progress import Progress
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.services.league_rules import TIERS, next_tier, period_bounds, week_start
from app.services.user_language_service import get_active_language

router = APIRouter(prefix="/api", tags=["competitions"])
Tier = Literal["bronze", "silver", "gold", "sapphire", "ruby", "diamond"]
Period = Literal["day", "week", "month", "all"]


class JoinRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    target_language: str | None = None


class Standing(BaseModel):
    user_id: int
    username: str
    display_name: str
    avatar: str | None
    xp: int
    rank: int
    is_current_user: bool


class LeaderboardResponse(BaseModel):
    target_language: str
    period: Period
    starts_on: date | None
    ends_on: date
    total: int
    offset: int
    limit: int
    entries: list[Standing]
    current_user: Standing | None


class LeagueResponse(BaseModel):
    season_id: int | None
    target_language: str
    week_start: date
    week_end: date
    ends_at: datetime
    finalized: bool
    joined: bool
    tier: Tier
    tiers: list[str]
    total: int
    offset: int
    limit: int
    entries: list[Standing]
    current_user: Standing | None
    next_tier: Tier | None


async def _language(db: AsyncSession, user: User, requested: str | None) -> str:
    if requested is None:
        active = await get_active_language(db, user.id)
        if active is None:
            raise HTTPException(404, "No active language")
        return active.target_language
    language = await db.scalar(select(UserLanguage).where(
        UserLanguage.user_id == user.id,
        UserLanguage.target_language == requested,
    ))
    if language is None:
        raise HTTPException(404, "Language not found for user")
    return language.target_language


def _xp(language: str, start: date | None, end: date):
    # Include archived plans so plan regeneration does not reset competition XP.
    points = case((Progress.xp_earned > 0, Progress.xp_earned), else_=0)
    query = select(
        Progress.user_id.label("user_id"), func.sum(points).label("xp")
    ).join(StudyPlan, StudyPlan.id == Progress.study_plan_id).where(
        StudyPlan.target_language == language,
        StudyPlan.user_id == Progress.user_id,
        Progress.date < end,
    )
    if start is not None:
        query = query.where(Progress.date >= start)
    return query.group_by(Progress.user_id).subquery()


def _ranking(language: str, start: date | None, end: date,
             season: LeagueSeason | None = None, tier: int | None = None):
    if season is not None and season.finalized:
        return select(
            LeagueMembership.user_id.label("user_id"),
            LeagueMembership.final_xp.label("xp"),
            LeagueMembership.final_rank.label("rank"),
        ).join(User, User.id == LeagueMembership.user_id).where(
            LeagueMembership.season_id == season.id,
            LeagueMembership.tier == tier,
            LeagueMembership.final_rank.is_not(None),
            User.is_active.is_(True), User.role != "admin",
        ).subquery()

    xp = _xp(language, start, end)
    base = select(
        User.id.label("user_id"), func.coalesce(xp.c.xp, 0).label("xp")
    ).outerjoin(xp, xp.c.user_id == User.id).where(
        User.is_active.is_(True), User.role != "admin",
    )
    if season is not None:
        base = base.join(LeagueMembership, LeagueMembership.user_id == User.id).where(
            LeagueMembership.season_id == season.id,
            LeagueMembership.tier == tier,
        )
    else:
        # Public standings expose only learners who explicitly joined competition.
        opted_in = select(LeagueMembership.id).join(
            LeagueSeason, LeagueSeason.id == LeagueMembership.season_id
        ).where(
            LeagueMembership.user_id == User.id,
            LeagueSeason.target_language == language,
        ).exists()
        base = base.where(opted_in)
    scores = base.subquery()
    return select(
        scores.c.user_id, scores.c.xp,
        func.rank().over(order_by=scores.c.xp.desc()).label("rank"),
    ).subquery()


async def _page(db: AsyncSession, ranking, user_id: int, limit: int, offset: int):
    total = int(await db.scalar(select(func.count()).select_from(ranking)) or 0)
    query = select(
        User.id.label("user_id"), User.username, User.display_name, User.avatar,
        ranking.c.xp, ranking.c.rank,
    ).join(ranking, ranking.c.user_id == User.id)

    def serialize(row):
        return Standing(
            user_id=row.user_id, username=row.username, display_name=row.display_name,
            avatar=row.avatar, xp=int(row.xp), rank=int(row.rank),
            is_current_user=row.user_id == user_id,
        )

    rows = (await db.execute(query.order_by(
        ranking.c.rank, User.id
    ).offset(offset).limit(limit))).all()
    own = (await db.execute(query.where(User.id == user_id))).one_or_none()
    return total, [serialize(row) for row in rows], serialize(own) if own else None


async def _insert_once(db: AsyncSession, model, values: dict, keys: list[str]):
    # Atomic conflict handling also obtains SQLite's writer lock before rollover.
    dialect = db.get_bind().dialect.name
    insert = sqlite_insert if dialect == "sqlite" else pg_insert
    await db.execute(insert(model).values(**values).on_conflict_do_nothing(
        index_elements=keys
    ))


async def _finalize(db: AsyncSession, language: str, current_week: date):
    expired = (await db.scalars(select(LeagueSeason).where(
        LeagueSeason.target_language == language,
        LeagueSeason.week_start < current_week,
        LeagueSeason.finalized.is_(False),
    ).order_by(LeagueSeason.week_start).with_for_update())).all()
    for season in expired:
        for tier in range(len(TIERS)):
            ranking = _ranking(
                language, season.week_start, season.week_start + timedelta(days=7),
                season, tier,
            )
            standings = (await db.execute(select(ranking))).all()
            by_user = {row.user_id: row for row in standings}
            members = (await db.scalars(select(LeagueMembership).where(
                LeagueMembership.season_id == season.id,
                LeagueMembership.tier == tier,
            ))).all()
            for member in members:
                row = by_user.get(member.user_id)
                member.final_xp = int(row.xp) if row else 0
                member.final_rank = int(row.rank) if row else None
                member.next_tier = (
                    next_tier(tier, int(row.rank), len(standings), int(row.xp))
                    if row else tier
                )
        season.finalized = True
    await db.flush()


async def _league_response(db: AsyncSession, user: User, language: str, day: date,
                           requested_tier: Tier | None, limit: int, offset: int):
    start = week_start(day)
    end = start + timedelta(days=7)
    season = await db.scalar(select(LeagueSeason).where(
        LeagueSeason.target_language == language, LeagueSeason.week_start == start,
    ))
    member = None
    if season:
        member = await db.scalar(select(LeagueMembership).where(
            LeagueMembership.season_id == season.id, LeagueMembership.user_id == user.id,
        ))
    tier = TIERS.index(requested_tier) if requested_tier else (member.tier if member else 0)
    total, entries, own = 0, [], None
    if season:
        total, entries, own = await _page(
            db, _ranking(language, start, min(end, date.today() + timedelta(days=1)),
                         season, tier),
            user.id, limit, offset,
        )
    return LeagueResponse(
        season_id=season.id if season else None, target_language=language,
        week_start=start, week_end=end - timedelta(days=1),
        ends_at=datetime.combine(end, datetime.min.time(), tzinfo=UTC),
        finalized=bool(season and season.finalized), joined=member is not None,
        tier=TIERS[tier], tiers=list(TIERS), total=total, offset=offset, limit=limit,
        entries=entries, current_user=own,
        next_tier=TIERS[member.next_tier] if member and member.next_tier is not None else None,
    )


@router.get("/leaderboard", response_model=LeaderboardResponse)
@limiter.limit("60/minute")
async def leaderboard(
    request: Request, period: Period = "week", target_language: str | None = None,
    limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0, le=100000),
    user: User = Depends(require_learner), db: AsyncSession = Depends(get_db),
):
    language = await _language(db, user, target_language)
    start, end = period_bounds(period, date.today())
    total, entries, own = await _page(db, _ranking(language, start, end), user.id, limit, offset)
    return LeaderboardResponse(
        target_language=language, period=period, starts_on=start,
        ends_on=end - timedelta(days=1), total=total, offset=offset, limit=limit,
        entries=entries, current_user=own,
    )


@router.get("/leagues/current", response_model=LeagueResponse)
@limiter.limit("60/minute")
async def current_league(
    request: Request, target_language: str | None = None, tier: Tier | None = None,
    limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0, le=100000),
    user: User = Depends(require_learner), db: AsyncSession = Depends(get_db),
):
    language = await _language(db, user, target_language)
    return await _league_response(db, user, language, date.today(), tier, limit, offset)


@router.post("/leagues/join", response_model=LeagueResponse)
@limiter.limit("10/minute")
async def join_league(
    request: Request, body: JoinRequest,
    user: User = Depends(require_learner), db: AsyncSession = Depends(get_db),
):
    language = await _language(db, user, body.target_language)
    start = week_start(date.today())
    await _insert_once(db, LeagueSeason, {
        "target_language": language, "week_start": start, "finalized": False,
    }, ["target_language", "week_start"])
    # Lock the current language-season before touching old seasons on PostgreSQL.
    season = (await db.scalars(select(LeagueSeason).where(
        LeagueSeason.target_language == language, LeagueSeason.week_start == start,
    ).with_for_update())).one()
    await _finalize(db, language, start)
    previous = await db.scalar(select(LeagueMembership).join(
        LeagueSeason, LeagueSeason.id == LeagueMembership.season_id
    ).where(
        LeagueMembership.user_id == user.id,
        LeagueSeason.target_language == language, LeagueSeason.week_start < start,
        LeagueSeason.finalized.is_(True),
    ).order_by(LeagueSeason.week_start.desc()).limit(1))
    tier = previous.next_tier if previous and previous.next_tier is not None else 0
    await _insert_once(db, LeagueMembership, {
        "season_id": season.id, "user_id": user.id, "tier": tier,
        "joined_at": datetime.now(UTC).replace(tzinfo=None),
    }, ["season_id", "user_id"])
    await db.commit()
    return await _league_response(db, user, language, date.today(), None, 20, 0)


@router.get("/leagues/history", response_model=list[LeagueResponse])
@limiter.limit("30/minute")
async def league_history(
    request: Request, target_language: str | None = None,
    limit: int = Query(12, ge=1, le=52), offset: int = Query(0, ge=0, le=100000),
    user: User = Depends(require_learner), db: AsyncSession = Depends(get_db),
):
    language = await _language(db, user, target_language)
    seasons = (await db.scalars(select(LeagueSeason).join(
        LeagueMembership, LeagueMembership.season_id == LeagueSeason.id
    ).where(
        LeagueMembership.user_id == user.id,
        LeagueSeason.target_language == language,
        LeagueSeason.week_start < week_start(date.today()),
    ).order_by(LeagueSeason.week_start.desc()).offset(offset).limit(limit))).all()
    return [await _league_response(db, user, language, season.week_start, None, 20, 0)
            for season in seasons]
