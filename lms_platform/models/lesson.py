from pydantic import BaseModel

class LessonBase(BaseModel):
    ...


class Lesson(LessonBase):
    id: int

    class Config:
        orm_mode = True