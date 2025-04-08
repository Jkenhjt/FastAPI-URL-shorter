from fastapi import FastAPI

from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware

from database.database import UsersEngine, LinksEngine

from routers.links import routerLinks
from routers.users import routerUsers

from models.links import BaseLinks
from models.users import BaseUsers

import sqlalchemy

from redis.aioredis_client import AioredisSession


app = FastAPI(
    title="URL shortener",
    summary="Simple URL shortener",
    description="Pet project that creates a shortened URL that redirects to target",
    version="1.0.0",
    terms_of_service="",
    contact={
        "name": None,
        "url": "https://github.com/Jkenhjt",
        "email": None
    },
    license_info={
        "name": "MIT License",
        "url": "https://spdx.org/licenses/MIT.html"
    },
    docs_url="/documentation",
    redoc_url=None
)
app.add_middleware(GZipMiddleware, minimum_size=500, compresslevel=9)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


app.include_router(routerUsers)
app.include_router(routerLinks)


@app.on_event("startup")
async def start():
    async with UsersEngine.begin() as conn:
        try:
            await conn.run_sync(BaseUsers.metadata.create_all)
        except:
            pass


    async with LinksEngine.begin() as conn:
        try:
            await conn.run_sync(BaseLinks.metadata.create_all)
        except:
            pass

    app.state.async_redis = await AioredisSession()
    app.state.async_redis_session = app.state.async_redis
    
    await UsersEngine.dispose()
    await LinksEngine.dispose()

@app.on_event("shutdown")
async def stop():
    await app.state.async_redis_session.close()