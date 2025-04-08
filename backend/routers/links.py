import time

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse

from slowapi import Limiter
from slowapi.util import get_remote_address

from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound

from database.database import SessionLinks, SessionUsers

from schemas.links import LinksRecieve

from models.users import UsersScheme
from models.links import LinksScheme

from config import *


routerLinks = APIRouter()

limiter = Limiter(key_func=get_remote_address)


async def check_token(token: str, dbSession: SessionUsers):
    result = await dbSession.execute(select(UsersScheme).where(UsersScheme.token_session == token).limit(1))

    accountData = result.scalar_one()

    if(accountData == None):
        raise HTTPException(status_code=401, detail="Login to account before using shorter")

    return accountData


@routerLinks.get("/")
@limiter.limit("120/minute")
async def index(request: Request):
    raise HTTPException(status_code=404, detail="Have not done so yet")

@routerLinks.post("/create_link")
@limiter.limit("120/minute")
async def creating_link(linksRecieve: LinksRecieve, request: Request, dbSession: SessionUsers, dbLinks: SessionLinks):
    try:
        accountData = await check_token(request.cookies.get("session"), dbSession)
    except NoResultFound:
        raise HTTPException(status_code=401, detail="Register first before creating shortlinks")

    def convert_to_seconds(time: str) -> int:
        if(len(list(filter(str.isalpha, time))) > 1):
            raise HTTPException(status_code=404, detail="Error time")

        match time[-1]:
            case 'd':
                return int(time[:-1]) * 24 * 60 * 60
            case 'h':
                return int(time[:-1]) * 60 * 60
            case 'm':
                return int(time[:-1]) * 60
            case 's':
                return int(time[:-1])
            case _:
                raise HTTPException(status_code=404, detail="Error time")

    dbLink = LinksScheme(
        orig_url=linksRecieve.url,
        shorted_url=(DOMAIN + "/" + hex(int(time.time() * 1e6))[2::].upper()),

        create_date=int(time.time()),
        terminating_date=int(time.time())+convert_to_seconds(linksRecieve.time_ending),

        owner=hex(accountData.id)
    )

    dbLinks.add(dbLink)
    await dbLinks.commit()

    await request.app.state.async_redis_session.set(dbLink.shorted_url, dbLink.orig_url)

    return {"url": dbLink.shorted_url}

@routerLinks.get("/{shorted_url_id}")
@limiter.limit("60000/minute")
async def redirecting_to(shorted_url_id: str, request: Request, dbLinks: SessionLinks):
    try:
        cached_url = await request.app.state.async_redis_session.get((DOMAIN + "/" + shorted_url_id))
        if(cached_url != None):
            return RedirectResponse(url=cached_url, status_code=308)


        shortedUrl = (
            await dbLinks.execute(
                select(LinksScheme)
                .where(LinksScheme.shorted_url == (DOMAIN + "/" + shorted_url_id))
            )
        ).scalar_one()

        return RedirectResponse(url=shortedUrl.orig_url, status_code=308)
    except:
        raise HTTPException(status_code=404, detail="Url not found")

@routerLinks.delete("/{shorted_url_id}")
@limiter.limit("120/minute")
async def delete_shorted_url(shorted_url_id: str, request: Request, dbSession: SessionUsers, dbLinks: SessionLinks):
    try:
        accountData = await check_token(request.cookies.get("session"), dbSession)

        if(
            (
                await dbLinks.execute(
                    select(LinksScheme)
                    .where(LinksScheme.owner == hex(accountData.id))
                    .where(LinksScheme.shorted_url == (DOMAIN + "/" + shorted_url_id))
                )
            ).scalar_one() == None
        ):
            raise NoResultFound
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Url does not exist or you haven't permissions for delete")


    await dbLinks.execute(
        delete(LinksScheme)
        .where(LinksScheme.owner == hex(accountData.id))
        .where(LinksScheme.shorted_url == (DOMAIN + "/" + shorted_url_id))
    )
    await dbLinks.commit()

    await request.app.state.async_redis_session.delete((DOMAIN + "/" + shorted_url_id))

    return "Deleting successful!"