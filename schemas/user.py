from pydantic import BaseModel

class Users (BaseModel):
    username: int
    password: str
