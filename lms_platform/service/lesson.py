from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.lesson import Lesson, LessonCreate, LessonUpdate
from ..statuses.exceptions import HTTP403Exception, HTTP404Exception


class LessonService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_course(self, id: Optional[int] = None, slug: Optional[str] = None):
        course = self.session.query(tables.Course)
        if id:
            course = course.filter_by(id=id)
        elif slug:
            course = course.filter_by(slug=slug)

        return course

    def _get_lesson(
        self,
        course_id: Optional[int] = None,
        id: Optional[int] = None,
        slug: Optional[str] = None
    ):
        lesson = self.session.query(
            tables.Lesson)
        if id:
            lesson = lesson.filter_by(id=id)
        elif slug:
            lesson = lesson.filter_by(slug=slug)
        if course_id:
            lesson = lesson.filter_by(course_id=course_id)

        return lesson

    def get_lesson(self, course_slug: str, lesson_slug: str) -> Lesson | None:
        course = self._get_course(slug=course_slug).first()
        return self._get_lesson(course_id=course.id, slug=lesson_slug).first()

    def create_lesson(
        self,
        user_id: int,
        course_slug: str,
        lesson_data: LessonCreate
    ) -> Lesson:
        course = self._get_course(slug=course_slug).first()
        if user_id != course.user_id:
            raise HTTP403Exception()
        lesson = tables.Lesson(**lesson_data.dict(),
                               course_id=course.id, user_id=user_id)

        self.session.add(lesson)
        self.session.commit()

        return lesson

    def edit_lesson(
        self,
        user_id: int,
        course_slug: str,
        lesson_slug: str,
        lesson_data: LessonUpdate
    ) -> Lesson:
        course = self._get_course(slug=course_slug).first()
        lesson = self._get_lesson(
            course_id=course.id, slug=lesson_slug).first()

        if user_id != lesson.user_id:
            raise HTTP403Exception()

        if not lesson:
            raise HTTP404Exception()

        for field, value in lesson_data:
            setattr(lesson, field, value)

        self.session.commit()

        return lesson

    def delete_lesson(self, id: int, user_id: int):
        lesson = self._get_lesson(id=id)

        if lesson.first() is None:
            raise HTTP404Exception()

        if user_id != lesson.first().user_id:
            raise HTTP403Exception()

        lesson.delete(synchronize_session=False)
        self.session.commit()
