import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import Redis

# URL базы данных для тестирования
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Создание движка для базы данных
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_db)


@pytest.fixture(scope="session")
def redis_client():
    redis = Redis(host='localhost', port=6379)
    yield redis
    redis.close()


@pytest.fixture(scope="session")
def setup_cache(redis_client):
    FastAPICache.init(RedisBackend(redis_client), prefix='fastapi-cache')


@pytest.fixture(scope="session", autouse=True)
def init_cache(setup_cache):
    pass
