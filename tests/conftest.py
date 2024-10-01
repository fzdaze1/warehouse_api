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
    # Создание всех таблиц в тестовой базе данных
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Удаление всех таблиц после завершения тестов
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(db):
    # Переопределение зависимости get_db для использования тестовой базы данных
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    # Удаление переопределения зависимости после завершения тестов
    app.dependency_overrides.pop(get_db)


@pytest.fixture(scope="session")
def redis_client():
    # Инициализация клиента Redis
    redis = Redis(host='localhost', port=6379)
    yield redis
    redis.close()  # Закрытие соединения Redis после завершения тестов


@pytest.fixture(scope="session")
def setup_cache(redis_client):
    # Инициализация кэша FastAPI перед запуском тестов
    FastAPICache.init(RedisBackend(redis_client), prefix='fastapi-cache')


@pytest.fixture(scope="session", autouse=True)
def init_cache(setup_cache):
    """Автоматически инициализирует кэш для всех тестов."""
    pass
