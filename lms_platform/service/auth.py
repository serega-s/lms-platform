from datetime import datetime, timedelta, timezone

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.auth import Token, User, UserCreate
from ..settings import settings
from ..statuses.exceptions import (HTTP401Exception, HTTP404Exception,
                                   HTTP409Exception)

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
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[
                                 settings.algorithm])
        except JWTError as e:
            raise HTTP401Exception() from e

        user_data = payload.get('user')

        try:
            user = User.parse_obj(user_data)
        except ValidationError as exc:
            raise HTTP401Exception() from exc

        return user

    @classmethod
    def create_token(cls, user: tables.User) -> Token:
        user_data = User.from_orm(user)

        now = datetime.now(timezone.utc)

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

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def register_new_user(self, user_data: UserCreate) -> Token:
        user = self.session.query(tables.User).filter(
            tables.User.email == user_data.email).first()
        if user:
            raise HTTP409Exception()

        user = tables.User(
            email=user_data.email,
            password=self.hash_password(user_data.password),
            role=user_data.role
        )

        self.session.add(user)
        self.session.commit()

        return self.create_token(user)

    def authenticate_user(self, email: str, password: str) -> Token:  # username
        user = self.session.query(tables.User).filter(
            tables.User.email == email).first()

        if not user:
            raise HTTP401Exception()

        if not self.verify_password(password, user.password):
            raise HTTP401Exception()

        return self.create_token(user)

    def delete_user(self, user_id: int):
        user = self.session.query(tables.User).filter(
            tables.User.id == user_id)

        if user.first() is None:
            raise HTTP404Exception()

        user.delete()

        self.session.commit()
