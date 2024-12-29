import pytest_asyncio
from fakeredis import FakeAsyncRedis
from sqlalchemy.ext.asyncio import (async_sessionmaker,
                                    create_async_engine,
                                    AsyncEngine,
                                    AsyncSession)
from sqlalchemy.pool import StaticPool
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api import router as api_router
from cache.redis import get_redis
from db import get_session
from models import BaseOrm


@pytest_asyncio.fixture(scope="session")
async def engine_session(tmp_path_factory) -> tuple[
    AsyncEngine, async_sessionmaker[AsyncSession]
]:
    # SQLite database URL for testing
    db_path = tmp_path_factory.getbasetemp() / "test.sqlite"
    SQLITE_DATABASE_URL = f"sqlite+aiosqlite:///{db_path}"

    # Create a SQLAlchemy engine
    engine = create_async_engine(
        SQLITE_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create a sessionmaker to manage sessions
    TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False,
                                             bind=engine)

    # Create tables in the database
    async with engine.begin() as conn:
        await conn.run_sync(BaseOrm.metadata.create_all)

    return engine, TestingSessionLocal


@pytest_asyncio.fixture(scope="session")
async def db_session(engine_session):
    """Create a new database session with a rollback at the end of the test."""
    connection = await engine_session[0].connect()
    session = engine_session[1](bind=connection)
    yield session
    await session.close()
    await connection.close()


@pytest_asyncio.fixture(scope="session")
async def test_client(db_session):
    """Create a test client that uses the override_get_db
    fixture to return a session."""
    async def override_get_session():
        try:
            yield db_session
        finally:
            await db_session.close()

    def override_get_redis():
        redis = FakeAsyncRedis()
        return redis

    app = FastAPI()
    app.include_router(
        api_router,
        prefix="/api"
    )

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_redis] = override_get_redis
    with TestClient(app, base_url="http://127.0.0.1:8000/api") as test_client:
        yield test_client
