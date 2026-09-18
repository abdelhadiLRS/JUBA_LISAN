import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings
from app.core.database import Base, get_db
from app.core.deps import get_redis
from app.main import app
from app.models.refresh_token import RefreshToken
from app.models.user import User
import app.models  # noqa: F401


@pytest.mark.asyncio
async def test_desktop_refresh_token_survives_database_restart(tmp_path, monkeypatch):
    db_path = tmp_path / "database" / "juba_lisan.db"
    db_path.parent.mkdir(parents=True)
    url = f"sqlite+aiosqlite:///{db_path}"

    monkeypatch.setattr(settings, "DESKTOP_MODE", True)
    monkeypatch.setattr(settings, "DATABASE_URL", url)
    monkeypatch.setattr(settings, "DATA_DIR", str(tmp_path))
    monkeypatch.setattr(settings, "REDIS_ENABLED", False)
    monkeypatch.setattr(settings, "REDIS_URL", "")
    monkeypatch.setattr(settings, "SECRET_KEY", "desktop-auth-test-secret-key-32-chars-min")
    monkeypatch.setattr(settings, "EMAIL_ENABLED", False)

    engine = create_async_engine(url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    async def override_db():
        async with session_factory() as session:
            yield session

    async def override_redis():
        yield None

    app.dependency_overrides[get_db] = override_db
    app.dependency_overrides[get_redis] = override_redis

    try:
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            register = await client.post(
                "/api/auth/register",
                json={
                    "username": "desktopuser",
                    "email": "desktop@example.com",
                    "password": "StrongPass1!",
                    "display_name": "Desktop User",
                    "native_language": "fr",
                    "target_language": "en-GB",
                },
            )
            assert register.status_code == 200, register.text
            registration_token = register.json()["access_token"]
            assert registration_token

            logout_after_register = await client.post("/api/auth/logout")
            assert logout_after_register.status_code == 200

            login = await client.post(
                "/api/auth/login",
                json={
                    "email": "desktop@example.com",
                    "password": "StrongPass1!",
                },
            )
            assert login.status_code == 200, login.text
            access_token = login.json()["access_token"]
            assert access_token
            assert access_token != registration_token
            set_cookie = login.headers.get("set-cookie", "").lower()
            assert "refresh_token=" in set_cookie
            assert "httponly" in set_cookie
            assert "secure" not in set_cookie

            await engine.dispose()
            engine = create_async_engine(url)
            session_factory = async_sessionmaker(engine, expire_on_commit=False)

            refresh = await client.post("/api/auth/refresh")
            assert refresh.status_code == 200, refresh.text
            new_access_token = refresh.json()["access_token"]
            assert new_access_token
            assert new_access_token != access_token

            me = await client.get(
                "/api/auth/me",
                headers={"Authorization": f"Bearer {new_access_token}"},
            )
            assert me.status_code == 200, me.text
            assert me.json()["email"] == "desktop@example.com"

            logout = await client.post("/api/auth/logout")
            assert logout.status_code == 200

            refresh_after_logout = await client.post("/api/auth/refresh")
            assert refresh_after_logout.status_code == 401

            async with session_factory() as session:
                user = await session.get(User, 1)
                assert user is not None
                token_count = await session.scalar(select(func.count(RefreshToken.id)))
                assert token_count == 0
    finally:
        app.dependency_overrides.pop(get_db, None)
        app.dependency_overrides.pop(get_redis, None)
        await engine.dispose()
