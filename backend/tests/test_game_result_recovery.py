from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import func, select

from app.core.security import create_access_token
from app.models.game_progress_event import GameProgressEvent
from app.models.game_session import GameSession
from app.models.progress import Progress
from app.models.user import User
from tests.conftest import make_study_plan
from tests.test_game_competitions import start_memory, complete_memory


@pytest.mark.asyncio
async def test_result_recovery_requires_authentication(client):
    assert (await client.get('/api/progress/game-session/unknown/result')).status_code == 401


@pytest.mark.asyncio
async def test_unknown_session_does_not_expose_a_result(client, test_user):
    _, headers = test_user
    assert (await client.get('/api/progress/game-session/unknown/result', headers=headers)).status_code == 404


@pytest.mark.asyncio
async def test_unfinished_session_is_not_treated_as_saved(client, test_user, db_session):
    user, headers = test_user
    await make_study_plan(db_session, user_id=user.id, cefr_level='A1', is_active=True)
    await db_session.commit()
    started = await start_memory(client, headers)
    recovery = await client.get(f"/api/progress/game-session/{started['session_id']}/result", headers=headers)
    assert recovery.status_code == 409
    assert recovery.json()['detail'] == 'Game result not saved yet'
    assert await db_session.scalar(select(func.count()).select_from(GameProgressEvent)) == 0


@pytest.mark.asyncio
async def test_saved_result_is_read_only_and_does_not_change_competition_xp(client, test_user, db_session):
    user, headers = test_user
    await make_study_plan(db_session, user_id=user.id, cefr_level='A1', is_active=True)
    await db_session.commit()
    assert (await client.post('/api/leagues/join', json={}, headers=headers)).status_code == 200
    started = await start_memory(client, headers)
    saved, _ = await complete_memory(client, headers, db_session, started)
    before_xp = await db_session.scalar(select(func.sum(Progress.xp_earned)).where(Progress.user_id == user.id))
    before_events = await db_session.scalar(select(func.count()).select_from(GameProgressEvent))
    for _ in range(3):
        response = await client.get(f"/api/progress/game-session/{started['session_id']}/result", headers=headers)
        assert response.status_code == 200
        data = response.json()
        for field in ['xp_earned', 'round_score', 'round_correct', 'round_questions', 'total_xp', 'games_played', 'achievements']:
            assert data[field] == saved[field]
        # Recovery deliberately doesn't fabricate unpersisted response details.
        assert data['new_achievements'] == []
        assert data['skill_results'] == {}
        assert 'questions' not in data
        assert 'answer' not in data
    assert await db_session.scalar(select(func.sum(Progress.xp_earned)).where(Progress.user_id == user.id)) == before_xp
    assert await db_session.scalar(select(func.count()).select_from(GameProgressEvent)) == before_events
    board = (await client.get('/api/leaderboard', headers=headers)).json()
    league = (await client.get('/api/leagues/current', headers=headers)).json()
    assert board['current_user']['xp'] == league['current_user']['xp'] == before_xp


@pytest.mark.asyncio
async def test_completed_result_can_be_recovered_after_expiry_and_plan_archival(client, test_user, db_session):
    user, headers = test_user
    plan = await make_study_plan(db_session, user_id=user.id, cefr_level='A1', is_active=True)
    await db_session.commit()
    started = await start_memory(client, headers)
    saved, _ = await complete_memory(client, headers, db_session, started)
    session = await db_session.get(GameSession, started['session_id'])
    session.expires_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(days=1)
    plan.is_active = False
    await db_session.commit()
    response = await client.get(f"/api/progress/game-session/{started['session_id']}/result", headers=headers)
    assert response.status_code == 200
    assert response.json()['xp_earned'] == saved['xp_earned']


@pytest.mark.asyncio
async def test_other_learner_cannot_read_saved_result(client, test_user, db_session):
    user, headers = test_user
    await make_study_plan(db_session, user_id=user.id, cefr_level='A1', is_active=True)
    await db_session.commit()
    started = await start_memory(client, headers)
    await complete_memory(client, headers, db_session, started)
    other = User(username='recovery-other', display_name='Other', hashed_password='not-used', native_language='fr', target_language='en-US', role='user', is_active=True)
    db_session.add(other)
    await db_session.commit()
    other_headers = {'Authorization': f'Bearer {create_access_token(other.id, other.role)}'}
    response = await client.get(f"/api/progress/game-session/{started['session_id']}/result", headers=other_headers)
    assert response.status_code == 404
    assert response.json()['detail'] == 'Game session not found'
