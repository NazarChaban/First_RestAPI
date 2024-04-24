from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field
from pydantic import EmailStr


# Tags
class TagModel(BaseModel):
    name: str = Field(max_length=25)


class TagResponse(TagModel):
    id : int

    class Config:
        orm_model = True


# Notes
class NoteBase(BaseModel):
    title: str = Field(max_length=50)
    description: str = Field(max_length=150)


class NoteModel(NoteBase):
    tags: List[int]


class NoteUpdate(NoteModel):
    done: bool


class NoteStatusUpdate(BaseModel):
    done: bool


class NoteResponse(NoteModel):
    id: int
    created_at: datetime
    tags: List[TagResponse]

    class Config:
        orm_model = True


# Users
class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_model = True


class UserResponse(BaseModel):
    user: UserDb
    detail: str = 'User created successfully'


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


# Email
class RequestEmail(BaseModel):
    email: EmailStr
