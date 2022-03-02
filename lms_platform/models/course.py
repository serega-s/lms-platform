from pydantic import BaseModel

class CourseBase(BaseModel):
    title: str
    slug: str
    description: str
    image: str


class CourseCreate(CourseBase):
    ...


class Course(CourseBase):
    id: int

    class Config:
        orm_mode = True
