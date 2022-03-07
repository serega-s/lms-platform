from typing import Optional
from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    slug: str
    short_description: str
    description: str
    image: Optional[str] = None


class CourseCreate(CourseBase):
    ...


class CourseUpdate(CourseBase):
    ...


class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True
