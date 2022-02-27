from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.profile import Profile, ProfileCreate


class ProfileService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_profile(self, user_id: int, profile_data: ProfileCreate) -> Profile:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Profile already exists!',
        )
        profile = self.session.query(
            tables.Profile).filter_by(user_id=user_id).first()
            
        if profile:
            raise exception

        profile = tables.Profile(**profile_data.dict(), user_id=user_id)

        self.session.add(profile)
        self.session.commit()

        return profile
