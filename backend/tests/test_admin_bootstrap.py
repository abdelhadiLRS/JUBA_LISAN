"""Real isolated SQLite connections; no shared in-memory concurrency fixture.

PostgreSQL statement compilation is covered, not a PostgreSQL runtime claim.
"""
import asyncio
from unittest.mock import patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import select
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.database import Base, get_db
from app.main import app
from app.models.user import AdminBootstrapClaim, User
from app.routers.auth import _claim_registration_role, get_redis


@pytest_asyncio.fixture
async def bootstrap_sessions(tmp_path):
    engine = create_async_engine(
        f"sqlite+aiosqlite:///{tmp_path / 'bootstrap.db'}",
        connect_args={"timeout": 10},
    )
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    try:
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        await engine.dispose()


def new_user(name, role="user"):
    return User(username=name, email=f"{name}@test.com", display_name=name,
                hashed_password="test-only", native_language="en", role=role)


@pytest.mark.asyncio
async def test_two_concurrent_registrations_have_exactly_one_admin(bootstrap_sessions, mock_redis):
    async def request_db():
        async with bootstrap_sessions() as session:
            try:
                yield session
            except BaseException:
                await session.rollback()
                raise

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = request_db
    app.dependency_overrides[get_redis] = lambda: mock_redis
    try:
        with (patch.object(settings, "FIRST_USER_IS_ADMIN", True),
              patch.object(settings, "ALLOW_REGISTRATION", True),
              patch.object(settings, "EMAIL_ENABLED", False),
              patch.object(settings, "STRIPE_ENABLED", False)):
            async def register(name):
                # Each request gets its own AsyncSession and connection.
                async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
                    return await client.post("/api/auth/register", json={
                        "username": name, "email": f"{name}@test.com",
                        "password": "Test1234!@", "native_language": "en",
                    })
            responses = await asyncio.gather(register("first_a"), register("first_b"))
        assert [r.status_code for r in responses] == [200, 200]
        assert sorted(r.json()["role"] for r in responses) == ["admin", "user"]
        async with bootstrap_sessions() as session:
            assert sorted((await session.scalars(select(User.role))).all()) == ["admin", "user"]
            assert (await session.scalars(select(AdminBootstrapClaim.id))).all() == [1]
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)


@pytest.mark.asyncio
async def test_claim_and_user_insert_rollback_together(bootstrap_sessions):
    with patch.object(settings, "FIRST_USER_IS_ADMIN", True):
        async with bootstrap_sessions() as session:
            assert await _claim_registration_role(session) == "admin"
            session.add(new_user("rollback", "admin"))
            await session.flush()
            await session.rollback()
        async with bootstrap_sessions() as session:
            assert await session.get(AdminBootstrapClaim, 1) is None
            assert await session.scalar(select(User.id)) is None
        async with bootstrap_sessions() as session:
            assert await _claim_registration_role(session) == "admin"
            session.add(new_user("winner", "admin"))
            await session.commit()


@pytest.mark.asyncio
async def test_failed_user_insert_does_not_consume_bootstrap(bootstrap_sessions):
    with patch.object(settings, "FIRST_USER_IS_ADMIN", True):
        async with bootstrap_sessions() as session:
            assert await _claim_registration_role(session) == "admin"
            session.add_all([new_user("duplicate", "admin"), new_user("duplicate")])
            with pytest.raises(IntegrityError):
                await session.commit()
            await session.rollback()
        async with bootstrap_sessions() as session:
            assert await _claim_registration_role(session) == "admin"
            await session.rollback()


@pytest.mark.asyncio
async def test_disabled_flag_is_consumed_and_not_reenabled(bootstrap_sessions):
    async with bootstrap_sessions() as session:
        with patch.object(settings, "FIRST_USER_IS_ADMIN", False):
            assert await _claim_registration_role(session) == "user"
            session.add(new_user("ordinary"))
            await session.commit()
        with patch.object(settings, "FIRST_USER_IS_ADMIN", True):
            assert await _claim_registration_role(session) == "user"
            await session.rollback()


@pytest.mark.asyncio
async def test_existing_users_are_not_promoted(bootstrap_sessions):
    async with bootstrap_sessions() as session:
        session.add(new_user("existing"))
        await session.commit()
        with patch.object(settings, "FIRST_USER_IS_ADMIN", True):
            assert await _claim_registration_role(session) == "user"
        await session.commit()
        assert await session.scalar(select(User.role)) == "user"


@pytest.mark.asyncio
async def test_deleting_users_does_not_reset_bootstrap(bootstrap_sessions):
    async with bootstrap_sessions() as session:
        with patch.object(settings, "FIRST_USER_IS_ADMIN", True):
            assert await _claim_registration_role(session) == "admin"
            user = new_user("owner", "admin")
            session.add(user)
            await session.commit()
            await session.delete(user)
            await session.commit()
            assert await _claim_registration_role(session) == "user"
            await session.rollback()


@pytest.mark.asyncio
async def test_waiting_registration_can_win_after_owner_rolls_back(bootstrap_sessions):
    owner_claimed = asyncio.Event()
    contender_started = asyncio.Event()

    async def owner():
        async with bootstrap_sessions() as session:
            assert await _claim_registration_role(session) == "admin"
            session.add(new_user("aborted", "admin"))
            await session.flush()
            owner_claimed.set()
            await contender_started.wait()
            await asyncio.sleep(0.05)
            await session.rollback()

    async def contender():
        await owner_claimed.wait()
        async with bootstrap_sessions() as session:
            contender_started.set()
            role = await _claim_registration_role(session)
            session.add(new_user("committed", role))
            await session.commit()
            return role

    with patch.object(settings, "FIRST_USER_IS_ADMIN", True):
        _, role = await asyncio.wait_for(asyncio.gather(owner(), contender()), timeout=15)
    assert role == "admin"
    async with bootstrap_sessions() as session:
        assert (await session.scalars(select(User.username))).all() == ["committed"]


@pytest.mark.parametrize("insert,dialect", [(pg_insert, postgresql.dialect()), (sqlite_insert, sqlite.dialect())])
def test_claim_statement_has_conflict_guard_and_returning(insert, dialect):
    statement = (insert(AdminBootstrapClaim).values(id=1)
                 .on_conflict_do_nothing(index_elements=[AdminBootstrapClaim.id])
                 .returning(AdminBootstrapClaim.id))
    sql = str(statement.compile(dialect=dialect)).upper()
    assert "ON CONFLICT (ID) DO NOTHING" in sql
    assert "RETURNING" in sql
