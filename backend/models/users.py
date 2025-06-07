from pydantic import BaseModel


class UsersModel(BaseModel):
    username: str
    password: str
