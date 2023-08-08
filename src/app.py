import aioredis
from fastapi import APIRouter, FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.dish import dish_router
from src.menu import menu_router
from src.settings import settings
from src.submenu import submenu_router

app = FastAPI()

router = APIRouter(
    prefix='/api/v1'
)


@app.on_event('startup')
async def startup():
    redis = aioredis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
    )
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


router.include_router(menu_router.router)
router.include_router(submenu_router.router)
router.include_router(dish_router.router)

app.include_router(router)
