from typing import Optional

from fastapi import APIRouter, Depends, status
from slugify import slugify

from ..models.auth import User
from ..models.lesson import Lesson, LessonCreate
from ..service.auth import get_current_user
from ..service.lesson import LessonService

router = APIRouter(
    prefix='/lessons',
    tags=['lessons'],
)


@router.post('/{course_slug}/', response_model=Lesson)
def create_lesson(
    course_slug: str,
    title: str,
    short_description: str,
    description: str,
    draft: Optional[bool] = True,
    user: User = Depends(get_current_user),
    service: LessonService = Depends()
):
    slugified_title = slugify(title)

    lesson_obj = {
        'title': title,
        'slug': slugified_title,
        'short_description': short_description,
        'description': description,
        'draft': draft,
    }
    lesson_data = LessonCreate.parse_obj(lesson_obj)

    return service.create_lesson(user.id, course_slug, lesson_data)


@router.get('/{course_slug}/{lesson_slug}', response_model=Lesson)
def get_lesson(
    course_slug: str,
    lesson_slug: str,
    service: LessonService = Depends()
):
    return service.get_lesson(course_slug, lesson_slug)


@router.patch('/{course_slug}/{lesson_slug}', response_model=Lesson)
def edit_lesson(
    course_slug: str,
    lesson_slug: str,
    title: str,
    short_description: str,
    description: str,
    draft: Optional[bool] = True,
    user: User = Depends(get_current_user),
    service: LessonService = Depends()
):
    slugified_title = slugify(title)

    lesson_obj = {
        'title': title,
        'slug': slugified_title,
        'short_description': short_description,
        'description': description,
        'draft': draft,
    }
    lesson_data = LessonCreate.parse_obj(lesson_obj)

    return service.edit_lesson(user.id, course_slug, lesson_slug, lesson_data)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_lesson(
    id: int,
    service: LessonService = Depends(),
    user: User = Depends(get_current_user)
    ):
    return service.delete_lesson(id, user.id)
