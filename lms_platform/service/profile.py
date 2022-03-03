import shutil
from typing import Any, Optional

from fastapi import Depends, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.profile import Profile, ProfileCreate, ProfileUpdate


class ProfileService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, user_id: int):
        profile = self.session.query(
            tables.Profile).filter_by(user_id=user_id).first()
        return profile

    def get_profile(self, user_id: int):
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found!',
        )
        profile = self._get(user_id)

        if not profile:
            raise exception

        return profile

    def create_profile(self, user_id: int, profile_data: ProfileCreate, file: Optional[Any] = None) -> Profile:
        exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Profile already exists!',
        )
        profile = self._get(user_id)

        if profile:
            raise exception

        if file:
            with open(profile_data.image, 'wb+') as file_obj:
                shutil.copyfileobj(file.file, file_obj)

        profile = tables.Profile(**profile_data.dict(), user_id=user_id)  # url

        self.session.add(profile)
        self.session.commit()

        return profile

    def edit_profile(self, user_id: int, profile_data: ProfileUpdate, file: Optional[Any] = None) -> Profile:
        exception = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Profile not found!',
        )
        profile = self._get(user_id)

        if not profile:
            raise exception

        if file:
            with open(profile_data.image, 'wb+') as file_obj:
                shutil.copyfileobj(file.file, file_obj)
        if not profile_data.image:
            profile_data.image = profile.image

        for field, value in profile_data:
            setattr(profile, field, value)  # profile.field = value

        self.session.commit()

        return profile
