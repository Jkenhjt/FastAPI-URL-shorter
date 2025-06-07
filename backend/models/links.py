from pydantic import BaseModel


class LinksModel(BaseModel):
    url: str
    time_ending: str
