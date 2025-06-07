from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from config import POSTGRES_USER, POSTGRES_PASS, POSTGRES_URL, POSTGRES_DB_PATH


SQLALCHEMY_DATABASE_USERS_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_URL}/{POSTGRES_DB_PATH}"
SQLALCHEMY_DATABASE_LINKS_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASS}@{POSTGRES_URL}/{POSTGRES_DB_PATH}"
UsersEngine = create_async_engine(SQLALCHEMY_DATABASE_USERS_URL, echo=True, future=True)
LinksEngine = create_async_engine(SQLALCHEMY_DATABASE_LINKS_URL, echo=True, future=True)


async def CreateSessionUsersDB():
    async with AsyncSession(UsersEngine, expire_on_commit=False) as session:
        yield session


async def CreateSessionLinksDB():
    async with AsyncSession(LinksEngine, expire_on_commit=False) as session:
        yield session


SessionUsers = Annotated[AsyncSession, Depends(CreateSessionUsersDB)]
SessionLinks = Annotated[AsyncSession, Depends(CreateSessionLinksDB)]
