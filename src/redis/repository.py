from datetime import timedelta

from pydantic import BaseModel

from redis import asyncio as aioredis  # type: ignore
from src.settings import settings
from src.utils import object_to_str, str_to_object


class RedisRepository:
    def __init__(self):
        self._client = aioredis.Redis(
            host=settings.redis_host,
            port=settings.redis_port,
        )

    @staticmethod
    async def _generate_key(keys: list) -> str:
        result = ''
        for key in keys:
            result += str(key)

        return result

    async def get_data(
            self,
            keys: list,
            model: type[BaseModel]
    ) -> list[BaseModel] | None:
        data = await self._client.get(
            name=await self._generate_key(keys)
        )
        if data is not None:
            return str_to_object(data, model)

        return None

    async def set_data(
            self,
            keys: list,
            data: list[BaseModel],
            expire: int | timedelta | None = None
    ) -> bool:
        return await self._client.set(
            name=await self._generate_key(keys),
            value=object_to_str(data),
            ex=expire
        )

    async def invalidate_cache(
            self,
            keys: list
    ) -> int:
        names = await self._client.scan(
            match=f'*{await self._generate_key(keys)}*'
        )
        if names[-1]:
            return await self._client.delete(
                *names[-1]
            )
        return 0

    async def invalidate_caches(
            self,
            caches_keys: list[list]
    ) -> int:
        keys = [
            await self._generate_key(key) for key in caches_keys
        ]
        names = []
        for key in keys:
            name = await self._client.scan(
                match=f'*{key}*'
            )
            if name[-1]:
                names.extend(name[-1])

        if names:
            return await self._client.delete(
                *names
            )

        return 0
