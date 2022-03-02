import shutil
from typing import Any

from fastapi import Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.profile import Profile, ProfileCreate


class ProfileService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_profile(self, user_id: int, profile_data: ProfileCreate, file: Any) -> Profile:
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Profile already exists!',
        )
        profile = self.session.query(
            tables.Profile).filter_by(user_id=user_id).first()

        if profile:
            raise exception

        with open(profile_data.url, 'wb+') as file_obj:
            shutil.copyfileobj(file, file_obj)
        profile = tables.Profile(**profile_data.dict(), user_id=user_id)  # url

        self.session.add(profile)
        self.session.commit()

        return profile
