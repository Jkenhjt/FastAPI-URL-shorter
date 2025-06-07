import asyncio
import pytest

import bcrypt

import authlib

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import UsersEngine, LinksEngine

from schemas.users import UsersScheme
from schemas.links import LinksScheme

from redis.aioredis_client import AioredisSession

from models.users import UsersModel
from models.links import LinksModel

from security.jwt import create_token, key
from security.bcrypt_secure import bcrypt_securing


# Database Module


class TestDatabase:
    user: UsersScheme = UsersScheme(
        username="admins", password=b"admins", token_session="admintoken"
    )

    link: LinksScheme = LinksScheme(
        orig_url="https://www.test.com",
        shorted_url="https://www.shorttest.com/MF43N9VR8",
        create_date=9250,
        terminating_date=989043,
        owner="testuser",
    )

    @pytest.mark.asyncio
    async def test_users_database(self):
        async with AsyncSession(UsersEngine, expire_on_commit=False) as session:
            session.add(self.user)
            await session.commit()

            result = (
                await session.execute(
                    select(UsersScheme)
                    .where(UsersScheme.username == "admins")
                    .where(UsersScheme.password == b"admins")
                    .limit(1)
                )
            ).scalar_one()

            assert result.username == "admins"
            assert result.password == b"admins"
            assert result.token_session == "admintoken"

    @pytest.mark.asyncio
    async def test_links_database(self):
        async with AsyncSession(LinksEngine, expire_on_commit=False) as session:
            session.add(self.link)
            await session.commit()

            result = (
                await session.execute(
                    select(LinksScheme)
                    .where(LinksScheme.orig_url == "https://www.test.com")
                    .where(LinksScheme.owner == "testuser")
                    .limit(1)
                )
            ).scalar_one()

            assert result.orig_url == "https://www.test.com"
            assert result.shorted_url == "https://www.shorttest.com/MF43N9VR8"
            assert result.create_date == 9250
            assert result.terminating_date == 989043
            assert result.owner == "testuser"


# Models Module


class TestModels:
    def test_user_model(self):
        test_model = UsersScheme()

        assert test_model.id == None
        assert test_model.username == None
        assert test_model.password == None
        assert test_model.token_session == None

        test_model_2 = UsersScheme(
            username="testusername",
            password="testpass",
            token_session="testtoken",
        )

        assert test_model_2.username == "testusername"
        assert test_model_2.password == "testpass"
        assert test_model_2.token_session == "testtoken"

    def test_user_model2(self):
        test_model = LinksScheme()

        assert test_model.id == None
        assert test_model.orig_url == None
        assert test_model.shorted_url == None
        assert test_model.create_date == None
        assert test_model.terminating_date == None
        assert test_model.owner == None

        test_model_2 = LinksScheme(
            orig_url="https://www.test.com",
            shorted_url="https://www.shorttest.com/MF43N9VR8",
            create_date=925049832,
            terminating_date=98904328491,
            owner="testuser",
        )

        assert test_model_2.orig_url == "https://www.test.com"
        assert test_model_2.shorted_url == "https://www.shorttest.com/MF43N9VR8"
        assert test_model_2.create_date == 925049832
        assert test_model_2.terminating_date == 98904328491
        assert test_model_2.owner == "testuser"


# Redis Module


@pytest.mark.asyncio
async def test_redis_session():
    aioredis_model = await AioredisSession()
    async_session_model = aioredis_model

    assert await async_session_model.set("test", "test") == True
    assert (
        await async_session_model.hset(
            "test_dict", mapping={"test": "ok", "aio": "redis", "pytest": "good"}
        )
        == 3
    )

    assert await async_session_model.get("test") == "test"
    assert await async_session_model.hgetall("test_dict") == {
        "test": "ok",
        "aio": "redis",
        "pytest": "good",
    }


# Schemas Module


def test_user_scheme():
    test_scheme = UsersModel(username="testusername", password="testpass")

    assert test_scheme.username == "testusername"
    assert test_scheme.password == "testpass"


def test_link_scheme():
    test_scheme = LinksModel(url="http://test.com", time_ending="7d")

    assert test_scheme.url == "http://test.com"
    assert test_scheme.time_ending == "7d"


# Security Module


def test_bcrypt():
    password: str = "password"
    hashed_password: bytes = bcrypt_securing(password)

    assert bcrypt.checkpw(password.encode(), hashed_password) == True


def test_jwt():
    token_created = create_token(123456, "username")

    token_decoded = authlib.jose.jwt.decode(token_created, key)

    assert token_decoded["sub"] == 123456
    assert token_decoded["name"] == "username"
