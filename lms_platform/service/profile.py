from fastapi import Depends
from sqlalchemy.orm import Session

from .. import tables
from ..database import get_session
from ..models.profile import Profile, ProfileCreate


class ProfileService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_profile(self, user_id: int, profile_data: ProfileCreate) -> Profile:
        profile = tables.Profile(**profile_data.dict(), user_id=user_id)

        self.session.add(profile)
        self.session.commit()

        return profile
