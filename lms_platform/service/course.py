import shutil
from typing import Any, Optional

from fastapi import Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.course import Course, CourseCreate, CourseUpdate


class CourseService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, id: Optional[int] = None, slug: Optional[str] = None):
        course = self.session.query(tables.Course)
        if id:
            course = course.filter_by(id=id)
        elif slug:
            course = course.filter_by(slug=slug)

        return course

    def get_course(self, slug: str) -> Course:
        course = self._get(slug=slug).first()

        return course

    def get_courses(self) -> list[Course]:
        courses = self.session.query(tables.Course).all()

        return courses

    def create_course(self, user_id: int, course_data: CourseCreate, file: Any) -> Course:
        with open(course_data.image, 'wb+') as file_obj:
            shutil.copyfileobj(file.file, file_obj)

        course = tables.Course(**course_data.dict(), user_id=user_id) 

        self.session.add(course)
        self.session.commit()

        return course

    def edit_course(self, user_id: int, id: int, course_data: CourseUpdate, file: Optional[Any] = None) -> Course:
        course = self._get(id=id).first()

        if user_id != course.user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='Wrong object owner')

        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Course not found!')

        if file:
            with open(course_data.image, 'wb+') as file_obj:
                shutil.copyfileobj(file.file, file_obj)
        if not course_data.image:
            course_data.image = course.image

        for field, value in course_data:
            setattr(course, field, value)

        self.session.commit()

        return course

    def delete_course(self, id: int, user_id: int):
        course = self._get(id=id)

        if course.first() is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Course not found!')

        if user_id != course.first().user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='Wrong object owner')

        course.delete(synchronize_session=False)
        self.session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
