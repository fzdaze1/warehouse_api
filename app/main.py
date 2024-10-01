from fastapi import FastAPI
from .api import products, orders
from redis import Redis
from fastapi_cache import FastAPICache
from contextlib import asynccontextmanager
from fastapi_cache.backends.redis import RedisBackend

app = FastAPI()

redis = Redis(host='redis', port=6379)


@asynccontextmanager
async def lifespan(app: FastAPI):
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield
    await FastAPICache.clear()

app.add_event_handler("startup", lambda: FastAPICache.init(
    RedisBackend(redis), prefix='fastapi-cache'))
app.add_event_handler("shutdown", lambda: FastAPICache.clear())

app.include_router(products.router, prefix="/api/v1")
app.include_router(orders.router, prefix="/api/v1")
