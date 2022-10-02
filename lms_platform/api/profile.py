from email.mime import image
from typing import Optional

from fastapi import APIRouter, Depends, File, UploadFile
from lms_platform.utils import build_image_url

from ..models.auth import User
from ..models.profile import Profile, ProfileCreate, ProfileUpdate
from ..service.auth import get_current_user
from ..service.profile import ProfileService

router = APIRouter(
    prefix='/profiles',
    tags=['profiles']
)


@router.get('/', response_model=Profile)
def get_profile(user: User = Depends(get_current_user), service: ProfileService = Depends()):
    return service.get_profile(user.id)


@router.post('/', response_model=Profile)
def create_profile(
    full_name: str,
    bio: str,
    phone_number: str,
    file: Optional[UploadFile] = File(default=None),
    user: User = Depends(get_current_user),
    service: ProfileService = Depends(),
):
    profile_obj = {
        'full_name': full_name,
        'bio': bio,
        'phone_number': phone_number
    }

    if file:
        img_url = build_image_url(f'static/{user.id}/profile/', file)

        profile_obj |= {'image': img_url}

    profile_data = ProfileCreate.parse_obj(profile_obj)

    return service.create_profile(user.id, profile_data, file)


@router.patch('/', response_model=Profile)
def edit_profile(
    full_name: str,
    bio: str,
    phone_number: str,
    file: Optional[UploadFile] = File(default=None),
    user: User = Depends(get_current_user),
    service: ProfileService = Depends(),
):
    profile_obj = {
        'full_name': full_name,
        'bio': bio,
        'phone_number': phone_number
    }

    if file:
        img_url = build_image_url(f'static/{user.id}/profile/', file)

        profile_obj |= {'image': img_url}

    profile_data = ProfileUpdate.parse_obj(profile_obj)

    return service.edit_profile(user.id, profile_data, file)
