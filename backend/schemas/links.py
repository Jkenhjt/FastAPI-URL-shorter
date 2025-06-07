from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

BaseLinks = declarative_base()


class LinksScheme(BaseLinks):
    __tablename__ = "links"

    id = Column(Integer(), primary_key=True)

    orig_url = Column(String())
    shorted_url = Column(String())

    create_date = Column(Integer())
    terminating_date = Column(Integer())

    owner = Column(String())

    def __repr__(self) -> str:
        return f""" id={self.id}, orig_url={self.orig_url}, shorted_url={self.shorted_url}, 
                    create_date={self.create_date}, terminating_date={self.terminating_date}, owner={self.owner} """
