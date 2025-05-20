import aioredis

from config import REDIS_ADMIN_USERNAME, REDIS_ADMIN_PASSWORD, REDIS_URL

async def AioredisSession() -> aioredis.Redis:
    return await aioredis.from_url(
        "redis://" + REDIS_ADMIN_USERNAME + ":" + REDIS_ADMIN_PASSWORD + "@" + REDIS_URL,
        decode_responses=True)