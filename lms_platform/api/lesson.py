from fastapi import APIRouter

router = APIRouter(
    prefix='/lessons',
    tags=['lessons']
)


@router.post('/{course_slug}')
def create_lesson(course_slug: str):
    ...


@router.get('/{course_slug}/{lesson_slug}')
def get_lesson(course_slug: str, lesson_slug: str):
    ...


@router.patch('/{course_slug}/{lesson_slug}')
def edit_lesson(course_slug: str, lesson_slug: str):
    ...


@router.delete('/{id}')
def delete_lesson(id: int):
    ...
