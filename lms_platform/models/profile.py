from typing import Optional

from pydantic import BaseModel


class ProfileBase(BaseModel):
    """
        Base structure of Profile model object
    """
    full_name: str
    phone_number: str
    bio: str
    image: Optional[str] = None


class ProfileCreate(ProfileBase):
    """
        Create Profile object
    """
    ...


class ProfileUpdate(ProfileBase):
    """
        Update Profile object
    """
    ...


class Profile(ProfileBase):
    """
        Initial Profile object
    """
    id: int

    class Config:
        orm_mode = True
