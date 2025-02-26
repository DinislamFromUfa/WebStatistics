from pydantic import BaseModel, Field


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

