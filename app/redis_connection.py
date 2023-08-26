import redis.asyncio as redis


async def get_redis():
    # return await redis.Redis(host='localhost', port=6379, decode_responses=True, )
    return await redis.Redis(host='restaurant_redis', port=6379, decode_responses=True, )
