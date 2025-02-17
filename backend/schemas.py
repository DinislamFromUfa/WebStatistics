from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserCreate(UserBase):pass

