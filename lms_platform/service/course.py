from fastapi import UploadFile, Depends
from sqlalchemy.orm import Session

from ..database import get_session

class CourseService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def create_course(self, file: UploadFile):
        ...

    def create_lesson(self, ):
        ...