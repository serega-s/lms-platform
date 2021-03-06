from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from ..models.auth import Token, User, UserCreate
from ..service.auth import AuthService, get_current_user

router = APIRouter(
    prefix='/auth',
    tags=['users']
)


@router.get('/user', response_model=User)
def get_user(user: User = Depends(get_current_user)):
    return user


@router.post('/sign-up', response_model=Token)
def sign_up(
    user_data: UserCreate,
    service: AuthService = Depends()
):
    return service.register_new_user(user_data)


@router.post('/sign-in', response_model=Token)
def sign_in(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends()
):
    return service.authenticate_user(form_data.username, form_data.password)


@router.delete('/user', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user: User = Depends(get_current_user), service: AuthService = Depends()):
    return service.delete_user(user.id)
