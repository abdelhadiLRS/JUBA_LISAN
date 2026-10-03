import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-for-pytest-ci-32b"
os.environ["RATE_LIMIT_ENABLED"] = "false"
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core.database import Base, get_db
from app.core.session_factory import get_session_factory, set_session_factory, reset_session_factory
from app.core.security import create_access_token
from app.main import app


def _set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.close()


@pytest.fixture(scope="session")
def test_engine():
    engine = create_async_engine(os.environ["DATABASE_URL"], echo=False)
    event.listen(engine.sync_engine, "connect", _set_sqlite_pragma)
    return engine


@pytest.fixture
def test_session_factory(test_engine):
    return async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_db(test_engine):
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(autouse=True)
async def shared_session_factory(test_session_factory):
    # Covers real routes, streaming persistence and captured background factories.
    # Direct service tests can still supply a factory explicitly.
    app.dependency_overrides[get_session_factory] = lambda: test_session_factory
    token = set_session_factory(test_session_factory)
    yield
    reset_session_factory(token)
    app.dependency_overrides.pop(get_session_factory, None)


@pytest_asyncio.fixture(autouse=True)
async def clear_sessions():
    yield


@pytest_asyncio.fixture
async def db_session(test_session_factory, setup_db):
    async with test_session_factory() as session:
        yield session


@pytest.fixture
def mock_redis():
    store = {}
    class MockRedis:
        async def setex(self, key, ttl, value):
            store[key] = value
        async def set(self, key, value, *args, **kwargs):
            if kwargs.get("nx") and key in store:
                return False
            store[key] = value
            return True
        async def get(self, key):
            return store.get(key)
        async def delete(self, key):
            return int(store.pop(key, None) is not None)
        async def exists(self, key):
            return int(key in store)
        async def getex(self, key):
            return store.get(key)
        async def scan(self, cursor, match=None, count=None):
            import fnmatch
            keys = list(store.keys())
            if match:
                keys = [key for key in keys if fnmatch.fnmatch(key, match)]
            return 0, keys
    return MockRedis()


@pytest_asyncio.fixture
async def client(db_session, mock_redis, test_session_factory):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_session_factory] = lambda: test_session_factory
    from app.routers.admin import get_redis as admin_get_redis
    from app.routers.assessment import get_redis as assessment_get_redis
    from app.routers.auth import get_redis as auth_get_redis
    from app.core.deps import get_redis as deps_get_redis
    for dependency in (admin_get_redis, assessment_get_redis, auth_get_redis, deps_get_redis):
        app.dependency_overrides[dependency] = lambda: mock_redis
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session):
    from app.core.security import hash_password
    from app.models.user import User
    from app.models.user_language import UserLanguage
    user = User(username="testuser", email="test@example.com", display_name="Test User", hashed_password=hash_password("testpass"),
        role="user", native_language="es", target_language="en-US", is_active=True)
    db_session.add(user)
    await db_session.flush()
    db_session.add(UserLanguage(user_id=user.id, target_language="en-US", is_active=True))
    await db_session.commit()
    await db_session.refresh(user)
    token = create_access_token(user.id, user.role)
    return user, {"Authorization":f"Bearer {token}"}


@pytest_asyncio.fixture
async def admin_user(db_session):
    from app.core.security import hash_password
    from app.models.user import User
    from app.models.user_language import UserLanguage
    user = User(username="admin", email="admin@example.com", display_name="Admin", hashed_password=hash_password("adminpass"),
        role="admin", native_language="en", target_language="en-US", is_active=True)
    db_session.add(user)
    await db_session.flush()
    db_session.add(UserLanguage(user_id=user.id, target_language="en-US", is_active=True))
    await db_session.commit()
    await db_session.refresh(user)
    return user, {"Authorization":f"Bearer {create_access_token(user.id,user.role)}"}


async def make_study_plan(db_session, *, user_id:int, target_language:str="en-US", **kwargs):
    from app.models.study_plan import StudyPlan
    from app.models.user_language import UserLanguage
    language = (await db_session.execute(select(UserLanguage).where(UserLanguage.user_id == user_id, UserLanguage.target_language == target_language))).scalar_one_or_none()
    if language is None:
        language = UserLanguage(user_id=user_id, target_language=target_language, is_active=False)
        db_session.add(language)
        await db_session.flush()
    plan = StudyPlan(user_id=user_id, user_language_id=language.id, target_language=target_language, **kwargs)
    db_session.add(plan)
    await db_session.flush()
    return plan


async def deactivate_active_plans(db_session, user_id:int, target_language:str="en-US") -> None:
    from app.models.study_plan import StudyPlan
    from app.models.user_language import UserLanguage
    language = (await db_session.execute(select(UserLanguage).where(UserLanguage.user_id == user_id, UserLanguage.target_language == target_language))).scalar_one_or_none()
    if language is None:
        return
    plans = (await db_session.execute(select(StudyPlan).where(StudyPlan.user_language_id == language.id, StudyPlan.is_active.is_(True)))).scalars().all()
    for plan in plans:
        plan.is_active = False
    await db_session.flush()


@pytest_asyncio.fixture
async def test_user_with_plan(test_user, db_session):
    from app.models.study_plan import StudyPlan
    from app.models.user_language import UserLanguage
    user, headers = test_user
    language = (await db_session.execute(select(UserLanguage).where(UserLanguage.user_id == user.id, UserLanguage.target_language == "en-US"))).scalar_one()
    db_session.add(StudyPlan(user_id=user.id, user_language_id=language.id, cefr_level="A1", target_language="en-US", goals=["grammar"],
        duration_weeks=4, days_per_week=4, current_unit="", generated_plan={}, is_active=True))
    await db_session.commit()
    return user, headers


@pytest_asyncio.fixture
async def user_language(test_user):
    return test_user
