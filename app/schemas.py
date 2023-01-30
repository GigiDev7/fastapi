from pydantic import BaseModel, EmailStr
from typing import Optional, Any, List
from pydantic.types import conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    email: str
    id: int

    class Config:
        orm_mode = True


class PostResponse(PostBase):
    id: int
    user: UserResponse
    votes: List

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    token: str


class TokenData(BaseModel):
    user_id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    direction: conint(ge=0, le=1)
