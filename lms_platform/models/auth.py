from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserRole(str, Enum):
    TEACHER = 'teacher'
    STUDENT = 'student'


class UserBase(BaseModel):
    username: str
    email: Optional[str]
    role: UserRole


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
