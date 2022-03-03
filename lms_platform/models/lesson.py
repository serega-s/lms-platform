from pydantic import BaseModel

class LessonBase(BaseModel):
    title: str
    slug: str
    short_description: str
    description: str
    image: str

class LessonCreate(LessonBase):
    ...


class Lesson(LessonBase):
    id: int

    class Config:
        orm_mode = True