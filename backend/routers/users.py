from fastapi import APIRouter, HTTPException, Request, Response

from slowapi import Limiter
from slowapi.util import get_remote_address

from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound

from database.database import SessionUsers

from schemas.users import UsersScheme

from models.users import UsersModel

from security.jwt import create_token
from security.bcrypt_secure import bcrypt_securing


routerUsers = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@routerUsers.post("/register", tags=["Account"])
@limiter.limit("10/minute")
async def register(account: UsersModel,
                   request: Request,
                   dbSession: SessionUsers) -> None:
    try:
        account_result = await dbSession.execute(select(UsersScheme)
                                                .where(UsersScheme.username == account.username))
        if(account_result.scalar_one() != None):
            raise HTTPException(status_code=406,
                                detail="User already exist")
    except NoResultFound:
        pass

    db_new_user = UsersScheme(
        username=account.username,
        password=bcrypt_securing(account.password)
    )

    dbSession.add(db_new_user)
    await dbSession.commit()

    return Response(status_code=200)

@routerUsers.post("/login", tags=["Account"])
@limiter.limit("10/minute")
async def login(account: UsersModel,
                request: Request,
                response: Response,
                dbSession: SessionUsers) -> None:
    try:
        dbAccount = (
            await dbSession.execute(
                select(UsersScheme)
                .where(UsersScheme.username == account.username)
            )
        ).scalar_one()

        if(dbAccount.password != bcrypt_securing(account.password)):
            raise NoResultFound
    except NoResultFound:
        raise HTTPException(status_code=404,
                            detail="Username or password is incorrect")

    token: str = create_token(dbAccount.id)

    await dbSession.execute(update(UsersScheme)
                           .where(UsersScheme.id == dbAccount.id)
                           .values(token_session=token))
    await dbSession.commit()

    return response.set_cookie(key="session",
                               value=token)