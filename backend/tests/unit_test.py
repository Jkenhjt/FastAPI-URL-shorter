import asyncio
import pytest

import requests

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import UsersEngine, LinksEngine

from models.users import UsersScheme
from models.links import LinksScheme

from redis.aioredis_client import AioredisSession

from schemas.users import UsersRecieve
from schemas.links import LinksRecieve

from security.jwt import create_token
from security.bcrypt_secure import bcrypt_securing




# Database Module

class TestDatabase():
    user: UsersScheme = UsersScheme(
        username="admins",
        password="admins",
        token_session="admintoken"
    )

    link: LinksScheme = LinksScheme(
        orig_url="https://www.test.com",
        shorted_url="https://www.shorttest.com/MF43N9VR8",
        create_date=9250,
        terminating_date=989043,
        owner="testuser"
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
                    .where(UsersScheme.password == "admins")
                    .limit(1)
                )
            ).scalar_one()

            assert result.username == "admins"
            assert result.password == "admins"
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

class TestModels():
    username: str = "testusername"
    password: str = "testpass"
    token_session: str = "testtoken"

    orig_url: str = "https://www.test.com"
    shorted_url: str = "https://www.shorttest.com/MF43N9VR8"
    create_date: int = 925049832
    terminating_date: int = 98904328491
    owner: str = "testuser"

    def test_user_model(self):
        test_model = UsersScheme()

        assert test_model.id == None
        assert test_model.username == None
        assert test_model.password == None
        assert test_model.token_session == None

        test_model_2 = UsersScheme(
            username=self.username,
            password=self.password,
            token_session=self.token_session
        )

        assert test_model_2.username == self.username
        assert test_model_2.password == self.password
        assert test_model_2.token_session == self.token_session

    def test_user_model(self):
        test_model = LinksScheme()

        assert test_model.id == None
        assert test_model.orig_url == None
        assert test_model.shorted_url == None
        assert test_model.create_date == None
        assert test_model.terminating_date == None
        assert test_model.owner == None

        test_model_2 = LinksScheme(
            orig_url=self.orig_url,
            shorted_url=self.shorted_url,
            create_date=self.create_date,
            terminating_date=self.terminating_date,
            owner=self.owner
        )

        assert test_model_2.orig_url == self.orig_url
        assert test_model_2.shorted_url == self.shorted_url
        assert test_model_2.create_date == self.create_date
        assert test_model_2.terminating_date == self.terminating_date
        assert test_model_2.owner == self.owner



# Redis Module

@pytest.mark.asyncio
async def test_redis_session():
    aioredis_model = await AioredisSession()
    async_session_model = aioredis_model

    assert await async_session_model.set("test", "test") == True
    assert await async_session_model.hset("test_dict", mapping={"test": "ok", "aio": "redis", "pytest": "good"}) == 3

    assert await async_session_model.get("test") == "test"
    assert await async_session_model.hgetall("test_dict") == {"test": "ok", "aio": "redis", "pytest": "good"}



# Routers Module


cookies: str = ""

shorted_url: str = ""

def test_account_register():
    username: str = "admin"
    password: str = "admin"

    payload = {
        "username": username,
        "password": password
    }

    resp = requests.post("http://0.0.0.0:8000/register", json=payload)

    assert resp.status_code == 200

    assert resp.json()["username"] == username
    assert resp.json()["password"] == password


def test_account_login():
    username: str = "admin"
    password: str = "admin"

    payload = {
        "username": username,
        "password": password
    }

    resp = requests.post("http://0.0.0.0:8000/login", json=payload)

    assert resp.status_code == 200

    assert resp.cookies.get_dict()["session"] != None

    global cookies
    cookies = resp.cookies.get_dict()["session"]

    return

def test_create_link():
    org_url: str = "https://www.google.com"

    payload = {
        "url": org_url,
        "time_ending": "7d"
    }

    resp = requests.post("http://0.0.0.0:8000/create_link", json=payload, cookies={"session": cookies})

    assert resp.status_code == 200

    assert "http://0.0.0.0:8000/" in resp.json()["url"]

    global shorted_url
    shorted_url = resp.json()["url"]

def test_get_link():
    resp = requests.get(shorted_url)
    assert resp.status_code == 200

def test_delete_link():
    resp = requests.delete(shorted_url, cookies={"session": cookies})
    assert resp.status_code == 200

# Schemas Module

def test_user_scheme():
    test_scheme = UsersRecieve(
        username="testusername",
        password="testpass"
    )

    assert test_scheme.username == "testusername"
    assert test_scheme.password == "testpass"

def test_link_scheme():
    test_scheme = LinksRecieve(
        url="http://test.com",
        time_ending="7d"
    )

    assert test_scheme.url == "http://test.com"
    assert test_scheme.time_ending == "7d"



# Security Module

def test_jwt():
    token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOjEyMzQ1NiwiZXhwIjotMX0.XH53II-RWiUZXNuThNFtYgVOjVf1U2XQw6W_V2Qzyyc"

    assert create_token(123456) == token

def test_bcrypt_securing():
    token: str = "e82c477f3a388c437399f46de2046856c6dd31fecf6f5dbc0f7ca863952a7745987a37956e66b7789ed6420532e8fe8bd392527f51708369b2f184eef696ce8b"

    assert bcrypt_securing("test") == token