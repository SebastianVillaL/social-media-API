#Python
from typing import Optional
from datetime import datetime
#Pydantic
from pydantic import BaseModel, EmailStr

class Post(BaseModel): #This is a schema(to format our posts with the following criteria)
    title: str
    content: str
    published: bool = True
    class Config:
        orm_mode = True


class PostOut(Post):
    id: int
    created_at: datetime


class User(BaseModel): #This is a schema(to format our users with the following criteria)
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    toke_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
