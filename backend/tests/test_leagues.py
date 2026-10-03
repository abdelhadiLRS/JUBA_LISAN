from datetime import date, timedelta

import pytest
from sqlalchemy import func, select

from app.models.league import LeagueMembership, LeagueSeason
from app.models.progress import Progress
from app.models.user import User
from app.services.league_rules import next_tier, period_bounds, week_start
from tests.conftest import make_study_plan


def test_period_boundaries():
    day = date(2027, 1, 1)
    assert period_bounds("week", day) == (date(2026, 12, 28), date(2027, 1, 2))
    assert period_bounds("month", day) == (day, date(2027, 1, 2))
    assert period_bounds("day", day) == (day, date(2027, 1, 2))
    assert period_bounds("all", day) == (None, date(2027, 1, 2))
    with pytest.raises(ValueError):
        period_bounds("invalid", day)


def test_tier_rules():
    assert next_tier(1, 1, 10, 100) == 2
    assert next_tier(1, 10, 10, 0) == 0
    assert next_tier(1, 5, 10, 50) == 1
    assert next_tier(1, 1, 4, 100) == 1
    assert next_tier(1, 1, 10, 0) == 1
    assert next_tier(5, 1, 10, 100) == 5
    assert next_tier(0, 10, 10, 0) == 0
    # Tied last place begins at rank 8, outside the bottom-two cutoff: neither falls.
    assert next_tier(1, 8, 10, 10) == 1


async def add_competitor(db, season, name, *, xp=0, tier=0, active=True, role="user"):
    user = User(
        username=name, display_name=name, hashed_password="not-used-in-this-test",
        native_language="ar", target_language=season.target_language,
        is_active=active, role=role,
    )
    db.add(user)
    await db.flush()
    plan = await make_study_plan(
        db, user_id=user.id, target_language=season.target_language,
        cefr_level="A1", is_active=True,
    )
    db.add(LeagueMembership(season_id=season.id, user_id=user.id, tier=tier))
    db.add(Progress(
        user_id=user.id, study_plan_id=plan.id, date=season.week_start,
        xp_earned=xp,
    ))
    await db.flush()
    return user


@pytest.mark.asyncio
async def test_authentication_required(client):
    for url in ["/api/leaderboard", "/api/leagues/current", "/api/leagues/history"]:
        assert (await client.get(url)).status_code == 401
    assert (await client.post("/api/leagues/join", json={})).status_code == 401


@pytest.mark.asyncio
async def test_admin_cannot_join(client, admin_user):
    _, headers = admin_user
    assert (await client.post("/api/leagues/join", json={}, headers=headers)).status_code == 403


@pytest.mark.asyncio
async def test_empty_reads_do_not_create_membership(client, test_user, db_session):
    _, headers = test_user
    league = await client.get("/api/leagues/current", headers=headers)
    assert league.status_code == 200
    assert league.json()["joined"] is False
    assert league.json()["season_id"] is None
    assert league.json()["entries"] == []
    assert (await client.get("/api/leaderboard", headers=headers)).json()["total"] == 0
    assert await db_session.scalar(select(func.count()).select_from(LeagueMembership)) == 0


@pytest.mark.asyncio
async def test_join_is_idempotent_and_rejects_client_points(client, test_user, db_session):
    user, headers = test_user
    first = await client.post("/api/leagues/join", json={}, headers=headers)
    second = await client.post("/api/leagues/join", json={}, headers=headers)
    assert first.status_code == second.status_code == 200
    assert first.json()["season_id"] == second.json()["season_id"]
    assert first.json()["joined"] is True
    assert first.json()["tier"] == "bronze"
    assert first.json()["current_user"]["xp"] == 0
    assert await db_session.scalar(select(func.count()).select_from(LeagueMembership)) == 1
    assert (await client.post(
        "/api/leagues/join", json={"xp": 99999, "tier": "diamond", "user_id": user.id},
        headers=headers,
    )).status_code == 422


@pytest.mark.asyncio
async def test_real_xp_scope_ties_and_pagination(client, test_user, db_session):
    user, headers = test_user
    joined = (await client.post("/api/leagues/join", json={}, headers=headers)).json()
    season = await db_session.get(LeagueSeason, joined["season_id"])
    old = await make_study_plan(
        db_session, user_id=user.id, cefr_level="A1", is_active=False,
    )
    active = await make_study_plan(
        db_session, user_id=user.id, cefr_level="A2", is_active=True,
    )
    french = await make_study_plan(
        db_session, user_id=user.id, target_language="fr-FR", cefr_level="A1", is_active=True,
    )
    db_session.add_all([
        Progress(user_id=user.id, study_plan_id=old.id, date=date.today(), xp_earned=30),
        Progress(user_id=user.id, study_plan_id=active.id, date=date.today(), xp_earned=95, reward_xp=25),
        Progress(user_id=user.id, study_plan_id=french.id, date=date.today(), xp_earned=9000),
        Progress(user_id=user.id, study_plan_id=active.id, date=season.week_start - timedelta(days=1), xp_earned=700),
        Progress(user_id=user.id, study_plan_id=active.id, date=date.today() + timedelta(days=1), xp_earned=800),
    ])
    peer = await add_competitor(db_session, season, "tied-peer", xp=125)
    await add_competitor(db_session, season, "third-peer", xp=45)
    await add_competitor(db_session, season, "inactive-peer", xp=9999, active=False)
    await add_competitor(db_session, season, "admin-peer", xp=9999, role="admin")
    # A nonparticipant must not appear even with real XP.
    outsider = User(username="not-enrolled", display_name="Not Enrolled", hashed_password="unused", native_language="ar", target_language="en-US")
    db_session.add(outsider)
    await db_session.flush()
    outside_plan = await make_study_plan(db_session, user_id=outsider.id, cefr_level="A1")
    db_session.add(Progress(user_id=outsider.id, study_plan_id=outside_plan.id, date=date.today(), xp_earned=99999))
    await db_session.commit()
    response = await client.get("/api/leaderboard?period=week&limit=1&offset=1", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 3
    assert len(data["entries"]) == 1
    assert data["entries"][0]["user_id"] == peer.id
    assert data["entries"][0]["rank"] == 1
    assert data["current_user"]["xp"] == 125
    assert data["current_user"]["rank"] == 1
    assert "email" not in data["entries"][0]
    third = (await client.get("/api/leaderboard?offset=2", headers=headers)).json()
    assert third["entries"][0]["rank"] == 3
    beyond = (await client.get("/api/leaderboard?offset=99", headers=headers)).json()
    assert beyond["entries"] == []
    assert beyond["current_user"]["user_id"] == user.id
    french_board = (await client.get("/api/leaderboard?target_language=fr-FR", headers=headers)).json()
    assert french_board["total"] == 0


@pytest.mark.asyncio
async def test_validation_and_language_ownership(client, test_user):
    _, headers = test_user
    for query in ["limit=0", "limit=101", "offset=-1", "period=invalid"]:
        assert (await client.get("/api/leaderboard?" + query, headers=headers)).status_code == 422
    assert (await client.get("/api/leagues/current?tier=invalid", headers=headers)).status_code == 422
    assert (await client.get("/api/leaderboard?target_language=fr-FR", headers=headers)).status_code == 404
    assert (await client.post("/api/leagues/join", json={"target_language": "fr-FR"}, headers=headers)).status_code == 404


@pytest.mark.asyncio
async def test_rollover_snapshots_and_promotes_once(client, test_user, db_session):
    user, headers = test_user
    start = week_start(date.today()) - timedelta(days=7)
    season = LeagueSeason(target_language="en-US", week_start=start)
    db_session.add(season)
    await db_session.flush()
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level="A1", is_active=True)
    membership = LeagueMembership(user_id=user.id, season_id=season.id, tier=1)
    points = Progress(user_id=user.id, study_plan_id=plan.id, date=start, xp_earned=50)
    db_session.add_all([membership, points])
    for index, xp in enumerate([40, 30, 20, 10]):
        await add_competitor(db_session, season, f"previous-{index}", xp=xp, tier=1)
    await db_session.commit()
    joined = await client.post("/api/leagues/join", json={}, headers=headers)
    assert joined.status_code == 200
    assert joined.json()["tier"] == "gold"
    await db_session.refresh(season)
    await db_session.refresh(membership)
    assert season.finalized is True
    assert (membership.final_xp, membership.final_rank, membership.next_tier) == (50, 1, 2)
    points.xp_earned = 9999
    await db_session.commit()
    history = (await client.get("/api/leagues/history", headers=headers)).json()
    assert len(history) == 1
    assert history[0]["current_user"]["xp"] == 50
    assert history[0]["next_tier"] == "gold"
    repeated = (await client.post("/api/leagues/join", json={}, headers=headers)).json()
    assert repeated["tier"] == "gold"
    assert await db_session.scalar(select(func.count()).select_from(LeagueMembership).where(LeagueMembership.user_id == user.id)) == 2


@pytest.mark.asyncio
async def test_languages_have_independent_membership(client, test_user, db_session):
    user, headers = test_user
    await make_study_plan(db_session, user_id=user.id, target_language="fr-FR", cefr_level="A1")
    await db_session.commit()
    english = (await client.post("/api/leagues/join", json={}, headers=headers)).json()
    french = (await client.post("/api/leagues/join", json={"target_language": "fr-FR"}, headers=headers)).json()
    assert english["season_id"] != french["season_id"]
    assert english["tier"] == french["tier"] == "bronze"
    assert french["target_language"] == "fr-FR"
