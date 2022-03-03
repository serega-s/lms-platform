from typing import Optional
from pydantic import BaseModel


class ProfileBase(BaseModel):
    full_name: str
    phone_number: str
    bio: str
    image: Optional[str] = None


class ProfileCreate(ProfileBase):
    ...


class ProfileUpdate(ProfileBase):
    ...


class Profile(ProfileBase):
    id: int

    class Config:
        orm_mode = True


# class Student(ProfileBase):
#     id: int

#     class Config:
#         orm_mode = True


# class StudentCreate(ProfileBase):
#     ...
