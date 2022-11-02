from enum import Enum
from typing import Optional

from pydantic import BaseModel


class UserRole(str, Enum):
    """
        Two types of user role choice
    """
    TEACHER = 'teacher'
    STUDENT = 'student'


class UserBase(BaseModel):
    """
        Base structure of User model object
    """
    email: str
    role: UserRole


class UserCreate(UserBase):
    """
        Create User object
    """
    password: str


class User(UserBase):
    """
        Initial User object
    """
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
