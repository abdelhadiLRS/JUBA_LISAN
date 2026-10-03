"""Actual ASGI routes + isolated file-backed SQLite transactions.

Optional real Redis test uses TEST_REDIS_URL, never flushes shared databases.
Run: pytest tests/test_operational_integration.py -q
"""
import asyncio
import os
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from uuid import uuid4
from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from redis.asyncio import Redis
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.config import settings
from app.core.database import Base, get_db
from app.core.deps import get_redis
from app.core.security import create_access_token, hash_password
from app.main import app
from app.models.game_progress_event import GameProgressEvent
from app.models.game_session import GameSession
from app.models.progress import Progress
from app.models.refresh_token import RefreshToken
from app.models.study_plan import StudyPlan
from app.models.user import User
from app.models.user_language import UserLanguage
from app.routers.auth import _consume_refresh_token, _store_refresh_token

BANK = [SimpleNamespace(word=w, definition=d) for w, d in [
    ('book', 'a written work'), ('water', 'a drink'), ('school', 'a place to study'),
    ('friend', 'a person you like'), ('sun', 'a bright star'), ('door', 'an entrance'),
]]


@pytest_asyncio.fixture
async def operational(tmp_path, mock_redis, monkeypatch):
    engine = create_async_engine(f"sqlite+aiosqlite:///{tmp_path / 'integration.db'}", connect_args={'timeout': 10})
    sessions = async_sessionmaker(engine, expire_on_commit=False)
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    async with sessions() as db:
        user = User(username='learner', email='learner@test.com', display_name='Learner',
                    native_language='en', target_language='en-US', role='user',
                    hashed_password=hash_password('Test1234!@'), is_active=True)
        db.add(user)
        await db.flush()
        language = UserLanguage(user_id=user.id, target_language='en-US', is_active=True)
        db.add(language)
        await db.flush()
        plan = StudyPlan(user_id=user.id, user_language_id=language.id, cefr_level='A1', target_language='en-US',
                         goals=['vocabulary'], duration_weeks=4, days_per_week=4, current_unit='', generated_plan={}, is_active=True)
        db.add(plan)
        await db.commit()
        user_id, plan_id = user.id, plan.id
    async def request_db():
        async with sessions() as db:
            try:
                yield db
            except BaseException:
                await db.rollback()
                raise
    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = request_db
    app.dependency_overrides[get_redis] = lambda: mock_redis
    monkeypatch.setattr(settings, 'STRIPE_ENABLED', False)
    monkeypatch.setattr(settings, 'EMAIL_ENABLED', False)
    headers = {'Authorization': 'Bearer ' + create_access_token(user_id, 'user')}
    with patch('app.routers.game_results.get_vocabulary_by_level', return_value=[SimpleNamespace(words=BANK)]):
        async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
            try:
                yield SimpleNamespace(client=client, sessions=sessions, redis=mock_redis, headers=headers, user_id=user_id, plan_id=plan_id)
            finally:
                app.dependency_overrides.clear()
                app.dependency_overrides.update(previous)
                await engine.dispose()


async def start(ctx, game='quick_choice'):
    response = await ctx.client.post('/api/progress/game-session/arena', headers=ctx.headers,
        json={'game_id': game, 'target_language': 'en-US', 'difficulty': 1, 'relaxed': True})
    assert response.status_code == 200, response.text
    return response.json()


async def send(ctx, state, kind, **kwargs):
    payload = dict(action_id=str(uuid4()), version=state['version'], kind=kind, value='', order=[])
    payload.update(kwargs)
    response = await ctx.client.post(f"/api/progress/game-session/arena/{state['session_id']}/move", headers=ctx.headers, json=payload)
    return response, payload


@pytest.mark.asyncio
async def test_one_answer_then_leave_records_one_attempt_and_replay_once(operational):
    ctx = operational
    state = await start(ctx)
    async with ctx.sessions() as db:
        game = await db.get(GameSession, state['session_id'])
        answer = game.questions[0]['questions'][0]['definition']
    response, _ = await send(ctx, state, 'answer', value=answer)
    assert response.status_code == 200
    response, request = await send(ctx, response.json(), 'leave')
    assert response.status_code == 200, response.text
    saved = response.json()['result']
    assert saved['round_correct'] == saved['round_questions'] == 1
    assert saved['xp_earned'] == 5 and saved['current_correct_streak'] == 0
    # Simulate a committed response lost in transport: same request must recover.
    replay = await ctx.client.post(f"/api/progress/game-session/arena/{state['session_id']}/move", headers=ctx.headers, json=request)
    assert replay.status_code == 200 and replay.json()['result'] == saved
    async with ctx.sessions() as db:
        events = await db.scalar(select(func.count(GameProgressEvent.id)))
        progress = await db.scalar(select(Progress).where(Progress.user_id == ctx.user_id))
        assert events == 1 and progress.exercises_total == progress.exercises_correct == 1
        assert progress.xp_earned == 5 and progress.skills['vocabulary'] == 1.0


@pytest.mark.asyncio
async def test_rejected_move_rolls_back_and_another_move_can_succeed(operational):
    ctx = operational
    state = await start(ctx, 'memory')
    response, _ = await send(ctx, state, 'leave')
    assert response.status_code == 409
    restored = await ctx.client.get(f"/api/progress/game-session/arena/{state['session_id']}", headers=ctx.headers)
    assert restored.status_code == 200 and restored.json()['version'] == 0
    assert all(c['label'] is None for c in restored.json()['cards'])
    response, _ = await send(ctx, restored.json(), 'flip', value=restored.json()['cards'][0]['id'])
    assert response.status_code == 200 and response.json()['version'] == 1


@pytest.mark.asyncio
async def test_expired_and_changed_plan_rounds_are_not_restored(operational):
    ctx = operational
    state = await start(ctx)
    async with ctx.sessions() as db:
        await db.execute(update(GameSession).where(GameSession.id == state['session_id']).values(expires_at=datetime.now(UTC).replace(tzinfo=None) - timedelta(seconds=1)))
        await db.commit()
    assert (await ctx.client.get(f"/api/progress/game-session/arena/{state['session_id']}", headers=ctx.headers)).status_code == 410
    state = await start(ctx)
    async with ctx.sessions() as db:
        await db.execute(update(StudyPlan).where(StudyPlan.id == ctx.plan_id).values(is_active=False))
        await db.commit()
    assert (await ctx.client.get(f"/api/progress/game-session/arena/{state['session_id']}", headers=ctx.headers)).status_code == 404


@pytest.mark.asyncio
@pytest.mark.parametrize('sql_refresh', [False, True])
async def test_password_change_revokes_old_access_and_refresh_in_both_stores(operational, sql_refresh):
    ctx = operational
    if sql_refresh:
        app.dependency_overrides[get_redis] = lambda: None
    login = await ctx.client.post('/api/auth/login', json={'email': 'learner@test.com', 'password': 'Test1234!@'})
    assert login.status_code == 200
    old_cookie = login.cookies.get('refresh_token')
    old_headers = {'Authorization': 'Bearer ' + login.json()['access_token']}
    changed = await ctx.client.patch('/api/auth/me', headers=old_headers, json={'password': 'NewPass123!@'})
    assert changed.status_code == 200, changed.text
    assert (await ctx.client.get('/api/auth/me', headers=old_headers)).status_code == 401
    ctx.client.cookies.clear()
    rejected = await ctx.client.post('/api/auth/refresh', headers={'Cookie': f'refresh_token={old_cookie}'})
    assert rejected.status_code == 401 and 'refresh_token=' not in rejected.headers.get('set-cookie', '')
    fresh = await ctx.client.post('/api/auth/login', json={'email': 'learner@test.com', 'password': 'NewPass123!@'})
    assert fresh.status_code == 200
    assert (await ctx.client.get('/api/auth/me', headers={'Authorization': 'Bearer ' + fresh.json()['access_token']})).status_code == 200
    async with ctx.sessions() as db:
        user = await db.get(User, ctx.user_id)
        assert user.session_version == 1


@pytest.mark.asyncio
async def test_password_reset_revokes_prior_sessions(operational):
    ctx = operational
    token = str(uuid4())
    await ctx.redis.setex(f'reset_password:{token}', 3600, str(ctx.user_id))
    login = await ctx.client.post('/api/auth/login', json={'email': 'learner@test.com', 'password': 'Test1234!@'})
    old_cookie = login.cookies.get('refresh_token')
    response = await ctx.client.post('/api/auth/reset-password', json={'token': token, 'new_password': 'ResetPass123!@'})
    assert response.status_code == 200
    assert (await ctx.client.get('/api/auth/me', headers=ctx.headers)).status_code == 401
    ctx.client.cookies.clear()
    assert (await ctx.client.post('/api/auth/refresh', headers={'Cookie': f'refresh_token={old_cookie}'})).status_code == 401


@pytest.mark.asyncio
@pytest.mark.parametrize('sql_refresh', [False, True])
async def test_inactive_account_does_not_receive_rotated_credentials(operational, sql_refresh):
    ctx = operational
    if sql_refresh:
        app.dependency_overrides[get_redis] = lambda: None
    login = await ctx.client.post('/api/auth/login', json={'email': 'learner@test.com', 'password': 'Test1234!@'})
    async with ctx.sessions() as db:
        await db.execute(update(User).where(User.id == ctx.user_id).values(is_active=False))
        await db.commit()
    response = await ctx.client.post('/api/auth/refresh')
    assert response.status_code == 401 and 'set-cookie' not in response.headers
    if sql_refresh:
        async with ctx.sessions() as db:
            assert await db.scalar(select(func.count(RefreshToken.id))) == 0


@pytest.mark.asyncio
async def test_concurrent_consumers_cannot_reuse_redis_token(mock_redis):
    token = str(uuid4())
    await _store_refresh_token(mock_redis, token, 42, 60, session_version=3)
    results = await asyncio.gather(_consume_refresh_token(mock_redis, token), _consume_refresh_token(mock_redis, token))
    assert sorted(v for v in results if v is not None) == [42]


@pytest.mark.asyncio
async def test_real_redis_atomic_consumption_when_configured():
    url = os.environ.get('TEST_REDIS_URL')
    if not url:
        pytest.skip('Set TEST_REDIS_URL for the real Redis integration test')
    redis = Redis.from_url(url, decode_responses=True)
    token = str(uuid4())
    try:
        await _store_refresh_token(redis, token, 42, 60, session_version=0)
        results = await asyncio.gather(*[_consume_refresh_token(redis, token) for _ in range(10)])
        assert sum(v == 42 for v in results) == 1
    finally:
        await redis.delete(f'refresh:{token}')
        await redis.aclose()
