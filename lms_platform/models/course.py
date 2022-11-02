from typing import Optional

from pydantic import BaseModel

from .lesson import Lesson


class CourseBase(BaseModel):
    """
        Base structure of Course model object
    """
    title: str
    slug: str
    short_description: str
    description: str
    image: Optional[str] = None


class CourseCreate(CourseBase):
    """
        Create Course object
    """
    ...


class CourseUpdate(CourseBase):
    """
        Update Course object
    """
    ...


class FullCourse(CourseBase):
    """
        Full course object with lessons
    """
    id: int
    lessons: list[Lesson]

    class Config:
        orm_mode = True


class Course(CourseBase):
    """
        Initial Course object 
    """
    id: int

    class Config:
        orm_mode = True
