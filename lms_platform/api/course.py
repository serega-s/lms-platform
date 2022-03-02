from fastapi import APIRouter

router = APIRouter(
    prefix='/courses',
    tags=['courses']
)


@router.post('/')
def create_course():
    ...


@router.get('/{slug}')
def get_course(slug: str):
    ...


@router.patch('/{slug}')
def edit_course(slug: str):
    ...


@router.delete('/{id}')
def delete_course(id: int):
    ...
