from fastapi import HTTPException

from sqlalchemy import select

from database.database import SessionUsers

from schemas.users import UsersScheme


async def check_token(token: str, dbSession: SessionUsers):
    result = await dbSession.execute(
        select(UsersScheme).where(UsersScheme.token_session == token)
    )

    accountData = result.scalar_one()

    if accountData == None:
        raise HTTPException(
            status_code=401, detail="Login to account before using shorter"
        )

    return accountData
