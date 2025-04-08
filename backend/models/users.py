from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

BaseUsers = declarative_base()

class UsersScheme(BaseUsers):
    __tablename__ = "users"

    id = Column(Integer(), primary_key=True)

    username = Column(String())
    password = Column(String())

    token_session = Column(String())

    def __repr__(self) -> str:
        return f""" id={self.id}, username={self.username}, password={self.password} """