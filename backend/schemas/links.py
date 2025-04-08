from pydantic import BaseModel

class LinksRecieve(BaseModel):
    url: str
    time_ending: str