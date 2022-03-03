from fastapi import Depends
from sqlalchemy.orm import Session

from ..database import get_session


class CourseService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
