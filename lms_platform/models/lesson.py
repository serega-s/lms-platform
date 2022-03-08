from pydantic import BaseModel

class LessonBase(BaseModel):
    title: str
    slug: str
    short_description: str
    description: str
    draft: bool

class LessonCreate(LessonBase):
    ...

class LessonUpdate(LessonBase):
    ...


class Lesson(LessonBase):
    id: int
    course_id: int

    class Config:
        orm_mode = True