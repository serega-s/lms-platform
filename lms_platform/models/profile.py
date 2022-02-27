from pydantic import BaseModel


class ProfileBase(BaseModel):
    full_name: str
    phone_number: str
    bio: str
    image: str


class ProfileCreate(ProfileBase):
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
