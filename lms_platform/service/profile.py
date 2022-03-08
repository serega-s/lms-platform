import shutil
from typing import Any, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.profile import Profile, ProfileCreate, ProfileUpdate
from ..statuses.exceptions import HTTP404Exception, HTTP409Exception


class ProfileService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get_profile(self, user_id: int):
        profile = self.session.query(
            tables.Profile).filter_by(user_id=user_id).first()
        return profile

    def get_profile(self, user_id: int) -> Profile:
        profile = self._get_profile(user_id)

        if not profile:
            raise HTTP404Exception()

        return profile

    def create_profile(
        self,
        user_id: int,
        profile_data: ProfileCreate,
        file: Optional[Any] = None
    ) -> Profile:
        profile = self._get_profile(user_id)

        if profile:
            raise HTTP409Exception()

        if file:
            with open(profile_data.image, 'wb+') as file_obj:
                shutil.copyfileobj(file.file, file_obj)

        profile = tables.Profile(**profile_data.dict(), user_id=user_id)  # url

        self.session.add(profile)
        self.session.commit()

        return profile

    def edit_profile(
        self,
        user_id: int,
        profile_data: ProfileUpdate,
        file: Optional[Any] = None
    ) -> Profile:
        profile = self._get_profile(user_id)

        if not profile:
            raise HTTP404Exception()

        if file:
            with open(profile_data.image, 'wb+') as file_obj:
                shutil.copyfileobj(file.file, file_obj)
        if not profile_data.image:
            profile_data.image = profile.image

        for field, value in profile_data:
            setattr(profile, field, value)

        self.session.commit()

        return profile
