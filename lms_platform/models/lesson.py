from pydantic import BaseModel


class LessonBase(BaseModel):
    """
        Base structure of Lesson model object
    """
    title: str
    slug: str
    short_description: str
    description: str
    draft: bool


class LessonCreate(LessonBase):
    """
        Create Lesson object
    """
    ...


class LessonUpdate(LessonBase):
    """
        Update Lesson object
    """
    ...


class Lesson(LessonBase):
    """
        Initial Lesson object
    """
    id: int
    course_id: int

    class Config:
        orm_mode = True
