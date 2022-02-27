from fastapi import APIRouter, Depends

from ..models.auth import User
from ..models.profile import ProfileCreate
from ..service.auth import get_current_user
from ..service.profile import ProfileService

router = APIRouter(
    prefix='/profiles',
    tags=['profiles']
)


@router.post('/create-profile')
def create_profile(
    profile_data: ProfileCreate,
    user: User = Depends(get_current_user),
    service: ProfileService = Depends(),
):
    return service.create_profile(user.id, profile_data)
