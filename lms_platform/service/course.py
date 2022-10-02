from typing import Any, Optional

from fastapi import Depends
from lms_platform.utils import copy_fileobj
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.course import Course, CourseCreate, CourseUpdate, FullCourse
from ..statuses.exceptions import HTTP403Exception, HTTP404Exception


class CourseService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_course(self, id: Optional[int] = None, slug: Optional[str] = None):
        course = self.session.query(tables.Course)
        if id:
            course = course.filter_by(id=id)
        elif slug:
            course = course.filter_by(slug=slug)

        return course

    def get_course(self, slug: str) -> FullCourse:
        if course := self._get_course(slug=slug).first():
            return course
        else:
            raise HTTP404Exception()

    def get_courses(self) -> list[Course]:
        return self.session.query(tables.Course).all()

    def create_course(self, user_id: int, course_data: CourseCreate, file: Any) -> Course:
        #
        copy_fileobj(course_data.image, file.file)

        course = tables.Course(**course_data.dict(), user_id=user_id)

        self.session.add(course)
        self.session.commit()

        return course

    def edit_course(
        self,
        user_id: int,
        slug: str,
        course_data: CourseUpdate,
        file: Optional[Any] = None
    ) -> Course:
        course = self._get_course(slug=slug).first()

        if user_id != course.user_id:
            raise HTTP403Exception()

        if not course:
            raise HTTP404Exception()

        if file:
            copy_fileobj(course_data.image, file.file)
        if not course_data.image:
            course_data.image = course.image

        for field, value in course_data:
            setattr(course, field, value)

        self.session.commit()

        return course

    def delete_course(self, id: int, user_id: int):
        course = self._get_course(id=id)

        if course.first() is None:
            raise HTTP404Exception()

        if user_id != course.first().user_id:
            raise HTTP403Exception()

        course.delete(synchronize_session=False)
        self.session.commit()
