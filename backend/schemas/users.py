from pydantic import BaseModel

class UsersRecieve(BaseModel):
    username: str
    password: str