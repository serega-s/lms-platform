from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile, status
from slugify import slugify

from ..models.auth import User
from ..models.course import Course, CourseCreate
from ..service.auth import get_current_user
from ..service.course import CourseService
from ..utils import static_image_url

router = APIRouter(
    prefix='/courses',
    tags=['courses']
)


@router.get('/', response_model=list[Course])
def get_courses(
    service: CourseService = Depends()
):
    return service.get_courses()


@router.post('/', response_model=Course)
def create_course(
    title: str,
    short_description: str,
    description: str,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    service: CourseService = Depends()
):
    img_url = static_image_url(f'static/{user.id}/course/', file)
    slugified_title = slugify(title) + '-' + str(datetime.utcnow())

    course_obj = {
        'title': title,
        'slug': slugified_title,
        'short_description': short_description,
        'description': description,
        'image': img_url
    }
    course_data = CourseCreate.parse_obj(course_obj)

    return service.create_course(user.id, course_data, file)


@router.get('/{slug}', response_model=Course)
def get_course(
    slug: str,
    service: CourseService = Depends()
):
    return service.get_course(slug)


@router.patch('/{slug}', response_model=Course)
def edit_course(
    slug: str,
    title: str,
    short_description: str,
    description: str,
    file: Optional[UploadFile] = File(default=None),
    user: User = Depends(get_current_user),
    service: CourseService = Depends()
):
    slugified_title = slugify(title) + '-' + str(datetime.utcnow())
    course_obj = {
        'title': title,
        'slug': slugified_title,
        'short_description': short_description,
        'description': description,
    }

    if file:
        img_url = static_image_url(f'static/{user.id}/course/', file)
        course_obj.update(image=img_url)

    course_data = CourseCreate.parse_obj(course_obj)

    return service.edit_course(user.id, slug, course_data)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_course(
    id: int,
    user: User = Depends(get_current_user),
    service: CourseService = Depends()
):
    return service.delete_course(id, user.id)
