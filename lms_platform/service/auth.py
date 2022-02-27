from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.auth import Token, User, UserCreate
from ..service.profile import ProfileService
from ..settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/auth/sign-in')


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    return AuthService.validate_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

    @classmethod
    def validate_token(cls, token: str) -> User:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[
                                 settings.algorithm])
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.from_orm(user)

        now = datetime.utcnow()

        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(seconds=settings.access_token_expire_minutes),
            'sub': str(user_data.id),
            'user': user_data.dict()
        }
        token = jwt.encode(payload, settings.secret_key,
                           algorithm=settings.algorithm)

        return Token(access_token=token)

    def __init__(self, session: Session = Depends(get_session), profile_service: ProfileService = Depends()):
        self.session = session
        self.profile_service = profile_service

    def register_new_user(self, user_data: UserCreate) -> Token:
        user = tables.User(
            username=user_data.username,
            email=user_data.email,
            password=self.hash_password(user_data.password),
            role=user_data.role
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={
                'WWW-Authenticate': "Bearer"
            }
        )
        user = self.session.query(tables.User).filter(
            tables.User.username == username).first()

        if not user:
            raise exception

        if not self.verify_password(password, user.password):
            raise exception

        return self.create_token(user)
