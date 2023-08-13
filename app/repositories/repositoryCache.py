from redis.asyncio import Redis


async def set_cache(key: str, value: str, redis: Redis) -> None:
    await redis.set(key, value, 120)


async def get_cache(key: str, redis: Redis):
    result = await redis.get(key)
    return result


async def del_cache(key: str, redis: Redis) -> None:
    await redis.delete(key)


async def flush(redis: Redis) -> None:
    await redis.flushall()
