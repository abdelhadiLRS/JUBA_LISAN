"""Game -> persisted progress -> competition rankings integration contract."""
from datetime import date

import pytest
from sqlalchemy import func, select

from app.models.game_session import GameSession
from app.models.progress import Progress
from tests.conftest import make_study_plan


async def start_memory(client, headers):
    response = await client.post(
        '/api/progress/game-session',
        json={'game_id': 'memory', 'language': 'en', 'difficulty': 1},
        headers=headers,
    )
    assert response.status_code == 200
    return response.json()


async def complete_memory(client, headers, db, started):
    # Read the server-owned solution in the test, without overwriting any answer,
    # XP, award or score. The production UI sends the learner's actual moves.
    game = await db.get(GameSession, started['session_id'])
    pairs = game.questions[0]['interaction']['solution']['pairs']
    grouped = {}
    for card_id, pair_id in pairs.items():
        grouped.setdefault(pair_id, []).append(card_id)
    trace = [{'first': ids[0], 'second': ids[1]} for ids in grouped.values()]
    body = {
        'session_id': started['session_id'], 'interaction_trace': trace,
        'daily_challenge': started['daily_challenge'],
        'daily_challenge_date': started['daily_challenge_date'],
    }
    response = await client.post('/api/progress/game-session/complete', json=body, headers=headers)
    assert response.status_code == 200
    return response.json(), body


@pytest.mark.asyncio
async def test_saved_game_updates_leaderboard_and_league_once(client, test_user, db_session):
    user, headers = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level='A1', is_active=True)
    await db_session.commit()
    joined = await client.post('/api/leagues/join', json={}, headers=headers)
    assert joined.status_code == 200
    assert joined.json()['current_user']['xp'] == 0

    started = await start_memory(client, headers)
    # Session creation and playing without saving cannot earn ranking XP.
    before = await client.get('/api/leaderboard?period=week', headers=headers)
    assert before.json()['current_user']['xp'] == 0
    saved, body = await complete_memory(client, headers, db_session, started)
    assert saved['xp_earned'] > 0
    persisted = int(await db_session.scalar(select(func.sum(Progress.xp_earned)).where(
        Progress.user_id == user.id, Progress.study_plan_id == plan.id,
        Progress.date == date.today(),
    )) or 0)
    assert persisted == saved['xp_earned']

    for period in ['day', 'week', 'month', 'all']:
        board = await client.get('/api/leaderboard?period=' + period, headers=headers)
        assert board.status_code == 200
        assert board.json()['current_user']['xp'] == persisted
        assert board.json()['current_user']['rank'] == 1
    league = await client.get('/api/leagues/current', headers=headers)
    assert league.json()['current_user']['xp'] == persisted
    assert league.json()['current_user']['rank'] == 1
    assert league.json()['season_id'] == joined.json()['season_id']

    # The same completion cannot contribute another copy of XP.
    replay = await client.post('/api/progress/game-session/complete', json=body, headers=headers)
    assert replay.status_code == 409
    board = await client.get('/api/leaderboard', headers=headers)
    league = await client.get('/api/leagues/current', headers=headers)
    assert board.json()['current_user']['xp'] == persisted
    assert league.json()['current_user']['xp'] == persisted


@pytest.mark.asyncio
async def test_games_before_enrollment_count_without_auto_enrollment(client, test_user, db_session):
    user, headers = test_user
    await make_study_plan(db_session, user_id=user.id, cefr_level='A1', is_active=True)
    await db_session.commit()
    started = await start_memory(client, headers)
    saved, _ = await complete_memory(client, headers, db_session, started)
    before = await client.get('/api/leaderboard', headers=headers)
    assert before.json()['current_user'] is None
    assert before.json()['total'] == 0
    league = await client.get('/api/leagues/current', headers=headers)
    assert league.json()['joined'] is False
    joined = await client.post('/api/leagues/join', json={}, headers=headers)
    assert joined.status_code == 200
    assert joined.json()['current_user']['xp'] == saved['xp_earned']
    board = await client.get('/api/leaderboard', headers=headers)
    assert board.json()['current_user']['xp'] == saved['xp_earned']


@pytest.mark.asyncio
async def test_invalid_game_completion_does_not_change_competition_scores(client, test_user, db_session):
    user, headers = test_user
    await make_study_plan(db_session, user_id=user.id, cefr_level='A1', is_active=True)
    await db_session.commit()
    assert (await client.post('/api/leagues/join', json={}, headers=headers)).status_code == 200
    started = await start_memory(client, headers)
    rejected = await client.post('/api/progress/game-session/complete', json={
        'session_id': started['session_id'],
        'interaction_trace': [{'first':'forged-card', 'second':'another-forged-card'}],
    }, headers=headers)
    assert rejected.status_code == 422
    board = await client.get('/api/leaderboard', headers=headers)
    league = await client.get('/api/leagues/current', headers=headers)
    assert board.json()['current_user']['xp'] == 0
    assert league.json()['current_user']['xp'] == 0


@pytest.mark.asyncio
async def test_game_xp_does_not_leak_into_other_language_competitions(client, test_user, db_session):
    user, headers = test_user
    await make_study_plan(db_session, user_id=user.id, cefr_level='A1', is_active=True)
    await make_study_plan(db_session, user_id=user.id, target_language='fr-FR', cefr_level='A1', is_active=True)
    await db_session.commit()
    assert (await client.post('/api/leagues/join', json={'target_language':'fr-FR'}, headers=headers)).status_code == 200
    assert (await client.post('/api/leagues/join', json={'target_language':'en-US'}, headers=headers)).status_code == 200
    started = await start_memory(client, headers)
    saved, _ = await complete_memory(client, headers, db_session, started)
    english = await client.get('/api/leaderboard?target_language=en-US', headers=headers)
    french = await client.get('/api/leaderboard?target_language=fr-FR', headers=headers)
    league = await client.get('/api/leagues/current?target_language=fr-FR', headers=headers)
    assert english.json()['current_user']['xp'] == saved['xp_earned']
    assert french.json()['current_user']['xp'] == 0
    assert league.json()['current_user']['xp'] == 0
