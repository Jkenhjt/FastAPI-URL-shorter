from fastapi import APIRouter, HTTPException, Request, Response

from slowapi import Limiter
from slowapi.util import get_remote_address

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from database.database import SessionUsers

from models.users import UsersScheme

from schemas.users import UsersRecieve

from security.jwt import create_token
from security.bcrypt_secure import bcrypt_securing


routerUsers = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@routerUsers.post("/register")
@limiter.limit("10/minute")
async def register(account: UsersRecieve, request: Request, dbSession: SessionUsers):
    account_secured = bcrypt_securing(account.username)

    accountDB = await dbSession.execute(select(UsersScheme).where(UsersScheme.username == account_secured).limit(1))

    try:
        if(accountDB.scalar_one() != None):
            raise HTTPException(status_code=406, detail="User already exist")
    except NoResultFound:
        pass

    db_new_user = UsersScheme(
        username=account_secured,
        password=bcrypt_securing(account.password)
    )

    dbSession.add(db_new_user)
    await dbSession.commit()

@routerUsers.post("/login")
@limiter.limit("10/minute")
async def login(account: UsersRecieve, request: Request, response: Response, dbSession: SessionUsers):
    try:
        dbAccount = (
            await dbSession.execute(
                select(UsersScheme)
                .where(UsersScheme.username == bcrypt_securing(account.username))
                .limit(1)
            )
        ).scalar_one()

        if(dbAccount.password != bcrypt_securing(account.password)):
            raise NoResultFound
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Username or password is incorrect")

    token: str = create_token(dbAccount.id)

    await dbSession.execute(update(UsersScheme).where(UsersScheme.id == dbAccount.id).values(token_session=token))
    await dbSession.commit()

    return response.set_cookie(key="session", value=token)